"""Regressions inspect actual history/OOB outcomes, not duplicate reward models."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from build import HERE,ROOT,MOD,TAGS,FLAG,parse,get,walk,selected,read_source,normalized_hash
from audit import report,actual_case


class Legacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=report();cls.cases=cls.data['cases']

    def test_all_actual_source_contexts_pass(self):
        self.assertEqual(40,len(self.cases))
        for row in self.cases:self.assertFalse(row['errors'],(row['tag'],row['bba'],row['mtg'],row['human_tags'],row['errors']))

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
            for dlcs in (set(),{'By Blood Alone','Man the Guns'}):
                before=[n for n in selected(old,dlcs,tag) if n[0] not in military]
                after=[n for n in selected(new,dlcs,tag) if n[0] not in military and not(n[0]=='set_country_flag' and n[2]==FLAG)]
                self.assertEqual(before,after,tag)

    def test_startup_reload_guards_prevent_duplicate_force_or_stock_grants(self):
        for tag in TAGS:
            history=parse(next((MOD/'history/countries').glob(tag+' - *.txt')).read_text())
            for dlcs in (set(),{'By Blood Alone','Man the Guns'}):
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
        self.assertEqual(20,len(absent));self.assertTrue(all('RELEASE GAP' in r['capability_status'] for r in absent))
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


if __name__=='__main__':unittest.main(verbosity=2)
