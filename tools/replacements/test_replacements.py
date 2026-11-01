"""Actual replacement-source regressions, with explicit manual-route exceptions."""
from collections import Counter
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import worksheet as owner
from worksheet import ROOT,MOD,TAGS,MATRIX,parse,get,walk,digest,json_digest,load,report,case,states_by_country,is_naval,key
from build_notes import NOTES,outputs

BASE=json.loads((HERE/'baseline.json').read_text())
ADDITIONS={'SNS':{'587':{'aluminium':3}},'AMB':{'501':{'aluminium':1}},
           'UGE':{'474':{'aluminium':3,'steel':5}},'DEL':{'268':{'aluminium':3,'steel':5}}}


class Replacements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=report();cls.cases=cls.data['cases']
        cls.contract=json.loads((HERE/'primary_contract.json').read_text())

    def test_all_48_actual_dlc_profiles_pass_with_fixed_capacity(self):
        self.assertEqual(48,len(self.cases))
        expected={'EMM':(14,6),'EVA':(16,4),'SNS':(5,2),'AMB':(4,2),'UGE':(3,1),'DEL':(3,1)}
        for row in self.cases:
            self.assertFalse(row['errors'],(row['tag'],row['bba'],row['mtg'],row['nsb'],row['errors']))
            self.assertEqual(expected[row['tag']],(row['MIL'],row['yards']))
            self.assertGreaterEqual(row['industrial_import_CIV_margin'],0)
            self.assertTrue(all(r['industrial_import_CIV_margin']>=0 for r in row['manual_rotations']))

    def test_exact_histories_politics_leaders_and_force_payloads_preserved(self):
        import hashlib
        def force_sha(tree):return hashlib.sha256(json.dumps([n for n in tree if n[0]!='instant_effect'],separators=(',',':')).encode()).hexdigest()
        for tag,row in BASE['countries'].items():
            self.assertEqual(row['history_sha256'],digest((ROOT/row['history']).read_bytes()),tag)
            for name,before in row['rosters'].items():
                self.assertEqual(before['force_sha256'],force_sha(load(ROOT/name)),name)
                if tag=='ERU':self.assertEqual(before['source_sha256'],digest((ROOT/name).read_bytes()),name)

    def test_all_state_identity_industry_logistics_and_original_resource_floors_preserved(self):
        import hashlib
        observed={}
        for tag,row in BASE['countries'].items():
            for name,before in row['states'].items():
                state=get(load(ROOT/name),'state');protected=[n for n in state if n[0]!='resources']
                self.assertEqual(before['protected_sha256'],hashlib.sha256(json.dumps(protected,separators=(',',':')).encode()).hexdigest(),name)
                resources={k:float(v) for k,_,v in get(state,'resources',[])}
                for resource,minimum in before['resources'].items():self.assertGreaterEqual(resources.get(resource,0),minimum,(name,resource))
                delta={r:resources.get(r,0)-before['resources'].get(r,0) for r in set(resources)|set(before['resources']) if resources.get(r,0)!=before['resources'].get(r,0)}
                if delta:observed.setdefault(tag,{})[get(state,'id')]=delta
        self.assertEqual(ADDITIONS,observed)

    def test_each_approved_addition_is_minimal_for_the_rounded_import_budget(self):
        # Removing one raw unit from any reviewed addition must break at least
        # one actual DLC/rotation endpoint under the same captured laws.
        states=states_by_country()
        for tag,changes in ADDITIONS.items():
            for ident,resources in changes.items():
                for resource in resources:
                    changed=copy.deepcopy(states[tag])
                    state=next(s for _,s,_,_ in changed if get(s,'id')==ident)
                    cell=next(n for n in get(state,'resources') if n[0]==resource);cell[2]=str(float(cell[2])-1)
                    results=[case(tag,b,m,n,self.contract,changed) for b,m,n in MATRIX]
                    self.assertTrue(any(any('imports exceed' in e for e in r['errors']) for r in results),(tag,resource))

    def test_fielded_CAS_has_a_funded_line_on_both_equipment_routes(self):
        for row in self.cases:
            if row['tag'] not in ('EMM','EVA','SNS','AMB'):continue
            cas='small_plane_cas_airframe_1' if row['bba'] else 'CAS_equipment_1'
            self.assertEqual(1,sum(v['factories'] for v in row['production'] if v['equipment']==cas))
            self.assertEqual(60 if row['tag'] in ('EMM','EVA') else 12,row['aircraft_deployed'][cas])
            if row['tag']!='AMB':
                fighter='small_plane_airframe_1' if row['bba'] else 'fighter_equipment_1'
                self.assertEqual(1,sum(v['factories'] for v in row['production'] if v['equipment']==fighter))

    def test_large_fleets_have_all_four_funded_roles_without_extra_yards(self):
        for row in self.cases:
            if row['tag'] not in ('EMM','EVA'):continue
            expected={'convoy_1',*(['ship_hull_light_2','ship_hull_cruiser_2','ship_hull_submarine_2'] if row['mtg'] else ['destroyer_2','light_cruiser_2','submarine_2'])}
            self.assertEqual(expected,{v['equipment'] for v in row['production'] if is_naval(v['equipment'])})
            self.assertEqual(0,row['stored_replacement_hulls'])

    def test_tiny_yards_retain_convoys_and_all_manual_endpoints_are_accounted(self):
        for row in self.cases:
            expected={'EMM':0,'EVA':0,'SNS':1,'AMB':3,'UGE':1,'DEL':1}[row['tag']]
            self.assertEqual(expected,len(row['manual_rotations']))
            convoy=next(v for v in row['production'] if v['equipment']=='convoy_1')
            self.assertEqual(1,convoy['factories'])
            self.assertEqual(0,row['stored_replacement_hulls'])
            if row['tag'] in ('UGE','DEL'):
                self.assertEqual(1,len([v for v in row['production'] if is_naval(v['equipment'])]))
                self.assertEqual('convoy_1',row['manual_rotations'][0]['switches'][0]['from_equipment'])
            for rotation in row['manual_rotations']:
                self.assertIn('no automatic AI rotation',rotation['implementation'])

    def test_amber_air_exception_uses_exact_existing_reserves_not_new_grants(self):
        for row in self.cases:
            if row['tag']!='AMB':continue
            fighter='small_plane_airframe_1' if row['bba'] else 'fighter_equipment_1'
            cas='small_plane_cas_airframe_1' if row['bba'] else 'CAS_equipment_1'
            self.assertEqual((36,12),(row['aircraft_deployed'][fighter],row['starting_reserves'][fighter]))
            self.assertEqual((12,6),(row['aircraft_deployed'][cas],row['starting_reserves'][cas]))
            self.assertFalse(any(v['equipment']==fighter for v in row['production']))
            self.assertTrue(any(any(s['to_equipment']==fighter for s in r['switches']) for r in row['manual_rotations']))
            self.assertEqual(16.6667,row['reserve_loss_sensitivity_2percent_per_month']['air_reserve_months'][fighter])

    def test_omitted_CAS_line_is_a_real_source_failure(self):
        path=MOD/'history/units/EMM_anea_air_bba.txt';tree=load(path)
        instant=get(tree,'instant_effect');instant[:]=[v for v in instant if get(get(v[2],'equipment'),'type')!='small_plane_cas_airframe_1']
        from script import render
        altered=render(tree);read=Path.read_text
        def replacement(p,*args,**kwargs):return altered if p==path else read(p,*args,**kwargs)
        with patch.object(Path,'read_text',replacement):
            row=case('EMM',True,True,False,self.contract,states_by_country()['EMM'])
        self.assertTrue(any('replacement role gap' in e for e in row['errors']))

    def test_actual_DLC_production_gate_cannot_be_waived_by_granted_tech(self):
        altered=copy.deepcopy(self.contract)
        for row in altered['recipes'].values():
            if row['equipment']=='small_plane_cas_airframe_1':row['can_be_produced']=[['always','=','no']]
        with self.assertRaisesRegex(ValueError,'production gate'):
            case('EMM',True,True,False,altered,states_by_country()['EMM'])

    def test_army_fuel_includes_needed_equipment_and_stays_a_labeled_proxy(self):
        for row in self.cases:
            if row['tag'] not in ('EMM','EVA'):continue
            fuel=row['fuel_sensitivity']
            self.assertGreater(fuel['daily_army_equipment_per_subunit_proxy'],0)
            self.assertGreater(fuel['daily_army_literal_equipment_sum_stress'],fuel['daily_army_equipment_per_subunit_proxy'])
        self.assertTrue(any('native aggregation' in text for text in self.data['limitations']))
        self.assertTrue(any(row['fuel_sensitivity']['industrial_and_full_proxy_fuel_import_CIV_margin']<0 for row in self.cases))

    def test_visible_notes_are_read_only_and_bind_existing_authored_icons(self):
        category=get(parse(outputs()['common/decisions/categories/ac_replacement_notes.txt']),'ac_rp_replacements')
        decisions=get(parse(outputs()['common/decisions/ac_replacement_notes.txt']),'ac_rp_replacements')
        self.assertEqual('ac_anea_recovery',get(category,'icon'))
        self.assertEqual(6,len(decisions))
        for tag in TAGS:
            body=get(decisions,tag+'_rp_production_notes')
            self.assertEqual('no',get(get(body,'available'),'always'))
            self.assertEqual([['custom_effect_tooltip','=','ac_rp_reference_only']],get(body,'complete_effect'))
        gfx=(MOD/'interface/ac_anea_art.gfx').read_text()
        for ident in ('GFX_decision_category_ac_anea_recovery','GFX_decision_ac_anea_recovery'):self.assertIn('"'+ident+'"',gfx)
        for tag in ('UGE','DEL'):self.assertIn('no stored replacement hulls',NOTES[tag][1])

    def test_source_policy_and_technical_hashes_are_explicit(self):
        self.assertTrue(self.contract['sources'])
        for name,value in self.contract['sources'].items():
            if name.startswith('mod/'):self.assertEqual(value,digest((MOD/name.split('/',1)[1]).read_bytes()),name)
        for row in self.cases:
            self.assertIn(row['opening_policies']['laws']['trade_laws'],('limited_exports','export_focus'))
            self.assertTrue(all(len(d)==64 for d in row['source_sha256'].values()))

    def test_all_generators_and_actual_worksheet_are_reproducible(self):
        for script in ('tools/anea/foundation.py','tools/world_foundation/build.py','tools/world_foundation/placements.py',
                       'tools/replacements/build_notes.py','tools/replacements/worksheet.py'):
            result=subprocess.run([sys.executable,'-B',str(ROOT/script),'--check'],capture_output=True,text=True)
            self.assertEqual(0,result.returncode,script+'\n'+result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
