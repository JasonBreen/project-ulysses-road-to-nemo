"""Collect only latest successful invocations against exact current source.

Original component receipts remain historical. Folder order, old exit codes and
newly computed payload hashes cannot turn them into current source acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify
from evidence_journal import read_current


def collect(root):
    root=Path(root);source=capture(root)
    checks,attempts=read_current(root,source)
    payload=hashlib.sha256()
    for path in sorted((root/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(root).as_posix().encode()+b'\0'+path.read_bytes())
    verify(source,root)
    return dict(schema=2,source_inputs=source,payload_sha256=payload.hexdigest(),
        payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw delivered mod bytes.',
        latest_checks=checks,superseded_attempts=attempts,native_acceptance=False,
        scope='Only listed exact-source subprocess invocations. Historical formatting/folder reports are not accepted or relabelled.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/evidence/fato-south-belka/current-source-receipts.json')
    args=parser.parse_args();receipt=collect(ROOT)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    # Deliver the immutable reports and every attempt's logs. Convenience
    # output folders may be reused without erasing a prior invocation.
    paths={r['archived_report']for r in receipt['latest_checks']+receipt['superseded_attempts']}
    paths|={str(Path(p).parent/'invocation.json')for p in paths}
    paths|={r['archived_log']for r in receipt['latest_checks']+receipt['superseded_attempts']if r['exit_code']is not None}
    for relative in sorted(paths):
        source=ROOT/relative
        if not source.exists():continue
        suffix=source.relative_to(ROOT/'runtime-output/fato-south-belka/invocations')
        destination=args.output.parent/'invocations'/suffix
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(source.read_bytes())
    for row in receipt['latest_checks']+receipt['superseded_attempts']:
        for field in ('archived_report','archived_log'):
            row[field]=str(args.output.parent.relative_to(ROOT)/'invocations'/Path(row[field]).relative_to('runtime-output/fato-south-belka/invocations')).replace('\\','/')
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(str(len(receipt['latest_checks']))+' exact-source current gates; earlier attempts retained; native paused')


if __name__=='__main__':main()
