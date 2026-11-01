"""In-memory assertion sensitivity; never changes a production script or file.

Reproduce from the repository root:
python -B docs/evidence/programme-funding/dynamic-state-review/mutation_probe.py
"""
import copy
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify

CASES=(('partner','tools/usean_partners/test_integration.py','RealNationalContracts','test_enabled_unready_accounts_cannot_start_any_partner_programme'),
       ('reconstruction','tools/Test-ReconstructionContinuations.py','ReconstructionRuntime','test_enabled_unready_accounts_cannot_start_any_reconstruction_service'),
       ('superpower','tools/Test-SuperpowerProgrammes.py','SuperpowerProgrammes','test_enabled_unready_accounts_cannot_start_any_superpower_service'))


def main():
    before=capture(ROOT);rows=[]
    for owner,relative,classname,method in CASES:
        spec=importlib.util.spec_from_file_location('review_dynamic_state_'+owner,ROOT/relative)
        module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
        cls=getattr(module,classname);cls.setUpClass();original=module.World.run
        for attribute in('pp','ideas','timed_ideas'):
            observations=[]
            def mutated_run(world,name,tag,*args,**kwargs):
                result=original(world,name,tag,*args,**kwargs)
                if name.endswith('_start'):
                    country=world.countries[tag];unchanged=copy.deepcopy(country)
                    if attribute=='pp':country.pp-=Decimal(1)
                    elif attribute=='ideas':country.ideas.add('ac_review_dynamic_state_probe')
                    else:
                        if not hasattr(country,'timed_ideas'):country.timed_ideas={}
                        country.timed_ideas['ac_review_dynamic_state_probe']=world.today+90
                    observations.append(dict(dataclass_equality_ignores_mutation=country==unchanged,
                        full_state_detects_mutation=vars(country)!=vars(unchanged),attribute=attribute,
                        existed_before=hasattr(unchanged,attribute)))
                return result
            caught=False
            with patch.object(module.World,'run',mutated_run):
                try:getattr(cls(method),method)()
                except AssertionError:caught=True
            if len(observations)!=1 or not caught or not all(observations[0][key]for key in('dataclass_equality_ignores_mutation','full_state_detects_mutation')):
                raise AssertionError('Mutation was not caught by the actual unready-account assertion: '+owner+'/'+attribute)
            rows.append(dict(owner=owner,assertion_detected_mutation=caught,**observations[0]))
    after=verify(before,ROOT)
    # All production payload/capture blobs remain the exact published inputs.
    import subprocess
    changed=subprocess.check_output(['git','diff','--name-only','65666017797753012327b1183d537b5edab11b41','HEAD','--','.',':(exclude)docs/evidence/**'],cwd=ROOT,text=True).splitlines()
    expected={relative for _,relative,_,_ in CASES}
    if set(changed)!=expected:raise AssertionError('Unexpected source changes outside the three review assertions: '+str(changed))
    output=dict(source_inputs=before,source_inputs_after=after,published_base='65666017797753012327b1183d537b5edab11b41',
        production_and_original_capture_files_changed=[],test_files_changed=changed,mutation_cases=rows,passed=len(rows),
        scope='Assertion sensitivity using in-memory mutations after actual rejected starts; no native or production logic change.',native_acceptance=False)
    Path(__file__).with_name('mutation-probes.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PASS:9 injected dynamic-attribute mutations caught by actual assertions; dataclass equality ignored all9; clean source fence preserved.')


if __name__=='__main__':main()
