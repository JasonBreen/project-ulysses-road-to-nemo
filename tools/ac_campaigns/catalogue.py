"""Reviewable campaign capabilities and operations; all mechanics are provisional.

Official framing is cited in sources.json. No operation asserts combat telemetry,
an order of battle, geography or a historical outcome merely because time passed.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Nation:
    tag: str
    name: str
    lanes: tuple
    themes: tuple
    policies: tuple
    after: str


# A lane has a register, two alternative policies, preparation, review and a
# standing account. Its preparation unlocks an operation, not an abstract score.
NATIONS = (
    Nation('ERU','Erusea',('Occupation authority','Service before legend','The continental position','Orders after defeat'),('security','tools','command','peace'),(('Civil guarantees','Military discretion'),('Preserve the maintenance reserve','Demand immediate readiness'),('Authorize an orderly withdrawal','Hold the final positions'),('Hear the occupation cases','Keep the command account')),'2000.1.1'),
    Nation('FCU','Central Usea and ISAF',('Consent to command','A surviving coalition','The way back','Terms of victory'),('assembly','radar','air','peace'),(('Shared authority','Unified direction'),('Preserve the receiving reserve','Concentrate the offensive effort'),('Protect the engineering families','Protect the strike schedule'),('A public settlement account','A protected command review')),'2000.1.1'),
    Nation('OSE','Osea',('Verified contact','The fleet and the island','Authority under suspicion','An order to stop'),('communications','carrier','document','peace'),(('Publish the verified exchange','Keep an authenticated channel'),('Disperse the receiving capacity','Concentrate fleet support'),('Protect the evidence trail','Protect the investigation team'),('A public reciprocal mandate','A bounded command mandate')),'2006.1.1'),
    Nation('YUK','Yuktobania',('Orders that can be questioned','A sea denied','The homeland behind the front','The authority to answer'),('document','submarine','shelter','peace'),(('Civilian scrutiny','Professional safeguards'),('Maintain the maritime perimeter','Prepare the carrier recall'),('Publish the evacuation limits','Protect the receiving instructions'),('A civilian peace mandate','A professional command review')),'2006.1.1'),
    Nation('BLK','Belka',('What the settlement left','A government and a network','The price of a secret','The reckoning'),('document','security','satellite','scales'),(('Open the settlement files','Keep the service account'),('Resist the covert network','Build the covert network'),('Protect the independent witness','Extend procurement influence'),('A public reckoning','Contest strategic access')),'1996.1.1'),
    Nation('SNS','San Salvacion',('A city that must continue',),('medical',),('Civil continuity','Protected local administration'),'2003.1.1'),
    Nation('NPT','North Point',('The last receiving field',),('runway',),('Dispersed reception','Fortified headquarters'),'2003.1.1'),
    Nation('AMB','Amber',('The reserve has an address',),('logistics',),('Published allocations','Protected transport schedule'),'2003.1.1'),
    Nation('UGE','Ugellas',('Space for the next arrival',),('bridge',),('Dispersed capacity','Concentrated receiving sites'),'2003.1.1'),
    Nation('DEL','Delarus',('A signature that survives',),('document',),('Independent inspection','Command inspection'),'2003.1.1'),
    Nation('SBK','South Belka',('Living beside the accusation',),('scales',),('Civil protections','Security review'),'2006.1.1'),
    Nation('SAP','Sapin',('Access is a commitment',),('diplomacy',),('Parliamentary mandate','Limited executive mandate'),'2006.1.1'),
    Nation('UST','Ustio',('The sovereign answer',),('gate',),('Strictly limited support','A conditional mission'),'2006.1.1'),
    Nation('GEB','Gebet',('The road through the border',),('rail',),('Published transit rules','Escorted transit'),'2006.1.1'),
    Nation('REC','Recta',('Promises the treasury can bear',),('economy',),('Domestic recovery first','A bounded contribution'),'2006.1.1'),
    Nation('FAT','FATO',('A council before a commitment',),('assembly',),('Unanimous consultation','Delegated limited mandate'),'2006.1.1'),
)


@dataclass(frozen=True)
class Operation:
    key: str
    tag: str
    lane: int
    title: str
    after: str
    campaign: str
    condition: str
    objective: str
    glyph: str
    days: int = 14
    previous: str = ''
    success: str = ''


AIR = 'check_variable = { deployed_airforce_manpower_k > 0 } check_variable = { num_deployed_planes > 0 }'
FOOTHOLD = 'ac_cpw_osean_foothold = yes'
OPERATIONS = (
    Operation('relief','SNS',0,'The clinic receiving route','2003.6.20','ucw','country_exists = ERU country_exists = FCU','Keep a civilian clinic supplied while both commands inspect its transport.','medical',7),
    Operation('occupation','ERU',0,'A limited occupation mandate','2003.6.20','ucw','310 = { is_controlled_by = ERU }','Issue enforceable civilian access instructions to the garrison.','security',14),
    Operation('recon','FCU',0,'Eyes over the retreat','2003.8.21','ucw',AIR,'Rebuild reconnaissance coverage with aircraft actually deployed.','radar',7),
    Operation('rearbase','NPT',0,'Receive the allied headquarters','2003.8.21','ucw','has_global_flag = ac_ucw_isaf_formed NOT = { has_war_with = FCU }','Prepare a receiving base; accepting the headquarters needs present consent.','runway',14),
    Operation('transport','AMB',0,'A funded transport reserve','2003.8.21','ucw','country_exists = FCU NOT = { has_war_with = FCU }','Deliver a defined transport commitment without assuming coalition consent.','logistics'),
    Operation('dispersal','UGE',0,'A second receiving site','2003.8.21','ucw','country_exists = FCU NOT = { has_war_with = FCU }','Open distributed reception and accept its continuing administrative burden.','bridge'),
    Operation('inspection','DEL',0,'Inspect the command docket','2003.8.21','ucw','country_exists = FCU NOT = { has_war_with = FCU }','Verify the coalition order trail and preserve the unresolved cases.','document'),
    Operation('fleet','FCU',1,'The harbor offensive','2004.11.22','ucw',AIR,'Prepare maritime targeting and support the conventional naval campaign.','navy',14,'recon'),
    Operation('comona','FCU',1,'The sky over Comona','2004.12.30','ucw',AIR,'Commit a prepared air force to the air campaign.','air',7,'recon'),
    Operation('landing','FCU',2,'A continental bridgehead','2005.1.23','ucw','any_controlled_state = { is_core_of = ERU }','Establish an actual mainland foothold before claiming a continental landing.','bridge',14,'comona'),
    Operation('engineers','FCU',2,'Bring the engineers through','2005.3.13','ucw',AIR,'Protect the engineers and families whose information makes an attack possible.','refugees',7,'landing'),
    Operation('battery','FCU',2,'Silence the battery','2005.4.1','ucw',AIR,'Exploit the engineering intelligence and commit the prepared strike.','radar',7,'engineers'),
    Operation('maintenance','ERU',1,'Keep the reserve aircraft grounded','2004.10.1','ucw','has_country_flag = ERU_camp_1_policy_a','Accept reduced immediate readiness to complete safety repairs.','tools',14,'occupation'),
    Operation('withdrawal','ERU',2,'A withdrawal with its people','2005.8.1','ucw','has_country_flag = ERU_camp_2_policy_a','Authorize withdrawal rather than consuming the surviving cadre in a last stand.','gate',14,'maintenance'),
    Operation('liberation','FCU',3,'The city after the front','2005.7.9','ucw','310 = { is_controlled_by = SNS }','Return to the clinic and resolve the occupation records after actual liberation.','medical',7,'battery'),
    Operation('megalith','FCU',3,'The final launch complex','2005.9.25','ucw',AIR,'Prepare the final assault after the military surrender.','missile',7,'battery'),
    Operation('eru_account','ERU',3,'The orders we signed','2005.9.25','aftermath','ac_ucw_war_over = yes','Hear the occupation cases under the settlement that actually occurred.','scales',14,'occupation'),
    Operation('contact','OSE',0,'Keep the original messages','2006.1.1','peace','country_exists = YUK NOT = { has_war_with = YUK }','Preserve reciprocal messages and their authors instead of assuming consent.','communications'),
    Operation('yuk_contact','YUK',0,'The officer who asks again','2006.1.1','peace','country_exists = OSE NOT = { has_war_with = OSE }','Verify disputed orders and protect the right to ask for confirmation.','document'),
    Operation('island','OSE',1,'Defend the receiving island','2010.9.29','cpw',AIR,'Prepare aircraft, dispersal and warning coverage before the first carrier strike.','runway',7,'contact'),
    Operation('submarine','OSE',1,'The first submarine hunt','2010.10.3','cpw',AIR,'Use current air capability and the island defense records to attack the carrier.','submarine',7,'island'),
    Operation('denial','YUK',1,'The submerged perimeter','2010.9.29','cpw',AIR,'Coordinate maritime denial and give the submarine crews a credible withdrawal plan.','submarine',7,'yuk_contact'),
    Operation('naval_reserve','YUK',1,'Recall the second carrier','2010.11.1','cpw','has_country_flag = YUK_camp_1_policy_b','Preserve the second strategic carrier at the cost of withdrawing its threat.','navy',7,'denial'),
    Operation('foothold','OSE',2,'Support the Bastok landing','2010.10.31','cpw',FOOTHOLD,'Support an observed foothold; orders cannot create possession of the peninsula.','bridge',7,'submarine'),
    Operation('second_submarine','OSE',2,'The Razgriz Straits strike','2010.11.13','cpw',AIR+' NOT = { has_global_flag = ac_camp_naval_reserve_success }','Attack the second carrier before a completed recall removes its operational threat.','submarine',7,'submarine'),
    Operation('evacuation','YUK',2,'The homeland receiving line','2010.10.31','cpw','OSE = { ac_cpw_osean_foothold = yes }','Receive civilians from the actual invasion front without inventing provincial transfers.','refugees',7,'denial'),
    Operation('rescue_cover','OSE',2,'A rescue plan before the ceremony','2010.11.1','cpw',AIR,'Reserve rescue coverage and a recovery crew before the ceremony attack.','medical',7,'island'),
    Operation('evidence','OSE',2,'The order that does not match','2010.11.1','cpw','has_country_flag = OSE_camp_2_prepared','Protect contradictory orders and pursue the compromised command channel.','document',7,'contact'),
    Operation('breakout','OSE',2,'The flight outside the command','2010.12.6','cpw',AIR,'Protect the squadron departure after the investigation breaks with compromised command.','air',7,'evidence'),
    Operation('liaison','YUK',2,'The independent liaison','2010.12.6','cpw','has_country_flag = YUK_camp_2_prepared','Protect the independent contact needed to locate the imprisoned political authority.','communications',7,'evacuation'),
    Operation('harling','OSE',3,'Bring the president back','2010.12.8','cpw',AIR,'Use the protected evidence to mount the political rescue.','gate',7,'breakout'),
    Operation('nikanor','YUK',3,'An authority the army cannot erase','2010.12.22','cpw','has_country_flag = YUK_camp_3_prepared','Restore the political voice needed for a reciprocal peace effort.','assembly',7,'liaison'),
    Operation('joint_fleet','OSE',3,'A mixed force that can receive orders','2010.12.29','cpw','YUK = { has_country_flag = YUK_camp_3_prepared }','Coordinate the final joint effort with a present Yuktobanian command.','carrier',7,'harling'),
    Operation('arkbird','OSE',3,'Intercept the captured platform','2010.12.18','cpw',AIR+' has_global_flag = ac_cpw_arkbird_committed','Intercept only a platform that was actually committed to the war.','air',7,'evidence'),
    Operation('solg','OSE',3,'The last interception','2010.12.30','cpw',AIR,'Complete the interception before asking either government to call the crisis resolved.','satellite',7,'harling'),
    Operation('archive','BLK',0,'Open the settlement files','1996.1.1','domestic','always = yes','Read the actual earlier settlement before deciding what Belka owes its veterans.','document'),
    Operation('counterintel','BLK',1,'Protect the independent investigation','2006.1.1','domestic','has_country_flag = BLK_camp_1_policy_a','Protect witnesses and a trail of procurement influence from political interference.','scales',14,'archive'),
    Operation('network','BLK',1,'Build the covert channel','2006.1.1','domestic','has_country_flag = BLK_camp_1_policy_b','Spend national capacity on a covert channel that can also be discovered.','communications',14,'archive'),
    Operation('procurement','BLK',2,'Influence the procurement chain','2008.1.1','domestic','has_country_flag = BLK_camp_2_policy_b','Extend the network while accepting a permanent trail of exposure.','industry',14,'network'),
    Operation('witness','BLK',2,'Bring the witness into daylight','2008.1.1','domestic','has_country_flag = BLK_camp_2_policy_a','Deliver evidence that gives the foreign investigations an independent corroboration.','document',14,'counterintel'),
    Operation('seizure','BLK',3,'Contest the orbital command channel','2010.12.1','network','has_country_flag = BLK_camp_3_policy_b','Attempt strategic access while Osean and Yuktobanian investigators close in.','satellite',7,'procurement'),
    Operation('reckoning','BLK',3,'The state answers for its secrets','2011.1.1','domestic','always = yes','Record exposure, defeat or an alternate network success without declaring a national war.','scales',14,'archive'),
    Operation('civil_files','SBK',0,'Protect the civil files','2006.1.1','domestic','always = yes','Protect residents from collective suspicion while investigating specific conduct.','scales'),
    Operation('access','SAP',0,'A mandate for access','2006.1.1','domestic','country_exists = OSE NOT = { has_war_with = OSE }','Offer limited access under the current mandate; Osea must answer.','diplomacy'),
    Operation('sovereignty','UST',0,'The limited sovereign mission','2006.1.1','domestic','country_exists = OSE NOT = { has_war_with = OSE }','Offer bounded assistance while preserving an independent decision to withdraw.','gate'),
    Operation('transit','GEB',0,'The inspected transit route','2006.1.1','domestic','country_exists = FAT NOT = { has_war_with = FAT }','Offer a transit arrangement with inspection and a present receiving permission.','rail'),
    Operation('contribution','REC',0,'The affordable contribution','2006.1.1','domestic','country_exists = FAT NOT = { has_war_with = FAT }','Offer a limited contribution whose domestic opportunity cost remains visible.','economy'),
    Operation('consultation','FAT',0,'The council receives the offer','2006.1.1','domestic','always = yes','Open consultation without silently granting access, guarantees or faction membership.','assembly'),
)

PARTNERS = {'rearbase':'FCU','transport':'FCU','dispersal':'FCU','inspection':'FCU','access':'OSE','sovereignty':'OSE','transit':'FAT','contribution':'FAT'}

# Canonical anchors now open playable operations. The war owners remain the
# only writers of their stage flags and the existing story-facing outcomes.
CPW_GATES = {'sand_island':'submarine','bastok':'foothold','cruik':'foothold',
             'harling':'harling','nikanor':'nikanor','arkbird_lost':'arkbird','solg':'solg','razgriz_straits':'second_submarine'}
UCW_GATES = {'counteroffensive':'landing','stonehenge':'battery'}
