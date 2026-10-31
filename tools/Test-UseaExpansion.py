"""Expansion regressions. Offline execution is deliberately distinct from native evidence."""
import copy,importlib.util,json,re,subprocess,sys,unittest
from collections import Counter
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246';ART=ROOT/'tools/usea_expansion'
sys.path.insert(0,str(ART))
from script import parse,get,walk
from content import FOCUSES
spec=importlib.util.spec_from_file_location('ucw',ROOT/'tools/Test-ContinentalWar.py');ucw=importlib.util.module_from_spec(spec);sys.modules['ucw']=ucw;spec.loader.exec_module(ucw)
def load(path):return parse((MOD/path).read_text(encoding='utf-8-sig'))
class World(ucw.World):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for tag in ('REC','YUK','OSE'):self.countries[tag]=ucw.Country(tag)
        self.effects.update(ucw.mapping(ucw.load('common/scripted_effects/ac_expansion.txt')))
        self.effects['ac_pwi_bound_pressures']=ucw.mapping(ucw.load('common/scripted_effects/ac_pwi.txt'))['ac_pwi_bound_pressures']
        self.triggers.update(ucw.mapping(ucw.load('common/scripted_triggers/ac_expansion.txt')))
        self.triggers['ac_pwi_active']=ucw.mapping(ucw.load('common/scripted_triggers/ac_pwi.txt'))['ac_pwi_active']
        self.events.update({ucw.mapping(v)['id']:(k,v) for k,_,v in ucw.load('events/ac_expansion.txt') if k=='country_event'})
        for path in (MOD/'common/national_focus').glob('*.txt'):
            if path.name.startswith(('ERU','FCU','NPT','REC','YUK')):
                for k,n in walk(ucw.load('common/national_focus/'+path.name)):
                    if k in ('focus','shared_focus') and get(n,'id'):self.focuses[get(n,'id')]=n

class Expansion(unittest.TestCase):
    def test_exact_counts_and_unique_positions(self):
        world=World();counts=Counter(i[:3] for i in world.focuses)
        self.assertEqual(dict(ERU=54,FCU=54,NPT=30,REC=24,YUK=30),dict(counts))
        seen={}
        for ident,n in world.focuses.items():
            phase='opening' if ident[:3] in ('ERU','FCU') and '_exp_' in ident and '_ucw_' not in ident else 'later'
            key=(ident[:3],phase,int(get(n,'x')),int(get(n,'y')))
            self.assertNotIn(key,seen,(ident,seen.get(key)));seen[key]=ident
            for k,_,v in n:
                if k=='prerequisite':
                    for _,_,other in v:
                        self.assertIn(other,world.focuses)
                        self.assertLess(int(get(world.focuses[other],'y')),int(get(n,'y')),(ident,other))
    def test_opening_choices_applied_after_initialization_once(self):
        for fiscal in (False,True):
            for tag in ('ERU','FCU'):
                w=World('1991.1.1',fiscal=fiscal);c=w.countries[tag]
                for kind in ('civil','logistics','relief','readiness'):c.flags[tag+'_exp_prepared_'+kind]=None
                w.run('ac_exp_apply_opening',tag);self.assertFalse(c.variables)
                w.today=ucw.day('1999.12.1');w.run('ac_ucw_world_start',tag);w.run('ac_ucw_country_start',tag)
                self.assertEqual(54,c.variables['ac_ucw_recovery']);self.assertEqual(35,c.variables['ac_ucw_pressure'])
                self.assertEqual('ac_ucw_'+tag.lower()+'_tree',c.tree)
                snapshot=copy.deepcopy(c)
                reloaded=copy.deepcopy(w);reloaded.run('ac_ucw_country_start',tag);reloaded.run('ac_exp_apply_opening',tag)
                self.assertEqual(snapshot,reloaded.countries[tag])
    def test_old_save_never_receives_preparation_rewards(self):
        w=World('2004.1.1');c=w.countries['ERU'];w.run('ac_ucw_world_start','ERU');w.run('ac_ucw_country_start','ERU')
        self.assertEqual(45,c.variables['ac_ucw_recovery']);self.assertEqual(40,c.variables['ac_ucw_pressure'])
        c.flags['ERU_exp_prepared_logistics']=None;w.run('ac_exp_apply_opening','ERU')
        self.assertEqual(45,c.variables['ac_ucw_recovery'])
    def test_every_new_reward_is_once_and_revalidates_capitulation(self):
        for row in FOCUSES:
            w=World('1991.1.1' if row.phase=='opening' else '2005.1.1');c=w.countries[row.tag]
            if row.phase=='later':
                c.flags['ac_ucw_started']=None;c.variables.update(ac_ucw_recovery=45,ac_ucw_pressure=40,ac_ucw_grievance=45)
                w.globals.update(ucw.OUTCOMES);w.globals.add('ac_ucw_war_averted')
            reward=get(w.focuses[row.id],'completion_reward')
            for idea in re.findall(r'has_idea\s*=\s*(\w+)',row.available):c.ideas[idea]=None
            c.capitulated=True;before=copy.deepcopy(c);w.execute(reward,c);self.assertEqual(before,c,row.id)
            c.capitulated=False;w.execute(reward,c);after=copy.deepcopy(c);w.execute(reward,c);self.assertEqual(after,c,row.id)
            self.assertIn(row.id+'_done',c.flags,row.id)
    def test_diplomatic_publication_checks_both_participants(self):
        for mode in ('valid','war','annexed','partner_subject','own_subject','partner_capitulated','own_capitulated','no_partnership'):
            w=World('2001.1.1');c=w.countries['YUK'];p=w.countries['OSE'];c.flags['ac_yuk_arkbird_partner']=None
            if mode=='war':w.wars.add(frozenset(('YUK','OSE')))
            if mode=='annexed':p.exists=False
            if mode=='partner_subject':p.subject=True
            if mode=='own_subject':c.subject=True
            if mode=='partner_capitulated':p.capitulated=True
            if mode=='own_capitulated':c.capitulated=True
            if mode=='no_partnership':c.flags.clear()
            reward=get(w.focuses['YUK_exp_data_protocols'],'completion_reward');w.execute(reward,c);w.execute(reward,c)
            self.assertEqual(1 if mode=='valid' else 0,len(c.opinions),mode)
            self.assertEqual(len(c.opinions),len(p.opinions),mode)
    def test_events_dispatch_once_expire_and_policies_are_exclusive(self):
        for tag in ('ERU','FCU','NPT','REC','YUK'):
            w=World('1996.1.1');c=w.countries[tag]
            for ready in ('opening_ready','choice_2_ready','choice_3_ready','assessment_ready'):c.flags[tag+'_exp_'+ready]=None
            w.run('ac_exp_weekly',tag);self.assertEqual(4,len(w.queue));w.run('ac_exp_weekly',tag);self.assertEqual(4,len(w.queue))
            event='ac_expansion.'+str(('ERU','FCU','NPT','REC','YUK').index(tag)*10+2)
            w.choose(event,0,tag);snapshot=copy.deepcopy(c);w.choose(event,1,tag);self.assertEqual(snapshot,c)
            self.assertIn(tag+'_exp_civil',c.ideas);self.assertNotIn(tag+'_exp_directive',c.ideas)
            w=World('2005.12.31');c=w.countries[tag]
            for ready in ('opening_ready','choice_2_ready','choice_3_ready'):c.flags[tag+'_exp_'+ready]=None
            w.run('ac_exp_weekly',tag);self.assertFalse(w.queue)
    def test_late_assessments_require_completion_and_remain_once_only(self):
        for offset,tag in enumerate(('ERU','FCU','NPT','REC','YUK')):
            with self.subTest(tag=tag):
                w=World('2006.1.1');c=w.countries[tag]
                # Updating a late save must not replay expired preparation choices.
                for ready in ('opening_ready','choice_2_ready','choice_3_ready'):
                    c.flags[tag+'_exp_'+ready]=None
                w.run('ac_exp_weekly',tag);self.assertFalse(w.queue)
                for index in (1,2,3):
                    event=w.events['ac_expansion.'+str(offset*10+index)][1]
                    self.assertFalse(w.trigger(get(event,'trigger'),c))
                ident='ac_expansion.'+str(offset*10+4)
                event=w.events[ident][1]
                c.flags[tag+'_exp_assessment_ready']=None
                c.capitulated=True
                w.run('ac_exp_weekly',tag);self.assertFalse(w.queue)
                self.assertFalse(w.trigger(get(event,'trigger'),c))
                c.capitulated=False
                w.run('ac_exp_weekly',tag);w.run('ac_exp_weekly',tag)
                self.assertEqual([(w.today+1,tag,ident)],w.queue)
                w.today+=1
                self.assertTrue(w.trigger(get(event,'trigger'),c))
                w.drain();self.assertIn(tag+'_exp_event_4_answered',c.flags)
                answered=copy.deepcopy(c)
                w.choose(ident,1,tag);w.run('ac_exp_weekly',tag)
                self.assertEqual(answered,c);self.assertFalse(w.queue)
                self.assertFalse(w.trigger(get(event,'trigger'),c))
    def test_september_isaf_settlement_finishes_after_year_end_and_unlocks_services(self):
        for fiscal in (False,True):
            with self.subTest(fiscal=fiscal):
                w=World('2005.9.26',fiscal=fiscal)
                w.run('ac_ucw_world_start','ERU');w.run('ac_ucw_country_start','ERU')
                w.globals.add('ac_ucw_outcome_isaf_victory')
                w.queue.clear()  # Isolate the national assessment from calendar briefs.
                for suffix in ('provisional_government','rebuild_under_oversight',
                               'exp_reconstruction_oversight','exp_settlement_assessment'):
                    ident='ERU_ucw_'+suffix
                    self.assertTrue(w.focus_available(ident,'ERU'))
                    w.today+=int(get(w.focuses[ident],'cost'))*7
                    w.complete(ident,'ERU')
                self.assertEqual(ucw.day('2006.1.16'),w.today)
                w=copy.deepcopy(w)  # Reload after completing the capstone.
                w.today+=7  # Allow a full weekly dispatch interval.
                w.run('ac_exp_weekly','ERU')
                self.assertEqual([(w.today+1,'ERU','ac_expansion.4')],w.queue)
                w=copy.deepcopy(w)  # Reload while the event is queued.
                w.run('ac_exp_weekly','ERU');self.assertEqual(1,len(w.queue))
                w.today+=1;c=w.countries['ERU']
                self.assertTrue(w.trigger(get(w.events['ac_expansion.4'][1],'trigger'),c))
                w.drain();self.assertIn('ERU_exp_service',c.ideas)
                category=get(load('common/decisions/categories/ac_expansion.txt'),'ERU_exp_programmes')
                decision=get(get(load('common/decisions/ac_expansion.txt'),'ERU_exp_programmes'),'ERU_exp_maintain_services')
                self.assertTrue(w.trigger(get(category,'visible'),c))
                self.assertTrue(w.trigger(get(decision,'available'),c))
                before=c.variables['ac_ucw_recovery']
                w.execute(get(decision,'complete_effect'),c)
                self.assertEqual(before+2,c.variables['ac_ucw_recovery'])
    def test_saved_policy_and_completed_focus_survive_handoff(self):
        w=World('1991.1.1');c=w.countries['ERU'];w.complete('ERU_exp_opening','ERU');c.ideas['ERU_exp_civil']=None
        w=copy.deepcopy(w);w.today=ucw.day('1999.12.1');w.run('ac_ucw_world_start','ERU');w.run('ac_ucw_country_start','ERU')
        self.assertIn('ERU_exp_opening',w.countries['ERU'].focuses);self.assertIn('ERU_exp_civil',w.countries['ERU'].ideas)
        self.assertFalse(w.focus_available('ERU_exp_registry','ERU'))

    def test_fcu_four_policy_combinations_open_useful_branches_and_survive_transition(self):
        for fund in (0,1):
            for reserve in (0,1):
                w=World('1991.1.1');c=w.countries['FCU']
                for suffix in ('opening','treaty_register','burden_formula','civil_protection','medical_register'):
                    w.complete('FCU_exp_'+suffix,'FCU')
                w.choose('ac_expansion.12',fund,'FCU');w.choose('ac_expansion.13',reserve,'FCU')
                chosen='treaty_audit' if fund else 'liaison_offices'
                rejected='liaison_offices' if fund else 'treaty_audit'
                w.complete('FCU_exp_'+chosen,'FCU')
                self.assertFalse(w.focus_available('FCU_exp_'+rejected,'FCU'))
                chosen='public_information' if reserve else 'shelter_exercises'
                rejected='shelter_exercises' if reserve else 'public_information'
                w.complete('FCU_exp_'+chosen,'FCU')
                self.assertFalse(w.focus_available('FCU_exp_'+rejected,'FCU'))
                w.complete('FCU_exp_opening_assessment','FCU')
                ideas=copy.deepcopy(c.ideas)
                w.today=ucw.day('1999.12.1');w.run('ac_ucw_world_start','FCU');w.run('ac_ucw_country_start','FCU')
                self.assertEqual(ideas,c.ideas)
                c.variables.update(ac_ucw_pressure=40,ac_ucw_recovery=45)
                w.execute(get(w.focuses['FCU_ucw_exp_transport_board'],'completion_reward'),c)
                self.assertEqual(50 if reserve else 48,c.variables['ac_ucw_recovery'])
                self.assertEqual(40 if reserve else 36,c.variables['ac_ucw_pressure'])
                before=copy.deepcopy(c)
                w.choose('ac_expansion.12',1-fund,'FCU');w.choose('ac_expansion.13',1-reserve,'FCU')
                self.assertEqual(before,c,'Old council choices must not replay after the handoff')

    def test_fcu_mediation_revalidates_partners_and_prevents_duplicate_answers(self):
        for failure in ('none','war','own_subject','partner_subject','own_capitulated','partner_capitulated','annexation','expired'):
            w=World('2001.1.1')
            for tag in ('ERU','FCU'):
                w.run('ac_ucw_world_start',tag);w.run('ac_ucw_country_start',tag)
            w.run('ac_ucw_offer_mediation','FCU');pending=len(w.queue)
            w.run('ac_ucw_offer_mediation','FCU');self.assertEqual(pending,len(w.queue))
            if failure=='war':w.wars.add(frozenset(('FCU','ERU')))
            if failure=='own_subject':w.countries['FCU'].subject=True
            if failure=='partner_subject':w.countries['ERU'].subject=True
            if failure=='own_capitulated':w.countries['FCU'].capitulated=True
            if failure=='partner_capitulated':w.countries['ERU'].capitulated=True
            if failure=='annexation':w.countries['FCU'].exists=False
            if failure=='expired':w.today+=31
            w.choose('ac_ucw.13',0,'ERU');w.choose('ac_ucw.13',0,'ERU')
            self.assertEqual(1 if failure=='none' else 0,len(w.countries['FCU'].opinions),failure)
            self.assertEqual(len(w.countries['FCU'].opinions),len(w.countries['ERU'].opinions))
            if failure!='none':
                self.assertTrue(w.trigger(get(w.options('ac_ucw.13')[2],'trigger'),w.countries['ERU']))
                w.choose('ac_ucw.13',2,'ERU');self.assertNotIn('ac_ucw_mediation_pending',w.countries['ERU'].flags)
    def test_tooltip_substitutions(self):
        text=(MOD/'localisation/english/bookmarks_l_english.yml').read_text(encoding='utf-8-sig')
        self.assertRegex(text,r'COUNTRY_SELECTION_CHARACTER_DESC_NAME:\d* "\$NAME\|Y\$"')
        self.assertIn('$TRAITS_DESC|$',text)
    def test_details_are_bounded_scrollable_and_controls_preserved(self):
        original=json.loads((ART/'focus_contract.json').read_text());current=load('interface/nationalfocusview.gui')
        for name in ('national_focus_detail_view','coninuous_focus_detail_view'):
            old=next(n for _,n in walk(original) if get(n,'name')=='"'+name+'"')
            new=next(n for _,n in walk(current) if get(n,'name')=='"'+name+'"')
            self.assertEqual(Counter(get(n,'name') for _,n in walk(old) if get(n,'name')),Counter(get(n,'name') for _,n in walk(new) if get(n,'name')))
            controls={get(n,'name','').strip('"'):n for _,n in walk(new)}
            desc,reward=controls['desc'],controls['reward']
            self.assertIn('ac_exp_standardtext_slider',get(desc,'scrollbarType'));self.assertIn('ac_exp_standardtext_slider',get(reward,'scrollbarType'))
            self.assertLess(int(get(get(desc,'position'),'y'))+int(get(desc,'maxHeight')),int(get(get(controls['reward_label'],'position'),'y')))
            self.assertLessEqual(int(get(get(reward,'position'),'y'))+int(get(reward,'maxHeight')),int(get(get(new,'size'),'height')))
            self.assertEqual(Counter((k,str(v)) for _,n in walk(old) for k,_,v in n if k.lower() in ('shortcut','moveable','zoom')),Counter((k,str(v)) for _,n in walk(new) for k,_,v in n if k.lower() in ('shortcut','moveable','zoom')))
    def test_assets_frames_alpha_and_unique_compositions(self):
        records=json.loads((ART/'assets.json').read_text())+json.loads((ART/'media_assets.json').read_text())+json.loads((ART/'leader_assets.json').read_text())
        for row in records:
            with Image.open(MOD/row['file']) as im:
                self.assertEqual((row['width'],row['height']),im.size,row['file'])
                self.assertEqual(0,im.width%row['frames'],row['file'])
                if '/focus/' in row['file']:
                    alpha=im.getchannel('A');self.assertEqual(0,alpha.getpixel((0,0)));self.assertGreater(alpha.getextrema()[1],200)
        focus=[r for r in records if '/focus/' in r['file']];self.assertEqual(192,len(focus));self.assertEqual(192,len({r['sha256'] for r in focus}))
        compositions=json.loads((ART/'focus_art.json').read_text())
        self.assertEqual(192,len({(r['tag'],tuple(r['motifs']),r['composition']) for r in compositions}))
    def test_gui_dependencies_are_owned_and_sprite_definitions_unique(self):
        from port_1_19.pdx import top_items
        definitions={}
        for path in (MOD/'interface').rglob('*.gfx'):
            for kind,name,raw in top_items(path.read_text(encoding='utf-8-sig',errors='replace'),'spriteTypes'):
                if not name:continue
                definitions.setdefault(name,[]).append((path,raw))
        for name,defs in definitions.items():
            if name.startswith(('GFX_ac_exp_','GFX_ac_ui_','GFX_ac8_')):self.assertEqual(1,len(defs),name)
        gui=load('interface/nationalfocusview.gui');bars={get(n,'name','').strip('"') for k,n in walk(gui) if k.lower() in ('scrollbartype','extendedscrollbartype')}
        for _,n in walk(gui):
            for k,_,v in n:
                if k.lower() in ('spritetype','quadtexturesprite') and isinstance(v,str):
                    name=v.strip('"')
                    if name=='GFX_flag_small2':continue
                    self.assertTrue(name in definitions,'Unresolved GUI sprite: '+name)
                    self.assertIn('gfx/interface/ac_expansion/',definitions[name][0][1],name)
                if k.lower() in ('scrollbartype','verticalscrollbar','horizontalscrollbar') and isinstance(v,str):self.assertIn(v.strip('"'),bars)
    def test_reproducible_sources(self):
        for file in ('build_content.py','build_ui.py'):
            subprocess.run([sys.executable,'-B',str(ART/file),'--check'],check=True,capture_output=True)

    def test_native_presentation_regressions(self):
        # These faults escaped a texture-exists audit and were seen in 1.19.4.
        gui=load('interface/nationalfocusview.gui')
        item=next(n for _,n in walk(gui) if get(n,'name')=='"national_focus_item"')
        title=next(n for _,n in walk(item) if get(n,'name')=='"name"')
        background=next(n for _,n in walk(item) if get(n,'name')=='"bg"')
        with Image.open(MOD/'gfx/interface/ac_expansion/ui/GFX_focus_can_start.dds') as frame:
            self.assertLessEqual(int(get(get(title,'position'),'y'))+int(get(title,'maxHeight')),
                                 int(get(get(background,'position'),'y'))+frame.height)
        self.assertEqual(54,int(get(title,'maxHeight')), 'Three 18px text lines must fit')
        self.assertEqual('"ACBriefing16"',get(title,'font'))
        self.assertTrue((MOD/'interface/nationalfocusview.gfx').exists(), 'Engine filename override is required for runtime state sprites')
        with Image.open(MOD/'gfx/interface/ac_expansion/ui/GFX_focus_link_left_right.dds') as im:
            # Horizontal tiles must have transparent top/bottom edges in every frame.
            for x in range(im.width):
                self.assertEqual(0,im.getpixel((x,0))[3])
                self.assertEqual(0,im.getpixel((x,im.height-1))[3])
        media=json.loads((ART/'media_assets.json').read_text())
        gfx=(MOD/'interface/ac_expansion_media.gfx').read_text()
        for row in media:
            if '/event_pictures/' in row['file']:
                self.assertLessEqual(row['width'],200,'Country event art must fit beside option buttons')
                self.assertLessEqual(row['height'],160)
        for name in ('cockpit','formation','pilot','joker_flight'):
            sprite='GFX_ac8_'+name+'_small'
            self.assertIn('name = "'+sprite+'"',gfx)
            self.assertEqual(1,len([r for r in media if r['sprite']==sprite]))
        for filename in ('GFX_ac_ui_dialog_bg.dds','GFX_ac_ui_tiled_window_2b_border.dds'):
            path=MOD/'gfx/interface/ac_expansion/ui'/filename
            if path.exists():
                with Image.open(path) as im:self.assertEqual(255,im.getpixel((im.width//2,im.height//2))[3],filename)

if __name__=='__main__':unittest.main()
