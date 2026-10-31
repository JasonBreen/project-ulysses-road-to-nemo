"""Five direct-control macro pages using original briefing geometry and fonts."""
import io, json, hashlib
from PIL import Image, ImageDraw


def build_ui():
    loc = {}; controls = []; triggers = []; effects = []; positions = {}; properties = []
    def local(key, text):
        loc[key]=text; return key
    def box(name, text, x,y,w=382,h=30,font=16,page=None,condition=None,tooltip=None):
        key=local('AC_MACRO_'+name.upper(),text)
        controls.append(f'instantTextboxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "ACBriefing{font}" text = "{key}" maxWidth = {w} maxHeight = {h} format = left '+(f'pdx_tooltip = "{tooltip}" ' if tooltip else '')+'}')
        positions[name]=(x,y,w,h,page)
        if page is not None: triggers.append(f'{name}_visible = {{ ac_macro_ready = yes check_variable = {{ ac_macro_ui_page = {page} }} '+(condition or '')+' }')
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
    for i,title in enumerate(('Overview','Budget','Industry','Debt / contracts','Ledger')):
        button('macro_tab_'+str(i),title,28+158*i,108,f'set_variable = {{ ac_macro_ui_page = {i} }}')
        triggers.append(f'macro_tab_{i}_visible = {{ ac_macro_ready = yes }}')
    box('macro_inactive','These accounts are unavailable in this save. Full economic simulation initializes only new campaign histories; saved disabled and experimental economies retain their original rules and balances.',28,180,790,180)
    triggers.append('macro_inactive_visible = { ac_macro_ready = no }')
    box('macro_footer','All amounts: billions of abstract fiscal units, at current prices unless marked real. Fictional gameplay calibration. Forecast refresh never collects money or records a settlement.',28,650,790,40)
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
    box('economy_healthy','No active fiscal warning. Two materially underfunded settlements open a three-month correction period.',28,582,790,48,page=0,condition='NOT = { has_country_flag = ac_macro_warning } NOT = { has_country_flag = ac_macro_crisis }')
    box('economy_warning','Fiscal warning: [?ac_macro_warning_months_left|.0] monthly correction settlements remain. Raise revenue, reprioritize spending or arrange sustainable finance.',28,582,790,48,page=0,condition='has_country_flag = ac_macro_warning NOT = { has_country_flag = ac_macro_crisis }')
    box('economy_crisis','Fiscal crisis: [?ac_macro_recovery_months|.0] / 3 funded recovery settlements. Arrears must decline or remain zero. Debt is retained.',28,582,790,48,page=0,condition='has_country_flag = ac_macro_crisis')
    # Page 1: independently adjustable tax lanes and category budgets.
    box('budget_title','TAX POLICY AND CATEGORY FUNDING',28,165,790,28,20,1)
    rows=[('income_tax','Income tax: [?ac_macro_income_tax|%0]'),('business_tax','Business tax: [?ac_macro_business_tax|%0]'),('consumption_tax','Consumption tax: [?ac_macro_consumption_tax|%0]')]
    rows += [(c,' '.join(x.capitalize() for x in c.split('_'))+': level [?ac_macro_budget_'+c+'|.0] / 2  ·  [?ac_macro_spending_'+c+'|.3] billion/month') for c in ('administration','services','education','development','defense')]
    for i,(name,text) in enumerate(rows):
        tooltip = 'AC_MACRO_EXPLAIN_' + name.upper()
        y=202+i*39;box('budget_'+name,text,28,y,465,32,page=1,tooltip=tooltip)
        variable='ac_macro_'+name if i<3 else 'ac_macro_budget_'+name
        maximum={'income_tax':.4,'business_tax':.35,'consumption_tax':.15}.get(name,2)
        for direction,x,label,comparison in [('down',520,'Decrease','> 0'),('up',680,'Increase','< '+str(maximum))]:
            button('budget_'+name+'_'+direction,label,x,y,f'ac_macro_{name}_{direction} = yes',1,
                   f'ac_macro_can_change_policy = yes check_variable = {{ {variable} {comparison} }}')
    for i,preset in enumerate(('balanced','development','relief','mobilization')):
        button('preset_'+preset,preset.capitalize(),28+184*i,536,'ac_macro_preset_'+preset+' = yes',1,'ac_macro_can_change_policy = yes')
    box('budget_note','Hover each policy for its economic base or delivered service. Tax bases differ; collection efficiency is [?ac_macro_effective_collection|%0]. Levels 0 / 1 / 2 fund 75% / 100% / 125% of the standard category envelope.',28,586,790,52,page=1)
    # Page 3: debt, explicit commitments and native-production funding escrow.
    box('finance_title','DEBT AND CONTRACT OBLIGATIONS',28,165,790,28,20,3)
    finance=[('rate','Annual sovereign rate: [?ac_macro_interest_rate|.2]%'),('interest','Monthly debt service: [?ac_macro_interest|.3]'),
             ('room','Remaining credit: [?ac_macro_credit_room|.3]'),('loan','One financing tranche: [?ac_macro_loan_size|.3]'),
             ('arrears','Unpaid obligations: [?ac_macro_arrears|.3]'),('new_arrears','Last new arrears: [?ac_macro_last_arrears_added|.3]'),
             ('stress','Consecutive shortfall months: [?ac_macro_stress_months|.0]'),('recovery','Successful recovery months: [?ac_macro_recovery_months|.0]')]
    for i,(name,text) in enumerate(finance):box('finance_'+name,text,28+(i%2)*410,210+(i//2)*36,page=3)
    box('finance_commitments','Other annual commitments: [?ac_macro_commitments_annual|.3]  |  Replacement escrow: [?ac_macro_replacement_escrow|.3]',28,365,790,32,page=3)
    box('finance_note','Two failed settlements begin a three-month correction warning. Further underfunding after that window activates a recoverable crisis. Recovery needs three funded months with arrears declining or already cleared.',28,402,790,50,page=3)
    button('macro_borrow','Borrow tranche',28,474,'ac_macro_borrow = yes',3,'ac_macro_can_borrow = yes')
    button('macro_repay','Repay tranche',212,474,'ac_macro_repay = yes',3,'ac_macro_can_repay = yes')
    button('macro_ease','Ease credit',438,474,'ac_macro_policy_rate_down = yes',3,'ac_macro_can_change_policy = yes check_variable = { ac_macro_policy_rate > 2 }')
    button('macro_tighten','Tighten credit',622,474,'ac_macro_policy_rate_up = yes',3,'ac_macro_can_change_policy = yes check_variable = { ac_macro_policy_rate < 8 }')
    for i,title in enumerate(('low','standard','high')):
        button('macro_tax_preset_'+title,title.capitalize()+' taxes',28+184*i,532,'ac_macro_tax_'+title+' = yes',3,'ac_macro_can_change_policy = yes')
    button('macro_stabilize','Stabilization',622,532,'ac_macro_preset_stabilization = yes',3,'ac_macro_can_change_policy = yes')
    box('finance_accounts','The ledger records paid and unpaid obligations separately. Active political commitments remain owned by their institutions; national aid keeps its own eligibility and delivery guards.',28,586,790,52,page=3)
    # Page 2 combines physical capacity and its operating obligations.
    box('industry_title','INDUSTRY AND SUSTAINED READINESS',28,165,790,28,20,2)
    for i,(name,text) in enumerate([('civ','Civilian factories: [?ac_macro_civilian_factories|.0]'),('mil','Military factories: [?ac_macro_military_factories|.0]'),
                                   ('docks','Dockyards: [?ac_macro_dockyards|.0]'),('escrow','Replacement escrow: [?ac_macro_replacement_escrow|.3]'),
                                   ('produced','Native infantry production total: [?ac_macro_infantry_produced|.0]'),('target','Programme completion target: [?ac_macro_replacement_target|.0]')]):
        box('industry_'+name,text,28+(i%2)*410,205+(i//2)*29,h=28,page=2)
    forces=[('army','Army personnel: [?ac_macro_army_k|.1] thousand'),('navy','Naval personnel: [?ac_macro_navy_k|.1] thousand'),
            ('aircrew','Air personnel: [?ac_macro_air_k|.1] thousand'),('planes','Deployed aircraft: [?ac_macro_planes|.0]'),
            ('ships','Commissioned hulls: [?ac_macro_ships|.0]'),('upkeep','Monthly force obligation: [?ac_macro_upkeep|.3]'),
            ('readiness','Sustained readiness: [?ac_macro_readiness|.0] / 100'),('envelope','Defense envelope: [?ac_macro_spending_defense|.3]')]
    for i,(name,text) in enumerate(forces):box('forces_'+name,text,28+(i%2)*410,307+(i//2)*29,h=28,page=2)
    box('industry_note','Funding reserves 0.005 billion until native queues produce 100 more infantry equipment. Completion supports readiness and grants no duplicate goods. Fuel, supply, losses and replacement equipment remain physical requirements.',28,440,790,66,page=2)
    button('macro_order','Fund replacements',28,522,'ac_macro_fund_replacements = yes',2,'ac_macro_can_fund_replacements = yes')
    button('macro_cancel','Cancel funding',212,522,'ac_macro_cancel_replacements = yes',2,'ac_macro_ready = yes check_variable = { ac_macro_replacement_escrow > 0 }')
    box('forces_note','Underfunding reduces readiness gradually. Funded operations allow recovery; a missed payment does not delete units. Defense obligations cannot fall below observed force requirements.',28,584,790,52,page=2)
    # Page 4: twelve actually settled results. Graph frames are written only by
    # the monthly ledger owner; selecting a tab never changes the history.
    box('ledger_title','SETTLED MONTHLY LEDGER',28,165,790,28,20,4)
    box('ledger_empty','No settled monthly accounts have been recorded. The opening forecast is not a historical payment. The first scheduled settlement is February 1991.',28,230,790,120,page=4,condition='check_variable = { ac_macro_history_count = 0 }')
    box('ledger_output_label','Real annual output | scale [?ac_macro_graph_output_max|.2]',28,202,382,26,page=4,condition='check_variable = { ac_macro_history_count > 0 }')
    box('ledger_net_label','Settled revenue minus bills | ±[?ac_macro_graph_net_max|.3]',438,202,382,26,page=4,condition='check_variable = { ac_macro_history_count > 0 }')
    for i in range(12):
        for kind,x,y,h,sprite in [('output',40+(11-i)*28,235,96,'output'),('net_positive',450+(11-i)*28,235,48,'net_positive'),('net_negative',450+(11-i)*28,284,48,'net_negative')]:
            name=f'ledger_graph_{i}_{kind}'
            controls.append(f'iconType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "GFX_ac_macro_graph_{sprite}" }}')
            positions[name]=(x,y,20,h,4)
            triggers.append(f'{name}_visible = {{ ac_macro_ready = yes check_variable = {{ ac_macro_ui_page = 4 }} check_variable = {{ ac_macro_history_count > {i} }} }}')
            properties.append(f'{name} = {{ frame = ac_macro_graph_{i}_{kind} }}')
    box('ledger_direction','Cash quantum: 0.001b; remainders carry forward. Graphs: oldest left, latest right; one recorded settlement per column.',28,340,790,26,page=4,condition='check_variable = { ac_macro_history_count > 0 }')
    headings=[('sequence','Entry',28,70),('revenue','Revenue',108,132),('bill','Bills',250,132),('paid','Paid',392,132),('debt','Debt',534,132),('arrears','Arrears',676,144)]
    for field,title,x,w in headings:box('ledger_head_'+field,title,x,376,w,26,page=4,condition='check_variable = { ac_macro_history_count > 0 }')
    for i in range(12):
        for field,title,x,w in headings:
            fmt='.0' if field=='sequence' else '.3'
            box(f'ledger_{i}_{field}',f'[?ac_macro_history_{i}_{field}|{fmt}]',x,406+i*19,w,19,page=4,condition=f'check_variable = {{ ac_macro_history_count > {i} }}')
    gui='guiTypes = { containerWindowType = { name = "ac_macro_economy_screen" position = { x = 0 y = 0 } orientation = CENTER origo = CENTER size = { width = 860 height = 700 } moveable = yes background = { name = "Background" quadTextureSprite = "GFX_ac_macro_panel" }\n'+'\n'.join(controls)+'\n} }\n'
    sg='scripted_gui = { ac_macro_economy_screen = { window_name = "ac_macro_economy_screen" context_type = player_context visible = { has_variable = project_ulysses_economy_screen_open ac_macro_mode = yes } properties = {\n'+'\n'.join(properties)+'\n} triggers = {\n'+'\n'.join(triggers)+'\n} effects = {\n'+'\n'.join(effects)+'\n} } }\n'
    out={'interface/ac_macro_economy.gui':gui,'common/scripted_guis/ac_macro_economy.txt':sg}
    assets=[];gfx=[]
    for name,w,h,n in [('panel',860,700,1),('button',140,36,4),('close',36,36,4),('graph_output',20,96,33),('graph_net_positive',20,48,33),('graph_net_negative',20,48,33)]:
        image=Image.new('RGBA',(w*n,h),(0,0,0,0))
        for frame in range(n):
            tile=Image.new('RGBA',(w,h),(8,22,33,255));d=ImageDraw.Draw(tile)
            color=[(93,208,223,255),(218,237,242,255),(230,181,95,255),(52,82,98,255)][min(frame,3)]
            if name.startswith('graph_'):
                color=(149,179,221,255) if name=='graph_net_negative' else (93,208,223,255)
                extent=round((h-1)*frame/32)
                if extent:
                    # Reserve one baseline pixel. Even frame2 must visibly
                    # differ from zero instead of being painted over by it.
                    if name=='graph_net_negative':d.rectangle((3,1,w-4,extent),fill=color)
                    else:d.rectangle((3,h-1-extent,w-4,h-2),fill=color)
                d.line((0,0 if name=='graph_net_negative' else h-1,w-1,0 if name=='graph_net_negative' else h-1),fill=(52,82,98,255))
            else:d.rectangle((0,0,w-1,h-1),outline=color,width=1)
            if name=='panel':
                d.line((18,96,842,96),fill=(52,82,98,255));d.line((18,644,842,644),fill=(52,82,98,255))
            if name=='close':
                d.line((10,10,26,26),fill=color,width=2);d.line((10,26,26,10),fill=color,width=2)
            image.alpha_composite(tile,(frame*w,0))
        stream=io.BytesIO();image.save(stream,format='DDS');data=stream.getvalue()
        path='gfx/interface/ac_macro/'+name+'.dds';out[path]=data
        gfx.append(f'spriteType = {{ name = "GFX_ac_macro_{name}" texturefile = "{path}" noOfFrames = {n} }}')
        assets.append(dict(file=path,width=w*n,height=h,frames=n,sha256=hashlib.sha256(data).hexdigest(),source='original procedural geometry; tools/economy_v2/ui.py'))
    out['interface/ac_macro_economy.gfx']='spriteTypes = {\n'+'\n'.join(gfx)+'\n}\n'
    loc.update(AC_MACRO_EXPLAIN_INCOME_TAX='Household income is estimated at 55% of nominal taxable output. Its selected rate and collection efficiency apply to that base; monthly receipts are annual receipts divided by12. Forecast: [?ac_macro_revenue_income|.3] billion/month.',
               AC_MACRO_EXPLAIN_BUSINESS_TAX='Business surplus is estimated at 25% of nominal taxable output. Its selected rate and collection efficiency apply to that base. Forecast: [?ac_macro_revenue_business|.3] billion/month.',
               AC_MACRO_EXPLAIN_CONSUMPTION_TAX='Consumption is estimated at 65% of nominal taxable output, a different incidence from household income and business surplus. Forecast: [?ac_macro_revenue_consumption|.3] billion/month.',
               AC_MACRO_EXPLAIN_ADMINISTRATION='The standard annual envelope is1.5% of nominal output. Delivered administration supports collection efficiency; levels0/1/2 fund75%/100%/125% of that envelope.',
               AC_MACRO_EXPLAIN_SERVICES='The standard annual envelope is5% of nominal output. Delivered public services affect stability. A target is an obligation; it is not proof that services were funded.',
               AC_MACRO_EXPLAIN_EDUCATION='The standard annual envelope is3% of nominal output. Funded education and research support research capability and gradual productive growth.',
               AC_MACRO_EXPLAIN_DEVELOPMENT='The standard annual envelope is2% of nominal output. Delivered development supports construction and gradual disruption recovery; native queues still build physical capacity.',
               AC_MACRO_EXPLAIN_DEFENSE='The standard annual envelope is3% of nominal output, with observed force requirements as a floor. Funding supports personnel, maintenance and readiness; it does not replace physical fuel, supplies or equipment.')
    loc.update(ac_economy_full='Full national economy',ac_economy_full_desc='Default for new campaigns. Model real output, inflation, category budgets, public debt and sustained military costs. National accounts and prices are fictional calibration. Saved legacy campaigns retain their original mode.',
               AC_MACRO_POLICY_TIMING='Tax, spending and monetary changes share a 30-day cooldown. Forecasts update immediately; public services and investment benefits are delivered through monthly settlement.',
               ac_macro_economy_modifier='Public accounts and force readiness',ac_macro_economy_modifier_desc='Delivered public services and sustained operating funds affect the national economy and military readiness.',
               **{'ac_macro.1.t':'A shortfall in public accounts','ac_macro.1.d':'The monthly accounts show that not all approved obligations were funded. Departments are carrying unpaid bills. The government still has time to reprioritize the budget, improve revenue or arrange financing.','ac_macro.1.a':'Review the accounts.',
                  'ac_macro.2.t':'The fiscal warning becomes a crisis','ac_macro.2.d':'Two failed settlements were followed by three correction months, but a material funding gap remains. Readiness and civilian services are deteriorating. Sustainable funding and repayment of arrears can restore the accounts without imposing a government or territorial outcome.','ac_macro.2.a':'Prepare a recovery budget.',
                  'ac_macro.3.t':'Public accounts stabilize','ac_macro.3.d':'Three funded settlements with arrears declining or already cleared have ended the active fiscal crisis. Outstanding debt and unpaid obligations still have to be honored. Readiness and productive conditions will take time to recover.','ac_macro.3.a':'Keep the recovery on course.'})
    out['localisation/english/ac_macro_l_english.yml']=('l_english:\n'+'\n'.join(' '+key+':0 "'+value.replace('"','\\"')+'"' for key,value in sorted(loc.items()))+'\n').encode('utf-8-sig')
    # Metadata stays beside delivered textures so the source-only builder can
    # validate hashes without importing any installed reference imagery.
    out['gfx/interface/ac_macro/manifest.json']=json.dumps(dict(schema=1,assets=assets,positions=positions,native_status='untested'),indent=2)+'\n'
    return out
