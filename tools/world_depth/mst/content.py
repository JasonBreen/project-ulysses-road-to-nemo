"""Monstrua (MST): bespoke national focus tree, era e1 (1991 to 2005).

Source layers. Mod provenance: the inherited history file (the fascism party ruling with 90
percent popularity, elections suspended since the November 1987 vote, stability 0.5 and war
support 0.80), the unnamed National Administration office, the party-specific country names,
the four 1991 states with their inherited captions, the railway and the map. Official: ACES
Chronicle rows used only as date anchors for distant pressures, each cited by its exact key.
Everything else, including every Monstruan choice, office, idea, building, decision and event,
is provisional gameplay.
"""
from spec import *  # noqa: F401,F403

COUNTRY = Country(tag='MST', name='Monstrua', root='world', package='mst',
                  themes=('security', 'air', 'industry'), max_columns=35)

SCHEMA = 2
ERAS = ('e1',)

SOURCES = (
    Source('Mod provenance',
           'Inherited 1991 state: capital state 406; ruling_party fascism; last_election 1987.11.9, election_frequency 48, '
           'elections_allowed = no; popularities fascism 90, neutrality 5, communism 3, democratic 2; stability 0.5 and war '
           'support 0.80; four research slots; tech_mountaineers, early_fighter and basic_train among the starting '
           'technologies; grand doctrines superior_firepower, new_fleet_in_being and new_operational_integrity. The starting '
           'leader is the unnamed National Administration office (MST_ac_government_office, fascism_ideology), whose 1991 '
           'holder has not been established. Party names: Monstruan State (fascism), Monstruan Junta (neutrality), Monstruan '
           'Republic (democratic), Union of Monstruan Socialist Republics (communism), Kingdom of Monstrua (monarchism). The '
           'tree calls the ruling party the movement and never names a holder.',
           'mod/2985041246/history/countries/MST - Monstrua.txt; mod/2985041246/common/characters/ac_starting_governments.txt; '
           'mod/2985041246/localisation/english/ac_starting_governments_l_english.yml; '
           'mod/2985041246/localisation/english/countries_l_english.yml'),
    Source('Mod provenance',
           'Geography: four 1991 states. 406 Colmillo (capital; large_city, eight shared slots, seven used by 3 arms factories, '
           '3 industrial complexes and the fuel silo; infrastructure 5; air base 3; naval base and victory point 90 at '
           'province 8233, captioned Bufang; supply nodes at 8233 and 8533; hills, forest and plains). 408 Garracia (town, four '
           'slots all used; infrastructure 4; hills and forest; supply node 8526; land frontier with AQU via 784 and 8526). '
           '422 Colana (town, three of four slots used; infrastructure 3; air base 1; plains; supply node and victory point 5 '
           'at 1917; land frontier with VLK and AQU via 1428). 439 Vuelona (large_city, seven of eight slots used by 4 arms '
           'factories and 3 industrial complexes; infrastructure 5; no air base, resources or victory point). Every state is '
           'coastal. Level-2 railway: 8233-3639-1989-8533 inside Colmillo; trunk 1989-1473-25-4123-3285-1917 through all four '
           'states; spurs 4123-8526 to the Garracia frontier depot and 25-2247-3587 to the Vuelona coast. Sea neighbours: '
           'Sotoa across sea provinces 10225 and 10929 to the south; Valka and Aquitoria across 10722 and 10014. Adjacency and '
           'compass words come from map/provinces.bmp, map/definition.csv and province centroids. The state captions and '
           'Bufang are inherited archive names; the logistics-centre hub captions are not used as place names.',
           'mod/2985041246/history/states/406-State_406.txt; 408-State_408.txt; 422-State_422.txt; 439-State_439.txt; '
           'mod/2985041246/localisation/english/state_names_l_english.yml; '
           'mod/2985041246/localisation/english/victory_points_l_english.yml; mod/2985041246/map/railways.txt; '
           'mod/2985041246/map/supply_nodes.txt; tools/world_foundation/country_registry.json (MST)'),
    Source('Mod provenance',
           'Neighbours as inherited: Aquitoria a crown government with its chamber unelected since 1987; Valka and Sotoa ruled '
           'by democratic parties with fascism 50 and neutrality 48 percent popularity and elections suspended. The Aquitoria '
           'spec describes a market road and customs post on its southern frontier, Monstruan uniformed men at the Monstruan '
           'end of that post, Monstruan exiles living in Aquitoria and Monstruan envoys calling at its crown office; this tree '
           'writes the Monstruan side of those and never assumes which Aquitorian answer was chosen. No border, core or '
           'faction of any neighbour changes.',
           'mod/2985041246/history/countries/AQU - Aquitoria.txt; VLK - Valka.txt; SOA - Sotoa.txt; '
           'tools/world_depth/aqu/content.py (neighbours branch and neighbour_notes event)'),
    Source('Provisional gameplay',
           'World-start calibration the tree builds on: role territorial and air reserve with no combat navy; 10 civilian and '
           '10 military factories, no dockyard; 8 infantry formations of five battalions with replacement-backed engineer and '
           'artillery companies; 72 fighters and 12 support aircraft on two airfields, with 18 and 4 more in storage; stocks of '
           '1920 infantry equipment, 1040 motorized equipment, 32 trains, 384 support equipment and 240 artillery; 60 convoys; '
           'research priority Physical Sustainment. Resources oil 14, aluminium 14, steel 16, rubber 7, tungsten 4, no '
           'chromium. Fiscal calibration GDP 280 billion, debt ratio 0.3, collection 0.85, growth 3.0, inflation 2.0; '
           'command_administration institution, capacity 40. Fictional gameplay calibration, not canon national accounts.',
           'tools/world_starts/profiles.json (MST); tools/economy_v2/profiles.json; tools/institutions/profiles.json; '
           'docs/WORLD_STARTS_CALIBRATION.md; mod/2985041246/localisation/english/ac_world_starts_l_english.yml'),
    Source('Official',
           'Date anchor: the IAU announces that the asteroid Ulysses will pass close to the Earth and may strike it. Opening '
           'of the asteroid branch; Monstruan preparations are gameplay.', '1994 / 12.10'),
    Source('Official',
           'Date anchor: the Belkan War breaks out. Date gate of the distant-war branch; Monstrua takes no part.',
           '1995 / 03.25'),
    Source('Official',
           'The Belkan Army uses seven nuclear devices in the Waldreich Mountains. Background to the fallout focus, which also '
           'reads the mod flag belka_dropped_nukes; no effect on Monstrua is claimed.', '1995 / 06.06'),
    Source('Official',
           'Date anchor: a treaty is signed in Lumen and the Belkan War ends. Date gate of the postwar focus.', '1995 / 06.20'),
    Source('Official',
           'Date anchor: the FCU announces that Ulysses will impact the Earth. Date gate of the shelter expansion focus; '
           'where fragments fall is never stated.', '1996 / 04.20'),
    Source('Official',
           'Date anchor: Ulysses passes through the Roche limit of the Earth. Date gate of the shelter night focus and '
           'event; no damage in Monstrua is claimed.', '1999 / 07.08'),
    Source('Official',
           'Date anchor: Osea, Emmeria and other nations join economic sanctions against Estovakia. Date gate of the import '
           'review focus; Monstrua is not claimed among the sanctioning states.', '2002 / 03.20'),
    Source('Official',
           'Erusea invades the neutral country of San Salvacion, seizes Stonehenge and uses its railguns against aircraft. '
           'Premise of the stored-airframe branch; no Monstruan sale is claimed as fact.', '2003 / SUMMER'),
    Source('Official',
           'The FCU establishes the ISAF. Mentioned in the opening of the stored-airframe branch; trade only, no faction.',
           '2003 / 08.22'),
    Source('Official',
           'Farbanti falls, the ISAF accepts the Erusean surrender and the Continental War ends. Date gate of the closing '
           'account; the outcome focuses read the mod outcome flags instead of assuming this ending.', '2005 / 09.19'),
    Source('Mod provenance',
           'Campaign hooks read only, never set: belka_won_belkan_war, belka_lost_belkan_war and belka_dropped_nukes '
           '(events/Belka.txt); ac_ucw_outcome_isaf_victory, ac_ucw_outcome_erusean_victory and ac_ucw_outcome_stalemate '
           '(common/scripted_effects/ac_ucw.txt). Each reaction is a leaf focus, so no outcome blocks the tree.',
           'mod/2985041246/events/Belka.txt; mod/2985041246/common/scripted_effects/ac_ucw.txt'),
    Source('Provisional gameplay',
           'All Monstruan focuses, ideas, offices, buildings, flags, decisions and events in this spec. No named people; '
           'offices are collective and unnamed; no border, core, war, annexation or faction effects. Shared buildings use only '
           'the single free slots in Colmillo, Colana and Vuelona; the rest are air bases, radar and infrastructure within '
           'their caps. No dockyard and no combat navy, following the calibration.'),
)

# --- ideas ---------------------------------------------------------------------------------------
IDEAS = (
    # the movement and the state
    IdeaDef('ninety_percent', 'The Ninety in a Hundred', 'The movement claims nine Monstruans in ten and has counted no vote since 1987.',
            {'political_power_gain': 0.10, 'war_support_factor': 0.05, 'stability_factor': -0.03}, ('assembly', 'command')),
    IdeaDef('stairwell_wardens', 'Stipended Stairwell Wardens', 'A paid movement warden on every stairwell of the big apartment blocks.',
            {'stability_factor': 0.03, 'political_power_factor': -0.03}, ('civil', 'security')),
    IdeaDef('ministry_cells', 'Cells Inside the Ministries', 'Party cells review every appointment and budget line.',
            {'political_power_gain': 0.15, 'war_support_factor': 0.05, 'stability_factor': -0.03}, ('assembly', 'document')),
    IdeaDef('staff_memorandum', 'The Officers Memorandum', 'The general staff has asked in writing to manage the state.',
            {'army_org_factor': 0.04, 'planning_speed': 0.05, 'political_power_gain': 0.05}, ('command', 'document')),
    IdeaDef('round_table', 'The Charter Round Table', 'Movement moderates and the old notables draft a written charter together.',
            {'stability_factor': 0.03, 'research_speed_factor': 0.02, 'political_power_gain': -0.05}, ('ballot', 'document')),
    IdeaDef('movement_code', 'The Directorate Statute Book', 'One code of decrees for the press, unions, columns and frontier.',
            {'political_power_gain': 0.15, 'war_support_factor': 0.08, 'stability_factor': 0.04}, ('document', 'security')),
    IdeaDef('military_districts', 'Rule by Four District Commands', 'Each state is a military district answering to the council.',
            {'army_org_factor': 0.06, 'planning_speed': 0.10, 'stability_factor': 0.04}, ('command', 'rail')),
    IdeaDef('first_chamber', 'A Chamber Counted Again', 'An elected chamber sits under the charter; the movement holds a majority, not every seat.',
            {'stability_factor': 0.07, 'political_power_factor': 0.06, 'research_speed_factor': 0.03}, ('ballot', 'assembly')),
    # Colmillo and Bufang
    IdeaDef('quay_survey', 'The Harbour Survey Volumes', 'Four volumes on why ships wait at anchor off Bufang.',
            {'production_speed_buildings_factor': 0.03}, ('navy', 'document')),
    IdeaDef('fast_quays', 'Quick Turnaround at Bufang', 'Modern cranes and a quay rail spur halve the time a ship spends in port.',
            {'consumer_goods_factor': -0.04, 'production_speed_buildings_factor': 0.05}, ('tools', 'navy')),
    IdeaDef('depot_sidings', 'Double Track to the Depot', 'Freight leaves the quays without blocking the passenger trains.',
            {'production_speed_infrastructure_factor': 0.10, 'supply_consumption_factor': -0.03}, ('rail', 'logistics')),
    IdeaDef('quay_hall', 'The Movement Hall by the Quay', 'The directorate governs Bufang from a hall beside the merchant quay.',
            {'political_power_gain': 0.10, 'stability_factor': 0.02}, ('assembly', 'navy')),
    IdeaDef('harbour_command', 'Bufang Under District Command', 'The port runs as a military installation with curfews and patrols.',
            {'stability_factor': 0.04, 'army_core_defence_factor': 0.05}, ('security', 'navy')),
    IdeaDef('city_council', 'An Elected Bufang Council', 'The capital chooses its own council and sets its own street budget.',
            {'stability_factor': 0.05, 'consumer_goods_factor': -0.02}, ('ballot', 'civil')),
    IdeaDef('bufang_fair', 'Fair Season on the Quay', 'Foreign buyers walk the merchant quay looking for orders.',
            {'consumer_goods_factor': -0.04, 'research_speed_factor': 0.02}, ('economy', 'diplomacy')),
    # twenty plants
    IdeaDef('plant_ledger', 'One Ledger for Twenty Plants', 'Every hall and works reports real output to the planning office.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': -0.03}, ('industry', 'document')),
    IdeaDef('spares_quota', 'The Spares Quota', 'Each plant delivers replacement parts before any new item leaves the line.',
            {'repair_speed_factor': 0.10, 'supply_consumption_factor': -0.03}, ('tools', 'logistics')),
    IdeaDef('vuelona_yards', 'Ore Trains Inside the Walls', 'Ore wagons unload inside the Vuelona hall yards.',
            {'production_factory_efficiency_gain_factor': 0.04}, ('rail', 'industry')),
    IdeaDef('guns_first', 'The Arms Belt Has Priority', 'Credit and the best machine tools go to the arms halls first.',
            {'production_speed_arms_factory_factor': 0.10, 'industrial_capacity_factory': 0.04, 'consumer_goods_factor': 0.03}, ('missile', 'industry')),
    IdeaDef('shop_windows', 'Full Shop Windows', 'Civilian plants make household goods, building materials and farm tools.',
            {'consumer_goods_factor': -0.05, 'stability_factor': 0.04, 'production_speed_industrial_complex_factor': 0.08}, ('economy', 'civil')),
    IdeaDef('motor_economy', 'Trucks, Wagons and Spares', 'Industry specialises in what keeps everything else moving.',
            {'supply_consumption_factor': -0.05, 'production_factory_max_efficiency_factor': 0.04, 'army_speed_factor': 0.03}, ('logistics', 'tools')),
    IdeaDef('tool_credit', 'Lathes Bought on Credit', 'Modern machine tools installed plant by plant, paid in foreign currency.',
            {'production_factory_max_efficiency_factor': 0.05, 'political_power_gain': -0.05}, ('tools', 'economy')),
    # oil and ore
    IdeaDef('survey_maps', 'The Geological Maps', 'Every well and seam is mapped and its ten-year yield estimated.',
            {'production_speed_buildings_factor': 0.03}, ('tools', 'document')),
    IdeaDef('oil_trust', 'The State Oil and Ore Trust', 'One trust sells every barrel and ingot to Monstruan plants at fixed prices.',
            {'production_speed_buildings_factor': 0.05, 'political_power_gain': 0.05}, ('economy', 'command')),
    IdeaDef('drilling_leases', 'Twenty-Year Drilling Leases', 'Foreign companies drill and mine for royalties paid in hard currency.',
            {'production_speed_industrial_complex_factor': 0.08, 'consumer_goods_factor': -0.02, 'stability_factor': -0.02}, ('economy', 'diplomacy')),
    IdeaDef('aluminium_mill', 'Sheet from Monstruan Bauxite', 'A rolling mill feeds the airframe repair shops.',
            {'repair_speed_factor': 0.08, 'production_factory_efficiency_gain_factor': 0.02}, ('air', 'industry')),
    IdeaDef('alloy_contracts', 'Long Alloy Contracts', 'Chromium and extra tungsten bought abroad on long contracts and stockpiled.',
            {'production_factory_max_efficiency_factor': 0.03, 'consumer_goods_factor': 0.02}, ('scales', 'document')),
    # the army and the columns
    IdeaDef('muster_rolls', 'Rolls of the Eight Formations', 'The general staff knows who answers a call and which trucks start.',
            {'army_org_factor': 0.03, 'training_time_army_factor': -0.05}, ('training', 'command')),
    IdeaDef('battery_drill', 'Concentrated Batteries', 'The guns are gathered into a few well-drilled batteries with spare barrels.',
            {'army_attack_factor': 0.04, 'experience_gain_army_factor': 0.05}, ('missile', 'training')),
    IdeaDef('column_reserve', 'Columns on the Reserve Rolls', 'Trained youth column members are listed as army reservists.',
            {'training_time_army_factor': -0.10, 'army_core_defence_factor': 0.05}, ('training', 'security')),
    IdeaDef('party_guard', 'The Party Guard', 'An armed movement guard beside the army, answering to the committee.',
            {'stability_factor': 0.05, 'political_power_gain': 0.05, 'army_org_factor': -0.03}, ('security', 'assembly')),
    IdeaDef('columns_stood_down', 'Columns Stood Down', 'The youth columns are disbanded and their rifles returned to depots.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02, 'war_support_factor': -0.04}, ('peace', 'civil')),
    IdeaDef('column_battalions', 'Battalions of Former Columns', 'Reserve battalions recruited whole from the old columns.',
            {'training_time_army_factor': -0.15, 'army_core_defence_factor': 0.08}, ('medal', 'training')),
    IdeaDef('guard_barracks', 'A Guard Barracked by Every Ministry', 'The party guard holds its own barracks beside every ministry.',
            {'stability_factor': 0.08, 'political_power_gain': 0.08, 'army_org_factor': -0.03}, ('security', 'command')),
    IdeaDef('camp_schools', 'Camps Turned into Schools', 'Old column camps teach welding, wiring and engine repair.',
            {'research_speed_factor': 0.04, 'stability_factor': 0.03}, ('science', 'civil')),
    IdeaDef('hill_companies', 'Companies Trained on Slopes', 'One battalion per formation trained to fight in the Garracia hills.',
            {'army_defence_factor': 0.05, 'attrition': -0.05}, ('training', 'tools')),
    # the air reserve
    IdeaDef('crowded_fields', 'Two Overcrowded Fields', 'Eighty-four aircraft share two fields built for half that number.',
            {'experience_gain_air_factor': 0.05, 'air_mission_efficiency': -0.03}, ('air', 'runway')),
    IdeaDef('home_sky', 'Keep the Home Sky Clear', 'The air reserve exists to keep foreign aircraft out of Monstruan airspace.',
            {'air_superiority_efficiency': 0.08, 'air_detection': 0.05, 'experience_gain_air_factor': 0.05}, ('air', 'radar')),
    IdeaDef('battery_wings', 'Air Support for the Guns', 'Fighters escort strike aircraft that hit what the batteries cannot reach.',
            {'air_mission_efficiency': 0.08, 'army_attack_factor': 0.03, 'experience_gain_air_factor': 0.05}, ('missile', 'air')),
    IdeaDef('colana_school', 'The Colana Flying School', 'Pilots learn to fly away from the alert squadrons.',
            {'experience_gain_air_factor': 0.08, 'training_time_factor': -0.05}, ('training', 'air')),
    IdeaDef('weekend_reserve', 'The Saturday Squadrons', 'Former pilots and qualified civilians fly on weekends and answer a call-up.',
            {'air_defence_factor': 0.05, 'experience_gain_air_factor': 0.05, 'political_power_gain': -0.03}, ('medal', 'air')),
    IdeaDef('patrol_hours', 'Hours Logged on Silo Fuel', 'Long coastal patrols flown on the strategic fuel reserve.',
            {'experience_gain_air_factor': 0.10, 'air_detection': 0.05}, ('air', 'logistics')),
    # neighbours by land and sea
    IdeaDef('northern_watch', 'Eyes on the Northern Hills', 'Envoys and frontier posts report on both northern neighbours.',
            {'army_core_defence_factor': 0.04, 'political_power_gain': 0.03}, ('diplomacy', 'security')),
    IdeaDef('market_road_post', 'Duties on the Market Road', 'A Monstruan customs post where the hill farmers cross to the plain markets.',
            {'consumer_goods_factor': -0.02, 'stability_factor': 0.01}, ('economy', 'security')),
    IdeaDef('exile_lists', 'Names Sent North', 'The committee has asked the Aquitorian crown office to watch named exiles.',
            {'political_power_gain': 0.05, 'stability_factor': -0.02}, ('document', 'security')),
    IdeaDef('return_letters', 'Letters of Safe Conduct Home', 'Exiles may return without prosecution if they stay out of politics.',
            {'stability_factor': 0.03, 'political_power_gain': -0.03}, ('peace', 'refugees')),
    IdeaDef('frontier_files', 'Files on Every Traveller', 'The Garracia frontier police check couriers, letters and parcels.',
            {'political_power_gain': 0.08, 'army_core_defence_factor': 0.03, 'stability_factor': -0.02}, ('document', 'gate')),
    IdeaDef('returning_families', 'Families Back from the North', 'Returned exiles live under a weekly warden visit and talk in every stairwell.',
            {'stability_factor': 0.04, 'research_speed_factor': 0.02}, ('refugees', 'civil')),
    IdeaDef('valka_freight_siding', 'Wagons to the Valkan Post', 'Freight wagons run from the Colana depot to the Valkan crossing.',
            {'consumer_goods_factor': -0.03}, ('rail', 'diplomacy')),
    IdeaDef('valkan_friends', 'Friends of the Valkan Nationalists', 'Movement presses and meeting halls court the nationalist half of Valka.',
            {'war_support_factor': 0.04, 'political_power_gain': 0.05, 'stability_factor': -0.02}, ('diplomacy', 'assembly')),
    IdeaDef('valka_correct', 'Business Only with Valka', 'Envoys discuss freight, water and fishing with whoever governs Valka.',
            {'stability_factor': 0.03, 'consumer_goods_factor': -0.02}, ('diplomacy', 'scales')),
    IdeaDef('southern_crossing', 'Direct Sailings to Sotoa', 'Freighters sail from Bufang to Sotoan ports without middlemen.',
            {'consumer_goods_factor': -0.03, 'stability_factor': 0.01}, ('navy', 'economy')),
    # the asteroid
    IdeaDef('impact_committee', 'The Asteroid Committee', 'A movement committee sits every week on what Ulysses might do.',
            {'stability_factor': 0.02, 'political_power_gain': -0.03}, ('meteor', 'assembly')),
    IdeaDef('single_bulletin', 'One Bulletin for Everyone', 'Every asteroid report passes through a single movement office.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03, 'research_speed_factor': -0.02}, ('communications', 'security')),
    IdeaDef('open_figures', 'Orbit Figures on the Radio', 'University physicists explain each new observatory figure every week.',
            {'research_speed_factor': 0.03, 'stability_factor': -0.02}, ('telescope', 'document')),
    IdeaDef('quay_cellars', 'Shelters Under the Quay District', 'The old merchant cellars of Bufang joined into ventilated shelters.',
            {'static_anti_air_damage_factor': 0.08, 'stability_factor': 0.02}, ('shelter', 'civil')),
    IdeaDef('hill_tunnels', 'Tunnels Behind the Arms Belt', 'Shelter tunnels in the Vuelona hills that double as protected stores.',
            {'static_anti_air_damage_factor': 0.05, 'supply_consumption_factor': -0.03}, ('shelter', 'tools')),
    IdeaDef('impact_programme', 'Six-Month Shelter Programme', 'Compulsory drills, doubled shelter budgets and stored grain in every district.',
            {'stability_factor': 0.04, 'war_support_factor': 0.03, 'consumer_goods_factor': 0.03}, ('meteor', 'shelter')),
    IdeaDef('quiet_bill', 'The Unpublished Shelter Bill', 'The plants absorb the shelter costs and no figure is printed.',
            {'political_power_gain': 0.05, 'stability_factor': 0.02}, ('document', 'economy')),
    IdeaDef('shelter_accounts', 'Shelter Accounts in Print', 'Every district can read what its shelters cost and who built them.',
            {'stability_factor': 0.03, 'political_power_factor': 0.04}, ('scales', 'shelter')),
    # the Belkan War years
    IdeaDef('war_news', 'Maps of the Belkan Front', 'Whole newspaper pages follow the fighting in Belka.',
            {'war_support_factor': 0.05}, ('communications', 'command')),
    IdeaDef('fallout_monitors', 'Radiation Monitors at the Depots', 'Counters at the quays and the Colana depot, and iodine in every district.',
            {'stability_factor': 0.03}, ('medical', 'security')),
    IdeaDef('postwar_lull', 'Cancelled Arms Enquiries', 'Foreign buyers withdraw half their enquiries after the Lumen treaty.',
            {'production_speed_arms_factory_factor': -0.05, 'consumer_goods_factor': -0.02}, ('peace', 'industry')),
    IdeaDef('isolation_lessons', 'No State Stands Alone', 'The staff concludes that discipline did not save a country without friends.',
            {'army_core_defence_factor': 0.05, 'stability_factor': 0.02}, ('document', 'diplomacy')),
    IdeaDef('belkan_style_orders', 'Orders in the Belkan Style', 'Foreign buyers want weapons built the way the Belkan reports describe.',
            {'production_speed_arms_factory_factor': 0.08, 'industrial_capacity_factory': 0.03}, ('missile', 'economy')),
    IdeaDef('sanctions_review', 'The Import Exposure Review', 'The ministries know which imports could be cut off and for how long.',
            {'production_factory_efficiency_gain_factor': 0.03, 'political_power_gain': 0.03}, ('scales', 'document')),
    # the Usean war years
    IdeaDef('airframe_sales', 'Stored Airframes Sold Abroad', 'Surplus fighters sold with spares and training to buyers far from Usea.',
            {'political_power_gain': 0.08, 'consumer_goods_factor': -0.03, 'air_superiority_efficiency': -0.03}, ('air', 'economy')),
    IdeaDef('hangar_reserve', 'Nothing Leaves the Hangars', 'Every stored airframe stays in Monstrua while the Usean war lasts.',
            {'air_defence_factor': 0.05, 'consumer_goods_factor': 0.02}, ('air', 'shelter')),
    IdeaDef('refitted_squadrons', 'Fewer Aircraft, Better Kept', 'Sale money bought new engines and avionics for the aircraft that stayed.',
            {'air_superiority_efficiency': 0.06, 'air_mission_efficiency': 0.05}, ('air', 'tools')),
    IdeaDef('rotated_hangars', 'A Second Line That Flies', 'Stored aircraft are run, flown and inspected twice a year.',
            {'air_defence_factor': 0.08, 'experience_gain_air_factor': 0.05}, ('runway', 'training')),
    IdeaDef('decade_account', 'The Account of Fifteen Years', 'A plain public record of what the years since 1991 cost and taught.',
            {'stability_factor': 0.04, 'political_power_factor': 0.04}, ('document', 'peace')),
    # decision ideas
    IdeaDef('rally_fervour', 'After the Rally Day', 'Banners on every block for a few weeks after a national rally.',
            {'war_support_factor': 0.05, 'political_power_gain': 0.05}, ('assembly', 'medal')),
    IdeaDef('callup_exercise', 'Saturday Pilots Called Up', 'The weekend reserve flies a full week with the front-line squadrons.',
            {'experience_gain_air_factor': 0.10}, ('air', 'training')),
    IdeaDef('trunk_clearance', 'Troop Trains Have the Line', 'Civilian freight waits while battalions move on the trunk line.',
            {'army_speed_factor': 0.05, 'consumer_goods_factor': 0.02}, ('rail', 'command')),
    IdeaDef('market_day_crowds', 'Market Day at the Frontier', 'Traders from both sides crowd the Garracia customs post for a day.',
            {'stability_factor': 0.02, 'consumer_goods_factor': -0.01}, ('economy', 'peace')),
    IdeaDef('siren_drill', 'Siren Drill Week', 'Every district walks to its shelters on the sirens.',
            {'static_anti_air_damage_factor': 0.05, 'stability_factor': -0.01}, ('shelter', 'communications')),
)

# --- offices ---------------------------------------------------------------------------------------
OFFICES = (
    Office('movement_directorate', 'Directorate of the Monstruan Movement',
           'The movement senior committee constituted as a directorate that holds every ministry through party cells, with the '
           'youth columns and the stairwell wardens as arms of the state. Provisional gameplay office with no named holder.',
           'fascism', 'fascism_ideology'),
    Office('district_council', 'Council of the Four District Commands',
           'A council of the four military district commanders that holds the government seals, with the movement committee kept '
           'as an advisory body. Provisional gameplay office with no named holder.',
           'neutrality', 'stratocracy'),
    Office('charter_cabinet', 'Cabinet Under the Monstruan Charter',
           'A provisional cabinet named under a written charter, answerable to a chamber elected on a fixed calendar and bound by '
           'courts the movement does not appoint. Provisional gameplay office with no named holder.',
           'democratic', 'conservatism', elections=True),
)

# --- events --------------------------------------------------------------------------------------
EVENTS = (
    EventDef('loyalty_count', 'The Loyalty Returns', (
        "The district offices send their returns to Bufang in sealed folders, one for each state. On paper the totals match "
        "the movement's boast: nine Monstruans in ten count themselves its supporters. The folders also hold what the totals "
        "hide. In the Vuelona arms belt loyalty is strongest among older workers who remember worse shortages. On the Colana "
        "plains it is thinnest among farmers who mostly meet the movement as tax collectors in new uniforms.",
        "The general staff appears in the returns as well. Officers back the movement because it pays for the army, not "
        "because they enjoy its marches, and several district commanders have written remarks of their own in the margins. "
        "The handful of democrats and neutral notables who still meet in public turn out to be better organised than anyone "
        "in the committee believed, with membership lists that run to thousands in the capital alone.",
        "The committee must decide what to do with the folders. It can circulate them among its own members and argue over "
        "them behind closed doors, seal them in the archive and keep repeating the public figure, or pass a copy to the "
        "general staff and ask the officers plainly what they intend. Each choice shapes the argument about what the movement "
        "should become.",
    ), (
        Option('Circulate the returns inside the committee.', (PP(20), Stability(-0.01))),
        Option('Seal the folders and repeat the figure.', (WarSupport(0.02), PP(5))),
        Option('Ask the general staff for its view.', (PP(-10), Event('staff_reply', 14))),
    ), picture=0),
    EventDef('staff_reply', 'The General Staff Replies', (
        "Two weeks after receiving the folders, the general staff answers by courier instead of through the usual ministry "
        "channels. The letter is courteous, long and signed by all four district commanders. It thanks the movement for the "
        "army budget, praises the youth columns for their discipline and commends the committee for its patience with an "
        "officer corps that seldom says thank you.",
        "Then it reaches its point. The officers write that four states, eight formations and twenty plants cannot be run by "
        "rallies, and that the stairwell wardens collect more grievances than the ministries can answer. They propose that "
        "trained managers, many of them serving officers, take charge of the ministries that matter most. They do not say "
        "what follows if the committee refuses.",
        "The letter leaks within days. Movement newspapers call it ingratitude; officers' families find themselves snubbed at "
        "public concerts; foreign attaches cable home speculation about a coup that nobody has actually planned. The "
        "committee can answer warmly and promise a review, answer coldly and remind the officers who pays them, or file the "
        "letter without any reply and wait to see who loses patience first.",
    ), (
        Option('Thank the officers and promise a review.', (Stability(0.02), PP(-15))),
        Option('Remind the officers who funds the army.', (PP(25), Stability(-0.02))),
        Option('File the letter without reply.', (WarSupport(0.01), PP(5))),
    ), picture=0),
    EventDef('berth_queue', 'Ships at Anchor off Bufang', (
        "The harbour survey takes a full season and fills four bound volumes, yet its central finding fits on one page. A "
        "merchant ship arriving at Bufang lies at anchor for days before a berth opens, then waits again while three worn "
        "cranes lift its cargo one sling at a time. Monstrua's trade moves on some sixty chartered convoys, and every idle day "
        "is paid for in foreign currency.",
        "The volumes also explain why nobody fixed the problem. Customs officers collect a fee for fast clearance, which makes "
        "slow clearance profitable. Dock gangs are paid by the shift rather than by the tonne. The port authority has asked "
        "for new cranes in every budget its staff can remember, and every time it has been told that the air reserve comes "
        "first.",
        "Shipping agents want the volumes published so that the ministries feel the embarrassment in public. The customs "
        "service wants them locked away. The movement's dockside branch, which counts most of the crane drivers among its "
        "members, wants a written promise that faster unloading will not cost a single job. The ministry cannot satisfy all "
        "three, and it must choose whose patience to spend.",
    ), (
        Option('Publish the survey and name the delays.', (PP(-15), Stability(0.02))),
        Option('Promise the dock gangs their jobs first.', (Stability(0.01), PP(10))),
    ), picture=1),
    EventDef('ledger_returns', 'Twenty Plants in One Book', (
        "The planning office binds the plant returns into a single ledger, the first in living memory to cover every hall and "
        "works in the country. Ten civilian plants and ten arms halls appear side by side, each with its machine ages, power "
        "demand, missing parts and true output rather than the output its director reported. Several plants turn out to have "
        "been counted twice in earlier returns.",
        "The picture is uneven. The Vuelona arms belt runs well when the ore trains arrive and stops when they do not. The "
        "Colmillo plants run short of power every evening. Garracia's two halls work on lathes older than their foremen, and "
        "the single arms hall in Colana survives mainly by borrowing parts from the civilian plants on the same street.",
        "Three schools of planners read the same pages and reach three conclusions. One wants every scarce resource for the "
        "arms halls, one wants the civilian plants to fill the shops, and one wants the whole economy built around trucks, "
        "engines and spare parts. The ledger supports each of them somewhere. The office must decide who reads it first, and "
        "that decision is already a kind of answer.",
    ), (
        Option('Send the ledger to every plant director.', (Stability(0.01), PP(-10))),
        Option('Keep it inside the planning office.', (PP(20), Stability(-0.01))),
    ), picture=2),
    EventDef('survey_findings', 'What Lies Under the Hills', (
        "The geologists come back from a year in the field with maps, core samples and a report that pleases nobody "
        "completely. Colmillo, Garracia and Colana all hold oil, bauxite and iron ore in useful amounts, enough to keep the "
        "country's own plants supplied for many years at the present rate. Rubber and tungsten deposits exist but are small. "
        "Of chromium the survey finds no trace at all.",
        "Vuelona, home of the busiest arms halls, sits on nothing worth digging, so every barrel and ingot it uses must cross "
        "the hills on the trunk line. The geologists add a strategic note: the Colana wells lie close to both the coast and "
        "the Valkan crossing, where a foreign company could load tankers with ease and an unfriendly army could reach them "
        "almost as easily.",
        "Two camps form around the report before the ink is dry. The movement's economic office wants a state trust that keeps "
        "every barrel at home for Monstruan plants. The treasury wants foreign drilling companies on long leases paying in "
        "hard currency. On one point both camps agree: the country must stop pretending it can make hard steel without "
        "importing the alloys.",
    ), (
        Option('Publish the maps to attract buyers.', (PP(-10), Stability(0.01))),
        Option('Classify the maps as state secrets.', (PP(15), WarSupport(0.01))),
    ), picture=2),
    EventDef('columns_question', 'The Columns at the Roadside', (
        "The muster of the eight formations draws crowds along every road, and the most disciplined of them wear the uniforms "
        "of the movement's youth columns. Thousands of young Monstruans have drilled on weekends for years. They can march, "
        "read a map and strip a rifle blindfolded. What they cannot say is whom they would obey if the movement and the army "
        "ever gave them different orders.",
        "The general staff wants the trained columns on its reserve rolls under regular officers. The committee wants them "
        "kept as the movement's own guard, armed and separate. Teachers, parents and the plant directors who lose young "
        "workers every Saturday want the columns stood down altogether, arguing that the country already has an army and "
        "needs welders more than marchers.",
        "Nothing will be settled this week. The muster report, however, must say something about the columns, and its wording "
        "will be quoted by every faction for years to come. It can praise them as the nation's true reserve, describe them "
        "carefully as a movement organisation outside the army, or record their numbers and say nothing else at all.",
    ), (
        Option('Praise them as the nation\'s reserve.', (WarSupport(0.02), Stability(-0.01))),
        Option('Call them a movement organisation.', (PP(15), Stability(0.01))),
        Option('Record the numbers and nothing more.', (Stability(0.01), PP(-5))),
    ), picture=0),
    EventDef('crowded_aprons', 'Wing to Wing on the Apron', (
        "An inspection team from the air staff walks the capital field at dawn and counts aircraft parked so tightly that "
        "their wingtips nearly touch. The Colana strip is no better. Seventy-two fighters and a dozen ground support aircraft "
        "share two fields built for half that number, while stored airframes fill every spare hangar and fuel bowsers queue "
        "along the taxiways.",
        "The team's report is blunt. One fire on the apron could spread through a squadron before anyone reached the "
        "extinguishers, and one raid could finish the air reserve before it left the ground. Ground crews work double shifts "
        "because there is room to service only a few aircraft at a time, and pilots fly fewer hours than their syllabus "
        "requires.",
        "The air staff wants new fields, and it wants them before the next budget is written. The treasury replies that "
        "runways are expensive and that the country already spends more on aircraft than on roads. The ministers can fund "
        "dispersal at once and cut something else to pay for it, or order the squadrons to rotate between the two fields "
        "while the money is found.",
    ), (
        Option('Fund dispersal at once.', (PP(-20), XP('air', 10))),
        Option('Rotate the squadrons and wait.', (PP(10), Stability(-0.01))),
    ), picture=1),
    EventDef('envoys_report', 'The Envoys Come Home', (
        "The two envoys return within a week of each other, each carrying a formal reply and a private report. The Aquitorian "
        "reply is courteous and brief, and the envoy suspects the crown office wrote it with one eye on whatever it was telling "
        "Valka. The Valkan reply is longer and warmer, though its cabinet seemed anxious both to be seen talking to Monstrua and "
        "to be seen keeping its distance.",
        "The private reports matter more. The envoy to Aquitoria counted Monstruan exiles at work in the port and the shops, "
        "and found them better organised than the committee believed, with a newsletter carried over the hills by hand. The "
        "envoy to Valka heard the nationalist half of the Valkan public speak admiringly of the movement, and the other half "
        "speak of little except how to avoid becoming like it.",
        "The committee must decide how much of this its own public will hear. The movement's newspapers want to print the "
        "Valkan admiration and ignore everything else. The foreign desk wants both reports kept confidential so that both "
        "neighbours keep talking. Whichever way it goes, Monstrua's frontier policy for the next decade begins with these two "
        "folders.",
    ), (
        Option('Print the warm words from Valka.', (WarSupport(0.02), PP(-5))),
        Option('Keep both reports confidential.', (PP(20), Stability(0.01))),
    ), picture=0),
    EventDef('sky_warning', 'Numbers from a Foreign Observatory', (
        "The warning came from the International Astronomical Union in December 1994: the asteroid Ulysses is on a course "
        "that brings it near the Earth, and a collision cannot be ruled out. Nobody can yet calculate what a strike would do. "
        "Monstrua owns no telescope able to check the figures. The Bufang radio stations read every foreign bulletin aloud, "
        "and the stairwell wardens field questions they have no answers for.",
        "The movement's committee meets late into the night. Its members have spent years telling Monstruans that discipline "
        "and unity can overcome any danger, and they are unsure how that message applies to a rock from space. The general "
        "staff offers engineers and depots. The university physicists offer to explain the orbit on the radio, if anyone will "
        "let them near a microphone.",
        "The committee's first statement on the asteroid cannot wait any longer. It can promise that the movement will "
        "protect every family and leave the details for later, or it can admit plainly that the danger is real, the numbers "
        "uncertain and the preparations only beginning. Whichever it chooses, the wardens will repeat it on every stairwell by "
        "nightfall, and the statement will be remembered long after Ulysses has done whatever it eventually does.",
    ), (
        Option('Promise protection for every family.', (WarSupport(0.03), Stability(-0.01))),
        Option('Admit what is not yet known.', (Stability(0.02), PP(-15))),
    ), citation='date anchor only, ACES Chronicle row 1994 / 12.10; Monstruan preparations are gameplay', picture=1),
    EventDef('roche_night', 'A Night in the Cellars', (
        "The asteroid crosses the Roche limit on 8 July 1999 and starts to break up overhead. In Bufang the sirens sound at dusk, "
        "and families file into the quay cellars with blankets, radios and children who think it is an adventure. In "
        "Vuelona the night shift banks the furnaces and climbs to the hill tunnels. The trunk line stops running at "
        "midnight.",
        "Foreign stations contradict one another all night. Reports of impacts arrive, are corrected, and arrive again with "
        "different coordinates. The wardens repeat whatever the movement's office passes down the telephone lines, and the "
        "office, it turns out, is listening to the same foreign broadcasts as the families sitting on crates in the cellars "
        "below it.",
        "At first light the shelters empty into streets that look exactly as they did the evening before. Nobody can yet say "
        "where the fragments landed or what they destroyed. The committee must choose between keeping the shelters manned, "
        "the trains stopped and the furnaces banked until the picture is clear, or sending the country back to work and "
        "trusting the sirens to sound again if anything falls late.",
    ), (
        Option('Keep the shelters manned for a week.', (WarSupport(0.02), Stability(-0.01))),
        Option('Send the country back to work.', (Stability(0.02), PP(10))),
    ), citation='date anchor only, ACES Chronicle row 1999 / 07.08; no damage in Monstrua is claimed', picture=1),
    EventDef('belkan_wire', 'Dispatches from the Belkan Front', (
        "The Belkan War, which broke out on 25 March 1995, reaches Monstrua as wire dispatches, grainy photographs and cables "
        "from attaches in foreign capitals. The movement's newspapers give whole pages to maps of the fighting. Monstruans "
        "raised on parades and weekend drill follow the campaign like a sporting season, arguing in the stairwells about "
        "armour, mountain passes and air power.",
        "The ministries watch different numbers. Convoy insurers raise their rates on every route that passes near the war. "
        "Foreign buyers send enquiries to the arms belt for shells, small arms and spares, some from governments the foreign "
        "desk would rather not answer at all. Oil prices climb, which helps the hill wells and hurts the air reserve's fuel "
        "budget in the same month.",
        "The committee must set the tone for the war years. It can let the newspapers celebrate the fighting as a lesson in "
        "national strength, which will please the youth columns and alarm the neighbours, or instruct them to report it "
        "soberly as a distant tragedy with consequences for prices and trade. Either line will shape how Monstruans read the "
        "next war too.",
    ), (
        Option('Let the newspapers celebrate.', (WarSupport(0.03), Stability(-0.01))),
        Option('Report the war soberly.', (Stability(0.02), WarSupport(-0.01))),
    ), citation='date anchor only, ACES Chronicle row 1995 / 03.25; Monstrua takes no part', picture=2),
    EventDef('usean_buyers', 'Who Still Has Fighters to Sell', (
        "Erusea's seizure of Stonehenge in the summer of 2003, and the railguns it turns on aircraft over Usea, send air "
        "staffs everywhere back to their arithmetic. By late August the FCU has founded the ISAF to oppose it. Aircraft are "
        "being lost faster than factories replace them, and governments far from Usea start looking for second-hand fighters "
        "to fill gaps of their own.",
        "Monstrua's air reserve keeps some twenty fighters and support aircraft in storage behind its front-line squadrons. "
        "Brokers arrive in Bufang within weeks, some speaking for governments the foreign desk knows, others for companies "
        "registered in ports it has never heard of. Their offers are generous. The air staff observes that generosity usually "
        "means somebody expects to lose aircraft soon.",
        "The committee must decide whether the stored airframes are a reserve or a stock for sale. Selling them to buyers well "
        "away from the fighting would earn hard currency and some goodwill. Keeping them would preserve a second line that "
        "Monstrua spent years assembling. The brokers, meanwhile, are content to wait in the capital's hotels for as long as "
        "the answer takes.",
    ), (
        Option('Hear the brokers out.', (PP(15), Stability(-0.01))),
        Option('Send the brokers home for now.', (WarSupport(0.02), PP(-10))),
    ), citation='date anchors only, ACES Chronicle rows 2003 / SUMMER and 2003 / 08.22; no Monstruan sale is claimed as fact',
        picture=1),
)

# --- branches ------------------------------------------------------------------------------------
MOVEMENT = Branch('movement', 'The Movement Without Rivals', 1991, 'FOCUS_FILTER_POLITICAL', (
    Focus('mv_ninety', 'Nine Monstruans in Ten',
          "The movement that governs Monstrua claims the loyalty of nine citizens in ten, and no vote has been counted since "
          "November 1987. The National Administration rules by ordinance while the old election calendar gathers dust. Before "
          "deciding what the movement should become, its senior committee orders a quiet count, district by district, of what "
          "that loyalty is actually made of.",
          ('assembly', 'command'), reward=(Idea('ninety_percent'), Event('loyalty_count'))),
    Focus('mv_stairwells', 'A Warden on Every Stairwell',
          "In the apartment blocks of Bufang and the Vuelona arms belt, the movement keeps a warden on each stairwell who knows "
          "every tenant by name. Paying the wardens a stipend and a desk at the district office turns gossip into "
          "administration. Complaints reach the ministries faster, and so do denunciations, which is why many tenants now speak "
          "quietly even in their own kitchens.",
          ('civil', 'security'), after=('mv_ninety',), reward=(TimedIdea('stairwell_wardens', 730),)),
    Focus('mv_columns', 'Columns of the Young',
          "The movement's youth columns march on every holiday and drill on weekends in forest camps above the Colmillo coast. "
          "Their numbers explain much of the country's warlike mood. Giving them army instructors and a written syllabus turns "
          "parades into skills that a reserve could use. Teachers complain that drill now competes with arithmetic for the same "
          "Saturday hours, and parents are divided.",
          ('training', 'assembly'), after=('mv_ninety',), reward=(Flag('columns_drilled'), XP('army', 10))),
    Focus('mv_cells_path', 'Party Cells for the Ministries',
          "The committee's hardliners argue that the movement already has the people and should now take the desks. Every "
          "ministry would receive a party cell with the right to review appointments and budgets, so that decisions follow the "
          "movement's line rather than the habits of the civil service. Senior clerks and officers who have run the state for "
          "years would answer to party secretaries half their age.",
          ('assembly', 'document'), after=('mv_stairwells', 'mv_columns'), exclusive=('mv_staff_path', 'mv_charter_path'),
          reward=(SwapIdea('ninety_percent', 'ministry_cells'),)),
    Focus('mv_staff_path', 'The Officers Put It in Writing',
          "A memorandum from the general staff circulates among the ministers. It says the marches and wardens have made the "
          "country loud but not strong, and that eight formations, two airfields and twenty plants need managers rather than "
          "speeches. The officers offer to govern through military districts until the state runs on professional lines. The "
          "movement reads the memorandum as ingratitude, and some of its authors as rivals.",
          ('command', 'document'), after=('mv_stairwells', 'mv_columns'), exclusive=('mv_cells_path', 'mv_charter_path'),
          reward=(SwapIdea('ninety_percent', 'staff_memorandum'),)),
    Focus('mv_charter_path', 'Talk of a Written Charter',
          "A minority inside the committee, joined by the few democrats and neutral notables who still meet openly, proposes a "
          "written charter: elections on a fixed calendar, a chamber that can refuse a budget and courts the movement does not "
          "appoint. They argue that a movement this popular can only gain from a counted vote. Hardliners answer that a counted "
          "vote is exactly how popular movements lose.",
          ('ballot', 'document'), after=('mv_stairwells', 'mv_columns'), exclusive=('mv_cells_path', 'mv_staff_path'),
          reward=(SwapIdea('ninety_percent', 'round_table'),)),
    Focus('mv_directorate', 'The Directorate Takes the Desks',
          "The senior committee reconstitutes itself as a directorate and takes the ministries outright. Party cells sign every "
          "appointment, the youth columns become a recognised arm of the state and the old ordinances are reissued as "
          "directorate decrees. Officers keep their commands but lose their independence. The Monstruan State now means the "
          "movement itself, and nobody is left to blame but the directorate.",
          ('command', 'assembly'), after=('mv_cells_path',), cost=10, exclusive=('mv_junta', 'mv_republic'),
          reward=(Regime('movement_directorate'), Flag('path_movement'))),
    Focus('mv_junta', 'The District Commanders Take the Seals',
          "The general staff forms a council of the four military district commanders and takes the government seals, keeping "
          "the movement's committee as an advisory body that is told rather than consulted. Wardens report to garrison "
          "officers and the columns to recruiting depots. The Monstruan Junta gains a disciplined administration and loses the "
          "mass enthusiasm that was the movement's only real asset.",
          ('command', 'security'), after=('mv_staff_path',), cost=10, exclusive=('mv_directorate', 'mv_republic'),
          reward=(Regime('district_council'), Flag('path_junta'))),
    Focus('mv_republic', 'A Republic Under the Charter',
          "The committee yields to the charter faction and proclaims the Monstruan Republic, with a provisional cabinet, a "
          "chamber to be elected within a year and courts named under the new text. Movement moderates reorganise as the "
          "largest party and expect to win any vote. What changes is that they now have to win it, and that losing would no "
          "longer be treason.",
          ('ballot', 'peace'), after=('mv_charter_path',), cost=10, exclusive=('mv_directorate', 'mv_junta'),
          reward=(Regime('charter_cabinet'), Flag('path_republic'))),
    Focus('mv_code', 'The Directorate Code',
          "The directorate replaces a decade of scattered ordinances with one code covering the press, the unions, the youth "
          "columns and the frontier. Officials finally know which rules apply, because the directorate wrote all of them, and "
          "production planners welcome the clarity. Monstruans who disagree learn that the code has a chapter on them too, and "
          "that the wardens have read it closely.",
          ('document', 'security'), after=('mv_directorate',), reward=(SwapIdea('ministry_cells', 'movement_code'),)),
    Focus('mv_districts', 'Four Districts, Four Commanders',
          "The junta divides the country into four military districts matching the four states, from the Colmillo coast to the "
          "Vuelona hills. Each district commander answers for roads, rations, recruiting and public order. The arrangement is "
          "tidy and fast. It also means that one poor commander can ruin a quarter of the country before the council in the "
          "capital notices anything is wrong.",
          ('command', 'rail'), after=('mv_junta',), reward=(SwapIdea('staff_memorandum', 'military_districts'),)),
    Focus('mv_first_ballot', 'Ballots Counted Again',
          "The first chamber election since 1987 runs under the new charter. The movement's successors win a clear majority, as "
          "everyone expected, but not every seat, and opposition deputies from the Colana plains and the Bufang docks take their "
          "places. Debates turn noisy and budgets slow down. For the first time the government's authority rests on a count that "
          "outsiders can check for themselves.",
          ('ballot', 'assembly'), after=('mv_republic',), reward=(SwapIdea('round_table', 'first_chamber'),)),
    Focus('mv_settled', 'One Answer Since 1987',
          "Whatever form the state took, the argument opened by the loyalty count gives way to ordinary government. Ministries "
          "know whom they answer to and the frontier posts know whose orders to follow. The losing factions remain, some in "
          "exile across the northern hills and some inside the governing camp itself. Outsiders can at least predict who will "
          "sign the decrees next month.",
          ('peace', 'document'), after_any=('mv_code', 'mv_districts', 'mv_first_ballot'),
          reward=(Flag('order_settled'), Stability(0.04))),
))

CAPITAL = Branch('capital', 'Colmillo and the Bufang Quays', 1991, 'FOCUS_FILTER_INTERNAL_AFFAIRS', (
    Focus('cap_quays', 'Count the Bufang Quays',
          "Bufang is the capital and the country's only naval base, and every merchant convoy Monstrua charters unloads at its "
          "quays. Nobody has measured how long a ship waits for a berth or how much cargo spoils in the sheds. A harbour survey "
          "answers both questions. Shipping agents cooperate eagerly; customs officers, who earn fees from the delays, "
          "cooperate rather less.",
          ('navy', 'document'), reward=(Idea('quay_survey'), Event('berth_queue'))),
    Focus('cap_cranes', 'New Cranes on the Merchant Quay',
          "The survey shows ships waiting days for three ageing cranes that break down every month. Buying modern cranes and "
          "laying a short rail spur along the merchant quay halves the time a ship spends in port. The cranes cost foreign "
          "currency the treasury would rather spend on aircraft, and the dock gangs fear that faster unloading means fewer "
          "shifts for them.",
          ('tools', 'navy'), after=('cap_quays',), reward=(SwapIdea('quay_survey', 'fast_quays'),)),
    Focus('cap_silo', 'Fill the Colmillo Fuel Silo',
          "The capital keeps the country's only fuel silo, and it has seldom been more than half full. Topping it up from the "
          "hill wells and holding a strategic reserve means aircraft and trucks keep moving through a blockade or a hard winter. "
          "The oil sits idle and earns nothing. Treasury officials call it the costliest tank in the country; the air staff "
          "calls it insurance.",
          ('logistics', 'security'), after=('cap_quays',), reward=(Flag('silo_full'), Research('synth_resources', 0.5, 1))),
    Focus('cap_rail_loop', 'The Bufang Rail Loop',
          "The line from the quays runs along the forested coast to the junction where the trunk line leaves for the other "
          "three states, then on to the second supply depot in southern Colmillo. Doubling the track and adding sidings at the "
          "junction lets freight leave the port without blocking passenger trains. Rail crews gain overtime, and a city park is "
          "lost to the new sidings.",
          ('rail', 'logistics'), after=('cap_quays',), reward=(Research('train_tech', 0.5, 1), TimedIdea('depot_sidings', 730))),
    Focus('cap_harbour_radar', 'A Radar Mast over Bufang',
          "Bufang's approaches have no radar, and the harbour master still counts ships through binoculars. A radar mast on the "
          "high ground above the port tracks shipping and low aircraft over the western sea. There are no warships to direct, "
          "but the air reserve gains warning time. Fishing crews grumble about the restricted zone drawn around the mast.",
          ('radar', 'navy'), after=('cap_cranes',), reward=(Build('radar_station', 1, 0),)),
    Focus('cap_movement_hall', 'A Movement Hall on the Quay',
          "Under the directorate, the movement builds its central hall beside the merchant quay, with offices for the youth "
          "columns, the wardens and the party press. Every arriving sailor walks past its banners. The hall becomes the real "
          "seat of government in the capital, and also the obvious target of every complaint the city has, because everyone "
          "knows where decisions are made.",
          ('assembly', 'navy'), after_any=('cap_rail_loop', 'cap_harbour_radar'), requires=(HasFlag('path_movement'),),
          reward=(Idea('quay_hall'),)),
    Focus('cap_garrison', 'The Garrison Holds Bufang',
          "Under the junta, the Colmillo district command moves into the harbour offices and runs the port as a military "
          "installation. Curfews end the dockside black market almost overnight. Merchant captains find the paperwork stricter "
          "and the bribes smaller. Residents grow used to patrols at every crossing and learn which officers can be approached "
          "and which cannot.",
          ('security', 'navy'), after_any=('cap_rail_loop', 'cap_harbour_radar'), requires=(HasFlag('path_junta'),),
          reward=(Idea('harbour_command'),)),
    Focus('cap_city_council', 'An Elected Council for Bufang',
          "Under the charter, the capital elects a city council for the first time in a generation. Its first budget repairs "
          "tram lines and the water mains of the dock wards before it touches a single monument. Movement councillors still hold "
          "the majority, but they must now explain their votes at public meetings, and petitions that once went to wardens go "
          "to elected members.",
          ('ballot', 'civil'), after_any=('cap_rail_loop', 'cap_harbour_radar'), requires=(HasFlag('path_republic'),),
          reward=(Idea('city_council'),)),
    Focus('cap_fair', 'A Trade Fair at Bufang',
          "Once the question of government is settled, the capital holds its first trade fair in years along the merchant "
          "quay. Buyers from across the sea inspect trucks, rail wagons, aluminium sheet and whatever else the plants can spare. "
          "Orders are modest. The fair matters more as a signal that Monstrua is open for business, whoever governs it, and "
          "the hotels are full for a week.",
          ('economy', 'diplomacy'), after_any=('cap_movement_hall', 'cap_garrison', 'cap_city_council'),
          requires=(HasFlag('order_settled'),), reward=(TimedIdea('bufang_fair', 365),)),
))

PLANTS = Branch('plants', 'Ten Halls and Ten Works', 1991, 'FOCUS_FILTER_INDUSTRY', (
    Focus('hall_ledger', 'Twenty Plants on One Ledger',
          "Monstrua runs ten civilian plants and ten arms halls, an even split that no planner ever chose on purpose. Vuelona "
          "holds four of the arms halls, Colmillo three, Garracia two and Colana one. A single ledger of output, machine age and "
          "missing parts gives the first honest picture of the economy, and plant directors who reported only good news must "
          "now explain themselves.",
          ('industry', 'document'), reward=(Idea('plant_ledger'), Event('ledger_returns'))),
    Focus('hall_spares', 'Replacement Parts Come First',
          "Planners have long measured success in new rifles, trucks and aircraft delivered. Yet half the trucks wait for parts, "
          "and the artillery parks strip some guns to keep others firing. A spares programme gives every plant a quota of "
          "replacement parts before any new item leaves the line. Output figures look worse for a year, and the equipment the "
          "country already owns begins to work.",
          ('tools', 'logistics'), after=('hall_ledger',), reward=(Idea('spares_quota'),)),
    Focus('hall_vuelona_yards', 'The Vuelona Arms Belt',
          "Vuelona is the most industrial state in the country, with four arms halls and three civilian plants, and not one "
          "mine or well of its own. Every ingot and barrel arrives over the hills by rail. Rebuilding the hall yards so that ore "
          "trains unload inside the walls saves days on each delivery. It also tells Vuelona plainly that it will always depend "
          "on the hills.",
          ('rail', 'industry'), after=('hall_ledger',), reward=(Research('industry', 0.5, 1), TimedIdea('vuelona_yards', 730))),
    Focus('hall_guns', 'Keep the Guns First',
          "One school of planners says the arms halls are the part of the economy that works best, and that a country with "
          "this much war support should lean on them. Credit and the best machine tools go to the arms belt, and the army and "
          "air reserve get their equipment on time. Shops stay thin, and the civilian plants run on whatever the halls discard.",
          ('missile', 'industry'), after_any=('hall_spares', 'hall_vuelona_yards'), cost=10,
          exclusive=('hall_shops', 'hall_motors'), reward=(SwapIdea('plant_ledger', 'guns_first'),)),
    Focus('hall_shops', 'Fill the Shop Windows',
          "A second school argues that the movement's popularity rests on promises of a better life that empty shops keep "
          "breaking. It wants credit, foreign tools and power supply moved to the civilian plants for household goods, building "
          "materials and farm equipment. Families notice within a year. The arms halls lose their priority, and the general "
          "staff counts every delayed delivery aloud.",
          ('economy', 'civil'), after_any=('hall_spares', 'hall_vuelona_yards'), cost=10,
          exclusive=('hall_guns', 'hall_motors'), reward=(SwapIdea('plant_ledger', 'shop_windows'),)),
    Focus('hall_motors', 'A Motor Works Economy',
          "The third school follows the research staff's priority of physical sustainment. It wants the country to specialise in "
          "what keeps everything else moving: trucks, rail wagons, engines and spare parts, sold to the army and abroad alike. "
          "The plan suits a country with a thousand trucks and one trunk line. It also ties industry to a narrow product range "
          "that foreign rivals already make more cheaply.",
          ('logistics', 'tools'), after_any=('hall_spares', 'hall_vuelona_yards'), cost=10,
          exclusive=('hall_guns', 'hall_shops'), reward=(SwapIdea('plant_ledger', 'motor_economy'),)),
    Focus('hall_fifth_hall', 'A Fifth Arms Hall at Vuelona',
          "Under the guns-first plan, Vuelona gets the country's newest arms hall on the last free plot of its industrial "
          "district, beside the coastal spur. Machine tools come from abroad on credit the treasury must repay in hard currency. "
          "The hall turns out shells and small arms within a year. City planners lose the land they had set aside for new "
          "housing.",
          ('industry', 'missile'), after=('hall_guns',), reward=(Build('arms_factory', 1, 439),)),
    Focus('hall_household', 'Household Goods from Vuelona',
          "Under the shop-window plan, the last free plot in Vuelona becomes a plant for stoves, bicycles, sewing machines and "
          "window glass. Workers who expected to make shells make kitchen goods instead, at lower wages and with less overtime. "
          "The products are plain and sell out within weeks, and the movement's newspapers photograph the queues as proof of "
          "success.",
          ('civil', 'industry'), after=('hall_shops',), reward=(Build('industrial_complex', 1, 439),)),
    Focus('hall_truck_works', 'Truck Works at the Junction',
          "Under the motor plan, the last free plot in Colmillo, beside the rail junction where the trunk line leaves the coast, becomes "
          "a truck and engine works. Parts arrive by rail and finished trucks leave the same way. The site is ideal and the "
          "neighbourhood is not consulted. The works grow quickly, and every truck they build shares the same few faults at "
          "first.",
          ('logistics', 'industry'), after=('hall_motors',), reward=(Build('industrial_complex', 1, 0),)),
    Focus('hall_tool_credit', 'Machine Tools on Credit',
          "Whatever the plan, nearly every plant in the country runs on machine tools older than most of its workers. A credit "
          "line abroad buys modern lathes, presses and gauges, installed one plant at a time. Productivity climbs wherever they "
          "arrive. The debt is in foreign currency, and the government must hope that exports grow faster than the interest "
          "does.",
          ('tools', 'economy'), after_any=('hall_fifth_hall', 'hall_household', 'hall_truck_works'),
          reward=(Idea('tool_credit'),)),
))

GROUND = Branch('ground', 'Oil and Ore in the Hills', 1992, 'FOCUS_FILTER_INDUSTRY', (
    Focus('ore_survey', 'Survey Wells and Ore Seams',
          "Three of Monstrua's four states hold oil, bauxite, iron ore and a little tungsten, spread through the Colmillo "
          "forests, the Garracia hills and the Colana plains. Vuelona, the busiest industrial state, holds none. A geological "
          "survey maps what each well and seam can deliver over ten years, and its findings will decide whether the country "
          "refines at home or sells raw material abroad.",
          ('tools', 'document'), reward=(Idea('survey_maps'), Event('survey_findings'))),
    Focus('ore_trust', 'A State Oil Trust',
          "One answer folds every well and mine into a single state trust that sells oil and ore only to Monstruan plants at "
          "fixed prices. The arms halls and the air reserve never go short of fuel or aluminium. Prices stay low inside the "
          "country and the treasury earns nothing abroad. Foreign drilling companies are told politely that their services "
          "are not required.",
          ('economy', 'command'), after=('ore_survey',), cost=10, exclusive=('ore_leases',),
          reward=(SwapIdea('survey_maps', 'oil_trust'),)),
    Focus('ore_leases', 'Drilling Leases for Foreigners',
          "The other answer offers twenty-year leases to foreign drilling and mining companies that pay royalties in hard "
          "currency and bring their own rigs. Output rises quickly. The movement's newspapers, which spent years denouncing "
          "foreign capital, must now explain why foreign engineers are welcome in the Garracia hills, and some of the oil "
          "leaves on foreign ships.",
          ('economy', 'diplomacy'), after=('ore_survey',), cost=10, exclusive=('ore_trust',),
          reward=(SwapIdea('survey_maps', 'drilling_leases'),)),
    Focus('ore_refinery', 'Refinery Sheds at Colana',
          "The trust builds its first processing plant on the last free plot in Colana, close to the eastern wells and the rail "
          "depot at the end of the trunk line. Crude oil and bauxite are treated there before travelling west to the arms belt. "
          "The plant is loud and smells for miles, and Colana farmers complain to the district office about their water.",
          ('industry', 'tools'), after=('ore_trust',), reward=(Build('industrial_complex', 1, 422),)),
    Focus('ore_terminal', 'A Lease Terminal at Colana',
          "The leaseholders build pumps, storage tanks and a loading works on the last free plot in Colana, between the coast "
          "and the rail depot. Oil goes out by sea and foreign machinery comes in. Local hiring is written into every lease. The "
          "terminal raises Colana's wages and its rents together, and the district office watches the foreign managers "
          "closely.",
          ('logistics', 'economy'), after=('ore_leases',), reward=(Build('industrial_complex', 1, 422),)),
    Focus('ore_aluminium', 'A Rolling Mill for Bauxite',
          "Bauxite from the hills has always left the country as ore, while the air reserve imports its aluminium sheet. A "
          "small rolling mill attached to the arms belt changes that. Airframe repair shops stop waiting for foreign "
          "deliveries, and engineers learn to work the metal at home. The mill draws power the civilian plants also need, and "
          "blackouts follow at first.",
          ('air', 'industry'), after_any=('ore_trust', 'ore_leases'),
          reward=(Research('excavation_tech', 0.5, 1), TimedIdea('aluminium_mill', 730))),
    Focus('ore_alloys', 'No Chromium at Home',
          "The survey confirms that Monstrua has no chromium at all, and its tungsten barely covers the arms belt's needs. Every "
          "gun barrel and engine part made of hard steel depends on imports. Long contracts with foreign suppliers and a "
          "stockpile in the Vuelona yards cushion the risk. The contracts are expensive, and they tie the country to sea lanes "
          "it cannot defend.",
          ('scales', 'document'), after=('ore_survey',), reward=(Idea('alloy_contracts'),)),
    Focus('ore_grades', 'Ore Trains Through Garracia',
          "Ore and crude reach Vuelona over the trunk line through the Garracia hills, where the spur to the frontier depot "
          "also branches off. The hill section is single track on steep grades. Easing the grades and adding passing loops lets "
          "heavier trains run. Garracia gains better roads beside the rail, and its hill villages lose some fields to the "
          "cuttings.",
          ('rail', 'bridge'), after_any=('ore_aluminium', 'ore_alloys'), reward=(Build('infrastructure', 1, 408),)),
    Focus('ore_rubber', 'Rubber for a Thousand Trucks',
          "The army runs more than a thousand trucks on rubber the country barely produces, and domestic deposits cover only a "
          "fraction of what the motor pool consumes. A small chemistry programme in the plant laboratories works on synthetic "
          "rubber and retreaded tyres. The chemists need years and imported equipment, and until they succeed every new truck "
          "is also a new import bill.",
          ('science', 'logistics'), after=('ore_alloys',), reward=(Research('synth_resources', 0.75, 1), PP(-15))),
))

ARMY = Branch('army', 'Eight Formations and the Columns', 1992, 'FOCUS_FILTER_MANPOWER', (
    Focus('army_muster', 'Muster of the Eight Formations',
          "Monstrua's army is eight infantry formations of five battalions each, backed by engineer and artillery companies and "
          "stores of nearly two thousand sets of infantry kit. Calling every formation to muster on one day shows the general "
          "staff how many soldiers answer, how many trucks start and how many guns fire. The movement's youth columns watch "
          "from the roadside, waiting to be asked.",
          ('training', 'command'), reward=(Idea('muster_rolls'), Event('columns_question'))),
    Focus('army_batteries', 'Massed Batteries',
          "The army's doctrine trusts in firepower, and two hundred and forty guns are its proudest possession. Many sit in "
          "depots with worn barrels and half-trained crews. Gathering them into a few well-drilled batteries, with spare barrels "
          "and live practice on the Vuelona ranges, makes them usable. Infantry commanders lose their own guns and must now "
          "request fire support like everyone else.",
          ('missile', 'training'), after=('army_muster',),
          reward=(Research('artillery', 0.5, 1), TimedIdea('battery_drill', 365))),
    Focus('army_sappers', 'Sappers for the Hill Roads',
          "Engineer companies are the army's most useful and least celebrated soldiers. Sending them to widen hill roads, bridge "
          "the Garracia streams and survey the Colana plains teaches them the ground and leaves something useful behind. Their "
          "equipment wears out faster on real work than on exercises, a price the general staff considers entirely fair.",
          ('bridge', 'tools'), after=('army_muster',), reward=(Research('engineers_tech', 0.5, 1), XP('army', 10))),
    Focus('army_fold', 'Fold the Columns into the Army',
          "The cleanest answer to the columns question puts every drilled member of the youth columns on the army's reserve "
          "rolls, with regular officers in command and the movement's banners left at home. The army gains a deep reserve of "
          "willing recruits. The movement loses its own uniformed arm, and the committee suspects the generals have just "
          "doubled their strength at its expense.",
          ('training', 'security'), after_any=('army_batteries', 'army_sappers'), cost=10,
          exclusive=('army_guard', 'army_home'), requires=(HasFlag('columns_drilled'),), reward=(Idea('column_reserve'),)),
    Focus('army_guard', 'A Party Guard Apart',
          "The committee's answer keeps the columns under its own command as a party guard, with uniforms, rifles and barracks "
          "beside the army's. The guard protects ministries, rallies and the stairwell wardens, and it answers to the movement "
          "rather than the general staff. Two armed services now share one small country, and their officers watch each other "
          "more closely than the frontier.",
          ('security', 'assembly'), after_any=('army_batteries', 'army_sappers'), cost=10,
          exclusive=('army_fold', 'army_home'), reward=(Idea('party_guard'),)),
    Focus('army_home', 'Send the Columns Home',
          "A third answer stands the columns down entirely. Their rifles return to army depots, their camps become schools and "
          "their members go back to study and work. The movement loses its loudest arm and the army loses a reserve it never "
          "fully trusted. Families welcome their children home on Saturdays, while hardliners call the decision a disarming of "
          "the nation's spirit.",
          ('peace', 'civil'), after_any=('army_batteries', 'army_sappers'), cost=10,
          exclusive=('army_fold', 'army_guard'), reward=(Idea('columns_stood_down'),)),
    Focus('army_column_battalions', 'Reserve Battalions of Former Columns',
          "Former column members on the reserve rolls are formed into battalions of their own, recruited by district so that "
          "neighbours serve together. They train for a fortnight each summer under regular officers. Recruiting becomes almost "
          "effortless. The battalions carry the columns' habits of loud loyalty into the army, which some regular officers find "
          "useful and others find tiresome.",
          ('medal', 'training'), after=('army_fold',), reward=(SwapIdea('column_reserve', 'column_battalions'),)),
    Focus('army_guard_barracks', 'Guard Barracks by the Ministries',
          "The party guard receives permanent barracks beside each ministry and at the main rail depots, with its own armoury "
          "and pay scale. Ministers feel protected, and the general staff feels watched. The guard's budget comes partly from "
          "the army's, which the officers do not forget. Order in the capital is firm, and its keepers answer to the committee "
          "alone.",
          ('security', 'command'), after=('army_guard',), reward=(SwapIdea('party_guard', 'guard_barracks'),)),
    Focus('army_camp_schools', 'Camps Become Technical Schools',
          "The forest camps where the columns used to drill reopen as technical schools that teach welding, wiring and engine "
          "repair on the same weekend timetable. Many former column members enrol, and the plants gain trained hands within two "
          "years. The movement loses a ritual it valued. The country gains mechanics, which the motor pool and the air reserve "
          "both need badly.",
          ('science', 'civil'), after=('army_home',), reward=(SwapIdea('columns_stood_down', 'camp_schools'),)),
    Focus('army_hill_companies', 'Mountain Companies for Garracia',
          "Garracia's hills face the Aquitorian frontier, and the army has kept mountain training on its books for years "
          "without a unit that uses it. One battalion from each formation now spends a season in the Garracia hills learning "
          "to move and fight on slopes. Training accidents rise. The battalions come back able to hold ground the rest of the "
          "army can barely cross.",
          ('training', 'tools'), after=('army_sappers',), reward=(Idea('hill_companies'),)),
    Focus('army_staff_school', 'A Staff School for Firepower',
          "Officers learned the firepower doctrine from manuals written for a larger and richer army. A staff school in Colmillo "
          "rewrites it for eight formations, two hundred and forty guns and a thousand trucks. Classes teach how to plan fire, "
          "move ammunition and keep batteries supplied along a single railway. The school takes good officers out of their "
          "units for a year at a time.",
          ('command', 'document'), after_any=('army_column_battalions', 'army_guard_barracks', 'army_camp_schools'),
          reward=(Research('land_doctrine', 0.5, 1), XP('army', 20))),
))

AIR = Branch('air', 'Eighty-Four Aircraft, Two Fields', 1992, 'FOCUS_FILTER_AIR_XP', (
    Focus('air_two_fields', 'Two Fields for Eighty-Four Aircraft',
          "The air reserve flies seventy-two fighters and a dozen ground support aircraft from just two airfields, the capital "
          "field and a small strip in Colana, with more airframes in storage. It is a large air arm for so small a country, "
          "and it is parked wing to wing. A single bad night could destroy half of it on the ground, so the air staff asks for "
          "room.",
          ('air', 'runway'), reward=(Idea('crowded_fields'), Event('crowded_aprons'))),
    Focus('air_colana', 'Widen the Colana Strip',
          "The Colana strip on the eastern plain has one short runway and a few hangars. Lengthening the runway and adding "
          "dispersal pens makes it a proper second base, closer to both northern frontiers than the capital is. Farmland around "
          "the strip is bought at prices the farmers call insulting. Within a year the fighters on the capital field have room "
          "to breathe.",
          ('runway', 'tools'), after=('air_two_fields',), reward=(Build('air_base', 2, 422),)),
    Focus('air_garracia', 'Dispersal Strips in the Garracia Hills',
          "Short grass strips and camouflaged pens in the Garracia hills give the air reserve somewhere to scatter if the main "
          "fields are threatened. The strips are rough, and aircraft flying from them need more maintenance. Hill villagers see "
          "fighters overhead for the first time. The air staff sleeps better knowing that the reserve no longer sits in two "
          "baskets.",
          ('runway', 'security'), after=('air_two_fields',), reward=(Build('air_base', 2, 408),)),
    Focus('air_vuelona', 'A Southern Field at Vuelona',
          "Vuelona, the busiest industrial state, has no airfield of its own, and its arms halls rely on fighters scrambled "
          "from the capital. A field on the coastal plain of southern Vuelona puts interceptors over the arms belt within "
          "minutes. The land is valuable and the halls want it for storage. The air staff wins the argument by promising to buy "
          "locally made spares.",
          ('air', 'industry'), after_any=('air_colana', 'air_garracia'), reward=(Build('air_base', 2, 439),)),
    Focus('air_home_sky', 'Guard the Home Sky',
          "One doctrine makes the air reserve an interceptor force that exists to keep foreign aircraft out of Monstruan skies. "
          "Pilots train for altitude, speed and radar-directed intercepts over the coast. The ground support aircraft are kept "
          "but get the oldest engines. It suits a country that expects to defend itself, and it leaves the army fighting under "
          "an empty sky.",
          ('air', 'radar'), after_any=('air_colana', 'air_garracia'), cost=10, exclusive=('air_battery_wings',),
          reward=(SwapIdea('crowded_fields', 'home_sky'),)),
    Focus('air_battery_wings', 'Wings for the Batteries',
          "The other doctrine ties the air reserve to the army's firepower school. Fighters escort ground support aircraft that "
          "strike what the batteries cannot reach, and pilots train beside artillery observers on the Vuelona ranges. The army "
          "welcomes the attention. Air defence of the capital becomes an afterthought, and interceptor pilots resent flying "
          "escort for someone else's battle.",
          ('missile', 'air'), after_any=('air_colana', 'air_garracia'), cost=10, exclusive=('air_home_sky',),
          reward=(SwapIdea('crowded_fields', 'battery_wings'),)),
    Focus('air_radar_chain', 'Radar on the Northern Coast',
          "The interceptor doctrine needs warning, and the northern coast has almost none. Radar posts on the Garracia shore, "
          "above the bay that Monstrua shares with Aquitoria and Valka, track aircraft long before they cross the coast, and "
          "controllers in the capital vector fighters toward them. The posts are lonely duty and the sets need constant "
          "repair.",
          ('radar', 'communications'), after=('air_home_sky',),
          reward=(Build('radar_station', 1, 408), Research('radar_tech', 0.5, 1))),
    Focus('air_forward_strip', 'Forward Strip Behind the Guns',
          "The support doctrine needs aircraft close to the batteries they serve. A forward strip beside the Vuelona artillery "
          "ranges lets ground support aircraft refuel and rearm between sorties without flying back to the capital. Pilots and "
          "gunners learn each other's language in the same mess hall. The strip is muddy most of the year and hard on "
          "undercarriages.",
          ('runway', 'missile'), after=('air_battery_wings',), reward=(Build('air_base', 1, 439), XP('air', 15))),
    Focus('air_school', 'A Flying School at Colana',
          "Pilots now learn to fly on the same crowded fields where operational squadrons stand alert, and accidents follow. A "
          "flying school at the widened Colana strip separates training from operations, with its own trainers, instructors "
          "and syllabus. Graduates reach their squadrons ready to fly. The school ties up experienced pilots as instructors, and "
          "squadron commanders resent the loss.",
          ('training', 'air'), after=('air_colana',), reward=(Idea('colana_school'),)),
    Focus('air_weekend_pilots', 'Weekend Pilots of the Reserve',
          "The air reserve is meant to be a reserve, yet nearly all its pilots serve full time. Training former pilots and "
          "qualified civilians to fly at weekends, with a call-up in any crisis, doubles the pool without doubling the budget. "
          "Weekend flyers are rusty and keen in equal measure, and squadron commanders must keep aircraft free for them every "
          "Saturday.",
          ('medal', 'air'), after=('air_school',), reward=(Idea('weekend_reserve'),)),
    Focus('air_long_patrols', 'Long Patrols on Silo Fuel',
          "With the Colmillo silo full, the air reserve can fly patrols that used to be cancelled for want of fuel. Fighters "
          "stay aloft longer over the coast, and pilots log the hours their syllabus demands. The silo drains faster than the "
          "treasury likes. The air staff argues that fuel kept in a tank is worth less than pilots who know their aircraft.",
          ('air', 'logistics'), after_any=('air_home_sky', 'air_battery_wings'), requires=(HasFlag('silo_full'),),
          reward=(TimedIdea('patrol_hours', 365), XP('air', 15))),
))

FRONTIERS = Branch('frontiers', 'Neighbours by Land and Sea', 1993, 'FOCUS_FILTER_POLITICAL', (
    Focus('fr_envoys', 'Envoys North to Two Capitals',
          "Monstrua shares its northern frontiers with Aquitoria, a crown government whose chamber has been shut since 1987, "
          "and with Valka, whose public is split almost evenly between a nationalist camp and a non-aligned one. The movement "
          "sends envoys to both capitals with short, formal notes asking where each stands on frontier patrols and on the "
          "Monstruan exiles living north of the hills.",
          ('diplomacy', 'document'), reward=(Idea('northern_watch'), Event('envoys_report'))),
    Focus('fr_market_post', 'Our End of the Market Road',
          "Garracia hill farmers have always carried produce down to the plain markets across the frontier. A customs post at "
          "the Monstruan end turns the trail into lawful trade and gives the district office a count of who crosses and with "
          "what. The movement posts more uniformed men there than trade alone requires. Farmers resent the questions and pay "
          "the duties anyway.",
          ('economy', 'security'), after=('fr_envoys',), reward=(TimedIdea('market_road_post', 730),)),
    Focus('fr_exile_lists', 'Lists for the Aquitorian Crown',
          "The committee knows the names of the exiles who crossed the northern hills, and it can send those names to the "
          "Aquitorian crown office with a request for surveillance and closed doors. Aquitoria may or may not oblige. Either "
          "way the exiles learn they are watched, and some stop writing home. Opposition papers in the north will print the "
          "lists as proof of Monstruan reach.",
          ('document', 'security'), after=('fr_market_post',), exclusive=('fr_safe_return',), reward=(Idea('exile_lists'),)),
    Focus('fr_safe_return', 'Letters of Safe Return',
          "The opposite course offers the exiles letters of safe return: no prosecution for past membership of banned clubs, "
          "restored property and the right to work, provided they come home and stay out of politics. A few return, mostly the "
          "old and the homesick. Those who remain north are now visibly choosing exile, and hardliners call the offer an "
          "invitation to every critic.",
          ('peace', 'refugees'), after=('fr_market_post',), exclusive=('fr_exile_lists',), reward=(Idea('return_letters'),)),
    Focus('fr_frontier_files', 'Frontier Files at Garracia',
          "With the lists sent north, the frontier police at the Garracia post open a file on everyone who uses the market road. "
          "Couriers, letters and parcels are opened and copied. The files catch a few smugglers and inconvenience many farmers. "
          "Exiles stop using the road altogether, which the committee counts as a success and the market traders count as lost "
          "custom.",
          ('document', 'gate'), after=('fr_exile_lists',), reward=(SwapIdea('exile_lists', 'frontier_files'),)),
    Focus('fr_returning_families', 'The First Returning Families',
          "The first families to accept the letters arrive at the Garracia post with their belongings on hired trucks. The "
          "district office finds them flats, jobs and a warden who calls every week. Their stories of life in the north travel "
          "through every stairwell. Some are grateful to be home; others are already quietly asking whether they made a "
          "mistake.",
          ('refugees', 'civil'), after=('fr_safe_return',), reward=(SwapIdea('return_letters', 'returning_families'),)),
    Focus('fr_valka_siding', 'A Siding Facing Valka',
          "Colana touches Valka at a single plains crossing near the coast, and trade across it moves on carts and small trucks. "
          "A freight siding from the Colana depot to the crossing lets wagons reach the frontier post directly. Valkan traders "
          "gain a shorter route to Monstruan markets, and Monstruan customs officers gain a busier post and a clearer view of "
          "who comes south.",
          ('rail', 'diplomacy'), after=('fr_envoys',),
          reward=(Build('infrastructure', 1, 422), TimedIdea('valka_freight_siding', 730))),
    Focus('fr_valka_friends', 'Friends in the Valkan Camp',
          "Half of the Valkan public leans toward its nationalist camp, and the movement's newspapers speak warmly of it. "
          "Cultivating that camp with invitations, student places and printing presses wins sympathy across the frontier. It "
          "also tells the Valkan government that Monstrua is meddling in its politics. No alliance is offered and no faction "
          "joined; the friendship stays in print and in meeting halls.",
          ('diplomacy', 'assembly'), after=('fr_valka_siding',), exclusive=('fr_valka_correct',),
          reward=(Idea('valkan_friends'),)),
    Focus('fr_valka_correct', 'Correct Relations with Valka',
          "The alternative deals only with the Valkan government, whichever camp it leans toward, and keeps the movement's "
          "newspapers out of Valkan politics. Envoys discuss freight, water and fishing rather than ideology. The Valkan "
          "nationalists feel snubbed. The Valkan government finds that its southern neighbour, whatever else it may be, keeps "
          "its word on small matters.",
          ('diplomacy', 'scales'), after=('fr_valka_siding',), exclusive=('fr_valka_friends',),
          reward=(Idea('valka_correct'),)),
    Focus('fr_southern_sea', 'Freight Across the Southern Sea',
          "Sotoa lies across the southern waters from Vuelona and Colana, close enough for small freighters, yet most Monstruan "
          "trade with it passes through middlemen in other ports. Direct sailings from Bufang under a simple freight agreement "
          "cut those middlemen out. Sotoan goods appear in Monstruan shops, and the movement must decide what it thinks of a "
          "neighbour it rarely mentions.",
          ('navy', 'economy'), after=('fr_envoys',), reward=(TimedIdea('southern_crossing', 730),)),
))

ASTEROID = Branch('asteroid', 'Ulysses and the Shelters', 1994, 'FOCUS_FILTER_STABILITY', (
    Focus('sky_warning', 'The Astronomers Speak',
          "The International Astronomical Union's warning of December 1994, that Ulysses will come near the Earth and might hit "
          "it, finds Monstrua with no observatory able to check the claim and no plan for the case that it is true. The "
          "movement's committee forms a standing body on the asteroid. Its first instinct is to control the news; its second is "
          "to ask the army how deep it can dig.",
          ('meteor', 'telescope'), requires=(After('1994.12.10'),),
          reward=(Idea('impact_committee'), Event('sky_warning'))),
    Focus('sky_one_voice', 'One Voice on the Radio',
          "One answer puts every bulletin about the asteroid through a single movement office. Radio, newspapers and stairwell "
          "wardens repeat the same calm message, and rumour is treated as sabotage. Panic is rare. So is trust: when the office "
          "later has bad news to give, Monstruans who have learned to read between its lines will assume the truth is worse.",
          ('communications', 'security'), after=('sky_warning',), exclusive=('sky_open_figures',),
          reward=(Idea('single_bulletin'), Flag('news_controlled'))),
    Focus('sky_open_figures', 'Publish the Orbit Figures',
          "The other answer publishes everything the foreign observatories release, with plain explanations from university "
          "physicists on the radio every week. Some families panic and hoard food. Others begin digging cellars on their own "
          "initiative. The movement loses control of the story, but the public learns to tell a measured risk from a rumour, "
          "which will matter as the risk grows.",
          ('telescope', 'document'), after=('sky_warning',), exclusive=('sky_one_voice',),
          reward=(Idea('open_figures'), Flag('news_open'))),
    Focus('sky_cellars', 'Cellars Under Bufang',
          "The merchant cellars beneath the Bufang quay district already run deep and connect in places. Engineers join them "
          "into shelters with ventilation shafts, water tanks and medical posts for a large share of the capital's people. The "
          "work disrupts the port district for two years. Merchants who lose their cellars receive compensation, though rarely "
          "as much as they ask.",
          ('shelter', 'civil'), after_any=('sky_one_voice', 'sky_open_figures'), reward=(Idea('quay_cellars'),)),
    Focus('sky_tunnels', 'Tunnels in the Vuelona Hills',
          "The Vuelona arms belt lies below wooded hills, and the army proposes cutting shelter tunnels into them for the "
          "workers and their families. Tunnels cost less per person than cellars and resist blast better, but they are a long "
          "walk from the tenements. The halls lose shifts to tunnel duty, and the finished galleries double as protected stores.",
          ('shelter', 'tools'), after_any=('sky_one_voice', 'sky_open_figures'), reward=(Idea('hill_tunnels'),)),
    Focus('sky_announced', 'The FCU Confirms the Strike',
          "In April 1996 the FCU announces that Ulysses will strike the Earth, and where its fragments will fall is still "
          "uncertain. The committee doubles the shelter budget, orders six months of grain into store and makes shelter drills "
          "compulsory in every block. The bill lands on the plants' budgets, and nobody in the governing camp argues against it "
          "in public.",
          ('meteor', 'shelter'), after_any=('sky_cellars', 'sky_tunnels'), requires=(After('1996.4.20'),),
          reward=(SwapIdea('impact_committee', 'impact_programme'),)),
    Focus('sky_quiet_bill', 'The Shelter Bill Stays Quiet',
          "Because every asteroid bulletin passes through one office, the cost of the shelters never appears in print. The "
          "plants absorb it as overhead and the ministries report only completed galleries. The public sees progress and no "
          "price. Plant directors know exactly what they paid, and they expect the favour returned when the next quota is set.",
          ('document', 'economy'), after=('sky_announced',), requires=(HasFlag('news_controlled'),),
          reward=(Idea('quiet_bill'),)),
    Focus('sky_open_ledger', 'Print the Shelter Accounts',
          "Having published the orbit figures, the government can hardly hide the shelter accounts. Each district receives a "
          "printed statement of what its cellars and tunnels cost, who built them and how many people they hold. Some districts "
          "complain loudly about the comparison. Others start raising money for extra galleries, which is more than any decree "
          "achieved.",
          ('scales', 'shelter'), after=('sky_announced',), requires=(HasFlag('news_open'),),
          reward=(Idea('shelter_accounts'),)),
    Focus('sky_roche', 'The Roche Limit Night',
          "Ulysses reaches the Roche limit on 8 July 1999 and starts breaking up. Monstrua spends the night in its "
          "cellars and tunnels, listening to foreign radio. The trunk line stops and the furnaces are banked. By dawn the "
          "country must decide how long to stay underground, and every hour of caution costs output it will not recover.",
          ('meteor', 'communications'), after=('sky_announced',), requires=(After('1999.7.8'),),
          reward=(Event('roche_night'),)),
    Focus('sky_fragment_watch', 'Watching for Late Fragments',
          "Pieces of the asteroid will keep coming down for years, and nobody can predict where each will land. A radar post on "
          "the Vuelona coast, wired to the shelter sirens, gives the arms belt a few minutes' warning of anything large entering "
          "the sky. Most alarms prove false. Workers learn to walk, not run, to the tunnels, which is itself a kind of victory.",
          ('radar', 'meteor'), after=('sky_roche',), reward=(Build('radar_station', 1, 439),)),
))

BELKA = Branch('belka', 'The Belkan War on the Wire', 1995, 'FOCUS_FILTER_WAR_SUPPORT', (
    Focus('bw_outbreak', 'War Breaks Out in Belka',
          "On 25 March 1995 war breaks out in Belka, far from Monstrua's coasts. The movement's newspapers follow every report "
          "with the enthusiasm of a public raised on parades. The ministries ask a harder question: what does a distant war "
          "mean for convoy rates, oil prices and the buyers who keep the arms belt busy? The answer will set the tone of the "
          "war years.",
          ('communications', 'command'), requires=(After('1995.3.25'),),
          reward=(TimedIdea('war_news', 365), Event('belkan_wire'))),
    Focus('bw_attaches', 'Attaches Read the Reports',
          "Monstrua has no observers at the front, but its attaches in friendly capitals gather every report, photograph and "
          "rumour about the fighting. The general staff studies how air power, mountain passes and fortified lines shape the "
          "campaign. The lessons are second-hand and often wrong. They are still the only modern war Monstruan officers can "
          "study without paying for it.",
          ('document', 'air'), after=('bw_outbreak',),
          reward=(Research('air_doctrine', 0.5, 1), Research('land_doctrine', 0.5, 1))),
    Focus('bw_waldreich', 'After the Waldreich Flashes',
          "In June 1995 the Belkan Army uses seven nuclear devices in the Waldreich Mountains. Monstrua is far from the blasts, "
          "yet the news reaches every stairwell within a day. The committee buys radiation counters for the Bufang quays and "
          "the Colana depot, stocks iodine in every district and explains on the radio what the danger is and is not. Each step "
          "costs money and calm.",
          ('medical', 'security'), after=('bw_outbreak',), requires=(HasGlobal('belka_dropped_nukes'), After('1995.6.6')),
          reward=(Idea('fallout_monitors'),)),
    Focus('bw_lumen', 'The Lumen Treaty and the Arms Belt',
          "On 20 June 1995 a treaty signed in Lumen ends the Belkan War. Convoy insurers lower their rates within weeks, and "
          "foreign buyers withdraw half their enquiries to the arms belt. The planners face the familiar postwar problem of "
          "halls sized for a market that has just closed. The movement's newspapers call the peace a pause, which is what they "
          "call every peace.",
          ('peace', 'industry'), after=('bw_outbreak',), requires=(After('1995.6.20'),),
          reward=(TimedIdea('postwar_lull', 365),)),
    Focus('bw_belka_lost', 'A Lesson from Belka Defeated',
          "Belka, whose armies the Monstruan press praised all spring, has lost its war to a coalition of neighbours. Officers "
          "who admired its divisions draw an uncomfortable conclusion: firepower and discipline did not save a country that "
          "stood alone. The committee orders a review of every frontier arrangement and trade partner, and the newspapers stop "
          "praising Belkan generals.",
          ('document', 'diplomacy'), after=('bw_lumen',), requires=(HasGlobal('belka_lost_belkan_war'),),
          reward=(Idea('isolation_lessons'),)),
    Focus('bw_belka_won', 'Belka Holds Its Ground',
          "In this course of events Belka comes out of the war with its armies intact and its enemies divided. The Monstruan "
          "press treats the result as proof that a disciplined state can face a coalition and win. The general staff is more "
          "cautious. Foreign buyers, though, suddenly want weapons proven in the Belkan manner, and the arms belt receives "
          "enquiries it never expected.",
          ('missile', 'economy'), after=('bw_lumen',), requires=(HasGlobal('belka_won_belkan_war'),),
          reward=(TimedIdea('belkan_style_orders', 365),)),
    Focus('bw_sanctions', 'Watching the Estovakian Sanctions',
          "In March 2002 Osea, Emmeria and other nations join economic sanctions against Estovakia, citing its internal "
          "corruption. Monstrua is no party to the dispute, but its government counts no votes either, and the committee reads "
          "the news carefully. The ministries quietly list which imports could be cut off and how long the country could manage "
          "without each of them.",
          ('scales', 'document'), after=('bw_lumen',), requires=(After('2002.3.20'),), reward=(Idea('sanctions_review'),)),
))

USEA = Branch('usea', 'Stored Airframes and the Usean War', 2003, 'FOCUS_FILTER_AIR_XP', (
    Focus('us_railguns', 'Stonehenge Fires on Aircraft',
          "In the summer of 2003 Erusea invades the neutral country of San Salvacion, seizes the Stonehenge railgun complex and "
          "turns its guns on aircraft. Usea is very far from Monstrua, but every air staff in the world studies what follows. "
          "Buyers on several continents begin asking who still has fighters to sell, and Monstrua's air reserve keeps airframes "
          "in storage.",
          ('missile', 'air'), requires=(After('2003.9.1'),), reward=(Event('usean_buyers'),)),
    Focus('us_sell', 'Sell the Stored Airframes',
          "The air reserve keeps more than twenty fighters and support aircraft in storage beyond its front-line strength. "
          "Selling them to buyers far from Usea, with spares and training contracts, earns hard currency at the best prices in a "
          "decade. The reserve thins. If the next crisis comes to Monstrua rather than to a distant continent, those airframes "
          "will not be waiting.",
          ('air', 'economy'), after=('us_railguns',), cost=10, exclusive=('us_keep',), reward=(Idea('airframe_sales'),)),
    Focus('us_keep', 'Every Airframe Stays Home',
          "The air staff argues that a war in which railguns shoot down aircraft shows how quickly an air arm can be consumed. "
          "Every stored airframe stays in its hangar, rotated and maintained, and no Monstruan aircraft is sold while the Usean "
          "war lasts. Buyers go elsewhere and the treasury gives up the income. The reserve stays whole, at least on paper.",
          ('air', 'shelter'), after=('us_railguns',), cost=10, exclusive=('us_sell',), reward=(Idea('hangar_reserve'),)),
    Focus('us_refit', 'Refit What Remains',
          "The sale money pays for new engines, avionics and spares for the aircraft Monstrua kept. Front-line squadrons fly "
          "better machines than before, though fewer of them, and mechanics trained on the sold types retrain on the survivors. "
          "The air staff accepts the bargain grudgingly and keeps a list of every airframe it would buy back if it could.",
          ('tools', 'air'), after=('us_sell',), reward=(SwapIdea('airframe_sales', 'refitted_squadrons'),)),
    Focus('us_rotate', 'Rotation in the Storage Hangars',
          "Stored aircraft decay if they are simply left alone. A rotation schedule brings every airframe out twice a year for "
          "engine runs, test flights and inspection by the weekend reserve crews. The schedule costs fuel and mechanic hours. "
          "It turns a stockpile of ageing airframes into a genuine second line that could fly within days of a call-up.",
          ('runway', 'training'), after=('us_keep',), reward=(SwapIdea('hangar_reserve', 'rotated_hangars'),)),
    Focus('us_isaf_outcome', 'The Coalition Wins in Usea',
          "The ISAF's victory ends the Usean war with Erusea defeated and the railguns silent. Prices for second-hand fighters "
          "collapse within months, and brokers who crowded the capital's hotels disappear. Monstrua's air staff studies how a "
          "coalition rebuilt an air arm from near destruction, and concludes that pilots and spares mattered more than the "
          "number of airframes.",
          ('medal', 'air'), after_any=('us_refit', 'us_rotate'), requires=(HasGlobal('ac_ucw_outcome_isaf_victory'),),
          reward=(Research('air_doctrine', 0.75, 1), Stability(0.02))),
    Focus('us_erusea_outcome', 'Erusea Prevails in Usea',
          "In this course of events Erusea ends the war holding the field, and the railgun complex is proven as a weapon that "
          "can close a whole sky. Monstruan officers draw the obvious conclusion for a small country with eighty-odd aircraft: "
          "ground defences matter as much as fighters. The air staff begins asking what radar and guns would cost along every "
          "coast.",
          ('radar', 'security'), after_any=('us_refit', 'us_rotate'), requires=(HasGlobal('ac_ucw_outcome_erusean_victory'),),
          reward=(Research('radar_tech', 0.75, 1), WarSupport(0.02))),
    Focus('us_stalemate_outcome', 'No Victor in Usea',
          "In this course of events the Usean war ends without a decision, and neither side can claim the continent. Buyers keep "
          "asking for aircraft because nobody believes the quiet will last. Monstrua's foreign desk advises caution: a war that "
          "pauses can resume, and fighters sold into it can return to the market, or to the sky, in unexpected hands.",
          ('scales', 'air'), after_any=('us_refit', 'us_rotate'), requires=(HasGlobal('ac_ucw_outcome_stalemate'),),
          reward=(PP(30), Research('air_doctrine', 0.5, 1))),
    Focus('us_account', 'Fifteen Years in Plain Figures',
          "As the Usean war winds down in 2005, the government publishes a plain account of what the years since 1991 cost and "
          "taught: the question of who governs, the shelters, the plants, the frontiers and the air reserve. It promises nothing "
          "about the coming decade. It does give whoever governs next a record of what the country can and cannot do alone.",
          ('document', 'peace'), after_any=('us_refit', 'us_rotate'), requires=(After('2005.6.1'),),
          reward=(Idea('decade_account'),)),
))

BRANCHES = (MOVEMENT, CAPITAL, PLANTS, GROUND, ARMY, AIR, FRONTIERS, ASTEROID, BELKA, USEA)

# --- decisions -----------------------------------------------------------------------------------
DECISIONS = (
    DecisionDef('rally_day', 'Proclaim a National Rally Day',
                'The movement fills every square for a day of marches and speeches. Repeatable once a year while the charter has '
                'not replaced the movement.',
                25, (TimedIdea('rally_fervour', 60), WarSupport(0.01)),
                requires=(Completed('mv_ninety'), NotFlag('path_republic')), cooldown=365),
    DecisionDef('weekend_callup', 'Call the Weekend Pilots Up',
                'The weekend reserve flies a full week beside the front-line squadrons. Repeatable every six months; it costs '
                'fuel and lost working days.',
                30, (TimedIdea('callup_exercise', 60), XP('air', 10)), requires=(Completed('air_weekend_pilots'),), cooldown=180),
    DecisionDef('trunk_priority', 'Clear the Trunk Line for Troops',
                'Battalions move the length of the country by rail while civilian freight waits in the sidings. Repeatable every '
                'six months.',
                30, (TimedIdea('trunk_clearance', 60), XP('army', 10)), requires=(Completed('army_muster'),), cooldown=180),
    DecisionDef('hill_strip', 'Grade Another Hill Strip',
                'Pays for one more graded strip and pen in the Garracia hills. A one-time charge on the air budget.',
                60, (Build('air_base', 1, 408),), requires=(Completed('air_garracia'),)),
    DecisionDef('market_day', 'Hold a Market Day at the Post',
                'The Garracia customs post opens for a day of trade with fewer questions asked. Repeatable once a year.',
                20, (TimedIdea('market_day_crowds', 90), Stability(0.01)), requires=(Completed('fr_market_post'),), cooldown=365),
    DecisionDef('siren_drill', 'Sound the Shelter Sirens',
                'Every district walks to its shelters on the sirens and is counted at the door. Repeatable every six months.',
                25, (TimedIdea('siren_drill', 90), WarSupport(0.01)), requires=(Completed('sky_cellars'),), cooldown=180),
)
