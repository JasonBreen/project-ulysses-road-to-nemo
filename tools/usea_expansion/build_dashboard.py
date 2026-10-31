"""Repair the fiscal dashboard from its recorded control contract.

Page controls are direct scripted-GUI children with individual visibility rules.
The previous nested-container rules left all three pages visible in 1.19.4.
"""
import argparse,copy,json
from pathlib import Path
from script import parse,render,get,setv,walk,xy,size
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'

POSITIONS={
    'dashboard_title':(28,20,730,28),'dashboard_subtitle':(28,54,760,40),
    'close_button':(794,16),'tab_overview':(28,108),'tab_budget':(202,108),'tab_contracts':(376,108),
    'ov_title':(28,168,790,28),'ov_treasury':(28,211,382,32),'ov_debt':(438,211,382,32),
    'ov_arrears':(28,254,382,32),'ov_credit':(438,254,382,32),
    'ov_capacity':(28,297,382,32),'ov_current_balance':(438,297,382,32),
    'ov_budget_header':(28,350,790,28),'ov_revenue':(28,392,382,32),'ov_civil':(438,392,382,32),
    'ov_military':(28,435,382,32),'ov_interest':(438,435,382,32),'ov_last':(28,478,790,32),
    'refresh_button':(28,524),
    'budget_title':(28,168,790,28),'budget_tax':(28,211,790,32),'budget_tax_cooldown':(28,248,790,32),
    'tax_low_button':(28,290),'tax_standard_button':(202,290),'tax_high_button':(376,290),
    'budget_services':(28,363,790,32),'budget_services_cooldown':(28,400,790,32),
    'services_basic_button':(28,442),'services_rebuild_button':(202,442),'budget_note':(28,517,790,48),
    'contracts_title':(28,168,790,28),'contracts_credit':(28,211,790,32),'contracts_debt':(28,248,790,32),
    'borrow_button':(28,290),'repay_button':(202,290),'contracts_procurement':(28,363,790,32),
    'contracts_pulses':(28,400,790,32),'order_button':(28,442),'cancel_order_button':(202,442),
    'contracts_note':(28,517,790,48),'footer':(28,590,790,40),
}

def build():
    data=json.loads((HERE/'dashboard_contract.json').read_text())
    gui=copy.deepcopy(data['gui']);sg=copy.deepcopy(data['scripted_gui'])
    window=next(n for _,n in walk(gui) if get(n,'name')=='"project_ulysses_economy_screen"')
    logic=get(get(sg,'scripted_gui'),'project_ulysses_economy_screen')
    # Full mode uses the new five-page directorate; saved legacy mode retains
    # this exact three-page control/transaction contract.
    setv(logic,'visible',parse('has_variable = project_ulysses_economy_screen_open ac_macro_mode = no'))
    triggers=get(logic,'triggers');triggers[:]=[r for r in triggers if not r[0].endswith('_panel_visible')]
    setv(window,'size',size(860,640))
    setv(get(window,'background'),'quadTextureSprite','"GFX_ac_ui_economy_background"')
    # Flatten only the three page containers. Preserve all click/control IDs.
    flat=[]
    for kind,op,node in window:
        if kind=='containerWindowType' and get(node,'name','').strip('"') in ('overview_panel','budget_panel','contracts_panel'):
            page=('overview_panel','budget_panel','contracts_panel').index(get(node,'name').strip('"'))
            for row in node:
                if row[0] not in ('instantTextboxType','buttonType'):continue
                flat.append(row)
                name=get(row[2],'name').strip('"')
                triggers.append([name+'_visible','=',parse('ac_econ_ready = yes check_variable = { ac_econ_ui_tab = '+str(page)+' }')])
        else:flat.append([kind,op,node])
    window[:]=flat
    for _,node in walk(gui):
        name=get(node,'name','').strip('"')
        for field in ('font','buttonFont'):
            old=get(node,field)
            if old:setv(node,field,'"ACBriefing20"' if '20' in old else '"ACBriefing16"')
        if name in POSITIONS:
            p=POSITIONS[name];setv(node,'position',xy(*p[:2]))
            if len(p)>2:setv(node,'maxWidth',str(p[2]));setv(node,'maxHeight',str(p[3]))
        if get(node,'spriteType')=='"GFX_icon_button_60x60"':
            setv(node,'spriteType','"GFX_ac_ui_economy_close"' if name=='close_button' else '"GFX_ac_ui_economy_button"')
        if name=='close_button':setv(node,'shortcut','"ESCAPE"')
        if name=='project_ulysses_economy_screen_open_button':
            setv(node,'position',xy(-188,-68));setv(node,'size',size(160,40))
    for tab in ('tab_overview','tab_budget','tab_contracts'):
        triggers.append([tab+'_visible','=',parse('ac_econ_ready = yes')])
    window.extend(parse('''instantTextboxType = {
        name = "disabled_title" position = { x = 28 y = 172 } font = "ACBriefing20"
        text = "AC_ECON_UI_DISABLED_TITLE" maxWidth = 790 maxHeight = 28 format = left
    }
    instantTextboxType = {
        name = "disabled_message" position = { x = 28 y = 218 } font = "ACBriefing16"
        text = "AC_ECON_UI_DISABLED_MESSAGE" maxWidth = 790 maxHeight = 270 format = left
        scrollbarType = "ac_exp_standardtext_slider"
    }'''))
    for name in ('disabled_title','disabled_message'):
        triggers.append([name+'_visible','=',parse('NOT = { ac_econ_ready = yes }')])
    # The effect owners retain all readiness/cooldown/escrow checks.
    return {'interface/ac_economy_gui.gui':render(gui)+'\n','common/scripted_guis/ac_economy.txt':render(sg)+'\n'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for file,text in build().items():
        target=MOD/file
        if a.check:
            if target.read_text()!=text:raise SystemExit('Dashboard differs from authoring source: '+file)
        else:target.write_text(text,encoding='utf-8')
    print('Economy dashboard: bounded 860x640; individual page visibility; explicit inactive state.')
