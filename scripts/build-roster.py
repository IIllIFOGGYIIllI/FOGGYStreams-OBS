"""Index public roster artwork links. No image binaries are copied."""
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
import re, json, sys
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
def main():
    # Fail soft: a blocked source must not prevent the overlay deployment.
    result={}
    for url,base in ((ROSTER,BASE),(OFFICIAL,WWE)):
        try:
            records=parse(fetch(url),base)
            print(f"{url}: indexed {len(records)} portrait links")
            for n,u in records.items():result.setdefault(n,u)
        except Exception as exc:print(f"::warning::Roster artwork source unavailable: {exc}")
    target=Path("dist/wwe-2k26/roster-generated.js")
    if result:
        target.write_text("const GENERATED_ROSTER = "+json.dumps(result,ensure_ascii=False)+";\n",encoding="utf-8")
    else:print("::warning::No new artwork indexed; built-in portraits remain available.")
    print(f"Imported {len(result)} artwork links")
if __name__=="__main__":main()
