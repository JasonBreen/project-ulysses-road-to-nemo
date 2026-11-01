"""Actual additive land definitions, physical routes and retained-start contracts.

These tests execute source/owner fixtures and inspect authored DDS/control data.
They do not establish native research, designer, AI or save compatibility.
"""
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

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/economy_v2')]
from script import parse,get,walk
from land_content import FAMILIES,YEARS,TECHS,AI_TARGET_TECHS,AI_TARGET_STOCKS,recipe,model_id,chassis_id,prerequisites
import audit
spec=importlib.util.spec_from_file_location('land_ui',HERE/'build_ui.py');build_ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(build_ui)
from render_review import Atlas,locs,render,named,pos
from PIL import Image
from harness import World
from forces import DATA,observable_names

ENGINE=None
def read(path):return parse(path.read_text(encoding='utf-8-sig'))
def ids(nodes):return {k for k,_,_ in nodes}
def sha(path):return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


class Land(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tech=audit.new_techs();cls.gear=audit.new_equipment();cls.modules=audit.new_modules()
        cls.facts=json.loads((HERE/'primary_contract.json').read_text())
        cls.art=json.loads((HERE/'assets.json').read_text())

    def test_real_authored_inventory_and_unique_ids(self):
        self.assertEqual(32,len(self.tech));self.assertEqual(42,len(self.gear));self.assertEqual(36,len(self.modules))
        self.assertEqual(2,sum(get(b,'is_archetype')=='yes' for b in self.gear.values()))
        for row in TECHS:self.assertIn(row['id'],self.tech)
        for ident in [*self.tech,*self.gear,*self.modules]:self.assertTrue(ident.startswith('ac_land_'))
        for path in (MOD/'common/technologies').glob('*.txt'):
            if path.name=='ac_land_program.txt':continue
            self.assertFalse(set(self.tech)&ids(get(read(path),'technologies',[])),str(path))

    def test_every_node_has_paid_dated_prerequisites_and_a_real_effect(self):
        for row in TECHS:
            body=self.tech[row['id']];year=row['year'];required=set(prerequisites(row['family'],row['tier']))
            self.assertEqual(str(year),get(body,'start_year'));self.assertGreater(float(get(body,'research_cost')),1)
            self.assertEqual(required,ids(get(body,'dependencies')))
            self.assertEqual(required,{v for k,_,v in get(body,'allow') if k=='has_tech'})
            dates=[(op,v) for k,op,v in get(body,'allow') if k=='date']
            self.assertEqual([('>',f'"{year-1}.12.31"')],dates)
            self.assertFalse(audit.condition(get(body,'allow'),(year-1,12,31),required,set()))
            self.assertTrue(audit.condition(get(body,'allow'),(year,1,1),required,set()))
            for missing in required:
                self.assertFalse(audit.condition(get(body,'allow'),(year,1,1),required-{missing},set()))
            self.assertTrue(get(body,'enable_equipments'))
            self.assertEqual('ac_land_folder',get(get(body,'folder'),'name'))
            self.assertTrue(ids(get(body,'enable_equipments'))<=self.gear.keys())
            self.assertTrue(ids(get(body,'enable_equipment_modules',[]))<=self.modules.keys())

    def test_dates_and_topology_block_preparation_then_reach_all_four_tiers(self):
        for year,count in [(1991,0),(2005,0),(2006,8),(2010,16),(2015,24),(2020,32),(2030,32)]:
            research=audit.researched_by(year,self.tech,self.facts['existing_prerequisites'])
            self.assertEqual(count,len(set(self.tech)&research),year)
        for family in FAMILIES:
            for index,year in enumerate(YEARS):
                body=self.tech[f'ac_land_{family.id}_{year}'];children=[get(b,'leads_to_tech') for k,_,b in body if k=='path']
                self.assertEqual([] if index==3 else [f'ac_land_{family.id}_{YEARS[index+1]}'],children)

    def test_no_start_grants_or_calendar_owners_are_introduced(self):
        forbidden={'add_equipment_to_stockpile','load_oob','set_technology','create_unit','add_building_construction',
                   'transfer_state','declare_war_on','load_focus_tree','set_global_flag','set_country_flag','country_event'}
        for folder in ('common/technologies','common/units','common/ai_equipment','common/ai_strategy','common/ai_templates'):
            for path in (MOD/folder).rglob('*ac_land*.txt'):
                tree=read(path)
                self.assertFalse(forbidden&{k for b in [tree]+[v for _,v in walk(tree)] for k,_,_ in b},str(path))
        for body in self.gear.values():
            if get(body,'is_archetype')!='yes':self.assertEqual('no',get(body,'active'))

    def test_all_16_dlc_combinations_select_exactly_one_paid_route(self):
        for flags in itertools.product((False,True),repeat=4):
            dlc={name for name,value in zip(('No Step Back','By Blood Alone','Man the Guns','La Resistance'),flags) if value}
            research=audit.researched_by(2020,self.tech,self.facts['existing_prerequisites'])
            for family in FAMILIES:
                for year in YEARS:
                    choices=[model_id(family.id,year)]+([chassis_id(family.id,year)] if family.id in ('mbt','tracked_artillery') else [])
                    eligible=[i for i in choices if audit.condition(get(self.gear[i],'can_be_produced',[]),(2020,1,1),research,dlc)]
                    self.assertEqual(1,len(eligible),(flags,choices))
                    chosen=eligible[0];fact=self.facts['default_designs'].get(chosen,self.facts['equipment'][chosen])
                    self.assertGreater(fact['stats']['build_cost_ic'],0);self.assertTrue(fact['resources'])
                    if family.id in ('mbt','tracked_artillery'):
                        self.assertEqual(flags[0],chosen==chassis_id(family.id,year))

    def test_armor_recipes_have_valid_required_slots_components_and_equal_physical_costs(self):
        for family in ('mbt','tracked_artillery'):
            for year in YEARS:
                legacy=self.facts['equipment'][model_id(family,year)];designer=self.facts['default_designs'][chassis_id(family,year)]
                self.assertEqual(recipe(family,year),designer['modules']);self.assertEqual(5,len(designer['slots']))
                self.assertEqual(legacy['stats'],designer['stats']);self.assertEqual(legacy['resources'],designer['resources'])
                self.assertGreater(legacy['stats']['fuel_consumption'],0);self.assertGreater(legacy['stats']['manpower'],0)
                self.assertTrue(set(designer['modules'].values())<=self.modules.keys())
                for slot,data in designer['slots'].items():
                    self.assertIn(data['category'],data['allowed_categories']);self.assertIn(slot,designer['modules'])

    def test_new_company_roles_require_real_equipment_and_have_useful_tradeoffs(self):
        old=self.facts['units'];units={k:b for k,_,b in get(read(MOD/'common/units/ac_land_support.txt'),'sub_units')}
        for ident,count,gear,kind in [('ac_land_surveillance_company',10,'ac_land_sensor_equipment','recon'),
                                      ('ac_land_electronic_support_company',12,'ac_land_electronic_equipment','signal_company')]:
            body=units[ident];needs={k:int(v) for k,_,v in get(body,'need')}
            self.assertEqual({gear:count,'support_equipment':15,'motorized_equipment':8},needs)
            self.assertEqual(kind,get(body,'same_support_type'));self.assertEqual('support',get(body,'group'))
            self.assertGreater(int(get(body,'manpower')),0);self.assertGreater(float(get(body,'supply_consumption')),0)
            self.assertEqual('no',get(body,'active'));self.assertGreater(len(ids(get(body,'categories'))),2)
        self.assertGreater(float(get(units['ac_land_surveillance_company'],'recon')),float(old['mot_recon']['recon']))
        # Native signal's0.1 plus inherited three0.12 improvements; not a cosmetic downgrade.
        old_signal=float(old['signal_company']['initiative'])+sum(float(get(get(b,'signal_company',[]),'initiative',0)) for b in self.facts['existing_support_technologies'].values())
        self.assertGreaterEqual(float(get(units['ac_land_electronic_support_company'],'initiative')),old_signal)
        for tier,year in enumerate(YEARS):
            supply=get(self.tech[f'ac_land_logistics_{year}'],'logistics_company');self.assertLess(float(get(supply,'supply_consumption_factor')),0)
            self.assertGreater(float(get(get(self.tech[f'ac_land_support_{year}'],'maintenance_company'),'reliability_factor')),0)

    def test_optics_and_radio_have_separate_research_real_slots_and_extra_cost(self):
        for family in ('mbt','tracked_artillery'):
            for year in YEARS:
                ident=chassis_id(family,year);optional=self.facts['optional_designs'][ident];base=self.facts['default_designs'][ident]
                self.assertEqual(7,len(optional['slots']))
                for slot in ('special_type_slot_1','special_type_slot_2'):
                    row=optional['slots'][slot];self.assertIn(row['category'],row['allowed_categories'])
                self.assertGreater(optional['stats']['build_cost_ic'],base['stats']['build_cost_ic'])
                self.assertEqual(2,optional['resources']['aluminium']-base['resources'].get('aluminium',0))
                self.assertIn('ac_land_optics_'+str(year),ids(get(self.tech['ac_land_surveillance_'+str(year)],'enable_equipment_modules')))
                self.assertIn('ac_land_protected_radio_'+str(year),ids(get(self.tech['ac_land_electronic_support_'+str(year)],'enable_equipment_modules')))

    def test_ai_pays_for_buffers_before_recommending_supplied_support(self):
        strategies={k:b for k,_,b in read(MOD/'common/ai_strategy/ac_land_replacements.txt')}
        research=set(AI_TARGET_TECHS)
        for family in ('surveillance','electronic_support'):
            body=strategies[f'ac_land_{family}_manufactured_buffer'];enable=get(body,'enable')
            self.assertFalse(audit.condition(enable,(1991,1,1),research,set()))
            self.assertFalse(audit.condition(enable,(2006,1,1),research,set(),mil=12))
            self.assertTrue(audit.condition(enable,(2006,1,1),research,set(),mil=13))
            self.assertEqual('equipment_production_min_factories_archetype',get(get(body,'ai_strategy'),'type'))
            self.assertEqual('1',get(get(body,'ai_strategy'),'value'))
        role=get(strategies['ac_land_supplied_specialist_role'],'enable')
        for stocks in ({},{'ac_land_sensor_equipment':100,'ac_land_electronic_equipment':120}):
            self.assertFalse(audit.condition(role,(2006,1,1),research,set(),stocks))
        self.assertTrue(audit.condition(role,(2006,1,1),research,set(),AI_TARGET_STOCKS))
        targets=get(read(MOD/'common/ai_templates/ac_land_supplied_support.txt'),'ac_land_supplied_support')
        target=get(targets,'ac_land_supplied_target')
        self.assertEqual(role,get(target,'enable'));self.assertTrue(get(target,'can_upgrade_in_field'))
        self.assertIn('ac_land_surveillance_company',ids(get(get(target,'target_template'),'support')))

    def test_complete_ai_target_requires_each_actual_unlocked_unit_and_all_equipment(self):
        body=get(read(MOD/'common/ai_templates/ac_land_supplied_support.txt'),'ac_land_supplied_support')
        target=get(body,'ac_land_supplied_target');template=get(target,'target_template');needs={}
        for unit,_,amount in get(template,'regiments')+get(template,'support'):
            for gear,_,count in self.facts['units'][unit]['need']:
                needs[gear]=needs.get(gear,0)+int(amount)*int(count)
        self.assertEqual({'infantry_equipment':610,'support_equipment':80,'motorized_equipment':26,
                          'ac_land_sensor_equipment':10,'ac_land_electronic_equipment':12},needs)
        for gear,amount in needs.items():self.assertGreaterEqual(AI_TARGET_STOCKS[gear],amount)
        for kind in ('enable','can_upgrade_in_field'):
            guards=get(target,kind);research=set(AI_TARGET_TECHS)
            self.assertTrue(audit.condition(guards,(2006,1,1),research,set(),AI_TARGET_STOCKS))
            for missing in research:self.assertFalse(audit.condition(guards,(2006,1,1),research-{missing},set(),AI_TARGET_STOCKS),missing)
            for missing in needs:
                stocks={**AI_TARGET_STOCKS,missing:0}
                self.assertFalse(audit.condition(guards,(2006,1,1),research,set(),stocks),missing)
        for ident,unit in [('tech_engineers','engineer'),('tech_logistics_company','logistics_company')]:
            self.assertIn(unit,ids(get(self.facts['existing_support_technologies'][ident],'enable_subunits')))

    def test_each_equipment_tier_ranks_above_its_effective_inherited_parent(self):
        for ident,row in self.facts['equipment'].items():
            if not ident.startswith('ac_land_') or row.get('is_archetype')=='yes':continue
            self.assertGreater(int(row['priority']),int(row.get('parent_priority') or 0),ident)

    def test_ai_designer_groups_do_not_take_1991_priority_or_unresearched_modules(self):
        groups=read(MOD/'common/ai_equipment/ac_land_designs.txt')
        for ident,_,body in groups:
            family='mbt' if '_mbt_' in ident else 'tracked_artillery'
            modifiers=[v for k,_,v in get(body,'priority') if k=='modifier']
            self.assertTrue(any(audit.condition([n for n in m if n[0]!='factor'],(1991,1,1),set(),set()) for m in modifiers))
            for key,_,design in body:
                if not key.startswith('ac_land_'):continue
                when=int(key.rsplit('_',1)[1]);enable=get(design,'enable')
                self.assertFalse(audit.condition(enable,(when,1,1),set(),{'No Step Back'}))
                self.assertFalse(audit.condition(enable,(when,1,1),{f'ac_land_{family}_{when}'},set()))
                self.assertTrue(audit.condition(enable,(when,1,1),{f'ac_land_{family}_{when}'},{'No Step Back'}))
                self.assertEqual(set(recipe(family,when).values()),ids(get(design,'allowed_modules')))

    def test_existing_source_contract_and_61_start_coverage_stay_unchanged(self):
        baseline=json.loads((HERE/'preserved_sources.json').read_text())
        repairs=baseline.get('reviewed_source_repairs',{})
        self.assertEqual({'mod/2985041246/history/units/UST_band_of_broders_units.txt'},set(repairs))
        for name,expected in baseline['protected_sources_sha256'].items():
            if name not in repairs:
                self.assertEqual(expected,sha(ROOT/name),name)
                continue
            repair=repairs[name]
            self.assertEqual(expected,repair['old_normalized_sha256'])
            self.assertEqual(repair['new_normalized_sha256'],sha(ROOT/name),name)
            data=(ROOT/name).read_bytes().replace(b'\r\n',b'\n')
            self.assertTrue(data.endswith(b'\n}\n'))
            self.assertEqual(expected,hashlib.sha256(data[:-3]).hexdigest())
            with self.assertRaisesRegex(ValueError,'Unclosed block'):parse(data[:-3].decode('utf-8-sig'))
            self.assertTrue(parse(data.decode('utf-8-sig')))
            evidence=json.loads((ROOT/repair['evidence']).read_text())
            for field in ('old_normalized_sha256','new_normalized_sha256'):
                self.assertEqual(repair[field],evidence[field])
        self.assertEqual({'active_countries':61,'base_cases':244},baseline['starting_coverage'])
        current=json.loads((ROOT/'tools/world_starts/coverage.json').read_text())
        self.assertEqual(61,current['active_countries']);self.assertEqual(244,current['base_BBA_MTG_selected_cases'])
        self.assertEqual('no',get(get(get(read(MOD/'common/technology_tags/00_technology.txt'),'technology_folders'),'nsb_armour_folder'),'available')[0][2])

    def test_research_ui_changes_only_bounded_addition_and_description_scrollbars(self):
        old=read(build_ui.SOURCE);now=read(build_ui.TARGET)
        self.assertEqual(old,build_ui.normalized(now))
        boxes=[b for _,b in walk(now) if get(b,'name')=='"tech_info_description"']
        self.assertEqual(2,len(boxes));self.assertTrue(all(get(b,'scrollbarType')=='"ac_exp_standardtext_slider"' for b in boxes))
        folder=named(now,'ac_land_folder')
        self.assertEqual('{ left middle }','{ '+' '.join(k for k,_,_ in get(folder,'drag_scroll'))+' }')
        self.assertTrue(get(folder,'verticalScrollbar'));self.assertTrue(get(folder,'horizontalScrollbar'))
        self.assertEqual('40',get(folder,'scroll_wheel_factor'))
        for kind,body in walk(folder):self.assertNotIn(kind.lower(),('editboxtype','searchbox'))

    def test_actual_font_caption_bounds_nodes_and_three_display_configurations(self):
        _,report=render();self.assertEqual([],report['findings']);self.assertEqual(32,len(report['node_rectangles']))
        boxes=report['node_rectangles']
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                self.assertFalse(a['x']<b['x']+b['width'] and a['x']+a['width']>b['x'] and a['y']<b['y']+b['height'] and a['y']+a['height']>b['y'],(a,b))
        for case in report['display_cases']:self.assertTrue(case['last_node_reachable']);self.assertTrue(case['tab_inside'])
        card=named(read(MOD/'interface/ac_land_techtree.gui'),'techtree_ac_land_folder_item')
        self.assertTrue({'Name','Icon','Background','bonus_icon','bonus','can_assign_design_team_icon','special_project_specialization_list'}<={get(b,'name','').strip('"') for _,b in walk(card) if isinstance(get(b,'name',''),str)})
        font=Atlas('ACBriefing16');strings=locs()
        for ident in self.tech:self.assertLessEqual(len(font.wrap(strings[ident],175))*font.height,36)
        self.assertGreater(max(len(strings[i+'_desc']) for i in self.tech),180)

    def test_complete_english_names_descriptions_actual_bindings_and_no_duplicate_keys(self):
        path=MOD/'localisation/english/ac_land_program_l_english.yml';raw=path.read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        keys=re.findall(r'^\s*(\w+):',raw.decode('utf-8-sig'),re.M);self.assertEqual(len(keys),len(set(keys)))
        strings=locs()
        for ident in [*self.tech,*self.modules,*[i for i,b in self.gear.items() if get(b,'is_archetype')!='yes']]:
            self.assertTrue(strings.get(ident));self.assertTrue(strings.get(ident+'_desc'))
        for ident in self.tech:self.assertNotIn('TODO',strings[ident+'_desc'])
        sprites={r['name'] for r in self.art['sprites']}
        for ident in self.tech:self.assertIn('GFX_'+ident+'_medium',sprites)
        for ident in self.modules:self.assertIn('GFX_EMI_'+ident,sprites)
        for ident in self.gear:self.assertIn('GFX_'+ident,sprites)

    def test_all_dds_sources_alpha_frames_palette_and_compositions(self):
        self.assertEqual(106,len(self.art['assets']));self.assertEqual(158,len(self.art['sprites']))
        self.assertEqual(len(self.art['sprites']),len({r['name'] for r in self.art['sprites']}))
        groups={}
        for row in self.art['assets']:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as im:
                self.assertEqual((row['width'],row['height']),im.size);self.assertEqual(0,im.width%row['frames'])
                rgba=im.convert('RGBA');self.assertEqual((row['alpha_min'],row['alpha_max']),rgba.getchannel('A').getextrema())
                self.assertFalse(any(r>150 and g>120 and b<90 and a>0 for r,g,b,a in rgba.getdata()),row['file'])
                if row['frames']>1:
                    frames=[rgba.crop((i*row['frame_width'],0,(i+1)*row['frame_width'],im.height)).tobytes() for i in range(row['frames'])]
                    self.assertEqual(row['frames'],len(set(frames)))
                if row['role'].endswith('composition'):groups.setdefault(row['role'],[]).append(rgba.tobytes())
            if 'source' in row:self.assertEqual(row['source_sha256'],sha(ROOT/row['source']))
        for role,images in groups.items():self.assertEqual(len(images),len(set(images)),role)
        self.assertEqual(68,len(list((HERE/'source/art').glob('*.svg'))))

    def test_actual_owner_equipment_allowance_covers_every_new_archetype(self):
        covered=set()
        for family in DATA['armor_families']:covered.update([family['parent'],*family['children']])
        for group in DATA['land'].values():covered.update(group['archetypes'])
        for ident,fact in self.facts['equipment'].items():
            if ident.startswith('ac_land_') and fact.get('archetype'):self.assertIn(fact['archetype'],covered,ident)
        for ident in ('ac_land_sensor_equipment','ac_land_electronic_equipment'):
            self.assertIn('num_equipment_in_armies_k@'+ident,observable_names())
            world=World();world.action('on_startup');c=world.countries['SNS']
            c.observables['num_equipment_in_armies_k@'+ident]=1;world.run('ac_macro_quote','SNS')
            self.assertEqual(D('.003'),c.variables['ac_macro_upkeep']*12)
            self.assertFalse(c.equipment);self.assertEqual(0,c.variables['ac_macro_settlements'])

    def test_actual_armor_owner_handles_parent_child_observation_overlap_once(self):
        world=World();world.action('on_startup');c=world.countries['SNS']
        c.observables.update({'num_equipment_in_armies_k@modern_tank_chassis':1,
                              'num_equipment_in_armies_k@medium_tank_chassis':1,
                              'num_equipment_in_armies_k@medium_tank_artillery_chassis':1})
        world.run('ac_macro_quote','SNS');self.assertEqual(D('.4'),c.variables['ac_macro_upkeep']*12)
        c.observables['num_equipment_in_armies_k@ac_land_mbt_equipment_2006']=999
        world.run('ac_macro_quote','SNS');self.assertEqual(D('.4'),c.variables['ac_macro_upkeep']*12)

    def test_actual_specialist_company_cost_is_positive_and_fiscal_disabled_is_inert(self):
        world=World();world.action('on_startup');c=world.countries['SNS']
        c.observables.update({'num_equipment_in_armies_k@ac_land_sensor_equipment':D('.01'),
                              'num_equipment_in_armies_k@ac_land_electronic_equipment':D('.012'),
                              'num_equipment_in_armies_k@support_equipment':D('.03'),
                              'num_equipment_in_armies_k@motorized_equipment':D('.016'),
                              'deployed_army_manpower_k':D('.55')})
        world.run('ac_macro_quote','SNS');self.assertEqual(D('.033796'),c.variables['ac_macro_upkeep']*12)
        disabled=World(mode='disabled');disabled.action('on_startup');d=disabled.countries['SNS'];before=copy.deepcopy(d.variables)
        disabled.run('ac_macro_quote','SNS');self.assertEqual(before,d.variables)

    def test_primary_capture_and_offline_capability_receipt(self):
        report=audit.report(ENGINE);self.assertEqual([],report['errors']);self.assertFalse(report['native_acceptance'])
        self.assertEqual(report,json.loads((HERE/'capabilities.json').read_text()))

    def test_generators_and_visual_artifacts_are_byte_reproducible(self):
        for script in ('build.py','build_ui.py','build_art.py','render_review.py'):
            result=subprocess.run([sys.executable,'-B',str(HERE/script),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path);args,rest=parser.parse_known_args();ENGINE=args.engine
    unittest.main(argv=[sys.argv[0],*rest],verbosity=2)
