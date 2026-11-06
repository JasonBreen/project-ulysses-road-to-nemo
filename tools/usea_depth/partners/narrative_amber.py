"""Amber's long-form events (ac_ud_up.17-28). Provisional gameplay except the cited Chronicle anchors."""
from narrative import PROVISIONAL

P = PROVISIONAL["AMB"]

EVENTS = [
dict(n=17, tag="AMB", title="Who Signs for Amber?", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"In Amber the government is a signature. For as long as anyone can remember, the cabinet has governed by contract: it signs for roads, for rolling stock, for grain, for the maintenance of yards it does not own, and it answers for those signatures to nobody but itself. The arrangement has made Amber rich by the standards of its neighbours and has never once asked its citizens what they thought of it.",
"In the first weeks of 1991 three groups asked anyway. The largest contract holders, whose firms built most of what the cabinet signed for, proposed a Chartered Development Board: a government of the people who actually build things, answerable to the contracts they sign. The freight unions, whose members moved everything the contractors built, proposed a compact: they would keep Amber moving if the state guaranteed their wages, their safety and a vote. And a league of nationalists, noisy and growing, said that Amber had sold itself one contract at a time to foreign capitals and demanded that every foreign clause be struck out.",
"The cabinet's answer was to keep signing. It had delivered growth without elections and without a scandal anyone could prove. It saw no reason to hand the pen to people who would use it to sign for themselves. Yet its ministers noticed that the three movements were drawing crowds, and that the crowds were not all asking for the same thing.",
"Someone will hold the pen when the crisis years come. Amber must decide whose hand it trusts.",
], options=[
("Invite the movements to submit written proposals.", 5, "axis:development+2;stab-0.01"),
("The cabinet will sign as it always has.", 10, "axis:transport+2"),
]),
dict(n=18, tag="AMB", title="The Board Publishes Its Schedule", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Chartered Development Board took office in a hired conference hall, because its members agreed that the old cabinet rooms were too small for a government that intended to build things. Twenty-one seats were filled: fourteen by the largest contract holders in proportion to the value of their public work, five by regional delegates and two by the freight unions, who did not come. The chair of the Board was elected on the first ballot by the contractors, and the regional delegates abstained.",
"The Board's first act was to publish a schedule. It ran to five years and four hundred pages, and it allocated every yard, road and depot in Amber to a programme of work. Nothing outside the schedule would be built, and nothing inside it would be delayed. It was, the Board explained, a manifesto that could be audited: a promise written in tonnes, kilometres and completion dates rather than slogans.",
"Amber's citizens found that they had a government that knew exactly what it wanted to do, and that they had very little say in it. The schedule was efficient and largely sensible. It favoured the regions where the contractors already worked and the projects they already knew how to deliver. The freight unions called it a timetable for profit. The Sovereign Contracts League called it the old cabinet in new clothes, with the foreign clauses still inside.",
"The Board does not mind criticism, so long as the schedule is met. It intends to be judged on its deliveries, and its first deliveries are due within the year.",
], options=[
("Meet every deadline, whatever it costs.", 0, "axis:development+4;stab-0.02"),
("Revise the schedule each year in public.", 0, "axis:service+3;stab+0.02"),
]),
dict(n=19, tag="AMB", title="The Compact Takes the Cabinet", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Labour Compact Cabinet was sworn in at the central freight yard, on a platform built from railway sleepers, in front of several thousand rail crews, dockers and warehouse staff who had stopped work for the afternoon and would make it up on Sunday. The compact's terms were read aloud before the oath: a wage floor, a national safety code, an elected chamber, and a freight workers' veto over any law that would break a strike.",
"The cabinet's ministers were union officials, transport engineers and two former contract managers who had changed sides. They had never governed anything larger than a pension fund. They knew, however, exactly how Amber moved, because they had moved it, and their first decisions were about the yards: rest periods, inspections and the right to stop work that would kill someone.",
"The contractors were alarmed and said so. A safety code would slow the freight; a wage floor would raise the price of every contract; an elected chamber would be full of people who had never signed anything. Several firms threatened to move their work abroad. The cabinet replied that the yards, the rails and the people who worked them would stay in Amber, and that the firms were welcome to take their offices wherever they liked.",
"Freight moves more slowly now, and fewer people die moving it. Whether Amber can afford that trade will be decided by the first election.",
], options=[
("Hold the first election as soon as the code is in force.", 0, "stab-0.02;axis:service+4"),
("Make the code permanent before facing the voters.", 0, "axis:transport+3;stab+0.02"),
]),
dict(n=20, tag="AMB", title="The League in the Ministries", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Sovereign Contracts League did not win an election, because there was none. It won the streets, then the newspapers, then the loyalty of enough officials that the old cabinet found its orders unanswered. When the cabinet resigned, the League's directorate moved into the ministries the same evening and hung its banners from the windows: long lists of every foreign clause in Amber's public contracts, each one marked for renegotiation.",
"The lists were accurate. Amber had signed contracts that gave foreign firms first claim on its freight in an emergency, that priced its grain in foreign currency and that allowed foreign inspectors into its yards. The League's conclusions were another matter. It promised that every foreign clause would be struck out and every bargain rewritten on Amber's terms, and it promised that the rewriting would cost nothing, because foreigners needed Amber more than Amber needed them.",
"The directorate's first letters went out within a week. Foreign partners were invited to sign new terms; partners who refused were sued, delayed or expelled. The contractors who had built Amber's prosperity were given deadlines and told that their loyalty would be remembered. The press was given instructions, and the newspapers that had made the League's name were the first to receive them.",
"Amber is now governed by people who believe it has been cheated, and they are partly right. Whether they can renegotiate the world without breaking the country remains to be seen.",
], options=[
("Renegotiate every contract at once.", 0, "ws+0.03;axis:development+3"),
("Begin with the contracts that bind Amber's freight in an emergency.", 0, "axis:transport+4"),
]),
dict(n=21, tag="AMB", title="The Cabinet's Promise", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The contracting cabinet renewed its own mandate with a promise rather than a vote. Every public contract would be published, the cabinet announced: large or small, foreign or domestic, completed or in dispute. Every bargain would be explained in plain language, with its cost, its beneficiary and the minister who signed it. The cabinet asked for nothing in return except time.",
"Publication proved harder than promising. The ministries held contracts in filing cabinets, in safes, in the private papers of retired officials and in the memories of clerks who had died. Some contracts had been signed twice, by different ministers, for the same work. Some had never been signed at all and had been honoured anyway, on the strength of a handshake and a dinner. The cabinet's audit office began to count them and discovered that nobody knew how many there were.",
"The movements that had wanted to replace the cabinet watched the audit closely. The Chartered Board movement found its own members' contracts on the list and argued for discretion. The freight unions found clauses that allowed contractors to cut safety inspections in a hurry and demanded that they be printed first. The League read every foreign clause aloud at its rallies, and the crowds grew.",
"The cabinet has made a promise it cannot quickly keep. If it keeps it slowly and honestly, Amber may come to trust a government it never chose.",
], options=[
("Publish the foreign clauses first.", 5, "axis:service+3;stab+0.01"),
("Publish in order of value, largest contracts first.", 10, "axis:development+3"),
]),
dict(n=22, tag="AMB", title="A Register of Usean Contracts", picture="yards", layer="Provisional gameplay", citation=P, paragraphs=[
"Amber's firms hold contracts in half the capitals of Usea. They build roads in one country, run freight in another and maintain rolling stock for a third. Until 1991 nobody in Amber's government had tried to list them all. The register, when the trade ministry began compiling it, turned out to be the most important document the country had ever produced, because it showed what Amber had promised abroad and therefore what it could still promise at home.",
"The first draft listed three hundred contracts. The second draft, after the ministry asked the firms directly, listed eleven hundred. Many committed Amber's freight capacity to foreign clients for years ahead. Some committed it in an emergency, on terms that nobody in the cabinet had read. A few committed the same wagons to different clients on the same dates, and the firms involved explained that the clients would never all need them at once.",
"The register raised two questions. The first was practical: how much freight could Amber move for itself, once its foreign obligations were met? The second was political: who had authorised these obligations, and on whose behalf? The freight yards survey would answer the first. The treaty office would begin to answer the second, by reading every treaty Amber had signed and marking every clause that put its trains at someone else's disposal.",
"A country that sells its capacity must know how much it has sold. Amber is about to find out.",
], options=[
("Require every firm to register its foreign contracts.", 10, "axis:service+3"),
("Ask the firms to register voluntarily.", 5, "axis:development+3;stab+0.01"),
]),
dict(n=23, tag="AMB", title="Contracts after the Warning", picture="warning", layer="Official", citation="ACES Chronicle, 1996 / 04.20; Amber's response is provisional gameplay", paragraphs=[
"When Central Usea announced on the twentieth of April 1996 that the asteroid Ulysses would strike the Earth, Amber's freight offices received their first telephone calls before the cabinet had met. Foreign clients wanted guarantees. If the fragments came, would their contracted wagons still run? Would Amber honour its emergency clauses, or would it keep its trains at home? The clerks who answered the telephones did not know, and said so.",
"The yards at home asked the opposite question. If Amber's trains were needed for relief, whose relief would come first: the foreign clients who had paid in advance, or the Amber districts that had paid nothing but would need the trains most? The register of Usean contracts suddenly mattered more than any document in the country, because it showed exactly how much of Amber's freight had already been promised to someone else's emergency.",
"International relief was being discussed in every capital. A consortium was forming to coordinate the response, and Amber was invited to join as its freight and contracting house. Membership would give Amber a voice in where relief went. It would also bind Amber's trains to the consortium's priorities, which might not be Amber's own. The alternative was to remain an independent contractor, selling freight to whoever needed it on Amber's terms.",
"The asteroid has turned every freight contract into an emergency contract. Amber must decide whose emergency it will serve first.",
], options=[
("Honour every foreign emergency clause as written.", 10, "axis:service+3;prep+1"),
("Suspend foreign emergency clauses pending review.", 5, "axis:transport+3;stab+0.01"),
]),
dict(n=24, tag="AMB", title="Contracts in the Coup Summer", picture="coup", layer="Official", citation="ACES Chronicle, 1997 / 05.30; Amber's contracts are provisional gameplay", paragraphs=[
"On the thirtieth of May 1997 a coup broke out across Usea, and by the next morning Amber's lawyers were working through the night. Contracts signed with governments that had been overthrown overnight were suddenly contracts with nobody. Payments due from ministries that no longer existed were suddenly debts without a debtor. One freight consignment was halfway across a border when the government at its destination changed twice.",
"Unified Command defeated the coup, and within weeks most of the governments that had fallen were restored. The contracts were not so easily restored. Some coup governments had signed new orders in their few days of power, and the restored governments refused to honour them. Some of Amber's firms had accepted payment from the coup governments and now faced claims from their successors. The register of Usean contracts, so carefully compiled, had developed a new column: valid, disputed, void.",
"Through it all the trains kept running. Amber's freight crews had learned long ago that a train in motion is easier to protect than a train in a siding, and they kept moving consignments whose destinations were uncertain until someone told them otherwise. Nobody did, and most of the consignments arrived. The crews were thanked in the cabinet's statement, in the last paragraph.",
"The coup has taught Amber that a contract is only as stable as the government that signed it. The question is what Amber does with the lesson.",
], options=[
("Honour only contracts signed by governments now in power.", 10, "axis:service+3"),
("Honour every contract the crews delivered, and settle the claims later.", 5, "axis:transport+3;stab+0.01"),
]),
dict(n=25, tag="AMB", title="Every Government Wants the Same Trains", picture="impact", layer="Official", citation="ACES Chronicle, 1999 / 07.08; Amber's relief is provisional gameplay", paragraphs=[
"On the eighth of July 1999 Ulysses broke apart over the Earth, and the fragments fell across Usea. Amber's yards took damage: a roundhouse burned, two bridges cracked and a signal box vanished with its operator. The relief rail plan had named the trains that would run, and most of them ran, crewed by people who had rehearsed the timetable for three years and hoped never to use it.",
"By noon the telephones were ringing in every freight office. The consortium wanted trains for the fragment fields. Foreign clients wanted their contracted wagons. Amber's own districts, several of them burning, wanted everything. The relief plan had assumed that Amber would decide how its capacity was used. Within hours it was clear that every government in Usea was asking for the same trains at the same time, and that Amber had fewer trains than it had promised.",
"The capacity board met in the basement of the transport ministry. It could open the yards to everyone, moving relief in the order requests arrived and accepting that Amber's own districts would wait their turn. Or it could ration capacity by a published formula: domestic need first, contracts second, appeals third. The first would make Amber the hero of the relief effort; the second would make it the protector of its own people.",
"The trains are waiting at the yards. Whichever answer the board gives, some of the people asking will be refused.",
], options=[
("Run the relief plan exactly as written.", 10, "axis:transport+3"),
("Send the medical freight first, wherever it is needed.", 5, "axis:service+3;stab+0.01"),
]),
dict(n=26, tag="AMB", title="Refugees on the Freight Lines", picture="refugees", layer="Official", citation="ACES Chronicle, 2000 / 04.21; Amber's refugee policy is provisional gameplay", paragraphs=[
"On the twenty-first of April 2000 Erusea closed its border to refugees, and the displaced of the fragment years turned south. Many of them rode Amber's freight trains: on wagon roofs, in empty boxcars, on the couplings between cars. The freight crews did not stop them. Many of the crews had relatives in the fragment fields, and all of them had carried refugees before, unofficially, on the relief trains.",
"The yards became the first place the refugees stopped. Families camped in sidings, in warehouses and in the shelters built for the impact. They washed at the yard taps, cooked on the yard braziers and asked the yard foremen for work. Some of the foremen hired them, because the yards were short of labour after the fragments, and the refugees worked hard for very little.",
"The unions objected. A refugee who worked for half wages undercut every member of the compact or the old agreements, and the freight workers had fought too long for their wages to watch them fall. The contractors welcomed the labour and asked the government to regularise it. The League, where it had influence, demanded that the refugees be sent onward in sealed trains, fed, treated and gone.",
"The government must decide whether the refugees on the freight lines are workers, guests or passengers. The yards cannot hold them for long without an answer.",
], options=[
("Let the yards hire refugees at the agreed wage.", 10, "axis:development+3"),
("Keep the refugees out of the yards until a policy is set.", 5, "axis:service+3;stab+0.01"),
]),
dict(n=27, tag="AMB", title="War Comes to the Yards", picture="war", layer="Official", citation="ACES Chronicle, 2003 / SUMMER (Erusea invades San Salvacion); Amber's wartime exposure is provisional gameplay", paragraphs=[
"In the summer of 2003 Erusea invaded San Salvacion and seized Stonehenge, and the war reached every partner of Central Usea. In Amber it arrived as a telephone call from the transport ministry to every yard foreman in the country: dim the lights, hood the signals, prepare the shelters. The yards that had moved relief for four years were now targets, because the coalition would need them to move everything else.",
"The first raids came within weeks. They were small and inaccurate, and they taught Amber what the next raids would be like. A junction burned for two days. A train of empty wagons was destroyed in a siding. The crews learned to shunt in the dark, to repair track by night and to sleep in the shelters at the junctions. Accidents rose for a month and then fell, as people learned how to work in a war.",
"The cabinet had to decide what Amber's freight was for. The coalition wanted trains; Amber's towns wanted food. The development programme could be converted to war production under contract, with profits capped and deliveries guaranteed. Or a protected share of freight and industry could be kept for civilian life, giving the coalition less and keeping Amber's towns fed and calm.",
"The war has come to the yards. Amber's crews have kept the trains running through the fragments, and they intend to keep them running through this.",
], options=[
("Put the yards on a war footing tonight.", 10, "ws+0.05;axis:transport+2"),
("Keep the civilian timetable running as long as possible.", 5, "stab+0.02;axis:service+2"),
]),
dict(n=28, tag="AMB", title="The Yards after the War", picture="peace", layer="Provisional gameplay", citation=P, paragraphs=[
"The crisis years are over. The warning, the fragments, the refugees and, for most of Usea, the war: Amber has carried all of them on its freight lines, and its yards show it. Half of them are ruins, half are improvisations, and all of them are working. Crews who learned to repair track by night now repair it by day, and the shelters at the junctions are being turned into storerooms.",
"The question now is what to rebuild. The old yards could be rebuilt to the old plans by the old firms, quickly and familiarly, leaving every old bottleneck where it was. Or the yards could be rebuilt as a hub for the continent's reconstruction: larger, more open and designed to carry the freight that would rebuild Usea's cities. The first would serve Amber. The second would serve everyone, and would make Amber indispensable, which is not the same thing as loved.",
"The contractors, the freight unions and whatever remains of the League each have their own answer. The contractors want the work, and the larger the better. The unions want the jobs, and the safety code that protects them. The League's survivors want to know who will own the new yards and whose clauses will govern them.",
"Amber has always been a country of bargains. The bargain it strikes now will shape its next generation.",
], options=[
("Ask the regions what they need rebuilt first.", 10, "axis:service+3;stab+0.01"),
("Ask the contractors what they can build fastest.", 5, "axis:development+3"),
]),
]
