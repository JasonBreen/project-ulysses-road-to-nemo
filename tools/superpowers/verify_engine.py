"""Read-only SP96 primary contract check using the shared metadata verifier."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reconstruction import verify_engine
verify_engine.HERE=Path(__file__).resolve().parent

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reference',required=True,type=Path);args=parser.parse_args()
    contract=json.loads((verify_engine.HERE/'engine_contracts.json').read_text())
    for row in contract['presentation_scripting']:
        source=args.reference/row['source'][len('engine://'):];data=source.read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['sha256'],row['source']
        assert row['name']in data.decode('utf-8-sig').splitlines()[row['line']-1],row['name']
    verify_engine.main()
    print('PASS:4 presentation scripting forms independently present in primary national-focus/decision files; native rendering untested.')
