"""Regressions for the defects actually shown in the October 30 screenshots."""
import copy,json,re,subprocess,sys,unittest
from collections import Counter
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246';SRC=ROOT/'tools/usea_expansion'
sys.path.insert(0,str(SRC))
from script import parse,get,walk
from economy_script import Harness,Country

def read(file):return parse((MOD/file).read_text(encoding='utf-8-sig'))
def named(tree,name):return next(n for _,n in walk(tree) if get(n,'name','').strip('"')==name)

class Repairs(unittest.TestCase):
    def test_dashboard_pages_are_exclusive_in_enabled_and_disabled_economies(self):
        sg=get(read('common/scripted_guis/ac_economy.txt'),'scripted_gui')
        main=get(sg,'project_ulysses_economy_screen');triggers=dict((k,v) for k,_,v in get(main,'triggers'))
        window=named(read('interface/ac_economy_gui.gui'),'project_ulysses_economy_screen')
        self.assertFalse(any(k=='containerWindowType' for k,_,v in window),'Page-container visibility failed in native 1.19.4; use direct controls')
        controls={get(n,'name','').strip('"'):n for k,_,n in window if k in ('instantTextboxType','buttonType')}
        for enabled in (False,True):
            h=Harness(enabled=enabled);c=Country(factories=20);h.action('on_startup',[c])
            for tab in range(3):
                c.variables['ac_econ_ui_tab']=tab
                for prefix,expected in (('ov_',0),('budget_',1),('contracts_',2)):
                    for name in controls:
                        if name.startswith(prefix):self.assertEqual(enabled and tab==expected,h.trigger(triggers[name+'_visible'],c,{}),(name,enabled,tab))
                self.assertEqual(not enabled,h.trigger(triggers['disabled_message_visible'],c,{}))
                for name in ('refresh_button','borrow_button','repay_button','order_button','cancel_order_button','tax_low_button','tax_standard_button','tax_high_button','services_basic_button','services_rebuild_button'):
                    self.assertIn(name+'_visible',triggers)
                    if not enabled:self.assertFalse(h.trigger(triggers[name+'_click_enabled'],c,{}),name)

    def test_dashboard_geometry_opaque_background_and_button_frames(self):
        from build_dashboard import POSITIONS
        # All local bounds fit inside 860x640: 1075x800 at UI scale 1.25.
        for name,p in POSITIONS.items():
            w,h=p[2:] if len(p)>2 else (40,40) if name=='close_button' else (160,40)
            self.assertLessEqual(p[0]+w,860,name);self.assertLessEqual(p[1]+h,640,name)
        for page in ('ov_','budget_','contracts_'):
            texts=[(k,p) for k,p in POSITIONS.items() if len(p)>2 and (k.startswith(page) or k in ('dashboard_title','dashboard_subtitle','footer'))]
            for i,(an,a) in enumerate(texts):
                for bn,b in texts[i+1:]:self.assertFalse(a[0]<b[0]+b[2] and b[0]<a[0]+a[2] and a[1]<b[1]+b[3] and b[1]<a[1]+a[3],(an,bn))
        with Image.open(MOD/'gfx/interface/ac_expansion/ui/GFX_ac_ui_economy_background.dds') as im:
            self.assertEqual((860,640),im.size);self.assertEqual((255,255),im.getchannel('A').getextrema())
        with Image.open(MOD/'gfx/interface/ac_expansion/ui/GFX_ac_ui_economy_button.dds') as im:self.assertEqual((640,40),im.size)

    def test_country_and_news_event_controls_and_scrollbars(self):
        old=json.loads((SRC/'event_contract.json').read_text());new=read('interface/eventwindow.gui')
        for name in ('EventWindow','EventWindow_News','event_option_entry'):
            a=named(old,name);b=named(new,name)
            self.assertEqual(Counter(get(n,'name') for _,n in walk(a)),Counter(get(n,'name') for _,n in walk(b)))
            if name=='event_option_entry':continue
            desc=named([[name,'=',b]],'Description')
            self.assertEqual('"ac_exp_standardtext_slider"',get(desc,'scrollbarType'))
            self.assertLessEqual(int(get(desc,'maxHeight')),230)
            self.assertEqual(get(a,'moveable'),get(b,'moveable'))

    def test_all_authored_scripted_gui_windows_and_click_targets_exist(self):
        windows={}
        for path in (MOD/'interface').rglob('*.gui'):
            for kind,node in walk(parse(path.read_text(encoding='utf-8-sig',errors='replace'))):
                if kind.lower()=='containerwindowtype' and get(node,'name'):windows[get(node,'name').strip('"')]=node
        for path in (MOD/'common/scripted_guis').glob('*.txt'):
            for ident,_,node in get(parse(path.read_text(encoding='utf-8-sig')),'scripted_gui',[]):
                name=get(node,'window_name').strip('"');self.assertIn(name,windows,ident)
                controls={get(n,'name','').strip('"') for _,n in walk(windows[name])}
                for effect,_,_ in get(node,'effects',[]):
                    button=re.sub(r'_(?:(?:alt|control|shift|right)_)*click$','',effect)
                    self.assertIn(button,controls,(ident,button))
                for _,_,dynamic in get(node,'dynamic_lists',[]):
                    entry=get(dynamic,'entry_container')
                    if entry:self.assertIn(entry.strip('"'),windows,ident)

    def test_vanilla_isolation_keeps_authored_decisions_and_mio_parents(self):
        policy=json.loads((SRC/'vanilla_cleanup.json').read_text())
        for p in (ROOT/'mod/2985041246.mod',MOD/'descriptor.mod',MOD/'ProjectUlysses.mod'):
            for folder in policy['replace_paths']:self.assertIn('replace_path="'+folder+'"',p.read_text())
        for row in policy['retired']:self.assertEqual([],read(row['file']))
        cats={k for p in (MOD/'common/decisions/categories').glob('*.txt') for k,_,_ in parse(p.read_text(encoding='utf-8-sig'))}
        decisions=set()
        for p in (MOD/'common/decisions').glob('*.txt'):
            for cat,_,node in parse(p.read_text(encoding='utf-8-sig')):
                self.assertIn(cat,cats,p.name)
                decisions.update(k for k,_,v in node if isinstance(v,list))
        for folder in ('common/national_focus','common/scripted_effects','common/scripted_guis','events'):
            for p in (MOD/folder).glob('*.txt'):
                text=re.sub(r'#.*','',p.read_text(encoding='utf-8-sig'))
                for target in re.findall(r'\bactivate_mission\s*=\s*(\w+)',text):self.assertIn(target,decisions,(p.name,target))
        orgs={k:v for p in (MOD/'common/military_industrial_organization/organizations').glob('*.txt') for k,_,v in parse(p.read_text(encoding='utf-8-sig'))}
        for name,node in orgs.items():
            for key,_,parent in node:
                if key=='include':self.assertIn(parent,orgs,name)
        cnea=get(read('common/decisions/categories/00_ac_decisions_categories.txt'),'CNEA_parliament_decisions_category')
        self.assertEqual('no',get(get(cnea,'visible'),'always'))

    def test_starting_leader_coverage_and_existing_identities(self):
        from build_leaders import capture
        # capture deliberately ignores the generated character file, so validate
        # shipped roles and recruitment independently.
        roles={}
        groups=get(read('common/ideologies/00_ideologies.txt'),'ideologies')
        owners={s:g for g,_,b in groups for s,_,_ in get(b,'types',[])}
        for path in (MOD/'common/characters').glob('*.txt'):
            for ident,_,n in get(parse(path.read_text(encoding='utf-8-sig')),'characters',[]):
                roles[ident]={owners.get(get(v,'ideology','').strip('"')) for k,_,v in n if k=='country_leader'}
        for row in json.loads((SRC/'leaders.json').read_text()):
            history=read(row['history']);party=get(get(history,'set_politics',[]),'ruling_party','neutrality')
            self.assertTrue(any(party in roles.get(v,set()) for k,_,v in history if k=='recruit_character') or row['legacy'],row['tag'])
            for ident in row['existing_active']:self.assertIn(['recruit_character','=',ident],history)
        self.assertIn(['recruit_character','=','FCU_robert_sinclair'],read('history/countries/FCU - Central Usea.txt'))
        self.assertIn('provisional mod chronology',(MOD/'localisation/english/ac_starting_governments_l_english.yml').read_text(encoding='utf-8-sig'))

    def test_generated_sources(self):
        for name in ('build_dashboard.py','build_events_ui.py','build_leaders.py','build_retired_mechanics.py'):
            subprocess.run([sys.executable,'-B',str(SRC/name),'--check'],check=True,capture_output=True)

    def test_retired_events_cannot_restart_crises_or_change_government(self):
        from build_retired_mechanics import IDEAS,MISSIONS
        contracts=json.loads((SRC/'retired_event_contract.json').read_text())
        for row in contracts:
            events=[n for k,_,n in read('events/'+row['file']) if k==row.get('event_kind','country_event')]
            self.assertEqual(set(row['events']),{get(n,'id') for n in events})
            for node in events:
                self.assertEqual('yes',get(node,'hidden'));self.assertEqual('yes',get(node,'is_triggered_only'))
                self.assertIsNone(get(node,'mean_time_to_happen'));self.assertIsNone(get(node,'trigger'))
                self.assertFalse(any(k=='option' for k,_,v in node))
        cleanup=get(read('common/scripted_effects/ac_retired_mechanics.txt'),'ac_retire_vanilla_crises')
        self.assertEqual(set(IDEAS),{v for k,_,v in cleanup if k=='remove_ideas'})
        self.assertEqual(set(MISSIONS),{get(n,'remove_mission') for k,n in walk(cleanup) if k=='if'})
        text=(MOD/'common/scripted_effects/ac_retired_mechanics.txt').read_text()
        for forbidden in ('set_politics','add_ideas','add_political_power','set_country_leader','transfer_state'):
            self.assertNotIn(forbidden,text)

if __name__=='__main__':unittest.main()
