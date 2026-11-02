"""Reproduce a searchable caption/provenance comparison, never a native map."""
import argparse
import html
import json
from build import ROOT,HERE,all_changes,build

OUTPUT=ROOT/'docs/evidence/regional-labels/caption-review.html'


def render():
    data=json.loads((HERE/'labels.json').read_text());build(data)
    rows=[]
    for item in all_changes(data):
        kind='state' if 'province' not in item and 'state' in item else 'locality' if 'province' in item else 'institution'
        old=item['old'] if item['old'] else '(missing or empty English caption)'
        values=[kind,item.get('owner','SAP'),item['key'],old,item['value'],item['source_layer']]
        rows.append('<tr>'+''.join('<td>'+html.escape(str(value))+'</td>' for value in values)+'</tr>')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Regional caption source review</title>
<style>body{background:#081621;color:#daedf2;font:16px system-ui;padding:24px}h1{color:#5dd0df}input{background:#0d202e;color:#daedf2;border:1px solid #5dd0df;padding:10px;width:90%;max-width:700px}table{border-collapse:collapse;width:100%;margin-top:18px}td,th{text-align:left;border-bottom:1px solid #2d5568;padding:8px}th{color:#5dd0df}td:nth-child(3){font:13px monospace}</style>
<h1>Regional captions: source comparison</h1><p>206 state captions, 37 existing locality captions and four inherited school titles. Every new name is provisional gameplay presentation. This table is not a rendered game map and establishes no canonical regional location. Protected states 171/607 and physical geography remain unchanged.</p>
<label>Filter by country, key or caption <input id="filter" type="search"></label>
<table><thead><tr><th>Kind</th><th>Owner</th><th>Key</th><th>Inherited caption</th><th>Replacement</th><th>Source layer</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table>
<script>document.getElementById('filter').addEventListener('input',e=>{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))});</script></html>
'''


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();text=render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8')!=text:raise SystemExit('Stale caption comparison')
    else:OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_text(text,encoding='utf-8',newline='\n')
    print('247 source-caption comparisons verified; no native rendering claim.')
