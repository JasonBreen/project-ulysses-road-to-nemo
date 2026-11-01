"""Actual naval source, primary replay, real fiscal owner and UI consumers."""
import argparse
import copy
from decimal import Decimal as D
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/economy_v2')]
from script import parse,get,walk,setv
from naval_content import YEARS,MTG,SHIPS,FAMILIES,TECHS,MODULES,tech_id,model_id,hull_id,module_id,recipe,dependencies
from naval_primary import Primary,STATS
import audit
from harness import World
ENGINE=None
def digest(path):return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def read(path):return parse(path.read_text(encoding='utf-8-sig'))

class Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts=json.loads((HERE/'primary_contract.json').read_text());cls.tech=audit.technologies();cls.gear=audit.equipment();cls.parts=audit.modules()
        cls.p=Primary.from_capture(cls.facts['catalog'],cls.gear,cls.parts)
    def test_inventory_namespaces_no_new_archetypes_or_duplicate_old_ids(self):
        self.assertEqual((24,40,64),(len(self.tech),len(self.gear),len(self.parts)))
        self.assertTrue(all(i.startswith('ac_naval_') for i in [*self.tech,*self.gear,*self.parts]))
        self.assertTrue(all(get(b,'is_archetype') is None and get(b,'active')=='no' for b in self.gear.values()))
        folders=get(read(MOD/'common/technology_tags/ac_naval_categories.txt'),'technology_folders')
        self.assertEqual(get(self.facts['native_folder'],'ledger'),get(get(folders,'ac_naval_folder'),'ledger'))
        for path in (MOD/'common/technologies').glob('*.txt'):
            if path.name!='ac_naval_program.txt':self.assertFalse(set(self.tech)&{k for k,_,v in get(read(path),'technologies',[])})
    def test_actual_date_and_each_first_foundation_are_required(self):
        foundations=set(self.facts['foundations'])
        for row in TECHS:
            b=self.tech[row['id']];required=set(dependencies(row['family'],row['tier']));alltech=foundations|set(self.tech)
            self.assertEqual(required,{k for k,_,v in get(b,'dependencies')});self.assertEqual(str(row['year']),get(b,'start_year'))
            self.assertGreater(float(get(b,'research_cost')),0)
            for mtg in (False,True):
                dlc={MTG} if mtg else set();self.assertFalse(audit.condition(get(b,'allow'),(row['year']-1,12,31),alltech,dlc))
                self.assertTrue(audit.condition(get(b,'allow'),(row['year'],1,1),alltech,dlc))
                for missing in required:self.assertFalse(audit.condition(get(b,'allow'),(row['year'],1,1),alltech-{missing},dlc))
        for f in SHIPS:
            b=self.tech[tech_id(f.id,2006)]
            for mtg in (False,True):
                missing=f.designer_foundation if mtg else f.legacy_foundation
                self.assertFalse(audit.condition(get(b,'allow'),(2006,1,1),(foundations|set(self.tech))-{missing},{MTG} if mtg else set()))
    def test_all_dates_and_sixteen_independent_dlc_profiles(self):
        for year,tiers in ((1991,0),(2005,0),(2006,1),(2010,2),(2015,3),(2020,4),(2030,4)):
            for mtg in (False,True):self.assertEqual(6*tiers,len(audit.closure(year,{MTG} if mtg else set(),self.tech,self.facts['foundations'])&set(self.tech)))
        report=audit.report(ENGINE);self.assertEqual([],report['errors']);self.assertEqual((12,16),(len(report['cases']),len(report['independent_DLC_profiles'])))
        for row in report['independent_DLC_profiles']:
            self.assertEqual(20,len(row['models']));self.assertTrue(all(('_hull_' in i)==row['mtg'] for i in row['models']))
    def test_real_complete_and_modular_defaults_have_full_slot_coverage_and_parity(self):
        for f in SHIPS:
            for year in YEARS:
                a=self.p.design(model_id(f.id,year),complete=True);b=self.p.design(hull_id(f.id,year),complete=True)
                for key in ('stats','resources','effective_types','selected_modules','external_module_crew'):self.assertEqual(a[key],b[key],(f.id,year,key))
                self.assertEqual(set(a['all_slots']),set(a['selected_modules']))
                for k in ('build_cost_ic','fuel_consumption','manpower','naval_speed','naval_range'):self.assertGreater(a['stats'][k],0)
                self.assertTrue(all(v>0 for v in a['resources'].values()))
    def test_defaults_and_external_deck_crew_are_counted_exactly_once(self):
        native=self.facts['native_semantic_modules']['ship_deck_space'];self.assertEqual('500',get(native,'manpower'));self.assertIsNone(get(get(native,'add_stats'),'manpower'))
        escort=self.p.stats(model_id('escort',2006));self.assertEqual(5,escort['stats']['lg_attack']);self.assertEqual(2460,escort['stats']['build_cost_ic'])
        self.assertEqual(9,escort['stats']['fuel_consumption']);self.assertEqual(240,escort['stats']['manpower'])
        carrier=self.p.stats(model_id('carrier',2006));self.assertEqual(9920,carrier['stats']['build_cost_ic']);self.assertEqual(2400,carrier['stats']['manpower'])
        self.assertEqual(600,carrier['external_module_crew']);self.assertEqual(6,carrier['stats']['carrier_size'])
        for f in SHIPS:
            ident=model_id(f.id,2006);selected=self.p.stats(ident)['selected_modules'];self.assertEqual(self.p.stats(ident),self.p.stats(ident,selected))
        bad=copy.deepcopy(self.gear);ident=model_id('escort',2006);setv(bad[ident],'lg_attack','5')
        with patch.object(audit,'equipment',lambda:bad):self.assertTrue(any('parity mismatch' in v for v in audit.report()['errors']))
    def test_first_weapon_advances_preserve_actual_primary_capabilities(self):
        old=self.facts['native_semantic_modules']
        for new,parent in [('surface_torpedo','ship_torpedo_4'),('sub_torpedo','ship_torpedo_sub_4')]:
            body=self.parts[module_id(new,2006)]
            for stat in ('torpedo_attack','naval_torpedo_hit_chance_factor'):
                self.assertGreaterEqual(D(get(get(body,'add_stats'),stat)),D(get(get(old[parent],'add_stats'),stat)))
        self.assertGreaterEqual(D(get(get(self.parts[module_id('escort_battery',2006)],'add_stats'),'anti_air_attack')),D(get(get(old['dp_light_battery_4'],'add_stats'),'anti_air_attack')))
        self.assertGreaterEqual(D(get(get(self.parts[module_id('fleet_battery',2006)],'add_average_stats'),'hg_armor_piercing')),D(get(get(old['ship_medium_battery_4'],'add_average_stats'),'hg_armor_piercing')))
        for f in ('escort','submarine'):
            self.assertEqual(.02,self.p.stats(model_id(f,2006))['stats']['naval_torpedo_hit_chance_factor'])
            self.assertEqual(.035,self.p.stats(model_id(f,2020))['stats']['naval_torpedo_hit_chance_factor'])
    def test_captured_parent_priorities_and_priority_regression(self):
        for ident,body in self.gear.items():self.assertGreater(int(get(body,'priority')),int(self.p.resolve(get(body,'parent'))['priority']))
        bad=copy.deepcopy(self.gear);setv(bad[model_id('escort',2006)],'priority','100')
        with patch.object(audit,'equipment',lambda:bad):self.assertTrue(any('priority' in v for v in audit.report()['errors']))
    def test_medium_battery_promotes_only_the_correct_cruiser_classification(self):
        ident=hull_id('fleet',2006);self.assertEqual('screen_ship',get(self.gear[ident],'type'))
        self.assertIn('capital_ship',self.p.stats(ident)['effective_types']);self.assertNotIn('screen_ship',self.p.stats(ident)['effective_types'])
        selected=self.p.stats(ident)['selected_modules'];selected['fixed_ship_battery_slot']=module_id('cruiser_battery',2006)
        optional=self.p.design(ident,selected);self.assertIn('screen_ship',optional['effective_types']);self.assertNotIn('capital_ship',optional['effective_types'])
        bad=copy.deepcopy(self.parts);setv(bad[module_id('fleet_battery',2006)],'add_equipment_type','anti_air')
        with patch.object(audit,'modules',lambda:bad):self.assertTrue(any('classification' in v for v in audit.report()['errors']))
    def test_sonar_and_depth_charge_statistics_do_not_claim_mission_equivalence(self):
        for y in YEARS:
            escort=self.p.stats(model_id('escort',y));self.assertGreaterEqual(escort['stats']['sub_attack'],15);self.assertGreaterEqual(escort['stats']['sub_detection'],2)
            self.assertEqual(0,self.p.stats(model_id('submarine',y))['stats']['sub_attack'])
        self.assertTrue(all(not r['native_mission_equivalence'] for r in audit.report()['default_physical_parity']))
        self.assertEqual(10,self.facts['semantics']['carrier_size_increment'])
    def test_missing_required_slot_wrong_category_and_optional_default_coverage_fail(self):
        ident=model_id('escort',2006);selected=self.p.stats(ident)['selected_modules'];selected['fixed_ship_engine_slot']='empty'
        with self.assertRaisesRegex(ValueError,'Missing required'):self.p.design(ident,selected)
        selected=self.p.stats(ident)['selected_modules'];selected['fixed_ship_engine_slot']=module_id('deck',2006)
        with self.assertRaisesRegex(ValueError,'Incompatible naval'):self.p.design(ident,selected)
        p=copy.deepcopy(self.p);defaults=get(p.equipment[ident],'default_modules');defaults[:]=[r for r in defaults if r[0]!='mid_1_custom_slot']
        with self.assertRaisesRegex(ValueError,'slot coverage'):p.design(ident,complete=True)
    def test_every_repeated_count_limit_is_preserved_and_enforced(self):
        catalog={**self.facts['catalog']['equipment'],**self.gear}
        def declarations(ident):
            body=catalog[ident];parent=get(body,'parent',get(body,'archetype'))
            return (declarations(parent) if parent else [])+[v for k,_,v in body if k=='module_count_limit']
        for ident in self.gear:self.assertEqual(declarations(ident),self.p.resolve(ident)['module_count_limit'])
        p=copy.deepcopy(self.p);ident=hull_id('escort',2006)
        a=['module_count_limit','=',[['category','=','ship_radar'],['count','<','1']]];b=['module_count_limit','=',[['category','=','ship_sonar'],['count','<','2']]]
        p.equipment[ident].extend([a,b]);self.assertEqual([a[2],b[2]],p.resolve(ident)['module_count_limit'][-2:])
        with self.assertRaisesRegex(ValueError,'ship_radar'):p.design(ident)
    def test_unfunded_material_cost_and_multiple_average_mutations_fail(self):
        bad=copy.deepcopy(self.gear);bad[hull_id('escort',2006)].append(['unsupported_tracking','=','99'])
        with patch.object(audit,'equipment',lambda:bad):self.assertTrue(any('Uninspected owned naval field' in v for v in audit.report()['errors']))
        ident=hull_id('escort',2006);p=copy.deepcopy(self.p);setv(p.equipment[ident],'build_cost_ic','-10000')
        with self.assertRaisesRegex(ValueError,'Unfunded'):p.design(ident)
        p=copy.deepcopy(self.p);setv(get(p.modules[module_id('light_engine',2006)],'build_cost_resources'),'chromium','-100')
        with self.assertRaisesRegex(ValueError,'Non-positive'):p.design(ident)
        p=copy.deepcopy(self.p);p.equipment[ident].append(['module_add_stats_multiplier','=',[['lg_attack','=','1']]])
        with self.assertRaisesRegex(ValueError,'Uninspected naval hull'):p.stats(ident)
        selected=self.p.stats(ident)['selected_modules'];selected['mid_1_custom_slot']=module_id('escort_battery',2006)
        # The actual modern light hull's mid slot excludes batteries first.
        with self.assertRaisesRegex(ValueError,'Multiple averaged'):self.p.stats(ident,selected)
    def test_preserved_sources_and_no_early_grants_or_new_war_project_owners(self):
        manifest=json.loads((HERE/'preserved_sources.json').read_text());self.assertEqual(1110,len(manifest['sources']))
        updates=json.loads((ROOT/'tools/air_program/reviewed_owner_updates.json').read_text())['files']
        for path,expected in manifest['sources'].items():
            update=updates.get(path)
            if update:self.assertEqual(expected,update['old_sha256'],path)
            self.assertEqual(update['new_sha256']if update else expected,digest(ROOT/path),path)
        forbidden={'set_technology','load_oob','create_unit','add_equipment_to_stockpile','create_equipment_variant','transfer_state','set_country_flag','set_global_flag','declare_war_on','country_event','add_to_faction'}
        for path in [MOD/'common/technologies/ac_naval_program.txt',MOD/'common/ai_equipment/ac_naval_designs.txt',MOD/'common/ai_strategy/ac_naval_replacements.txt']:
            nodes=read(path);self.assertFalse(forbidden&{k for b in [nodes]+[v for _,v in walk(nodes)] for k,_,v in b})
    def test_retained_old_tabs_and_technology_ids_are_explicit(self):
        rows=audit.report()['retained_surfaces'];self.assertEqual([32,40,47],[len(r['technologies']) for r in rows])
        for row in rows:self.assertEqual(row['sha256'],digest(MOD/row['source']))
    def test_ai_uses_verified_roles_dates_current_research_and_paid_existing_yards(self):
        designs=read(MOD/'common/ai_equipment/ac_naval_designs.txt');strategies=read(MOD/'common/ai_strategy/ac_naval_replacements.txt')
        for f in SHIPS:
            group=get(designs,'ac_naval_'+f.id+'_designs');self.assertEqual('naval',get(group,'category'))
            self.assertGreater(float(get(get(group,'priority'),'factor')),2*max(float(get(v['priority'],'factor','0')) for v in self.facts['native_design_groups'].values()))
            for year in YEARS:
                body=get(group,tech_id(f.id,year)+'_design');gate=get(body,'enable');tech={tech_id(f.id,year),tech_id('systems',year)}
                self.assertTrue(audit.condition(gate,(year,1,1),tech,{MTG}));self.assertFalse(audit.condition(gate,(year-1,12,31),tech,{MTG}))
                self.assertFalse(audit.condition(gate,(year,1,1),tech,set()))
                for missing in tech:self.assertFalse(audit.condition(gate,(year,1,1),tech-{missing},{MTG}))
                self.assertEqual(set(recipe(f.id,year).values()),{k for k,_,v in get(body,'allowed_modules')})
            gate=get(get(strategies,'ac_naval_'+f.id+'_replacement'),'enable');tech={tech_id(f.id,2006)}
            self.assertFalse(audit.condition(gate,(2006,1,1),tech,set(),yards=2));self.assertTrue(audit.condition(gate,(2006,1,1),tech,set(),yards=20))

class Economy(unittest.TestCase):
    def test_real_owner_bills_each_native_ship_class_and_actual_crew_once(self):
        facts=json.loads((HERE/'primary_contract.json').read_text());p=Primary.from_capture(facts['catalog'],audit.equipment(),audit.modules())
        for f in SHIPS:
            row=p.stats(model_id(f.id,2006));world=World();world.action('on_startup');c=world.countries['SNS'];crew=D(str(row['stats']['manpower']))/1000
            c.observables.update({'num_ships':1,'deployed_navy_manpower_k':crew,'num_ships_with_type@carrier':int(f.id=='carrier'),'num_ships_with_type@submarine':int(f.id=='submarine')})
            world.run('ac_macro_quote','SNS');expected=D('.08')+crew*D('.06')+(D('.8') if f.id=='carrier' else D('.02') if f.id=='submarine' else D(0))
            self.assertEqual(expected,c.variables['ac_macro_upkeep']*12);self.assertFalse(c.equipment)
    def test_aa_capital_screen_classifications_cannot_create_extra_ship_invoices(self):
        world=World();world.action('on_startup');c=world.countries['SNS']
        c.observables.update({'num_ships':1,'num_ships_with_type@capital':1,'num_ships_with_type@screen':1,'num_ships_with_type@anti_air':1})
        world.run('ac_macro_quote','SNS');self.assertEqual(D('.08'),c.variables['ac_macro_upkeep']*12)
    def test_disabled_mode_has_no_account_or_ship_grant(self):
        world=World(mode='disabled');world.action('on_startup');c=world.countries['SNS'];before=copy.deepcopy(c.variables);c.observables['num_ships']=20
        world.run('ac_macro_quote','SNS');self.assertEqual(before,c.variables);self.assertFalse(c.equipment)

class Presentation(unittest.TestCase):
    def test_all_actual_designer_controls_dimensions_apertures_and_selected_categories(self):
        from presentation import blueprint_contracts
        rows=blueprint_contracts();self.assertEqual(20,len(rows))
        self.assertTrue(all(r['container']==[512,260] and r['dimensions']==[508,248] and r['primary_structure_preserved'] for r in rows))
        self.assertTrue(all(s['normal'] and s['highlight'] for r in rows for s in r['selected_categories']))
    def test_actual_wrong_dds_frame_binding_and_required_control_fixtures_fail(self):
        from presentation import blueprint_contracts,named
        gfx=read(MOD/'interface/ac_naval_art.gfx');rows=get(gfx,'spriteTypes')
        target=next(b for _,_,b in rows if get(b,'name')=='"GFX_SD_ac_naval_escort_hull_2006"')
        setv(target,'texturefile','"gfx/AC_naval/modules/sonar_2006.dds"')
        with self.assertRaisesRegex(ValueError,'DDS/frame/scale'):blueprint_contracts(gfx=gfx)
        gfx=read(MOD/'interface/ac_naval_art.gfx');target=next(b for _,_,b in get(gfx,'spriteTypes') if get(b,'name')=='"GFX_SD_ac_naval_escort_hull_2006"');setv(target,'noOfFrames','2')
        with self.assertRaisesRegex(ValueError,'DDS/frame/scale'):blueprint_contracts(gfx=gfx)
        gui=read(MOD/'interface/equipmentdesigner/ships/ac_naval_blueprints.gui');window=named(gui,'equipment_designer_ac_naval_escort_hull_2006')
        setv(window,'name','"broken_required_window"')
        with self.assertRaises(StopIteration):blueprint_contracts(gui=gui)
        gui=read(MOD/'interface/equipmentdesigner/ships/ac_naval_blueprints.gui');window=named(gui,'equipment_designer_ac_naval_escort_hull_2006');setv(get(window,'size'),'width','511')
        with self.assertRaisesRegex(ValueError,'geometry/control'):blueprint_contracts(gui=gui)
    def test_actual_sprite_manifest_dds_alpha_original_sources_and_distinct_compositions(self):
        manifest=json.loads((HERE/'assets.json').read_text());self.assertEqual((273,333),(len(manifest['assets']),len(manifest['sprites'])))
        self.assertEqual(333,len({r['name'] for r in manifest['sprites']}));hashes={}
        for row in manifest['assets']:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as image:
                self.assertEqual((row['width'],row['height']),image.size);self.assertEqual(0,image.width%row['frames']);rgba=image.convert('RGBA')
                self.assertEqual((row['alpha_min'],row['alpha_max']),rgba.getchannel('A').getextrema())
                if row['role']!='deliberately transparent technical background':self.assertGreater(row['alpha_max'],0)
                bbox=rgba.getchannel('A').getbbox();self.assertEqual(row['alpha_bbox'],list(bbox) if bbox else None)
                self.assertFalse(any(r>150 and g>120 and b<90 and a>0 for r,g,b,a in rgba.getdata()),row['file'])
                if row['frames']>1:self.assertEqual(row['frames'],len({rgba.crop((i*row['frame_width'],0,(i+1)*row['frame_width'],image.height)).tobytes() for i in range(row['frames'])}))
            if row.get('source'):self.assertEqual(row['source_sha256'],digest(ROOT/row['source']))
            if row['role'] in ('original research composition','original equipment composition','original designer module composition'):hashes.setdefault(row['role'],[]).append(row['sha256'])
        for role,values in hashes.items():self.assertEqual(len(values),len(set(values)),role)
        self.assertEqual(250,len(list((HERE/'source/art').glob('*.svg'))))
    def test_english_names_descriptions_technology_and_module_consumers_resolve(self):
        path=MOD/'localisation/english/ac_naval_program_l_english.yml';raw=path.read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        pairs=re.findall(r'^\s*(\w+):0\s+"([^"]*)"',raw.decode('utf-8-sig'),re.M);strings=dict(pairs);self.assertEqual(len(pairs),len(strings))
        sprites={r['name'] for r in json.loads((HERE/'assets.json').read_text())['sprites']}
        for ident in audit.technologies():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_'+ident+'_medium',sprites)
        for ident in audit.equipment():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_'+ident,sprites)
        for ident in audit.modules():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_EMI_'+ident,sprites)
    def test_authored_content_art_capability_and_review_are_reproducible(self):
        for name in ('build.py','build_ui.py','build_art.py','audit.py','render_review.py'):
            result=subprocess.run([sys.executable,'-B',str(HERE/name),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)

class ResearchUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('tested_naval_ui_owner',HERE/'build_ui.py');cls.ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.ui)
        spec=importlib.util.spec_from_file_location('tested_air_composition_owner',ROOT/'tools/air_program/build_ui.py');cls.air=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.air)
    def test_all_six_generation_orders_produce_one_identical_canonical_gui(self):
        text,templates,contract=self.ui.land.generated();land={self.ui.land.TARGET:text.encode(),MOD/'interface/ac_land_techtree.gui':templates.encode(),ROOT/'tools/land_program/ui_contract.json':contract.encode()}
        sets=[land,self.air.outputs(),self.ui.outputs()];canonical=None
        for order in itertools.permutations(sets):
            output={}
            for files in order:output.update(files)
            if canonical is None:canonical=output
            self.assertEqual(canonical,output)
            for path,raw in output.items():self.assertEqual(raw,path.read_bytes().replace(b'\r\n',b'\n'))
    def test_whole_original_gui_font_fingerprint_and_required_scrolls_are_preserved(self):
        from presentation import named
        tree=read(MOD/'interface/countrytechtreeview.gui');original=read(self.ui.land.SOURCE);self.assertEqual(original,self.ui.land.normalized(tree))
        folder=named(tree,'ac_naval_folder');self.assertEqual('"ac_exp_right_vertical_slider"',get(folder,'verticalScrollbar'));self.assertEqual('"ac_exp_bottom_horizontal_slider"',get(folder,'horizontalScrollbar'))
        self.assertEqual(['left','middle'],[k for k,_,v in get(folder,'drag_scroll')]);self.assertEqual('40',get(folder,'scroll_wheel_factor'))
        self.assertNotRegex((HERE/'naval_ui.py').read_text(),r'editboxType|name\s*=\s*"search"')
        bad=copy.deepcopy(tree);get(bad,'guiTypes').append(['containerWindowType','=',[['name','=','"unregistered_naval_window"']]])
        with self.assertRaisesRegex(ValueError,'Unregistered'):self.ui.land.normalized(bad)
    def test_actual_card_and_three_display_geometry_and_font_metrics(self):
        spec=importlib.util.spec_from_file_location('naval_actual_review',HERE/'render_review.py');review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)
        _,report=review.render();self.assertEqual([],report['findings']);self.assertEqual((24,20,3),(len(report['node_rectangles']),len(report['blueprints']),len(report['display_cases'])))
        self.assertTrue(all(c['tab_inside'] and c['last_node_reachable'] for c in report['display_cases']))
        atlas=review.land_review.Atlas('ACBriefing16');strings=review.strings()
        for ident in audit.technologies():self.assertLessEqual(len(atlas.wrap(strings[ident],175))*atlas.height,36)

class SourceReceipts(unittest.TestCase):
    def test_exact_receipt_cannot_relabel_retained_partial_results(self):
        result=subprocess.run([sys.executable,'-B',str(HERE/'run_checks.py'),'--exact-source','--only','naval'],cwd=ROOT,capture_output=True,text=True)
        self.assertNotEqual(0,result.returncode);self.assertIn('requires a full run',result.stdout+result.stderr)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path);args,rest=parser.parse_known_args();ENGINE=args.engine
    unittest.main(argv=[sys.argv[0],*rest],verbosity=2)
