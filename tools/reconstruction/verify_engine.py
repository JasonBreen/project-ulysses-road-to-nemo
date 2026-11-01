"""Read-only recapture check of the declared 1.19.4.1 primary contracts."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reference',required=True,type=Path);a=p.parse_args()
 contract=json.loads((HERE/'engine_contracts.json').read_text());checked=set()
 settings=json.loads((a.reference/'launcher-settings.json').read_text(encoding='utf-8-sig'))
 if settings['rawVersion']!=contract['version']:raise SystemExit('Primary version differs; reinspect before acceptance')
 def verify(uri,digest):
  assert uri.startswith('engine://')
  source=a.reference/uri[len('engine://'):];data=source.read_bytes()
  if hashlib.sha256(data).hexdigest()!=digest:raise SystemExit('Primary source changed; reinspect '+uri)
  checked.add(uri);return data.decode('utf-8-sig')
 for row in contract['modifiers']:
  source=verify(row['primary_national_idea_source'],row['source_sha256'])
  assert row['id']in source.splitlines()[row['line']-1],row['id']
 for row in contract['hook_sources']:verify(row['path'],row['sha256'])
 costs=contract['cost_fields'];source=verify(costs['source'],costs['sha256'])
 for field in costs['fields']:assert field in source,field
 print(f"PASS: {len(contract['modifiers'])} modifier uses, {len(contract['interruption_hooks'])} hook contracts and decision-cost fields; {len(checked)} primary files unchanged. Native semantics untested.")

if __name__=='__main__':main()
