"""Index public roster artwork links. No image binaries are copied."""
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
import re, json, sys, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
BASE = "https://www.thesmackdownhotel.com"
WWE = "https://www.wwe.com"
ROSTER = BASE + "/wwe2k26/roster/"
OFFICIAL = WWE + "/superstars"
def textname(s):
    s = re.sub(r"^\s*\d{2,3}\s+", "", s or "")
    s = re.sub(r"\s+NEW$", "", s, flags=re.I)
    return " ".join(s.split())
def fetch(url):
    req = Request(url, headers={"User-Agent":"Mozilla/5.0 (compatible; FOGGYStreams roster link index; contact via project repository)","Accept":"text/html"})
    with urlopen(req, timeout=20) as res:
        return res.read(9000000).decode("utf-8","replace")
def image(attrs, base):
    candidates=[]
    for k in ("data-src","data-lazy-src","data-original","src","data-srcset","srcset"):
        for v in (attrs.get(k) or "").split(","):
            v=v.strip().split(" ")[0]
            if not v: continue
            u=urljoin(base,v)
            parsed=urlparse(u)
            if parsed.scheme!="https": continue
            if parsed.hostname not in ("www.thesmackdownhotel.com","thesmackdownhotel.com","www.wwe.com","wwe.com"): continue
            low=parsed.path.lower()
            if not re.search(r"\.(png|webp|avif|jpe?g)$",low):continue
            if "placeholder" in low or "default" in low:continue
            if base==BASE and not any(x in low for x in ("roster","wrestlers","wwe2k")):continue
            if base==WWE and not any(x in low for x in ("profile","talent","superstar")):continue
            candidates.append(u)
    return candidates[0] if candidates else ""
class Cards(HTMLParser):
    def __init__(self,base):
        super().__init__(convert_charrefs=True)
        self.base=base;self.card=None;self.results={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a":
            path=urlparse(urljoin(self.base,a.get("href",""))).path
            pattern=r"^/roster/wwe2k26/[^/]+/?$" if self.base==BASE else r"^/superstars/[^/]+/?$"
            self.card={"name":a.get("title",""),"img":"","text":[]} if re.match(pattern,path) else None
        elif tag=="img" and self.card is not None:
            u=image(a,self.base)
            if u:
                self.card["img"]=u
                if a.get("alt"):self.card["name"]=a["alt"]
    def handle_data(self,data):
        if self.card is not None:self.card["text"].append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.card is not None:
            c=self.card;name=textname(c["name"] or " ".join(c["text"]))
            if c["img"] and 1<len(name)<=80 and name.lower() not in ("image","superstar","view all"):
                self.results[name]=c["img"]
            self.card=None
def parse(html,base):
    p=Cards(base);p.feed(html);return p.results
def valid_image(url):
    try:
        req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; FOGGYStreams roster verification)","Accept":"image/*","Range":"bytes=0-4095"})
        with urlopen(req,timeout=8) as res:
            ct=res.headers.get("Content-Type","").lower()
            head=res.read(4096)
            return ct.startswith("image/") and (head.startswith((b"\x89PNG",b"\xff\xd8\xff",b"RIFF",b"GIF8")) or b"ftypavif" in head[:32] or b"ftypavis" in head[:32])
    except Exception:return False

def roster_key(v):
    import unicodedata
    return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",v).encode("ascii","ignore").decode().lower()).strip()

def main():
    result={}
    expected=None
    source_error=""
    seed=json.loads(Path("wwe-2k26/roster-seed.json").read_text(encoding="utf-8"))
    cache=Path(".roster-cache/index.json")
    try:prior=json.loads(cache.read_text(encoding="utf-8"))
    except (OSError,ValueError):prior={}
    try:
        html=fetch(ROSTER)
        plain=re.sub(r"<[^>]*>"," ",html)
        m=re.search(r"\bALL\s*\(\s*(\d+)\s*\)",plain,re.I)
        expected=int(m[1]) if m else 512
        result=parse(html,BASE)
        print(f"Game roster source: {len(result)}/{expected} portrait links")
        if len(result)<expected:
            source_error="Source returned a partial roster"
            for name,url in prior.get("links",{}).items():result.setdefault(name,url)
    except Exception as exc:
        source_error=str(exc)
        result=prior.get("links",{})
        expected=prior.get("expected",512)
    game_count=len(result)
    keys={roster_key(n):n for n in seed}
    # Validate every imported link with real HTTP image content, without downloading full-size images.
    def check(item):
        name,url=item
        if valid_image(url):return name,url,True
        fallback=seed.get(keys.get(roster_key(name),""))
        if fallback and valid_image(fallback):return name,fallback,True
        return name,url,False
    with ThreadPoolExecutor(max_workers=8) as pool:checked=list(pool.map(check,result.items()))
    verified=sum(v for n,u,v in checked)
    # Preserve original source links even if a host temporarily blocks a build runner.
    # They are never described as verified. Browser onload provides an independent check.
    manifest={n:u for n,u,v in checked}
    missing=[n for n,u,v in checked if not v]
    required=["The Miz","Jeff Hardy","Chad Gable","Rey Fenix","Penta","Drew McIntyre"]
    with ThreadPoolExecutor(max_workers=6) as pool:required_status=dict(zip(required,pool.map(lambda n:valid_image(seed[n]),required)))
    report={"source":ROSTER,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"complete" if game_count==expected and verified==expected and not source_error and all(required_status.values()) else "incomplete","expected":expected,"indexed":game_count,"verified":verified,"missing":missing,"required_portraits":required_status,"source_error":source_error,"note":"Image HTTP content checks, not proof of exact in-game attire or browser display. Externally hosted artwork; seed portrait fallbacks are used where available."}
    target=Path("dist/wwe-2k26")
    target.mkdir(parents=True,exist_ok=True)
    (target/"roster-generated.js").write_text("const GENERATED_ROSTER = "+json.dumps(manifest,ensure_ascii=False)+";\nconst GENERATED_COVERAGE = "+json.dumps(report,ensure_ascii=False)+";\n",encoding="utf-8")
    (target/"roster-coverage.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_text(json.dumps({"expected":expected,"links":result},ensure_ascii=False),encoding="utf-8")
    print(f"ROSTER COVERAGE: {verified}/{expected} verified, {game_count} indexed, {len(missing)} unverified. Required: {required_status}")
    if report["status"]!="complete":print("::warning::Full artwork coverage is not verified; see roster-coverage.json")
    import os
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as out:
            out.write(f"## WWE 2K26 Artwork Coverage\n\nStatus: **{report['status']}**\n\nVerified {verified}/{expected}; indexed {game_count}.\n\nRequested portraits: {required_status}\n\nSource error: {source_error or 'None'}\n")
if __name__=="__main__":main()
