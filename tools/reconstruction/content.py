"""National recovery choices, 2006–2013: approved provisional gameplay.

No new official history, borders, leaders or military equipment are asserted.
Each six-definition branch contains two exclusive policies, two paid services,
a service review and an enduring conclusion. Original policy IDs remain stable.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    tag: str
    key: str
    entry: str
    titles: tuple
    descriptions: tuple
    subjects: tuple
    policies: tuple
    services: tuple


# Policy tuples: readable name, benefit, enduring countervailing cost.
# Service tuples: decision title, objective, responsible institution, modifiers.
BRANCHES = [
    Branch('NPT', 'mandate', 'NPT_exp_civil_resilience',
      ('Reopen the Island Mandate', 'A Guarded Access Charter', 'A Parliamentary Cooperation Mandate',
       'Standing Instructions for Foreign Requests', 'Publish the Mandate Review', 'The Right to Decide Again'),
      ('The emergency passed without settling who may promise the islands\' facilities to another government. An inventory of actual obligations gives the legislature a basis for renewing or limiting that authority.',
       'Future access requests require inspection, warning and a national right of refusal. The charter protects those powers without revoking existing defence undertakings, while accepting the continuing cost of an independent watch.',
       'Cooperation can be authorized without giving a foreign headquarters permanent discretion over local services. The legislature will publish the limits and accept the political burden of reviewing them.',
       'Each request will identify the facilities, receiving office and withdrawal condition involved. Those instructions remain useful when a partner refuses the terms or no longer qualifies for assistance.',
       'An actual service period must be examined before its procedures become permanent. The review compares promises with the work completed; it does not turn a paper alliance into a delivered service.',
       'The mandate now includes a renewal process rather than an assumption of permanent consent. Neutral and cooperative governments retain their different obligations and a useful national conclusion.'),
      (('ballot', 'document'), ('security', 'peace'), ('assembly', 'diplomacy'), ('document', 'gate'), ('scales', 'ballot'), ('assembly', 'peace')),
      (('Guarded access charter', {'stability_factor': 0.025}, {'political_power_gain': -0.05}),
       ('Reviewed cooperation mandate', {'air_mission_efficiency': 0.025}, {'consumer_goods_factor': 0.005})),
      (('Exercise the Mandate Desk', 'Test how a foreign request is accepted, limited or refused without promising facilities twice.', 'The parliamentary liaison and civil-service duty desk', {'political_power_gain': 0.08}),
       ('Inspect the Withdrawal Instructions', 'Verify that local services can resume ordinary work when an external commitment ends.', 'The parliamentary inspection committee', {'stability_factor': 0.025}))),
    Branch('NPT', 'harbours', 'NPT_exp_civil_resilience',
      ('A Working Harbour Register', 'Protect Civilian Berthing', 'Reserve a Defence Receiving Window',
       'Separate the Maintenance Queues', 'Reconcile the Harbour Accounts', 'Harbours That Can Keep Their Promises'),
      ('Harbour officers will distinguish usable berths, repair work and unfulfilled reservations. An island economy cannot count a quay as available to every ministry at once.',
       'Civilian schedules will receive a protected receiving window. Commercial services gain predictability, while the defence establishment accepts longer notice for exceptional movements.',
       'A limited military receiving window keeps emergency movements credible. Maintaining that reservation imposes a cost on ordinary traffic and does not create additional dockyards.',
       'Commercial repairs and defence support require different returns but draw on some of the same skilled crews. Separate queues will show the capacity withheld from each service.',
       'A funded receiving or maintenance period will supply the evidence for review. Unpaid plans and interrupted services cannot qualify as completed work.',
       'The final harbour compact preserves the chosen allocation and a tested release procedure. Native ports, convoys, fuel and repair capacity still determine what can physically move.'),
      (('navy', 'document'), ('logistics', 'civil'), ('navy', 'security'), ('tools', 'scales'), ('economy', 'navy'), ('bridge', 'navy')),
      (('Protected civilian berthing', {'production_factory_efficiency_gain_factor': 0.025}, {'naval_coordination': -0.01}),
       ('Reserved defence receiving', {'naval_coordination': 0.025}, {'consumer_goods_factor': 0.005})),
      (('Fund a Harbour Maintenance Rota', 'Reserve inspection and support crews for existing berths; this service grants no ships or port levels.', 'The harbour authority', {'repair_speed_factor': 0.04}),
       ('Run a Receiving-Window Trial', 'Test the chosen allocation against ordinary deliveries and emergency requests.', 'The harbour authority and customs service', {'naval_coordination': 0.025}))),
    Branch('NPT', 'airspace', 'NPT_exp_civil_resilience',
      ('Bring the Watch Stations Together', 'A Civil Warning Network', 'A Joint Air-Service Protocol',
       'Keep the Receiving Airfields Accountable', 'Review an Actual Watch Period', 'An Island Air-Service Settlement'),
      ('Watch stations, airfield services and civil authorities possess different parts of the same report. A common duty book will make responsibility clear without asserting telemetry for individual wings.',
       'The network will put public warning and protected local communications first. Air operations retain useful reporting, but cannot appropriate every civil channel without review.',
       'Compatible reporting procedures can support coalition aircraft while preserving national control. Maintaining a joint protocol costs staff capacity even when a foreign service makes no request.',
       'Receiving an aircraft requires trained ground staff and a usable runway, not a diplomatic signature alone. The service will keep local capacity separate from external requests.',
       'The government will examine a completed, funded watch or receiving period. An absent partner does not strand this domestic review.',
       'The settlement retains the chosen warning or cooperation policy and a tested national receiving service. It neither forces alignment nor grants aircraft that were never manufactured.'),
      (('radar', 'communications'), ('civil', 'radar'), ('air', 'diplomacy'), ('runway', 'document'), ('scales', 'radar'), ('air', 'peace')),
      (('Civil warning priority', {'stability_factor': 0.02}, {'air_mission_efficiency': -0.01}),
       ('Reviewed joint air service', {'air_mission_efficiency': 0.025}, {'political_power_gain': -0.05})),
      (('Staff a National Watch Period', 'Maintain a common reporting duty and a civilian warning contact.', 'The national air-watch service', {'air_detection': 0.025}),
       ('Inspect Airfield Receiving Teams', 'Test the existing ground-service rota without purchasing or spawning aircraft.', 'The airfield services inspectorate', {'air_mission_efficiency': 0.03}))),
    Branch('REC', 'records', 'REC_exp_recovery_assessment',
      ('Preserve the District Record', 'A Public Council Register', 'A Controlled Requisition Register',
       'Hear the Outstanding Claims', 'Audit a Completed Claims Period', 'A Durable Rectan Administrative Record'),
      ('Reconstruction has left overlapping claims to housing, workshops and public stores. The republic needs to preserve the record before another administrative reorganization disperses it.',
       'District councils will publish allocations and hear challenges in public. The process strengthens confidence while consuming staff time that a central order could otherwise redirect.',
       'The administration will retain direct control of requisitions, but require written receipts and a named official. Control becomes more dependable at a continuing political cost.',
       'A claims service gives residents a route to correct the register. Its work stays within the inherited settlement and makes no new territorial demand.',
       'The review requires completed casework rather than the announcement of a new office. Interrupted or unpaid periods leave the outstanding claims visible.',
       'The resulting record preserves either public review or accountable central control. The existing hardline and reform branches retain their identities; no new government or border is imposed.'),
      (('document', 'rebuild'), ('assembly', 'scales'), ('command', 'document'), ('civil', 'document'), ('scales', 'security'), ('document', 'peace')),
      (('Public district register', {'stability_factor': 0.025}, {'political_power_gain': -0.05}),
       ('Accountable central requisitions', {'production_factory_efficiency_gain_factor': 0.03}, {'stability_factor': -0.015})),
      (('Fund a District Claims Rota', 'Process contested allocations through the selected public or central register.', 'The republican district administration', {'stability_factor': 0.025}),
       ('Inspect Requisition Receipts', 'Reconcile receiving signatures with the claims record and identify unresolved cases.', 'The district inspection service', {'production_factory_efficiency_gain_factor': 0.035}))),
    Branch('REC', 'works', 'REC_exp_recovery_assessment',
      ('Map the Remaining Service Gaps', 'Municipal Repair Compacts', 'A Central Works Schedule',
       'Keep Repair Crews in Service', 'Review the Works Actually Delivered', 'Reconstruction beyond the Emergency'),
      ('A completed reconstruction programme can leave ordinary services uneven. Municipal returns will identify the maintenance work still required inside Recta\'s existing states.',
       'Municipalities will retain a protected repair allocation and publish their own priorities. Local knowledge improves service at the price of a slower national redirection process.',
       'A central schedule will move technical crews between districts according to reported urgency. The administration accepts the political burden of explaining why a district must wait.',
       'Repair crews need recurring inspection, training and a receiving office after the opening contract ends. A standing rota supports native construction and repair without creating buildings by decree.',
       'The government must review a service period that was actually funded and completed. No preparation reward can be backdated from this later work.',
       'The chosen works policy becomes a normal service obligation instead of a succession of emergency promises. Later recovery remains useful without revising the established territorial settlement.'),
      (('rebuild', 'document'), ('civil', 'tools'), ('command', 'tools'), ('tools', 'logistics'), ('scales', 'rebuild'), ('rebuild', 'peace')),
      (('Municipal repair compacts', {'repair_speed_factor': 0.035}, {'political_power_gain': -0.05}),
       ('Central works schedule', {'production_speed_infrastructure_factor': 0.04}, {'consumer_goods_factor': 0.005})),
      (('Fund a Municipal Maintenance Period', 'Keep existing repair crews accountable to a receiving district office.', 'The republican works administration', {'repair_speed_factor': 0.045}),
       ('Inspect the Central Repair Queue', 'Test whether the chosen allocation can release crews after priority repairs.', 'The works inspection service', {'production_speed_infrastructure_factor': 0.045}))),
    Branch('REC', 'neighbours', 'REC_exp_recovery_assessment',
      ('A Ledger of External Obligations', 'Compatible Civil Standards', 'Protected National Control',
       'Prepare a Useful Refusal', 'Review the Liaison Service', 'Cooperation within the Settlement'),
      ('Contacts with Gebet and FATO have produced obligations that survive a single meeting. The republic will record which services it can provide and which require a separate national authorization.',
       'Compatible inspection and receiving standards make trade and assistance easier. They do not compel a partner to accept an offer or alter either country\'s diplomatic status.',
       'National control will take priority over routine external access. Domestic technical services remain useful, while the government accepts the extra burden of maintaining its own procedures.',
       'An external request may be declined because a partner is absent, at war, a subject or unwilling to cooperate. A domestic fallback will preserve the service without fabricating a bilateral agreement.',
       'A funded liaison or standards period gives the government evidence of what can be sustained. The review does not require a foreign government to accept a treaty.',
       'The resulting policy keeps useful relations with eligible neighbours and a viable national alternative. Existing faction consent and postwar settlement owners remain authoritative.'),
      (('document', 'diplomacy'), ('diplomacy', 'tools'), ('security', 'gate'), ('peace', 'document'), ('scales', 'diplomacy'), ('diplomacy', 'peace')),
      (('Compatible civil standards', {'research_speed_factor': 0.015}, {'consumer_goods_factor': 0.005}),
       ('Protected national procedures', {'army_org_factor': 0.025}, {'political_power_gain': -0.05})),
      (('Staff the Neighbour Liaison Desk', 'Maintain receiving contacts and a clear route for declining an ineligible request.', 'The republican external-services office', {'political_power_gain': 0.08}),
       ('Run a Domestic Standards Period', 'Retain the technical value of compatible procedures even without foreign participation.', 'The national standards service', {'research_speed_factor': 0.02}))),
    Branch('SAP', 'mandate', 'SAP_pwi_legacy',
      ('Return Commitments to the Chamber', 'A Parliamentary Service Mandate', 'A Protected Defence Appropriation',
       'Publish the Burden of External Service', 'Review a Funded Mandate', 'An Accountable National Commitment'),
      ('Postwar guarantees have become continuing work for the government. The chamber will distinguish a political promise from the staff, transport and readiness needed to sustain it.',
       'The chamber will review external obligations against ordinary public services. Civil consent becomes more dependable while ministers accept a slower process for emergency reallocations.',
       'A protected defence appropriation preserves training and readiness against other claims. Its continuing civilian opportunity cost must appear in the national accounts.',
       'Publishing the burden allows an agreement to be limited, renewed or refused without pretending that consent creates additional physical capacity.',
       'A completed service period will test the chosen mandate. The review remains useful after a neighbour refuses cooperation or the wider diplomatic settlement changes.',
       'The final mandate gives the existing institutions a repeatable authorization process. It preserves the chosen civilian or defence priority without replacing the monarch, cabinet or chamber.'),
      (('assembly', 'document'), ('ballot', 'civil'), ('security', 'economy'), ('scales', 'diplomacy'), ('document', 'ballot'), ('assembly', 'peace')),
      (('Parliamentary service mandate', {'stability_factor': 0.025}, {'political_power_gain': -0.05}),
       ('Protected defence appropriation', {'army_org_factor': 0.025}, {'consumer_goods_factor': 0.005})),
      (('Fund a Parliamentary Service Review', 'Inspect the actual staffing and receiving obligations attached to a national commitment.', 'The parliamentary appropriations committee', {'political_power_gain': 0.08}),
       ('Exercise the Appropriation Rota', 'Test how protected readiness and civilian claims are reconciled without adding equipment.', 'The cabinet budget secretariat', {'planning_speed': 0.035}))),
    Branch('SAP', 'air_service', 'SAP_pwi_legacy',
      ('Keep the Air-Service Record', 'Open Professional Review', 'A Restricted Service Debrief',
       'Put Maintenance Lessons into Practice', 'Review the Training Actually Delivered', 'A Professional Air Service'),
      ('The service has training records, unanswered questions and commitments that outlast the postwar ceremony. Preserving those records is a professional obligation rather than a claim about a named squadron.',
       'A professional review will permit civilian questions about service conduct and training. Openness improves confidence while taking instructors away from immediate operational work.',
       'A restricted debrief preserves operational discretion and gives command a common account. The service accepts a continuing political cost for limiting access.',
       'Training lessons require ground crews, inspection intervals and a receiving unit. The programme improves existing capability rather than awarding an aircraft that was not produced.',
       'The review needs a completed, funded training or maintenance period. An interrupted exercise cannot be counted as delivered instruction.',
       'The air service retains its chosen review culture and a tested route from instruction to maintenance. No disappearance, return or cameo of an official pilot is invented.'),
      (('air', 'document'), ('training', 'assembly'), ('command', 'air'), ('tools', 'air'), ('scales', 'training'), ('air', 'peace')),
      (('Open professional review', {'experience_gain_air_factor': 0.035}, {'political_power_gain': -0.05}),
       ('Restricted service debrief', {'air_mission_efficiency': 0.025}, {'stability_factor': -0.015})),
      (('Fund an Air-Service Training Period', 'Reserve instructors and a supervised return of training results.', 'The air-service training inspectorate', {'experience_gain_air_factor': 0.045}),
       ('Inspect the Maintenance Lesson Book', 'Keep a maintenance rota attached to actual service experience.', 'The air-service technical inspectorate', {'air_mission_efficiency': 0.03}))),
    Branch('GEB', 'sovereignty', 'GEB_pwi_legacy',
      ('An Independent Receiving Authority', 'Civil Control at the Frontier', 'A Protected Defence Transit Rota',
       'Write the National Refusal Procedure', 'Review the Frontier Service', 'Sovereignty in Ordinary Administration'),
      ('Independence depends on ordinary officials being able to accept, inspect or refuse a request. A receiving authority will identify the national responsibility behind those decisions.',
       'Civilian authorities will retain control over ordinary frontier services. Their predictable procedures improve confidence while limiting rapid military reassignment.',
       'A protected defence transit rota keeps contingency movement credible. Reserving that capacity imposes a visible cost on other services and grants no automatic access through a neighbour.',
       'A request from an ineligible or unwilling partner must leave a useful national alternative. Written refusal and appeal procedures protect sovereignty without manufacturing a diplomatic incident.',
       'A completed inspection or transit-support period provides evidence for the review. Native military access and faction consent remain separate requirements.',
       'The final charter puts independent authority into a repeatable service rather than a permanent emergency. It does not redraw a frontier or reopen a settled territorial claim.'),
      (('gate', 'document'), ('civil', 'security'), ('logistics', 'security'), ('document', 'peace'), ('scales', 'gate'), ('security', 'peace')),
      (('Civil frontier control', {'stability_factor': 0.025}, {'army_speed_factor': -0.01}),
       ('Protected defence transit', {'supply_consumption_factor': -0.025}, {'consumer_goods_factor': 0.005})),
      (('Fund a Frontier Inspection Period', 'Keep a national receiving office and a documented appeal route in service.', 'The independent customs administration', {'political_power_gain': 0.08}),
       ('Exercise the Defence Transit Desk', 'Test domestic dispatch and receiving instructions without granting foreign military access.', 'The defence transit inspectorate', {'supply_consumption_factor': -0.03}))),
    Branch('GEB', 'recovery', 'GEB_pwi_legacy',
      ('A Register of Remaining Repair Work', 'District Civil-Service Boards', 'A Central Recovery Dispatch',
       'Reserve Skilled Maintenance Crews', 'Publish the Delivered Recovery Record', 'An Economy beyond Mobilization'),
      ('Reconstruction returns will distinguish completed work from projects still waiting for crews. An honest register prevents the same capacity appearing in several ministries\' plans.',
       'District boards will protect ordinary services and publish their maintenance priorities. Local control improves continuity while accepting a continuing administrative burden.',
       'A central dispatch will concentrate skilled crews where disruptions are greatest. The cabinet accepts the political cost of deciding which district waits.',
       'Keeping skilled crews available supports existing workshops, railways and public services. Their rota cannot substitute for native construction, equipment or fuel.',
       'The record must describe a funded period that actually finished. Later administrative improvement cannot become a retroactive wartime preparation reward.',
       'The final recovery policy preserves the chosen local or central priorities and an ordinary maintenance institution. Prosperity remains dependent on productive capacity and a sustainable budget.'),
      (('rebuild', 'document'), ('civil', 'assembly'), ('command', 'logistics'), ('tools', 'rebuild'), ('scales', 'economy'), ('industry', 'peace')),
      (('District service boards', {'repair_speed_factor': 0.035}, {'political_power_gain': -0.05}),
       ('Central recovery dispatch', {'production_factory_efficiency_gain_factor': 0.03}, {'consumer_goods_factor': 0.005})),
      (('Fund a District Maintenance Period', 'Keep district receiving offices and skilled repair crews working to the same record.', 'The civil-service recovery boards', {'repair_speed_factor': 0.045}),
       ('Inspect the Recovery Dispatch Queue', 'Test whether priority crews can return to ordinary productive work after their assignment.', 'The national recovery inspectorate', {'production_factory_efficiency_gain_factor': 0.035}))),
]

COUNTRY_NAMES = {'NPT': 'North Point', 'REC': 'Recta', 'SAP': 'Sapin', 'GEB': 'Gebet'}
SUFFIXES = ('register', 'civil_policy', 'defence_policy', 'operations', 'review', 'settlement')


def branch_id(branch):
    return branch.tag + '_rc_' + branch.key


def focus_id(branch, index):
    return branch_id(branch) + '_' + SUFFIXES[index]


assert len(BRANCHES) == 10
assert all(len(r.titles) == len(r.descriptions) == len(r.subjects) == 6 for r in BRANCHES)
