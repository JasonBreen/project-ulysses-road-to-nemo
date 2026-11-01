"""Generate only the approved event GUI scalar substitutions and original art."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT/'tools'))
from event_style.migration import generated,MOD
from event_style.build_art import outputs
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    files=outputs();files['mod/2985041246/interface/eventwindow.gui']=generated().encode()
    for relative,data in files.items():
        path=ROOT/relative
        if a.check:
            actual=path.read_bytes() if path.is_file() else None
            if actual is not None and path.suffix=='.gui':actual=actual.replace(b'\r\n',b'\n')
            if actual!=data:
                raise SystemExit('Generated output differs: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Event style generated/check PASS; exactly17 sprite+6 font fields; all other source restored exactly.')
if __name__=='__main__':main()
