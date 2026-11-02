"""Durable invocation order and immutable subprocess evidence archives.

SQLite allocates a monotonic sequence within this checkout. Output-folder names
and wall clocks never determine which execution supersedes an earlier attempt.
This is local evidence accounting, not protection against deliberate tampering.
"""
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import uuid


def write_json(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')


def begin(root,output,names,source):
    root=Path(root);runtime=root/'runtime-output/fato-south-belka'
    relative_output=Path(output).resolve().relative_to(root.resolve()).as_posix()
    runtime.mkdir(parents=True,exist_ok=True)
    identity=uuid.uuid4().hex
    with closing(sqlite3.connect(runtime/'invocations.sqlite3',timeout=30))as database,database:
        database.execute('CREATE TABLE IF NOT EXISTS invocations (sequence INTEGER PRIMARY KEY AUTOINCREMENT, identity TEXT UNIQUE NOT NULL)')
        sequence=database.execute('INSERT INTO invocations(identity) VALUES (?)',(identity,)).lastrowid
    directory=runtime/'invocations'/f'{sequence:08d}-{identity}'
    directory.mkdir(parents=True)
    invocation=dict(schema=1,sequence=sequence,identity=identity,checks=list(names),source_inputs=source,
                    output_folder=relative_output)
    write_json(directory/'invocation.json',invocation)
    return directory,invocation


def finish(directory,invocation,report,output):
    directory=Path(directory);output=Path(output)
    report=json.loads(json.dumps(report));report['invocation']=invocation
    if {r['name']for r in report['checks']}!=set(invocation['checks']):
        raise ValueError('Completed check set differs from invocation')
    for row in report['checks']:
        data=(output/(row['name']+'.txt')).read_bytes()
        with (directory/(row['name']+'.txt')).open('xb')as target:target.write(data)
        row['log_sha256']=hashlib.sha256(data).hexdigest()
    if (directory/'checks.json').exists():raise ValueError('Invocation has already finished')
    write_json(directory/'checks.json',report)
    return report


def read_current(root,current):
    root=Path(root);base=root/'runtime-output/fato-south-belka/invocations'
    manifests=list(base.glob('*/invocation.json'))
    if not manifests:raise ValueError('No durable invocations; legacy folder reports cannot certify current source')
    entries=[];seen=set()
    for path in manifests:
        invocation=json.loads(path.read_text(encoding='utf-8'))
        order=invocation.get('sequence')
        if type(order)is not int or order<1 or order in seen:raise ValueError('Invalid or duplicate invocation sequence')
        seen.add(order);entries.append((order,path.parent,invocation))
    latest={};attempts=[]
    for _,directory,invocation in sorted(entries):
        report_path=directory/'checks.json'
        report=json.loads(report_path.read_text(encoding='utf-8'))if report_path.exists()else None
        if report and (report.get('invocation')!=invocation or report.get('source_inputs')!=invocation.get('source_inputs')):
            raise ValueError('Invocation and tested-source metadata disagree')
        rows=report['checks']if report else[dict(name=name,exit_code=None)for name in invocation['checks']]
        if len(rows)!=len(invocation['checks'])or {r['name']for r in rows}!=set(invocation['checks']):raise ValueError('Archived invocation check set differs')
        for row in rows:
            item=dict(row,invocation=invocation,source_inputs=invocation.get('source_inputs'),
                      archived_report=report_path.relative_to(root).as_posix(),
                      archived_log=(directory/(row['name']+'.txt')).relative_to(root).as_posix())
            if row['name']in latest:attempts.append(latest[row['name']])
            latest[row['name']]=item
    for name,row in latest.items():
        if row['exit_code']is None:raise ValueError('Latest invocation is incomplete: '+name)
        if row['exit_code']!=0:raise ValueError('Latest invocation failed: '+name)
        if row['source_inputs']!=current:raise ValueError('Latest check tested different or unpinned source: '+name)
        data=(root/row['archived_log']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=row.get('log_sha256'):raise ValueError('Archived log changed: '+name)
    return list(latest.values()),attempts
