"""Read-only installed-reference graph for the exact original SP96 resources.

Packet-owned closure and requested screen ownership are separate from the full
completed-presentation gate, whose failing inherited backlog stays explicit.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/overhaul'))
from audit_consumers import Audit,DEFAULT_MOD
from capture_dependency_evidence import compact


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reference',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
 profile=json.loads((HERE/'audit_profile.json').read_text());audit=Audit(DEFAULT_MOD,a.reference,profile)
 requested=['countrydecisionview.gui','ac_macro_economy.gui']
 report=audit.run(requested,True)
 owned=[row for row in report['consumers']if row.get('consumer','').endswith('/ac_superpower_programmes.txt')]
 failures=[row for row in owned if row.get('classification')!='authored']
 expected={'focus':96,'idea':136,'decision':68,'decision_category':2,'event_picture':36}
 from collections import Counter
 actual=dict(Counter(r['consumer_family']for r in owned))
 if actual!=expected:failures.append(dict(status='owned_consumer_inventory_differs',expected=expected,actual=actual))
 screen_failures={k:len(report['gate_covered_screens'][k]['failures'])for k in requested}
 owned_summary=dict(evidence='Read-only effective textual graph, not native render/activation acceptance',captured_utc=datetime.now(timezone.utc).isoformat(),
   profile='tools/superpowers/audit_profile.json',profile_sha256=hashlib.sha256((HERE/'audit_profile.json').read_bytes()).hexdigest(),
   distinct_authored_textures=len(profile['provenance']),owned_consumer_references=len(owned),by_family=actual,
   owned_scope_passed=not failures,owned_failures=failures,selected_screen_ownership_failures=screen_failures,
   full_completed_presentation_passed=report['completed_presentation_gate']['passed'],
   full_completed_presentation_failures=len(report['completed_presentation_gate']['failures']),
   full_conversion_status='PASS only if full_completed_presentation_passed; owned-scope success never closes the inherited backlog',
   inherited_parse_failures=len(report['parse_failures']))
 report=compact(report);report['sp96_scope']=owned_summary
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(owned_summary,indent=2));raise SystemExit(bool(failures)or any(screen_failures.values()))

if __name__=='__main__':main()
