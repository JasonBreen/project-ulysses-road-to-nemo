"""Curated operational uses for 117 formerly index-only focus capabilities.

Each named capability is nonfungible: its completion enables a specific part of
one paid inspection/service scope. Stocks are earned by the existing national
systems. The scope's benefits always have a continuing opportunity cost.
"""
from dataclasses import dataclass
from content import FOCUSES


@dataclass(frozen=True)
class Scope:
    tag: str
    suffix: str
    title: str
    resource: str
    requirements: tuple
    modifier: str
    purpose: str
    primary: str
    secondary: str

    @property
    def id(self): return self.tag + "_up_scope_" + self.suffix


DATA = {
"SNS": [
 ("dispatch_chain", "Inspect the Dispatch Chain", "contacts", "dispatch_register route_permissions depot_receipts allocation_board",
  "supply_consumption_factor = -0.02\npolitical_power_factor = -0.03", "Check signed instructions, route permission, receipt and the allocation appeal together. The complete chain supports dependable existing supply while reserving political attention.", "logistics", "document"),
 ("relay_maintenance", "Staff a Tested Relay Network", "contacts", "service_crews night_contacts line_maintenance local_relay_plans",
  "planning_speed = 0.025\nproduction_speed_buildings_factor = -0.02", "Assign the trained rota, night contact, maintenance window and local fallback to one relay service. Coordination improves while those technicians are unavailable for ordinary construction.", "communications", "tools"),
 ("safe_water", "Inspect Shelter Water Turnover", "protection", "water_desks water_reserve_checks receiving_points shelter_turnover",
  "stability_factor = 0.02\nconsumer_goods_factor = 0.0125", "Verify treatment, reserve transport, receiving responsibility and cleaning between shelter occupants. Confidence improves at a continuing civilian allocation cost.", "medical", "shelter"),
 ("volunteer_replacements", "Credential a Replacement Protection Rota", "protection", "volunteer_credentials protected_rosters protection_rotation protection_training",
  "experience_gain_army_factor = 0.025\nwar_support_factor = -0.01", "Bring credentials, protected staffing, rest intervals and replacement instruction into one trained civil rota. Organisational learning improves while civilian priorities restrain mobilisation enthusiasm.", "training", "civil"),
 ("family_custody", "Open an Accountable Family Contact Service", "contacts", "district_exercises family_enquiries evacuation_contacts backup_registers",
  "surrender_limit = 0.02\npolitical_power_factor = -0.03", "A practised district, common enquiry, receiving contact and retrievable backup give families a dependable service during disruption. Keeping that responsibility open consumes political attention.", "refugees", "document"),
 ("clinic_reserve", "Inspect a Staffed Medical Receiving Reserve", "protection", "shelter_keys medical_reserve_lists shelter_inspections",
  "army_org_factor = 0.02\nconsumer_goods_factor = 0.015", "Match an accessible site, reconciled medical staff and a current inspection. The temporary reserve supports existing personnel; it neither creates supplies nor counts an unopened building as a hospital.", "medical", "document"),
 ("warning_liaison", "Assign a Civil Scientific Liaison", "contacts", "scientific_liaison forecast_revisions stonehenge_access",
  "research_speed_factor = 0.02\nplanning_speed = -0.015", "Combine a scientific receiving rota, revised public instructions and accountable complex access. Technical learning gains attention that otherwise supports military planning. The project owner remains unchanged.", "science", "radar"),
 ("mobile_triage", "Dispatch an Accountable Mobile Service Desk", "contacts", "after_the_crisis repair_requests mobile_desks dispersed_custody displaced_staff",
  "supply_consumption_factor = -0.025\nindustrial_capacity_factory = -0.01", "Current repair priorities, mobile authority, surviving custody and located staff let a desk travel with useful records. Movement becomes more dependable while workshops support its operation.", "assembly", "logistics"),
 ("settlement_routes", "Reconcile Domestic and Partner Dispatches", "contacts", "dispatch_fallback settlement_instructions restoration_order coalition_accounts postwar_contact_desks",
  "army_speed_factor = 0.02\nproduction_speed_buildings_factor = -0.025", "Follow the actual settlement, deliverable orders and separate coalition accounts. A domestic route remains useful after refusal or an invalid partner; it grants no diplomatic acceptance reward.", "bridge", "diplomacy"),
 ("lasting_custody", "Staff the Permanent Recovery Record", "protection", "missing_files local_repair_compacts district_return_rota archives_of_disruption permanent_service_terms protection_endowment",
  "stability_factor = 0.015\nresearch_speed_factor = 0.01\nconsumer_goods_factor = 0.015", "Join unresolved files, local repair terms, returning staff and the disruption archive to a funded permanent service. The inspected record supports confidence and learning at an ordinary civilian cost.", "document", "scales"),
],
"AMB": [
 ("supplier_links", "Allocate an Inspected Workshop Receiving Slot", "slots", "development_register common_timetable workshop_routes regional_bargains",
  "production_factory_efficiency_gain_factor = 0.04\nconsumer_goods_factor = 0.015", "Match the supplier obligation, common timetable, workshop route and regional maintenance bargain before committing one funded slot. Existing workshops learn more efficiently while civilian capacity is reserved.", "industry", "bridge"),
 ("receiving_windows", "Reserve a Verified Receiving Window", "slots", "service_authorisations transport_inspection contingency_slots receiving_windows",
  "supply_consumption_factor = -0.025\nindustrial_capacity_factory = -0.015", "Combine the bounded authority, inspected vehicle, contingency slot and receiving window. Dependable delivery uses capacity that cannot also support workshop output.", "logistics", "scales"),
 ("workshop_reserve", "Exercise a Supplier Replacement Reserve", "slots", "maintenance_bargains contract_scenarios supplier_reserves capacity_exercises",
  "production_factory_max_efficiency_factor = 0.02\nproduction_speed_buildings_factor = -0.025", "Test protected maintenance and replacement obligations against a disrupted contract. A verified reserve improves sustained production at a construction opportunity cost; no physical spare parts are granted.", "tools", "industry"),
 ("forecast_dispatch", "Issue a Joint Contingency Dispatch", "slots", "forecast_contacts joint_planning_table freight_contingencies crisis_timetable",
  "planning_speed = 0.03\npolitical_power_factor = -0.03", "A current forecast contact, joint planning record and freight fallback support a deliverable timetable. The allocation improves coordination while using political attention.", "rail", "communications"),
 ("receiving_triage", "Inspect Contested Relief Receipts", "slots", "supplier_continuity service_triage relief_receipts contractor_failure",
  "stability_factor = 0.02\narmy_org_factor = -0.01", "Reconcile surviving suppliers, prioritised requests, receiving signatures and a failed contractor. Civil confidence gains a protected allocation that is unavailable for immediate military organisation.", "medical", "document"),
 ("domestic_redeployment", "Reassign Capacity to a Domestic Workshop Rota", "slots", "domestic_reservations workshop_recovery service_replacement transport_rotation",
  "production_speed_buildings_factor = 0.025\nwar_support_factor = -0.015", "Use the domestic reservation, recovered workshop, replacement task and rested transport crew together. This remains useful after a refused offer and trades mobilisation attention for deliverable domestic work.", "tools", "civil"),
 ("settlement_arbitration", "Fund a Deliverable Settlement Arbitration", "slots", "release_service_slots settlement_routes reconstruction_timetable supplier_arbitration",
  "research_speed_factor = 0.02\npolitical_power_factor = -0.03", "Release the expired emergency claim, follow the actual route and timetable, and arbitrate the unfinished bargain. Technical learning improves while the board answers competing claims.", "scales", "document"),
 ("standing_terms", "Renew Inspected Standing Service Terms", "slots", "service_cost_review coalition_reconciliation maintain_local_bargains domestic_service_terms postwar_transport",
  "industrial_capacity_factory = 0.02\nconsumer_goods_factor = 0.015", "Verify costs, separate coalition receipts, retained local bargains and the domestic fallback before renewing postwar transport. Existing output benefits from a service that accepts an ordinary civilian burden.", "logistics", "economy"),
],
"UGE": [
 ("depot_custody", "Lease Verified Dispersed Custody", "occupied_slot", "reserve_rota slot_authority depot_contingencies protected_storage",
  "surrender_limit = 0.025\nproduction_speed_buildings_factor = -0.02", "Assign a custodian, expiry authority, fallback route and inspected storage terms. Resilience occupies one scarce slot and diverts construction attention until the ninety-day lease ends.", "logistics", "security"),
 ("driver_relay", "Lease a Tested Driver and Receiving Relay", "occupied_slot", "movement_exercises forecast_dispatch local_drivers service_slot_review",
  "army_speed_factor = 0.03\npolitical_power_factor = -0.03", "An exercised movement, current dispatch, named driver and reviewed slot authority make a limited relay useful. The slot cannot simultaneously support another reserve task.", "bridge", "communications"),
 ("receiving_chain", "Lease an Inspected Emergency Receiving Chain", "occupied_slot", "dispersed_accounts emergency_movement after_the_warning receiving_repairs",
  "supply_consumption_factor = -0.03\nconsumer_goods_factor = 0.015", "Match surviving accounts and authorised movement to a repaired receiving office under current conditions. The service uses a scarce slot and continuing civilian allocation; it grants no new vehicles.", "bridge", "tools"),
 ("reopening_rotation", "Lease a Bounded Depot Reopening Rotation", "occupied_slot", "depot_recovery slot_rotation mobility_recovery settlement_inventory",
  "production_speed_buildings_factor = 0.03\nplanning_speed = -0.02", "Recovered custody, an actual slot rotation and repaired mobility follow the surviving settlement. Construction gains a limited allocation at the cost of immediate military planning.", "tools", "logistics"),
 ("trained_reserve", "Lease a Costed Replacement Mobility Rota", "occupied_slot", "review_slot_costs depot_terms mobility_training coalition_receipts",
  "army_org_factor = 0.025\nindustrial_capacity_factory = -0.015", "Publish the slot cost, permanent custody terms, replacement training and separate coalition receipts. The readiness allocation remains useful without a foreign partner and occupies real administrative reserve space.", "training", "scales"),
],
"DEL": [
 ("receiving_evidence", "Allocate a Verified Requisition Inspection", "cases", "record_returns casework_rota command_accounts receiving_standards",
  "supply_consumption_factor = -0.025\nplanning_speed = -0.015", "A receiving return, responsible clerk, standing command account and common proof standard permit a sampled requisition inspection. It spends a case that could instead close an outstanding obligation.", "document", "scales"),
 ("warning_review", "Allocate an Inspected Scientific Docket", "cases", "contingency_dockets service_obligations scientific_returns inspection_exercises",
  "research_speed_factor = 0.025\nconsumer_goods_factor = 0.015", "Test scientific advice against contingency authority, published service duties and the exercised inspection chain. The case supports technical work at a continuing civilian cost without changing the project owner.", "science", "document"),
 ("competing_demands", "Allocate a Bounded Competing-Demand Review", "cases", "reserve_commitments records_duplicates emergency_casework command_requests",
  "planning_speed = 0.04\nstability_factor = -0.01", "Use documented reserve claims, retrievable duplicates and emergency staffing to answer conflicting command demands. Faster planning means defending an explicit refusal to an excluded service.", "command", "scales"),
 ("mobile_audit", "Allocate a Mobile Receiving Audit", "cases", "crisis_accounts records_in_motion requisition_audits receiving_backlog",
  "army_org_factor = 0.02\nproduction_speed_buildings_factor = -0.02", "Compare post-crisis accounts, travelling records, sampled requisitions and the receiving backlog. Existing organisation gains dependable evidence while inspectors leave ordinary development work.", "assembly", "document"),
 ("settlement_appeal", "Allocate a Verified Settlement Appeal", "cases", "obligation_settlement actual_terms casework_recovery",
  "stability_factor = 0.025\npolitical_power_factor = -0.04", "Read the actual terms, answer the outstanding obligation and recover the supporting casework. A verified appeal supports public confidence under local or external conditions while consuming political attention.", "peace", "scales"),
 ("standing_accounts", "Allocate a Joint Standing-Service Inspection", "cases", "standing_inspection command_service_terms coalition_dockets",
  "production_factory_max_efficiency_factor = 0.02\nconsumer_goods_factor = 0.015", "Scheduled inspection, published command-service terms and separate coalition dockets support a costed continuing allocation. The same case cannot also discharge a command obligation.", "scales", "industry"),
],
}

SCOPES = [Scope(tag, suffix, title, resource, tuple(requirements.split()), modifier, purpose, primary, secondary)
          for tag, rows in DATA.items() for suffix, title, resource, requirements, modifier, purpose, primary, secondary in rows]
CAPABILITIES = {tag + '_up_' + suffix: scope for scope in SCOPES for tag in [scope.tag] for suffix in scope.requirements}
if len(SCOPES) != 29 or sum(len(scope.requirements) for scope in SCOPES) != 117 or len(CAPABILITIES) != 117:
    raise ValueError('Expected 29 curated scopes using 117 nonfungible capabilities exactly once')
if not set(CAPABILITIES) <= {row.id for row in FOCUSES}:
    raise ValueError('An operational scope refers to an unknown focus')
