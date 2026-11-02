"""Regressions inspect actual history/OOB outcomes, not duplicate reward models."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from build import HERE,ROOT,MOD,TAGS,FLAG,ARMOR,parse,get,walk,selected,read_source,normalized_hash
from audit import report,actual_case
from primary import Primary


DLC_PROFILES=[set(name for name,on in zip(('By Blood Alone','Man the Guns','No Step Back'),(b,m,n)) if on)
              for b in (False,True) for m in (False,True) for n in (False,True)]


class Legacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=report();cls.cases=cls.data['cases']

    def test_all_actual_source_contexts_pass(self):
        self.assertEqual(80,len(self.cases))
        self.assertEqual((40,40),(self.data['core_profiles'],self.data['lar_disabled_gap_profiles']))
        for row in self.cases:self.assertFalse(row['errors'],(row['tag'],row['bba'],row['mtg'],row['nsb'],row['lar'],row['human_tags'],row['errors']))

    def test_deployed_counts_and_named_hulls_are_preserved(self):
        expected={'BLK':(57,1130,38),'OSE':(73,932,229),'SAP':(18,220,31),'FAT':(28,195,16)}
        for row in self.cases:
            counts=(row['division_count'],row['aircraft_count'],row['ship_count'])
            wanted=expected[row['tag']]
            if row['tag']=='FAT' and row['human_tags']:wanted=(36,195,16)
            self.assertEqual(wanted,counts)
        for tag in TAGS:
            old=[(get(n,'name'),get(n,'definition')) for k,n in walk(parse(read_source('units',tag+'_navy_dlc.txt'))) if k=='ship']
            for row in [r for r in self.cases if r['tag']==tag]:
                new=[(n['name'],n['definition']) for r in row['rosters'] for n in r['ships']]
                self.assertEqual(old,new)

    def test_every_inherited_land_template_and_deployed_division_is_unchanged(self):
        for tag in TAGS:
            for suffix in (('land','land_vs_ai') if tag=='FAT' else ('land',)):
                name=tag+'_'+suffix+'.txt';before=parse(read_source('units',name));after=parse((MOD/'history/units'/name).read_text())
                for wanted in ('division_template','division'):
                    self.assertEqual([v for k,v in walk(before) if k==wanted],[v for k,v in walk(after) if k==wanted],name+':'+wanted)

                projected=parse((MOD/'history/units'/(tag+'_'+suffix+'_nsb.txt')).read_text())
                stripped=copy.deepcopy(projected)
                stripped_before=copy.deepcopy(before)
                for tree in (stripped,stripped_before):
                    for kind,body in walk(tree):
                        if kind=='division':body[:]=[n for n in body if n[0]!='force_equipment_variants']
                for wanted in ('division_template','division'):
                    self.assertEqual([v for k,v in walk(stripped_before) if k==wanted],[v for k,v in walk(stripped) if k==wanted],name+':NSB:'+wanted)

    def test_original_air_wings_retained_with_only_scout_gap_added(self):
        for tag in TAGS:
            for suffix in ('air','air_dlc'):
                name=tag+'_'+suffix+'.txt';old=get(parse(read_source('units',name)),'air_wings',[])
                new=get(parse((MOD/'history/units'/name).read_text()),'air_wings',[])
                self.assertEqual(old,new[:len(old)])
                added=[(k,int(get(v,'amount'))) for _,_,wings in new[len(old):] for k,_,v in wings]
                self.assertTrue(all(k=='scout_plane_equipment_1' for k,_ in added))
                self.assertEqual({'BLK':30,'OSE':50}.get(tag,0) if suffix=='air' else 0,sum(n for _,n in added))

    def test_politics_leaders_and_existing_shared_history_flags_unchanged(self):
        military={'set_technology','create_equipment_variant','set_oob','set_air_oob','set_naval_oob','add_equipment_to_stockpile'}
        for tag in TAGS:
            old=parse(read_source('countries',next((HERE/'baseline/countries').glob(tag+' - *.txt')).name))
            new=parse(next((MOD/'history/countries').glob(tag+' - *.txt')).read_text())
            for dlcs in DLC_PROFILES:
                before=[n for n in selected(old,dlcs,tag) if n[0] not in military]
                after=[n for n in selected(new,dlcs,tag) if n[0] not in military and not(n[0]=='set_country_flag' and n[2]==FLAG)]
                self.assertEqual(before,after,tag)

    def test_startup_reload_guards_prevent_duplicate_force_or_stock_grants(self):
        for tag in TAGS:
            history=parse(next((MOD/'history/countries').glob(tag+' - *.txt')).read_text())
            for dlcs in DLC_PROFILES:
                first=list(selected(history,dlcs,tag));repeat=list(selected(history,dlcs,tag,loaded=True))
                self.assertEqual(3,sum(k in ('set_oob','set_air_oob','set_naval_oob') for k,_,_ in first))
                self.assertFalse(any(k in ('set_oob','set_air_oob','set_naval_oob','add_equipment_to_stockpile') for k,_,_ in repeat))

    def test_production_caps_count_core_capacity_and_preserve_queued_belkan_hulls(self):
        for row in self.cases:
            for kind in ('mil','yards'):self.assertLessEqual(row['requested_capacity'][kind],row['core_capacity'][kind])
        before=parse(read_source('units','BLK_navy_dlc.txt'));after=parse((MOD/'history/units/BLK_navy_dlc.txt').read_text())
        def totals(tree):
            rows=[v for k,v in walk(tree) if k=='add_equipment_production']
            return sum(int(get(r,'requested_factories','0')) for r in rows),sum(int(get(r,'amount','0')) for r in rows)
        self.assertEqual((13,28),totals(before));self.assertEqual((12,28),totals(after))

    def test_unused_osean235_definition_and_explicit_divergence_are_retained(self):
        before=(HERE/'baseline/units/OSE_navy.txt').read_bytes();after=(MOD/'history/units/OSE_navy.txt').read_bytes()
        self.assertEqual(before.replace(b'\r\n',b'\n'),after.replace(b'\r\n',b'\n'))
        rows=self.data['legacy_naval_divergences']['OSE']
        self.assertEqual((235,229),(rows['navy']['total'],rows['navy_dlc']['total']))
        self.assertEqual((10,12),(rows['navy']['roles']['light_cruiser'],rows['navy_dlc']['roles']['light_cruiser']))
        self.assertEqual((79,71),(rows['navy']['roles']['submarine'],rows['navy_dlc']['roles']['submarine']))

    def test_lar_disabled_context_is_visible_release_gap_not_universal_acceptance(self):
        absent=[r for r in self.cases if not r['lar']]
        self.assertEqual(40,len(absent));self.assertTrue(all('RELEASE GAP' in r['capability_status'] for r in absent))
        contract=json.loads((HERE/'primary_contract.json').read_text())
        self.assertIn('La Resistance',str(contract['lar']['legacy_allow_branch']))

    def test_generated_and_manifest_consistency(self):
        for script in ('build.py','audit.py'):
            subprocess.run([sys.executable,'-B',str(HERE/script),'--check'],check=True,capture_output=True)

    def test_hidden_transport_bridge_and_p3_exact_equipment_binding(self):
        tech=parse((MOD/'common/technologies/ac_world_legacy_support.txt').read_text())
        body=get(get(tech,'technologies'),'ac_wl_transport_support')
        self.assertEqual('no',get(get(body,'allow'),'always'))
        self.assertEqual('transport_plane_equipment_1',get(body,'enable_equipments')[0][0])
        for row in self.cases:
            if row['tag']=='OSE' and row['bba']:
                p3=[v for v in row['variants'] if v['name']=='"P-3 Orion"']
                self.assertEqual(['large_plane_maritime_patrol_plane_airframe_0'],[v['equipment'] for v in p3])

    def test_nsb_force_bindings_match_actual_templates_and_replacement_queues(self):
        for row in self.cases:
            land=next(r for r in row['rosters'] if '_land' in r['name'])
            self.assertEqual(row['nsb'],land['name'].endswith('_nsb'))
            templates={t['name']:t for t in land['templates']}
            variants={(v['equipment'],v['name']):v for v in row['variants']}
            for division in land['divisions']:
                if not row['nsb']:continue  # Original owner-only selectors are preserved on this route.
                units=templates[division['template']]['regiments']
                required={recipe['modern']:'"'+row['tag']+' '+recipe['label']+'"'
                          for recipe in ARMOR.values() if recipe['subunit'] in units}
                forced={f['equipment']:f['version'] for f in division['forced_equipment']}
                self.assertEqual(required,forced,(row['tag'],division['name']))
                for equipment,version in forced.items():
                    self.assertIn((equipment,version),variants)
                    recipe=next(r for r in ARMOR.values() if r['modern']==equipment)
                    self.assertEqual(recipe['modules'],variants[(equipment,version)]['modules'])
                    self.assertIn(recipe['technology'],row['selected_technology'])
            for queue in land['production']:
                if row['nsb']:
                    self.assertNotIn(queue['equipment'],ARMOR)
                else:self.assertNotIn(queue['equipment'],[r['modern'] for r in ARMOR.values()])

            for recipe in ARMOR.values():
                if not any(recipe['subunit'] in t['regiments'] for t in land['templates']):continue
                equipment=recipe['modern'] if row['nsb'] else recipe['legacy']
                self.assertTrue(any(p['equipment']==equipment for p in land['production']),(row['tag'],equipment,'replacement queue missing'))
                self.assertTrue(any(s['equipment']==equipment and s['amount']>=100 for s in row['stockpiles']),(row['tag'],equipment,'replacement reserve missing'))

    def test_shared_armor_owner_is_captured_and_history_only(self):
        path=MOD/'common/technologies/ac_ws_armour_support.txt'
        contract=json.loads((HERE/'primary_contract.json').read_text())
        self.assertEqual(normalized_hash(path.read_bytes()),contract['sources']['mod/common/technologies/ac_ws_armour_support.txt'])
        techs=get(parse(path.read_text()),'technologies')
        for recipe in ARMOR.values():
            body=get(techs,recipe['technology'])
            self.assertEqual('no',get(get(body,'allow'),'always'))
            self.assertIsNone(get(body,'folder'))
            self.assertIn(recipe['modern'],[k for k,_,_ in get(body,'enable_equipments')])

    def test_inherited_efficiency_preserved_and_new_lines_follow_native_oob_convention(self):
        for tag in TAGS:
            suffixes=['land','air','air_dlc','navy_dlc']+(['land_vs_ai'] if tag=='FAT' else [])
            for suffix in suffixes:
                name=tag+'_'+suffix+'.txt'
                old=[v for k,v in walk(parse(read_source('units',name))) if k=='add_equipment_production']
                if name=='BLK_navy_dlc.txt':
                    matches=[i for i,v in enumerate(old) if get(get(v,'equipment'),'version_name')=='"Zerstörer 1934A Class"']
                    del old[matches[1]]
                output_names=[name]+([tag+'_'+suffix+'_nsb.txt'] if suffix.startswith('land') else [])
                for output in output_names:
                    new=[v for k,v in walk(parse((MOD/'history/units'/output).read_text())) if k=='add_equipment_production']
                    self.assertGreaterEqual(len(new),len(old))
                    for before,after in zip(old,new):
                        self.assertEqual(get(before,'efficiency'),get(after,'efficiency'),output)
                        progress=float(get(before,'progress','0'))
                        self.assertEqual(progress/100 if progress>1 else progress,float(get(after,'progress','0')),output)
                    for added in new[len(old):]:
                        self.assertEqual(('0','50'),(get(added,'progress'),get(added,'efficiency')),output)
        contract=json.loads((HERE/'primary_contract.json').read_text())
        self.assertEqual(3,len(contract['production_context_sources']))
        self.assertIn('unverified',contract['production_context_note'])

    def test_primary_slot_aliases_preserve_categories_but_child_lists_replace_parent_slots(self):
        primary=Primary.__new__(Primary)
        primary.equipment={
            'base':parse('module_slots = { fixed = { required = yes allowed_module_categories = { gun } } obsolete = { allowed_module_categories = { old } } }'),
            'derived':parse('parent = base module_slots = { fixed = inherit custom = fixed }'),
            'whole':parse('parent = derived module_slots = inherit')}
        slots=dict((k,v) for k,_,v in primary.resolve('derived')['module_slots'])
        self.assertEqual({'fixed','custom'},set(slots))
        self.assertEqual(slots['fixed'],slots['custom'])
        self.assertEqual(primary.resolve('derived')['module_slots'],primary.resolve('whole')['module_slots'])

    def test_actual_turret_override_is_required_not_silently_skipped(self):
        path=HERE/'primary_contract.json';contract=json.loads(path.read_text())
        # The reviewed modern turret explicitly admits a medium cannon in the
        # main-armament slot. Removing that actual rule must reject the design.
        overrides=contract['modules']['tank_modern_tank_turret']['allowed_module_categories']
        self.assertIn('main_armament_slot',overrides)
        altered=copy.deepcopy(contract)
        altered['modules']['tank_modern_tank_turret']['allowed_module_categories']={}
        real_read=Path.read_text
        def read(candidate,*args,**kwargs):
            return json.dumps(altered) if candidate==path else real_read(candidate,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            failures=actual_case('BLK',True,True,nsb=True)['errors']
        self.assertTrue(any('Invalid slot/category modern_tank_chassis_1:main_armament_slot:tank_medium_cannon_2' in failure for failure in failures),failures)


if __name__=='__main__':unittest.main(verbosity=2)
