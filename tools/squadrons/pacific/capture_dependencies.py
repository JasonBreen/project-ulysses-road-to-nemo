"""Exact new-resource ownership; inherited global backlog remains explicit."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from config import HERE,ROOT,MOD,campaigns
sys.path[:0]=[str(ROOT/'tools/overhaul'),str(ROOT/'tools')]
from audit_consumers import Audit,DEFAULT_MOD
from capture_dependency_evidence import compact


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--engine',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    profile=json.loads((ROOT/'tools/circum_pacific/audit.json').read_text());profile['name']='Pacific personal stories: exact authored current resources; explicit base-only static profile'
    assets=json.loads((HERE/'assets.json').read_text())['assets']
    profile['provenance'] += [dict(provider='mod',path=r['file'],sha256=r['sha256'],classification='authored',reason='Exact independently reviewed original master or editable procedural composition',evidence='tools/squadrons/pacific/assets.json; tools/squadrons/pacific_art/plan.json')for r in assets]
    profile_path=HERE/'audit.json';profile_path.write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8',newline='\n')
    report=Audit(DEFAULT_MOD,a.engine,profile).run(['countrydecisionview.gui','ac_macro_economy.gui'],True)
    rows=[r for r in report['consumers']if r['consumer'].endswith('/ac_squadrons_pacific.txt')]
    n=len(campaigns());expected=dict(decision=27*n,decision_category=n,idea=1,event_picture=47*n)
    actual=dict(Counter(r['consumer_family']for r in rows));failures=[r for r in rows if r['classification']!='authored']
    if expected!=actual:failures.append(dict(problem='Actual personal story consumers differ',expected=expected,actual=actual))
    screens={name:r['failure_count']if'failure_count'in r else len(r['failures'])for name,r in report['gate_covered_screens'].items()if name in('countrydecisionview.gui','ac_macro_economy.gui')}
    summary=dict(expected=expected,actual=actual,resources=len(assets),runtime_references=len(rows),failures=failures,
        portrait_exports=4*n,portrait_export_scope='Explicit156x210 personal exports have no national leader consumer; castcards use200x160',
        selected_screens=screens,native_acceptance=False)
    result=compact(report);result['pacific_stories_scope']=summary;a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,indent=2));raise SystemExit(bool(failures)or any(screens.values()))
