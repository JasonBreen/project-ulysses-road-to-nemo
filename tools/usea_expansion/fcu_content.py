"""Central Usea's distinct domestic bargains; provisional campaign design."""

# title, description, enduring modifiers, artwork subject
POLICIES={
 'civil':('Equal-Member Compact','Contributions are certified publicly and each member retains a voice. The appeals process sustains confidence but consumes political attention.','stability_factor = 0.04\npolitical_power_gain = -0.08','assembly'),
 'directive':('Needs-Based Common Fund','The secretariat directs reconstruction toward the greatest need. A permanent common contribution and disputes with net contributors are the price of faster construction.','production_speed_buildings_factor = 0.04\nconsumer_goods_factor = 0.02\nstability_factor = -0.01','economy'),
 'service':('Treaty Recovery Secretariat','A permanent civilian staff maintains repair contracts and relief routes after the settlement. Its payroll continues after emergency mobilisation ends.','supply_consumption_factor = -0.03\nconsumer_goods_factor = 0.01','rebuild'),
 'relief_priority':('Protected Civil Convoys','Medical and shelter transport is ring-fenced from military requisition. Supply planning improves while the government limits its mobilisation rhetoric.','supply_consumption_factor = -0.04\nwar_support_factor = -0.02','medical'),
 'dual_use':('Dual-Use Transport Reserve','Civilian carriers train with the services and remain available for mobilisation. Joint planning improves, but keeping the reserve ready ties up commercial capacity.','planning_speed = 0.08\nconsumer_goods_factor = 0.01','logistics'),
 'joint_staff':('Coalition Liaison Rotation','For one year, liaison teams train headquarters together. Frequent exercises accelerate planning and consume additional supplies.','planning_speed = 0.10\nsupply_consumption_factor = 0.02','command'),
 'air_picture':('Coordinated Air Reporting','For one year, shared identification and reporting procedures improve air missions. Maintaining the liaison network consumes political attention.','air_mission_efficiency = 0.05\npolitical_power_gain = -0.05','radar'),
}

OPTIONS={
 1:[('Publish the shortfalls and request a public mandate.','set_country_flag = FCU_exp_open_public\nadd_political_power = -20\nadd_stability = 0.03'),
    ('Authorize a temporary coordination staff.','set_country_flag = FCU_exp_open_staff\narmy_experience = 8\nadd_political_power = -10')],
 2:[('Guarantee equal members and published contributions.','remove_ideas = FCU_exp_directive\nadd_ideas = FCU_exp_civil'),
    ('Pool contributions and allocate them by need.','remove_ideas = FCU_exp_civil\nadd_ideas = FCU_exp_directive')],
 3:[('Protect the civilian convoy allocation.','remove_ideas = FCU_exp_dual_use\nadd_ideas = FCU_exp_relief_priority\nadd_political_power = -20\nset_country_flag = FCU_exp_relief_allocation\nset_country_flag = FCU_exp_prepared_relief\nif = { limit = { ac_ucw_active = yes } add_to_variable = { ac_ucw_pressure = -5 } ac_ucw_bound = yes }'),
    ('Contract a reserve for civil and military use.','remove_ideas = FCU_exp_relief_priority\nadd_ideas = FCU_exp_dual_use\nadd_political_power = -20\nset_country_flag = FCU_exp_dual_use_reserve\nset_country_flag = FCU_exp_prepared_readiness\nif = { limit = { ac_ucw_active = yes } add_to_variable = { ac_ucw_recovery = 2 } ac_ucw_bound = yes }')],
 4:[('Retain the treaty recovery secretariat.','add_ideas = FCU_exp_service\nadd_political_power = -20'),
    ('Return the emergency reserve to the districts.','remove_ideas = FCU_exp_service\nadd_stability = 0.03\nif = { limit = { ac_ucw_active = yes } add_to_variable = { ac_ucw_recovery = 6 } ac_ucw_bound = yes }')],
}

def apply(rows):
    by={r.id:r for r in rows}
    def update(ident,**kw):
        row=by['FCU_'+ident]
        for k,v in kw.items():setattr(row,k,v)
    update('exp_treaty_register',reward='add_political_power = -10\nadd_stability = 0.01')
    update('exp_burden_formula',desc='A flat contribution protects equal voting rights, while a common fund can direct more resources to districts with greater need. The council must choose a lasting fiscal bargain. Public certification improves stability at a political cost; pooled contributions accelerate construction but consume civilian capacity and provoke disputes.')
    update('exp_liaison_offices',title='Guarantee the Equal-Member Compact',x=1,y=3,
           available='has_idea = FCU_exp_civil',excludes=('FCU_exp_treaty_audit',),
           desc='Permanent liaison offices will enforce published contributions and hear member appeals. This implements the equal-member settlement. The common-fund alternative is closed for this opening programme.',
           reward='set_country_flag = FCU_exp_prepared_civil\nadd_stability = 0.02\nadd_political_power = -20')
    update('exp_treaty_audit',title='Empower the Common Fund',x=3,y=3,prerequisite=('FCU_exp_burden_formula',),
           available='has_idea = FCU_exp_directive',excludes=('FCU_exp_liaison_offices',),
           desc='The secretariat will certify deliveries and direct common contributions to the most exposed districts. This implements the needs-based settlement. The equal-member alternative is closed for this opening programme.',
           reward='set_country_flag = FCU_exp_prepared_logistics\nadd_tech_bonus = { name = FCU_exp_treaty_audit bonus = 0.5 uses = 1 category = industry }\nadd_political_power = -25')
    update('exp_medical_register',reward='add_political_power = -15\nset_country_flag = FCU_exp_choice_3_ready',
           desc='A common medical register reveals the vehicles and trained crews available for one reserve. The council will decide whether to protect civilian convoys or contract a dual-use reserve. That choice has a continuing cost and determines the next focus in this branch.')
    update('exp_shelter_exercises',title='Ring-Fence the Civil Convoys',x=11,y=3,
           available='has_idea = FCU_exp_relief_priority',excludes=('FCU_exp_public_information',),
           reward='set_country_flag = FCU_exp_prepared_relief\nadd_stability = 0.02',
           desc='Exercise hospital transfers and shelter deliveries using protected civilian transport. Military headquarters must plan around that commitment. The reserve will reduce refugee pressure when the Usean emergency begins.')
    update('exp_public_information',title='Train the Dual-Use Reserve',x=13,y=3,prerequisite=('FCU_exp_medical_register',),
           available='has_idea = FCU_exp_dual_use',excludes=('FCU_exp_shelter_exercises',),
           reward='set_country_flag = FCU_exp_prepared_readiness\narmy_experience = 10\nnavy_experience = 5',
           desc='Civilian operators will rehearse mobilisation, emergency routing and the return to commercial service. Their readiness is useful in peace as well as war, but the protected-convoy alternative is closed for this opening programme.')
    update('exp_opening_assessment',prerequisite=('FCU_exp_liaison_offices','FCU_exp_treaty_audit','FCU_exp_interoperable_workshops','FCU_exp_shelter_exercises','FCU_exp_public_information','FCU_exp_readiness_commitment'))
    update('ucw_exp_burden_review',reward='set_country_flag = FCU_exp_choice_2_ready\nif = { limit = { has_idea = FCU_exp_civil } add_stability = 0.02 add_to_variable = { ac_ucw_pressure = -3 } }\nelse_if = { limit = { has_idea = FCU_exp_directive } add_to_variable = { ac_ucw_recovery = 4 } add_war_support = -0.01 }\nelse = { add_to_variable = { ac_ucw_recovery = 3 } }\nac_ucw_bound = yes',
           desc='Apply the bargain made before the disaster. Equal-member certification eases camp pressure and sustains confidence; the common fund accelerates recovery while accepting domestic opposition. A government without a previous bargain receives a fresh council vote.')
    update('ucw_exp_transport_board',reward='if = { limit = { has_idea = FCU_exp_relief_priority } add_to_variable = { ac_ucw_pressure = -4 } add_to_variable = { ac_ucw_recovery = 3 } }\nelse_if = { limit = { has_idea = FCU_exp_dual_use } add_to_variable = { ac_ucw_recovery = 5 } army_experience = 5 }\nelse = { add_to_variable = { ac_ucw_recovery = 4 } }\nac_ucw_bound = yes',
           desc='The transport board inherits the reserve chosen before the emergency. Protected convoys ease refugee pressure and restore services; dual-use carriers improve recovery and liaison practice. Neither policy creates unlimited shipping or changes faction membership.')
    update('ucw_exp_staff_training',reward='add_timed_idea = { idea = FCU_exp_joint_staff days = 365 }\nadd_political_power = -20')
    update('ucw_exp_radar_reporting',reward='add_timed_idea = { idea = FCU_exp_air_picture days = 365 }\nadd_political_power = -20')
    update('ucw_exp_escort_schedules',reward='navy_experience = 10\nif = { limit = { has_idea = FCU_exp_relief_priority } add_to_variable = { ac_ucw_pressure = -3 } }\nelse_if = { limit = { has_idea = FCU_exp_dual_use } add_to_variable = { ac_ucw_recovery = 3 } }\nac_ucw_bound = yes')
    update('ucw_exp_repatriation',desc='Provide documents, transport and credible information for voluntary returns. The transport allocation already chosen remains binding; governments that never settled it receive a council vote. No return is compulsory and this office changes no borders.')
