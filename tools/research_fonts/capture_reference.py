"""Read-only installed font metadata and effective ownership evidence; no pixels."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/overhaul')]
from research_fonts import build
from audit_consumers import Audit


def capture(engine):
    primary=build.PRIMARY
    try:
        with tempfile.TemporaryDirectory()as temporary:
            build.PRIMARY=Path(temporary)/'primary.json';build.capture(engine)
            fresh=json.loads(build.PRIMARY.read_text())
            if fresh!=json.loads(primary.read_text()):raise ValueError('Installed default English font contract changed')
    finally:build.PRIMARY=primary
    profile=json.loads((ROOT/'tools/research_fonts/audit_profile.json').read_text())
    report=Audit(build.MOD,engine,profile).run(['countrydecisionview.gui','countrytechtreeview.gui'])
    fonts=[r for r in report['gate_covered_screens']['countrytechtreeview.gui']['consumers']if r['family']=='font']
    grouped={}
    for row in fonts:
        if row['name']not in grouped:grouped[row['name']]={**row,'assignments':0}
        grouped[row['name']]['assignments']+=1
    result=dict(schema=1,coverage='Actual effective research screen mod-ownership closure and exact-hash-authored font subset; not the completed presentation gate or native acceptance',
        engine_version=fresh['version'],source_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        profile='tools/research_fonts/audit_profile.json',primary_contract_matches_installed=True,
        dlc_archive_coverage=report['dlc_archive_coverage'],gate_covered_screens={},
        font_assignments=len(fonts),authored_font_consumers=[grouped[k]for k in sorted(grouped)],
        native_acceptance=False,global_classification_summary=report['classification_summary'],
        completed_presentation_gate=report['completed_presentation_gate'])
    for name,row in report['gate_covered_screens'].items():
        result['gate_covered_screens'][name]=dict(consumer_count=len(row['consumers']),failures=row['failures'])
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/evidence/research-fonts/research-dependencies.json');args=parser.parse_args()
    result=capture(args.engine)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    rows=result['authored_font_consumers']
    if len(rows)!=14 or any(row['classification']!='authored'for row in rows):raise SystemExit('Effective font provenance closure failed; evidence retained')
    if any(row['failures']for row in result['gate_covered_screens'].values()):raise SystemExit('Effective screen ownership failed; evidence retained')
    print('Effective font aliases:14 authored; primary contract unchanged; research/decision ownership failures:0; native untested')
