"""Earliest legal focus schedules, not native AI or natural playtest evidence."""
import argparse
import copy
from datetime import date
from itertools import product
import json
import hashlib
import inspect
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from content import FOCUSES
import build
# Preload this owner's distinct scene table before the inherited parser paths.
import narrative
from owner_harness import baseline

def schedules():
    base=baseline('disabled');out=[]
    for tag,start in [('FAT',(1991,1,1)),('SBK',(1995,6,21))]:
        rows=[r for r in FOCUSES if r.tag==tag];pairs=[(r.suffix,r.exclusive)for r in rows if r.exclusive and r.suffix<r.exclusive]
        for choices in product((0,1),repeat=len(pairs)):
            w=copy.deepcopy(base);w.today=date(*start).toordinal();c=w.countries[tag];exclude={pair[1-pick]for pair,pick in zip(pairs,choices)};pending=[r for r in rows if r.suffix not in exclude];records=[];wait=0;longest=0
            while pending:
                candidates=[]
                for r in pending:
                    body=w.focuses[r.id]
                    if not w.trigger(__import__('owner_harness').get(body,'available'),c):continue
                    if any(not any(tag+'_nat_'+s in c.completed for s in group)for group in r.requirements):continue
                    candidates.append(r)
                if not candidates:
                    next_dates=[]
                    for r in pending:
                        bound=build.earliest(r)
                        if bound:
                            ordinal=date(*map(int,bound.split('.'))).toordinal()+1
                            if ordinal>w.today:next_dates.append(ordinal)
                    if not next_dates:raise ValueError('Non-calendar prerequisite or availability deadlock: '+tag)
                    delta=min(next_dates)-w.today;w.advance(delta);wait+=delta
                    if w.today>date(2020,12,31).toordinal():raise ValueError('Focus schedule stranded: '+tag+' '+str([r.id for r in pending]))
                    continue
                r=candidates[0];longest=max(longest,wait);began=w.today;w.advance(r.cost*7)
                if not w.complete(r.id,tag):raise ValueError('Actual focus completion failed: '+r.id)
                w.run('ac_fsb_narrative_tick',tag);pending.remove(r)
                records.append(dict(id=r.id,started=date.fromordinal(began).isoformat(),completed=date.fromordinal(w.today).isoformat(),calendar_wait_before=wait,focus_days=r.cost*7));wait=0
            out.append(dict(tag=tag,policy_choices=[pair[pick]for pair,pick in zip(pairs,choices)],selected_focuses=len(records),focus_days=sum(r['focus_days']for r in records),completed=records[-1]['completed'],longest_calendar_wait_days=longest,focuses=records))
    return dict(schema=1,evidence='Earliest legal source DAG/calendar schedules in an offline disabled-fiscal fixture; no console-completed prerequisites, no foreign consent required. This is not AI selection, player behaviour, natural progression or native timing acceptance.',native='paused',
        content_sha256=hashlib.sha256((HERE/'content.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        calendar_owner_sha256=hashlib.sha256(inspect.getsource(build.earliest).replace('\r\n','\n').encode()).hexdigest(),paths=out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();text=json.dumps(schedules(),indent=2)+'\n';path=HERE/'pacing.json'
    if a.check:
        if not path.exists()or path.read_text()!=text:raise SystemExit('Focus pacing schedules differ')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('24 legal exclusive-path focus schedules; source calendar only, native AI pending')
