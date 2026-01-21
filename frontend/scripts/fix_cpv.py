import xml.etree.ElementTree as ET
from pathlib import Path
import json

src = Path(r'C:/Users/yanry/Downloads/cpv_2008_xml/cpv_2008.xml')
out = Path('frontend/public/cpv.json')

root = ET.parse(str(src)).getroot()
result = {}

for cpv in root.findall('CPV'):
    code = cpv.attrib.get('CODE')
    if not code:
        continue
    entry = {}
    for t in cpv.findall('TEXT'):
        lang = t.attrib.get('LANG')
        txt = (t.text or '').strip()
        if lang == 'EN':
            entry['en'] = txt
        elif lang == 'PL':
            entry['pl'] = txt
        elif lang in ('UA', 'UK'):
            entry['ua'] = txt
    result[code] = entry

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f'Wrote {len(result)} entries to {out}')

