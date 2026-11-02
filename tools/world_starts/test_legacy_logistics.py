"""Actual external force receipts, additive state setup and owned logistics."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import legacy_foundation as owner
from legacy_worksheet import report
from placement import derive,topology
from script import parse,get
from inventory import selected,condition

parser=argparse.ArgumentParser();parser.add_argument('--reference',type=Path);parser.add_argument('--require-integrated-owner',action='store_true');args,rest=parser.parse_known_args()
M=json.loads(owner.FOUNDATION.read_text());P=json.loads(owner.PROFILES.read_text())['countries'];S=json.loads(owner.INPUTS.read_text())


class LegacyLogisticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.defs,cls.graph,_,_,_=topology()

    def test_four_exact_countries_and_zero_foreign_history_or_force_writes(self):
        self.assertEqual(set(M['countries']),{'BLK','OSE','SAP','FAT'})
        for relative in owner.outputs(M):
            self.assertTrue(relative.startswith(('history/states/','map/','localisation/english/replace/')),relative)
        for tag,p in P.items():
            self.assertEqual(p['mode'],'external_owner');self.assertFalse(p['formations']);self.assertFalse(p['production'])
            self.assertGreater(M['countries'][tag]['external_requested_capacity']['mil'],0)

    def test_real_external_owner_receipts_are_required_for_integration(self):
        gaps=owner.binding_gaps()
        if not (owner.ROOT/S['component_manifest']).exists() and not args.require_integrated_owner:
            self.skipTest('External legacy force component is not yet integrated; this source-binding gate is open')
        self.assertFalse(gaps,gaps)

    def test_missing_mutated_and_stale_local_receipts_fail_closed(self):
        import tempfile
        source=owner.ROOT/S['component_manifest']
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(owner,'ROOT',root):
                self.assertTrue(owner.binding_gaps())
                target=root/S['component_manifest'];target.parent.mkdir(parents=True);target.write_text('{}')
                self.assertIn('Legacy manifest receipt changed',owner.binding_gaps())
                self.assertTrue(any('Legacy source receipt differs:' in gap for gap in owner.binding_gaps()))
                # Merely copying the manifest does not bless absent source files.
            if source.exists():
                target.write_bytes(source.read_bytes())
                with patch.object(owner,'ROOT',root):
                    self.assertTrue(owner.binding_gaps())
                # A valid manifest plus copied source files can bind; mutating
                # one selected roster must immediately invalidate that receipt.
                real_root=owner.ROOT
                for relative in S['component_inputs_sha256']:
                    path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((real_root/relative).read_bytes())
                technical=json.loads(owner.FOUNDATION.read_text())['primary_sources_sha256']
                for relative in technical:
                    if relative.startswith('mod/'):
                        relative='mod/2985041246/'+relative.removeprefix('mod/')
                        path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((real_root/relative).read_bytes())
                with patch.object(owner,'ROOT',root):self.assertFalse(owner.binding_gaps())
                stale=copy.deepcopy(S);stale['countries']['BLK']['cases'][0]['division_count']+=1
                stale_path=root/'snapshot.json';stale_path.write_text(json.dumps(stale))
                with patch.object(owner,'ROOT',root),patch.object(owner,'INPUTS',stale_path):
                    self.assertIn('Legacy selected-case snapshot differs: BLK',owner.binding_gaps())
                stale=copy.deepcopy(S);next(iter(stale['countries']['BLK']['rosters'].values()))['text']+='# stale captured roster\n'
                stale_path.write_text(json.dumps(stale))
                with patch.object(owner,'ROOT',root),patch.object(owner,'INPUTS',stale_path):
                    self.assertTrue(any(gap.startswith('Legacy roster snapshot differs:') for gap in owner.binding_gaps()))
                relative=next(r for r in S['component_inputs_sha256'] if '/history/units/' in r)
                (root/relative).write_text('# changed selected roster\n')
                with patch.object(owner,'ROOT',root):self.assertIn('Legacy source receipt differs: '+relative,owner.binding_gaps())

    def test_actual_setup_guards_stop_duplicate_rosters_and_stock_grants(self):
        for tag,snapshot in S['countries'].items():
            for case in snapshot['cases']:
                dlcs={name for name,key in [('By Blood Alone','bba'),('Man the Guns','mtg'),('No Step Back','nsb'),('La Resistance','lar')] if case[key]}
                flags={};history=parse(snapshot['history_source'])
                first=list(selected(history,dlcs,tag,case['human_tags'],flags))
                second=list(selected(history,dlcs,tag,case['human_tags'],flags))
                roster_keys=('set_oob','load_oob','set_air_oob','set_naval_oob')
                self.assertEqual(sum(k in roster_keys for k,_,_ in first),3,(tag,dlcs))
                self.assertTrue(any(k=='add_equipment_to_stockpile' for k,_,_ in first))
                self.assertFalse(any(k in (*roster_keys,'add_equipment_to_stockpile','add_fuel') for k,_,_ in second),(tag,dlcs))
        # Cross-country tests must read that country's flag set rather than ROOT.
        self.assertTrue(condition(parse('BLK = { has_country_flag = ready }'),set(),'FAT',(),{'BLK':{'ready'}}))
        self.assertFalse(condition(parse('BLK = { has_country_flag = ready }'),set(),'FAT',(),{'FAT':{'ready'}}))
        with self.assertRaisesRegex(ValueError,'Uninspected history condition'):
            condition(parse('unknown_history_trigger = yes'),set(),'FAT',(),{})

    def test_economy_marker_and_legacy_history_owner_compose_without_moving_setup(self):
        sys.path.insert(0,str(owner.ROOT/'tools/economy_v2'))
        spec=importlib.util.spec_from_file_location('legacy_macro_history_owner',owner.ROOT/'tools/economy_v2/build.py')
        macro=importlib.util.module_from_spec(spec);spec.loader.exec_module(macro)
        for tag,snapshot in S['countries'].items():
            source=snapshot['history_source']
            self.assertEqual(macro.history_marker(source),source,tag)
            self.assertEqual(macro.history_marker(macro.history_marker(source)),source,tag)
            suffix=source[source.index('# BEGIN LEGACY WORLD START STOCKS'):]
            self.assertTrue(macro.history_marker(source).endswith(suffix))

    def test_geometry_and_outputs_reproduce_without_external_source_or_game(self):
        self.assertEqual(derive(None,owner.PROFILES,owner.FOUNDATION),M)
        for relative,text in owner.outputs(M).items():self.assertEqual((owner.MOD/relative).read_text(encoding='utf-8'),text,relative)
        self.assertEqual(report(),json.loads((HERE/'legacy_sustainment.json').read_text()))

    def test_every_inherited_state_quantity_identity_and_budget_is_preserved(self):
        for tag,row in M['countries'].items():
            totals={k:0 for k in ('civilian','military','dockyard')}
            for ident,old in row['baseline'].items():
                state=get(parse((owner.MOD/old['path']).read_text()),'state');history=get(state,'history');buildings=get(history,'buildings')
                self.assertEqual(get(history,'owner'),tag)
                self.assertEqual([v for k,_,v in history if k=='add_core_of'],old['cores'])
                self.assertEqual(int(get(state,'manpower')),old['manpower'])
                self.assertEqual([int(k) for k,_,_ in get(state,'provinces')],old['provinces'])
                for key,field in [('civilian','industrial_complex'),('military','arms_factory'),('dockyard','dockyard')]:
                    amount=int(get(buildings,field,'0'));self.assertEqual(amount,old['buildings'][key]);totals[key]+=amount
                resources={k:float(v) for k,_,v in get(state,'resources',[])}
                for key,value in old['resources'].items():self.assertGreaterEqual(resources[key],float(value))
                for province,level in old['ports'].items():self.assertEqual(int(get(get(buildings,province),'naval_base')),level)
            self.assertEqual(totals,P[tag]['target_industry'])

    def test_all_operational_targets_reach_owned_component_terminals(self):
        for tag,row in M['countries'].items():
            connected=set()
            for c in row['components']:
                group=set(c['provinces']);connected.add(c['root'])
                for path in c['routes']:
                    self.assertEqual(path[0],c['root']);self.assertTrue(set(path)<=group)
                    for a,b in zip(path,path[1:]):self.assertIn(b,self.graph[a]);self.assertTrue(self.defs[a]['land'] and self.defs[b]['land'])
                    connected.update(path)
                self.assertTrue(set(c['terminals'])<=connected)
                if c['index'] and not c.get('sealed_source_exception'):self.assertTrue(c['ports'])
            self.assertTrue(set(P[tag]['required_land_deployments'])<=connected)
            for state,count in P[tag]['required_air_bases'].items():
                self.assertGreaterEqual(row['placements'][state]['air_base']*200,count)
                self.assertIn(row['airports'][state],connected)
            self.assertTrue(set(P[tag]['required_naval_ports'])<={p['province'] for p in row['ports']})
            for state in row['existing_industrial_states']:
                # The same authored airport coordinate is the industrial
                # district's declared logistics anchor; no coordinate is moved.
                from placement import parse as parse_script
                airports={int(k):int(v[0][0]) for k,_,v in parse_script((owner.MOD/'map/airports.txt').read_text()) if k.isdigit() and v}
                self.assertIn(airports[state],connected)

    def test_ports_have_existing_coastal_sea_spawn_geometry(self):
        spawns={(int(v[0]),int(v[6])) for line in (owner.MOD/'map/buildings.txt').read_text().splitlines() if ';' in line and (v:=line.split(';'))[1]=='naval_base_spawn'}
        for row in M['countries'].values():
            for port in row['ports']:
                self.assertTrue(self.defs[port['province']]['coastal'])
                self.assertTrue(any(self.defs[n]['kind']=='sea' and (port['state'],n) in spawns for n in self.graph[port['province']]))

    def test_belkan_sealed_area_has_no_required_target_or_shared_state_allocation(self):
        row=M['countries']['BLK'];sealed=[c for c in row['components'] if c.get('sealed_source_exception')]
        self.assertEqual(len(sealed),1);self.assertEqual(sealed[0]['provinces'],[1939,5906,7545,7569,7570,7595,7603])
        self.assertFalse(sealed[0]['terminals']);self.assertFalse(sealed[0]['routes']);self.assertFalse(sealed[0]['ports'])
        state=row['baseline']['309'];self.assertEqual(state['manpower'],101046);self.assertEqual(state['cores'],['BLK','UST'])
        self.assertEqual(row['placements']['309']['resources'],state['resources'])
        for key,value in state['buildings'].items():self.assertEqual(row['placements']['309'][key],value)
        forbidden=set(P['BLK']['required_land_deployments'])|set(P['BLK']['required_naval_ports'])|set(row['all_supply_hubs'])
        self.assertFalse(set(sealed[0]['provinces'])&forbidden)
        self.assertNotIn('309',P['BLK']['required_air_bases'])
        self.assertFalse(any(record['state']==309 for record in row['resource_additions']))

    def test_literal_policy_import_capacity_and_personnel_budgets_are_explicit(self):
        data=report();self.assertFalse(data['universal_sustainable_start_acceptance'])
        for tag,row in data['countries'].items():
            for case in row['cases']:
                self.assertGreaterEqual(case['industrial_trade_CIV_margin'],0,(tag,case['human_tags']))
                self.assertGreaterEqual(case['personnel_headroom'],0,(tag,case['human_tags']))
                self.assertFalse(case['missing_enabled_ground_equipment'],(tag,case['missing_enabled_ground_equipment']))
                self.assertIn('no native unit interpretation',case['production_efficiency_unit_status'])
        self.assertEqual(M['countries']['OSE']['opening_policies']['laws']['trade_laws'],'free_trade')
        self.assertEqual(M['countries']['SAP']['opening_policies']['modifiers']['local_resources_factor'],-.2)

    @unittest.skipUnless(args.reference,'No read-only installed primary reference supplied')
    def test_primary_contract_recapture_matches(self):
        self.assertEqual(derive(args.reference,owner.PROFILES,owner.FOUNDATION,owner.capture),M)


if __name__=='__main__':unittest.main(argv=[sys.argv[0]]+rest,verbosity=2)
