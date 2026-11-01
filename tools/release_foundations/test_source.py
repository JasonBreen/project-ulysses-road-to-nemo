"""Protected source, exact outputs, known geometry and art packaging."""
import copy,hashlib,importlib.util,json,sys,unittest
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/anea')]
import source_contract,author,physical,network,leaders
import release_worksheet as worksheet
from foundation_map import topology
from release_harness import World,parse,get

class Source(unittest.TestCase):
    def test_protected_native_events_and_all_geography_inputs_match(self):self.assertEqual(8,source_contract.validate()['protected_events'])
    def test_actual_fraction_and_treaty_mutations_fail_closed(self):
        for relative,old,new in [('events/AWWNB.txt','size = 0.25','size = 0.35'),('events/Belka.txt','transfer_state = 316','transfer_state = 345')]:
            text=(MOD/relative).read_text(encoding='utf-8-sig');self.assertIn(old,text)
            with self.assertRaisesRegex(ValueError,'Protected native'):source_contract.validate_event_operations({relative:text.replace(old,new,1)})
    def test_generated_lifecycle_and_maintenance_match_exact_text(self):
        for relative,text in (author.outputs()|physical.outputs()|leaders.outputs()).items():self.assertEqual(text,(MOD/relative).read_text(encoding='utf-8-sig'),relative)
    def test_network_edges_are_existing_owned_land_geometry_and_never_replace_a_rail(self):
        defs,graph,_,_,_=topology();intake=json.loads((HERE/'intake.json').read_text());data=physical.contract()['networks'];old=set()
        for line in (MOD/'map/railways.txt').read_text().splitlines():
            route=list(map(int,line.split()[2:]));old.update(tuple(sorted(edge)) for edge in zip(route,route[1:]))
        self.assertEqual(data,network.capture(intake))
        for tag,cases in data['countries'].items():
            for case in cases:
                own=set(case['controlled_provinces'])
                for a,b in case['missing_edges']:
                    self.assertTrue(defs[a]['land'] and defs[b]['land']);self.assertIn(b,graph[a]);self.assertTrue({a,b}<=own);self.assertNotIn(tuple(sorted((a,b))),old)
                for component in case['components']:
                    if not component['capital_component']:self.assertTrue(component['receiving_ports'] or component['landlocked_detached'])
    def test_all_known_footprints_choose_owned_capitals_and_never_mint_combat_units(self):
        intake=json.loads((HERE/'intake.json').read_text())
        for tag,country in intake['countries'].items():
            for case in country['known_cases']:
                w=World();w.release_action('on_startup')
                for state in case['states']:w.states[state].owner=w.states[state].controller=tag
                for p in case.get('controlled_exclusions',[]):w.province_controllers[p]='BLK'
                w.release_action('on_release_as_free',tag,'BLK')
                self.assertEqual(case['capital_state'],w.capitals[tag]);self.assertIn(w.capitals[tag],case['states']);self.assertEqual(0,w.armies[tag])
    def test_country_already_exists_without_land_is_adopted_before_later_recovery(self):
        w=World(new=False);w.external_exists.add('REC');w.release_action('on_startup')
        w.states[316].owner=w.states[316].controller='REC';w.release_action('on_release_as_free','REC','BLK')
        self.assertIn('ac_release_REC_adopted',w.globals);self.assertEqual({},w.countries['REC'].equipment);self.assertEqual(0,w.armies['REC'])
    def test_structural_snapshot_resume_preserves_receipts_without_claiming_native_reload(self):
        w=World();w.release_action('on_startup');w.armies['BLK']=40;w.fire('awwnb.1','BLK');w=copy.deepcopy(w);w.fire('awwnb.2','BLK');before=copy.deepcopy((w.armies,w.countries['AWW'].equipment))
        w=copy.deepcopy(w);w.release_action('on_startup');w.fire('awwnb.2','BLK',stale=True)
        self.assertEqual(before,(w.armies,w.countries['AWW'].equipment))
    def test_stock_and_finance_receipts_are_distinct_and_all_profiles_remain_conditional(self):
        data=worksheet.report();self.assertFalse(data['universal_sustainable_release_acceptance']);self.assertEqual(7,len(data['countries']))
        for tag,row in data['countries'].items():
            for case in row['cases']:self.assertEqual(0,case['new_automatically_deployed_personnel']);self.assertEqual(4,len(case['replacement_choices']))
        self.assertTrue(all(c['direct_roster_core_pool_margin']<0 for c in data['countries']['AWW']['cases']))
        self.assertNotEqual('ac_release_REC_transport_delivered','ac_macro_initialized')
    def test_artwork_frames_alpha_and_sprite_bindings(self):
        assets=json.loads((HERE/'assets.json').read_text());self.assertEqual(17,len(assets['assets']));gfx=(MOD/'interface/ac_release_foundations.gfx').read_text();digests=set()
        for row in assets['assets']:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest());self.assertEqual(1,row['frames']);self.assertIn('name = "'+row['sprite']+'"',gfx)
            with Image.open(path) as image:self.assertEqual((row['width'],row['height']),image.size);self.assertEqual((row['alpha_min'],255),image.getchannel('A').getextrema())
            self.assertEqual((26,29) if '/decision/' in row['file'] else (100,100) if '/category/' in row['file'] else (156,210),(row['width'],row['height']))
            if '/decision/' in row['file']:self.assertIn('name = "GFX_'+row['sprite'].removeprefix('GFX_decision_')+'" texturefile = "'+row['file']+'"',gfx)
            digests.add(row['sha256'])
        self.assertEqual(17,len(digests))
    def test_state_controller_hook_uses_previous_country_and_capitulation_cancels(self):
        for hook in ('on_state_control_changed','on_capitulation'):
            w=World();w.release_action('on_startup');w.states[316].owner=w.states[316].controller='REC';w.release_action('on_release_as_free','REC','GEB');c=w.countries['REC'];c.variables['ac_macro_cash']=__import__('decimal').Decimal('.02');w.run('ac_release_REC_start_military','REC')
            if hook=='on_state_control_changed':w.states[316].controller='BLK';w.release_action(hook,'BLK','REC')
            else:w.release_action(hook,'REC','BLK')
            self.assertNotIn('ac_release_REC_military_active',c.flags)

if __name__=='__main__':unittest.main(verbosity=2)
