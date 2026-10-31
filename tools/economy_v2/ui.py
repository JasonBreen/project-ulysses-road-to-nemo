"""Five direct-control macro pages using original briefing geometry and fonts."""
import io, json, hashlib
from PIL import Image, ImageDraw


def build_ui():
    loc = {}; controls = []; triggers = []; effects = []; positions = {}
    def local(key, text):
        loc[key]=text; return key
    def box(name, text, x,y,w=382,h=30,font=16,page=None):
        key=local('AC_MACRO_'+name.upper(),text)
        controls.append(f'instantTextboxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "ACBriefing{font}" text = "{key}" maxWidth = {w} maxHeight = {h} format = left }}')
        positions[name]=(x,y,w,h,page)
        if page is not None: triggers.append(f'{name}_visible = {{ ac_macro_ready = yes check_variable = {{ ac_macro_ui_page = {page} }} }}')
    def button(name,text,x,y,action,page=None,enabled='ac_macro_ready = yes'):
        key=local('AC_MACRO_'+name.upper(),text)
        sprite='GFX_ac_macro_close' if name=='macro_close' else 'GFX_ac_macro_button'
        tooltip='AC_MACRO_POLICY_TIMING' if 'ac_macro_can_change_policy' in enabled else key
        controls.append(f'buttonType = {{ name = "{name}" position = {{ x = {x} y = {y} }} quadTextureSprite = "{sprite}" buttonFont = "ACBriefing16" buttonText = "{key}" pdx_tooltip = "{tooltip}" clicksound = click_default '+('shortcut = "ESCAPE" ' if name=='macro_close' else '')+'}')
        positions[name]=(x,y,36 if name=='macro_close' else 140,36,page)
        effects.append(f'{name}_click = {{ {action} }}')
        triggers.append(f'{name}_click_enabled = {{ {enabled} }}')
        if page is not None:triggers.append(f'{name}_visible = {{ ac_macro_ready = yes check_variable = {{ ac_macro_ui_page = {page} }} }}')
    box('macro_title','FISCAL DIRECTORATE',28,20,730,28,20)
    box('macro_subtitle','National output, public accounts and sustained military capacity',28,58,790,32)
    button('macro_close','',794,16,'clear_variable = project_ulysses_economy_screen_open',enabled='always = yes')
    for i,title in enumerate(('Economy','Budget','Finance','Industry','Forces')):
        button('macro_tab_'+str(i),title,28+158*i,108,f'set_variable = {{ ac_macro_ui_page = {i} }}')
        triggers.append(f'macro_tab_{i}_visible = {{ ac_macro_ready = yes }}')
    box('macro_inactive','These accounts are unavailable in this save. Full economic simulation initializes only new campaign histories; saved disabled and experimental economies retain their original rules and balances.',28,180,790,180)
    triggers.append('macro_inactive_visible = { ac_macro_ready = no }')
    box('macro_footer','Forecasts update without collecting revenue. Amounts use abstract fiscal units; national accounts are fictional gameplay calibration.',28,590,790,40)
    # Page 0: macro stocks and the settled/forecast distinction.
    box('economy_title','OUTPUT AND PUBLIC ACCOUNTS',28,165,790,28,20,0)
    overview=[('real','Real annual GDP: [?ac_macro_real_gdp|.2] billion'),('nominal','Nominal annual GDP: [?ac_macro_nominal_gdp|.2] billion'),
              ('growth','Annualized real growth: [?ac_macro_growth|.2]%'),('inflation','Annual inflation: [?ac_macro_inflation|.2]%'),
              ('cash','Treasury: [?ac_macro_cash|.3] billion'),('debt','Public debt: [?ac_macro_debt|.3] billion'),
              ('revenue','Monthly revenue forecast: [?ac_macro_revenue|.3]'),('bill','Monthly obligations: [?ac_macro_bill|.3]'),
              ('balance','Forecast balance: [?ac_macro_balance|.3]'),('funding','Last obligation funding: [?ac_macro_funding|%0]'),
              ('last_revenue','Last settled revenue: [?ac_macro_last_revenue|.3]'),('last_paid','Last settled payment: [?ac_macro_last_paid|.3]')]
    for i,(name,text) in enumerate(overview):box('economy_'+name,text,28+(i%2)*410,210+(i//2)*42,page=0)
    box('economy_note','Real output uses constant 1991 prices. Nominal output includes the price index. Factories and construction queues remain physical capacity.',28,476,790,42,page=0)
    button('macro_refresh','Refresh forecast',28,532,'ac_macro_quote = yes',0)
    # Page 1: independently adjustable tax lanes and category budgets.
    box('budget_title','TAX POLICY AND CATEGORY FUNDING',28,165,790,28,20,1)
    rows=[('income_tax','Income tax: [?ac_macro_income_tax|%0]'),('business_tax','Business tax: [?ac_macro_business_tax|%0]'),('consumption_tax','Consumption tax: [?ac_macro_consumption_tax|%0]')]
    rows += [(c,' '.join(x.capitalize() for x in c.split('_'))+': level [?ac_macro_budget_'+c+'|.0] / 2  ·  [?ac_macro_spending_'+c+'|.3] billion/month') for c in ('administration','services','education','development','defense')]
    for i,(name,text) in enumerate(rows):
        y=202+i*39;box('budget_'+name,text,28,y,465,32,page=1)
        variable='ac_macro_'+name if i<3 else 'ac_macro_budget_'+name
        maximum={'income_tax':.4,'business_tax':.35,'consumption_tax':.15}.get(name,2)
        for direction,x,label,comparison in [('down',520,'Decrease','> 0'),('up',680,'Increase','< '+str(maximum))]:
            button('budget_'+name+'_'+direction,label,x,y,f'ac_macro_{name}_{direction} = yes',1,
                   f'ac_macro_can_change_policy = yes check_variable = {{ {variable} {comparison} }}')
    for i,preset in enumerate(('balanced','development','relief','mobilization')):
        button('preset_'+preset,preset.capitalize(),28+184*i,536,'ac_macro_preset_'+preset+' = yes',1,'ac_macro_can_change_policy = yes')
    # Page 2: financing and recoverable distress, no opaque bankruptcy switch.
    box('finance_title','CREDIT AND PAYMENT PRIORITIES',28,165,790,28,20,2)
    finance=[('rate','Annual sovereign rate: [?ac_macro_interest_rate|.2]%'),('interest','Monthly debt service: [?ac_macro_interest|.3]'),
             ('room','Remaining credit: [?ac_macro_credit_room|.3]'),('loan','One financing tranche: [?ac_macro_loan_size|.3]'),
             ('arrears','Unpaid obligations: [?ac_macro_arrears|.3]'),('new_arrears','Last new arrears: [?ac_macro_last_arrears_added|.3]'),
             ('stress','Consecutive shortfall months: [?ac_macro_stress_months|.0]'),('recovery','Successful recovery months: [?ac_macro_recovery_months|.0]')]
    for i,(name,text) in enumerate(finance):box('finance_'+name,text,28+(i%2)*410,210+(i//2)*42,page=2)
    box('finance_note','Credit can cover a shortfall without erasing debt. Unfunded obligations become arrears. Three sustained shortfall months trigger a recoverable fiscal crisis.',28,400,790,52,page=2)
    button('macro_borrow','Borrow tranche',28,474,'ac_macro_borrow = yes',2,'ac_macro_can_borrow = yes')
    button('macro_repay','Repay tranche',212,474,'ac_macro_repay = yes',2,'ac_macro_can_repay = yes')
    button('macro_ease','Ease credit',438,474,'ac_macro_policy_rate_down = yes',2,'ac_macro_can_change_policy = yes check_variable = { ac_macro_policy_rate > 2 }')
    button('macro_tighten','Tighten credit',622,474,'ac_macro_policy_rate_up = yes',2,'ac_macro_can_change_policy = yes check_variable = { ac_macro_policy_rate < 8 }')
    for i,title in enumerate(('low','standard','high')):
        button('macro_tax_preset_'+title,title.capitalize()+' taxes',28+184*i,532,'ac_macro_tax_'+title+' = yes',2,'ac_macro_can_change_policy = yes')
    button('macro_stabilize','Stabilization',622,532,'ac_macro_preset_stabilization = yes',2,'ac_macro_can_change_policy = yes')
    # Page 3: queue-observed procurement; never claim an unimplemented reservation.
    box('industry_title','PHYSICAL INDUSTRY AND REPLACEMENT FUNDING',28,165,790,28,20,3)
    for i,(name,text) in enumerate([('civ','Civilian factories: [?ac_macro_civilian_factories|.0]'),('mil','Military factories: [?ac_macro_military_factories|.0]'),
                                   ('docks','Dockyards: [?ac_macro_dockyards|.0]'),('escrow','Replacement escrow: [?ac_macro_replacement_escrow|.3]'),
                                   ('produced','Native infantry production total: [?ac_macro_infantry_produced|.0]'),('target','Programme completion target: [?ac_macro_replacement_target|.0]')]):
        box('industry_'+name,text,28+(i%2)*410,210+(i//2)*46,page=3)
    box('industry_note','A replacement programme reserves 0.005 billion until the native production queue makes 100 additional infantry equipment. Completion supports readiness; the equipment already exists and is never granted twice. No factory or production line is reserved by this programme.',28,370,790,94,page=3)
    button('macro_order','Fund replacements',28,500,'ac_macro_fund_replacements = yes',3,'ac_macro_can_fund_replacements = yes')
    button('macro_cancel','Cancel funding',212,500,'ac_macro_cancel_replacements = yes',3,'ac_macro_ready = yes check_variable = { ac_macro_replacement_escrow > 0 }')
    # Page 4: observed deployed forces and sustained readiness.
    box('forces_title','OPERATING FORCES AND READINESS',28,165,790,28,20,4)
    forces=[('army','Army personnel: [?ac_macro_army_k|.1] thousand'),('navy','Naval personnel: [?ac_macro_navy_k|.1] thousand'),
            ('aircrew','Air personnel: [?ac_macro_air_k|.1] thousand'),('planes','Deployed aircraft: [?ac_macro_planes|.0]'),
            ('ships','Commissioned hulls: [?ac_macro_ships|.0]'),('upkeep','Monthly force obligation: [?ac_macro_upkeep|.3]'),
            ('readiness','Sustained readiness: [?ac_macro_readiness|.0] / 100'),('envelope','Defense envelope: [?ac_macro_spending_defense|.3]')]
    for i,(name,text) in enumerate(forces):box('forces_'+name,text,28+(i%2)*410,210+(i//2)*44,page=4)
    box('forces_note','Personnel, hulls and aircraft determine operating obligations. War raises their burden. Supply, fuel and equipment remain physical systems. Underfunding degrades readiness gradually; restoring funding permits recovery without deleting units.',28,418,790,92,page=4)
    gui='guiTypes = { containerWindowType = { name = "ac_macro_economy_screen" position = { x = 0 y = 0 } orientation = CENTER origo = CENTER size = { width = 860 height = 640 } moveable = yes background = { name = "Background" quadTextureSprite = "GFX_ac_macro_panel" }\n'+'\n'.join(controls)+'\n} }\n'
    sg='scripted_gui = { ac_macro_economy_screen = { window_name = "ac_macro_economy_screen" context_type = player_context visible = { has_variable = project_ulysses_economy_screen_open ac_macro_mode = yes } triggers = {\n'+'\n'.join(triggers)+'\n} effects = {\n'+'\n'.join(effects)+'\n} } }\n'
    out={'interface/ac_macro_economy.gui':gui,'common/scripted_guis/ac_macro_economy.txt':sg}
    assets=[];gfx=[]
    for name,w,h,n in [('panel',860,640,1),('button',140,36,4),('close',36,36,4)]:
        image=Image.new('RGBA',(w*n,h),(0,0,0,0))
        for frame in range(n):
            tile=Image.new('RGBA',(w,h),(8,22,33,255));d=ImageDraw.Draw(tile)
            color=[(93,208,223,255),(218,237,242,255),(230,181,95,255),(52,82,98,255)][frame]
            d.rectangle((0,0,w-1,h-1),outline=color,width=1)
            if name=='panel':
                d.line((18,96,842,96),fill=(52,82,98,255));d.line((18,578,842,578),fill=(52,82,98,255))
            if name=='close':
                d.line((10,10,26,26),fill=color,width=2);d.line((10,26,26,10),fill=color,width=2)
            image.alpha_composite(tile,(frame*w,0))
        stream=io.BytesIO();image.save(stream,format='DDS');data=stream.getvalue()
        path='gfx/interface/ac_macro/'+name+'.dds';out[path]=data
        gfx.append(f'spriteType = {{ name = "GFX_ac_macro_{name}" texturefile = "{path}" noOfFrames = {n} }}')
        assets.append(dict(file=path,width=w*n,height=h,frames=n,sha256=hashlib.sha256(data).hexdigest(),source='original procedural geometry; tools/economy_v2/ui.py'))
    out['interface/ac_macro_economy.gfx']='spriteTypes = {\n'+'\n'.join(gfx)+'\n}\n'
    loc.update(ac_economy_full='Full national economy',ac_economy_full_desc='Default for new campaigns. Model real output, inflation, category budgets, public debt and sustained military costs. National accounts and prices are fictional calibration. Saved legacy campaigns retain their original mode.',
               AC_MACRO_POLICY_TIMING='Tax, spending and monetary changes share a 30-day cooldown. Forecasts update immediately; public services and investment benefits are delivered through monthly settlement.',
               ac_macro_economy_modifier='Public accounts and force readiness',ac_macro_economy_modifier_desc='Delivered public services and sustained operating funds affect the national economy and military readiness.',
               **{'ac_macro.1.t':'A shortfall in public accounts','ac_macro.1.d':'The monthly accounts show that not all approved obligations were funded. Departments are carrying unpaid bills. The government still has time to reprioritize the budget, improve revenue or arrange financing.','ac_macro.1.a':'Review the accounts.',
                  'ac_macro.2.t':'The fiscal warning becomes a crisis','ac_macro.2.d':'Three successive settlements have left a material funding gap. Readiness and civilian services are deteriorating. The state can recover through sustainable funding and repayment of arrears; no government or territorial outcome is imposed by this accounting crisis.','ac_macro.2.a':'Prepare a recovery budget.',
                  'ac_macro.3.t':'Public accounts stabilize','ac_macro.3.d':'Three successful settlements and cleared arrears have ended the fiscal crisis. Departments can plan again, although readiness and productive conditions will take time to recover.','ac_macro.3.a':'Keep the recovery on course.'})
    out['localisation/english/ac_macro_l_english.yml']=('l_english:\n'+'\n'.join(' '+key+':0 "'+value.replace('"','\\"')+'"' for key,value in sorted(loc.items()))+'\n').encode('utf-8-sig')
    # Metadata stays beside delivered textures so the source-only builder can
    # validate hashes without importing any installed reference imagery.
    out['gfx/interface/ac_macro/manifest.json']=json.dumps(dict(schema=1,assets=assets,positions=positions,native_status='untested'),indent=2)+'\n'
    return out
