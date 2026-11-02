"""Explicit national purposes, not a count-driven grid.

All policy, dialogue and institutional detail below is provisional authored
gameplay. Chronicle dates are context only; no territorial or war owner here.
"""
from dataclasses import dataclass

COUNTRIES = {
    'FAT': dict(name='FATO', tree='fat_national_campaign', category='Authorisations and obligations', columns=6),
    'SBK': dict(name='South Belka', tree='sbk_civil_recovery_campaign', category='The civil docket', columns=7),
}

@dataclass(frozen=True)
class Focus:
    tag: str
    suffix: str
    title: str
    narrative: str
    purpose: str
    kind: str
    hook: str
    subjects: tuple
    phase: int
    index: int
    requirements: tuple = ()
    exclusive: str = ''
    major: bool = False

    @property
    def id(self): return self.tag + '_nat_' + self.suffix
    @property
    def x(self): return 2 + (self.index % COUNTRIES[self.tag]['columns']) * 3
    @property
    def y(self): return POSITIONS[self.id][1]
    @property
    def cost(self): return 10 if self.major else 5

FOCUSES=[]
def add(tag, phase, suffix, title, narrative, purpose, kind, hook, subjects, req=(), exclusive='', major=False):
    index=sum(r.tag==tag and r.phase==phase for r in FOCUSES)
    # A prerequisite tuple is an OR group; separate tuples are AND groups.
    requirements=tuple((item,) if isinstance(item,str) else tuple(item) for item in req)
    FOCUSES.append(Focus(tag,suffix,title,narrative,purpose,kind,str(hook),tuple(subjects.split('/')),phase,index,requirements,exclusive,major))

def fat(phase,*args,**kwargs):add('FAT',phase,*args,**kwargs)
def sbk(phase,*args,**kwargs):add('SBK',phase,*args,**kwargs)

# FATO: the 1991 authorisation system, the burden of the existing crisis, and
# a later renewal. Each row has an explicit consumer/effect in build.py.
fat(0,'accounts_at_the_gate','Accounts at the Gate',
    'The freight works has three requisitions and enough wagons for two. The clerk asks which signature carries the authority to turn the third away. Before promising anything abroad, the government must decide how its own factories are heard.',
    'Opening allocation hearing chooses a public or executive accounting procedure.','scene',1,'document/industry')
fat(0,'civilian_priority','Protect the Civilian Order Book',
    'A replacement pump rarely looks urgent beside a military requisition. Yet missed civilian orders close workshops and send skilled people elsewhere. Reserve a share of production for those contracts, accepting the cost to the armament schedule.',
    'Enduring civilian priority: construction and stability, with a military-output cost.','policy','civilian_priority','civil/assembly',req=['accounts_at_the_gate'],exclusive='plant_priority',major=True)
fat(0,'plant_priority','The Plant Comes First',
    'Managers argue that full military order books keep the whole industrial district employed. They offer a tighter production schedule, provided civilian customers accept longer waits. The government can back that bargain without pretending the postponed work disappears.',
    'Alternative industrial priority: military output with consumer and stability burdens.','policy','plant_priority','industry/command',req=['accounts_at_the_gate'],exclusive='civilian_priority',major=True)
fat(0,'invoice_rules','An Invoice Must Name Its Author',
    'A requisition stamped by three offices can still belong to none of them. Require an identifiable author and a reason for every exceptional order. An audit will cost staff time; its findings will also make a withdrawal defensible.',
    'Unlock a paid invoice audit that improves institutional capacity and records an inspected warrant.','action','invoice_audit','scales/document',req=['accounts_at_the_gate'])
fat(0,'labour_bench','A Place for the Workshop Delegate',
    'The wage clerk knows when a nominally spare shift is already exhausted. Give workshop delegates access to the allocation meeting. Their presence slows an order down but permits a genuine negotiated maintenance interval.',
    'Unlock a negotiated maintenance interval, exchanging current output for reliability.','action','maintenance_interval','tools/ballot',req=['accounts_at_the_gate'])
fat(0,'reserve_floor','The Reserve Is Not a Promise',
    'An unopened crate in a warehouse is not automatically available to an ally. The quartermaster wants a published domestic floor beneath every shipment. Keeping that floor makes smaller offers credible and prevents a signature from consuming the last replacement batch.',
    'Require a larger domestic infantry reserve before delivery; unlock a smaller emergency consignment.','capability','reserve_floor','logistics/security',req=[('civilian_priority','plant_priority')])
fat(0,'border_book','The Border Accounts',
    'The existing border leaves the customs desk with inherited ledgers, disputed invoices and ordinary traffic. The question before the ministry is administrative: accept locally checked receipts, or hold every exception for a central signature. Neither choice redraws a frontier.',
    'Choose local verification or central review of existing border accounts.','scene',2,'gate/document',req=['invoice_rules'])
fat(0,'route_contract','Contract for the Journey',
    'A promised truck is useful only if somebody has reserved its journey and its replacement. Put transport on its own warrant instead of hiding it inside a general promise. Vehicles must leave a real stockpile when the delivery is made.',
    'Unlock stock-backed motor-transport warrants.','capability','mobility_warrant','rail/logistics',req=['reserve_floor'])
fat(0,'partner_register','A Register of Willing Recipients',
    'A neighbouring government is entitled to decline. Contact the existing authorities in Gebet, Recta and Osea through a written offer that specifies its stock and deadline. These contacts are practical arrangements and confer no faction membership.',
    'Unlock bounded requests to three eligible existing partners, with receiver consent.','capability','partner_register','diplomacy/document',req=['border_book'])
fat(0,'consent_clause','Consent Survives the Signature',
    'An acceptance made before a crisis may no longer fit the receiver\'s circumstances. Give each authority a visible right to revoke before dispatch. Extend the response period, but require a fresh check of both governments at delivery.',
    'Allow a longer consent window and recipient revocation; no automatic delivery.','capability','long_consent','diplomacy/scales',req=['partner_register'])
fat(0,'shopfloor_ballot','The Shift Meeting',
    'A voluntary extra shift needs more than a ministerial slogan. Let the plant committee negotiate its duration and rest period. A limited productivity campaign can then be authorised without making permanent emergency hours the default.',
    'Unlock a paid, temporary negotiated extra shift with an explicit rest cooldown.','action','extra_shift','assembly/ballot',req=['labour_bench'])
fat(0,'rolling_gauges','The Rolling Gauges',
    'Dispatchers report that the delay lies in maintenance and incompatible paperwork, not an absence of grand plans. A modest inspection of loading procedures can improve the use of the routes already owned. No new track is conjured by the report.',
    'Unlock a temporary loading-efficiency allocation that reserves a civilian factory.','action','loading_gauges','rail/tools',req=['route_contract'])
fat(0,'spare_batch','A Batch That Can Be Spared',
    'An infantry consignment will be written as a quantity, not a percentage of whatever happens to be in store. The quartermaster may refuse dispatch if the domestic reserve has fallen. An accepted request is permission to deliver, never permission to invent equipment.',
    'Unlock fixed infantry-equipment warrants backed by actual stock.','capability','infantry_warrant','assembly/logistics',req=['partner_register'])
fat(0,'testing_bench','Before the Crate Is Sealed',
    'Support equipment ties several workshops to a single shipment. Separate its warrant from the infantry order and record the inspection before it leaves. The recipient can ask for this practical assistance without accepting a broader military commitment.',
    'Unlock a separate support-equipment warrant with its own stock test.','capability','support_warrant','tools/science',req=['spare_batch'])
fat(0,'delivery_ledger','Two Open Commitments',
    'The clerk can reconcile a second open obligation if each has its own due date and recipient. Anything beyond that should wait. This is a staffing limit, not a claim that two pieces of paper provide two factories.',
    'Raise the maximum simultaneous pending or accepted warrants from one to two.','capability','second_warrant','document/communications',req=['consent_clause'])
fat(0,'no_blank_cheques','No Blank Cheques',
    'A ministry must be able to say that an order has become impossible. Publish a cancellation procedure before using it. Withdrawal still closes the warrant and its consent; a clerk cannot quietly reuse the same signature on another delivery.',
    'Allow costless administrative withdrawal of an unfulfilled warrant.','capability','clean_withdrawal','scales/security',req=['delivery_ledger'])
fat(0,'domestic_dispatch','Dispatch to Our Own Depots',
    'When no foreign request fits, the loading gang can still move a real consignment to domestic training depots. That decision consumes replacements now in exchange for a limited training programme. It is useful in neutrality and under external supervision alike.',
    'Unlock a domestic training allocation that consumes infantry stock instead of donating it.','action','domestic_training','training/logistics',req=['spare_batch'])
fat(0,'signed_ceiling','The Signed Ceiling',
    'The completed schedule reaches the minister with an uncomfortable blank at the bottom: what happens when every request is described as essential? Choose a published ceiling or an emergency exception that must be reviewed in public.',
    'Choose a restraint rule or a time-limited emergency authorisation.','scene',3,'command/scales',req=['delivery_ledger','testing_bench'],major=True)

fat(1,'wartime_return','The Return from the Works',
    'Whether the expected war came or was avoided, the works report the orders actually received. Ministers cannot balance the account with a victory they did not win. The next allocation must fit the present country, its obligations and the people doing the work.',
    'Assess an actual war, peaceful or subject context and choose a production burden.','scene',5,'industry/document',req=['signed_ceiling'])
fat(1,'essential_quota','An Essential Civilian Quota',
    'Keep a protected list for pumps, tools and replacement parts even when other ministries press for output. The list binds the allocation office itself. It helps ordinary repairs but takes an enduring share of industrial effort.',
    'Replace the initial priority with protected repair capacity and lower military output.','policy','essential_quota','rebuild/civil',req=['wartime_return'],exclusive='surge_quota',major=True)
fat(1,'surge_quota','The Limited Surge Schedule',
    'The emergency schedule will have an end and a visible cost. Plants receive priority for military deliveries, while households bear the delayed civilian work. Choose that burden openly rather than describing it as free efficiency.',
    'Alternative industrial surge policy with consumer and political burdens.','policy','surge_quota','assembly/command',req=['wartime_return'],exclusive='essential_quota',major=True)
fat(1,'neutrality_file','Keep a Neutrality File',
    'A refusal to enter a new commitment should leave a paper trail, not a silent desk. Publish which domestic contracts are protected when a foreign request is declined. The same procedure remains useful if another power controls external relations.',
    'Unlock domestic conversion of a refused or withdrawn offer, with real domestic stock expenditure.','capability','refused_domestic','peace/document',req=['no_blank_cheques'])
fat(1,'refugee_freight','A Freight Slot for Relief',
    'Relief planners ask for trucks and loading time rather than an invented border settlement. Their allocation must compete with military haulage. A paid transport interval can reduce local supply losses without claiming that every displaced family has been resettled.',
    'Unlock a relief freight allocation consuming motor stock and civilian capacity.','action','relief_freight','refugees/rail',req=['route_contract'])
fat(1,'host_capacity','Room Behind the Platform',
    'The arrivals hall needs clerks, medical space and a quiet waiting room. A temporary hosting allocation supports the people already present. It promises neither new population nor a permanent territorial reward.',
    'Unlock a temporary civil reception allocation with consumer-goods cost.','action','civil_reception','medical/shelter',req=['refugee_freight'])
fat(1,'requisition_window','The First Refused Requisition',
    'The receiver has returned the papers unsigned. Some in the ministry call this an insult; the dispatch clerk calls it an answer. Decide whether to publish the refusal and reserve the batch domestically, or reopen a narrower discussion later.',
    'A refusal scene chooses domestic finality or a costed fresh request procedure.','scene',4,'diplomacy/gate',req=['neutrality_file'])
fat(1,'arbitration_desk','A Smaller Request',
    'The original quantity may have been wrong for both parties. Permit a smaller infantry consignment when the domestic reserve rule is in force. A new request still needs new consent and cannot revive the expired signature.',
    'Unlock the smaller stock-backed infantry warrant as an alternative quantity.','capability','small_warrant','scales/logistics',req=['requisition_window'])
fat(1,'three_signatures','The Third Signature',
    'Three simultaneous obligations are now possible, provided each names a responsible office. This is the outer limit of the staff available. A fourth request must wait even if it would be politically convenient to accept it.',
    'Raise the open-warrant ceiling to three; the ceiling never grows further.','capability','third_warrant','document/command',req=['delivery_ledger','arbitration_desk'])
fat(1,'exhausted_shifts','Listen to the Exhausted Shift',
    'The plant can finish the current batch by borrowing against next month\'s health. Workers ask for a maintenance pause instead. Authorise the pause and accept a present output loss in return for safer training and equipment care.',
    'Unlock a rest-and-inspection alternative that cannot overlap an extra shift.','action','rest_interval','medical/tools',req=['shopfloor_ballot'])
fat(1,'family_accounts','The Invoices at Home',
    'The settlement is signed elsewhere, but household invoices arrive here. A peaceful outcome still leaves deferred maintenance, and occupation adds another authority to the desk. Choose whose unpaid work the local review will hear first.',
    'Settlement or peaceful domestic assessment chooses repair priorities without altering war outcomes.','scene',6,'civil/economy',req=[('essential_quota','surge_quota')])
fat(1,'relief_quota','Relief without a New Treaty',
    'The existing reconstruction authorities own their settlement and relief accounts. The national office can fund its own reception work alongside them. Read the response already chosen; do not claim the same reconstruction award a second time.',
    'Unlock an enhanced local reception allocation only after the owning postwar response, or a peaceful substitute.','capability','pwi_liaison','refugees/document',req=['family_accounts'])
fat(1,'inventory_recovery','Recover the Maintenance Margin',
    'Support stores can keep equipment in service instead of leaving another shipment on the quay. A domestic maintenance allocation consumes those stores explicitly. It is not a returning foreign gift and does not replenish the warehouse by decree.',
    'Unlock support-stock expenditure for a bounded maintenance benefit.','action','support_maintenance','tools/rebuild',req=['testing_bench'])
fat(1,'civilian_consignment','The Civilian Consignment',
    'A consignment reserved at home should have a destination and an expiry just like a foreign warrant. Give training depots and repair teams a published choice. The allocation cannot use the same stock twice.',
    'Allow domestic support allocation as an alternative to infantry training.','capability','domestic_support','civil/logistics',req=['inventory_recovery'])
fat(1,'audited_settlement','An Audited Settlement Account',
    'The public hearing can inspect what the national office actually promised. It cannot rewrite a treaty or award reparations from an absent treasury. Decide whether to close disputed invoices or keep a costed inspection staff at work.',
    'Choose a closed local settlement file or continuing independent scrutiny.','scene',7,'scales/peace',req=['family_accounts','invoice_rules'])
fat(1,'occupation_liaison','A Desk under Supervision',
    'External supervision limits what a national office can promise abroad. A liaison desk can still protect local repair schedules and record conflicting instructions. Its practical value does not depend on winning permission for an independent foreign policy.',
    'Unlock a subject-compatible civil liaison; independent countries use the same desk for domestic coordination.','action','supervised_liaison','gate/civil',req=['audited_settlement'])
fat(1,'unbroken_production','Keep the Existing Lines Running',
    'The works ask for a reliable maintenance cycle rather than another factory built on paper. A bounded continuity allocation improves current efficiency retention. It consumes administrative attention and leaves the physical production budget unchanged.',
    'Unlock a production-retention allocation with staff and fiscal opportunity costs.','action','line_continuity','assembly/tools',req=['exhausted_shifts'])
fat(1,'local_obligation_register','The Obligations that Remain',
    'The current register must make sense after victory, defeat, a refused request or an avoided war. Close the external account that no longer fits and keep the domestic permissions already earned. The next government should inherit a limit, not an impossible promise.',
    'Unlock a once-only reconciliation of current warrants and a domestic institutional review.','action','local_reconciliation','document/peace',req=['audited_settlement','three_signatures'],major=True)

fat(2,'renewal_hearing','Renew the Mandate in Public',
    'The later review is not a replay of the old emergency. Delegates ask which obligations still serve a purpose and which survive only because nobody owns the cancellation form. Open a new hearing with the actual register on the table.',
    '2006 renewal scene selects scrutiny or a bounded executive mandate.','scene',8,'ballot/scales',req=['local_obligation_register'])
fat(2,'open_tenders','Publish the Tender',
    'Publishing a tender invites objections before the order is placed. It slows exceptional procurement but protects ordinary access to the works. Accept that delay as an enduring rule instead of treating openness as a free output bonus.',
    'Standing open-procurement policy with industrial and political tradeoffs.','policy','open_tenders','document/ballot',req=['renewal_hearing'],exclusive='directed_orders',major=True)
fat(2,'directed_orders','A Directed Order Book',
    'A single coordinating office can move priority orders quickly. Its instructions must also name the civilian work being displaced. The policy concentrates authority and output while carrying a continuing public burden.',
    'Alternative directed-procurement policy with a consumer and legitimacy cost.','policy','directed_orders','command/industry',req=['renewal_hearing'],exclusive='open_tenders',major=True)
fat(2,'contract_appeal','An Appeal before Dispatch',
    'A recipient or workshop should not have to wait for a failed delivery before objecting. Permit an appeal while stock is still at home. The appeal cancels consent and demands a new request; it does not undo a completed shipment.',
    'Allow withdrawal after acceptance without a penalty; completed deliveries remain final.','capability','accepted_appeal','scales/gate',req=['no_blank_cheques'])
fat(2,'supplier_liability','The Supplier Must Answer',
    'The failed component reaches the hearing before the supplier\'s explanation does. An inspection can cost more than the replacement itself, but ignoring the failure shifts the burden to the next crew. Choose how liability will be recorded.',
    'Procurement failure scene chooses a paid independent inspection or a disclosed limited repair.','scene',9,'tools/scales',req=[('open_tenders','directed_orders')])
fat(2,'skilled_shift','Retain the Skilled Shift',
    'Training a replacement crew does not recreate the workers who left. Offer a limited retention interval tied to maintenance and instruction. The payroll and civilian cost remain visible while the production lines continue using their existing equipment.',
    'Unlock a skill-retention allocation; it competes with the existing production interval.','action','skill_retention','training/assembly',req=['unbroken_production'])
fat(2,'domestic_veto','The Domestic Veto',
    'The national office must be able to stop every undelivered external commitment when domestic conditions change. Publish a single suspension order. It clears permissions and staff limits; it does not claw equipment back from a receiver.',
    'Unlock immediate cancellation of all unfulfilled warrants and return to domestic work.','action','suspend_warrants','security/document',req=['contract_appeal'])
fat(2,'joint_inspection','Invite a Receiving Inspector',
    'The receiver may prefer inspection to a larger shipment. Permit a narrow, optional inspection at the dispatch desk. Acceptance grants a longer practical training benefit only if both sides agree to that specific form of cooperation.',
    'Unlock recipient choice of inspected cooperation rather than automatic extra stock.','capability','joint_inspection','science/diplomacy',req=['supplier_liability'])
fat(2,'independent_audit','The Auditor Keeps a Separate Key',
    'A public auditor needs access to the national register without becoming another requisition office. Give the staff a separate, limited budget. Its continuing scrutiny lowers political discretion and carries a real administrative burden.',
    'Unlock a standing audit policy with a distinct institutional cost.','action','independent_audit','security/scales',req=['invoice_rules','renewal_hearing'])
fat(2,'civilian_retainer','Retain Civilian Repair Capacity',
    'Keep a small permanent repair retainer for ordinary clients after the exceptional programmes end. It supports construction and maintenance while reserving resources that cannot also be promised to a military surge.',
    'Terminal civilian retainer replaces earlier production priorities.','policy','civilian_retainer','civil/tools',req=['skilled_shift'],exclusive='industrial_retainer',major=True)
fat(2,'industrial_retainer','Retain the Industrial Reserve',
    'The final retainer will keep a military replacement margin available, not create a new factory. Civilian customers carry the standing reserve cost. Publish that burden so a later government can see what has been chosen.',
    'Alternative terminal industrial retainer replaces earlier production priorities.','policy','industrial_retainer','assembly/security',req=['skilled_shift'],exclusive='civilian_retainer',major=True)
fat(2,'alternate_deliveries','An Alternative after Interruption',
    'An annexed receiver or a broken route ends the foreign obligation. The dispatch office may redirect remaining stock into a domestic programme after cancellation, with a fresh stock check. Nothing is paid merely because a partner disappeared.',
    'Allow a fresh domestic transport allocation after a cancelled external warrant.','capability','interrupted_transport','logistics/gate',req=['domestic_veto'])
fat(2,'outstanding_accounts','The Outstanding Accounts',
    'The final assessment counts deliveries actually made, promises refused and commitments withdrawn. A peaceful and cautious record can be defensible; a busy register is not automatically a good one. Decide what the public account will preserve.',
    '2013 assessment selects accountable cooperation or a domestic-first conclusion.','scene',10,'document/medal',req=['renewal_hearing','supplier_liability'])
fat(2,'winding_warrants','Close the Expired Warrants',
    'An expired signature should not remain an invisible claim on staff. Authorise a complete reconciliation of permissions with the present partner list. The process closes dead offers without awarding a delivery that never happened.',
    'Unlock a registry sweep of expired or ineligible partner warrants.','action','sweep_warrants','document/peace',req=['outstanding_accounts'])
fat(2,'standing_transport','A Standing Dispatch Standard',
    'A common loading standard can outlast a particular foreign agreement. Retain the practical procedures as a domestic option, with the same stock and civilian costs when they are used. Cooperation remains a choice rather than a permanent permission slip.',
    'Extend the paid domestic transport option to peaceful routine use.','capability','routine_transport','rail/document',req=['alternate_deliveries'])
fat(2,'no_automatic_successor','No Automatic Successor',
    'A change of authority ends the old mandate unless the new authorities sign again. Record that principle in the national procedure. Annexation and reintegration remain owned elsewhere; this office only cancels its own unfulfilled permissions.',
    'Unlock a succession review that closes outstanding warrants before a new domestic mandate.','action','succession_review','gate/command',req=['winding_warrants'])
fat(2,'public_commitment_limit','A Public Commitment Limit',
    'The final limit is not a fourth signature. It is a rule that the existing three must fit both the treasury and the staffing ledger. Fund a stricter review if the government wants its remaining external permissions to stay credible.',
    'Unlock a funded compliance interval that improves capacity while limiting current output.','action','commitment_review','economy/scales',req=['independent_audit'])
fat(2,'bounded_cooperation','Cooperation within the Means',
    'The programme ends with a practical distinction: foreign consent permits a delivery, while domestic authority pays for it. Keep the permissions earned, the right to refuse and the cost of the standing policy. That is a workable conclusion even if no coalition formed.',
    'Unlock a final assessment action with distinct subject, domestic and delivered-cooperation outcomes.','action','final_mandate','peace/diplomacy',req=['outstanding_accounts',('civilian_retainer','industrial_retainer'),'public_commitment_limit'],major=True)

# South Belka: a finite docket of specific civil cases, not a service meter.
sbk(0,'civil_register','A Register under Present Authority',
    'The first clerk asks which authority is entitled to sign today, not which future the newspapers predict. Open a civil register for the territory actually held. The record must remain useful under a supervising power and must not promise new sovereignty.',
    'Contemporary first-entry scene chooses a registry priority without replaying historical transfers.','scene',101,'document/gate')
sbk(0,'urgent_repairs','The First Work Order',
    'The workshop brings a list of stopped pumps and missing parts. Residents want to know who will choose the first repair. Begin with a practical priority and an honest account of the staff and stores available.',
    'Choose urgent utility maintenance or a broader case hearing.','scene',102,'tools/rebuild',req=['civil_register'])
sbk(0,'resident_casework','Hear the Resident First',
    'Give residents a predictable hearing before issuing exceptional work orders. Casework becomes slower but more credible. The administration accepts the staffing cost of listening rather than calling participation a free source of capacity.',
    'Resident-first standing procedure: stability and slower discretionary production.','policy','resident_casework','civil/ballot',req=['civil_register'],exclusive='emergency_orders',major=True)
sbk(0,'emergency_orders','An Emergency Order Desk',
    'A single desk can issue urgent instructions before a full hearing. Its authority needs a published burden and a later route of appeal. Faster repairs under this procedure do not imply that residents have consented to every order.',
    'Alternative emergency procedure: repair speed with public and consumer burdens.','policy','emergency_orders','command/tools',req=['civil_register'],exclusive='resident_casework',major=True)
sbk(0,'property_claims','The Property File',
    'Two families bring different copies of the same record. The clerk cannot settle title by changing a map or handing out a core. Open a bounded civil case that can choose protected possession or a documented temporary arrangement.',
    'Unlock the one-time property case with two materially different settlements.','capability','case_property','document/scales',req=['urgent_repairs'])
sbk(0,'service_docket','The Utility Work Docket',
    'The maintenance list should name a repair, its stores and the public authority responsible. A utility case can fund a careful repair or ration the present service while parts are conserved. Neither choice creates a factory or a population grant.',
    'Unlock the utility case, including real support-stock expenditure.','capability','case_utilities','rebuild/tools',req=['urgent_repairs'])
sbk(0,'stores_reconciliation','Reconcile the Stores',
    'The transfer inventory and the warehouse inventory need not agree. Audit the stock actually held before it is assigned to a new programme. The inherited transfer remains final; the case decides how current stores are used.',
    'Unlock a stock-accountability case; no duplication of inherited transfers.','capability','case_stores','logistics/document',req=['civil_register'])
sbk(0,'civil_receipts','Receipts for Civil Work',
    'A work order without a receipt leaves the next office unable to distinguish a repair from a promise. Establish a small verification round. The staff time is a cost; a verified record permits later maintenance work on better terms.',
    'Unlock paid receipt verification that changes the docket resolution cost.','action','verify_receipts','document/science',req=['service_docket'])
sbk(0,'bounded_advisers','An Adviser with a Written Remit',
    'A visiting specialist offers help and asks who may open the workshop. The administration can seek a narrow agreement from the actual eligible counterpart or proceed with domestic expertise. A signature here neither creates nor ends a subject relationship.',
    'Choose to seek limited technical advice or keep the work entirely domestic.','scene',103,'diplomacy/gate',req=['stores_reconciliation'])
sbk(0,'records_recovery','The Displaced Records',
    'The recovered boxes are incomplete. Clerks propose either reconstructing household records with witnesses or placing the uncertain files under temporary protection. Both are civil procedures for people already present, not a new population settlement.',
    'Choose witness-based record recovery or protected interim records.','scene',104,'refugees/document',req=['property_claims'])
sbk(0,'hearing_calendar','A Day for Security Questions',
    'Residents cannot be expected to bring a security complaint to an unmarked office. Publish a hearing day and the limits of its inquiry. The case can review local procedure; it has no power to undo a war settlement.',
    'Unlock the security-remit civil case.','capability','case_security','security/ballot',req=['records_recovery'])
sbk(0,'local_witnesses','Local Witnesses',
    'A witness who can explain a ledger may save weeks of formal correspondence. Admit that evidence under a published rule. It makes a particular property or record settlement possible; it is not a generic measure of national loyalty.',
    'Unlock witness-led property and archive resolutions with a different staffing cost.','capability','local_witnesses','civil/document',req=['records_recovery'])
sbk(0,'two_signatures','Two Cases, Two Responsible Officers',
    'The civil office can carry a second case if each file names an officer. Beyond two, the hearing calendar becomes fiction. Keep the limit visible and require an existing case to close before opening a third.',
    'Raise simultaneous civil cases from one to two; no unlimited case slots.','capability','second_case','document/command',req=['civil_receipts','hearing_calendar'])
sbk(0,'provisional_charter','A Provisional Civil Procedure',
    'Write down what the office may do with the powers it presently has. The procedure covers work orders and civil hearings, not an unearned declaration of independence. Its continuing benefit rests on a continuing administrative burden.',
    'Unlock a costed standing civil charter tailored to subject or independent status.','action','civil_charter','scales/civil',req=[('resident_casework','emergency_orders'),'two_signatures'],major=True)

sbk(1,'review_authority','Review the Authority to Order',
    'The hearing opens with a practical question: which instructions reached the local office, and which could it lawfully carry out? Review the present remit after the existing settlement or its peaceful alternative. No new settlement is awarded here.',
    'Security and administrative review chooses published limits or rapid instruction handling.','scene',105,'security/scales',req=['provisional_charter'])
sbk(1,'published_orders','Publish the Order',
    'A published instruction can be questioned before it becomes a fait accompli. Keep that protection as the normal rule, accepting the delay to exceptional work. The office cannot promise that publicity alone removes external supervision.',
    'Replace the initial procedure with public-order scrutiny.','policy','published_orders','document/ballot',req=['review_authority'],exclusive='delegated_command',major=True)
sbk(1,'delegated_command','A Defined Delegation',
    'The order desk receives a precise delegation for local work. Its advantage is speed, and its cost is concentrated discretion. The delegation stays within the present government and cannot alter who owns a state.',
    'Alternative delegated local-command policy with continuing legitimacy cost.','policy','delegated_command','command/gate',req=['review_authority'],exclusive='published_orders',major=True)
sbk(1,'core_and_resident','Residents beyond the Register',
    'Some residents fall outside the inherited constitutional record. Their utility bill still needs an answer. A case may extend civil access on a provisional basis without adding cores, manpower or a claim to any new territory.',
    'Unlock a resident-access case useful on non-core treaty footprints.','capability','case_access','civil/gate',req=['review_authority'])
sbk(1,'appeal_routes','The Route of Appeal',
    'A closed file should be challengeable once if new evidence appears. Make the cost and limit explicit. The second hearing cannot pay the first award again, and it must replace the old arrangement before establishing another.',
    'Allow each closed case one costed reopening, replacing rather than stacking its prior benefit.','capability','case_appeal','scales/document',req=['core_and_resident'])
sbk(1,'limited_remit','The Limit of a Guarantee',
    'An external authority may offer advice, supervision or nothing at all. Decide whether to request a narrow technical remit or rely on a domestic hearing. The answer cannot postpone the existing reintegration owner or manufacture a sovereignty guarantee.',
    'Choose external technical consent or an explicitly domestic continuation.','scene',106,'diplomacy/security',req=['bounded_advisers'])
sbk(1,'service_inspector','The Workshop Inspector',
    'A permitted technical visitor may inspect the work, not command the administration. Keep the distinction in the access papers. If consent is refused or expires, a paid domestic inspection remains available.',
    'Unlock the limited adviser request and a useful domestic inspection after refusal.','capability','adviser_request','science/gate',req=['limited_remit'])
sbk(1,'displaced_archives','An Archive Case',
    'The boxes recovered in the first months now need a lasting arrangement. A witness-led reconstruction and a protected interim archive have different costs and permissions. Settle the case with the records actually available.',
    'Unlock the archive case, including the earned witness alternative.','capability','case_archive','document/refugees',req=['records_recovery'])
sbk(1,'security_review','Review the Local Security Remit',
    'A security hearing is useful only if its conclusion binds the local service. Publish a narrower procedure or fund a supervised inspection. It cannot disarm another country or remove an inherited national spirit that was never applied.',
    'Unlock the enhanced security-case resolution; no phantom demobilisation reward.','capability','security_review','security/scales',req=['hearing_calendar'])
sbk(1,'measured_training','Instruction within the Existing Service',
    'The administration can improve instruction for personnel already assigned to it. Fund a bounded course and accept its political cost. This is organisation and maintenance, with no instant recruitable population or new formation grant.',
    'Unlock a paid service-instruction interval using existing support equipment.','action','civil_instruction','training/security',req=['security_review'])
sbk(1,'maintenance_budget','An Account for Maintenance',
    'A repair completed once still needs parts later. Reserve a small standing maintenance account, stated separately from the cost of a particular hearing. The commitment supports current service and remains removable through the public procedure.',
    'Unlock a standing maintenance policy with a real annual fiscal commitment when enabled.','action','maintenance_account','economy/tools',req=['service_docket'])
sbk(1,'public_receipts','Read the Unresolved Claims',
    'The public file includes claims that could not be proved. Decide whether to protect an interim arrangement or pay for a further investigation. Neither option turns a disputed document into a canonical border.',
    'Unresolved-claims scene chooses protected interim access or paid inquiry.','scene',108,'scales/document',req=['displaced_archives'])
sbk(1,'standing_work_orders','A Work Order after the Hearing',
    'Give completed utility and access cases a longer maintenance interval when the records justify it. The staff must still pay the initial resolution cost. An unresolved or interrupted case receives no completed-work benefit.',
    'Extend future utility and access case settlements only after actual resolution.','capability','standing_orders','tools/document',req=['public_receipts'])
sbk(1,'civil_continuity','Continuity without a New Settlement',
    'The civil record should survive a pause in work without pretending that the work was completed. Publish an interruption procedure and keep the costs already incurred in the ledger. Annexation and reintegration remain decisions of their owning authorities.',
    'Unlock an interruption review that closes open cases without a completion award.','action','interruption_review','peace/document',req=['public_receipts','appeal_routes'],major=True)

sbk(2,'renewal_of_authority','Renew the Civil Authority',
    'The later administration inherits files rather than a blank page. Review who may sign the next budget and what the public may expect from it. A country released later receives this as a contemporary review, never as aid backdated to an earlier crisis.',
    '2006-or-later budget-authority scene chooses public review or a professional case bench.','scene',107,'ballot/economy',req=['civil_continuity'])
sbk(2,'elected_hearing','A Public Hearing Bench',
    'Keep lay representatives at the hearing table. The slower calendar buys a more open civil process, with a continuing cost in exceptional production. The policy does not replace the country\'s existing leader or ruling party.',
    'Terminal participatory case procedure preserves existing political identities.','policy','elected_hearing','ballot/civil',req=['renewal_of_authority'],exclusive='professional_bench',major=True)
sbk(2,'professional_bench','A Professional Case Bench',
    'A permanent professional bench can clear technical files more quickly. It is also more distant from the residents whose cases it decides. Keep that tradeoff visible in the standing policy and preserve a separate right of appeal.',
    'Alternative terminal technical procedure with political and consumer burdens.','policy','professional_bench','science/scales',req=['renewal_of_authority'],exclusive='elected_hearing',major=True)
sbk(2,'obsolete_claims','Close an Obsolete Claim',
    'Some requests no longer fit the territory or authority held. A documented closure is better than an impossible promise. Permit a file to close without a settlement bonus, while preserving its record and the possibility of one lawful appeal.',
    'Unlock costless closure of a currently open case without granting its outcome.','capability','close_obsolete','document/peace',req=['appeal_routes'])
sbk(2,'external_orders','Two Conflicting Instructions',
    'The office receives two incompatible requests. Under supervision it must identify the actual competent authority; independently it must still choose a lawful local remit. A new signature cannot cancel the existing annexation contract.',
    'Choose a narrow local remit or disclosed external coordination with useful subject and refusal outcomes.','scene',109,'command/scales',req=['renewal_of_authority','limited_remit'])
sbk(2,'accountable_services','Account for the Standing Service',
    'The annual service budget needs a public account separate from any single case. A standing policy can improve reliability only while its political and financial burdens remain accepted. It is a commitment, not a treasury grant.',
    'Unlock a removable civil reliability policy with an exact recorded fiscal commitment.','action','service_account','economy/civil',req=['maintenance_budget'])
sbk(2,'relief_appeal','An Appeal beside Reconstruction',
    'The existing reconstruction response remains in its owning ledger. Use its recorded local choice as evidence for a civil appeal, or proceed on a peaceful domestic basis if no such contract exists. Do not pay the original relief award again.',
    'Unlock a local relief review contingent on the owning response or a peaceful substitute.','action','relief_review','refugees/scales',req=['public_receipts'])
sbk(2,'resident_consent','The Resident May Decline',
    'A civil file need not end in the arrangement preferred by the office. Give residents a protected interim option at a smaller immediate cost and with a smaller benefit. It is a useful conclusion, not a failed test of loyalty.',
    'Unlock the low-stock interim settlement for utility and access cases.','capability','resident_consent','civil/gate',req=['obsolete_claims'])
sbk(2,'narrow_security_remit','A Narrow Security Remit',
    'Limit the local security service to the procedure actually authorised. Inspection may improve organisation, while a narrower remit protects public confidence. Neither outcome creates forces or changes an external military guarantee.',
    'Unlock a narrowly bounded oversight policy independent of foreign adviser consent.','action','security_remit','security/document',req=['external_orders','security_review'])
sbk(2,'municipal_workshops','The Municipal Maintenance Round',
    'The workshops need predictable parts and a chance to teach the next crew. Fund a temporary maintenance round using current support stock. It remains worthwhile whether the country is independent, supervised or waiting on an unanswered adviser request.',
    'Unlock a domestic stock-backed workshop interval available under every alignment.','action','workshop_round','tools/training',req=['standing_work_orders'])
sbk(2,'common_archive','Keep a Common Civil Archive',
    'A common index lets the next clerk find the prior decision without reopening every dispute. The archive reduces the cost of future hearings only after it has been funded and checked. It cannot turn unproved claims into titles.',
    'Unlock a one-time archive verification that reduces future case fees.','action','archive_index','document/communications',req=['displaced_archives','renewal_of_authority'])
sbk(2,'public_interest_test','State the Public Interest',
    'Before maintaining an exceptional arrangement, publish the public interest it serves. This review can end the administration\'s standing policies and their exact recorded commitments. It never removes another owner\'s institutions or settlement burdens.',
    'Unlock voluntary removal of this campaign\'s standing policies and exact fiscal commitments.','action','public_interest','scales/economy',req=['accountable_services'])
sbk(2,'final_docket','The Final Docket',
    'The later assessment keeps resolved cases, refusals and unfinished claims in separate columns. A small administration can reach a useful conclusion without controlling every external decision. Decide what should remain a standing civil promise.',
    '2013-or-later assessment selects accountable continuity or a narrower interim administration.','scene',110,'document/medal',req=['external_orders','common_archive'])
sbk(2,'standing_civil_arrangement','A Standing Civil Arrangement',
    'The programme concludes with the authority and territory actually held. Preserve earned civil access and the right to review it; disclose the cost of any standing service. Reintegration, if the existing owner orders it, closes this programme rather than being blocked by it.',
    'Unlock distinct independent, supervised and domestic-after-refusal conclusions.','action','final_arrangement','peace/scales',req=['final_docket',('elected_hearing','professional_bench'),'public_interest_test'],major=True)

assert len([f for f in FOCUSES if f.tag=='FAT'])==54
assert len([f for f in FOCUSES if f.tag=='SBK'])==42
assert len({f.id for f in FOCUSES})==96

# Each modifier is a verified engine-native modifier, deliberately bounded.
# Members of one family replace one another instead of stacking across acts.
POLICIES={
 'civilian_priority':('FAT','priority',{'production_speed_industrial_complex_factor':.04,'stability_factor':.02,'industrial_capacity_factory':-.03}),
 'plant_priority':('FAT','priority',{'industrial_capacity_factory':.04,'consumer_goods_factor':.01,'stability_factor':-.02}),
 'essential_quota':('FAT','priority',{'production_speed_buildings_factor':.04,'industrial_capacity_factory':-.04,'consumer_goods_factor':.01}),
 'surge_quota':('FAT','priority',{'industrial_capacity_factory':.06,'consumer_goods_factor':.02,'political_power_gain':-.1}),
 'open_tenders':('FAT','procurement',{'production_factory_efficiency_gain_factor':.04,'political_power_gain':.05,'production_speed_buildings_factor':-.02}),
 'directed_orders':('FAT','procurement',{'industrial_capacity_factory':.04,'consumer_goods_factor':.01,'stability_factor':-.01}),
 'civilian_retainer':('FAT','priority',{'production_speed_buildings_factor':.05,'equipment_capture':.01,'industrial_capacity_factory':-.03,'consumer_goods_factor':.01}),
 'industrial_retainer':('FAT','priority',{'production_factory_max_efficiency_factor':.04,'industrial_capacity_factory':.03,'consumer_goods_factor':.02}),
 'resident_casework':('SBK','procedure',{'stability_factor':.03,'industrial_capacity_factory':-.02,'political_power_gain':-.05}),
 'emergency_orders':('SBK','procedure',{'production_speed_buildings_factor':.05,'consumer_goods_factor':.01,'stability_factor':-.02}),
 'published_orders':('SBK','procedure',{'stability_factor':.04,'political_power_gain':.05,'production_speed_buildings_factor':-.03}),
 'delegated_command':('SBK','procedure',{'production_speed_buildings_factor':.06,'consumer_goods_factor':.02,'political_power_gain':-.1}),
 'elected_hearing':('SBK','procedure',{'stability_factor':.05,'industrial_capacity_factory':-.03,'political_power_gain':-.05}),
 'professional_bench':('SBK','procedure',{'production_speed_buildings_factor':.06,'consumer_goods_factor':.01,'stability_factor':-.02}),
}

def resolved_positions():
    """Every prerequisite is above its child; acts get separate vertical bands.

    Columns express the authored subjects, while deterministic DAG depth prevents
    same-row prerequisite lines from crossing an icon. No relative-position
    engine inference or overlap-prone rectangular count matrix is required.
    """
    result={}
    for tag in COUNTRIES:
        used=set();base=1
        for phase in range(3):
            rows=[r for r in FOCUSES if r.tag==tag and r.phase==phase]
            for r in rows:
                y=max([base]+[result[tag+'_nat_'+s][1]+1 for group in r.requirements for s in group])
                while (r.x,y)in used:y+=1
                used.add((r.x,y));result[r.id]=(r.x,y)
            base=max(result[r.id][1]for r in rows)+3
    return result

POSITIONS=resolved_positions()
