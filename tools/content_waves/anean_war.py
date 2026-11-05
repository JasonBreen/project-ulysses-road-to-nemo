"""Wave E: the Emmeria-Estovakia War, 2015-2016 (Package 4). Emmeria 36 and Estovakia 36.

Source layers
-------------
Official (ACES site, read 4 November 2026; compiled in
docs/STRANGEREAL_2006_2020_SOURCES.md and docs/research/STRANGEREAL_LORE_1991_2020.md):
every Chronicle entry from 2015 / 04.21 to 2016 / 04.01; the ACE COMBAT 6
abstract (the air raid on Gracemeria, the retreat west toward Khesed Island,
the liberation, the coup and the ceasefire); the Super Weapons rows for the
Aigaion, the Gyges, the Kottos and the Chandelier. Named people, places, ships
and weapons appear only in event text, as the source names them; none becomes a
unit, character, leader, state, border or tag.

Mod provenance, read only: the Estovakian civil war record (``ac_ecw_*``), the
Anea accord, bureau and Nordennavic consultation (``ac_anea_*``), the Anea and
Wave B focus records that the earned alternatives read.

Provisional gameplay: every focus, policy, service, dialogue and value; the
owner's windows, idea values and decisions; the scripted ceasefire (user
decision, 5 November 2026); the two special projects (user decision); the
earned withheld declaration and early settlement; the divergent and
unreachable routes. The November 2015 fireballs are reported without
attribution: the Chronicle does not say what they were.
"""
from content_waves.framework import Branch, Wave, block, guard

P = "ac_eew"
STARTED = "has_global_flag = ac_eew_started"
ENDED = "has_global_flag = ac_eew_ended"
TAINTED = "has_global_flag = ac_eew_tainted"
EXISTING = "has_global_flag = ac_eew_existing_war_observed"
CLOSED = "has_global_flag = ac_eew_closed"
AVOIDED = "OR = { has_global_flag = ac_eew_declaration_withheld has_global_flag = ac_eew_route_divergent }"
ROUTE_SETTLED = f"NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_eew_declaration_withheld }} NOT = {{ {CLOSED} }}"
EMM_CAPITAL = 154
EVA_CAPITAL = 124

BRANCHES = (
    # Emmeria -----------------------------------------------------------------------
    Branch("EMM", "evacuation", (), "date > 2014.12.31",
        ("Open the Evacuation Registers", "Evacuate by District", "Shelter in Place",
         "Run the Western Rail Corridor", "Review an Evacuation Service Period", "A Population Accounted For"),
        ("Sixteen years after Ulysses the republic has rebuilt its cities faster than its plans for leaving them. The interior ministry will reopen the evacuation registers drawn up in the recovery years and test whether they still describe the people who live in each district.",
         "Each district will have a named route, a reception town and a date by which its registers are checked. The plan moves people early and in order; it costs the districts their workers whenever the plan is exercised.",
         "Most citizens will stay where they are, in shelters refitted for long stays, while only the most exposed districts move. The plan keeps the economy running and the roads clear; it asks people to trust the shelters with their lives.",
         "A rail corridor to the western provinces will be kept ready: rolling stock held in reserve, timetables rehearsed and stations staffed. The corridor is the republic's way out if the capital ever has to be left in a hurry.",
         "A completed, funded service period under the chosen plan must be reviewed before the registers become doctrine. The review compares the people the registers list with the people the exercises actually reached.",
         "The settlement fixes the republic's plan for moving or sheltering its people. It does not predict an invasion. It leaves a government that knows how many people it would have to move, and how."),
        (("refugees", "document"), ("refugees", "rail"), ("shelter", "civil"), ("rail", "logistics"), ("scales", "refugees"), ("refugees", "peace")),
        (("Evacuation by district", {"stability_factor": 0.02}, {"production_factory_efficiency_gain_factor": -0.02}),
         ("Shelter in place", {"army_core_defence_factor": 0.03}, {"consumer_goods_factor": 0.01})),
        (("Exercise a District Evacuation", "Move one district's registered population along its named route and back.", "The interior ministry", {"stability_factor": 0.025}),
         ("Hold the Rolling Stock Ready", "Keep the western corridor's reserve trains crewed and timetabled.", "The national railway", {"supply_consumption_factor": -0.03})),
        ("A Register That Is Out of Date",
         "The first exercise has found that a third of the names in one district's register belong to people who moved away years ago, and that the new tower blocks by the harbour are missing entirely.\n\nThe interior ministry wants to publish the error rates for every district and ask citizens to check their own entries. The security service would prefer to correct the registers quietly: a published list of how many people the state cannot find is a list an enemy can read too.",
         ("Publish the error rates and ask citizens to check.", "Correct the registers quietly.")),
        ("A Population Accounted For",
         "The final review lists every district with the people it registers, the route or shelter assigned and the result of its last exercise. The harbour towers are in the register now.\n\nNobody in the review mentions a war. The plan exists so that, if one comes, nobody has to invent it.")),
    Branch("EMM", "administration", (), STARTED,
        ("Govern From the West", "A Government in Exile Abroad", "A Government in the Western Provinces",
         "Keep the Ministries Paid", "Review a Western Administration Period", "The Republic Still Governs"),
        ("The ACES Chronicle records that Estovakian forces seized Gracemeria and that Emmerian forces retreated to western Anea (2015 / 08.30). The republic's government must decide where it governs from, and how it proves to its own people that it still does.",
         "The cabinet will govern from a friendly capital abroad, safe from attack and close to the republic's creditors. It keeps the state's accounts and treaties intact; it governs a country it cannot see.",
         "The cabinet will govern from the western provinces, within reach of the front and of the people still under its authority. It keeps the government visible; it also keeps it within range of the enemy.",
         "Civil servants, pensions and the ministries' own staff will be paid on time, wherever they are. A government that pays its people is a government; one that does not is a memory.",
         "A completed, funded service period of western administration must be reviewed before the arrangement becomes the republic's constitution in wartime. The review counts what the ministries delivered and to whom.",
         "The settlement records how the republic governed while its capital was occupied. It names no date of return. It leaves a state whose citizens could find its offices, and whose offices paid them."),
        (("assembly", "document"), ("diplomacy", "assembly"), ("assembly", "shelter"), ("economy", "civil"), ("scales", "assembly"), ("assembly", "peace")),
        (("Government in exile abroad", {"political_power_gain": 0.05}, {"stability_factor": -0.02}),
         ("Government in the western provinces", {"stability_factor": 0.02}, {"army_core_defence_factor": -0.02})),
        (("Run the Western Ministries", "Staff and fund the ministries operating from the western provinces.", "The cabinet office", {"political_power_gain": 0.08}),
         ("Pay the Displaced Civil Service", "Pay the salaries and pensions of civil servants displaced from the capital.", "The treasury", {"stability_factor": 0.025})),
        ("The Mayor Who Stayed",
         "A district mayor in occupied Gracemeria has kept her office open under the occupation, issuing ration cards and birth certificates on the republic's own forms. The occupation authorities tolerate her; the republic's cabinet cannot decide whether she is a patriot or a collaborator.\n\nThe interior ministry wants to recognise her work publicly as service to the republic. The security service wants nothing said: whatever the cabinet announces will reach the occupation authorities within a day.",
         ("Recognise her service publicly.", "Say nothing and keep her on the payroll.")),
        ("The Republic Still Governs",
         "The final review is a ledger of the ministries' work in the western provinces: salaries paid, schools opened, permits issued, complaints answered. Some entries carry an occupied district's name.\n\nThe mayor who stayed is in the ledger, with the decision the cabinet took about her and the reasons it gave.")),
    Branch("EMM", "reserve", (), STARTED,
        ("Form the Western Reserve", "A Reserve of Volunteers", "A Reserve by Call-Up",
         "Train at the Western Bases", "Review a Reserve Service Period", "A Reserve That Answered"),
        ("The forces that withdrew to western Anea need men and women to replace those lost in the capital. The ministry of defence will form a reserve in the western provinces and decide how to fill it.",
         "The reserve will take volunteers only, trained in short courses and sent forward when ready. Volunteers fight willingly and learn quickly; there may not be enough of them.",
         "The reserve will call up every eligible citizen in the western provinces by age group. The call-up fills the ranks; it empties the farms and workshops the provinces depend on.",
         "Recruits will train at the western bases under instructors withdrawn from the front for the purpose. Training costs the front experienced officers now so that it has trained soldiers later.",
         "A completed, funded service period of reserve training must be reviewed before the reserve becomes the republic's standing practice. The review counts the soldiers trained, the instructors spent and the units sent forward.",
         "The settlement fixes how the republic raised its reserve and what it cost the western provinces. It leaves an army that knows where its soldiers came from, and a province that knows what it gave."),
        (("training", "command"), ("training", "assembly"), ("training", "document"), ("training", "runway"), ("scales", "training"), ("training", "peace")),
        (("Reserve of volunteers", {"army_org_factor": 0.03}, {"political_power_gain": -0.03}),
         ("Reserve by call-up", {"army_core_defence_factor": 0.03}, {"industrial_capacity_factory": -0.03})),
        (("Run a Training Cycle", "Train one cycle of recruits at the western bases.", "The army's training command", {"army_org_factor": 0.03}),
         ("Fund the Reserve Depots", "Equip and supply the reserve's depots in the western provinces.", "The defence logistics office", {"supply_consumption_factor": -0.03})),
        ("Instructors From the Front",
         "The training command asks for fifty experienced officers to be withdrawn from the front line to teach. The front commanders answer that the line will not hold without them.\n\nThe defence minister can order the transfer and publish the reasons, or leave the decision to the commanders and accept whatever the training command receives.",
         ("Order the transfer and publish the reasons.", "Leave it to the front commanders.")),
        ("A Reserve That Answered",
         "The final review lists the reserve's units with their training records and the date each went forward. Beside each is the number of instructors it took to train them.\n\nThe front held, in the places it held. The review does not claim the reserve was the reason, only that it was there.")),
    Branch("EMM", "airforce", (), STARTED,
        ("Reconstitute the Air Force", "Fighters First", "Bases First",
         "Recover the Scattered Squadrons", "Review a Reconstitution Period", "An Air Force Rebuilt"),
        ("The Chronicle records that base and carrier air squadrons could not counter the Aigaion over Gracemeria (2015 / 08.30). The air force that survived is scattered across western airfields, short of aircraft, crews and spares. The air staff will decide how to rebuild it.",
         "Every available resource will go to keeping fighters in the air: airframes, pilots and ammunition first, everything else later. The air force fights now; it may have nowhere to land next month.",
         "The air force will first repair and defend its western bases, then fill them with aircraft. The rebuilding is slower; the aircraft it produces will have somewhere to come home to.",
         "Squadrons scattered by the retreat will be found, counted and reorganised under one command. Some exist only as a handful of aircraft and a commander's notes.",
         "A completed, funded service period of reconstitution must be reviewed before the new structure becomes the air force's order of battle. The review counts aircraft, crews and bases available on the last day.",
         "The settlement records the air force the republic rebuilt after the fall of its capital. It names no pilot and claims no victory. It leaves an air staff that knows what it has."),
        (("air", "tools"), ("air", "missile"), ("runway", "tools"), ("air", "radar"), ("scales", "air"), ("air", "peace")),
        (("Fighters first", {"air_superiority_efficiency": 0.04}, {"repair_speed_factor": -0.05}),
         ("Bases first", {"air_mission_efficiency": 0.03}, {"political_power_gain": -0.03})),
        (("Recover a Squadron", "Find, supply and reorganise one scattered squadron.", "The air staff", {"air_mission_efficiency": 0.03}),
         ("Repair a Western Airfield", "Repair runways, fuel stores and shelters at one western base.", "The air force engineers", {"repair_speed_factor": 0.05})),
        ("A Squadron With No Aircraft",
         "One squadron that escaped the capital has its pilots, its ground crew and its colours, but no aircraft that can fly. Another squadron has six serviceable aircraft and three pilots.\n\nThe air staff proposes merging them under the second squadron's commander and publishing the order. The first squadron's crews have asked to keep their own name and wait for new aircraft.",
         ("Merge the squadrons and publish the order.", "Keep both names and wait for aircraft.")),
        ("An Air Force Rebuilt",
         "The final review is the new order of battle: squadrons, aircraft, bases and crews, each with the date it returned to service. The merged squadron is listed under both names.\n\nThe review records what the air force had on its last day. What it did with it is in the war's own record.")),
    Branch("EMM", "liberation", (), STARTED,
        ("Plan the Return to Gracemeria", "Return With Terms", "Return Without Terms",
         "Restore the Capital's Services", "Review a Recovery Service Period", "A Capital Restored"),
        ("The Chronicle records that Emmerian forces liberated Gracemeria and that cruise missiles fired at the city that night were shot down by patrolling fighters (2016 / 03.31). Whatever the war brings, the government must plan for its return to the capital.",
         "The republic will offer Estovakia terms for the end of the war as soon as the capital is free: a ceasefire, prisoner exchanges and an accounting of the occupation. Terms end the fighting sooner; they also leave questions open.",
         "The republic will return to its capital without offering terms and fight until Estovakia stops. The government keeps every claim intact; the war lasts as long as Estovakia can fight.",
         "Water, power, hospitals and schools in the capital will be restored in a published order, with the occupied districts first. A capital is liberated when its people can live in it again.",
         "A completed, funded service period of recovery must be reviewed before the capital's restoration is declared complete. The review lists the services restored and the districts still waiting.",
         "The settlement records the republic's return to its capital and the terms it offered or withheld. It leaves a government back in Gracemeria, with a ledger of what the occupation cost."),
        (("gate", "civil"), ("peace", "document"), ("command", "gate"), ("civil", "rebuild"), ("scales", "civil"), ("civil", "peace")),
        (("Return with terms", {"stability_factor": 0.02}, {"war_support_factor": -0.02}),
         ("Return without terms", {"war_support_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Restore the Capital's Utilities", "Repair water, power and transport in the capital's occupied districts.", "The capital's municipal office", {"stability_factor": 0.025}),
         ("Reopen the Hospitals", "Restaff and resupply the capital's hospitals.", "The health ministry", {"political_power_gain": 0.08})),
        ("The Occupation's Paperwork",
         "The occupation authorities left their files behind: requisitions, arrests, the names of those who worked for them and those who did not. Every family in the occupied districts wants to know what is in them.\n\nThe justice ministry wants the files opened to the people named in them. The interior ministry wants them sealed until courts can examine them, before old neighbours start settling accounts on their own.",
         ("Open the files to the people named in them.", "Seal the files for the courts.")),
        ("A Capital Restored",
         "The final review lists the capital's districts with the date each regained water, power and a working school. The last entry is a district by the harbour that waited longest.\n\nThe occupation files are where the cabinet decided to put them. The review says where, and who decided.")),
    Branch("EMM", "peace", (), AVOIDED,
        ("Record the Peace That Held", "A Joint Commission", "A Watchful Border",
         "Open the Border Crossings", "Review a Peace Service Period", "A Peace That Held"),
        ("The war the ACES Chronicle records for 2015 did not come in this history: Estovakia withheld its declaration, or its government took another road after the civil war. The republic will decide how to keep a peace it did not have to win.",
         "A joint commission with Estovakia will meet every quarter on border incidents, refugees and trade. The commission gives both governments a place to complain before they act; it gives the republic's hawks a target.",
         "The republic will keep its border watched and its forces ready, without provoking its neighbour. Readiness reassures the public; it also tells Estovakia what Emmeria expects of it.",
         "Crossings closed during the civil war will reopen on a published schedule, with customs and health checks staffed from both sides. Open crossings make the peace visible to the people who live near the border.",
         "A completed, funded service period under the chosen policy must be reviewed before it becomes the republic's settled practice. The review counts incidents, crossings and the commission's answers.",
         "The settlement records a peace this history kept and the official record did not. It claims no reward for it. It leaves two neighbours that know how to talk before they fight."),
        (("peace", "diplomacy"), ("diplomacy", "assembly"), ("security", "radar"), ("gate", "civil"), ("scales", "peace"), ("peace", "civil")),
        (("Joint border commission", {"stability_factor": 0.03}, {"army_core_defence_factor": -0.02}),
         ("Watchful border", {"army_core_defence_factor": 0.03}, {"political_power_gain": -0.03})),
        (("Hold a Commission Session", "Convene the joint commission on the quarter's border incidents.", "The foreign ministry", {"political_power_gain": 0.08}),
         ("Staff the Crossings", "Staff the reopened border crossings with customs and health officers.", "The border service", {"stability_factor": 0.025})),
        ("A Shot Across the River",
         "A border patrol reports that a shot was fired across the river from the Estovakian side. Nobody was hurt. The Estovakian border service says it was a hunter.\n\nThe foreign ministry wants to raise it at the next commission session and publish the answer. The defence ministry wants to double the patrols and say nothing until it knows more.",
         ("Raise it at the commission and publish the answer.", "Double the patrols and wait.")),
        ("A Peace That Held",
         "The final review lists every incident on the border since the war did not come, with what each government said about it. The hunter's shot is there, with the commission's finding.\n\nThe list is longer than anyone wanted. None of its entries became a war.")),
    # Estovakia ---------------------------------------------------------------------
    Branch("EVA", "government", (), STARTED,
        ("Form the War Government", "Rule by the General Staff", "Rule by the Cabinet",
         "Answer to the Assembly", "Review a War Government Period", "Who Governed the War"),
        ("The war the Chronicle records began with Estovakia's invasion of Gracemeria (2015 / 08.30). The federation that fought it had just ended a civil war. Its leaders must decide who governs a country at war: the officers who won the last one, or the civilians who must pay for this one.",
         "The general staff will govern for the duration: decrees instead of laws, commanders instead of ministers. Decisions are fast; nobody outside the staff knows why they were taken.",
         "The cabinet will keep governing, with the general staff answering to it. Civil government is slower and argues more; it keeps a record of who decided what.",
         "The war's conduct will be reported to the assembly each month, with the casualties, costs and occupied territory listed. Reporting costs the government secrecy; it gives the country a reason to believe what it is told.",
         "A completed, funded service period under the chosen arrangement must be reviewed before it becomes the federation's wartime constitution. The review asks who decided, how quickly and on whose authority.",
         "The settlement records who governed Estovakia's war and how. It does not decide the war. It leaves a record that someone, later, will read."),
        (("command", "assembly"), ("command", "security"), ("assembly", "document"), ("assembly", "scales"), ("scales", "command"), ("document", "peace")),
        (("Rule by the general staff", {"army_org_factor": 0.03}, {"stability_factor": -0.02}),
         ("Rule by the cabinet", {"stability_factor": 0.02}, {"army_org_factor": -0.01})),
        (("Report to the Assembly", "Prepare and deliver one month's report on the war to the assembly.", "The cabinet office", {"stability_factor": 0.025}),
         ("Run the Decree Office", "Issue and record the war government's decrees for one period.", "The general staff's civil office", {"political_power_gain": 0.08})),
        ("A Report the Staff Will Not Sign",
         "The month's report to the assembly lists casualties higher than the general staff has announced. The staff refuses to sign it; the cabinet secretary refuses to send it unsigned.\n\nThe cabinet can send the report as written, with the staff's objection attached, or accept the staff's figures and send a shorter report.",
         ("Send the report with the objection attached.", "Send the shorter report.")),
        ("Who Governed the War",
         "The final review lists the war government's decisions with the name of the body that took each one. Some decisions have two names; a few have none.\n\nThe unsigned report is in the file, with the figures that turned out to be right.")),
    Branch("EVA", "logistics", (), "has_global_flag = ac_ecw_eastern_victory",
        ("Rebuild the Maintenance Base", "Central Depots", "Dispersed Workshops",
         "Train the Ground Crews", "Review a Maintenance Service Period", "A Fleet That Can Fly"),
        ("The civil war left Estovakia's aircraft industry in the hands of the faction that won it, and the federation's new aircraft need ground crews, depots and spares it does not yet have. The ministry of defence will rebuild the maintenance base.",
         "Maintenance will be concentrated in a few large depots with the best tools and engineers. Central depots repair faster and cost less; one raid can close them.",
         "Maintenance will be dispersed among many small workshops near the airfields. Dispersal survives attack; it needs more engineers than the federation has trained.",
         "Ground crews will be trained in a standard course, with the engineers who built the aircraft teaching the people who will keep them flying. The course is long and the instructors are few.",
         "A completed, funded service period under the chosen arrangement must be reviewed before it becomes the air force's standing practice. The review counts aircraft serviceable on the last day.",
         "The settlement fixes the federation's maintenance base. The Super Weapons record describes an Aerial Fleet built around a heavy command cruiser; whatever the federation builds, this is how it keeps it in the air."),
        (("tools", "air"), ("industry", "tools"), ("tools", "runway"), ("training", "tools"), ("scales", "tools"), ("air", "peace")),
        (("Central depots", {"repair_speed_factor": 0.05}, {"army_core_defence_factor": -0.02}),
         ("Dispersed workshops", {"army_core_defence_factor": 0.02}, {"production_factory_efficiency_gain_factor": -0.02})),
        (("Run a Depot Cycle", "Overhaul one cycle of aircraft at the depots.", "The air force maintenance command", {"repair_speed_factor": 0.05}),
         ("Train a Crew Class", "Train one class of ground crews in the standard course.", "The air force technical school", {"air_mission_efficiency": 0.03})),
        ("Engineers From Abroad",
         "The Super Weapons record says the Aigaion was designed on technology brought by Belkan refugees who fled to Estovakia. The maintenance command wants to hire more of them and their students; the security service wants every foreign engineer vetted first.\n\nThe ministry can publish the hiring rules and the vetting standard together, or let the security service vet each engineer in private.",
         ("Publish the hiring and vetting rules.", "Vet each engineer in private.")),
        ("A Fleet That Can Fly",
         "The final review lists the depots, the workshops and the crews trained, with the number of aircraft each kept in the air. The foreign engineers are in the list, with their vetting results.\n\nThe review records what the federation can maintain. What it chooses to build is decided elsewhere.")),
    Branch("EVA", "chandelier", (), "date > 2014.12.31 OR = { has_country_flag = EVA_ecw_chandelier_policy_b_done has_country_flag = EVA_an_chandelier_research_done }",
        ("Reopen the Chandelier Files", "Finish It for Its First Purpose", "Finish It as a Weapon",
         "Set the Firing Rules", "Review a Chandelier Service Period", "Rules Before the First Shot"),
        ("The Super Weapons record says the Chandelier railgun was built to destroy fragments of Ulysses, was unfinished when the asteroid arrived, and was later weaponised. The research team the civil war years kept together is still waiting to know what the federation wants of it.",
         "The railgun will be finished for the purpose it was designed for: tracking and destroying the fragments still in orbit. The programme keeps its civilian justification; it does not promise the generals a weapon.",
         "The railgun will be finished as a weapon, with targets on the ground. The programme gains the general staff's support and budget; it becomes a target itself.",
         "Rules for firing the Chandelier will be written before it can fire: who may order a shot, at what, and what record the order leaves. A weapon that can reach a city needs rules written while it is still incomplete.",
         "A completed, funded service period under the chosen purpose must be reviewed before the railgun is accepted. The review compares the firing rules with the targets the general staff has proposed.",
         "The settlement fixes the Chandelier's purpose and its firing rules. It fires no shot. The Super Weapons record says the railgun was used against an Emmerian-controlled city and later destroyed; this campaign records nothing of the kind by script."),
        (("science", "satellite"), ("satellite", "telescope"), ("missile", "science"), ("scales", "missile"), ("scales", "science"), ("science", "peace")),
        (("Finished for its first purpose", {"research_speed_factor": 0.02}, {"political_power_gain": -0.03}),
         ("Finished as a weapon", {"war_support_factor": 0.03}, {"stability_factor": -0.02})),
        (("Fund a Construction Period", "Fund one period of construction on the railgun's mount and power plant.", "The ministry of science", {"research_speed_factor": 0.03}),
         ("Run a Tracking Trial", "Track orbital fragments with the railgun's sensors without firing.", "The space tracking office", {"political_power_gain": 0.08})),
        ("A Target List From the Staff",
         "The general staff has sent the research team a list of ground targets within the railgun's range and asked for firing tables. The team's director answers that the firing rules have not been written.\n\nThe cabinet can publish the firing rules first and send the list back, or let the staff and the director settle it between them.",
         ("Publish the rules and send the list back.", "Let the staff and the director settle it.")),
        ("Rules Before the First Shot",
         "The final review records the Chandelier's purpose and its firing rules as adopted: who orders, what may be targeted and what record each order leaves. The general staff's list is in the appendix.\n\nThe railgun is closer to completion than it has been since the asteroid fell. The rules apply to whoever holds it.")),
    Branch("EVA", "occupation", (), STARTED,
        ("Administer the Occupied Districts", "A Humanitarian Administration", "A Martial Administration",
         "Account for the Requisitions", "Review an Occupation Period", "An Occupation on Record"),
        ("Estovakian forces hold Emmerian districts in this history, as the Chronicle records they held Gracemeria (2015 / 08.30). The federation must decide how it governs people who did not choose it, and what record it keeps of doing so.",
         "The occupied districts will be governed by civil administrators under the laws of war: food first, schools open, local officials kept where they will serve. The administration costs money and soldiers' patience; it gives the federation fewer enemies behind its lines.",
         "The occupied districts will be governed by the army: curfews, requisitions and arrests at the commanders' discretion. Martial rule secures the lines; it makes enemies of everyone it governs.",
         "Every requisition will be recorded with a receipt: what was taken, from whom and by which unit. A receipt is a promise that someone will be paid back.",
         "A completed, funded service period under the chosen administration must be reviewed before it becomes the federation's policy. The review counts what was requisitioned, what was paid and what was not.",
         "The settlement puts the occupation on record. It does not decide whether the districts are kept. The Chronicle records that the capital was liberated; whoever reads this record afterwards will know how it was governed."),
        (("gate", "document"), ("medical", "civil"), ("security", "gate"), ("scales", "document"), ("scales", "gate"), ("document", "peace")),
        (("Humanitarian administration", {"stability_factor": 0.02}, {"consumer_goods_factor": 0.02}),
         ("Martial administration", {"army_core_defence_factor": 0.03}, {"stability_factor": -0.02})),
        (("Run the Civil Administration", "Administer the occupied districts' food, schools and records for one period.", "The occupation's civil office", {"stability_factor": 0.025}),
         ("Audit the Requisitions", "Audit one period's requisitions against their receipts.", "The army's audit office", {"political_power_gain": 0.08})),
        ("Receipts Nobody Will Honour",
         "The audit office has found thousands of requisition receipts issued by units that no longer exist, for goods the federation has no budget to pay for. The holders of the receipts are queuing outside the civil office.\n\nThe administration can publish the full list and a payment schedule it cannot yet fund, or pay the receipts it can and keep the rest in the file.",
         ("Publish the list and a payment schedule.", "Pay what can be paid and keep the rest.")),
        ("An Occupation on Record",
         "The final review lists the occupied districts with the administration each had, the requisitions made and the receipts paid. The unpaid receipts are listed too.\n\nThe record will outlast the occupation. That is what it is for.")),
    Branch("EVA", "aftermath", (), "has_global_flag = ac_eew_stage_coup",
        ("Count the Cost of the Coup", "A Transitional Government", "A Government of the Officers",
         "Bring the Soldiers Home", "Review a Transition Period", "The Federation After the Coup"),
        ("The Chronicle records that Gustav Dvornik, one of the main architects of the invasion of Emmeria, died, and that an antigovernment coup in Estovakia left its forces unable to fight (2016 / 04.01). Whoever governs the federation now must decide what kind of government it will be.",
         "A transitional government of civilians and officers will govern until elections can be held, with a published timetable. The transition reassures the federation's neighbours; it gives the officers who won the civil war a reason to wait.",
         "The officers who led the coup will govern until order is restored, with no timetable. The officers keep the army together; the federation's neighbours wonder what they will do with it.",
         "Soldiers will be brought home from the front and the occupied districts on a published schedule, units with the longest service first. An army that comes home in order does not come home angry.",
         "A completed, funded service period of transition must be reviewed before the arrangement becomes the federation's constitution. The review asks whether the timetable held and whether the soldiers came home.",
         "The settlement records the federation's government after the coup. It names no new leader and decides no election. It leaves a country that ended a war it started, and must now explain it."),
        (("assembly", "ballot"), ("ballot", "assembly"), ("command", "security"), ("refugees", "rail"), ("scales", "assembly"), ("peace", "assembly")),
        (("Transitional government", {"stability_factor": 0.03}, {"army_org_factor": -0.02}),
         ("Government of the officers", {"army_org_factor": 0.02}, {"stability_factor": -0.02})),
        (("Demobilise a Formation", "Bring one formation home and discharge its conscripts.", "The general staff", {"stability_factor": 0.025}),
         ("Hold a Public Hearing", "Hold a public hearing on the war's conduct and costs.", "The assembly", {"political_power_gain": 0.08})),
        ("The Architect's Papers",
         "Dvornik's office has been sealed since his death. His papers describe how the invasion was planned and who approved it. Several of the people named are in the new government.\n\nThe transition can publish the papers and let the assembly judge, or hand them to a closed commission that will report in a year.",
         ("Publish the papers.", "Hand them to a closed commission.")),
        ("The Federation After the Coup",
         "The final review lists the government's decisions since the coup, the soldiers brought home and the hearings held. The architect's papers are where the government decided to put them.\n\nThe federation is not the country its last civil war promised. It is one that has started to answer for its war.")),
    Branch("EVA", "republic", (), AVOIDED,
        ("Govern After the Civil War", "A Federal Reconciliation", "A Centralised Republic",
         "Rebuild the Provinces", "Review a Reconstruction Period", "A Federation That Did Not March"),
        ("In this history the federation did not invade Emmeria: its government withheld the declaration the Chronicle records for 2015 (2015 / 08.30), or the civil war ended in a settlement the official record does not describe. The country that remains must decide how to govern itself in peace.",
         "The provinces that fought each other in the civil war will share power under a federal settlement, with a council where each has a voice. Reconciliation is slow and argumentative; it gives every faction a reason to keep the peace.",
         "The capital will govern the provinces directly, with the civil war's victors in charge. Centralisation is efficient; it leaves the losers with nothing to lose.",
         "The provinces the civil war damaged most will be rebuilt first, on a published schedule. Rebuilding is the federation's first chance to show its people what peace pays.",
         "A completed, funded service period under the chosen settlement must be reviewed before it becomes the federation's constitution. The review asks whether the provinces were rebuilt and whether the factions stayed at the table.",
         "The settlement records a federation that, in this history, did not march on Gracemeria. It claims nothing the official record does not. It leaves a country rebuilding instead of fighting."),
        (("assembly", "peace"), ("diplomacy", "assembly"), ("command", "assembly"), ("rebuild", "civil"), ("scales", "rebuild"), ("peace", "rebuild")),
        (("Federal reconciliation", {"stability_factor": 0.03}, {"political_power_gain": -0.03}),
         ("Centralised republic", {"political_power_gain": 0.05}, {"stability_factor": -0.02})),
        (("Rebuild a Province", "Fund one period of reconstruction in a war-damaged province.", "The reconstruction ministry", {"stability_factor": 0.025}),
         ("Convene the Provincial Council", "Convene the council of provinces on the period's disputes.", "The federal chancellery", {"political_power_gain": 0.08})),
        ("A General Who Wants a War",
         "A general who won the civil war has told a newspaper that Emmeria's prosperity was built while Estovakia burned, and that the federation should take its share. He has a following in the army and in the eastern provinces.\n\nThe government can answer him in public and set out why the federation will not march, or retire him quietly and let the newspaper wonder why.",
         ("Answer him in public.", "Retire him quietly.")),
        ("A Federation That Did Not March",
         "The final review lists the provinces rebuilt, the council's sessions and the disputes it settled. The general's interview is in the file, with the government's answer.\n\nThe federation that did not march is poorer than the one in the official record thought it would be. It is also at peace.")),
)

OPENINGS = {
    "EMM": ("Sixteen Years After Ulysses",
        "The cabinet meets with the records the recovery years have left: the registers, the shelter refits, the aid sent across the border during Estovakia's civil war and the agreements with its neighbours.\n\n[EMM_ew_route_context]\n\nThe question before the cabinet is what the republic owes its people if the peace of the recovery years ends, and how much of that answer to give in public.",
        ("Open the records to public questions.", "Begin with a protected cabinet docket.")),
    "EVA": ("The Federation After the Civil War",
        "The federation's ministries meet with the records the civil war left: the factions' accounts, the damaged provinces, the aircraft industry and the unfinished projects the war kept alive.\n\n[EVA_ew_route_context]\n\nThe question before the government is what the federation will be in the years after its civil war, and how much of that decision to make where its neighbours can see it.",
        ("Open the records to public questions.", "Begin with a protected cabinet docket.")),
}

# (trigger, text): the first entry whose trigger holds is shown; None is the fallback.
ROUTE_CONTEXT = {
    "EMM": (("has_global_flag = ac_ecw_eastern_victory", "Across the border the Eastern Faction won Estovakia's civil war, as the official record says it did. The road the record describes for 2015 runs through this history."),
            ("has_global_flag = ac_ecw_negotiated", "Across the border Estovakia's civil war ended in a negotiated settlement. The official record's 2015 war belongs to a history this republic's neighbour did not have."),
            ("ac_ecw_running = yes", "Across the border Estovakia's civil war has not ended. The official record's 2015 war needs a neighbour that is no longer fighting itself."),
            (None, "Across the border Estovakia has its own records of the civil war years.")),
    "EVA": (("has_global_flag = ac_ecw_eastern_victory", "The Eastern Faction won the civil war, as the official record says it did, and its officers hold the federation's offices."),
            ("has_global_flag = ac_ecw_negotiated", "The civil war ended in a negotiated settlement, and the factions that signed it share the federation's offices."),
            ("ac_ecw_running = yes", "The civil war has not ended, and the federation's offices are held by whoever holds the buildings."),
            (None, "The civil war years are in the files, with their obligations.")),
}

FINALS = {
    "EMM": ("The Republic That Came Home",
        "The cabinet's last review of the period lists what the republic did in the years the official record fills with a war: who it moved, where it governed from, who it trained and what it rebuilt. It names the offices responsible.\n\nEmmeria after this period is not the country its ministers planned in the recovery years. It is one whose government can say what it did, and to whom.",
        {"stability_factor": 0.02}),
    "EVA": ("A Federation Accounted For",
        "The government's last review of the period lists the decisions the federation took after its civil war: who governed, what it built, what it occupied and how it ended. Some entries are not to its credit; they are in the list.\n\nThe federation has not become a different country. It has become one whose record can be read in one place.",
        {"political_power_gain": 0.05}),
}

EMM_SETTLEMENTS = " ".join(f"has_country_flag = EMM_ew_{k}_settlement_done" for k in ("evacuation", "administration", "reserve", "airforce"))
EVA_SETTLEMENTS = " ".join(f"has_country_flag = EVA_ew_{k}_settlement_done" for k in ("government", "logistics", "chandelier", "occupation"))

WAVE = Wave(
    prefix=P, infix="ew", label="The Emmeria-Estovakia War", source="tools/content_waves",
    countries={"EMM": "Emmeria", "EVA": "Estovakia"},
    eligible="date > 2014.12.31",
    branches=BRANCHES,
    layout={"EMM_evacuation": (3, 37), "EMM_administration": (9, 37), "EMM_reserve": (15, 37), "EMM_airforce": (21, 37),
            "EMM_liberation": (27, 37), "EMM_peace": (33, 37),
            "EVA_government": (3, 37), "EVA_logistics": (9, 37), "EVA_chandelier": (15, 37), "EVA_occupation": (21, 37),
            "EVA_aftermath": (27, 37), "EVA_republic": (33, 37)},
    openings=OPENINGS, finals=FINALS,
    final_ready={"EMM": f"OR = {{ has_country_flag = EMM_ew_liberation_settlement_done has_country_flag = EMM_ew_peace_settlement_done {EMM_SETTLEMENTS} }}",
                 "EVA": f"OR = {{ has_country_flag = EVA_ew_aftermath_settlement_done has_country_flag = EVA_ew_republic_settlement_done {EVA_SETTLEMENTS} }}"},
    themes={"EMM": ("shelter", "air"), "EVA": ("command", "satellite")},
    weekly_extra={"EVA": "ac_eew_owner_weekly = yes\n"},
    event_base=50,
)

# Owner -------------------------------------------------------------------------
CALENDAR = "2015.4.19"       # the owner's calendar opens on 20 April 2015
ANCHOR = "2015.8.29"         # the invasion of Gracemeria, 30 August 2015 (Chronicle, 2015 / 08.30)
LATE_LIMIT = "2015.8.30"     # a first observation on or after the anchor never replays any expired date
CEASEFIRE = "2016.3.31"      # the coup and the ceasefire agreement, 1 April 2016 (Chronicle, 2016 / 04.01)

# (name, "date >" anchor, extra condition, body, news event). Each fires once while the owned war runs untainted.
STAGES = (
    ("gracemeria", "2015.8.29", f"EVA = {{ controls_state = {EMM_CAPITAL} }}",
     "EMM = { add_ideas = ac_eew_emm_capital_occupied }", 20),
    ("vitoze", "2015.11.23", "", "", 22),
    ("sipli", "2015.11.26", "", "", 23),
    ("bartolomeo", "2015.12.26", "", "EMM = { add_timed_idea = { idea = ac_eew_emm_khesed_secured days = 90 } }", 24),
    ("rargom", "2016.1.25", "", "", 25),
    ("selumna", "2016.2.11", "", "", 26),
    ("cavallia", "2016.2.14", "", "", 27),
    ("aerial_fleet", "2016.2.19", "has_global_flag = ac_sp_aerial_fleet_complete",
     "set_global_flag = ac_eew_aerial_fleet_lost\nremove_ideas = ac_sp_aerial_fleet_initiative", 28),
    ("ragno", "2016.3.5", "", "", 29),
    ("moloch", "2016.3.24", "", "add_timed_idea = { idea = ac_eew_eva_moloch_retreat days = 60 }", 30),
    ("fort_norton", "2016.3.25", "", "", 31),
    ("liberation", "2016.3.30", f"has_global_flag = ac_eew_stage_gracemeria EMM = {{ controls_state = {EMM_CAPITAL} }}",
     "EMM = { remove_ideas = ac_eew_emm_capital_occupied }", 32),
    ("coup", "2016.3.31", "", "add_timed_idea = { idea = ac_eew_eva_coup days = 120 }", 33),
    ("chandelier", "2016.3.31", "has_global_flag = ac_sp_chandelier_complete",
     "set_global_flag = ac_eew_chandelier_lost\nremove_ideas = ac_sp_chandelier_railgun", 34),
)
FIREBALLS = ("2015.10.31", "2015.12.1")   # November 2015; the Chronicle gives no day (2015 / 11.XX)

# Every idea the owner adds without a timer; all are removed when the war ends.
WAR_IDEAS = ("ac_eew_eva_war_footing", "ac_eew_emm_war_footing", "ac_eew_emm_capital_occupied")


def owner():
    effects, triggers, loc, ideas, events = {}, {}, {}, [], []

    def idea(ident, title, description, values):
        loc[ident] = title
        loc[ident + "_desc"] = description
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" +
                           block("modifier", "\n".join(f"{k} = {v}" for k, v in values.items()))))

    def news(number, picture):
        events.append(block("news_event", f"id = {P}.{number}\ntitle = {P}.{number}.t\ndesc = {P}.{number}.d\npicture = GFX_{picture}\n"
                            "is_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" + block("option", f"name = {P}.{number}.a")))

    # Triggers ---------------------------------------------------------------------
    triggers["ac_eew_principals"] = "country_exists = EMM country_exists = EVA"
    triggers["ac_eew_war_running"] = f"{STARTED} NOT = {{ {ENDED} }}"
    triggers["ac_eew_course_open"] = f"ac_eew_war_running = yes NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} ac_eew_principals = yes"
    triggers["ac_eew_pair_at_war"] = "ac_eew_principals = yes EVA = { has_war_with = EMM }"
    triggers["ac_eew_sourced_route"] = "has_global_flag = ac_ecw_eastern_victory"
    triggers["ac_eew_can_declare"] = ("tag = EVA original_tag = EVA has_capitulated = no is_subject = no country_exists = EMM "
                                      f"EMM = {{ has_capitulated = no is_subject = no }} NOT = {{ has_war_with = EMM }} ac_eew_sourced_route = yes {ROUTE_SETTLED}")
    # The withheld declaration is earned by both governments' civil-war policies and a record of contact
    # that the war would otherwise erase (the owner's own snapshot of the Anea accord or consultation).
    triggers["ac_eew_restraint_earned"] = ("tag = EVA original_tag = EVA has_country_flag = EVA_ecw_talks_policy_a_done "
                                           "EMM = { has_country_flag = EMM_ecw_aid_policy_a_done } "
                                           "OR = { has_global_flag = ac_eew_had_accord has_global_flag = ac_eew_nec_consulted }")
    triggers["ac_eew_third_party_present"] = ("any_country = { NOT = { tag = EMM } NOT = { tag = EVA } NOT = { is_subject_of = EMM } NOT = { is_subject_of = EVA } "
                                              "OR = { has_war_with = EMM has_war_with = EVA } }")
    triggers["ac_eew_principal_fallen"] = ("OR = { NOT = { country_exists = EMM } NOT = { country_exists = EVA } has_global_flag = ac_eew_emm_fallen "
                                           "has_global_flag = ac_eew_eva_fallen EMM = { has_capitulated = yes } EVA = { has_capitulated = yes } }")

    # Owner effects ------------------------------------------------------------------
    effects["ac_eew_restore"] = guard(f"ac_eew_war_running = yes NOT = {{ {EXISTING} }}",
        guard("tag = EVA NOT = { has_idea = ac_eew_eva_war_footing }", "add_ideas = ac_eew_eva_war_footing") +
        guard("country_exists = EMM EMM = { NOT = { has_idea = ac_eew_emm_war_footing } }", "EMM = { add_ideas = ac_eew_emm_war_footing }"))
    # At opening the owner snapshots the records an EMM-EVA war would erase (ac_anea_daily clears
    # them once the pair is at war), so the earned alternative can still read them.
    snapshot = (guard("has_global_flag = ac_anea_accord", "set_global_flag = ac_eew_had_accord") +
                guard("has_global_flag = ac_anea_bureau", "set_global_flag = ac_eew_had_bureau") +
                guard("has_global_flag = ac_anea_nec_participates", "set_global_flag = ac_eew_nec_consulted"))
    effects["ac_eew_calendar_tick"] = guard(
        f"date > {CALENDAR} NOT = {{ has_global_flag = ac_eew_calendar_started }} NOT = {{ {CLOSED} }}",
        guard(f"date < {LATE_LIMIT} ac_eew_principals = yes ac_eew_sourced_route = yes",
              "set_global_flag = ac_eew_calendar_started\n" + snapshot) +
        block("else_if", block("limit", f"date < {LATE_LIMIT} has_global_flag = ac_ecw_negotiated ac_eew_principals = yes") +
              "set_global_flag = ac_eew_closed\nset_global_flag = ac_eew_route_divergent\n" + snapshot + "news_event = { id = ac_eew.14 days = 1 }") +
        block("else_if", block("limit", f"date < {LATE_LIMIT} NOT = {{ ac_eew_sourced_route = yes }}") +
              "set_global_flag = ac_eew_closed\nset_global_flag = ac_eew_route_unreachable") +
        block("else_if", block("limit", "NOT = { ac_eew_principals = yes }") + "set_global_flag = ac_eew_closed\nset_global_flag = ac_eew_principal_missing") +
        block("else", "set_global_flag = ac_eew_closed\nset_global_flag = ac_eew_late_start_skipped"))
    effects["ac_eew_signature_tick"] = guard(
        "has_global_flag = ac_eew_calendar_started date > 2015.4.20 NOT = { has_global_flag = ac_eew_signature_seen } date < 2015.5.21",
        "set_global_flag = ac_eew_signature_seen\nnews_event = { id = ac_eew.16 days = 1 }")
    settle = "clr_country_flag = ac_eew_declaration_pending\nclr_country_flag = ac_eew_declaration_window\n"
    effects["ac_eew_observe_existing_war"] = guard(f"ac_eew_pair_at_war = yes {ROUTE_SETTLED}",
        settle + "set_global_flag = ac_eew_started\nset_global_flag = ac_eew_existing_war_observed\nnews_event = { id = ac_eew.3 days = 1 }")
    effects["ac_eew_taint"] = guard(f"ac_eew_war_running = yes NOT = {{ {TAINTED} }}", "set_global_flag = ac_eew_tainted")
    # The owner's state is written only if the engine actually created the war.
    effects["ac_eew_declare"] = guard("ac_eew_can_declare = yes",
        guard("OR = { has_war = yes EMM = { has_war = yes } }", "set_global_flag = ac_eew_pre_existing_war") +
        "declare_war_on = { target = EMM type = topple_government }\n" + settle +
        guard("has_war_with = EMM",
              "set_global_flag = ac_eew_started\nadd_ideas = ac_eew_eva_war_footing\n"
              "EMM = { add_ideas = ac_eew_emm_war_footing }\nnews_event = { id = ac_eew.1 days = 1 }\n" +
              guard("has_global_flag = ac_eew_pre_existing_war", "ac_eew_taint = yes\nnews_event = { id = ac_eew.4 days = 2 }")) +
        block("else", "clr_global_flag = ac_eew_pre_existing_war\nset_global_flag = ac_eew_closed\nset_global_flag = ac_eew_declaration_refused"))
    effects["ac_eew_withhold"] = guard("ac_eew_can_declare = yes ac_eew_restraint_earned = yes",
        "set_global_flag = ac_eew_declaration_withheld\n" + settle +
        "add_timed_idea = { idea = ac_eew_eva_restraint_kept days = 365 }\nnews_event = { id = ac_eew.2 days = 1 }")
    effects["ac_eew_declaration_tick"] = guard(
        f"has_global_flag = ac_eew_calendar_started date > {ANCHOR} {ROUTE_SETTLED}",
        guard("ac_eew_pair_at_war = yes", "ac_eew_observe_existing_war = yes") +
        block("else_if", block("limit", "ac_eew_can_declare = yes") +
              guard("NOT = { has_country_flag = ac_eew_declaration_asked }",
                    "set_country_flag = ac_eew_declaration_asked\nset_country_flag = ac_eew_declaration_pending\n"
                    "set_country_flag = { flag = ac_eew_declaration_window days = 14 }\ncountry_event = { id = ac_eew.5 days = 1 }") +
              block("else_if", block("limit", "has_country_flag = ac_eew_declaration_pending NOT = { has_country_flag = ac_eew_declaration_window }") +
                    "ac_eew_declare = yes")) +
        block("else", settle + "set_global_flag = ac_eew_closed\nset_global_flag = ac_eew_principal_unable"))
    remove_all = "".join(f"remove_ideas = {i}\n" for i in WAR_IDEAS)

    def end_news(number, survivor):
        return (guard(f"country_exists = {survivor} NOT = {{ has_global_flag = ac_eew_{survivor.lower()}_fallen }}",
                      f"{survivor} = {{ news_event = {{ id = ac_eew.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_eew.{number} days = 1 }}"))

    def survivor_news(number):
        return (guard("country_exists = EMM NOT = { has_global_flag = ac_eew_emm_fallen }", f"EMM = {{ news_event = {{ id = ac_eew.{number} days = 1 }} }}") +
                block("else_if", block("limit", "country_exists = EVA NOT = { has_global_flag = ac_eew_eva_fallen }") +
                      f"EVA = {{ news_event = {{ id = ac_eew.{number} days = 1 }} }}") +
                block("else", f"news_event = {{ id = ac_eew.{number} days = 1 }}"))
    not_external = "NOT = { has_global_flag = ac_eew_external_fall }"
    effects["ac_eew_record_end"] = guard("ac_eew_war_running = yes",
        "set_global_flag = ac_eew_ended\n" +
        guard(f"{not_external} OR = {{ NOT = {{ country_exists = EVA }} has_global_flag = ac_eew_eva_fallen EVA = {{ has_capitulated = yes }} }}",
              "set_global_flag = ac_eew_outcome_emmerian_victory\n" + end_news(9, "EMM")) +
        block("else_if", block("limit", f"{not_external} OR = {{ NOT = {{ country_exists = EMM }} has_global_flag = ac_eew_emm_fallen EMM = {{ has_capitulated = yes }} }}") +
              "set_global_flag = ac_eew_outcome_estovakian_victory\n" + end_news(10, "EVA")) +
        block("else_if", block("limit", "has_global_flag = ac_eew_ceasefire_signed") +
              "set_global_flag = ac_eew_outcome_ceasefire\n" +
              guard(f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }} has_global_flag = ac_eew_stage_coup NOT = {{ has_global_flag = ac_eew_ceasefire_early }}",
                    "set_global_flag = ac_eew_historical_course") +
              guard("has_global_flag = ac_eew_ceasefire_early", survivor_news(8)) + block("else", survivor_news(7))) +
        block("else_if", block("limit", f"NOT = {{ {TAINTED} }} NOT = {{ {EXISTING} }}") +
              "set_global_flag = ac_eew_outcome_cessation\n" + survivor_news(11)) +
        block("else", "set_global_flag = ac_eew_outcome_cessation\n" + survivor_news(12)) +
        guard("country_exists = EVA", "EVA = { " + remove_all.replace("\n", " ") + "}") +
        guard("country_exists = EMM", "EMM = { " + remove_all.replace("\n", " ") + "}"))
    effects["ac_eew_observation_tick"] = guard("ac_eew_war_running = yes",
        guard(f"NOT = {{ {TAINTED} }} ac_eew_third_party_present = yes", "ac_eew_taint = yes\nnews_event = { id = ac_eew.4 days = 1 }") +
        guard("OR = { ac_eew_principal_fallen = yes NOT = { ac_eew_pair_at_war = yes } }", "ac_eew_record_end = yes"))
    stages = ""
    for name, after, extra, body, number in STAGES:
        stages += guard(f"ac_eew_course_open = yes date > {after} NOT = {{ has_global_flag = ac_eew_stage_{name} }} {extra}".rstrip(),
                        f"set_global_flag = ac_eew_stage_{name}\n" + body + ("\n" if body else "") + f"news_event = {{ id = ac_eew.{number} days = 1 }}")
    # The fireballs have a month, not a day; the brief is skipped if the month passes unobserved.
    stages += guard(f"ac_eew_course_open = yes date > {FIREBALLS[0]} NOT = {{ has_global_flag = ac_eew_stage_fireballs }} NOT = {{ has_global_flag = ac_eew_stage_fireballs_skipped }}",
                    guard(f"date < {FIREBALLS[1]}", "set_global_flag = ac_eew_stage_fireballs\nnews_event = { id = ac_eew.21 days = 1 }") +
                    block("else", "set_global_flag = ac_eew_stage_fireballs_skipped"))
    effects["ac_eew_stage_tick"] = stages
    # The scripted ceasefire (user decision, 5 November 2026). The owner's state is written only if
    # the engine actually ended the war; otherwise the war is observed to its real end.
    effects["ac_eew_sign_ceasefire"] = guard("OR = { AND = { tag = EVA original_tag = EVA } AND = { tag = EMM original_tag = EMM } } ac_eew_war_running = yes ac_eew_pair_at_war = yes NOT = { has_global_flag = ac_eew_ceasefire_signed }",
        "clr_country_flag = ac_eew_ceasefire_pending\nclr_country_flag = ac_eew_ceasefire_window\n" +
        guard("tag = EVA", "white_peace = EMM") + block("else", "white_peace = EVA") +
        guard("NOT = { ac_eew_pair_at_war = yes }", "set_global_flag = ac_eew_ceasefire_signed\nac_eew_record_end = yes") +
        block("else", "set_global_flag = ac_eew_ceasefire_not_made\nac_eew_taint = yes"))
    effects["ac_eew_fight_on"] = guard("tag = EVA original_tag = EVA ac_eew_war_running = yes",
        "set_global_flag = ac_eew_ceasefire_refused\nclr_country_flag = ac_eew_ceasefire_pending\nclr_country_flag = ac_eew_ceasefire_window\n"
        "add_timed_idea = { idea = ac_eew_eva_fought_on days = 180 }\nnews_event = { id = ac_eew.13 days = 1 }")
    effects["ac_eew_ceasefire_tick"] = guard(
        f"ac_eew_course_open = yes date > {CEASEFIRE} has_global_flag = ac_eew_stage_coup NOT = {{ has_global_flag = ac_eew_ceasefire_refused }} NOT = {{ has_global_flag = ac_eew_ceasefire_not_made }}",
        guard("NOT = { has_country_flag = ac_eew_ceasefire_asked }",
              "set_country_flag = ac_eew_ceasefire_asked\nset_country_flag = ac_eew_ceasefire_pending\n"
              "set_country_flag = { flag = ac_eew_ceasefire_window days = 14 }\ncountry_event = { id = ac_eew.6 days = 1 }") +
        block("else_if", block("limit", "has_country_flag = ac_eew_ceasefire_pending NOT = { has_country_flag = ac_eew_ceasefire_window }") +
              "ac_eew_sign_ceasefire = yes"))
    effects["ac_eew_early_settlement"] = guard("tag = EMM original_tag = EMM ac_eew_war_running = yes ac_eew_pair_at_war = yes has_global_flag = ac_eew_stage_liberation "
                                               "has_country_flag = EMM_ew_liberation_policy_a_done NOT = { has_global_flag = ac_eew_ceasefire_signed } NOT = { has_global_flag = ac_eew_ceasefire_early }",
        "set_global_flag = ac_eew_ceasefire_early\nac_eew_sign_ceasefire = yes\n" +
        guard("NOT = { has_global_flag = ac_eew_ceasefire_signed }", "clr_global_flag = ac_eew_ceasefire_early"))
    effects["ac_eew_owner_weekly"] = guard("tag = EVA original_tag = EVA",
        "ac_eew_calendar_tick = yes\nac_eew_signature_tick = yes\nac_eew_declaration_tick = yes\nac_eew_observation_tick = yes\n"
        "ac_eew_stage_tick = yes\nac_eew_ceasefire_tick = yes")
    effects["ac_eew_owner_weekly_emm"] = guard("tag = EMM original_tag = EMM ac_eew_war_running = yes NOT = { country_exists = EVA }", "ac_eew_record_end = yes")
    principal = "OR = { AND = { tag = EMM original_tag = EMM } AND = { tag = EVA original_tag = EVA } } ac_eew_war_running = yes"
    fallen = guard("tag = EMM", "set_global_flag = ac_eew_emm_fallen") + block("else", "set_global_flag = ac_eew_eva_fallen")
    external = "set_global_flag = ac_eew_external_fall\nac_eew_taint = yes\n"
    effects["ac_eew_interrupt_principal"] = guard(principal,
        fallen + guard("NOT = { OR = { AND = { tag = EMM has_war_with = EVA } AND = { tag = EVA has_war_with = EMM } } }", external) +
        "ac_eew_record_end = yes")
    effects["ac_eew_interrupt_external"] = guard(principal, fallen + external + "ac_eew_record_end = yes")
    # Special-project completion effects. Each sets only its own completion flag and reward idea.
    effects["ac_sp_aerial_fleet_complete_effect"] = guard("NOT = { has_global_flag = ac_eew_aerial_fleet_lost }",
        "set_global_flag = ac_sp_aerial_fleet_complete\n" +
        guard("NOT = { has_idea = ac_sp_aerial_fleet_initiative }", "add_ideas = ac_sp_aerial_fleet_initiative"))
    effects["ac_sp_chandelier_complete_effect"] = guard("NOT = { has_global_flag = ac_eew_chandelier_lost }",
        "set_global_flag = ac_sp_chandelier_complete\n" +
        guard("NOT = { has_idea = ac_sp_chandelier_railgun }", "add_ideas = ac_sp_chandelier_railgun"))

    # Ideas (provisional values) ---------------------------------------------------------
    idea("ac_eew_eva_war_footing", "Estovakia at War", "The ACES Chronicle records Estovakia's invasion of Gracemeria and the outbreak of the Emmeria-Estovakia War for 30 August 2015 (2015 / 08.30). The federation is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_eew_emm_war_footing", "Emmeria at War", "The ACES Chronicle records Estovakia's invasion of Gracemeria and the outbreak of the Emmeria-Estovakia War for 30 August 2015 (2015 / 08.30). The republic is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_eew_emm_capital_occupied", "Gracemeria Occupied", "Estovakian forces hold the capital, as the Chronicle records they seized Gracemeria (2015 / 08.30). The republic governs from elsewhere until Emmerian forces actually hold the capital again; the values are provisional gameplay.",
         {"political_power_gain": -0.1, "stability_factor": -0.03})
    idea("ac_eew_emm_khesed_secured", "Khesed Island Secured", "The Chronicle records that Bartolomeo Fortress fell and Emmerian forces established full control of Khesed Island (2015 / 12.27). The western base steadies the republic for ninety days; the value is provisional gameplay.",
         {"stability_factor": 0.02, "war_support_factor": 0.03})
    idea("ac_eew_eva_moloch_retreat", "The Moloch Desert Retreat", "The Chronicle records that Estovakian forces retreated after a large-scale battle in the Moloch Desert (2016 / 03.25). Army organisation suffers for sixty days; the value is provisional gameplay.",
         {"army_org_factor": -0.04, "war_support_factor": -0.03})
    idea("ac_eew_eva_coup", "The Coup", "The Chronicle records that an antigovernment coup in Estovakia left its forces unable to fight (2016 / 04.01). The federation's will to fight collapses for 120 days; the value is provisional gameplay. Its politics are not changed by script.",
         {"war_support_factor": -0.15, "army_org_factor": -0.05})
    idea("ac_eew_eva_restraint_kept", "A Declaration Withheld", "Estovakia's government withheld the invasion the ACES Chronicle records for 30 August 2015 (2015 / 08.30), on the civil-war policies both governments chose and a record of contact between them. This earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "army_org_factor": -0.02, "political_power_gain": -0.03})
    idea("ac_eew_eva_fought_on", "Fighting On After the Coup", "Estovakia refused the ceasefire agreement the ACES Chronicle records for 1 April 2016 (2016 / 04.01) and fights on. This provisional alternative weighs on the federation for 180 days.",
         {"war_support_factor": -0.05, "stability_factor": -0.02})
    idea("ac_sp_aerial_fleet_initiative", "The Aerial Fleet", "§YProvisional gameplay§! reward. The Aerial Fleet Initiative is complete: an Aigaion-class heavy command cruiser escorted by Kottos-class electronic support and Gyges-class fire support platforms (Super Weapons, Aigaion, Kottos and Gyges). The aircraft remain text, not units; the Chronicle records the fleet's destruction (2016 / 02.20).",
         {"air_superiority_efficiency": 0.05, "air_mission_efficiency": 0.03})
    idea("ac_sp_chandelier_railgun", "The Chandelier", "§YProvisional gameplay§! reward. The Chandelier railgun, built to destroy fragments of Ulysses, is complete (Super Weapons, Chandelier). It is never fired by script; the Chronicle records its destruction on Sonne Island (2016 / 04.01).",
         {"war_support_factor": 0.03, "political_power_gain": -0.03})

    # Events ----------------------------------------------------------------------------
    texts = {
        1: ("The Emmeria-Estovakia War Begins",
            "Estovakian forces have begun an invasion of Gracemeria, the capital of the Republic of Emmeria. Base and carrier air squadrons could not counter the heavy command cruiser Aigaion, and Emmerian forces have decided to retreat to western Anea. The ACES Chronicle records the outbreak of the Emmeria-Estovakia War for this day (2015 / 08.30).\n\nThe capital's fall is reported only when Estovakian forces actually hold it; the war ends when the fighting actually ends, not on a calendar date.",
            "Anea is at war.", "ac_eew_news_declaration"),
        2: ("The Invasion That Estovakia Withheld",
            "30 August 2015 has passed without an Estovakian invasion of Emmeria. Both governments' choices in the civil war years and a record of contact between them gave Estovakia's government the standing to withhold the invasion the ACES Chronicle records for this day (2015 / 08.30).\n\nThis is an earned alternative to the official record and is provisional gameplay. Nothing prevents a later war by other means.",
            "Record the restraint.", "ac_eew_news_withheld"),
        3: ("Emmeria and Estovakia Already at War",
            "On the date the ACES Chronicle gives for Estovakia's invasion of Emmeria (2015 / 08.30), the two countries were already fighting one another by other means.\n\nThe owner records that war and observes it from outside: it asserts none of the official course and issues no further dated news. The war's end will be recorded when the fighting actually stops.",
            "Observe the war as it is.", "ac_eew_news_observed"),
        4: ("Other Fighting Enters the Anean War",
            "A third country is now at war with Emmeria or Estovakia. The war between the two is no longer the complete explanation of the fighting, and the owner moves to external observation.\n\nThe dated news of the official course stops here. The war's end will still be recorded when the fighting between Emmeria and Estovakia actually stops.",
            "Observe the wider war.", "ac_eew_news_expanded"),
        7: ("A Ceasefire Agreement",
            "Emmeria and Estovakia have agreed a ceasefire. The ACES Chronicle records the ceasefire agreement after the coup that left Estovakia's forces unable to fight (2016 / 04.01), and the official abstract records that it ended the conflict.\n\nThis campaign records the end on the day the agreement was actually signed.",
            "Begin the accounting.", "ac_eew_news_end"),
        8: ("An Early Settlement",
            "Emmeria has offered Estovakia terms after the liberation of its capital, and the fighting has stopped before the coup and ceasefire the ACES Chronicle records for 1 April 2016 (2016 / 04.01).\n\nThis is an earned alternative to the official record and is provisional gameplay. The war's account begins.",
            "Begin the accounting.", "ac_eew_news_end"),
        9: ("Estovakia Capitulates",
            "Estovakia has capitulated. The war between Emmeria and Estovakia ends in an Emmerian victory.\n\nThe ACES Chronicle records a different end: a coup in Estovakia and a ceasefire agreement (2016 / 04.01). This outcome is the actual result of the campaign, not the official one.",
            "Record the outcome.", "ac_eew_news_end"),
        10: ("Emmeria Capitulates",
             "Emmeria has capitulated. The war between Emmeria and Estovakia ends in an Estovakian victory.\n\nThe ACES Chronicle records a different end: the liberation of Gracemeria (2016 / 03.31), a coup in Estovakia and a ceasefire agreement (2016 / 04.01). This outcome is the actual result of the campaign, not the official one.",
             "Record the outcome.", "ac_eew_news_end"),
        11: ("The Emmeria-Estovakia War Ends",
             "The fighting between Emmeria and Estovakia has stopped. Neither country capitulated, and no ceasefire was signed through this owner.\n\nThe ACES Chronicle records the war's end in a ceasefire agreement after the coup of 1 April 2016 (2016 / 04.01). This campaign records the end on the day the fighting actually ceased, which is today.",
             "Begin the accounting.", "ac_eew_news_end"),
        12: ("The Fighting Between Emmeria and Estovakia Stops",
             "The fighting between Emmeria and Estovakia has stopped. The owner observed this war from outside and asserts nothing about how it was fought.\n\nThe ACES Chronicle's course for the war (2015 / 08.30 to 2016 / 04.01) is not asserted here; the end is recorded on the day the fighting actually ceased.",
             "Record the cessation.", "ac_eew_news_end"),
        13: ("Estovakia Fights On",
             "Estovakia has refused the ceasefire agreement the ACES Chronicle records after the coup of 1 April 2016 (2016 / 04.01) and fights on.\n\nThis is a provisional alternative to the official record. The owner issues no further dated news; the war's end will be recorded when the fighting actually stops.",
             "The war goes on.", "ac_eew_news_fought_on"),
        14: ("A Settlement in Estovakia, No March on Gracemeria",
             "Estovakia's civil war ended in a negotiated settlement in this history, and the federation that signed it is not the one the ACES Chronicle records invading Emmeria (2015 / 08.30).\n\nThe owner closes the sourced route: no war is invented in its place. Both governments' records of these years continue in their own branches.",
             "Record the divergence.", "ac_eew_news_withheld"),
        16: ("An Aircraft Signature Off Estovakia",
             "Yuktobanian spy satellites have spotted a massive aircraft signature near the southeast coast of Estovakia (2015 / 04.21).\n\nThe ACES Chronicle records the sighting and does not say what the signature was. This campaign asserts nothing beyond the record.",
             "Note the sighting.", "ac_eew_news_signature"),
        20: ("Gracemeria Falls",
             "Estovakian forces hold Gracemeria, the capital of the Republic of Emmeria, as the ACES Chronicle records they seized it on 30 August 2015 (2015 / 08.30). The Emmerian government governs from the west.\n\nThis campaign reports the fall only because Estovakian forces actually hold the capital; no state was moved by script.",
             "The capital is lost.", "ac_eew_news_gracemeria"),
        21: ("Fireballs Over the Retreat",
             "Witnesses report multiple giant fireballs attacking Emmerian forces as they retreat, in several places at once (2015 / 11.XX).\n\nThe ACES Chronicle records the sighting for November 2015 without giving the day or saying what the fireballs were. This campaign reports it in that month and asserts no cause.",
             "Note the reports.", "ac_eew_news_fireballs"),
        22: ("Bombers Over Vitoze",
             "Estovakia has sent a large formation of bombers toward the city of Vitoze on Khesed Island, and the remaining Emmerian forces based at Campagna Airport have intercepted them (2015 / 11.24).\n\nKhesed Island is not on this map; the record is reported as the Chronicle gives it.",
             "The island holds.", "ac_eew_news_vitoze"),
        23: ("The Breakthrough at Sipli Field",
             "Aiming to retake Khesed Island, Emmerian ground forces have broken through the Estovakian front-line base at Sipli Field (2015 / 11.27).\n\nThe Chronicle records the breakthrough; no territory changes hands by script.",
             "Press on.", "ac_eew_news_sipli"),
        24: ("Khesed Island Secured",
             "Bartolomeo Fortress has fallen, and Emmerian forces have established full control of Khesed Island (2015 / 12.27).\n\nThe island is not on this map; the republic's western base is represented by a timed spirit, which is provisional gameplay.",
             "The west is secure.", "ac_eew_news_khesed"),
        25: ("The Landing at Rargom Beach",
             "Emmerian land, air and sea forces have made a successful landing offensive at Rargom Beach on the western edge of Anea and established a bridgehead (2016 / 01.26).\n\nThe Chronicle records the landing; no territory changes hands by script.",
             "Hold the bridgehead.", "ac_eew_news_rargom"),
        26: ("Along the Selumna Peaks",
             "Emmerian ground forces are moving east along the Selumna Peaks (2016 / 02.12).\n\nThe Chronicle records the advance; this campaign records no more.",
             "Keep moving.", "ac_eew_news_selumna"),
        27: ("Cavallia Air Force Base Captured",
             "Emmerian forces have captured Cavallia Air Force Base in San Loma (2016 / 02.15).\n\nThe Chronicle records the capture; no state changes hands by script.",
             "Take the base.", "ac_eew_news_cavallia"),
        28: ("The Aerial Fleet Destroyed",
             "The Emmerian Air Force has attacked and destroyed the Aerial Fleet, restoring air superiority to Emmerian forces (2016 / 02.20).\n\nThis campaign reports the destruction because the Aerial Fleet project was completed; its reward is removed.",
             "The sky is clear.", "ac_eew_news_aerial_fleet"),
        29: ("Ragno Fortress",
             "Emmerian forces have made a decisive strike on Ragno Fortress in Grageo Canyon (2016 / 03.06).\n\nThe Chronicle records the strike; this campaign records no more.",
             "Note the strike.", "ac_eew_news_ragno"),
        30: ("The Moloch Desert",
             "A large-scale battle between Emmeria and Estovakia has broken out in the Moloch Desert, and Estovakian forces have retreated (2016 / 03.25).\n\nThe retreat weighs on Estovakia's army for sixty days; the value is provisional gameplay.",
             "Count the cost.", "ac_eew_news_moloch"),
        31: ("Fort Norton",
             "Emmerian forces have assaulted the mining city of Fort Norton, and Estovakia has been prevented from transporting catalysts for weapons of mass destruction (2016 / 03.26).\n\nThe Chronicle records the assault and the catalysts; this campaign records no more.",
             "Note the record.", "ac_eew_news_fort_norton"),
        32: ("Gracemeria Liberated",
             "Emmerian forces have liberated Gracemeria. That night a large number of cruise missiles were fired at the city and shot down in midair by patrolling fighters (2016 / 03.31).\n\nThis campaign reports the liberation because Emmerian forces actually hold the capital again.",
             "The capital is free.", "ac_eew_news_liberation"),
        33: ("The Coup in Estovakia",
             "An antigovernment coup in Estovakia has left its forces unable to fight. Gustav Dvornik, one of the main architects of the invasion of Emmeria, is dead (2016 / 04.01).\n\nThe ACES Chronicle records that a ceasefire agreement followed. The federation's politics are not changed by script; its government must now answer.",
             "The war is ending.", "ac_eew_news_coup"),
        34: ("The Chandelier Destroyed",
             "Emmerian forces have destroyed the Chandelier on Sonne Island (2016 / 04.01).\n\nThis campaign reports the destruction because the Chandelier project was completed; its reward is removed. The railgun was never fired by script.",
             "The railgun is gone.", "ac_eew_news_chandelier"),
    }
    for number, (title, prose, label, picture) in texts.items():
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, label
        news(number, picture)
    loc.update({
        "ac_eew.5.t": "The Invasion of 30 August 2015",
        "ac_eew.5.d": "The ACES Chronicle records that on this day Estovakian forces began an invasion of Gracemeria, the capital of the Republic of Emmeria, and that the Emmeria-Estovakia War broke out (2015 / 08.30). It records no reason for the invasion, and this campaign asserts none.\n\nThe government can begin the invasion the record describes, or withhold it, if the standing to withhold was earned: the federation's civil-war talks settled on a negotiated peace, Emmeria's aid kept its monitors, and a record of contact between the two survives. Withholding is a provisional alternative to the official record.",
        "ac_eew.5.a": "Begin the invasion.",
        "ac_eew.5.b": "Withhold the invasion.",
        "ac_eew.6.t": "The Ceasefire Agreement",
        "ac_eew.6.d": "The coup has left the federation's forces unable to fight. The ACES Chronicle records that a ceasefire agreement followed (2016 / 04.01).\n\nThe government can sign the ceasefire the record describes, or fight on. Fighting on is a provisional alternative; the owner then issues no further dated news, and the war's end is recorded when the fighting actually stops.",
        "ac_eew.6.a": "Sign the ceasefire.",
        "ac_eew.6.b": "Fight on.",
    })
    events.append(block("country_event", "id = ac_eew.5\ntitle = ac_eew.5.t\ndesc = ac_eew.5.d\npicture = GFX_ac_eew_event_eva_declaration\nis_triggered_only = yes\n"
                        "trigger = { tag = EVA original_tag = EVA ac_eew_can_declare = yes }\n" +
                        block("option", "name = ac_eew.5.a\nai_chance = { factor = 100 }\nac_eew_declare = yes") +
                        block("option", "name = ac_eew.5.b\ntrigger = { ac_eew_restraint_earned = yes }\nai_chance = { factor = 0 }\nac_eew_withhold = yes")))
    events.append(block("country_event", "id = ac_eew.6\ntitle = ac_eew.6.t\ndesc = ac_eew.6.d\npicture = GFX_ac_eew_event_eva_ceasefire\nis_triggered_only = yes\n"
                        "trigger = { tag = EVA original_tag = EVA ac_eew_course_open = yes ac_eew_pair_at_war = yes NOT = { has_global_flag = ac_eew_ceasefire_signed } }\n" +
                        block("option", "name = ac_eew.6.a\nai_chance = { factor = 100 }\nac_eew_sign_ceasefire = yes") +
                        block("option", "name = ac_eew.6.b\nai_chance = { factor = 0 }\nac_eew_fight_on = yes")))

    # Decisions ---------------------------------------------------------------------------
    decisions = {}
    ident = "EMM_ew_early_settlement"
    loc[ident] = "Offer Terms After the Liberation"
    loc[ident + "_desc"] = "Offer Estovakia terms once Gracemeria is free (2016 / 03.31), before the coup and ceasefire the Chronicle records for 1 April 2016 (2016 / 04.01). Requires the return with terms as policy. If the engine accepts the peace, the war ends now; this earned alternative is provisional gameplay."
    decisions["ac_eew_emm_services"] = [block(ident, f"icon = ac_eew_{ident}\nallowed = {{ tag = EMM original_tag = EMM }}\nvisible = {{ ac_eew_war_running = yes }}\n"
                                              "available = { ac_eew_war_running = yes ac_eew_pair_at_war = yes has_global_flag = ac_eew_stage_liberation has_country_flag = EMM_ew_liberation_policy_a_done NOT = { has_global_flag = ac_eew_ceasefire_signed } }\n"
                                              "cost = 50\nfire_only_once = yes\n" + block("complete_effect", "ac_eew_early_settlement = yes") + "ai_will_do = { base = 0 }\n")]
    # No-DLC fallback decisions for the two projects, under the shared Track C category.
    fallbacks = []
    for project, available, cancel, days in (
            ("aerial_fleet", "has_global_flag = ac_ecw_eastern_victory has_country_flag = EVA_ew_logistics_operations_done NOT = { has_global_flag = ac_sp_aerial_fleet_complete } NOT = { has_global_flag = ac_eew_aerial_fleet_lost }",
             "has_global_flag = ac_eew_aerial_fleet_lost", 300),
            ("chandelier", "date > 2014.12.31 has_country_flag = EVA_ew_chandelier_operations_done NOT = { has_global_flag = ac_sp_chandelier_complete } NOT = { has_global_flag = ac_eew_chandelier_lost }",
             "has_global_flag = ac_eew_chandelier_lost", 300)):
        body = (f"icon = GFX_decision_ac_sp_{project}\n" + block("allowed", 'NOT = { has_dlc = "Gotterdammerung" }\noriginal_tag = EVA') +
                block("visible", f"always = yes\nNOT = {{ has_global_flag = ac_sp_{project}_complete }}") + block("available", available) +
                block("cancel_trigger", block("OR", cancel)) +
                f"fire_only_once = yes\ncost = 75\ndays_remove = {days}\n" + block("ai_will_do", "base = 5") +
                block("complete_effect", "custom_effect_tooltip = ac_superweapons_programme_started_tt") +
                block("remove_effect", guard(f"NOT = {{ has_global_flag = ac_sp_{project}_complete }}", f"ac_sp_{project}_complete_effect = yes")))
        fallbacks.append(block(f"ac_superweapons_{project}", body))
    decisions["ac_superweapons"] = fallbacks

    # Special projects (user decision, 5 November 2026) --------------------------------------------
    def project(ident, specialization, blueprint, tag, allowed, available, complexity, duration, reward, options, generic):
        unique = block(reward["name"], f"icon = GFX_{reward['name']}\nfire_only_once = yes\n" + block("threshold", "min = 0\nmax = 80") +
                       block("weight", reward["weight"]) + "".join(block("option", o) for o in options))
        return block(ident, f"specialization = {specialization}\nicon = GFX_{ident}\nblueprint_image = {blueprint}\n" +
                     block("project_tags", tag) + block("allowed", f"original_tag = {allowed}") + block("visible", "always = yes") +
                     block("available", available) + f"complexity = sp_complexity.{complexity}\nprototype_time = sp_time.prototype.{duration}\n" +
                     block("ai_will_do", "base = 10") + block("project_output", block("country_effects", f"{ident}_complete_effect = yes")) +
                     block("generic_prototype_rewards", "\n".join(generic)) + block("unique_prototype_rewards", unique))

    projects = (
        "# Source: Super Weapons, Aigaion, Kottos and Gyges; Chronicle 2016 / 02.20. Gate and timing are provisional gameplay.\n" +
        project("ac_sp_aerial_fleet", "specialization_air", "GFX_ac_sp_blueprint_air_defence", "ac_sp_tag_aerial_fleet", "EVA",
                "has_global_flag = ac_ecw_eastern_victory\nFROM = { has_country_flag = EVA_ew_logistics_operations_done }\nNOT = { has_global_flag = ac_sp_aerial_fleet_complete }\nNOT = { has_global_flag = ac_eew_aerial_fleet_lost }",
                "large", "long", dict(name="ac_sp_aerial_fleet_reward_escort_doctrine", weight="base = 20"),
                ("token = ac_sp_aerial_fleet_reward_escort_doctrine_electronic\ndefault = yes\n" +
                 block("iteration_output", block("country_effects", "FROM = { add_project_progress_ratio = constant:sp_progress.gain.low }\nadd_stability = 0.02")),
                 "token = ac_sp_aerial_fleet_reward_escort_doctrine_fire_support\n" +
                 block("iteration_output", block("country_effects", "add_political_power = -50\nFROM = { add_project_progress_ratio = constant:sp_progress.gain.medium }"))),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_air_defence")) +
        "\n# Source: Super Weapons, Chandelier; Chronicle 2016 / 04.01. Completion only; the railgun is never fired by script. Gate and timing are provisional gameplay.\n" +
        project("ac_sp_chandelier", "specialization_land", "GFX_ac_sp_blueprint_land", "ac_sp_tag_railgun", "EVA",
                "date > 2014.12.31\nFROM = { has_country_flag = EVA_ew_chandelier_operations_done }\nNOT = { has_global_flag = ac_sp_chandelier_complete }\nNOT = { has_global_flag = ac_eew_chandelier_lost }",
                "large", "long", dict(name="ac_sp_chandelier_reward_firing_rules",
                                     weight="base = 20\n" + block("modifier", "add = 40\nEVA = { has_country_flag = EVA_ew_chandelier_settlement_done }")),
                ("token = ac_sp_chandelier_reward_firing_rules_written\ndefault = yes\n" +
                 block("iteration_output", block("country_effects", "FROM = { add_project_progress_ratio = constant:sp_progress.gain.low }\nadd_stability = 0.02")),
                 "token = ac_sp_chandelier_reward_firing_rules_staff\n" +
                 block("iteration_output", block("country_effects", "add_political_power = -50\nFROM = { add_project_progress_ratio = constant:sp_progress.gain.medium }"))),
                ("ac_sp_reward_breakthrough", "ac_sp_reward_test_setback", "ac_sp_reward_oversight_review", "ac_sp_reward_field_trials_orbital")))
    loc.update({
        "ac_sp_aerial_fleet": "The Aerial Fleet",
        "ac_sp_aerial_fleet_desc": "The Aerial Fleet Initiative (the P/F-X program): an Aigaion-class heavy command cruiser that fires Nimbus cruise missiles and serves as an airborne carrier, escorted by Kottos-class electronic support and Gyges-class fire support platforms (Super Weapons, Aigaion, Kottos and Gyges). Requires the civil war won by the Eastern Faction and the maintenance base rebuilt.\n\n§YProvisional gameplay§!: the gate, timing and reward values are balance choices. The Chronicle records the fleet's destruction on 20 February 2016.",
        "ac_sp_aerial_fleet_reward_escort_doctrine": "Escort Doctrine",
        "ac_sp_aerial_fleet_reward_escort_doctrine_desc": "The cruiser's escorts can be built around electronic support first, jamming the enemy's radar and communications, or around fire support first, with multi-barrel cannons and missiles beside the cruiser.",
        "ac_sp_aerial_fleet_reward_escort_doctrine_electronic": "Electronic support first",
        "ac_sp_aerial_fleet_reward_escort_doctrine_fire_support": "Fire support first",
        "ac_sp_chandelier": "The Chandelier",
        "ac_sp_chandelier_desc": "The Chandelier railgun, developed to destroy fragments of Ulysses and incomplete when the asteroid arrived (Super Weapons, Chandelier). Requires the railgun's files reopened and a funded period of construction.\n\n§YProvisional gameplay§!: the gate, timing and reward values are balance choices. It is never fired by script; the Chronicle records its destruction on Sonne Island on 1 April 2016.",
        "ac_sp_chandelier_reward_firing_rules": "Firing Rules",
        "ac_sp_chandelier_reward_firing_rules_desc": "The railgun's firing rules can be written into its control systems before the first test, or the general staff can set its own procedures and the rules follow.",
        "ac_sp_chandelier_reward_firing_rules_written": "Build the rules into the controls",
        "ac_sp_chandelier_reward_firing_rules_staff": "Let the staff set procedures",
        "ac_sp_tag_aerial_fleet": "Aerial Fleet Projects",
        "ac_sp_tag_aerial_fleet_speed_factor": "Aerial Fleet Projects Speed",
        "ac_sp_tag_aerial_fleet_speed_factor_tt": " $ac_sp_tag_aerial_fleet_speed_factor$: $RIGHT|+=%1$",
        "ac_superweapons_aerial_fleet": "The Aerial Fleet",
        "ac_superweapons_aerial_fleet_desc": "Without the special-projects feature, the Aerial Fleet programme runs as a timed decision and grants the same reward as the project (Super Weapons, Aigaion). It is cancelled if the Chronicle's destruction of the fleet is reached first.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
        "ac_superweapons_chandelier": "The Chandelier",
        "ac_superweapons_chandelier_desc": "Without the special-projects feature, the Chandelier programme runs as a timed decision and grants the same reward as the project (Super Weapons, Chandelier). It is cancelled if the Chronicle's destruction of the railgun is reached first.\n\n§YProvisional gameplay§!: cost and duration are balance choices.",
    })

    # Defined texts and readable flags ----------------------------------------------------------
    status = (("has_global_flag = ac_eew_outcome_emmerian_victory", "Ended: Estovakia capitulated. The ceasefire the Chronicle records for 1 April 2016 did not occur."),
              ("has_global_flag = ac_eew_outcome_estovakian_victory", "Ended: Emmeria capitulated. The ceasefire the Chronicle records for 1 April 2016 did not occur."),
              ("has_global_flag = ac_eew_historical_course", "Ended: the ceasefire was signed after the coup, as the official course records (2016 / 04.01)."),
              ("has_global_flag = ac_eew_ceasefire_early", "Ended: an early settlement was earned and signed after the liberation (provisional gameplay)."),
              ("has_global_flag = ac_eew_outcome_ceasefire", "Ended: a ceasefire was signed before the official course had run its length."),
              (f"{ENDED} OR = {{ {TAINTED} {EXISTING} }}", "Ended: the fighting stopped while the owner observed the war from outside."),
              (ENDED, "Ended: the fighting stopped without a ceasefire signed through this owner."),
              ("has_global_flag = ac_eew_ceasefire_refused ac_eew_war_running = yes", "Running after the coup: Estovakia refused the ceasefire; the end is recorded when the fighting stops."),
              ("has_global_flag = ac_eew_ceasefire_not_made", "Under external observation: the ceasefire was signed but the engine kept the war."),
              (TAINTED, "Under external observation: other fighting entered the war; the official course is no longer asserted."),
              (EXISTING, "Under external observation: the pair was already at war on the Chronicle's invasion date."),
              (STARTED, "Running on the official course since the invasion of 30 August 2015 (2015 / 08.30)."),
              ("has_global_flag = ac_eew_declaration_withheld", "Withheld: Estovakia withheld the invasion on its earned standing (provisional gameplay)."),
              ("has_global_flag = ac_eew_route_divergent", "Closed: Estovakia's civil war ended in a negotiated settlement; the sourced 2015 route does not apply."),
              ("has_global_flag = ac_eew_route_unreachable", "Closed: the Eastern Faction did not win Estovakia's civil war here; the sourced 2015 route is unreachable."),
              (CLOSED, "Closed: the pair could not fight the recorded war, or the record's dates had passed."),
              (None, "Pending: the Chronicle records Estovakia's invasion of Emmeria for 30 August 2015."))
    entries = ""
    for n, (condition, value) in enumerate(status):
        loc[f"ac_eew_status_{n}"] = value
        entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + f"localization_key = ac_eew_status_{n}")
    custom = block("defined_text", "name = ac_eew_status_text\n" + entries)
    for tag, rows_ in ROUTE_CONTEXT.items():
        entries = ""
        for n, (condition, value) in enumerate(rows_):
            key = f"{tag}_ew_route_context_{n}"
            loc[key] = value
            entries += block("text", (f"trigger = {{ {condition} }}\n" if condition else "") + "localization_key = " + key)
        custom += block("defined_text", f"name = {tag}_ew_route_context\n" + entries)
    loc.update({
        "ac_eew_started": "The Emmeria-Estovakia War has begun",
        "ac_eew_tainted": "The Emmeria-Estovakia War is under external observation",
        "ac_eew_declaration_withheld": "Estovakia withheld the 2015 invasion",
        "ac_eew_ended": "The Emmeria-Estovakia War has ended",
        "ac_eew_closed": "The Emmeria-Estovakia War owner is closed",
        "ac_eew_calendar_started": "The Emmeria-Estovakia War calendar is open",
        "ac_eew_historical_course": "The Emmeria-Estovakia War followed its official course",
        "ac_eew_outcome_cessation": "The fighting between Emmeria and Estovakia stopped without a ceasefire signed here",
        "ac_eew_outcome_ceasefire": "Emmeria and Estovakia signed a ceasefire",
        "ac_eew_outcome_emmerian_victory": "Estovakia capitulated",
        "ac_eew_outcome_estovakian_victory": "Emmeria capitulated",
        "ac_eew_pre_existing_war": "A principal was already at war when the invasion came",
        "ac_eew_existing_war_observed": "Emmeria and Estovakia were already at war when the Chronicle's invasion date came",
        "ac_eew_late_start_skipped": "The Chronicle's invasion date had passed before this content first loaded",
        "ac_eew_principal_missing": "Emmeria or Estovakia did not exist when the calendar opened",
        "ac_eew_principal_unable": "Emmeria or Estovakia could not fight the recorded war",
        "ac_eew_route_unreachable": "Estovakia's civil war did not end in the Eastern Faction's victory, so the sourced 2015 route is unreachable",
        "ac_eew_route_divergent": "Estovakia's civil war ended in a negotiated settlement, so the sourced 2015 route does not apply",
        "ac_eew_declaration_refused": "The engine did not create the declared war; the owner is closed",
        "ac_eew_declaration_asked": "The Estovakian government has been asked about the invasion",
        "ac_eew_declaration_pending": "The Estovakian invasion is pending",
        "ac_eew_declaration_window": "The invasion window is open",
        "ac_eew_ceasefire_asked": "The Estovakian government has been asked about the ceasefire",
        "ac_eew_ceasefire_pending": "The ceasefire answer is pending",
        "ac_eew_ceasefire_window": "The ceasefire window is open",
        "ac_eew_ceasefire_signed": "The ceasefire was signed",
        "ac_eew_ceasefire_early": "An early settlement was earned and signed",
        "ac_eew_ceasefire_refused": "Estovakia refused the ceasefire and fought on",
        "ac_eew_ceasefire_not_made": "The ceasefire was signed but the engine kept the war",
        "ac_eew_emm_fallen": "Emmeria has fallen during the Emmeria-Estovakia War",
        "ac_eew_eva_fallen": "Estovakia has fallen during the Emmeria-Estovakia War",
        "ac_eew_external_fall": "A principal fell to a third party, or outside the pair's own war",
        "ac_eew_had_accord": "The Anea accord was in force when the 2015 calendar opened",
        "ac_eew_had_bureau": "The Anea bureau was in force when the 2015 calendar opened",
        "ac_eew_nec_consulted": "Nordennavic took part in the Anea consultation when the 2015 calendar opened",
        "ac_eew_signature_seen": "The aircraft signature off Estovakia was reported",
        "ac_eew_aerial_fleet_lost": "The Aerial Fleet was destroyed",
        "ac_eew_chandelier_lost": "The Chandelier was destroyed",
        "ac_eew_stage_fireballs_skipped": "November 2015 passed without the fireballs being reported",
        "ac_eew_principals": "Emmeria and Estovakia both exist",
        "ac_eew_war_running": "The Emmeria-Estovakia War is running",
        "ac_eew_course_open": "The Emmeria-Estovakia War follows its official course",
        "ac_eew_pair_at_war": "Emmeria and Estovakia are at war",
        "ac_eew_sourced_route": "The Eastern Faction won Estovakia's civil war",
        "ac_eew_can_declare": "Estovakia can begin the recorded invasion",
        "ac_eew_restraint_earned": "Both governments' civil-war policies and a record of contact give Estovakia the standing to withhold the invasion",
        "ac_eew_third_party_present": "A third country is at war with Emmeria or Estovakia",
        "ac_eew_principal_fallen": "A principal has capitulated or fallen",
    })
    for name, _, _, _, number in STAGES:
        loc[f"ac_eew_stage_{name}"] = "Emmeria-Estovakia War stage: " + loc[f"{P}.{number}.t"]
    loc["ac_eew_stage_fireballs"] = "Emmeria-Estovakia War stage: " + loc[f"{P}.21.t"]

    # FROM is the annexer, the capitulation winner or the overlord: only the other principal's win is a victory.
    hooks = {
        "on_startup": "if = { limit = { country_exists = EVA } EVA = { ac_eew_restore = yes } }",
        "on_weekly_EMM": "ac_eew_owner_weekly_emm = yes",
        "on_annex": ("if = { limit = { OR = { tag = EMM tag = EVA } } FROM = { ac_eew_interrupt_principal = yes } }\n"
                     "else = { FROM = { ac_eew_interrupt_external = yes } }"),
        "on_capitulation_immediate": ("if = { limit = { FROM = { OR = { tag = EMM tag = EVA } } } ac_eew_interrupt_principal = yes }\n"
                                      "else = { ac_eew_interrupt_external = yes }"),
        "on_subject_annexed": ("if = { limit = { FROM = { OR = { tag = EMM tag = EVA } } } ac_eew_interrupt_principal = yes }\n"
                               "else = { ac_eew_interrupt_external = yes }"),
    }
    ai = "\n".join((
        block("ac_eew_eva_tension", "allowed = { original_tag = EVA }\n" +
              block("enable", f"has_global_flag = ac_eew_calendar_started {ROUTE_SETTLED}") +
              "abort_when_not_enabled = yes\nai_strategy = { type = antagonize id = EMM value = 60 }"),
        block("ac_eew_eva_war", "allowed = { original_tag = EVA }\n" + block("enable", "ac_eew_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = EMM value = 150 }"),
        block("ac_eew_emm_war", "allowed = { original_tag = EMM }\n" + block("enable", "ac_eew_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = EVA value = 120 }"),
    ))
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                categories=[], decisions=decisions, hooks=hooks, ai_strategy=ai,
                category_prefix={"EVA": "[ac_eew_status_text]\n\n", "EMM": "[ac_eew_status_text]\n\n"},
                projects=projects, project_tags=["ac_sp_tag_aerial_fleet"])


# Registry declarations ------------------------------------------------------
KEY = "E"
NAME = "anean_war"
IMPORTS = {"EMM": "ANEAN WAR", "EVA": "ANEAN WAR"}
LEDGER = "docs/CONTENT_WAVE_E.md"
SOURCES = {"official": ["Chronicle 2015 / 04.21 to 2016 / 04.01: the Emmeria-Estovakia War",
                        "Abstracts, ACE COMBAT 6: the raid on Gracemeria, the retreat west, the liberation, the coup and the ceasefire",
                        "Super Weapons: Aigaion; Kottos; Gyges; Chandelier"],
           "mod_provenance": "Estovakian civil war record, Anea accord, bureau and Nordennavic consultation, Anea and Wave B focus records, read only",
           "provisional_gameplay": "Every focus, policy, service, dialogue and value; the windows, idea values and decisions; the scripted ceasefire; the two projects; the earned and divergent alternatives"}
NEWS_ART = (("ac_eew_news_declaration", ("command", "air"), "The Emmeria-Estovakia War Begins", "EVA"),
            ("ac_eew_news_withheld", ("document", "peace"), "The Invasion That Estovakia Withheld", "EVA"),
            ("ac_eew_news_observed", ("telescope", "command"), "Emmeria and Estovakia Already at War", "EMM"),
            ("ac_eew_news_expanded", ("telescope", "assembly"), "Other Fighting Enters the Anean War", "EMM"),
            ("ac_eew_news_end", ("peace", "assembly"), "The Emmeria-Estovakia War Ends", "EMM"),
            ("ac_eew_news_fought_on", ("command", "security"), "Estovakia Fights On", "EVA"),
            ("ac_eew_news_signature", ("satellite", "radar"), "An Aircraft Signature Off Estovakia", "EVA"),
            ("ac_eew_news_gracemeria", ("gate", "air"), "Gracemeria Falls", "EMM"),
            ("ac_eew_news_fireballs", ("meteor", "refugees"), "Fireballs Over the Retreat", "EMM"),
            ("ac_eew_news_vitoze", ("air", "radar"), "Bombers Over Vitoze", "EMM"),
            ("ac_eew_news_sipli", ("command", "runway"), "The Breakthrough at Sipli Field", "EMM"),
            ("ac_eew_news_khesed", ("gate", "security"), "Khesed Island Secured", "EMM"),
            ("ac_eew_news_rargom", ("navy", "logistics"), "The Landing at Rargom Beach", "EMM"),
            ("ac_eew_news_selumna", ("logistics", "command"), "Along the Selumna Peaks", "EMM"),
            ("ac_eew_news_cavallia", ("runway", "air"), "Cavallia Air Force Base Captured", "EMM"),
            ("ac_eew_news_aerial_fleet", ("air", "missile"), "The Aerial Fleet Destroyed", "EMM"),
            ("ac_eew_news_ragno", ("gate", "command"), "Ragno Fortress", "EMM"),
            ("ac_eew_news_moloch", ("command", "security"), "The Moloch Desert", "EVA"),
            ("ac_eew_news_fort_norton", ("industry", "security"), "Fort Norton", "EMM"),
            ("ac_eew_news_liberation", ("peace", "civil"), "Gracemeria Liberated", "EMM"),
            ("ac_eew_news_coup", ("assembly", "security"), "The Coup in Estovakia", "EVA"),
            ("ac_eew_news_chandelier", ("science", "missile"), "The Chandelier Destroyed", "EVA"))
EVENT_ART = (("ac_eew_event_eva_declaration", ("command", "air"), "The Invasion of 30 August 2015", "EVA"),
             ("ac_eew_event_eva_ceasefire", ("peace", "assembly"), "The Ceasefire Agreement", "EVA"))
OWNER_ART = {
    "ac_eew_eva_war_footing": ("command", "air", "EVA"), "ac_eew_emm_war_footing": ("command", "shelter", "EMM"),
    "ac_eew_emm_capital_occupied": ("gate", "security", "EMM"), "ac_eew_emm_khesed_secured": ("gate", "peace", "EMM"),
    "ac_eew_eva_moloch_retreat": ("command", "security", "EVA"), "ac_eew_eva_coup": ("assembly", "security", "EVA"),
    "ac_eew_eva_restraint_kept": ("document", "peace", "EVA"), "ac_eew_eva_fought_on": ("command", "air", "EVA"),
    "ac_sp_aerial_fleet_initiative": ("air", "command", "EVA"), "ac_sp_chandelier_railgun": ("science", "missile", "EVA"),
}
PROJECT_ART = {
    "ac_sp_aerial_fleet": ("air", "command", "EVA", {"escort_doctrine": "radar"}),
    "ac_sp_chandelier": ("science", "missile", "EVA", {"firing_rules": "document"}),
}
