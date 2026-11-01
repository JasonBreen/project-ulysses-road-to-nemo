"""Authored national programmes; chronology is a gate, not an invented history.

Each row carries its own editorial subject and art direction. National effects
are bounded programme capacities, exclusive enduring policies and real service
rules, never a chain of free factories or interchangeable political-power gifts.
"""
from dataclasses import dataclass

COUNTRIES = {
    "SNS": {"name": "San Salvacion", "rows": 6, "axes": ["continuity", "protection", "dispatch"],
            "axis_titles": ["Continuity networks", "Civil protection", "Dispatch discipline"], "category": "Continuity and Civil Protection"},
    "AMB": {"name": "Amber", "rows": 5, "axes": ["development", "service", "transport"],
            "axis_titles": ["Development bargains", "Service capacity", "Transport coordination"], "category": "Development and Coalition Services"},
    "UGE": {"name": "Ugellas", "rows": 4, "axes": ["dispersal", "mobility", "reserve"],
            "axis_titles": ["Dispersal planning", "Emergency mobility", "Reserved capacity"], "category": "Dispersal and Emergency Mobility"},
    "DEL": {"name": "Delarus", "rows": 4, "axes": ["oversight", "command", "records"],
            "axis_titles": ["Civil oversight", "Command coordination", "Verified records"], "category": "Oversight and Command Obligations"},
}
PHASES = ("administration", "preparedness", "response", "settlement")

# suffix | title | narrative | primary subject | supporting subject
DATA = {
"SNS": [
"""
district_switchboards|Connect the District Switchboards|Each district can reach the capital, but too few can reach one another. A common contact book will turn separate local services into a continuity network without claiming ownership of their records.|communications|document
protection_inventory|Inventory Civil Protection|Shelter lists count doors while medical returns count beds. Comparing them will expose the journey between the two, where an emergency plan most often fails.|shelter|medical
dispatch_register|A Register of Dispatches|Instructions leave several offices with different signatures. A register will identify which instruction takes priority and who must explain a cancelled movement.|document|command
local_switchboards|Keep Local Switchboard Authority|Local operators know which line fails in bad weather and which official will answer after midnight. Keeping that discretion protects public confidence but requires a larger standing service.|communications|civil
central_dispatch|Build a Central Dispatch Office|A single dispatch office can move scarce crews quickly. Its authority improves coordination, while the districts give up some discretion and the office consumes political attention.|command|communications
service_crews|Put Service Crews on a Rota|The same technicians cannot maintain a telephone exchange and repair a pumping station at once. A published rota makes that competition visible before anyone calls it an emergency.|tools|medical
records_crosscheck|Cross-check Missing Records|Local registers contain duplicates as well as omissions. Cross-checking the files improves continuity work and makes later service authorisations less demanding on institutional capacity.|document|scales
water_desks|Water and Sanitation Desks|A functioning shelter is of little use without clean water and a maintenance contact. Small joint desks will keep those needs attached to the protection inventory.|medical|tools
route_permissions|Standardise Route Permissions|A driver carrying an urgent consignment should not negotiate a different permission at every district office. Standard forms preserve accountability while giving dispatchers a usable route.|bridge|document
night_contacts|Maintain the Night Contact Book|The official responsible for an overnight failure must be identifiable before the failure happens. Naming a duty contact protects the network from depending on a single familiar voice.|communications|assembly
volunteer_credentials|Credential Civil Volunteers|Experience and enthusiasm are different qualifications. A modest credential scheme will show which volunteers can handle first aid, communications or supervised shelter work.|civil|medical
depot_receipts|Receipts at Every Depot|A consignment is not delivered because it disappeared from the sending warehouse. Receiving signatures will give the dispatch service a record it can defend.|logistics|document
line_maintenance|Give the Lines a Maintenance Window|Routine inspection looks wasteful until a neglected connection is needed. Reserving maintenance windows makes the network more dependable at a continuing service cost.|tools|communications
protected_rosters|Protected Service Rosters|Civil protection needs people who cannot simply be reassigned when another office is short of staff. Protected rosters preserve that capacity and expose its opportunity cost.|civil|scales
allocation_board|An Accountable Allocation Board|An allocation board will hear competing requests for vehicles and technical crews. Its purpose is to leave an intelligible record of which service had to wait.|assembly|logistics
continuity_manual|Issue the Continuity Manual|The manual will describe how the offices work when the capital cannot answer. It turns the contact book into a continuing national service rather than an opening exercise.|document|communications
protection_charter|A Civil Protection Charter|Local authorities will know the minimum service they are expected to maintain and the assistance they may request. The charter strengthens protection while preserving the budget argument that pays for it.|shelter|assembly
dispatch_service|Establish the Dispatch Service|A permanent dispatch service can support later relief and reconstruction. Its standing obligations remain separate from any promise of military alignment.|logistics|command
""",
"""
district_exercises|District Continuity Exercises|Practice will begin with ordinary failures rather than a prediction of the next catastrophe. Districts must demonstrate how they keep essential instructions moving when an office closes.|training|communications
shelter_keys|Account for the Shelter Keys|A shelter plan must identify who opens the building and who checks it afterward. Recording those responsibilities is more useful than counting every public room as available capacity.|shelter|document
international_warning|Read the International Warning|The April 1996 warning changes the scale of contingency planning. Officials must explain what is known and what remains uncertain without treating a scientific forecast as a timetable for panic.|meteor|science
distributed_shelters|A Distributed Shelter Charter|Local protection sites reduce dependence on a few central locations. Maintaining them places a continuing burden on construction and inspection services.|shelter|civil
priority_corridors|Reserve Priority Corridors|Priority corridors concentrate the available dispatch capacity on movements the administration can sustain. Ordinary traffic bears some of the cost of keeping those routes ready.|bridge|logistics
scientific_liaison|A Scientific Liaison Rota|The warning must reach the people who maintain public instructions. A liaison rota keeps revisions attached to decisions instead of leaving a changing forecast on an unattended desk.|science|communications
family_enquiries|A Common Family Enquiry Form|People seek information through whichever office they can reach. A common form will make those enquiries usable across the continuity network while keeping access accountable.|refugees|document
medical_reserve_lists|Reconcile Medical Reserve Lists|Medical stores and trained staff need separate returns. The protection service will identify the gaps that a pile of unopened supplies cannot fill.|medical|logistics
forecast_revisions|Explain Revised Forecasts|A revision is not evidence that every earlier instruction was dishonest. Officials will explain what changes in the estimate require practical changes in local planning.|telescope|document
evacuation_contacts|Contacts before Evacuation Orders|An evacuation instruction must name a destination and a receiving office. Contact work preserves continuity even when movement cannot begin immediately.|communications|refugees
shelter_inspections|Shelter Inspection Intervals|Inspection teams will revisit sites rather than treating a completed form as permanent proof of readiness. Longer protection services become possible when those intervals are credible.|shelter|tools
stonehenge_access|Account for Stonehenge Access|The existing railgun complex creates civilian access, security and service questions. Recording those burdens does not grant the national programme authority to create, seize or operate the project.|radar|document
backup_registers|Keep Backup Registers Outside the Main Office|A second copy helps only if it can be found without the first office. The network will test retrieval and custody instead of merely duplicating paper.|document|security
water_reserve_checks|Check the Water Reserve Plan|Water handling requires transport, treatment and responsible staff. Rehearsing that chain makes the protection inventory a service the government can call upon.|medical|logistics
project_burden_review|Review the Project's Civil Burden|Technical importance does not make support work free. The administration will record the ordinary service capacity committed around Stonehenge without changing its owning project state.|scales|radar
mutual_contact_drill|A Mutual Contact Drill|Neighbouring desks will test the route by which an urgent question becomes an acknowledged answer. The drill improves local continuity regardless of a later diplomatic offer.|training|communications
civil_instruction_cards|Practical Civil Instruction Cards|Public instructions will identify actions people can actually take. Their value lies in the services prepared before the crisis, not in distributing a reassuring card afterward.|civil|shelter
preparedness_record|Close the Preparedness Record|The service will record the preparations completed before the July 1999 crisis. Later repairs remain useful, but cannot be backdated into that preparation record.|document|meteor
""",
"""
local_relay_plans|Keep Local Relays Working|The continuity network must remain useful when central offices are overloaded. Relay plans give local operators a defined responsibility instead of an unlimited emergency mandate.|communications|civil
receiving_points|Name the Receiving Points|Relief movements require somewhere to arrive and someone to take responsibility. The protection service will publish receiving points sized to actual local capacity.|shelter|logistics
after_the_crisis|The Service after Ulysses|The crisis makes it necessary to distinguish preparations from repairs. Current service work can protect people and restore routines without claiming an earlier state of readiness.|meteor|tools
civilian_continuity|Protect Civilian Continuity|Civil records, family enquiries and essential services receive a protected allocation. The policy supports confidence while reducing the attention available for military mobilisation.|civil|document
command_circuits|Reserve Command Circuits|The command chain receives dependable communications at a continuing civil cost. This helps organise existing forces and does not decide whether the continental war begins.|command|communications
repair_requests|Triage Repair Requests|The service will separate repairs that restore a useful route from requests that merely clear an embarrassing report. Dispatch discipline makes the distinction enforceable.|tools|scales
mobile_desks|Prepare Mobile Service Desks|A mobile desk carries authority and records, not simply a vehicle. Teams will practise operating away from their usual office without losing the chain of responsibility.|assembly|logistics
medical_receiving|Medical Receiving Agreements|Receiving facilities will state what they can accept before a convoy arrives. Clear limits protect medical staff and prevent dispatchers from counting the same spare capacity twice.|medical|document
coalition_contact|A Coalition Service Contact|The country can offer a bounded civil service to an eligible FCU partner. A contact does not guarantee acceptance, faction membership or military intervention.|diplomacy|logistics
dispersed_custody|Disperse the Custody of Records|Important records will have a route out of a threatened office. Dispersal preserves continuity without claiming that every threatened district can be defended.|document|refugees
shelter_turnover|Account for Shelter Turnover|Sites need cleaning, maintenance and a receiving plan before they can be used again. Accounting for turnover prevents a full site from remaining an imaginary reserve.|shelter|tools
stonehenge_liaison|Civil Liaison around Stonehenge|Civil service staff will keep an accountable contact with the authority actually responsible for the complex. The programme observes project ownership instead of setting a competing outcome.|radar|assembly
displaced_staff|Find the Displaced Staff|A service cannot be restored merely by reopening its building. The network will locate staff, verify surviving records and distinguish an absent official from an abandoned responsibility.|refugees|communications
protection_rotation|Rotate Protection Teams|Protecting exhausted staff is part of sustaining the service. A rotation retains a smaller dependable capacity instead of claiming that every team is continuously available.|civil|medical
dispatch_fallback|A Domestic Dispatch Fallback|A refused or interrupted partnership must not halt local service. Domestic dispatch arrangements retain useful work while leaving international rewards conditional on a valid agreement.|logistics|bridge
continuity_under_pressure|Continuity under Pressure|The contact network will record where it continued to function under disruption. Those findings support recovery without pretending that the national programme controlled the fighting.|communications|security
protection_service|A Sustainable Protection Service|Protection teams need an allocation that survives the immediate emergency. The country accepts that a useful service also requires a continuing claim on labour and materials.|shelter|scales
response_review|Review the Response Record|The review will distinguish local service, coalition assistance and the effects of occupation or disruption. It prepares an assessment rather than declaring a military outcome.|document|command
""",
"""
reopen_local_desks|Reopen the Local Desks|Recovery begins with a responsible official and a usable set of records. Reopening local desks gives the continuity network a place to receive unresolved cases.|assembly|document
protection_accounts|Audit Protection Accounts|The protection service will reconcile stores, damaged sites and unfinished obligations. An audit makes room for new work without turning reconstruction into a fresh emergency appropriation forever.|scales|shelter
settlement_instructions|Read the Actual Settlement|National instructions must follow the settlement that actually exists. The service will not assume victory, liberation or continued independence merely because the calendar has advanced.|document|peace
public_recovery_record|Publish the Recovery Record|A public record protects confidence and invites disputes over omissions. The administration accepts the political work of answering them.|document|civil
operational_record|Keep an Operational Record|A narrower operational record gives service managers room to move quickly. Its continuing administrative burden is the price of keeping that discretion accountable.|command|document
restoration_order|A Restoration Order That Can Be Delivered|A restoration order will identify its staff, receiving office and transport requirement. Dispatchers will refuse to count an instruction as completed merely because it was issued.|tools|logistics
missing_files|An Office for Missing Files|Unresolved cases deserve a responsible desk rather than a promise that all records survived. The office will reconstruct what it can and preserve the limits of the evidence.|document|refugees
local_repair_compacts|Local Protection Repair Compacts|Repair work will be divided into commitments local services can maintain. The compacts improve protection without creating a new national border or a project ownership claim.|tools|shelter
coalition_accounts|Reconcile Coalition Accounts|Assistance offered, accepted, refused and interrupted will be recorded separately. The accounting keeps useful domestic work from depending on an unearned diplomatic reward.|scales|diplomacy
district_return_rota|A District Return Rota|The return of service staff must be coordinated with the work awaiting them. A rota preserves continuity while avoiding the fiction that every displaced office reopens at full strength.|communications|refugees
protection_training|Train the Next Protection Rota|The service will retain the experience gained during the crisis and teach it to replacements. Institutional memory requires funded training rather than another commemorative announcement.|training|medical
archives_of_disruption|Preserve the Disruption Archive|The archive will record lost connections and displaced responsibilities as well as successes. It gives later recovery an honest starting point.|document|security
permanent_service_terms|Permanent Service Terms|Continuity staff will know the limits of their standing commitment. Clear terms support a lasting network and expose the opportunity cost of keeping it ready.|assembly|communications
protection_endowment|Maintain the Protection Allocation|The protection allocation becomes an ordinary continuing obligation. It supports limited recurring services instead of a one-time burst of emergency strength.|shelter|economy
postwar_contact_desks|Postwar Contact Desks|Neighbours can exchange practical service information where both remain eligible. The desks preserve a domestic function when a foreign partner is absent or unwilling.|diplomacy|document
local_control_recovery|Recover under Local Control|Where the country remains free to organise its own affairs, local institutions will carry the reconstruction record forward. Their authority does not erase the costs already incurred.|peace|assembly
external_conditions_recovery|Recover under External Conditions|Occupation, displacement or external supervision leaves practical constraints on the service. A usable recovery programme must acknowledge those constraints rather than wait for a preferred political outcome.|refugees|scales
network_assessment|Assess the Continuity Network|The final assessment records the actual settlement, chosen policies and surviving services. It remains available when the prerequisite work finishes after the nominal campaign window.|document|communications
"""],
"AMB": [
"""
development_register|Register Development Bargains|Public contracts reserve people and transport as well as money. A common register will show which development promises depend on the same small group of suppliers.|document|industry
service_inventory|Inventory Service Capacity|A ministerial promise is not a free wagon or a rested driver. Amber will account for the capacity that remains available after routine public work.|logistics|scales
transport_returns|Require Transport Returns|Operators will distinguish vehicles that exist from vehicles fit to carry a consignment. Honest returns make the coalition's later requests easier to evaluate.|rail|document
tendered_development|Tender the Development Programme|Competitive tenders make the price of ordinary development visible. Predictable civilian work improves construction while creating continuing political obligations to unsuccessful bidders.|industry|scales
service_guarantees|Guarantee Strategic Services|Standing guarantees give selected suppliers confidence to retain capacity. They support output at a continuing public-service burden rather than supplying free industrial expansion.|assembly|tools
common_timetable|Publish a Common Timetable|Civil and government traffic will work from one timetable. A shared schedule exposes bottlenecks before they are concealed by competing priority notices.|rail|document
contract_appeals|An Appeal against Contract Decisions|Suppliers need a route to challenge an allocation without stopping every shipment. An appeals procedure makes continuing development bargains more credible.|scales|assembly
spare_capacity|Count Only Spare Capacity|Capacity already promised to a hospital or a repair service cannot also be offered abroad. The service register will enforce that distinction.|logistics|medical
workshop_routes|Connect Workshops to Receiving Offices|A repaired item is useful when the receiving office knows how to collect it. Coordinated routing brings small workshops into the national service system.|tools|bridge
regional_bargains|Regional Development Bargains|Regional authorities will agree the maintenance obligations attached to new contracts. Their share of the bargain is a continuing task rather than an entry on opening day.|assembly|industry
service_authorisations|Issue Bounded Service Authorisations|Each service authorisation states its purpose, capacity and review date. Amber can then provide useful help without making an unlimited commitment.|document|logistics
transport_inspection|A Transport Inspection Rota|Inspection crews will work to a schedule that operators can plan around. The rota protects usable capacity at the cost of taking vehicles temporarily out of service.|tools|rail
development_compact|The Development Compact|The compact ties national priorities to commitments suppliers can actually deliver. It becomes the foundation for continuing development decisions.|industry|document
capacity_board|A Standing Capacity Board|A capacity board will arbitrate competing requests and publish the allocation. It must retain space for ordinary domestic services while evaluating foreign proposals.|assembly|scales
transport_service|A National Transport Service|The transport service coordinates existing operators and receiving offices. It does not nationalise their identity or create a new fleet by decree.|logistics|bridge
""",
"""
maintenance_bargains|Protect Maintenance in the Bargain|Routine maintenance will be written into public contracts. A development programme that consumes every workshop's time cannot also keep an emergency reserve.|tools|industry
contingency_slots|Reserve Contingency Slots|Operators will identify a small number of movements that can be reassigned in an emergency. Reserving those slots has a domestic opportunity cost.|rail|scales
read_the_warning|Bring the Warning to the Board|The international warning requires the capacity board to revisit its assumptions. A forecast changes planning priorities without making transport requirements disappear.|meteor|assembly
commercial_capacity|Protect Commercial Capacity|Civil trade keeps operators and workshops functioning between public calls. Protecting it supports construction while limiting the speed of a later military mobilisation.|economy|rail
government_slots|Reserve Government Service Slots|Reserved service slots improve the delivery of public and defence consignments. Holding them ready imposes a continuing burden on ordinary economic activity.|logistics|command
forecast_contacts|Keep Forecast Contacts Open|The board needs an accountable contact for changes in the warning. Operators should receive a usable instruction rather than several uncoordinated scientific summaries.|science|communications
contract_scenarios|Test the Contracts against Disruption|The board will ask which contracts survive the loss of a depot or a receiving office. Planning around a real interruption protects development bargains from becoming paper reserves.|document|security
receiving_windows|Give Receiving Offices Time Windows|A warehouse cannot accept every urgent consignment at once. Time windows preserve limited service capacity and make emergency requests more credible.|logistics|document
joint_planning_table|A Joint Planning Table|Civil protection and transport officers will compare the resources they expect to use. Their agreement will be bounded by the same national capacity record.|assembly|shelter
supplier_reserves|Supplier Reserve Obligations|Suppliers accepting a standing contract will identify the replacement parts they can hold. The obligation belongs in the bargain instead of being counted as a free national stockpile.|tools|scales
capacity_exercises|Exercise the Spare Capacity|A reserve is useful only if it can be called upon without collapsing routine service. Exercises will test that margin before it is offered to a partner.|training|logistics
freight_contingencies|Freight Contingency Instructions|Dispatchers will receive fallback instructions for common disruptions. Their purpose is to keep a limited service working, not to promise movement through every blocked route.|rail|bridge
development_review|Review the Protected Programme|The review records which development bargains can continue alongside civil preparation. It protects useful work without backdating later repairs into preparedness.|industry|document
service_reserve|Maintain the Service Reserve|The reserve will be renewed through a continuing allocation. Its capacity can be spent on a domestic task or, where eligible, a bounded coalition service.|logistics|economy
warning_record|Record Preparations before the Crisis|Amber will close its preparation record at the crisis boundary. Work begun afterward belongs to response and recovery, even when it uses the same personnel.|document|meteor
""",
"""
supplier_continuity|Keep Suppliers Accountable|A disrupted contractor still needs a record of what was delivered and what remains owed. Accountable continuity protects later development work.|tools|document
service_triage|Triage Service Requests|The capacity board will distinguish an urgent request from an unlimited claim on the reserve. Triage keeps Amber's available slots finite.|scales|logistics
crisis_timetable|A Timetable after the Crisis|The crisis changes routes and demands. The transport service must issue a usable current timetable instead of pretending its earlier assumptions remain intact.|meteor|rail
civil_freight|Give Civil Freight a Protected Share|A protected civil share sustains public confidence and ordinary supply. Military planners must work around the space it occupies.|civil|logistics
military_timetables|Adopt Military Timetables|Defence consignments receive a larger protected share of the schedule. The gain in military movement comes at a continuing cost to civilian construction.|command|rail
relief_receipts|Receipts for Relief Movements|Relief traffic will retain the same custody record as other consignments. An urgent label is not permission to stop asking whether the delivery arrived.|refugees|document
contractor_failure|Plan for Contractor Failure|A failed supplier should trigger a defined reallocation process. The country will preserve the useful part of a development bargain instead of treating every failure as a new national emergency.|industry|scales
coalition_capacity|Offer a Bounded Coalition Service|Amber can commit one recorded service slot to an eligible FCU partner. The offer leaves the recipient free to refuse and does not change faction ownership.|diplomacy|logistics
domestic_reservations|Keep Domestic Reservations|An external request cannot spend capacity already assigned to domestic services. The board will preserve that constraint even when cooperation is politically attractive.|assembly|civil
workshop_recovery|Restore Workshop Routes|Repair work will be routed to receiving offices that can use it. Restoring that chain supports development without creating new factories by decree.|tools|bridge
service_replacement|Replace an Interrupted Service|A refused or invalid foreign agreement leaves a real domestic task available. Amber will redirect the slot rather than wait indefinitely for a preferred partner.|logistics|document
transport_rotation|Rotate the Transport Crews|Overworked crews make an impressive schedule unreliable. Rotation protects a smaller service capacity that can actually be sustained.|rail|training
continuity_contracts|Continuity Clauses in Public Contracts|Contracts will state what happens when a receiving office, route or supplier is lost. Clear clauses reduce disputes over the development programme's remaining obligations.|document|industry
standing_service|A Standing Service Capability|The board will retain the ability to authorise a small continuing service. Every renewal still has to pay its administrative and economic cost.|logistics|scales
response_accounts|Close the Response Accounts|The response record separates accepted services, refusals and domestic reallocations. It provides a defensible basis for recovery under the actual settlement.|scales|peace
""",
"""
review_concessions|Review Development Concessions|Recovery gives the government an opportunity to inspect promises made under pressure. The review preserves valid obligations while exposing those that can no longer be delivered.|industry|document
release_service_slots|Release Emergency Service Slots|The reserve must distinguish continuing obligations from slots held for an emergency that has ended. Releasing one commitment makes room for another without inventing new capacity.|logistics|scales
settlement_routes|Routes under the Actual Settlement|The transport service will plan around the political and military conditions that actually remain. It cannot restore a lost route by publishing the old timetable.|bridge|peace
public_concession_review|Publish the Concession Review|Public scrutiny improves the quality of later development work. The government accepts the political effort required to defend and amend the record.|document|science
long_service_bonds|Negotiate Long Service Bonds|Longer service bargains support productive continuity. Their predictable claim on public resources remains a continuing cost.|economy|industry
reconstruction_timetable|A Reconstruction Timetable|Repair tasks will receive realistic delivery windows. Sequencing work preserves transport coordination when several districts want to be first.|rail|tools
supplier_arbitration|Arbitrate the Unfinished Bargains|An unfinished contract needs a responsible decision, not permanent emergency status. Arbitration protects the development programme from accumulating incompatible claims.|scales|assembly
service_cost_review|Review the Cost of Standing Capacity|The capacity board will show which standing services remain useful and what they prevent the country from doing elsewhere. Renewal becomes a deliberate choice.|logistics|economy
coalition_reconciliation|Reconcile Coalition Services|Accepted, refused and interrupted offers will be recorded separately. A previous political promise cannot substitute for a valid present partner.|diplomacy|document
maintain_local_bargains|Maintain Local Development Bargains|Local suppliers and authorities retain obligations after the national emergency ends. The country will support work that remains deliverable under those terms.|industry|tools
domestic_service_terms|Domestic Service Terms after Refusal|A refusal is an outcome, not a broken national programme. Domestic service terms keep the reserved capacity useful without a diplomatic reward.|civil|logistics
postwar_transport|Retain Postwar Transport Coordination|Coordination remains valuable after the wartime timetable is retired. The service will keep its contacts and inspection work at an ordinary continuing cost.|rail|communications
local_control_recovery|Settle the Bargains under Local Control|Where national institutions retain control, they will carry the development record into ordinary government. The settlement does not make earlier obligations disappear.|peace|assembly
external_conditions_recovery|Settle the Bargains under Constraints|External supervision, displacement or defeat changes what can be promised. The board will retain a useful domestic service within those conditions.|refugees|scales
service_assessment|Assess the Development and Service Bargain|The assessment records the chosen national policy, delivered capacity and actual settlement. It can conclude after the calendar window if the required work finishes late.|document|logistics
"""],
"UGE": [
"""
depot_register|Register the Dispersed Depots|Ugellas needs a record of which stores can be reached and who controls the keys. A depot on a list is not automatically a usable emergency reserve.|logistics|document
mobility_return|A Return of Available Mobility|Drivers, vehicles and receiving points will be reported separately. This prevents the administration from reserving the same transport for several incompatible tasks.|bridge|scales
reserve_space|Count the Remaining Reserve Space|A small country cannot maintain an unlimited collection of special reserves. The administration will begin with a finite number of service slots.|assembly|logistics
distributed_stores|Keep Stores Dispersed|Dispersal makes the national service less dependent on a single depot. Maintaining several sites consumes construction and inspection capacity.|logistics|security
central_mobile_pool|Create a Central Mobile Pool|A central pool improves the movement of existing forces and services. It requires continuing administrative attention and leaves fewer locally controlled assets.|command|bridge
reserve_rota|A Rota for Reserve Custody|Custody must pass to a named replacement when an official is absent. A rota turns reserve space into capacity that can actually be authorised.|document|assembly
depot_inspections|Inspect the Small Depots|Inspection will record the state of each depot rather than assume every dispersed site is ready. The work improves dispersal planning at a continuing service cost.|tools|logistics
receiving_contacts|Name the Mobility Receiving Contacts|A movement needs a destination able to accept its load. Named contacts make limited transport more useful than a longer list of vehicles.|communications|bridge
slot_authority|An Authority for Service Slots|Every new lease of reserve capacity will have an end date. The authority prevents temporary emergency assignments from becoming invisible permanent commitments.|assembly|scales
dispersal_service|A Standing Dispersal Service|The service will maintain the smallest network it can sustain. It supports later emergency allocations without creating a national stockpile from nothing.|logistics|civil
mobility_desk|An Emergency Mobility Desk|The desk will coordinate a limited pool of transport with real receiving offices. Routine movement remains part of the same national bargain.|bridge|document
reserve_manual|Issue the Reserve Manual|The manual explains how a slot is assigned, released and reviewed. A finite reserve is more credible than an open-ended emergency promise.|document|logistics
""",
"""
depot_contingencies|Depot Contingency Instructions|Each depot needs an instruction for the loss of its usual route. Dispersal planning will account for that interruption before it is called a catastrophe.|security|logistics
movement_exercises|Exercise the Movement Chain|An exercise will follow a consignment through its receiving office. The result improves mobility without holding every vehicle permanently mobilised.|training|bridge
read_the_forecast|Read the International Forecast|The international warning gives the reserve authority a new planning problem. Officials must explain the limits of available space as carefully as the warning itself.|meteor|document
local_reserve_space|Protect Local Reserve Space|Local protection retains a claim on the finite reserve. That resilience occupies resources which cannot also serve a military timetable.|shelter|logistics
route_contingencies|Fund Route Contingencies|A larger share of capacity goes to movement planning and alternative dispatch. The service accepts less planning attention for other military tasks.|bridge|command
forecast_dispatch|A Forecast Dispatch Contact|A changing estimate must reach the officials who allocate slots. A named contact prevents the reserve authority from acting on an abandoned version of the warning.|science|communications
protected_storage|Define Protected Storage Terms|Protected storage requires inspection and a receiving plan. The country will distinguish a funded reserve from goods merely left in an inconvenient building.|logistics|scales
local_drivers|A Local Driver Contact Rota|The mobility desk will maintain contacts with people who can carry out an authorised movement. A driver cannot be counted twice because two offices know the same name.|communications|training
service_slot_review|Review the Service Slot Limit|The authority will increase its usable slots only where record keeping and custody support them. Reserve capacity remains bounded even as the national programme matures.|assembly|document
dispersal_drill|A Dispersal Drill|The drill checks whether a small site can receive work when the main depot is unavailable. It is preparation only when completed before the crisis boundary.|training|logistics
mobility_instructions|Practical Mobility Instructions|Receiving offices will publish instructions they can actually honour. A useful route is one whose staff and capacity agree with the paperwork.|bridge|document
preparedness_register|Close the Reserve Preparation Register|The register records work completed before the crisis. Later repairs can restore mobility, but cannot create an earlier state of readiness.|document|meteor
""",
"""
dispersed_accounts|Reconcile Dispersed Accounts|The reserve authority must learn which sites and records still function. Reconciliation keeps the dispersal service useful under current conditions.|document|logistics
emergency_movement|Authorise Emergency Movement|A movement lease occupies one finite service slot. The country will gain a temporary capability while accepting its administrative and economic cost.|bridge|command
after_the_warning|Mobility after the Crisis|The crisis tests routes and receiving offices rather than the number of plans printed. Current mobility work belongs to response, not retrospective preparation.|meteor|bridge
civilian_convoys|Protect Civilian Convoy Allocations|Civilian services retain a protected share of limited movement capacity. The policy supports public confidence while leaving less attention for military organisation.|civil|logistics
defence_allocations|Reserve Defence Allocations|The existing forces receive a more reliable movement allocation. Holding that capacity ready imposes a continuing public-service burden.|command|logistics
receiving_repairs|Repair the Receiving Chain|The service will restore the offices and instructions that make a delivery usable. Mobility does not recover simply because a route is open on a map.|tools|bridge
depot_recovery|Recover a Dispersed Depot|Restoring a depot requires custody and inspection as well as a repaired roof. The authority will bring it back into the finite reserve system.|logistics|tools
coalition_mobility|Offer a Bounded Mobility Service|Ugellas may offer one practical service to an eligible FCU partner. A refusal leaves the country free to use its capacity at home.|diplomacy|bridge
slot_rotation|Rotate the Occupied Slots|Service leases must end or be deliberately renewed. Rotation stops a temporary assignment from permanently consuming reserve capacity.|scales|logistics
disruption_record|Record the Disrupted Sites|The country will retain a record of what failed and what survived. That evidence supports later recovery without claiming authority over the war's result.|document|security
domestic_mobility|A Domestic Mobility Fallback|An invalid or refused partnership does not remove local needs. The desk will keep a useful service available within the national programme.|bridge|civil
response_register|The Mobility Response Register|The register separates useful service from plans that could not be delivered. It prepares a recovery assessment under the actual settlement.|document|peace
""",
"""
reopen_depots|Reopen the Dispersed Depots|Recovery will return sites to accountable custody instead of declaring the whole reserve restored. Each useful depot belongs in the current service record.|tools|logistics
mobility_recovery|Restore Emergency Mobility|The movement chain will be repaired around the receiving offices that actually remain. Existing transport and ordinary supply still determine what can move.|bridge|tools
settlement_inventory|Inventory the Actual Settlement|The reserve authority must work within the country and obligations that survived. It cannot assume continued independence or a preferred military result.|document|peace
distributed_repair|Distribute the Repair Programme|Local repair work improves construction while imposing a continuing administrative burden. Its purpose is to retain a useful dispersal service.|tools|civil
readiness_transport|Retain a Readiness Transport Reserve|A protected transport reserve supports movement of the existing forces. Its ordinary public cost remains part of the national bargain.|command|bridge
review_slot_costs|Review the Cost of Each Slot|A service slot has a cost even while unused. The authority will publish the work displaced by keeping each commitment ready.|scales|logistics
depot_terms|Permanent Depot Service Terms|Custodians and receiving offices will know the minimum standard they must maintain. Clear terms make dispersed capacity more sustainable than emergency improvisation.|logistics|document
mobility_training|Train the Mobility Replacements|Replacement staff need the contacts and procedures that earlier crews learned under pressure. Training preserves a limited capability instead of promising unlimited movement.|training|bridge
coalition_receipts|Reconcile the Coalition Receipts|Offers, refusals and completed services will remain distinct in the record. A diplomatic promise cannot be counted as delivered mobility.|diplomacy|document
local_control_recovery|Manage the Reserve under Local Control|Where national institutions retain control, the reserve authority can adopt its own recovery terms. The finite slot system remains a safeguard against overcommitment.|peace|assembly
external_conditions_recovery|Manage the Reserve under Constraints|Displacement, external conditions or defeat changes the available service. The country will retain useful domestic mobility without waiting for an ideal settlement.|refugees|bridge
mobility_assessment|Assess the Reserve and Mobility Service|The assessment records the actual settlement and the services that can still be sustained. It remains reachable when recovery work finishes after the calendar window.|document|logistics
"""],
"DEL": [
"""
requisition_register|Register Command Requisitions|A requisition becomes an obligation when someone is expected to deliver it. Delarus will begin with a record of which office accepted each demand.|document|command
inspection_office|An Office for Administrative Inspection|Inspection gives civil officials a means to challenge incompatible claims. Its purpose is accountable delivery rather than an invented change of government.|scales|assembly
record_returns|Require the Receiving Record|A sending signature cannot prove a delivery. Receiving records give the administration a basis for settling obligations and identifying missing work.|document|logistics
civil_audit|Protect Civil Audit Authority|Civil inspectors retain the right to examine command requisitions. The policy supports confidence while consuming political and administrative attention.|scales|civil
command_delegation|Delegate Routine Command Authority|Command offices gain discretion to act quickly. Planning improves at a cost to confidence in the civil administration's ability to examine every request.|command|document
casework_rota|Put the Casework on a Rota|An unresolved demand needs an official responsible for answering it. A rota prevents the inspection office from relying on one overworked clerk.|assembly|communications
verification_rules|Rules for Verifying a Requisition|The inspection office will separate an urgent demand from a documented commitment. Better verification makes later administrative work less demanding on institutional capacity.|document|scales
command_accounts|An Account of Standing Command Obligations|The command chain will list what it expects public services to provide. An honest account exposes costs that cannot be paid through another priority stamp.|command|economy
receiving_standards|Common Receiving Standards|Receiving offices will state what evidence closes a case. The standard keeps delivery records from changing whenever a particular obligation becomes awkward.|logistics|document
administrative_compact|The Administrative Compact|The selected balance between civil oversight and command discretion becomes a continuing national policy. It leaves the existing leader and institutions responsible for its consequences.|assembly|scales
obligation_desk|A Desk for Competing Obligations|The desk will arbitrate demands made on the same service capacity. Recording a refusal is more accountable than pretending both commitments were delivered.|scales|command
records_service|Establish the Records Service|A permanent records service preserves the evidence needed to review an emergency. It does not replace command authority with an unlimited inspection mandate.|document|assembly
""",
"""
contingency_dockets|Prepare Contingency Dockets|The administration will identify which standing instructions survive a disruption. Preparing a docket makes it possible to review an emergency demand without starting from nothing.|document|security
service_obligations|Publish Service Obligations|Public services will know which command demands they are expected to meet. Clear terms prevent routine capacity from becoming an invisible emergency reserve.|assembly|command
warning_docket|Open the International Warning Docket|The April 1996 warning requires a new administrative record. The government must distinguish practical preparation from instructions that merely acknowledge the forecast.|meteor|document
published_obligations|Publish the Obligation Schedule|A public schedule makes costs and refusals visible. It improves the use of ordinary resources while requiring continuing political work to defend the record.|document|economy
military_reservations|Protect Military Reservations|The command chain receives a protected share of available attention. The policy supports war readiness while leaving less capacity for research and civil review.|command|scales
scientific_returns|Receive Scientific Returns Responsibly|Scientific advice needs a receiving office able to revise instructions. Delarus will record the forecast without turning uncertainty into an excuse for contradictory demands.|science|document
inspection_exercises|Exercise the Inspection Chain|Inspectors will follow a simulated urgent requisition from signature to receiving office. The exercise protects useful oversight rather than creating a second command system.|training|scales
reserve_commitments|Account for Reserve Commitments|A reserve already promised to one service is not available to every other office. The obligation desk will record that constraint before the crisis.|logistics|document
records_duplicates|Keep Accountable Record Duplicates|Duplicate files require custody and a retrieval procedure. The service will test those details instead of claiming that another copy guarantees continuity.|document|communications
verified_preparation|Verify Preparations before the Boundary|Inspection will record what was actually prepared before the crisis. Later emergency work will be judged on its current value rather than backdated into this account.|scales|meteor
obligation_review|Review the Protected Obligations|Protected commitments need a review date as well as an original signature. The desk will keep the programme sustainable by confronting commitments that cannot all be honoured.|command|document
preparedness_accounts|Close the Preparedness Accounts|The account distinguishes completed preparation from an unfulfilled instruction. That distinction remains useful even when the later outcome is different from the cabinet's expectations.|document|scales
""",
"""
emergency_casework|An Emergency Casework Rota|Demand rises precisely when familiar officials are unavailable. A rota preserves oversight without pretending every ordinary procedure can continue at full speed.|assembly|communications
command_requests|Review the Command Requests|Commanders need a usable answer, including a refusal where capacity is already committed. Reviewing requests protects the obligations the country can still deliver.|command|scales
crisis_accounts|Accounts after the Crisis|The administration will compare what was requested with what actually arrived. The crisis does not erase the need for a receiving record.|meteor|document
inspect_requisitions|Inspect Emergency Requisitions|Inspection supports organisation by finding incompatible demands. The gain in dependable administration comes at a cost to immediate planning speed.|scales|command
emergency_warrants|Authorise Emergency Warrants|A warrant gives the command chain room to act before every docket is complete. The country accepts a continuing public-service burden to support that speed.|command|document
records_in_motion|Keep the Records Moving|The service will plan for the movement of files and responsible staff. Losing an office must not automatically erase the obligations it accepted.|document|logistics
requisition_audits|Audit Requisitions under Pressure|A sampled audit can identify the demand that consumed capacity promised elsewhere. It improves oversight without claiming that inspection itself delivers the missing supplies.|scales|logistics
coalition_commitment|Offer a Defined Coalition Commitment|Delarus may offer an eligible FCU partner a bounded administrative service. The offer is not a blank cheque, and a refusal leaves domestic work available.|diplomacy|document
receiving_backlog|Separate the Receiving Backlog|The records service will distinguish unfinished delivery from paperwork that can be closed. That distinction makes a finite obligation review possible.|document|assembly
displaced_dockets|Preserve the Displaced Dockets|Disrupted offices will retain a route for reconstructing their files. The records programme can support later recovery without declaring what happened on the battlefield.|refugees|document
domestic_review|A Domestic Review after Refusal|A foreign refusal does not remove the need for accountable domestic work. The inspection office will continue under its own limited mandate.|scales|civil
response_docket|Close the Emergency Response Docket|The docket records accepted commitments, interrupted work and the chosen oversight policy. It prepares the country for a recovery assessment under the actual settlement.|document|peace
""",
"""
reopen_inspection|Reopen the Inspection Office|Recovery begins by finding responsible officials and usable evidence. Reopening the office does not imply that every emergency decision can be reconstructed.|assembly|document
obligation_settlement|Settle the Outstanding Obligations|Each outstanding demand requires an answer under the conditions that now exist. The desk will distinguish a valid continuing commitment from an expired emergency claim.|scales|command
actual_terms|Record the Actual Settlement Terms|The records service must describe the country and obligations that survived. It will not assume victory, independence or an unaltered command chain merely because a date has passed.|document|peace
civilian_oversight|Retain Civilian Oversight|A protected civilian review supports confidence after the emergency. It places a continuing political burden on institutions expected to explain difficult decisions.|scales|civil
joint_inspection|Adopt Joint Inspection Terms|Civil and command inspectors will work from a common receiving record. Better organisation retains an ordinary service cost instead of becoming a free postwar bonus.|command|document
casework_recovery|Recover the Missing Casework|Staff will reconstruct the chain of responsibility where evidence permits. An honest gap remains preferable to a fabricated record of completed delivery.|document|refugees
standing_inspection|Standing Inspection Intervals|The office will inspect continuing commitments on a schedule. Regular review keeps oversight useful after the emergency warrant is retired.|scales|training
command_service_terms|Publish Command Service Terms|Command offices will state the service they require and the capacity they accept is unavailable. Clear terms preserve a useful command relationship under either policy.|command|assembly
coalition_dockets|Reconcile the Coalition Dockets|Offers, refusals and interrupted assistance will have separate entries. A past diplomatic promise cannot be converted into an unearned current reward.|diplomacy|document
local_control_recovery|Settle the Record under Local Control|Where national institutions retain authority, they will carry the inspected record into ordinary government. Earlier costs remain part of that record.|peace|assembly
external_conditions_recovery|Settle the Record under Constraints|Defeat, displacement or external conditions may limit what the administration can promise. A useful inspection programme must work within those limits.|refugees|scales
oversight_assessment|Assess Oversight and Command Obligations|The assessment records the actual settlement and the balance chosen between inspection and command discretion. It remains available after the calendar window when the required work finishes late.|document|command
"""],
}


@dataclass(frozen=True)
class Focus:
    tag: str
    phase: str
    row: int
    lane: int
    suffix: str
    title: str
    desc: str
    primary: str
    secondary: str

    @property
    def id(self):
        return f"{self.tag}_up_{self.suffix}"

    @property
    def x(self):
        return 2 + self.lane * 5

    @property
    def y(self):
        index = PHASES.index(self.phase)
        value = index * (COUNTRIES[self.tag]["rows"] + 2) + self.row
        return value + (1 if self.phase == "settlement" and self.row == COUNTRIES[self.tag]["rows"] - 1 and self.lane == 2 else 0)

    @property
    def cost(self):
        # Enduring policy alternatives and completed national commitments are
        # major work. The supporting rota between policy alternatives is not.
        return 10 if (self.row == 1 and self.lane < 2) or self.row == COUNTRIES[self.tag]["rows"] - 1 else 5


FOCUSES = []
for tag, phases in DATA.items():
    for phase, raw in zip(PHASES, phases):
        rows = [line.split("|") for line in raw.strip().splitlines() if line.strip()]
        if len(rows) != COUNTRIES[tag]["rows"] * 3:
            raise ValueError(f"Wrong focus count in {tag}/{phase}: {len(rows)}")
        for index, (suffix, title, desc, primary, secondary) in enumerate(rows):
            FOCUSES.append(Focus(tag, phase, index // 3, index % 3, suffix, title, desc, primary, secondary))
if len(FOCUSES) != 228 or len({row.id for row in FOCUSES}) != 228:
    raise ValueError("The four country programmes require 228 distinct focuses")


# Per-country alternatives by act. Values have continuing countervailing costs.
POLICY_MODIFIERS = {
"SNS": [("stability_factor = 0.02\nconsumer_goods_factor = 0.01", "planning_speed = 0.02\npolitical_power_factor = -0.03"),
        ("surrender_limit = 0.03\nproduction_speed_buildings_factor = -0.02", "supply_consumption_factor = -0.03\nconsumer_goods_factor = 0.015"),
        ("stability_factor = 0.03\nwar_support_factor = -0.02", "planning_speed = 0.04\nconsumer_goods_factor = 0.02"),
        ("stability_factor = 0.02\npolitical_power_factor = -0.02", "army_org_factor = 0.02\nconsumer_goods_factor = 0.01")],
"AMB": [("production_speed_buildings_factor = 0.03\npolitical_power_factor = -0.03", "industrial_capacity_factory = 0.02\nconsumer_goods_factor = 0.015"),
        ("production_speed_buildings_factor = 0.025\nmobilization_speed = -0.05", "supply_consumption_factor = -0.03\nconsumer_goods_factor = 0.02"),
        ("stability_factor = 0.025\nplanning_speed = -0.02", "army_speed_factor = 0.03\nproduction_speed_buildings_factor = -0.02"),
        ("research_speed_factor = 0.015\npolitical_power_factor = -0.03", "industrial_capacity_factory = 0.02\nconsumer_goods_factor = 0.02")],
"UGE": [("supply_consumption_factor = -0.03\nproduction_speed_buildings_factor = -0.02", "army_speed_factor = 0.03\npolitical_power_factor = -0.04"),
        ("surrender_limit = 0.025\nconsumer_goods_factor = 0.015", "army_speed_factor = 0.03\nplanning_speed = -0.025"),
        ("stability_factor = 0.03\narmy_org_factor = -0.01", "army_org_factor = 0.03\nconsumer_goods_factor = 0.02"),
        ("production_speed_buildings_factor = 0.025\npolitical_power_factor = -0.02", "army_speed_factor = 0.025\nconsumer_goods_factor = 0.01")],
"DEL": [("stability_factor = 0.025\npolitical_power_factor = -0.03", "planning_speed = 0.04\nstability_factor = -0.015"),
        ("consumer_goods_factor = -0.01\npolitical_power_factor = -0.04", "war_support_factor = 0.03\nresearch_speed_factor = -0.01"),
        ("army_org_factor = 0.02\nplanning_speed = -0.02", "planning_speed = 0.05\nconsumer_goods_factor = 0.02"),
        ("stability_factor = 0.03\npolitical_power_factor = -0.03", "army_org_factor = 0.025\nconsumer_goods_factor = 0.015")],
}
