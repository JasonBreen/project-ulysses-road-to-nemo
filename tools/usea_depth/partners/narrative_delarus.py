"""Delarus's long-form events (ac_ud_up.41-52). Provisional gameplay except the cited Chronicle anchors."""
from narrative import PROVISIONAL

P = PROVISIONAL["DEL"]

EVENTS = [
dict(n=41, tag="DEL", title="Who Inspects the Government?", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"Delarus is a country of inspectors. It inspects its accounts, its requisitions, its contracts and its promises; it inspects its shelters, its stores and its roads; it keeps dockets on everything the state has undertaken and closes them only when the work is done. Its inspectors are proud, poorly paid and very hard to bribe. In 1991 a group of them asked a question that had never been asked in public: who inspects the government itself?",
"The senior inspectors had an answer ready. The government should be answerable to the same rules it enforced: published accounts, an independent audit office and an elected chamber to read the audits. They wrote an Inspectors' Charter and read it aloud at their own congress, to applause that surprised even them. The charter was not radical by the standards of other countries. In Delarus, where the government had always inspected others and never been inspected, it was a revolution on paper.",
"The senior commanders had a different answer. Inspection, they argued, had become obstruction. Every requisition was delayed by a docket, every order by an audit, every plan by an inquiry. A small country surrounded by larger ones could not afford to govern by committee. They proposed a Command Council that would govern by order and inspect afterwards, if at all.",
"The present government had balanced the inspectors against the commanders for years, and it intended to go on doing so. Both sides were now asking it to stop balancing and choose.",
], options=[
("Let the inspectors and commanders debate in public.", 5, "axis:oversight+2;stab-0.01"),
("Settle the question inside the government.", 10, "axis:records+2"),
]),
dict(n=42, tag="DEL", title="The Audit Office Audits Its Makers", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Inspectorate Cabinet took office under the Inspectors' Charter and called elections for a chamber within six months. Its first act was to make the audit office independent: the office's director could no longer be dismissed by any minister, its budget was fixed by law, and its reports would be published in full. Its second act was to ask the audit office to audit the cabinet.",
"The audit was published a year later, and it was thorough. It found that the old government had kept accounts nobody could reconcile, that the commanders had signed requisitions nobody had approved, and that the Inspectorate's own movement had accepted donations it had not declared. Three ministers resigned within the week. One of them had been a senior inspector and a signatory of the charter.",
"Delarus discovered that it had a government that could be embarrassed, and that liked it. The newspapers printed the audits in full, and people read them on the trams. The commanders complained that every plan now took a year to approve, and they were partly right: planning was slower, and the army's officers spent more time with auditors than with their units. Yet the requisitions that were approved were delivered, and nobody profited from them without being caught.",
"The audit office now audits the cabinet that created it. The question is whether the habit will survive the first crisis that demands speed instead of accounts.",
], options=[
("Publish every audit, including the embarrassing ones.", 0, "stab+0.02;axis:oversight+4"),
("Give the commanders a faster audit for urgent requisitions.", 0, "axis:command+3"),
]),
dict(n=43, tag="DEL", title="Orders without Appeal", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The Command Council took office on a weekday morning and suspended the old inspection regime by noon. Audit offices were placed under the Council's directorates. Dockets were closed, whether the work they recorded was finished or not. Inspectors were reassigned to the directorates as clerks, and many of them resigned rather than serve. The Council published its standing orders the next day: numbered, clear and binding, with no procedure for appeal.",
"Orders were faster now. A requisition that had taken a month to approve took an afternoon. A road that had waited three years for an inquiry was begun within a week. The army's officers, freed from the auditors, spent their time with their units, and the army improved. The Council's supporters pointed to all of this and asked whether the old inspections had ever achieved as much.",
"The Council's critics pointed to what could no longer be seen. Nobody outside the Council read its orders before they were carried out, and nobody inside it was required to explain them afterwards. The directorates spent money without publishing accounts. Contracts went to firms whose owners had served under the Council's members. The newspapers that reported this were warned, then closed.",
"Delarus has a government that can act quickly. It no longer has a government that can be inspected, and the inspectors, many of them now unemployed, are keeping their own dockets.",
], options=[
("Allow the old inspectors to keep their own dockets.", 0, "stab+0.01;axis:records+3"),
("Requisition the inspectors' private records.", 0, "axis:command+4;stab-0.02"),
]),
dict(n=44, tag="DEL", title="Inspected and Commanding", picture="politics", layer="Provisional gameplay", citation=P, paragraphs=[
"The present government renewed its mandate without new powers and without renouncing any. It promised to be inspected and to command, and to say in each case which it was doing. The promise was written into a short statement and read in the chamber of the old council of state, which had no legislative power but a good public gallery. The gallery was full of inspectors and commanders, and both groups listened for the clause that favoured them.",
"There was no such clause. The government's statement divided its business into two columns. Matters of command, including defence, emergency requisitions and the army's internal organisation, would be decided by order and reviewed afterwards. Matters of inspection, including public accounts, contracts and relief, would be decided only after audit. Every new matter would be assigned to a column by the cabinet, and the assignment would be published.",
"Both sides found reasons to object. The inspectors noted that the cabinet decided which column a matter belonged to, and that it could move anything it liked into the column of command. The commanders noted that relief had been placed among the matters of inspection, and that the next crisis would be a relief crisis. Neither side, however, could claim to have lost, and that was the government's intention.",
"Delarus is governed by a balance. A balance is only as stable as the hand that holds it, and the hand belongs to the present government.",
], options=[
("Open the government's dockets to the public after a year.", 5, "axis:records+3;stab+0.01"),
("Keep the dockets closed and publish summaries.", 10, "axis:command+3"),
]),
dict(n=45, tag="DEL", title="A Register of Foreign Obligations", picture="records", layer="Provisional gameplay", citation=P, paragraphs=[
"Delarus had signed more treaties, guarantees and relief pledges than anyone in its foreign ministry could list from memory. Some had been signed by governments that no longer existed; some promised things Delarus no longer had; a few contradicted each other. In 1991 the foreign ministry asked its docket clerks to compile a register of every obligation Delarus had undertaken abroad and of the official who was answerable for each.",
"The docket clerks were trained to read treaties the way inspectors read accounts: slowly, precisely and with a strong suspicion that something was missing. They found obligations in treaties, in exchanges of letters, in the minutes of conferences and in the private correspondence of former ministers. They found a guarantee to a neighbour that nobody had remembered for twenty years and a relief pledge that had been honoured twice by different ministries.",
"The register gave Delarus an idea. If its clerks could read treaties so carefully, perhaps they could read other countries' treaties too. A small country could make itself indispensable by verifying the obligations of larger ones: checking that pledges were kept, that relief reached the people it was meant for, that guarantees were honoured. It would make Delarus useful to everyone, and suspected by some.",
"Delarus now knows what it has promised. It must decide whether to offer its inspectors to the rest of Usea.",
], options=[
("Offer Delarus's inspectors to verify other countries' treaties.", 10, "axis:oversight+3"),
("Keep the inspectors at home and finish the register first.", 5, "axis:records+3"),
]),
dict(n=46, tag="DEL", title="A Docket for Every Pledge", picture="warning", layer="Official", citation="ACES Chronicle, 1996 / 04.20; Delarus's dockets are provisional gameplay", paragraphs=[
"When Central Usea announced on the twentieth of April 1996 that the asteroid Ulysses would strike the Earth, the pledges began within days. Governments pledged money, shelters, trains and grain; firms pledged equipment; international bodies pledged coordination. Delarus opened a docket for every pledge it heard of, recording who had promised what, to whom and by when, and then waited to see which pledges would be kept.",
"The docket clerks worked through the spring and summer. By autumn the dockets filled a room. Some pledges were already being honoured: shelters were being built, grain was being stored, trains were being reserved. Some had been quietly withdrawn. Many had simply never been mentioned again, and nobody had been asked to account for them. The clerks marked these with a single word: pending.",
"The dockets raised a question Delarus could not answer alone. The relief accounts of the Usean governments would be the largest sums of money spent on any single purpose in the continent's history. If nobody inspected them, some of the money would vanish. Delarus could offer to audit them, sending its inspectors to follow the money and say where it went. Or it could inspect only its own relief and leave foreign accounts to foreign governments.",
"Every pledge now has a docket. Somebody must decide who reads them.",
], options=[
("Publish the docket of pledges, kept and pending.", 10, "axis:oversight+3;prep+1"),
("Send the pledges' dockets privately to each government.", 5, "axis:records+3"),
]),
dict(n=47, tag="DEL", title="Orders Signed the Night Before", picture="coup", layer="Official", citation="ACES Chronicle, 1997 / 05.30; events in Delarus are provisional gameplay", paragraphs=[
"On the thirtieth of May 1997 a coup broke out across Usea. In Delarus it lasted less than a day. A group of officers seized a barracks and a broadcasting station, issued a proclamation and a series of orders, and were arrested the next morning when their own units declined to follow them. Unified Command defeated the coup across the continent within days. In Delarus the coup was over before most people had heard of it.",
"It left dockets everywhere. The officers had signed orders during their few hours of power: requisitions, transfers, appointments and one order dissolving the audit office. Some of the orders had been carried out before anyone realised who had signed them. Lorries had been requisitioned, officials had been transferred, money had been moved. The coup was over; its paperwork was not.",
"The government had to decide which of the coup's orders still stood. Some of them were harmless, and reversing them would cost more than leaving them in place. Some were clearly illegal. Some fell in between: a requisition that had delivered supplies to a town that needed them, an appointment of an official who had turned out to be competent. The inspectors wanted every order reviewed; the commanders wanted the matter closed.",
"Delarus has always believed that a signature creates an obligation. It must now decide what a signature means when the signer had no right to sign.",
], options=[
("Void every order signed during the coup.", 10, "axis:oversight+3"),
("Review each order and keep those that served the public.", 5, "axis:records+3;stab+0.01"),
]),
dict(n=48, tag="DEL", title="The Battery's Civilian Accounts", picture="desert", layer="Official", citation="ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge (an FCU-led international project); Delarus's verification role is provisional gameplay", paragraphs=[
"On the nineteenth of June 1998 Stonehenge was completed in San Salvacion's desert. The battery was an international project led by Central Usea, and its member governments had paid for it. Within a month several of them asked Delarus whether its inspectors could read the project's civilian accounts: the roads, the water, the housing and the services provided to the host district. The military accounts would remain secret. The civilian accounts, the members argued, should be verified by someone who had not written them.",
"Delarus's inspectors were flattered and cautious. A battery in someone else's desert, operated by someone else's crews, was not a matter for Delarus. The civilian accounts, however, were exactly the kind of thing Delarus was good at: roads that had been paid for and not built, water works that had been built and not paid for, housing allocated to people who did not exist. The inspectors suspected that all three would be found.",
"The commanders in Delarus's own government had a different worry. If Delarus's inspectors read the battery's accounts, Delarus would be seen as part of the project. If the project became a target, so might its inspectors. Neutrality was not Delarus's tradition, but caution was.",
"The members are waiting for an answer. Delarus must decide whether its inspectors will travel to the desert.",
], options=[
("Send the inspectors to read the civilian accounts.", 10, "axis:oversight+3"),
("Read the accounts in Delarus, from copies.", 5, "axis:records+3"),
]),
dict(n=49, tag="DEL", title="The Checklists Meet the Night", picture="impact", layer="Official", citation="ACES Chronicle, 1999 / 07.08; Delarus's relief is provisional gameplay", paragraphs=[
"On the eighth of July 1999 Ulysses broke apart over the Earth. In Delarus every relief docket was opened at once. Shelters that had been inspected with a tape measure and a torch filled with families; stores that had been counted against their dockets were opened and issued; relief convoys that had been listed for inspection left their depots and took to the roads.",
"The inspectors discovered which of their checklists were real. Most were. The shelters held, the stores were full and the convoys knew their routes. Some were not. A shelter that had passed inspection had been repaired with the wrong materials; a store that matched its docket had been filled with the wrong supplies; a convoy listed as ready had no fuel. The gap between the docket and the reality, which the inspectors had published every year, was suddenly a matter of life and death.",
"The government had to decide how relief would be run in the weeks ahead. Relief officers could be given emergency warrants to requisition what they needed and account for it later, making relief faster and accounts slower. Or every relief issue could be docketed and inspected even now, making relief slower and every sack traceable. The inspectors argued that a crisis was exactly when theft was easiest. The relief officers argued that a crisis was exactly when speed mattered most.",
"The fragments have fallen. Delarus must decide whether to trust its checklists or its officers.",
], options=[
("Send the inspectors with the convoys.", 10, "axis:oversight+3"),
("Send the convoys first, and the inspectors after.", 5, "axis:command+3"),
]),
dict(n=50, tag="DEL", title="Stay or Move On?", picture="refugees", layer="Official", citation="ACES Chronicle, 2000 / 04.21; Delarus's refugee policy is provisional gameplay", paragraphs=[
"On the twenty-first of April 2000 Erusea closed its border to refugees, and some of those turned back reached Delarus. They were docketed at the border, as everyone in Delarus was docketed: name, origin, family, health, skills and destination. The dockets were thorough, and they all ended with the same blank line. Under the heading destination, the clerks wrote nothing, because nobody had told them what to write.",
"The docket clerks pressed the question. A docket with a blank line could not be closed, and Delarus did not leave dockets open. Was the refugee to stay or to move on? If to stay, where, and doing what? If to move on, to where, and who would receive them? The interior ministry referred the question to the cabinet, and the cabinet referred it to a committee, and the dockets piled up in the border offices.",
"Two answers were proposed. Refugees could be allowed to settle in Delarus once they were registered, housed and assigned work, creating the most complete refugee register in Usea and a population that would change the country. Or they could cross Delarus under inspection, with food and care, but not stay, their dockets travelling with them to whatever country would take them.",
"The clerks are waiting to fill in the blank line. So are the people the dockets describe.",
], options=[
("Fill in the line case by case, as the dockets require.", 10, "axis:records+3"),
("Write a single destination for everyone until the policy is set.", 5, "axis:command+3"),
]),
dict(n=51, tag="DEL", title="The Page Marked War", picture="war", layer="Official", citation="ACES Chronicle, 2003 / SUMMER (Erusea invades San Salvacion); Delarus's wartime exposure is provisional gameplay", paragraphs=[
"In the summer of 2003 Erusea invaded San Salvacion and seized Stonehenge, and Central Usea's partners found themselves at war. In Delarus the foreign ministry opened its obligations ledger at the page marked war and found it longer than expected. Over the years Delarus had promised the coalition supplies, transit, liaison officers and inspectors, in treaties, letters and conference minutes. Some of the promises had been made by governments that no longer existed, but they were still in the ledger.",
"The government had to decide which promises it would keep. The commanders wanted all of them honoured at once, by order. The inspectors wanted each one reviewed, docketed and delivered on schedule. The coalition wanted everything immediately and was not interested in the difference. Requisitions began within the week, and so did the disputes: lorries taken from farmers who needed them for the harvest, warehouses taken from firms that had been storing relief.",
"Requisition tribunals were set up to hear the disputes. They worked quickly, and they gave every owner a receipt that a court would honour. The commanders called them a delay; the inspectors called them the only reason the requisitions were still lawful. Delarus's shelters, inspected for the fragments, were inspected again for the raids, and fewer of them passed.",
"The war has its own dockets now. Delarus must decide whether to run its war effort by order or by inspection.",
], options=[
("Honour every listed obligation on schedule.", 10, "ws+0.05;axis:command+2"),
("Review each obligation before delivering it.", 5, "stab+0.02;axis:oversight+2"),
]),
dict(n=52, tag="DEL", title="Open or Sealed", picture="peace", layer="Provisional gameplay", citation=P, paragraphs=[
"The crisis years are over. Delarus holds the most complete records of the war in Usea: requisitions, orders, losses, obligations and the dockets of every refugee who crossed its borders. Its inspectors kept them through the fragments, the refugees and the war, copying everything and storing the copies somewhere else. Now the government must decide what to do with them.",
"Some want the records opened. A commission could hear anyone who claimed to have been wronged: farmers whose lorries were requisitioned, families who lost relatives, refugees whose dockets were closed without their consent. It would take years and make enemies, but it would leave Delarus with an honest account of what it did. The inspectors who kept the records, many of whom worked through the war at great personal risk, want them read.",
"Others want the records sealed. The country has been through enough. Opening the records would reopen every quarrel, every grievance and every suspicion, and would set neighbours against each other for a generation. Sealing them for a fixed period would let the country move on, and the records would still be there when the people they describe were no longer alive to be hurt by them.",
"Delarus has always believed in records. It must now decide whether it believes in reading them.",
], options=[
("Ask the inspectors who kept the records.", 10, "axis:records+3;stab+0.01"),
("Ask the families the records describe.", 5, "axis:oversight+3"),
]),
]
