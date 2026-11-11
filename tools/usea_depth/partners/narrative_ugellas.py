"""Ugellas's long-form events (ac_ud_up.29-40). Provisional gameplay except the cited Chronicle anchors."""
from narrative import PROVISIONAL

P = PROVISIONAL["UGE"]

EVENTS = [
dict(n=29, tag="UGE", title="The Reserve Question", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"Ugellas does not keep its reserve in one place. It keeps it everywhere: in depots behind town halls, in tunnels under farms, in warehouses whose custodians are schoolteachers and grocers and retired sergeants. The habit is older than anyone can explain. It has made the country hard to surprise and impossible to summarise, and it has given the reserve officers who manage the depots a knowledge of the republic that no ministry can match.",
"In 1991 the reserve officers began to ask questions about the government. A circle of them, meeting in the evenings in a depot office, argued that a dispersed country needed a government that thought like a dispersed army: decentralised, disciplined, always ready to move, with every office holding a deputy somewhere else. They wrote their argument down and circulated it, and it was read in more depots than the government had expected.",
"The towns that hosted the depots had questions of their own. They had housed the reserve for decades, at a fee nobody had revised, and they wanted the reserve's money spent locally and its officers answerable locally. They formed a league, and the league asked for a federal parliament in which every town would have a seat and the capital would coordinate rather than command.",
"The national administration had kept the depots stocked and the borders quiet. It intended to continue, and it asked the reserve officers and the towns to be patient. Patience, in Ugellas, has always been a reserve too.",
], options=[
("Invite the circle and the league to a public inquiry.", 5, "axis:dispersal+2;stab-0.01"),
("Remind the reserve officers whom they serve.", 10, "axis:reserve+2"),
]),
dict(n=30, tag="UGE", title="The Council Disperses the State", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Reserve Council took office without a parade. Its members arrived at the old ministries in plain cars, signed the transfer documents and left the same afternoon, each to a different town. By the end of the week the Council's first order was in force: every ministry would be dispersed, every office would hold a deputy somewhere else, and every decision would be taken where it would be carried out.",
"Government in Ugellas became something that happened everywhere at once. The ministry of finance moved into a depot on a hillside, the ministry of health into a school, the ministry of the interior into three separate town halls that took turns being its headquarters. Officials commuted between offices that were deliberately far apart. Letters took longer to arrive, decisions took longer to coordinate, and yet the country found itself governed by people who could see what they were governing.",
"The towns were divided. Some welcomed the ministries and the salaries that came with them. Others resented officials who arrived with requisition orders and left with the town's best building. The municipal league, which had wanted a federal parliament, found itself governed by a council it had not elected and could not petition, because the Council had no single address.",
"The Council does not believe in capitals. It believes that a country that cannot be decapitated cannot be conquered. Whether it can be governed that way is the experiment.",
], options=[
("Publish the address of every dispersed office.", 0, "stab+0.02;axis:dispersal+3"),
("Keep the dispersed offices unlisted for security.", 0, "axis:reserve+3;tech:land_doctrine"),
]),
dict(n=31, tag="UGE", title="The Towns Hold the Purse", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The first federal parliament of Ugellas met in the largest depot in the country, because no other building had room for a delegate from every town. They sat on folding chairs between stacked crates of tinned food and blankets, and the chamber's acoustics were terrible. The parliament elected a federal cabinet on the second day and gave it a single instruction: coordinate, do not command.",
"The federal charter gave each town a seat, each region a budget and the capital a telephone. The cabinet discovered that the telephone was the most important instrument of government it had. It spent its days calling towns: asking, persuading, reminding, apologising. Decisions that the old administration had taken in an afternoon now took a month, because every town had to agree or at least be seen to have been consulted.",
"The reserve officers were not pleased. The depots were now governed by the towns that hosted them, and some towns had ideas about what a depot should hold that did not match the reserve's lists. The circle of reserve officers, which had argued for a Reserve Council, now argued for discipline, and its members found that discipline was hard to impose on a parliament of grocers and schoolteachers.",
"Ugellas has a government that answers to its towns. The towns are learning that answering is not the same as agreeing.",
], options=[
("Give every town a share of the reserve budget.", 0, "axis:dispersal+3;stab+0.02"),
("Keep the reserve budget national, under parliamentary audit.", 0, "axis:reserve+3"),
]),
dict(n=32, tag="UGE", title="The Administration Renews Its Lease", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The national administration of Ugellas renewed its mandate the way it renewed a depot lease. It conducted an inventory, held a review and signed a document. The inventory counted everything the administration governed: depots, roads, towns, people and the custodians who held the keys. The review found that the administration had governed adequately, which was what it had always found. The document was signed by the senior officials of every ministry and published without comment.",
"Nobody voted, and nobody was surprised. The reserve officers who had argued for a Reserve Council read the inventory and found their own depots listed accurately, which was a kind of compliment. The towns that had formed a municipal league read the review and noted that it said nothing about the fees they were paid to host the depots. Their delegates wrote to the administration, and the administration replied that the fees would be reviewed in due course.",
"The administration's strength is that it knows its country. Its weakness is that it knows it as an inventory: a list of things to be counted and kept, rather than a set of people with opinions. It has kept Ugellas stocked, quiet and ready for decades. It has never had to persuade anyone of anything.",
"The lease has been renewed. Whether the tenants accept it will depend on what the administration does with the next inventory.",
], options=[
("Publish the depot leases and their fees.", 5, "axis:reserve+3;stab+0.01"),
("Review the fees quietly, town by town.", 10, "axis:dispersal+3"),
]),
dict(n=33, tag="UGE", title="Depots No Map Shows", picture="depots", layer="Provisional gameplay", citation=P, paragraphs=[
"The census of the depots began with the official list, which named four hundred sites. It ended eighteen months later with a list of eleven hundred. The census teams found depots in barns, in churches, in a disused railway tunnel and in the cellar of a hotel whose owner had been paid a storage fee for thirty years without ever being told what was in it. Most of the depots held something useful. Some held things nobody could identify.",
"Every depot was assigned a custodian and a deputy who lived somewhere else. A depot without a custodian, the census report concluded, was a rumour, not a reserve. Custodians were schoolteachers, farmers, shopkeepers and retired soldiers; they were paid a modest fee, given a key and a list, and told to check the list against the contents twice a year. Many of them had been doing this informally for decades and were pleased to be asked officially.",
"The census also raised a question about neighbours. Several neighbouring governments had heard about Ugellas's depots and asked whether they could store their own emergency stocks in them. Storage was cheap to offer and expensive to honour: a depot holding a neighbour's grain could not hold Ugellas's own, and a custodian holding a neighbour's key might one day have to choose whom to open the door for.",
"Ugellas now knows what it has. It must decide whom it will share it with.",
], options=[
("Offer neighbours storage on published terms.", 10, "axis:mobility+3"),
("Keep the census confidential.", 5, "axis:reserve+3"),
]),
dict(n=34, tag="UGE", title="Can We Store People?", picture="warning", layer="Official", citation="ACES Chronicle, 1996 / 04.20; Ugellas's preparations are provisional gameplay", paragraphs=[
"When Central Usea announced on the twentieth of April 1996 that the asteroid Ulysses would strike the Earth, Ugellas's custodians received a circular from the national reserve office. It asked them to inventory their depots again, this time with a new column: could the depot hold people? A cellar that stored grain might shelter a family. A tunnel that stored fuel might shelter a village, if the fuel were moved somewhere else.",
"The neighbours who stored grain in Ugellas's depots telephoned the same week. Their governments had read the same announcement and done the same arithmetic. If the fragments came, where would their people shelter? Ugellas had more underground space than most countries its size, and its neighbours wanted to know whether a storage agreement for grain could become a storage agreement for people. Nobody had ever drafted such an agreement, and the lawyers were not sure it was possible.",
"The government faced a choice it had avoided for years. It could sign a Usean reserve pact, sharing its depots, its inventories and its obligation to open them with its neighbours. Its reserve would become a regional reserve, and its custodians might one day open the door to people who were not Ugellan. Or it could keep a national reserve only, selling neighbours what they needed but pledging the depots to nobody else's emergency.",
"The asteroid will not fall on borders. Ugellas must decide whether its depots will.",
], options=[
("Inventory every depot for shelter space.", 10, "prep+1;axis:dispersal+3"),
("Inventory only the depots near the towns.", 5, "axis:reserve+3"),
]),
dict(n=35, tag="UGE", title="Who Holds the Keys?", picture="coup", layer="Official", citation="ACES Chronicle, 1997 / 05.30; events in Ugellas are provisional gameplay", paragraphs=[
"On the thirtieth of May 1997 a coup broke out across Usea. In Ugellas it arrived as a question at the gate of a depot. Shortly after midnight a lorry pulled up outside a depot in the interior, and an officer with a rifle and an order the custodian did not recognise demanded the keys. The custodian, a retired schoolteacher, telephoned the deputy, who telephoned the reserve office, which telephoned the ministry, which did not answer.",
"The custodian refused. The custodian told the officer that the depot would open for the person named on the list and for nobody else, and that the officer was welcome to wait until morning, when the reserve office could confirm the order. The officer waited. By morning the coup in Ugellas had collapsed, the officer had been recalled, and the custodian had become the most famous schoolteacher in the country.",
"Unified Command defeated the coup across Usea within days. In Ugellas the coup had never really begun, because nobody could find the keys. Officers who had joined it discovered that the depots they meant to seize were held by thousands of custodians who answered to lists rather than orders, and that a dispersed reserve could not be taken by a single telephone call.",
"The coup has shown Ugellas what its depots are worth. It has also shown that the keys are held by civilians, and the government must decide whether that is a weakness or a strength.",
], options=[
("Honour the custodians and keep the keys with them.", 10, "stab+0.02;axis:dispersal+3"),
("Put every depot under a reserve officer's seal.", 5, "axis:reserve+3;xp:army+10"),
]),
dict(n=36, tag="UGE", title="A Battery in Someone Else's Desert", picture="desert", layer="Official", citation="ACES Chronicle, 1998 / 06.19 (Stonehenge completed); Ugellas's reserve policy is provisional gameplay", paragraphs=[
"On the nineteenth of June 1998 Stonehenge was completed in San Salvacion's desert. Eight railguns now stood ready to destroy the fragments of Ulysses before they reached the ground, and in Ugellas's cabinet room a minister asked the question several colleagues had been thinking. If the battery could stop the fragments, why was Ugellas spending so much on depots, shelters and custodians?",
"The custodians answered before the cabinet did. Their association published a letter in every newspaper, signed by more than a thousand of them. A battery, they wrote, could shoot at a fragment; it could not promise to hit every one. A battery in someone else's desert would protect someone else's country first. And a battery could not feed a family whose water works had been destroyed, house a village whose roofs had fallen in, or carry the injured to a hospital. The depots could.",
"The reserve office added its own arithmetic. The battery would reduce the risk; it would not remove it. The depots cost a fraction of what a single railgun had cost, and they would be needed after the fragments fell whatever the battery achieved. Cutting them now would save money for a year and leave Ugellas exposed for a generation.",
"The battery in the desert has changed the calculation. Ugellas must decide whether it has changed the answer.",
], options=[
("Keep every depot and every custodian.", 10, "axis:reserve+3;prep+1"),
("Close the smallest depots and fund the rest better.", 5, "axis:mobility+3"),
]),
dict(n=37, tag="UGE", title="The Dispersal Night", picture="impact", layer="Official", citation="ACES Chronicle, 1999 / 07.08; Ugellas's relief is provisional gameplay", paragraphs=[
"On the eighth of July 1999 Ulysses broke apart over the Earth. In Ugellas the sirens sounded an hour before the first fragments were visible, and families across the country walked to their assigned depots by torchlight. Each family had a card naming its depot; each depot had a list naming its families. The custodians stood at the gates with their lists and their torches and checked names as people came in.",
"Most of the lists were true. Families arrived at depots that had room for them, with blankets and water and a custodian who knew where everything was. Some lists were not: a depot built for forty held ninety, a tunnel listed as dry had flooded in the spring, a custodian had died and the deputy had moved away. The mobility columns spent the night carrying families from depots that were too full to depots that were not.",
"By morning the custodians knew what their own gates had seen and little else; the radio carried reports from across Usea, few of them confirmed. In the morning the custodians opened the depots and began to distribute what was in them. The question of how much to distribute was not on any list. The reserve was large, but it was not endless, and nobody knew whether this was the only crisis or the first.",
"The night is over. The depots are open. Ugellas must decide how much of its reserve to spend now, and how much to keep.",
], options=[
("Move families from the full depots first.", 10, "axis:mobility+3"),
("Keep every family where its card says.", 5, "axis:dispersal+3"),
]),
dict(n=38, tag="UGE", title="Refugees at the Depots", picture="refugees", layer="Official", citation="ACES Chronicle, 2000 / 04.21; Ugellas's refugee policy is provisional gameplay", paragraphs=[
"On the twenty-first of April 2000 Erusea closed its border to refugees, and some of those turned back found their way to Ugellas. They came to the depots, because the depots were where the food was and because the stories of the dispersal night had travelled. Custodians found families camped outside their gates, asking for bread, blankets and a place to sleep.",
"The custodians had lists, and the refugees were not on them. Some custodians opened the gates anyway, because the depots held food and the families outside were hungry. Others telephoned the reserve office and asked what to do, and the reserve office telephoned the ministry, which convened a committee. By the time the committee met, several depots had become camps, and several camps were becoming villages.",
"The government considered two answers. It could let the refugees settle around the depots, building villages where there had been only warehouses, and accept that Ugellas would grow by the size of a town. Or it could feed and treat the refugees and carry them onward in the mobility columns to wherever they were expected, keeping Ugellas a road rather than a destination.",
"The custodians are waiting for instructions. In the meantime they are doing what custodians always do: counting, feeding and keeping the gates.",
], options=[
("Let the custodians decide at their own gates.", 10, "axis:dispersal+3;stab-0.01"),
("Send the reserve office to every depot with refugees.", 5, "axis:reserve+3"),
]),
dict(n=39, tag="UGE", title="The Reserves Are Called", picture="war", layer="Official", citation="ACES Chronicle, 2003 / SUMMER (Erusea invades San Salvacion); Ugellas's wartime exposure is provisional gameplay", paragraphs=[
"In the summer of 2003 Erusea invaded San Salvacion and seized Stonehenge, and Central Usea's partners found themselves at war. In Ugellas the mobilisation notices went out by post and by radio. Reservists were to report to their depots, the same depots they had guarded, stocked and inventoried for a decade. Many of them reported within the day, still wearing the clothes they had been working in.",
"The depots that had held grain and blankets for the fragment years now held shells and fuel for the war. Coalition forces moving to the front asked to use them, and the custodians who had stored relief for their neighbours now stored munitions for the coalition. The command posts were dispersed across the country, so that no single raid could silence them. Orders arrived late, but they arrived.",
"Ugellas had prepared for a crisis, not for a war, and the difference was painful. The depots were scattered and small; the army needed large, concentrated stocks close to the front. The mobility columns knew the roads; they did not know how to move under air attack. The government had to decide whether to defend the depots where they stood, keeping the reserve at home, or to empty them forward to the coalition's front.",
"The reserve has been called. Ugellas must decide where its reserve will fight.",
], options=[
("Call every reservist at once.", 10, "ws+0.05;axis:reserve+2"),
("Call the reservists by depot, in order.", 5, "stab+0.02;axis:dispersal+2"),
]),
dict(n=40, tag="UGE", title="The Depots after the War", picture="peace", layer="Provisional gameplay", citation=P, paragraphs=[
"The crisis years are over. The warning, the fragments, the refugees and, for most of Usea, the war: Ugellas has met each of them from its depots, and its depots show the cost. Some are empty, their stocks spent on the dispersal night or sent forward to the coalition. Some are damaged, their tunnels cracked and their roofs fallen. Some are full of things nobody needs any more: munitions for a war that has ended, blankets for refugees who have gone home.",
"The country must now decide what a reserve is for in peacetime. The reserve officers want the depots restocked for the next war or the next crisis, and they point out that every crisis Ugellas has faced arrived without notice. The towns want the depots handed over for schools, clinics and workshops, and they point out that the depots were paid for by their taxes and housed in their buildings for decades.",
"The custodians, as always, want to know what will be on their lists. Many of them have held their keys for twenty years. They have opened their gates for families, refugees and soldiers, and they have closed them against officers with rifles. They would like to know whether they are still needed.",
"Ugellas survived the crisis years by being everywhere at once. It must now decide whether to stay that way.",
], options=[
("Ask the custodians what their depots should become.", 10, "axis:dispersal+3;stab+0.01"),
("Ask the reserve office what the next crisis will need.", 5, "axis:reserve+3"),
]),
]
