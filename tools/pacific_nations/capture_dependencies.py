"""Owned effective art closure; full inherited presentation debt remains visible."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/overhaul')]
from audit_consumers import Audit,DEFAULT_MOD
from capture_dependency_evidence import compact
from pacific_nations.model import countries


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--tag',required=True,choices=('OSE','YUK'));parser.add_argument('--reference',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    module=next(m for m in countries()if m.TAG==args.tag);profile=json.loads((HERE/('audit_'+args.tag+'.json')).read_text());assets=json.loads((HERE/('assets_'+args.tag+'.json')).read_text())['assets']
    report=Audit(DEFAULT_MOD,args.reference,profile).run(['countrydecisionview.gui','ac_macro_economy.gui'],True)
    own=[row for row in report['consumers']if row['consumer'].endswith('/ac_snc_'+args.tag.lower()+'.txt')]
    expected=dict(Counter({'focus':sum(len(b.steps)for b in module.BRANCHES),'idea':sum(a['role']=='idea'for a in assets),'decision':sum(a['role']=='decision row'for a in assets),'decision_category':1,'event_picture':14}))
    actual=dict(Counter(row['consumer_family']for row in own));failures=[row for row in own if row['classification']!='authored']
    if actual!=expected:failures.append(dict(problem='actual owned inventory differs',expected=expected,actual=actual))
    screen={name:len(value['failures'])for name,value in report['gate_covered_screens'].items()if name in('countrydecisionview.gui','ac_macro_economy.gui')}
    summary=dict(country=args.tag,owned_references=len(own),authored_resources=len(assets),by_family=actual,owned_failures=failures,owned_scope_passed=not failures,selected_screen_ownership_failures=screen,
        full_presentation_passed=report['completed_presentation_gate']['passed'],full_presentation_failures=len(report['completed_presentation_gate']['failures']),parse_failures=len(report['parse_failures']),native_acceptance=False,
        scope='Exact original national resources only; selected-screen ownership and failing full-conversion graph remain separate')
    output=compact(report);output['national_continuation_scope']=summary;args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,indent=2));raise SystemExit(bool(failures)or any(screen.values()))
