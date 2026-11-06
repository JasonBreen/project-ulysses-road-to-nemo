"""Long-form events for the Usean partners package (namespace ac_ud_up).

Each event is fired by exactly one focus (the reward token event:N in content.py).
Bodies are built with seams.event_text() and checked with seams.event_problems().
Options use the same reward tokens as focuses and never reach a regime effect.
"""

PROVISIONAL_SNS = "no official source describes San Salvacion's internal politics or policies; this is an authored alternative"
PROVISIONAL = {
    "AMB": "no official source covers Amber; its politics, treaty role and policies are authored for this mod",
    "UGE": "no official source covers Ugellas; its politics, treaty role and policies are authored for this mod",
    "DEL": "no official source covers Delarus; its politics, treaty role and policies are authored for this mod",
}

EVENTS = [
# --------------------------------------------------------------------------- San Salvacion
dict(n=1, tag="SNS", title="The Question of the Administration", picture="politics", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The question was not asked in a speech. It was asked in a memorandum, circulated among the permanent secretaries of San Salvacion's ministries on a winter morning in 1991, and it ran to a single line: on what authority does this administration govern? The national administration had kept the republic neutral through the long quarrels of its neighbours, balanced its budget in most years and opened more schools than it closed. It had never held an election, and nobody inside it could remember the last time anyone had asked it to.",
"The answers came back within a week, and they did not agree. The ministry of justice returned a draft charter written by its own junior lawyers, who had been meeting in the evenings with schoolteachers and district clerks. The civil protection service, the one national body every district already obeyed, returned a proposal that read like an inspection manual: a Directorate, a rota, and powers defined by the emergencies they were meant to meet. From the dry interior came a letter signed by the chairs of a dozen water councils, asking why a capital that could not fill a cistern should decide anything else at all.",
"The administration's own answer was the shortest. It works, the memorandum's author wrote in the margin of the last reply. The continent is rearming, the economy is fragile, and neutrality is a habit that a single bad year can break. Continuity is also a choice, and from now on it will have to be defended as one.",
"None of these answers is a government yet. Each is a movement, a draft, a committee and a set of grievances. Which of them San Salvacion follows will decide who holds the seals when the hard years come.",
], options=[
("Let the question be argued in public.", 5, "axis:continuity+2;stab-0.01"),
("The administration will answer it in its own time.", 10, "axis:dispatch+2"),
]),
dict(n=2, tag="SNS", title="The Charter Assembly Convenes", picture="politics", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The Charter Assembly met in the old customs hall because no other public building in the capital had enough chairs. Delegates came from every district with their credentials pinned to their coats and the draft charter folded in their pockets, many of them reading its first article for the hundredth time. San Salvacion is a neutral republic. It takes no side in the quarrels of other nations and lends its territory to no army. The second article was shorter and more dangerous: the republic is governed by an assembly elected by its citizens.",
"The national administration handed over the seals on the first afternoon. There was no ceremony, only a permanent secretary placing a wooden box on the presidium's table and asking for a receipt. Most of the administration's officials stayed at their desks. They had run the country for a generation, and the assembly needed someone who knew where the files were. Some of them believed in the charter. Others believed it would fail within a year and intended to be in the room when it did.",
"The presidium's first decisions were modest. It confirmed the budget, renewed the neutrality law and appointed a commission to draw the electoral districts. The commission's maps would take months, and every district wanted its own boundaries drawn by its own people. The assembly also had to decide what to do with the civil protection service and the water councils, whose movements had lost the argument but not their followers.",
"Outside the customs hall, the capital watched with the wary patience of a city that had seen many promises. A charter is a paper. Whether it becomes a constitution depends on what the assembly does when the paper is tested, and the years ahead will test it.",
], options=[
("Call the first general election within the year.", 0, "stab-0.02;axis:continuity+4"),
("Govern under the charter until the districts are drawn.", 0, "stab+0.02;axis:dispatch+3"),
]),
dict(n=3, tag="SNS", title="The Directorate Takes the Keys", picture="politics", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The civil protection Directorate did not seize power. It inspected it. On the morning of the transfer, officers in grey service jackets visited every ministry with a clipboard, counted the keys, checked the fire exits and asked each permanent secretary to name a deputy who could act in their absence. By noon the national administration had been replaced by a rota, and the rota had been posted on the door of every public building in the capital.",
"The Directorate's proclamation was brief and carefully worded. It assumed the functions of government for the duration of the national emergency. It did not say what the emergency was, when it had begun or when it would end. Asked by a foreign correspondent, a Directorate spokesman explained that a small country surrounded by rearming neighbours was always in an emergency, and that the only question was whether it prepared for one.",
"The districts accepted the change faster than the capital did. The civil protection service had been the only national body that came when called: it had dug out villages after floods, run water convoys in dry summers and kept the shelters in repair. The Charter Movement's lawyers and the water councils protested, wrote letters and were invited to join advisory committees, which met regularly and decided nothing.",
"Government by checklist has its virtues. It is predictable, it does not panic and it keeps records. Whether it can govern a republic rather than an emergency is a question the Directorate has chosen not to ask.",
], options=[
("Publish the rota and every name on it.", 0, "stab+0.02;axis:protection+3"),
("Keep the Directorate's membership confidential.", 0, "axis:dispatch+3;tech:land_doctrine"),
]),
dict(n=4, tag="SNS", title="A Government of the Councils", picture="politics", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The standing committee of the district councils arrived in the capital by bus, with a crate of water tallies, a list of unrepaired roads and no intention of staying longer than necessary. The national administration had agreed to hand over the ministries after the congress of councils made clear that the districts would otherwise stop paying for them. The committee took the keys, held its first meeting in the ministry of public works and voted to move half the ministry back to the interior.",
"Government by council is government by argument. Every district sends a delegate, every delegate has a mandate, and every mandate is about water. The dry districts want cisterns, the river districts want flood works and the capital wants to be remembered at all. The committee decides by majority, publishes its votes and reverses itself when the councils instruct it to, which happens often enough that ministry officials now keep two drafts of every order.",
"The capital is unhappy, and its newspapers say so daily. The Charter Movement calls the councils a federation of complaints; the civil protection service quietly continues its rotas under a committee it does not respect. Foreign embassies ask which office they should telephone and are given several numbers. Yet the wells are being dug, the roads repaired in the order the councils chose, and for the first time the interior can point to a government that answers when it calls.",
"Whether a republic can be governed from its districts depends on whether the districts can agree on anything except their grievances. The committee intends to find out.",
], options=[
("Move the ministries to the districts.", 0, "axis:dispatch+4;stab-0.02"),
("Keep the ministries in the capital, under council audit.", 0, "axis:continuity+3;stab+0.01"),
]),
dict(n=5, tag="SNS", title="A Mandate without a Ballot", picture="politics", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The national administration published its mandate on a Monday, in every newspaper and on the door of every district office. It was four pages long. It said what the administration governed, which was everything it had always governed; for how long, which was until the republic decided otherwise by lawful means; and on whose behalf, which was the citizens of San Salvacion, whose consent it did not claim but whose trust it intended to earn.",
"The mandate's critics noticed what it did not say. It did not say how the republic might decide otherwise, or what lawful means would be recognised, or who would recognise them. The Charter Movement called it a lease without a landlord. The water councils called it a promise from the people who had broken most of the others. The civil protection service, which had expected to be asked to govern, said nothing at all and renewed its rotas.",
"Inside the administration, the mandate was received as a reform. Permanent secretaries now had to publish their procedures, answer written questions from district offices and appear before an inspector they could not dismiss. Some resigned. Most adapted, as they had always adapted, and found that a published procedure was easier to defend than an unwritten one.",
"A mandate without a ballot is still a promise, and promises can be counted. The administration has given the republic something to count. If it keeps the count honest, continuity may yet become consent.",
], options=[
("Answer every written question in public.", 5, "axis:continuity+3;stab+0.01"),
("Answer through the district offices, quietly.", 10, "axis:dispatch+3"),
]),
dict(n=6, tag="SNS", title="What the Desert Needs First", picture="desert", layer="Provisional gameplay", citation=PROVISIONAL_SNS, paragraphs=[
"The civil survey of the desert district took a year and three vehicles, two of which did not come back under their own power. Its report ran to nine volumes. The first eight counted things: wells, cisterns, schools, clinics, roads, families and the distances between them. The ninth volume was a single chapter, and it asked the only question the government had to answer: what does the desert need first?",
"The water engineers answered at once. A district without water loses its people, and no road will bring them back. Wells, cisterns and pumping stations should come first, maintained by the people who use them and paid for by tariffs they set themselves. The cost would be high and the benefits local, but a district that could drink could stay.",
"The transport officials answered differently. A district without roads cannot sell what it produces, cannot reach a hospital and cannot be reached when something goes wrong. Roads would bring tankers, doctors and buyers. Water could follow the roads; roads could not follow the water. The cost would be high and the benefits national, and the haulage firms were already offering to carry public freight in return for concessions.",
"The survey's authors refused to choose. They wrote that both answers were right and that the republic could not afford both at once. The desert district has waited a long time for the capital to notice it. It will notice which answer the capital chooses.",
], options=[
("Publish the full survey, all nine volumes.", 5, "axis:continuity+2;tech:construction_tech"),
("Send the survey teams back to finish the count.", 10, "axis:dispatch+2"),
]),
dict(n=7, tag="SNS", title="News from the Skully Islands", picture="coup", layer="Official", citation="ACES Chronicle, 1995 / 12.31; San Salvacion's response is provisional gameplay", paragraphs=[
"The news reached San Salvacion's capital on the last day of 1995, by way of a radio bulletin and a telephone call from the border posts. Robert Tyler of Central Usea's Army Southern District had eliminated a rebel base in the Skully Islands, and Unified Command had defeated the rebels with Scarface Squadron. The bulletin was brief, the telephone call was not. The border officers wanted to know whether anyone fleeing the islands was likely to come their way, and what they were supposed to do if someone did.",
"Nobody in the capital knew. San Salvacion had no part in the action and wanted none. The government's first instinct was the one it always had: issue a statement of neutrality, recognise the authorities that existed and take no side. The statement was drafted within the hour. The harder question was what neutrality meant at a border post in the interior, at night, when a truck without papers stopped at the barrier.",
"The border posts asked for rules. Who may cross? Who must be detained? Who may be returned, and to whom? The interior ministry produced a draft that answered the first question, avoided the second and referred the third to a committee. The civil protection service offered to staff the posts with its own rota. The water councils pointed out that the posts were in their districts, and that nobody had asked them.",
"A rebellion on islands far away has turned into a question at San Salvacion's own gate. The answer the government gives tonight will become the rule for the years ahead.",
], options=[
("Detain no one without a charge; return no one without a hearing.", 10, "axis:continuity+3;stab+0.01"),
("Close the border posts to anyone without papers.", 5, "axis:protection+3;xp:army+10"),
]),
dict(n=8, tag="SNS", title="The Warning", picture="warning", layer="Official", citation="ACES Chronicle, 1996 / 04.20; San Salvacion's preparations are provisional gameplay", paragraphs=[
"Central Usea announced it on the twentieth of April 1996: the asteroid Ulysses would strike the Earth. The announcement was read on every radio station in San Salvacion within the hour, and in the afternoon the telephones at the national observatory rang without stopping. The observatory had two astronomers and one telescope that could see anything useful. They spent the evening explaining to ministers, journalists and frightened callers what an orbit was and why nobody in San Salvacion could change one.",
"The government's first task was to decide what to tell the country. Some ministers wanted to say very little until the international estimates were firmer. Others argued that silence would be filled by rumour, and that rumour would be worse than any estimate. The civil protection service wanted to publish shelter instructions at once. The finance ministry wanted to know what the instructions would cost before anyone promised them.",
"The second task was to decide what to ask of the neighbours. San Salvacion was small and neutral and had always relied on being left alone. Ulysses would not leave anyone alone. Central Usea was speaking of an international response, and an international response would need land, roads, water and the consent of whoever owned them.",
"By midnight the cabinet had agreed only that it would meet again in the morning. The observatory's lights were still on. Above the capital, the sky looked exactly as it always had, which was the hardest thing of all to explain.",
], options=[
("Tell the country everything we know, and what we do not.", 10, "prep+1;axis:protection+2"),
("Wait for the international estimates before speaking.", 5, "axis:continuity+2;stab+0.01"),
]),
dict(n=9, tag="SNS", title="The Coup across Usea", picture="coup", layer="Official", citation="ACES Chronicle, 1997 / 05.30; events inside San Salvacion are provisional gameplay", paragraphs=[
"On the thirtieth of May 1997 a coup broke out across Usea. The radio carried fragments of it all night: barracks seized in one country, a broadcasting station in another, an airfield that changed hands twice before dawn. Unified Command would defeat it, with Scarface 1 among the pilots sent against the rebels, but on that night nobody in San Salvacion's capital knew how it would end, and several officers had stopped answering their telephones.",
"The government met in the basement of the interior ministry because the basement had a generator. Ministers arrived one at a time, each with a different rumour. The garrison of the capital was loyal; the garrison of the capital was wavering; a battalion in the interior had declared for no one in particular and was waiting to see who won. The civil protection service had already put its own rota on the doors of every ministry and was asking for authority to keep it there.",
"By morning the worst rumours had proved false. A handful of officers had joined the coup, a few dozen soldiers had followed them and most had gone home when they realised nobody else was coming. The capital had not fallen. The republic had not been tested so much as frightened, and the question now was what to do with the frightened men who had briefly thought otherwise.",
"Every government in Usea is asking the same question this week. San Salvacion's answer will say what kind of republic it means to be.",
], options=[
("Arrest the conspirators and try them under ordinary law.", 10, "axis:continuity+3"),
("Hold them under emergency powers until the continent is calm.", 5, "axis:protection+3;stab-0.01"),
]),
dict(n=10, tag="SNS", title="The Host Terms", picture="desert", layer="Official", citation="ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge (an FCU-led international project in neutral San Salvacion's desert); the host terms are provisional gameplay", paragraphs=[
"Central Usea's proposal arrived in a folder thicker than most of the ministry's budgets. An international project, led by Central Usea, would place a battery of railguns in a desert region of San Salvacion to destroy the fragments of Ulysses before they reached the ground. The folder contained maps, engineering summaries, security annexes and a short letter asking for the host government's consent.",
"Consent was the only thing San Salvacion had to give, and the cabinet discovered that it was worth more than anyone had expected. The project needed land, which the republic owned. It needed roads, water and power, which the host district had in short supply. It needed airspace, customs exemptions, security arrangements and the promise that the host would neither obstruct the work nor claim what it produced. In return it offered protection from the sky, which was not something San Salvacion could refuse.",
"The cabinet divided along familiar lines. One faction wanted a sovereign lease: the site leased, not ceded, with national law, national customs and national inspectors at the gate. Another wanted joint custody: a share of the site's security and a voice inside the perimeter, at the cost of standing visibly beside the guns. A third wanted to know what would happen to the battery when the fragments had fallen, and found that nobody in the folder had answered.",
"Whatever the engineers' timetable, the host must decide what it is lending. Neutrality has never been tested by a guest this large.",
], options=[
("Negotiate every annex, line by line.", 10, "axis:continuity+3"),
("Consent quickly and negotiate the details afterwards.", 5, "axis:protection+3;prep+1"),
]),
dict(n=11, tag="SNS", title="Eight Guns in the Desert", picture="desert", layer="Official", citation="ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge (eight railguns); the host's response is provisional gameplay", paragraphs=[
"On the nineteenth of June 1998 Stonehenge was completed. Eight railguns stood in San Salvacion's desert, their barrels pointed at an empty sky that would, in a little over a year, be full of falling stone. Central Usea's engineers held a short ceremony. San Salvacion's delegation stood at the back, in borrowed hard hats, and was thanked in the third paragraph of the speech.",
"The host district had lived beside the project for long enough to know what it meant. Convoys on roads built for farm carts. Floodlights that turned the night white. A perimeter that kept moving outward, swallowing grazing land and a road the villages had used for generations. The district had also seen clinics, wages and paved streets it had asked the capital for in vain. Its people did not know whether they were protected or occupied, and most suspected they were both.",
"In the capital, the completion raised a question the host terms had not answered. The battery was built to defend the world from Ulysses. It stood on neutral soil, operated by foreign crews, with power enough to bring down anything that flew. San Salvacion had agreed to host it. It had not agreed to become the most strategically important desert on the continent, and it had no say over what the guns would be used for once the sky was clear.",
"Tonight the host district is quiet, and the guns are silent. San Salvacion must decide how to live beside them.",
], options=[
("Thank the engineers and claim nothing.", 10, "stab+0.02;axis:protection+2"),
("Remind the members, in writing, whose desert this is.", 5, "axis:continuity+3"),
]),
dict(n=12, tag="SNS", title="The Night of the Fragments", picture="impact", layer="Official", citation="ACES Chronicle, 1999 / 07.08; San Salvacion's relief is provisional gameplay", paragraphs=[
"On the eighth of July 1999 Ulysses passed the Roche limit and broke apart. In San Salvacion the night began with a light brighter than the moon and ended with a sound nobody who heard it would forget. Stonehenge fired into a sky full of falling stone, again and again, and the villages of the host district counted the shots until they lost count.",
"By morning the reports were confused and contradictory. Radio links to the interior failed for hours, the telephone exchanges jammed and rumours travelled faster than any official word. The government could confirm only what its own wardens and drivers had seen: a sky that had been on fire, a battery that had fired until its crews were exhausted, and roads filling with people from across the region who had not waited for instructions before leaving home.",
"The plans met the night they were written for. Some worked; wardens knew their streets, trains ran to their timetables and the field hospitals opened before the first ambulances arrived. Some did not; keys were held by the wrong office, convoys waited for orders that never came and a shelter built for a hundred people was found to hold three hundred. The preparation record closed at midnight. Everything done afterwards would be relief.",
"The morning brings its own questions. What was lost, what can be saved and what must be rebuilt are questions for the coming months. Tonight there is only the work.",
], options=[
("Send the field hospitals where the damage is worst.", 10, "axis:protection+3"),
("Restore water and roads before anything else.", 5, "axis:dispatch+3;tech:construction_tech"),
]),
dict(n=13, tag="SNS", title="The Border That Closed", picture="refugees", layer="Official", citation="ACES Chronicle, 2000 / 04.21; San Salvacion's refugee policy is provisional gameplay", paragraphs=[
"On the twenty-first of April 2000 Erusea stopped taking in refugees. The displaced of the fragment year, who had walked toward Erusea's cities, found the border closed and turned back. Many of them turned toward San Salvacion. Within a week the border posts in the interior reported columns on the roads: families with handcarts, lorries piled with furniture, children carrying younger children.",
"The government had planned for the fragments. It had not planned for this. The reception centres opened in the fragment year were still full. The water convoys were already stretched. The districts that would receive the newcomers were the same districts that had been stretched to breaking a year before, and their councils wanted to know who would pay.",
"The cabinet considered two answers. San Salvacion could be a refuge: open reception centres, register the newcomers, give them the right to work and accept that the country would change. Or it could be a corridor: feed them, treat them, give them a ticket and send them onward to whoever would take them. The first would cost money and comfort; the second would cost something harder to measure.",
"Erusea's decision was made in Erusea. San Salvacion's decision will be made here, and the people on the roads are waiting for it.",
], options=[
("Open the border posts tonight and decide the policy tomorrow.", 10, "stab-0.01;axis:protection+3"),
("Hold the columns at the posts until the policy is decided.", 5, "axis:continuity+3"),
]),
dict(n=14, tag="SNS", title="The Summer of the Invasion", picture="war", layer="Official", citation="ACES Chronicle, 2003 / SUMMER; the exact day and San Salvacion's response are provisional gameplay", paragraphs=[
"In the summer of 2003 Erusea invaded San Salvacion and seized Stonehenge. The first reports came from the host district: columns on the roads, aircraft over the perimeter, the project's crews disarmed or fled. Within days the railguns that had been built to shoot down falling stone were turned against aircraft, and the sky over the desert, which had been the safest in Usea, became the most dangerous.",
"San Salvacion's neutrality ended without the country choosing to end it. Its letters to every capital, its sovereign lease or its joint custody, its ledger of everything given and refused: none of it stopped a single armoured column. The border posts in the interior fought for an afternoon and were overrun. The government, meeting in the same basement it had used on the night of the coup, found itself governing a country that was being cut in pieces around it.",
"Central Usea and its partners are already at war with Erusea, and the coalition's help will come slowly if it comes at all. The government now has to decide how it will govern what it still holds, and how it will protect the people, the records and the institutions it no longer controls. Some ministers want to hold the free districts at any cost. Others want to prepare the ministries for occupation: to keep working quietly, keep records and wait.",
"The war has come to the desert because of the guns in it. Whatever San Salvacion does next, it will do as a country at war.",
], options=[
("Every ministry stays at its post.", 10, "axis:continuity+3;ws+0.05"),
("Move the ministries' records out of the capital tonight.", 5, "axis:protection+3;ws+0.03"),
]),
dict(n=15, tag="SNS", title="Liberation", picture="peace", layer="Official", citation="ACES Chronicle, 2005 / 07.10 (San Salvacion liberated); the reconstruction of government is provisional gameplay", paragraphs=[
"San Salvacion was liberated in the summer of 2005. The occupier's columns withdrew from the towns they had held for two years, the guns in the desert were silent, and the government returned to a capital that had learned to manage without it. People came out into the streets, not to cheer, at first, but to look: at each other, at the damage, at the soldiers of the coalition who had come so far to reach them.",
"Liberation has its own disorder. Officials who stayed under occupation and kept the quiet ministries running meet officials who governed the free districts and officials who fled abroad. Each has a record, and each record says something different about the others. Collaborators, real and alleged, are denounced in the squares. Families look for relatives who were displaced by the fighting, and the count of the displaced is longer than anyone wanted to believe.",
"The government's first act is to read the ledgers. The ledger of the occupation lists requisitions, arrests and debts. The host's ledger lists everything San Salvacion gave the battery and everything it was promised in return. The national budget, published every year under the administration or the assembly or the councils, has not been published for two. Somebody has to decide what the republic owes, and to whom.",
"The country that comes out of the war is not the country that went into it. It has governed itself in pieces. It must now decide how to govern itself whole.",
], options=[
("Try collaborators in ordinary courts, with ordinary evidence.", 10, "stab+0.03;axis:continuity+3"),
("Purge the ministries before they reopen.", 5, "axis:protection+3;stab-0.02"),
]),
dict(n=16, tag="SNS", title="The Desert after the Guns", picture="desert", layer="Official", citation="ACES Chronicle, 2005 / 04.02, and Super Weapons, Stonehenge (seven of eight batteries destroyed, where the war follows that course); the site's future is provisional gameplay", paragraphs=[
"The battery in the desert was built for one crisis and fought over in another. Where the war followed its historical course, ISAF destroyed it in April 2005, and seven of its eight great batteries lie broken in the sand. Where the war took another course, or never came, the guns still stand, silent, their foreign crews gone or going. Either way, the site belongs to San Salvacion again, and San Salvacion must decide what it is.",
"The host district has opinions. Some of its people want the site fenced and closed for ever: a grave for those who died there and a warning to anyone who might want to build something like it again. Others point to the roads, the power lines and the water works that the battery left behind, and ask why a district that went without them for a century should leave them to rust in the name of remembrance.",
"The survey teams have opinions too. The site is dangerous: unexploded munitions, damaged power systems, ground nobody wants to test. Whatever the government decides, the first years will be spent making the desert safe, and the decision will shape where the surveyors start.",
"Above the desert, the sky is empty again. The country that hosted the guns has to decide how to live without them.",
], options=[
("Ask the host district to decide first.", 10, "axis:dispatch+3;stab+0.01"),
("Make the decision in the capital and explain it in the district.", 5, "axis:continuity+3"),
]),
]


def all_events():
    """Every partner event in ID order."""
    from narrative_amber import EVENTS as amber
    from narrative_ugellas import EVENTS as ugellas
    from narrative_delarus import EVENTS as delarus
    return sorted(EVENTS + amber + ugellas + delarus, key=lambda event: event["n"])
