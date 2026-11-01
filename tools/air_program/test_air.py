"""Actual aviation sources and captured-primary replay; no native acceptance."""
import argparse
import copy
import io
import importlib.util
from decimal import Decimal as D
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/economy_v2')]
from script import parse,get,walk,setv
from air_content import FAMILIES,AIRCRAFT,YEARS,TECHS,MODULES,BBA,LAR,ROLE_PRESENTATION,tech_id,model_id,frame_id,recipe,common_dependencies
from air_primary import Primary,STATS
import audit
from harness import World
ENGINE=None


def ids(nodes):return {k for k,_,_ in nodes}
def read(path):return parse(path.read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


class Captured(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts=json.loads((HERE/'primary_contract.json').read_text());cls.tech=audit.technologies();cls.gear=audit.equipment();cls.parts=audit.modules()
        cls.primary=Primary.from_capture(cls.facts['replay_catalog'],cls.gear,cls.parts)


class Definitions(Captured):
    def test_older_aviation_surfaces_are_exactly_retained_and_declared(self):
        rows=audit.report()['retained_aviation_surfaces']
        self.assertEqual([38,41],[len(row['technologies']) for row in rows])
        for row in rows:
            self.assertEqual(digest(MOD/row['source']),row['source_sha256'])
            self.assertIn('not a completed',row['disposition'])
        old={r['id'] for row in rows for r in row['technologies']}
        self.assertTrue({'jet_fighter2','modern_small_airframe','photo_reconnaisance','jet_strategic_bomber1'}<=old)
        self.assertFalse(old&set(self.tech))

    def test_inventory_namespaces_and_existing_owners(self):
        self.assertEqual(24,len(self.tech));self.assertEqual(36,len(self.gear));self.assertEqual(32,len(self.parts))
        self.assertTrue(all(i.startswith('ac_air_') for i in [*self.tech,*self.gear,*self.parts]))
        for path in (MOD/'common/technologies').glob('*.txt'):
            if path.name!='ac_air_program.txt':self.assertFalse(set(self.tech)&ids(get(read(path),'technologies',[])))
        for ident,body in self.gear.items():self.assertEqual('no',get(body,'active'));self.assertNotIn('is_archetype',ids(body))

    def test_hard_date_dependencies_and_first_tier_dlc_foundations(self):
        all_foundations=set(self.facts['foundations'])
        for row in TECHS:
            body=self.tech[row['id']];required=set(common_dependencies(row['family'],row['tier']))
            self.assertEqual(required,ids(get(body,'dependencies')))
            self.assertEqual(str(row['year']),get(body,'start_year'));self.assertGreater(float(get(body,'research_cost')),0)
            self.assertEqual('ac_air_folder',get(get(body,'folder'),'name'))
            research=all_foundations|set(self.tech)
            for bba in (False,True):
                dlc=({BBA} if bba else set())|{LAR}
                self.assertFalse(audit.condition(get(body,'allow'),(row['year']-1,12,31),research,dlc))
                self.assertTrue(audit.condition(get(body,'allow'),(row['year'],1,1),research,dlc))
                for missing in required:self.assertFalse(audit.condition(get(body,'allow'),(row['year'],1,1),research-{missing},dlc))
        for family in AIRCRAFT:
            if not family.legacy_foundation:continue
            body=self.tech[tech_id(family.id,2006)];research=all_foundations|{tech_id('systems',2006)}
            for bba in (False,True):
                dlc=({BBA} if bba else set())|{LAR};missing=family.designer_foundation if bba else family.legacy_foundation
                self.assertFalse(audit.condition(get(body,'allow'),(2006,1,1),research-{missing},dlc),(family.id,bba))
            if family.id=='surveillance':self.assertFalse(audit.condition(get(body,'allow'),(2006,1,1),research-{'photo_reconnaisance'},{BBA,LAR}))

    def test_dated_closure_and_lar_disabled_optional_branch(self):
        for year,tiers in [(1991,0),(2005,0),(2006,1),(2010,2),(2015,3),(2020,4),(2030,4)]:
            for bba in (False,True):
                for lar in (False,True):
                    dlc=({BBA} if bba else set())|({LAR} if lar else set())
                    done=audit.closure(year,dlc,self.tech,self.facts['foundations'])&set(self.tech)
                    self.assertEqual(tiers*(6 if lar else 5),len(done),(year,bba,lar))
                    if not lar:self.assertFalse(any(i.startswith('ac_air_surveillance') for i in done))
        for family in FAMILIES:
            for index,year in enumerate(YEARS):
                children=[get(v,'leads_to_tech') for k,_,v in self.tech[tech_id(family.id,year)] if k=='path']
                self.assertEqual([] if index==3 else [tech_id(family.id,YEARS[index+1])],children)

    def test_all_16_dlc_profiles_have_one_paid_supported_route(self):
        report=audit.report(ENGINE);self.assertEqual([],report['errors']);self.assertEqual(16,len(report['independent_DLC_profiles']))
        for case in report['independent_DLC_profiles']:
            self.assertEqual(20 if case['lar'] else 16,len(case['eligible_2020_models']))
            for year in YEARS:
                self.assertIn(model_id('transport',year),case['eligible_2020_models'])
                for family in AIRCRAFT:
                    options={model_id(family.id,year)}|({frame_id(family.id,year)} if family.airframe_parent else set())
                    self.assertEqual(0 if family.id=='surveillance' and not case['lar'] else 1,len(options&set(case['eligible_2020_models'])))
        self.assertFalse(report['native_acceptance'])

    def test_default_recipes_have_actual_slots_limits_thrust_cost_and_physical_parity(self):
        p=self.primary
        for family in AIRCRAFT:
            for year in YEARS:
                legacy=p.stats(model_id(family.id,year));self.assertGreater(legacy['stats']['build_cost_ic'],0)
                self.assertGreater(legacy['stats']['fuel_consumption'],0);self.assertGreater(legacy['stats']['manpower'],0)
                self.assertTrue(all(v>0 for v in legacy['resources'].values()))
                if not family.airframe_parent:continue
                ident=frame_id(family.id,year);selected=recipe(family.id,year);contract=p.design(ident,selected);designer=p.stats(ident,selected)
                self.assertEqual(3,len(contract['slots']));self.assertGreater(len(contract['module_count_limits']),4)
                self.assertEqual([family.equipment_type],contract['effective_module_roles'])
                for key in STATS:self.assertAlmostEqual(legacy['stats'][key],designer['stats'][key],places=6)
                self.assertEqual(legacy['resources'],designer['resources']);self.assertGreaterEqual(designer['stats']['thrust'],designer['stats']['weight'])
        maritime=p.stats(frame_id('maritime',2020),recipe('maritime',2020))
        self.assertEqual(36,maritime['stats']['naval_strike_attack']);self.assertEqual(21,maritime['stats']['naval_strike_targetting'])

    def test_real_offense_is_present_for_declared_combat_roles(self):
        for family,stat in [('fighter','air_attack'),('strike','air_ground_attack'),('maritime','naval_strike_attack')]:
            for year in YEARS:self.assertGreater(self.primary.stats(model_id(family,year))['stats'][stat],0)
        for year in YEARS:
            scout=self.primary.stats(model_id('surveillance',year))
            self.assertEqual(0,scout['stats']['naval_strike_attack']);self.assertEqual(0,scout['stats']['air_superiority'])
            self.assertGreater(scout['stats']['surface_detection'],0)

    def test_priority_role_icons_and_native_air_upkeep_lineage(self):
        for family in AIRCRAFT:
            for year in YEARS:
                models=[model_id(family.id,year)]+([frame_id(family.id,year)] if family.airframe_parent else [])
                for ident in models:
                    row=self.facts['equipment'][ident];self.assertGreater(int(row['priority']),int(row['parent_priority'] or 0))
                    self.assertEqual('interface_category_air',row['interface_category']);self.assertEqual('archetype',row['group_by'])
                    self.assertEqual(family.archetype,row['archetype']);self.assertEqual(family.equipment_type,row['equipment_type'])
                    frame,index,sprite=ROLE_PRESENTATION[family.id]
                    self.assertEqual((str(frame),str(index),sprite),(row['air_map_icon_frame'],row['interface_overview_category_index'],row['sprite']))

    def test_mission_vocabulary_and_mining_difference_are_explicit(self):
        report=audit.report();vocabulary=set(self.facts['native_mission_vocabulary'])
        self.assertIn('attack_logistics',vocabulary);self.assertNotIn('logistics_strike',vocabulary)
        for row in report['default_physical_parity']:
            self.assertFalse(row['native_mission_equivalence'])
            self.assertTrue(set(row['legacy_missions'])<=vocabulary);self.assertTrue(set(row['designer_default_missions'])<=vocabulary)
            if row['family']=='maritime':self.assertEqual(['naval_mines_planting','naval_mines_sweeping'],row['legacy_only_source_missions'])
            else:self.assertEqual([],row['legacy_only_source_missions'])
        for year in YEARS:
            scouts=[model_id('surveillance',year),frame_id('surveillance',year)]
            for ident in scouts:self.assertFalse(audit.condition(get(self.gear[ident],'can_be_produced'),(2020,1,1),set(self.tech),{BBA}))

    def test_unknown_mission_cannot_be_blessed_by_capture_or_checker(self):
        bad=copy.deepcopy(self.facts);bad['equipment'][model_id('fighter',2006)]['declared_missions'].append('logistics_strike')
        original=Path.read_text
        def source(path,*args,**kwargs):return json.dumps(bad) if path==HERE/'primary_contract.json' else original(path,*args,**kwargs)
        with patch.object(Path,'read_text',source):self.assertTrue(any('Unknown mission token' in r for r in audit.report()['errors']))

    def test_research_does_not_seed_histories_forces_or_other_owners(self):
        forbidden={'set_technology','load_oob','add_equipment_to_stockpile','create_equipment_variant','create_unit','set_country_flag',
                   'set_global_flag','transfer_state','load_focus_tree','declare_war_on','add_to_faction','country_event'}
        for relative in ('common/technologies/ac_air_program.txt','common/ai_equipment/ac_air_designs.txt','common/ai_strategy/ac_air_replacements.txt','common/ai_strategy_plans/ac_air_research.txt'):
            tree=read(MOD/relative)
            self.assertFalse(forbidden&{k for body in [tree]+[v for _,v in walk(tree)] for k,_,_ in body},relative)
        text=(MOD/'common/technologies/ac_air_program.txt').read_text()
        self.assertNotIn('ac_wl_transport_support',text);self.assertNotIn('ac_sp_',text)
        baseline=json.loads((HERE/'preserved_sources.json').read_text())
        updates=json.loads((HERE/'reviewed_owner_updates.json').read_text())['files']
        for path,expected in baseline['sources'].items():
            update=updates.get(path)
            if update:self.assertEqual(expected,update['old_sha256'],path)
            self.assertEqual(update['new_sha256']if update else expected,digest(ROOT/path),path)

    def test_reviewed_release_owner_delta_matches_canonical_generator(self):
        updates=json.loads((HERE/'reviewed_owner_updates.json').read_text());files=updates['files']
        prefix='mod/2985041246/common/scripted_effects/'
        self.assertEqual({prefix+'ac_economy_compat.txt',prefix+'ac_macro_effects.txt'},set(files))
        expected={prefix+'ac_economy_compat.txt':({'ac_econ_initialize'},{'ac_econ_adopt_release_account','ac_econ_try_fund_release_project'}),
                  prefix+'ac_macro_effects.txt':({'ac_macro_initialize'},set())}
        for path,row in files.items():
            self.assertEqual([],row['removed']);self.assertEqual(expected[path],(set(row['changed']),set(row['added'])))
            current={key:value for key,_,value in read(ROOT/path)}
            old=row['unchanged_function_ast_sha256'];reviewed=row['reviewed_function_ast_sha256']
            self.assertEqual(set(current),set(old)|set(reviewed))
            self.assertFalse(set(old)&set(reviewed))
            for name,body in current.items():
                actual=hashlib.sha256(json.dumps(body,separators=(',',':')).encode()).hexdigest()
                self.assertEqual((reviewed if name in reviewed else old)[name],actual,(path,name))
        result=subprocess.run([sys.executable,'-B','tools/economy_v2/build.py','--check'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_ai_designs_require_research_current_components_dates_and_dlc(self):
        groups=read(MOD/'common/ai_equipment/ac_air_designs.txt')
        for ident,_,body in groups:
            family=ident.removeprefix('ac_air_').removesuffix('_designs')
            mods=[v for k,_,v in get(body,'priority') if k=='modifier']
            self.assertTrue(any(audit.condition([n for n in m if n[0]!='factor'],(1991,1,1),set(),set()) for m in mods))
            for key,_,design in body:
                if not key.startswith('ac_air_'):continue
                year=int(key.split('_')[-2]);required={tech_id(family,year),tech_id('systems',year)};dlc={BBA,LAR}
                self.assertTrue(audit.condition(get(design,'enable'),(year,1,1),required,dlc))
                self.assertFalse(audit.condition(get(design,'enable'),(year-1,12,31),required,dlc))
                self.assertFalse(audit.condition(get(design,'enable'),(year,1,1),required,set()))
                for missing in required:self.assertFalse(audit.condition(get(design,'enable'),(year,1,1),required-{missing},dlc))
                if family=='surveillance':self.assertFalse(audit.condition(get(design,'enable'),(year,1,1),required,{BBA}))
                self.assertEqual(set(recipe(family,year).values()),ids(get(design,'allowed_modules')))

    def test_transport_buffer_is_paid_capacity_bound_and_not_an_unsupported_role_token(self):
        strategies=read(MOD/'common/ai_strategy/ac_air_replacements.txt');body=get(strategies,'ac_air_transport_buffer');gate=get(body,'enable')
        research={tech_id('transport',2006)}
        self.assertFalse(audit.condition(gate,(2006,1,1),research,set(),mil=20))
        self.assertTrue(audit.condition(gate,(2006,1,1),research,set(),mil=21))
        self.assertFalse(audit.condition(gate,(2006,1,1),research,set(),{'transport_plane_equipment':21},mil=21))
        self.assertFalse(audit.condition(gate,(1991,1,1),research,set(),mil=50))
        self.assertEqual('equipment_production_min_factories_archetype',get(get(body,'ai_strategy'),'type'))
        self.assertEqual('transport_plane_equipment',get(get(body,'ai_strategy'),'id'));self.assertEqual('1',get(get(body,'ai_strategy'),'value'))


class PrimarySemantics(Captured):
    def test_real_material_cost_and_parity_mutations_are_rejected(self):
        gear=copy.deepcopy(self.gear);ident=model_id('fighter',2006)
        setv(gear[ident],'build_cost_ic','1')
        with patch.object(audit,'equipment',lambda:gear):
            self.assertTrue(any('Current equipment differs' in v for v in audit.report()['errors']))
        gear=copy.deepcopy(self.gear);setv(get(gear[ident],'resources'),'aluminium','-1')
        with patch.object(audit,'equipment',lambda:gear):
            self.assertTrue(any('Non-positive complete aircraft material' in v for v in audit.report()['errors']))
        p=copy.deepcopy(self.primary);selected=recipe('fighter',2006)
        module=p.modules[selected['engine_type_slot']]
        setv(get(module,'build_cost_resources'),'aluminium','-100')
        with self.assertRaisesRegex(ValueError,'Non-positive configured aircraft material'):p.design(frame_id('fighter',2006),selected)
        p=copy.deepcopy(self.primary);setv(p.equipment[frame_id('fighter',2006)],'build_cost_ic','-1000')
        with self.assertRaisesRegex(ValueError,'Unfunded configured aircraft'):p.design(frame_id('fighter',2006),selected)

    def test_missing_required_wrong_category_and_excess_weapons_fail(self):
        p=copy.deepcopy(self.primary);ident=frame_id('fighter',2006);selected=recipe('fighter',2006)
        missing={k:v for k,v in selected.items() if k!='engine_type_slot'}
        with self.assertRaisesRegex(ValueError,'Missing required'):p.design(ident,missing)
        wrong={**selected,'engine_type_slot':selected['fixed_main_weapon_slot']}
        with self.assertRaisesRegex(ValueError,'Incompatible module category'):p.design(ident,wrong)
        excess={**selected,'fixed_auxiliary_weapon_slot_1':selected['fixed_main_weapon_slot']}
        with self.assertRaisesRegex(ValueError,'count limit exceeded'):p.design(ident,excess)

    def test_zero_thrust_and_multiple_averaged_contributors_fail(self):
        p=copy.deepcopy(self.primary);ident=frame_id('fighter',2006);selected=recipe('fighter',2006)
        engine=p.modules[selected['engine_type_slot']];setv(get(engine,'add_stats'),'thrust','0')
        with self.assertRaisesRegex(ValueError,'Insufficient aircraft thrust'):p.design(ident,selected)
        selected=recipe('maritime',2006);selected['fixed_auxiliary_weapon_slot_1']=selected['fixed_main_weapon_slot']
        with self.assertRaisesRegex(ValueError,'Multiple averaged contributors'):self.primary.stats(frame_id('maritime',2006),selected)

    def test_unhandled_hull_multiplier_fails_instead_of_disappearing(self):
        p=copy.deepcopy(self.primary);ident=frame_id('fighter',2006)
        p.equipment[ident].append(['module_add_stats_multiplier','=',[['air_attack','=','0.5']]])
        with self.assertRaisesRegex(ValueError,'Uninspected aircraft-specific module multiplier'):p.stats(ident,recipe('fighter',2006))

    def test_synthetic_duplicate_keeps_type_for_each_and_mission_overrides(self):
        p=self.primary
        self.assertEqual('cas',p.resolve('small_plane_cas_airframe_1')['type'])
        scout=p.resolve('medium_plane_scout_plane_airframe_4');self.assertEqual('scout_plane',scout['type'])
        self.assertEqual('0',scout['air_superiority']);self.assertIn('training',scout['forbid_mission_type'])

    def test_every_repeated_module_limit_survives_and_first_limit_is_enforced(self):
        p=copy.deepcopy(self.primary);ident=frame_id('fighter',2006);body=p.equipment[ident]
        early=['module_count_limit','=',[['category','=','plane_jet_engine_type'],['count','<','1']]]
        late=['module_count_limit','=',[['category','=','recon_camera'],['count','<','2']]]
        body.extend([early,late]);limits=p.resolve(ident)['module_count_limit']
        self.assertEqual(early[2],limits[-2]);self.assertEqual(late[2],limits[-1])
        with self.assertRaisesRegex(ValueError,'plane_jet_engine_type'):p.design(ident,recipe('fighter',2006))


class Economy(unittest.TestCase):
    def test_actual_owner_charges_every_supported_native_air_role(self):
        facts=json.loads((HERE/'primary_contract.json').read_text())
        premiums={'fighter':D('.002'),'cas':D('.001'),'naval_bomber':D('.003'),'air_transport':D('.004'),'scout_plane':D(0)}
        for family in AIRCRAFT:
            row=facts['equipment'][model_id(family.id,2006)];world=World();world.action('on_startup');country=world.countries['SNS']
            country.observables.update({'num_deployed_planes':1,'deployed_airforce_manpower_k':D(str(row['stats']['manpower']))/1000,
                                        'num_deployed_planes_with_type@'+family.equipment_type:1})
            world.run('ac_macro_quote','SNS');expected=D('.008')+premiums[family.equipment_type]+D(str(row['stats']['manpower']))/1000*D('.06')
            self.assertEqual(expected,country.variables['ac_macro_upkeep']*12);self.assertFalse(country.equipment)

    def test_actual_owner_does_not_double_charge_multirole_aircraft(self):
        world=World();world.action('on_startup');c=world.countries['SNS']
        c.observables.update({'num_deployed_planes':1,'num_deployed_planes_with_type@fighter':1,'num_deployed_planes_with_type@cas':1,
                              'num_deployed_planes_with_type@naval_bomber':1})
        world.run('ac_macro_quote','SNS');self.assertEqual(D('.011'),c.variables['ac_macro_upkeep']*12)
        self.assertFalse(c.equipment)

    def test_disabled_fiscal_mode_does_not_write_account_or_aircraft(self):
        world=World(mode='disabled');world.action('on_startup');c=world.countries['SNS'];before=copy.deepcopy(c.variables)
        c.observables['num_deployed_planes']=20;world.run('ac_macro_quote','SNS')
        self.assertEqual(before,c.variables);self.assertFalse(c.equipment)


class Presentation(unittest.TestCase):
    def test_actual_blueprint_controls_consume_exact_508x248_overlays(self):
        from presentation import blueprint_contracts
        rows=blueprint_contracts();self.assertEqual(16,len(rows));self.assertEqual(16,len({r['control'] for r in rows}))
        for row in rows:self.assertEqual([508,248],row['dimensions']);self.assertEqual(1,row['frames'])

    def test_wrong_blueprint_dimensions_or_alias_fail_actual_consumer(self):
        from presentation import blueprint_contracts
        gui=read(MOD/'interface/equipmentdesigner/planes/ac_air_blueprints.gui')
        first=get(gui,'guiTypes')[0][2];setv(get(first,'size'),'width','507')
        with self.assertRaisesRegex(ValueError,'primary508x248'):blueprint_contracts(gui=gui)
        gui=read(MOD/'interface/equipmentdesigner/planes/ac_air_blueprints.gui');first=get(gui,'guiTypes')[0][2]
        setv(next(v for _,v in walk([['window','=',first]]) if get(v,'name')=='"equipment_image_overlay"'),'spriteType','"GFX_TC_ac_air_strike_airframe_2006"')
        with self.assertRaisesRegex(ValueError,'consumer binding'):blueprint_contracts(gui=gui)
        gfx=read(MOD/'interface/ac_air_art.gfx');definition=next(body for _,_,body in get(gfx,'spriteTypes') if get(body,'name')=='"GFX_TC_ac_air_fighter_airframe_2006"')
        setv(definition,'texturefile','"gfx/AC_air/modules/camera_2006.dds"')
        with self.assertRaisesRegex(ValueError,'DDS/control bounds mismatch'):blueprint_contracts(gfx=gfx)

    def test_all_original_dds_svg_alpha_frames_and_distinct_subjects(self):
        data=json.loads((HERE/'assets.json').read_text());self.assertEqual(94,len(data['assets']));self.assertEqual(146,len(data['sprites']))
        self.assertEqual(146,len({r['name'] for r in data['sprites']}));self.assertEqual(56,len(list((HERE/'source/art').glob('*.svg'))))
        hashes={}
        for row in data['assets']:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as im:
                self.assertEqual((row['width'],row['height']),im.size);self.assertEqual(0,im.width%row['frames'])
                rgba=im.convert('RGBA');self.assertEqual((row['alpha_min'],row['alpha_max']),rgba.getchannel('A').getextrema())
                self.assertFalse(any(r>150 and g>120 and b<90 and a>0 for r,g,b,a in rgba.getdata()),row['file'])
                if row['frames']>1:
                    frames={rgba.crop((i*row['frame_width'],0,(i+1)*row['frame_width'],im.height)).tobytes() for i in range(row['frames'])}
                    self.assertEqual(row['frames'],len(frames))
                if row['role'] not in ('original four-frame research tab','original tiled briefing background'):self.assertEqual(0,rgba.getpixel((0,0))[3])
            if 'source' in row:self.assertEqual(row['source_sha256'],digest(ROOT/row['source']))
            if 'composition' in row['role'] or 'blueprint' in row['role']:hashes.setdefault(row['role'],[]).append(row['sha256'])
        for role,values in hashes.items():self.assertEqual(len(values),len(set(values)),role)

    def test_english_names_descriptions_module_and_equipment_consumers_resolve(self):
        path=MOD/'localisation/english/ac_air_program_l_english.yml';raw=path.read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        strings=dict(re.findall(r'^\s*(\w+):0\s+"([^"]*)"',raw.decode('utf-8-sig'),re.M));keys=re.findall(r'^\s*(\w+):0',raw.decode('utf-8-sig'),re.M)
        self.assertEqual(len(keys),len(set(keys)));sprites={r['name'] for r in json.loads((HERE/'assets.json').read_text())['sprites']}
        for ident in audit.technologies():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_'+ident+'_medium',sprites)
        for ident in audit.equipment():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_'+ident,sprites)
        for ident in audit.modules():self.assertTrue(strings[ident]);self.assertTrue(strings[ident+'_desc']);self.assertIn('GFX_EMI_'+ident,sprites)

    def test_authored_content_and_art_are_reproducible(self):
        for script in ('build.py','build_ui.py','build_art.py','audit.py','render_review.py'):
            result=subprocess.run([sys.executable,'-B',str(HERE/script),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)


class ResearchUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('tested_air_ui_owner',HERE/'build_ui.py')
        cls.owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.owner)
        cls.land=cls.owner.land;cls.gui=read(MOD/'interface/countrytechtreeview.gui')

    def test_land_and_air_generators_compose_in_either_order(self):
        value,templates,contract=self.land.generated()
        land={self.land.TARGET:value.encode(),MOD/'interface/ac_land_techtree.gui':templates.encode(),ROOT/'tools/land_program/ui_contract.json':contract.encode()}
        air=self.owner.outputs();self.assertEqual(land[self.land.TARGET],air[self.land.TARGET])
        self.assertEqual({**land,**air},{**air,**land})
        for order in ((land,air),(air,land)):
            result={}
            for files in order:result.update(files)
            for path,data in result.items():self.assertEqual(data,path.read_bytes().replace(b'\r\n',b'\n'))

    def test_original_fingerprint_font_restoration_and_unknown_nodes(self):
        original=read(self.land.SOURCE);self.assertEqual(original,self.land.normalized(self.gui))
        bad=copy.deepcopy(self.gui);get(bad,'guiTypes').append(['containerWindowType','=',[['name','=','"unregistered_air_window"']]])
        with self.assertRaisesRegex(ValueError,'Unregistered research GUI structure'):self.land.normalized(bad)
        import air_ui
        from research_fonts.migration import migrate
        expected=parse(migrate((HERE/'source/research_land_base.gui').read_text()))
        stripped=air_ui.strip(self.gui);navy=self.land.naval_extension()
        if navy:
            self.assertEqual({'ac_naval_folder','ac_naval_folder_tab'},navy.NAMES)
            stripped=navy.strip(stripped)
        self.assertEqual(expected,stripped)
        with self.assertRaisesRegex(ValueError,'applied twice'):air_ui.extend((MOD/'interface/countrytechtreeview.gui').read_text())

    def test_actual_card_controls_fonts_icons_and_scroll_bindings(self):
        from presentation import named
        folder=named(self.gui,'ac_air_folder');self.assertTrue(get(folder,'verticalScrollbar'));self.assertTrue(get(folder,'horizontalScrollbar'))
        self.assertEqual({'left','middle'},ids(get(folder,'drag_scroll')));self.assertEqual('40',get(folder,'scroll_wheel_factor'))
        for kind,body in walk(folder):
            self.assertNotIn(kind.lower(),('editboxtype','searchbox'))
            for field in ('font','buttonFont'):
                if get(body,field):self.assertIn(get(body,field),('"ACBriefing16"','"ACBriefing20"'))
        for template in ('techtree_ac_air_folder_item','techtree_ac_air_folder_small_item'):
            card=named(read(MOD/'interface/ac_air_techtree.gui'),template)
            controls={get(body,'name','').strip('"') for _,body in walk([['card','=',card]]) if isinstance(get(body,'name',''),str)}
            self.assertTrue({'Name','Icon','Background','bonus','bonus_icon','can_assign_design_team_icon','special_project_specialization_list'}<=controls)
            label=named([['card','=',card]],'Name');icon=named([['card','=',card]],'Icon')
            title_bottom=int(get(get(label,'position'),'y'))+int(get(label,'maxHeight'));icon_top=int(get(get(icon,'position'),'y'))-20
            self.assertLess(title_bottom,icon_top)
        boxes=[body for _,body in walk(self.gui) if get(body,'name')=='"tech_info_description"']
        self.assertEqual(2,len(boxes));self.assertTrue(all(get(b,'scrollbarType')=='"ac_exp_standardtext_slider"' for b in boxes))

    def test_actual_reconstruction_all_24_nodes_and_three_display_cases(self):
        spec=importlib.util.spec_from_file_location('tested_air_review',HERE/'render_review.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        _,report=module.render();self.assertEqual([],report['findings']);self.assertEqual(24,len(report['node_rectangles']))
        self.assertEqual(16,len(report['blueprints']));self.assertFalse(report['native_acceptance'])
        self.assertEqual(3,len(report['display_cases']))
        for case in report['display_cases']:self.assertTrue(case['tab_inside']);self.assertTrue(case['last_node_reachable'])
        atlas=module.land_review.Atlas('ACBriefing16');strings=module.strings()
        for ident in audit.technologies():self.assertLessEqual(len(atlas.wrap(strings[ident],175))*atlas.height,36)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path);args,rest=parser.parse_known_args();ENGINE=args.engine
    unittest.main(argv=[sys.argv[0],*rest],verbosity=2)
