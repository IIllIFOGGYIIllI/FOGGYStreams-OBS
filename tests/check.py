from pathlib import Path
import json, re
root = Path(__file__).resolve().parents[1]
html = (root/'gta-vi/index.html').read_text()
js = re.search(r'<script>([\s\S]*?)</script>', html).group(1)
Path('/tmp/gta-vi-overlay.js').write_text(js)
assert 'Date.now()+600000' in js
assert 'brb:["Taking A Break","Be Right","Back","Grab A Drink — We’ll Be Back On The Streets Shortly",""]' in js
d = json.loads((root/'downloads/FOGGYStreams_Vice_City_OBS_v1.4.json').read_text())
sources = {s['uuid']:s for s in d['sources']}
assert len(sources)==29 and len(d['scene_order'])==12
for s in sources.values():
    if s['id']=='browser_source':
        assert s['settings']['url'].startswith('https://iillifoggyiilli.github.io/FOGGYStreams-OBS/gta-vi/index.html?scene=')
        assert s['settings']['width']==1920 and s['settings']['height']==1080
        mode=s['settings']['url'].split('scene=')[1]
        assert mode in js
    else:
        for i in s['settings']['items']:
            assert i['source_uuid'] in sources and sources[i['source_uuid']]['name']==i['name']
print('Overlay pack validation passed')
