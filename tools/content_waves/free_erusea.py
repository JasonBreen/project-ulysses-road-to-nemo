"""Wave A: Free Erusea and the oversight years, 2005-2009 (Package 3).

Source layers
-------------
* Official: the provisional autonomous government under ISAF oversight
  (Chronicle 2005 / 09.26, already implemented by ac_ucw), and the Free Erusea
  armed insurrection and its defeat by Mobius 1 (Chronicle 2006 / 09.26; see
  docs/STRANGEREAL_2006_2020_SOURCES.md).
* The historical route records that defeat through Central Usea's response.
  The prolonged insurrection -- pressure model, thresholds, crisis review and
  containment -- is a labelled provisional alternative, as is every policy,
  service, dialogue and number. No insurgent leader, membership, place,
  attack or territorial change is asserted, and Mobius 1 is named only in
  text. The insurrection is tagless: no country tag, civil war, transfer_state
  or core change is created.
"""
from content_waves.framework import Branch, Wave, block, guard

S = "ac_fe"  # owner namespace; also the wave namespace

ERU_ASSESSMENT = "ERU_ucw_exp_settlement_assessment"
FCU_ASSESSMENT = "FCU_ucw_exp_settlement_assessment"
ISAF = "has_global_flag = ac_ucw_outcome_isaf_victory"
STARTED = "has_global_flag = ac_fe_insurrection_started"

BRANCHES = (
    Branch("ERU", "oversight", (ERU_ASSESSMENT,), ISAF,
        ("Inventory the Oversight Instruments", "Civil Ministries First", "A Supervised Security Directorate",
         "Return Signatures to Erusean Offices", "Review a Supervised Service Period", "An Oversight with an End Date"),
        ("The provisional government works under instruments it did not draft and cannot yet amend. Before arguing about their limits, the ministries will list every approval, inspection and reporting duty the oversight arrangement actually requires, and the office that carries each one.",
         "Civil ministries will regain routine authority first: schools, utilities, courts and local registries. Supervisors keep their inspection rights, but ordinary services stop waiting for a foreign signature. The cost is a slower answer whenever security matters cross a civil desk.",
         "A supervised security directorate will concentrate police, border and reserve matters in one accountable office. It gives the oversight partners a single counterpart and the government a coherent plan, at a continuing political price for placing so much authority in one place.",
         "Each transferred duty needs an Erusean office that can sign, refuse and answer for it. The ministries will train receiving staff before asking that a supervisor's countersignature be withdrawn, so that the handover does not leave an empty desk.",
         "A funded service period under the chosen arrangement must be examined before its procedures become permanent. The review compares the promises in the instruments with the work Erusean offices delivered, and names the duties still waiting for a receiving office.",
         "The settlement does not end oversight by declaration. It sets out how each remaining duty returns to Erusean authority and what evidence that requires. The government keeps its chosen priority and accepts that the partners will read the same record."),
        (("document", "scales"), ("civil", "assembly"), ("security", "command"), ("document", "gate"), ("scales", "document"), ("assembly", "peace")),
        (("Civil ministries first", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Supervised security directorate", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.005})),
        (("Staff the Receiving Desks", "Train Erusean officials to take over routine approvals without a supervisor's countersignature.", "The provisional cabinet office", {"political_power_gain": 0.08}),
         ("Audit the Remaining Instruments", "Compare each surviving oversight duty with the office that now performs it.", "The provisional audit commission", {"stability_factor": 0.025})),
        ("A Countersignature at the Bottom of the Page",
         "The circular is ordinary: a school district asks permission to repair a roof before winter. The repair has been approved by the district, costed by the ministry and funded from the provisional budget. It has waited three weeks for a countersignature from an oversight office that has no objection and no time.\n\nThe cabinet secretary lays it beside a dozen others. None is controversial; together they explain why residents have begun to say that nothing in Farbanti can be decided by Eruseans. One minister wants the list published so that the partners see the cost of their caution. Another warns that publishing it will read as an accusation, and that the oversight offices will answer by countersigning more slowly, not less.",
         ("Publish the list of countersigned duties.", "Keep the duty list inside the cabinet office.")),
        ("Fewer Signatures, the Same Accountability",
         "The final review is shorter than the first inventory. Several duties have moved to Erusean offices that sign, refuse and answer for their decisions; the oversight staff now inspect a sample instead of reading every page. Others remain where they were, and the record says why.\n\nThe cabinet secretary keeps the old roof-repair circular in the file. It is not evidence that oversight was wrong. It is evidence of what a procedure costs when nobody is responsible for ending it.")),
    Branch("ERU", "insurrection", (ERU_ASSESSMENT,), ISAF + " " + STARTED,
        ("Answer Free Erusea", "Hearings in the Districts", "Security Cordons",
         "Separate Policing from Reprisal", "Review a Completed Response Period", "A Response the Districts Can Trust"),
        ("Free Erusea's armed insurrection made the provisional government's authority a daily question, whether it was put down in days or is still being fought. The cabinet will record where public services stopped, which offices were threatened and which complaints the insurrection used, before choosing how to answer them.",
         "District hearings will give residents a lawful place to raise grievances about the settlement and the oversight. Listening concedes nothing to the insurrection's methods. It does consume political attention and slows the security measures the partners expect.",
         "Security cordons will protect the public offices, depots and roads the government depends on. They leave armed groups less room to act, at a continuing civilian cost and with the risk that residents meet the state only at checkpoints.",
         "Every arrest, search and closure will be recorded with the office responsible for it. A response that punishes neighbours for an act it cannot solve would recruit for the next insurrection; written limits are part of the security policy, not a concession.",
         "The cabinet will examine one completed, funded response period rather than claim success from quiet weeks. The review asks whether services resumed, whether complaints were answered and whether the chosen policy reduced the pressure on ordinary administration.",
         "The settlement keeps the chosen response as a standing policy with published limits. It declares no victory of its own. It gives the districts a predictable government and leaves a record that later administrations can test."),
        (("security", "document"), ("assembly", "civil"), ("security", "gate"), ("scales", "security"), ("document", "scales"), ("civil", "peace")),
        (("District hearings", {"stability_factor": 0.03}, {"political_power_gain": -0.06}),
         ("Security cordons", {"army_org_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Fund a District Hearing Rota", "Keep hearing officers, clerks and a protected meeting place available in the affected districts.", "The provisional interior ministry", {"stability_factor": 0.03}),
         ("Protect the Public Offices", "Assign guards and inspection teams to the offices, depots and roads that keep services running.", "The provisional security directorate", {"army_org_factor": 0.03})),
        ("The Office That Stayed Open",
         "A district registry reopened on Monday after a week of closure during the fighting. By Wednesday its clerk had been warned twice to stay at home, and by Friday she had filed both warnings with the police along with the forty applications she processed in between. Her supervisor forwards the file to the cabinet with one question: what is the government prepared to do for the people who keep its offices open?\n\nThe interior ministry wants the file read aloud at the next district hearing, so that residents see who is threatened and who is not afraid. The security directorate wants it held back: names in a public record are names the insurrection can find.",
         ("Read the file at the district hearing.", "Protect the file and the clerk's name.")),
        ("A Government That Is Still There",
         "The final review does not claim a victory. It counts the offices that are open, the hearings that were held, the searches that were recorded and the complaints that received an answer. Some districts are calmer; some are not. The review says which, and why the cabinet believes the difference matters.\n\nThe registry clerk's file is in the appendix. She is still at work.")),
    Branch("ERU", "return", ("ERU_ucw_exp_resettlement",), "",
        ("Bring the Displaced Home", "District Return Registers", "A Central Resettlement Schedule",
         "Housing Before Promises", "Review the Returns Actually Made", "A Return That Lasts"),
        ("Years of refugee closures, emergency measures and reconstruction have left families recorded in camps, temporary housing and the wrong districts. The ministries will reconcile those registers before promising anyone a date to go home.",
         "District offices will keep their own return registers and decide the order in which households move. Local knowledge avoids sending families to houses that no longer exist, at the cost of uneven progress and constant negotiation with the capital.",
         "A central schedule will move households according to national priorities for housing, work and transport. It is faster where the capital's figures are right, and politically costly wherever a district learns it must wait.",
         "A return is only complete when there is a roof, water and a school place. Housing inspectors will certify each destination before a household is told to travel, even when that delays the published figures.",
         "The review counts households that stayed, not tickets issued. A funded period of returns must be complete before its procedures become national practice, and interrupted or unpaid periods leave the outstanding cases visible.",
         "The settlement turns resettlement into an ordinary service with a register, inspectors and an appeal route. Later governments inherit families who are home and a record of those who are still waiting."),
        (("refugees", "document"), ("civil", "rebuild"), ("command", "rail"), ("shelter", "tools"), ("scales", "refugees"), ("shelter", "peace")),
        (("District return registers", {"stability_factor": 0.02}, {"production_speed_infrastructure_factor": -0.02}),
         ("Central resettlement schedule", {"production_speed_infrastructure_factor": 0.04}, {"political_power_gain": -0.05})),
        (("Fund a Housing Inspection Period", "Certify destination housing and services before households are asked to travel.", "The housing inspectorate", {"production_speed_infrastructure_factor": 0.04}),
         ("Run a Return Transport Rota", "Schedule transport, receiving offices and first-month support for returning households.", "The transport and resettlement office", {"stability_factor": 0.025})),
        ("Two Registers, One Family",
         "The family appears twice: once in a camp register as waiting to return, and once in a district register as already home. Both entries are signed. The housing inspector who visits the district address finds a roof, no water connection and a neighbour who says the family came, stayed a fortnight and left again.\n\nThe district office wants to publish the discrepancy with every other one it can find, so that residents can correct the registers themselves. The resettlement office argues that a public list of failed returns will discourage families still deciding whether to travel, and asks for a protected reconciliation first.",
         ("Publish the discrepancies for correction.", "Reconcile the registers before publishing.")),
        ("The Second Visit",
         "The final review is built on second visits. An inspector returns to each certified address after the household has lived there through a season, and records whether they are still there and what they still lack. The numbers are smaller than the original schedule promised. They are also the first numbers that the ministries, the districts and the families agree on.\n\nThe family that appeared twice is now recorded once.")),
    Branch("ERU", "victor", ("ERU_ucw_exp_occupation_review",), "has_global_flag = ac_ucw_outcome_erusean_victory",
        ("Count the Cost of Victory", "Return Authority to Local Offices", "Hold the Garrison Line",
         "Bring the Reserves Home", "Review the Garrison Accounts", "A Peace That Does Not Need a Garrison"),
        ("Victory left Erusea responsible for more than it can comfortably govern. The cabinet will list every district, depot and garrison its forces still hold, with the cost of each, before deciding which obligations the republic can sustain.",
         "Local offices will resume civil administration wherever order allows, and Erusean commanders will answer to them on ordinary matters. The policy lowers the daily friction of occupation, but the army loses some freedom to act quickly.",
         "The garrison line will stay in place until the government is satisfied that no district will turn against it. Holding the line keeps commanders confident and the cabinet's options open, while soldiers and money stay away from home.",
         "Reservists called up for the war will be released in an order the economy can absorb. Each unit will hand over its duties to a receiving office before it leaves, so that withdrawal does not create a vacuum.",
         "A completed, funded garrison or demobilisation period must be examined before the policy becomes permanent. The review compares the garrison's cost with the order it actually maintained and the services that resumed.",
         "The settlement fixes the terms on which Erusea keeps or reduces its presence. It makes no new territorial claim. It gives the government a sustainable posture and an honest account of what victory now costs each year."),
        (("scales", "command"), ("civil", "gate"), ("security", "command"), ("training", "logistics"), ("economy", "scales"), ("peace", "gate")),
        (("Local civil authority", {"stability_factor": 0.025}, {"army_speed_factor": -0.01}),
         ("Standing garrison line", {"army_org_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Fund a Civil Handover Period", "Transfer routine administration in held districts to receiving civil offices.", "The ministry of the interior", {"stability_factor": 0.025}),
         ("Release a Reserve Contingent", "Return a scheduled group of reservists to civilian work with their duties handed over.", "The general staff demobilisation office", {"production_factory_efficiency_gain_factor": 0.03})),
        ("The Garrison's Monthly Return",
         "The garrison's monthly return arrives with a covering note from its commander. The district is quiet. The quiet costs a battalion, a fuel allocation the ministry of transport wants back and a reservist list whose members ask every week when they will go home. The commander does not recommend withdrawal. He recommends that somebody decide.\n\nThe interior ministry proposes publishing the return so that the public can see what holding the district costs. The general staff would rather present it to the cabinet alone, where the cost can be weighed against risks that are not suitable for print.",
         ("Publish the garrison's monthly return.", "Present the return to the cabinet only.")),
        ("The Cost Written Down",
         "The final account sets the garrison's cost beside the services that resumed and the reservists who went home. It does not pretend that the choice was free in either direction. The commander's covering note is attached; its request that somebody decide has been answered.\n\nThe settlement makes no claim on territory and asks no foreign government to accept anything. It records what Erusea is willing to pay for the peace it won.")),
    Branch("ERU", "armistice", ("ERU_ucw_exp_armistice_commission",), "has_global_flag = ac_ucw_outcome_stalemate",
        ("Keep the Armistice Line", "A Joint Line Commission", "A Fortified Line Posture",
         "Answer Incidents in Writing", "Review a Quiet Season", "An Armistice That Holds"),
        ("The armistice stopped the fighting without settling the questions that started it. The government will map every crossing, observation post and disputed field along the line, and the office answerable for incidents at each.",
         "A joint commission will meet the other side's officers on a fixed schedule to resolve incidents before they grow. The commission costs political capital at home, where critics call every meeting a concession.",
         "The line will be fortified and patrolled so that nobody doubts Erusea's ability to hold it. Deterrence is credible and expensive, and every new position gives the other side a reason to build one of its own.",
         "Every shot, crossing and accident on the line will be answered in writing through the agreed channel. Written answers are slower than a retaliatory patrol, and far less likely to restart a war that neither side can afford.",
         "The review needs a funded patrol or commission period that actually finished. A quiet season proves little on its own; the record shows whether incidents were reported, answered and closed.",
         "The settlement makes the armistice an institution rather than a pause. It keeps the chosen posture, the reporting channel and the costs that come with them. It does not turn the line into a border."),
        (("gate", "scales"), ("diplomacy", "assembly"), ("security", "gate"), ("document", "communications"), ("scales", "radar"), ("peace", "gate")),
        (("Joint line commission", {"stability_factor": 0.025}, {"political_power_gain": -0.05}),
         ("Fortified line posture", {"army_org_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Staff the Commission Desk", "Keep liaison officers and interpreters ready to meet on the agreed schedule.", "The armistice liaison office", {"political_power_gain": 0.08}),
         ("Run a Line Patrol Period", "Maintain reporting patrols that record incidents for the agreed channel.", "The line command", {"army_org_factor": 0.03})),
        ("A Field Nobody Ploughed",
         "A farmer has asked whether he may plough a field that lies between two observation posts. Both sides have watched it for a year; nobody has crossed it. His request reaches the liaison office as a single handwritten page, and it raises a question the armistice never answered: who decides what happens in the space the line created?\n\nThe liaison officers want to take the request to the joint channel openly, as a test of whether the other side will answer a civilian question. The line command prefers to resolve it quietly through local commanders, where a refusal would embarrass nobody.",
         ("Raise the request through the joint channel.", "Settle it quietly between local commanders.")),
        ("The Field Has an Answer",
         "The final review lists the incidents of the year and the answers each received. Most are routine. A few were dangerous and were closed in writing before anyone fired a second shot. The farmer's request is in the list, with the date it was answered and the reason given.\n\nThe armistice remains an armistice. It now has a procedure that both sides have used and neither has had reason to abandon.")),
    Branch("ERU", "ordinary", ("ERU_ucw_exp_peace_administration",), "has_global_flag = ac_ucw_war_averted",
        ("Ordinary Government Again", "A Civil Investment Programme", "A Standing Readiness Review",
         "Spend What Was Saved", "Review the Peacetime Accounts", "A Republic Without an Emergency"),
        ("The war that many expected did not come. The ministries still carry emergency rules, reserve plans and special budgets written for it. The cabinet will list which of those arrangements are still needed and which can lapse.",
         "Money held back for a war that did not happen will go to housing, transport and schools. The investment is visible and popular, and it leaves the armed forces with less margin if relations sour again.",
         "A standing readiness review will keep the armed forces trained and equipped at a level the budget can sustain. It reassures commanders and neighbours alike, at the cost of money that civilians can see is not reaching them.",
         "Savings will be spent through ordinary appropriations with published accounts, not emergency decrees. The procedure is slower and less flexible, which is the point: peacetime government should be predictable.",
         "A completed, funded period under the new procedures must be reviewed before they replace the emergency rules for good. The review compares the projects promised with the work delivered.",
         "The settlement retires the emergency framework and keeps the chosen balance between civil investment and readiness. The republic inherits a normal budget and the obligation to defend it in public."),
        (("document", "civil"), ("economy", "industry"), ("training", "command"), ("economy", "scales"), ("scales", "document"), ("peace", "civil")),
        (("Civil investment programme", {"production_factory_efficiency_gain_factor": 0.03}, {"army_org_factor": -0.01}),
         ("Standing readiness review", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.005})),
        (("Fund a Public Works Period", "Deliver a scheduled group of civil projects through ordinary appropriations.", "The ministry of public works", {"production_speed_infrastructure_factor": 0.04}),
         ("Run a Readiness Exercise", "Exercise reserve call-up and maintenance procedures without adding new units.", "The general staff training directorate", {"army_org_factor": 0.03})),
        ("The Emergency Rule Nobody Used",
         "The legal office has found an emergency regulation that allows the transport ministry to requisition trucks without notice. It was written for a war that did not come, renewed twice by habit and never used. It is still in force.\n\nA deputy proposes publishing every such regulation with a date on which it will lapse, so that the public can see what the government no longer needs. The defence ministry asks for a protected review first: some of those powers may be needed again, and announcing their repeal could look like an invitation.",
         ("Publish the emergency rules with lapse dates.", "Review the emergency rules in private first.")),
        ("A Budget Read Aloud",
         "The final peacetime budget is read in the chamber like any other. That is its achievement. The emergency regulations that lapsed are listed in an annex, and the ones the government chose to keep are listed with the reason for each.\n\nNobody can promise that the averted war will stay averted. The republic now prepares for that possibility through ordinary law.")),
    Branch("FCU", "oversight", (FCU_ASSESSMENT,), ISAF,
        ("Administer the Oversight Mandate", "Advise, Do Not Govern", "A Supervising Commission",
         "Hand Back the Routine Duties", "Review a Supervision Period", "A Mandate That Can End"),
        ("Central Usea has become responsible for supervising a government it fought. The treaty secretariat will list each oversight duty, the officials performing it and the cost to the federation, before the work becomes permanent by habit.",
         "Advisers will support Erusean ministries without signing in their place. The approach respects the provisional government and keeps Central Usean staffing modest, while accepting slower results and less direct control.",
         "A supervising commission will countersign key decisions and inspect their implementation. Control is firmer and partners are reassured, at a political and administrative cost that grows with every duty the commission keeps.",
         "Routine duties will return to Erusean offices on a published schedule once receiving staff are trained. Central Usea keeps the right to inspect, not the obligation to run daily administration indefinitely.",
         "A funded supervision period must be completed and examined before its procedures are renewed. The review asks what Central Usean staff actually did and which duties Erusean offices now perform.",
         "The settlement gives the mandate a renewal process and an end condition. Central Usea keeps its chosen posture, its costs and the duty to explain both to its partners and to Erusea."),
        (("document", "diplomacy"), ("diplomacy", "civil"), ("assembly", "scales"), ("document", "gate"), ("scales", "assembly"), ("diplomacy", "peace")),
        (("Advisory oversight", {"political_power_gain": 0.05}, {"stability_factor": -0.01}),
         ("Supervising commission", {"stability_factor": 0.02}, {"political_power_gain": -0.05})),
        (("Second an Advisory Team", "Place advisers with Erusean ministries for a defined period with a written handover.", "The treaty secretariat", {"political_power_gain": 0.08}),
         ("Inspect the Handover Schedule", "Check that returned duties are performed by trained Erusean offices.", "The oversight inspectorate", {"stability_factor": 0.025})),
        ("Advisers Without a Desk",
         "The advisory team's report is candid. Its members have been placed in Erusean ministries, given access to files and invited to meetings, and in two ministries nobody has asked them a question in a month. In a third they are asked to sign everything, because Erusean officials prefer that a foreigner carry the responsibility.\n\nThe treaty secretariat considers publishing the report to show the partners that oversight is neither oppressive nor idle. The federal cabinet would rather send it privately to the provisional government, which may read a public version as a list of complaints about its officials.",
         ("Publish the advisory report.", "Send the report privately to the provisional government.")),
        ("A Mandate With a Calendar",
         "The final review is organised by date. Each oversight duty has a scheduled return to Erusean authority, an inspection that confirms it and a named Central Usean office that will stop doing it. Some dates have passed and the duties have moved. Some have been postponed, with the reason recorded.\n\nNobody in the federal cabinet calls the mandate a success. They call it finite, which is what the partners were promised.")),
    Branch("FCU", "security", (FCU_ASSESSMENT,), ISAF + " " + STARTED,
        ("Support the Provisional Government's Security", "Civil Police Liaison", "Rapid Response Detachments",
         "Keep Support Under Erusean Command", "Review a Support Period", "Support Without Occupation"),
        ("Free Erusea's insurrection tested the arrangement Central Usea promised to support. Before sending anyone further, the federation will establish what the provisional government has asked for, what it can receive and who will command it.",
         "Central Usean police advisers and investigators will work alongside Erusean officers. The liaison strengthens civil policing without a military footprint, and it is slower to show results than the partners would like.",
         "Small detachments will stand ready to protect key sites at the provisional government's request. They respond quickly and are expensive to maintain, and every deployment risks being seen as a return of occupying troops.",
         "Every Central Usean team will operate under an Erusean request and an Erusean supervising officer. The rule protects the provisional government's authority and keeps the federation out of a war of its own.",
         "The federation will examine a completed, funded support period before renewing it. The review asks whether Erusean offices could do more on their own afterwards, not how many Central Usean personnel were deployed.",
         "The settlement fixes the terms of continuing support: who can request it, who commands it and when it ends. It keeps the chosen posture and its costs without making Central Usea a party to an internal war."),
        (("security", "diplomacy"), ("civil", "communications"), ("security", "air"), ("command", "document"), ("scales", "security"), ("peace", "diplomacy")),
        (("Civil police liaison", {"stability_factor": 0.02}, {"political_power_gain": -0.05}),
         ("Rapid response detachments", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.01})),
        (("Second Police Investigators", "Place investigators with Erusean police for a defined period under Erusean supervision.", "The federal police liaison office", {"stability_factor": 0.025}),
         ("Hold a Response Detachment Ready", "Keep a small detachment on notice for requests from the provisional government.", "The federal defence staff", {"army_org_factor": 0.03})),
        ("A Request Signed in Farbanti",
         "The request arrives with every stamp the procedure requires: the provisional interior ministry asks for investigators to help with a case it cannot close alone. It also arrives with a second, unsigned note from an Erusean officer who would rather the federation stayed away, because the insurrection's pamphlets already describe every foreign uniform as proof of occupation.\n\nThe federal liaison office proposes answering openly, publishing both the request and the conditions under which Central Usean investigators will work. The defence staff prefers a quiet answer through official channels, so that the investigators arrive without becoming a headline.",
         ("Answer the request publicly with its conditions.", "Answer quietly through official channels.")),
        ("Who Asked, Who Commanded",
         "The final review is organised around two questions for every Central Usean team: who asked for it, and who commanded it. The answers are Erusean in every case the review accepts. Two deployments failed that test and were withdrawn early; the review lists them too.\n\nThe insurrection's pamphlets have not stopped. The federation's record now gives the provisional government something to answer them with.")),
    Branch("FCU", "partners", (FCU_ASSESSMENT,), "",
        ("Share the Burden with Partners", "A Published Burden Formula", "Central Usean Carriage",
         "Let Partners Decline Usefully", "Review the Shared Accounts", "A Coalition That Can Afford Itself"),
        ("The coalition's preparations and their aftermath were paid for jointly, and the bills have not stopped. The treaty secretariat will list which costs Central Usea carries, which partners expected to share and which promises were never written down.",
         "A published formula will set each partner's share of continuing costs. Predictable shares are easier to defend in every capital, and the federation loses the flexibility to absorb a crisis quietly.",
         "Central Usea will carry the coalition's continuing costs itself and ask partners only for what they offer. The choice keeps the coalition calm and costs the federation money and patience every year.",
         "Partners must be able to refuse a request without a crisis. Each request will name a domestic fallback, so that a refusal changes the plan rather than breaking it, and no partner's consent is assumed.",
         "The secretariat will examine a completed, funded accounting period before the formula or the carriage becomes permanent. The review compares what was promised with what each party actually paid.",
         "The settlement keeps the chosen arrangement and makes its costs visible to every member. It does not compel a partner's participation, change any faction or create a new treaty."),
        (("economy", "diplomacy"), ("document", "scales"), ("logistics", "economy"), ("diplomacy", "gate"), ("scales", "economy"), ("assembly", "peace")),
        (("Published burden formula", {"political_power_gain": 0.05}, {"stability_factor": -0.01}),
         ("Central Usean carriage", {"stability_factor": 0.02}, {"consumer_goods_factor": 0.01})),
        (("Reconcile the Partner Accounts", "Match each partner's pledged contribution with the contribution actually received.", "The treaty secretariat accounts office", {"political_power_gain": 0.08}),
         ("Run a Shared Logistics Period", "Operate common transport and supply services with costs recorded by contributor.", "The coalition logistics office", {"supply_consumption_factor": -0.03})),
        ("The Invoice With No Addressee",
         "The logistics office has found an invoice for fuel delivered to a coalition depot during the crisis. The supplier has been paid by Central Usea. The pledge that was meant to cover it came from a partner whose records show a different depot, a different month and a smaller quantity. Nobody is accused of anything; the paperwork simply never met.\n\nThe secretariat proposes publishing all such mismatches, so that every partner can correct its own records. The federal treasury fears that a public list will look like a bill sent to friends, and asks to settle the mismatches bilaterally first.",
         ("Publish the mismatched accounts.", "Settle each mismatch bilaterally first.")),
        ("Accounts That Every Partner Can Read",
         "The final review is a table. Each row is a cost, each column a partner, and each cell is either a contribution received, a contribution declined with its domestic fallback, or a cost Central Usea chose to carry. The empty cells are labelled as choices rather than failures.\n\nThe invoice with no addressee is in the table, with the partner that eventually claimed it.")),
    Branch("FCU", "drawdown", (FCU_ASSESSMENT,), "NOT = { " + ISAF + " }",
        ("Stand Down the Coalition Posture", "Return Forces to Peacetime Duties", "Keep a Coalition Reserve",
         "Account for Every Commitment", "Review the Stand-Down", "A Federation After the Crisis"),
        ("The crisis did not end in a coalition victory, and the posture built for it is no longer affordable in full. The federation will list every deployment, reserve and promise still in force, and what each costs.",
         "Forces will return to peacetime duties as quickly as receiving bases and civilian jobs allow. The savings are real and the federation's capacity to respond to a new crisis is reduced.",
         "A smaller coalition reserve will stay ready and trained. The reserve keeps options open and reassures partners, at a cost that a federation recovering from the crisis will feel every year.",
         "Each remaining commitment will have an owner, a cost and an end condition. The federation will not keep promises alive only because nobody wrote down how to end them.",
         "A completed, funded stand-down or reserve period must be examined before its procedures become the new normal. The review compares the forces released with the capacity actually retained.",
         "The settlement fixes the federation's peacetime posture and the costs of keeping it. It records the outcome without reopening it, and leaves later governments a defensible starting point."),
        (("command", "document"), ("training", "civil"), ("security", "command"), ("document", "scales"), ("scales", "command"), ("peace", "assembly")),
        (("Peacetime duties", {"production_factory_efficiency_gain_factor": 0.025}, {"army_org_factor": -0.01}),
         ("Coalition reserve", {"army_org_factor": 0.025}, {"consumer_goods_factor": 0.005})),
        (("Release a Deployment", "Return a scheduled deployment to home bases with its duties handed over.", "The federal defence staff", {"production_factory_efficiency_gain_factor": 0.03}),
         ("Exercise the Reserve", "Exercise the retained reserve without adding new units.", "The coalition reserve command", {"army_org_factor": 0.03})),
        ("A Unit Still on the Roster",
         "A transport company appears on the coalition roster at a base it left months ago. Its commander has written twice to ask whether the unit is still assigned to a coalition task; nobody has answered, because the office that would answer was itself stood down. The company is waiting, fully paid, for an order that will not come.\n\nThe defence staff wants to publish the full roster of remaining commitments, so that every partner can see what the federation still promises. The cabinet would rather review it privately first, in case some of those commitments are ones the partners still rely on.",
         ("Publish the roster of remaining commitments.", "Review the roster privately first.")),
        ("Every Commitment Has an Owner",
         "The final review lists each remaining commitment with an owner, a cost and an end condition. The transport company is not on it; it went home with its duties handed over and its commander's letters answered.\n\nThe federation's posture is smaller than it was. It is also, for the first time since the crisis, fully accounted for.")),
)

OPENINGS = {
    "ERU": ("The Files on the Cabinet Table",
        "The cabinet meets with the files the last five years have left behind: emergency regulations, reserve lists, reconstruction registers and agreements that nobody in the room drafted alone. Each minister has marked the pages that touch their department. Some pages carry several marks.\n\n[ERU_fe_route_context]\n\nThe question before the cabinet is how to govern under these arrangements without letting every ordinary decision wait for an extraordinary signature, and how much of that argument to have in public.",
        ("Open the files to public questions.", "Begin with a protected cabinet docket.")),
    "FCU": ("What the Federation Promised",
        "The treaty secretariat has collected every promise the federation made during the Continental War years: to its coalition partners, to its neighbours and to its own citizens. Some promises were written into treaties. Others were made in speeches, and the secretariat has had to reconstruct them from transcripts.\n\n[FCU_fe_route_context]\n\nThe federal cabinet must decide which promises it will keep, which it will renegotiate and which it will openly let lapse, and how much of that sorting to do in front of the partners who heard them.",
        ("Open the promises to public questions.", "Begin with a protected cabinet docket.")),
}

ROUTE_CONTEXT = {
    "ERU": (("ac_ucw_outcome_isaf_victory", "Since September 2005 the provisional government has worked under ISAF oversight. The surrender terms and supervision protocols are among the files, and the choice to accept them was made in Farbanti before this cabinet met."),
            ("ac_ucw_outcome_erusean_victory", "The war ended in Erusea's favour. Among the files are garrison returns and administrative orders for districts the army still holds, with the cost of each."),
            ("ac_ucw_outcome_stalemate", "The war ended in an armistice. Among the files are the armistice terms, the incident reports from the line and the reserve lists that keep it manned."),
            ("ac_ucw_war_averted", "The war many expected did not come. Among the files are the emergency rules, reserve plans and special budgets written for it, most of them still in force."),
            (None, "Among the files are the records of the Continental War years and the obligations they left behind.")),
    "FCU": (("ac_ucw_outcome_isaf_victory", "Since September 2005 those promises include support for Erusea's provisional government under ISAF oversight."),
            ("ac_ucw_outcome_erusean_victory", "The war ended in Erusea's favour, and some of those promises were made for an outcome that did not happen."),
            ("ac_ucw_outcome_stalemate", "The war ended in an armistice, and several promises assumed a peace treaty that was never signed."),
            ("ac_ucw_war_averted", "The war many expected did not come, and several promises were made for a war that never started."),
            (None, "Several of those promises were made for circumstances that have since changed.")),
}

FINALS = {
    "ERU": ("The Government That Remains",
        "The cabinet's last review of the period is not a celebration. It lists what the government now does for itself, what it still does under supervision or pressure, and what it has not yet managed to do at all. It names the offices responsible for each.\n\nErusea after the Continental War years is not the country its ministers would have designed. It is a country whose government can now be held to account for what it does, by its own people as well as by its partners.",
        {"army_org_factor": 0.02}),
    "FCU": ("A Federation Accountable for Its Promises",
        "The final account of the period is a list of promises and what became of each. Some were kept in full. Some were kept late, or in part, or in a different form than the speech that made them. A few were openly abandoned, with the reason recorded.\n\nThe federation has not become a different kind of power. It has become one whose partners can read, in one place, what it said it would do and what it did.",
        {"supply_consumption_factor": -0.02}),
}

ERU_SETTLEMENTS = " ".join(f"has_country_flag = ERU_fe_{k}_settlement_done" for k in ("oversight", "insurrection", "victor", "armistice", "ordinary"))
FCU_SETTLEMENTS = " ".join(f"has_country_flag = FCU_fe_{k}_settlement_done" for k in ("oversight", "security", "drawdown"))

# Service and settlement consumers of the owner. Each relief effect is guarded
# by the owner itself, so it is inert outside a running insurrection.
_EXTRA = {
    ("ERU", "insurrection"): dict(service_effect="ac_fe_relief_major = yes\n", settlement_effect="ac_fe_relief_major = yes\n"),
    ("ERU", "oversight"): dict(settlement_effect="ac_fe_relief_small = yes\n"),
    ("ERU", "return"): dict(service_effect="ac_fe_relief_small = yes\n"),
    ("FCU", "oversight"): dict(settlement_effect="if = { limit = { country_exists = ERU } ERU = { ac_fe_relief_small = yes } }\n"),
    ("FCU", "security"): dict(service_effect="if = { limit = { country_exists = ERU ERU = { NOT = { has_war_with = FCU } } } ERU = { ac_fe_relief_service = yes } }\n"),
}
BRANCHES = tuple(Branch(**{**b.__dict__, **_EXTRA.get((b.tag, b.key), {})}) for b in BRANCHES)

WAVE = Wave(
    prefix=S, infix="fe", label="The Oversight Years", source="tools/content_waves",
    countries={"ERU": "Erusea", "FCU": "Central Usea"},
    eligible="date > 2005.9.25",
    branches=BRANCHES,
    layout={"ERU_oversight": (6, 16), "ERU_insurrection": (12, 16), "ERU_return": (18, 16),
            "ERU_victor": (24, 16), "ERU_armistice": (30, 16), "ERU_ordinary": (36, 16),
            "FCU_oversight": (8, 16), "FCU_security": (14, 16), "FCU_partners": (20, 16), "FCU_drawdown": (26, 16)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"ERU": f"has_country_flag = ERU_fe_return_settlement_done OR = {{ {ERU_SETTLEMENTS} }}",
                 "FCU": f"has_country_flag = FCU_fe_partners_settlement_done OR = {{ {FCU_SETTLEMENTS} }}"},
    themes={"ERU": ("document", "security"), "FCU": ("diplomacy", "scales")},
    weekly_extra={"ERU": "ac_fe_owner_weekly = yes\n"},
)

# Owner -------------------------------------------------------------------
ANCHOR = "2006.9.25"        # "date > 2006.9.25" means on or after 26 September 2006
LATE_LIMIT = "2007.9.26"     # later first observations never replay the outbreak
TIERS = (("severe", 69.99, {"stability_factor": -0.06, "political_power_gain": -0.15, "production_factory_efficiency_gain_factor": -0.02}),
         ("active", 34.99, {"stability_factor": -0.04, "political_power_gain": -0.08}),
         ("low", 0, {"stability_factor": -0.015}))
POLICY_DRIFT = (("ERU_fe_insurrection_policy_a_spirit", "0.7"), ("ERU_fe_insurrection_policy_b_spirit", "0.9"))


def owner():
    """Tagless Free Erusea insurrection owner: one ERU variable and three idea tiers."""
    effects, triggers, loc, ideas, events = {}, {}, {}, [], []

    def idea(ident, title, description, values):
        loc[ident] = title
        loc[ident + "_desc"] = description
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" +
                           block("modifier", "\n".join(f"{k} = {v}" for k, v in values.items()))))

    # A capitulated Erusea that still owns land neither starts nor continues the insurrection.
    triggers["ac_fe_owner_eligible"] = "tag = ERU original_tag = ERU any_owned_state = { always = yes } has_capitulated = no " + ISAF
    triggers["ac_fe_running"] = (f"{STARTED} NOT = {{ has_global_flag = ac_fe_insurrection_contained }} NOT = {{ has_global_flag = ac_fe_insurrection_closed }} "
                                 "NOT = { has_global_flag = ac_fe_insurrection_defeated }")
    triggers["ac_fe_fcu_can_respond"] = "country_exists = FCU FCU = { has_capitulated = no NOT = { has_war_with = ERU } }"
    remove_tiers = "".join(f"remove_ideas = ac_fe_pressure_{name}\n" for name, _, _ in TIERS)
    effects["ac_fe_update_tier"] = (
        guard("ac_fe_running = yes check_variable = { ac_fe_pressure > 69.99 }",
              guard("NOT = { has_idea = ac_fe_pressure_severe }", remove_tiers + "add_ideas = ac_fe_pressure_severe")) +
        block("else_if", block("limit", "ac_fe_running = yes check_variable = { ac_fe_pressure > 34.99 }") +
              guard("NOT = { has_idea = ac_fe_pressure_active }", remove_tiers + "add_ideas = ac_fe_pressure_active")) +
        block("else_if", block("limit", "ac_fe_running = yes") +
              guard("NOT = { has_idea = ac_fe_pressure_low }", remove_tiers + "add_ideas = ac_fe_pressure_low")) +
        block("else", remove_tiers.rstrip()))
    effects["ac_fe_begin"] = ("set_global_flag = ac_fe_insurrection_started\nset_variable = { ac_fe_pressure = 55 }\n"
                              "ac_fe_update_tier = yes\nnews_event = { id = ac_fe.1 days = 1 }\n" +
                              guard("ac_fe_fcu_can_respond = yes",
                                    "set_country_flag = { flag = ac_fe_response_window days = 30 }\nFCU = { country_event = { id = ac_fe.5 days = 1 } }") +
                              block("else", "set_global_flag = ac_fe_prolonged"))
    # Historical route: the Chronicle records the defeat by Mobius 1 (2006 / 09.26).
    # Central Usea must still be able to respond when it answers, not only when it was asked.
    effects["ac_fe_defeat"] = guard("ac_fe_running = yes NOT = { has_global_flag = ac_fe_prolonged } ac_fe_fcu_can_respond = yes",
        "set_global_flag = ac_fe_insurrection_defeated\n" + guard("country_exists = ERU", "ERU = { ac_fe_update_tier = yes }") +
        "news_event = { id = ac_fe.6 days = 1 }")
    effects["ac_fe_choose_prolonged"] = guard("ac_fe_running = yes", "set_global_flag = ac_fe_prolonged")
    drift = "set_temp_variable = { ac_fe_delta = 0.4 }\n"
    for policy, amount in POLICY_DRIFT:
        drift += guard(f"OR = {{ has_idea = {policy} has_idea = {policy}_settled }}", f"subtract_from_temp_variable = {{ ac_fe_delta = {amount} }}")
    drift += guard("has_idea = ac_fe_emergency_administration", "subtract_from_temp_variable = { ac_fe_delta = 0.5 }")
    drift += guard("has_idea = ac_fe_partner_assistance", "subtract_from_temp_variable = { ac_fe_delta = 0.5 }")
    drift += guard("has_stability < 0.35", "add_to_temp_variable = { ac_fe_delta = 0.3 }")
    drift += "add_to_variable = { ac_fe_pressure = ac_fe_delta }\nclamp_variable = { var = ac_fe_pressure min = 0 max = 100 }"
    effects["ac_fe_drift"] = drift
    for name, amount in (("small", 3), ("service", 6), ("major", 8)):
        effects[f"ac_fe_relief_{name}"] = guard("ac_fe_running = yes tag = ERU original_tag = ERU has_variable = ac_fe_pressure",
            f"subtract_from_variable = {{ ac_fe_pressure = {amount} }}\nclamp_variable = {{ var = ac_fe_pressure min = 0 max = 100 }}\nac_fe_update_tier = yes")
    effects["ac_fe_contain"] = ("set_global_flag = ac_fe_insurrection_contained\nac_fe_update_tier = yes\n"
                                "news_event = { id = ac_fe.3 days = 1 }")
    effects["ac_fe_close"] = guard(f"{STARTED} NOT = {{ has_global_flag = ac_fe_insurrection_contained }} NOT = {{ has_global_flag = ac_fe_insurrection_closed }} "
                                   "NOT = { has_global_flag = ac_fe_insurrection_defeated }",
        "set_global_flag = ac_fe_insurrection_closed\n" + guard("country_exists = ERU", "ERU = { " + remove_tiers.replace("\n", " ") + "}"))
    effects["ac_fe_owner_weekly"] = (
        guard(f"ac_fe_owner_eligible = yes NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_fe_insurrection_closed }} date > {ANCHOR}",
              guard(f"date < {LATE_LIMIT}", "ac_fe_begin = yes") +
              block("else", "set_global_flag = ac_fe_insurrection_closed\nset_global_flag = ac_fe_late_start_skipped")) +
        guard("ac_fe_running = yes",
              guard("ac_fe_owner_eligible = no", "ac_fe_close = yes") +
              block("else",
                    guard("NOT = { has_global_flag = ac_fe_prolonged } NOT = { has_country_flag = ac_fe_response_window }",
                          "set_global_flag = ac_fe_prolonged") +
                    "ac_fe_drift = yes\nac_fe_update_tier = yes\n" +
                    guard("check_variable = { ac_fe_pressure < 5 }", "ac_fe_contain = yes") +
                    block("else_if", block("limit", "check_variable = { ac_fe_pressure > 84.99 } NOT = { has_country_flag = ac_fe_crisis_cooldown }") +
                          "set_country_flag = { flag = ac_fe_crisis_cooldown days = 365 }\ncountry_event = { id = ac_fe.2 days = 1 }"))))

    idea("ac_fe_pressure_severe", "Free Erusea: Severe Insurrection Pressure",
         "Provisional prolonged route: the insurrection is stopping ordinary administration in several districts. Pressure: [?ac_fe_pressure|0]/100. Values and thresholds are provisional gameplay.", TIERS[0][2])
    idea("ac_fe_pressure_active", "Free Erusea: Active Insurrection",
         "Free Erusea's armed insurrection disrupts services and threatens officials, but the government still functions. Pressure: [?ac_fe_pressure|0]/100. Values and thresholds are provisional gameplay.", TIERS[1][2])
    idea("ac_fe_pressure_low", "Free Erusea: Residual Insurrection",
         "Provisional prolonged route: incidents continue, but the government's offices are open and its services reach most districts. Pressure: [?ac_fe_pressure|0]/100. Values and thresholds are provisional gameplay.", TIERS[2][2])
    idea("ac_fe_emergency_administration", "Administrative Emergency",
         "Emergency powers concentrate decisions in the cabinet for six months. Responses are faster; ordinary politics and consumer supply pay for it.",
         {"political_power_gain": -0.15, "consumer_goods_factor": 0.02, "army_org_factor": 0.02})
    idea("ac_fe_partner_assistance", "Partner Assistance Under Erusean Command",
         "Central Usean investigators and liaison staff support Erusean offices for six months at the provisional government's request.",
         {"stability_factor": 0.02, "political_power_gain": -0.03})
    idea("ac_fe_fcu_support_commitment", "Support Commitment to Erusea",
         "The federation has seconded staff to the provisional government for six months. Their salaries and the political cost of the commitment remain.",
         {"political_power_gain": -0.1})

    loc.update({
        "ac_fe.1.t": "The Free Erusea Insurrection",
        "ac_fe.1.d": "Free Erusea has begun an armed insurrection in Erusea, a year after the provisional government was established under ISAF oversight.\n\nThe ACES Chronicle records both the outbreak and the insurrection's defeat by Mobius 1 on 26 September 2006 (2006 / 09.26). In this campaign that defeat follows Central Usea's response. A prolonged insurrection, if the response is not sent, is provisional gameplay. Neither route creates a new state, border or country.",
        "ac_fe.1.a": "The provisional government and its partners must answer it.",
        "ac_fe.5.t": "Free Erusea Takes Up Arms",
        "ac_fe.5.d": "Free Erusea has begun an armed insurrection in Erusea. The ISAF can answer at once: the ACES Chronicle records that Mobius 1 defeated the insurrection on 26 September 2006 (2006 / 09.26).\n\nThe federation may instead leave the response to Erusea's provisional government. This campaign treats that as a provisional alternative in which the insurrection lasts longer and the provisional government carries the burden.",
        "ac_fe.5.a": "Send Mobius 1.",
        "ac_fe.5.b": "Leave the response to the provisional government.",
        "ac_fe.6.t": "Free Erusea Is Defeated",
        "ac_fe.6.d": "Free Erusea's armed insurrection has been defeated by Mobius 1, as the ACES Chronicle records for 26 September 2006 (2006 / 09.26).\n\nThe provisional government and its partners now face the aftermath: the grievances the insurrection used, the offices it closed and the records it left behind.",
        "ac_fe.6.a": "Turn to the aftermath.",
        "ac_fe.2.t": "The Insurrection Outpaces the Response",
        "ac_fe.2.d": "District reports describe offices closed for weeks, officials who no longer travel and services that have stopped reaching whole communities. The cabinet's current measures are not keeping pace. Ministers can ask the oversight partners for help under Erusean command, or take emergency powers for six months and answer alone.",
        "ac_fe.2.a": "Ask the partners for assistance under Erusean command.",
        "ac_fe.2.b": "Declare a six-month administrative emergency.",
        "ac_fe.3.t": "The Insurrection Recedes",
        "ac_fe.3.d": "Erusea's provisional authorities report that the insurrection no longer prevents ordinary administration. Incidents may continue, but offices are open and services reach the districts again.\n\nThis ends the provisional prolonged route on the government's own assessment. The official record (2006 / 09.26) places the insurrection's defeat at its outbreak, which is the historical route.",
        "ac_fe.3.a": "Keep the offices open.",
        "ac_fe.4.t": "A Request from the Provisional Government",
        "ac_fe.4.d": "Erusea's provisional government asks for investigators and liaison staff to support its offices against the insurrection, under Erusean command, for six months. Accepting will cost the federation political capital and staff. Declining leaves the provisional government to manage alone and the partners to draw their own conclusions.",
        "ac_fe.4.a": "Second investigators and liaison staff.",
        "ac_fe.4.b": "Decline, and offer advice only.",
        "ac_fe_assistance_requested": "Free Erusea: partner assistance requested",
        "ac_fe_assistance_declined": "Free Erusea: partner assistance declined",
        "ac_fe_assistance_given": "Free Erusea: partner assistance given",
        "ac_fe_crisis_cooldown": "Free Erusea: recent crisis review",
        "ac_fe_insurrection_started": "The Free Erusea insurrection has begun",
        "ac_fe_insurrection_contained": "The Free Erusea insurrection has receded",
        "ac_fe_insurrection_closed": "The Free Erusea insurrection owner is closed",
        "ac_fe_insurrection_defeated": "Free Erusea has been defeated (historical route)",
        "ac_fe_prolonged": "Free Erusea fights on (provisional prolonged route)",
        "ac_fe_response_window": "Free Erusea: Central Usea's response is pending",
        "ac_fe_fcu_can_respond": "Central Usea exists, has not capitulated and is not at war with Erusea",
        "ac_fe_late_start_skipped": "The Free Erusea outbreak date had passed before this content first loaded",
        "ac_fe_owner_eligible": "Erusea governs under the post-war oversight arrangement",
        "ac_fe_running": "The Free Erusea insurrection is active",
    })
    request = ("set_country_flag = ac_fe_assistance_requested\n" +
               guard("country_exists = FCU FCU = { NOT = { has_war_with = ERU } has_capitulated = no }", "FCU = { country_event = { id = ac_fe.4 days = 1 } }"))
    emergency = "add_timed_idea = { idea = ac_fe_emergency_administration days = 180 }\nac_fe_relief_service = yes"
    give = ("add_political_power = -40\nadd_timed_idea = { idea = ac_fe_fcu_support_commitment days = 180 }\n" +
            guard("country_exists = ERU", "ERU = { set_country_flag = ac_fe_assistance_given add_timed_idea = { idea = ac_fe_partner_assistance days = 180 } ac_fe_relief_service = yes }"))
    decline = guard("country_exists = ERU", "ERU = { set_country_flag = ac_fe_assistance_declined }")
    events.append(block("news_event", "id = ac_fe.1\ntitle = ac_fe.1.t\ndesc = ac_fe.1.d\npicture = GFX_ac_fe_news_insurrection\nis_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" +
                        block("option", "name = ac_fe.1.a")))
    events.append(block("country_event", "id = ac_fe.2\ntitle = ac_fe.2.t\ndesc = ac_fe.2.d\npicture = GFX_ac_fe_event_eru_national\nis_triggered_only = yes\n"
                        "trigger = { tag = ERU original_tag = ERU ac_fe_running = yes }\n" +
                        block("option", "name = ac_fe.2.a\nai_chance = { factor = 60 }\n" + request) +
                        block("option", "name = ac_fe.2.b\nai_chance = { factor = 40 }\n" + emergency)))
    events.append(block("news_event", "id = ac_fe.3\ntitle = ac_fe.3.t\ndesc = ac_fe.3.d\npicture = GFX_ac_fe_news_recedes\nis_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" +
                        block("option", "name = ac_fe.3.a")))
    events.append(block("country_event", "id = ac_fe.5\ntitle = ac_fe.5.t\ndesc = ac_fe.5.d\npicture = GFX_ac_fe_event_fcu_national\nis_triggered_only = yes\n"
                        "trigger = { tag = FCU original_tag = FCU ac_fe_running = yes NOT = { has_global_flag = ac_fe_prolonged } ac_fe_fcu_can_respond = yes }\n" +
                        block("option", "name = ac_fe.5.a\nai_chance = { factor = 100 }\nac_fe_defeat = yes") +
                        block("option", "name = ac_fe.5.b\nai_chance = { factor = 0 }\nac_fe_choose_prolonged = yes")))
    events.append(block("news_event", "id = ac_fe.6\ntitle = ac_fe.6.t\ndesc = ac_fe.6.d\npicture = GFX_ac_fe_news_defeated\nis_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" +
                        block("option", "name = ac_fe.6.a")))
    events.append(block("country_event", "id = ac_fe.4\ntitle = ac_fe.4.t\ndesc = ac_fe.4.d\npicture = GFX_ac_fe_event_fcu_national\nis_triggered_only = yes\n"
                        "trigger = { tag = FCU original_tag = FCU country_exists = ERU ac_fe_running = yes NOT = { has_war_with = ERU } }\n" +
                        block("option", "name = ac_fe.4.a\nai_chance = { factor = 70 }\n" + guard("ac_fe_running = yes", give)) +
                        block("option", "name = ac_fe.4.b\nai_chance = { factor = 30 }\n" + decline)))
    status = ("Free Erusea's outbreak and its defeat by Mobius 1 are official (Chronicle 2006 / 09.26). If the insurrection is not answered, "
              "the provisional prolonged route tracks pressure: [?ac_fe_pressure|0]/100, containment below 5, crisis review above 85.\n\n")
    custom = ""
    for tag, rows in ROUTE_CONTEXT.items():
        entries = ""
        for n, (flag, value) in enumerate(rows):
            key = f"{tag}_fe_route_context_{n}"
            loc[key] = value
            entries += block("text", (f"trigger = {{ has_global_flag = {flag} }}\n" if flag else "") + "localization_key = " + key)
        custom += block("defined_text", f"name = {tag}_fe_route_context\n" + entries)
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, category_prefix={"ERU": status}, custom=custom,
                interrupt_extra=guard("original_tag = ERU", "ac_fe_close = yes"))


# Registry declarations ------------------------------------------------------
KEY = "A"
NAME = "free_erusea"
IMPORTS = {"ERU": "OVERSIGHT YEARS", "FCU": "OVERSIGHT YEARS"}
LEDGER = "docs/CONTENT_WAVES_A_D.md"
SOURCES = {"official": ["Chronicle 2005 / 09.26: provisional government under ISAF oversight (ac_ucw)",
                        "Chronicle 2006 / 09.26: Free Erusea's armed insurrection and its defeat by Mobius 1"],
           "provisional_gameplay": "Every focus, policy, service, dialogue and value, and the prolonged-insurrection alternative"}
NEWS_ART = (("ac_fe_news_insurrection", ("security", "document"), "The Free Erusea Insurrection", "ERU"),
            ("ac_fe_news_recedes", ("civil", "peace"), "The Insurrection Recedes", "ERU"),
            ("ac_fe_news_defeated", ("air", "peace"), "Free Erusea Is Defeated", "ERU"))
OWNER_ART = {"ac_fe_pressure_severe": ("security", "refugees", "ERU"), "ac_fe_pressure_active": ("security", "communications", "ERU"),
             "ac_fe_pressure_low": ("security", "civil", "ERU"), "ac_fe_emergency_administration": ("command", "document", "ERU"),
             "ac_fe_partner_assistance": ("diplomacy", "security", "ERU"), "ac_fe_fcu_support_commitment": ("diplomacy", "command", "FCU")}
