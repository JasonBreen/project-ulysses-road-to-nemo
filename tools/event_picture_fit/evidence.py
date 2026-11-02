"""Fresh audit output and current failed/running receipts; no game execution."""
import json
from pathlib import Path
import shutil
import subprocess
import uuid


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
    temporary.replace(path)


def begin(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);current=output/'results.json'
    archived=None
    if current.exists():
        archived=output/'superseded'/uuid.uuid4().hex;archived.mkdir(parents=True)
        shutil.copyfile(current,archived/'results.json')
        names={'effective-eventwindow.json'}
        try:
            old=json.loads(current.read_text(encoding='utf-8'))
            if not isinstance(old,dict):old={}
            names.update(row['log']for row in old.get('checks',[])if isinstance(row,dict)and isinstance(row.get('log'),str))
        except (ValueError,TypeError,KeyError):pass
        for name in names:
            if Path(name).name==name and (output/name).is_file():shutil.copyfile(output/name,archived/name)
    write_json(current,dict(schema=2,status='running',passed=False,checks=[],native_acceptance=False,
        superseded_report=(archived/'results.json').relative_to(output).as_posix()if archived else None))


def run_json_audit(command,output,**kwargs):
    output=Path(output);output.unlink(missing_ok=True)
    try:result=subprocess.run(command,**kwargs)
    except OSError as error:
        result=subprocess.CompletedProcess(command,127,b'',str(error).encode())
    try:
        report=json.loads(output.read_text(encoding='utf-8-sig'))
        if not isinstance(report,dict):raise ValueError('Audit report is not an object')
    except (OSError,ValueError)as error:return result,None,'Missing or invalid fresh audit report: '+str(error)
    return result,report,None


def screen_failures(report,name):
    if not isinstance(report,dict):return None
    screens=report.get('gate_covered_screens')
    if not isinstance(screens,dict)or not isinstance(screens.get(name),dict):return None
    values=screens[name].get('failures')
    return values if isinstance(values,list)else None


def finish(output,before,after,checks,error=None):
    passed=bool(checks and before is not None and before==after and not error and
        all(row.get('accepted_contract',row['exit_code']==0)for row in checks))
    report=dict(schema=2,status='passed'if passed else'failed',passed=passed,source_before=before,source_after=after,
        checks=checks,error=error,native_acceptance=False,
        evidence='Only listed source/offline contracts; a recorded legacy ownership backlog is not whole-screen/global/native acceptance.')
    write_json(Path(output)/'results.json',report);return report
