"""Long-form events for the Central Usea (FCU) Usea Depth package, namespace ac_ud_fcu.

Each body has at least three paragraphs and 180 words, ends with a source-layer
line built by seams.event_text(), and uses straight quotes only. Official
paragraphs paraphrase the ACES Chronicle; everything around them is labelled.
Chronicle people (Robert Tyler, Scarface, Robert Sinclair) appear in text only.
"""
from content import R, pp, stab, ws, army, air, navy, manpower, flag, timed, ready, recovery

EVENTS = {}
OFFICIAL = "Official"
MOD = "Mod provenance"
GAME = "Provisional gameplay"
ALT_NOTE = "alternate history. No source shows a Central Usea regime change before ISAF's founding on 22 August 2003"


def E(number, title, paragraphs, layer, cite="", options=(("a", "Understood.", "", 100),), picture="assembly", variants=None):
    """options: (suffix, text, effects, ai_factor). variants: [(trigger, paragraphs)] for conditional bodies."""
    EVENTS[number] = dict(id="ac_ud_fcu.%d" % number, title=title, paragraphs=paragraphs, layer=layer, cite=cite,
                          options=list(options), picture=picture, variants=variants or [])


# ------------------------------------------------------------------ politics
E(1, "The Federal Question", [
    "The cabinet room is too small for the meeting it is holding. Ministers sit along the table, their deputies along the walls, and behind them the files that have followed every government since the Federation was formed: the treaty commitments, the regional grievances, the defence estimates, the arguments about who pays for what. Central Usea is the largest state on the continent. It chairs the Treaty Organization, it leads the faction its partners joined, and it has no plan for what happens when something truly large goes wrong.",
    "The question on the table is not new. It has been asked after every flood, every border scare and every budget that collapsed in committee. How should a federation this size govern itself in an emergency? One answer is that it already does: the presidency and the Assembly have managed every crisis of the last decade, slowly, imperfectly and lawfully. A second answer comes from the staff colleges and from some of the ministers who served in them: an emergency needs a single authority, and a statute that says when the soldiers take over is better than an improvised one. A third answer comes from the Assembly's back benches: if the Federation must face a crisis, it should face it with every party in government, so that nobody is left outside to blame the rest.",
    "The cabinet secretary has prepared a paper on each answer, and each paper is honest about its costs. Keeping the present government costs speed: every emergency decision will pass through the presidency, the ministries and, where the law requires it, the Assembly, and the law requires it often. A directorate costs consent: the regions, the courts and the newspapers would accept military authority only for as long as they believed the emergency was real. A unity cabinet costs coherence: every party would bring its own priorities to the table, and a government of rivals would argue about every decision before it took one. The papers recommend none of the three. They ask the cabinet to decide which cost it is most willing to pay.",
    "None of the three is a plot. Each has its supporters inside this room. The cabinet agrees on only one thing tonight: it will choose before the emergency comes, not during it.",
], GAME, "the 1991 government is mod provenance; the three paths are provisional gameplay, and two of them are " + ALT_NOTE, options=(
    ("a", "Put the question to the cabinet.", pp(15), 100),
    ("b", "Hear the regional governments first.", R(stab(0.01), pp(-10)), 20),
), picture="assembly")

E(2, "The Emergency Powers Debate", [
    "The draft runs to forty pages. Its first article defines a continental emergency; its second says who may declare one; its third, which the press will quote for a decade, says that during an emergency the executive authority of the Federation passes to a directorate formed around the commanders of Unified Command. The presidency remains. The Assembly remains. Neither governs until the directorate hands the authority back.",
    "The officers who wrote it insist that it is a fire code, not a coup. A federation of this size, they argue, cannot evacuate a coast or answer a rebellion through committees that meet twice a week. They point to the regional governments that disagreed for three weeks over a flood relief convoy, and to the Assembly sessions that ended without a vote while the water rose. Write the rules now, they say, while nobody is frightened, and the rules will be fairer than anything improvised in a panic.",
    "The opposition reads the same forty pages differently. A statute that hands power to soldiers when soldiers declare an emergency, they say, is not a fire code. It is a door, and someone will walk through it. The cabinet's own lawyers note, carefully, that the draft contains no expiry date and no court with the power to end the emergency.",
    "Outside the cabinet the draft leaks within a week, as drafts do. The regional governments ask whether a directorate would respect their constitutions. The courts ask whether they would still sit. Unified Command's own commanders, consulted informally, are divided: some welcome a clear chain of authority in a crisis, others warn that an army which governs in an emergency will be blamed for every hardship the emergency brings. Nobody outside the drafting committee asks the question the committee keeps returning to, which is what would happen if the emergency never ended.",
    "The cabinet sends the draft to committee with instructions to keep it. The argument has only begun.",
], GAME, ALT_NOTE, options=(
    ("a", "Add an expiry clause and keep going.", R(stab(0.01)), 100),
    ("b", "Keep the draft as the staff wrote it.", R(pp(25), stab(-0.02)), 50),
), picture="directorate")

E(3, "All-Party Talks", [
    "The invitations go out on federal letterhead to every party with a seat in the Assembly, including two that have not spoken to the governing majority in years. The talks will be held in a committee room rather than the cabinet room, at a table with no head, and the first session will have no agenda beyond a single question: if the Federation faced a disaster tomorrow, who would each party trust to lead it?",
    "The answers are less hostile than anyone expected. The regional parties want a guarantee that the provinces will not be overruled by the capital in an emergency. The opposition wants seats in any cabinet that asks it to share responsibility. The smaller parties want to be consulted before announcements rather than after. Nobody, it turns out, wants to be the party that refused to sit down while the country prepared for the worst.",
    "What they want in return is the problem. A unity government means dividing the portfolios, and every portfolio given to a partner is one taken from the majority that won the last election. The presidency's advisers warn that a cabinet of rivals will argue for weeks over every decision. The Assembly's elders reply that a cabinet of rivals cannot easily be brought down by the rivals it contains.",
    "The presidency's staff draw up a map of the Assembly that looks nothing like the usual seating plan. It shows which party is strong in which region, which ministries each could plausibly run and which pairs of parties have never sat in the same cabinet. The map is covered in pencil within a day. By the end of the week it has become the working document of the talks, and the staff who drew it spend their evenings explaining it to party whips who have never before had to count anyone's seats but their own.",
    "The first session ends late. The second is already scheduled.",
], GAME, ALT_NOTE, options=(
    ("a", "Offer the opposition real portfolios.", R(stab(0.02), pp(-20)), 100),
    ("b", "Start with advisory seats only.", R(pp(10)), 40),
), picture="assembly")

E(4, "The Course Held", [
    "The cabinet secretary's annual memorandum is usually read by the cabinet and nobody else. This year it is leaked within a day, and the newspapers print it in full, because for once it reads less like an administrative note and more like a chapter of history.",
    "It lists the decade's emergencies in order. The rebellion in the southern islands at the end of 1995, ended by the Southern District and Unified Command. The announcement of April 1996, when the Federation told the world that Ulysses would strike. The coup of May 1997, which broke out across Usea and was defeated by Unified Command. The completion of Stonehenge in June 1998. After each entry it records the same thing: the presidency governed, the Assembly sat, the courts opened in the morning. Nothing was suspended that the constitution did not allow to be suspended.",
    "The memorandum does not claim that this was efficient. It admits the weeks lost to committees and the convoys that waited for signatures. It argues only that a government which kept its own rules through all of this has earned the trust it will need when the fragments fall.",
    "The opposition calls the memorandum self-congratulation. The public, by the polls, calls it reassuring.",
], OFFICIAL, "Chronicle, 1995 / 12.31, 1996 / 04.20, 1997 / 05.30 and 1998 / 06.19 for the dated events; the memorandum is provisional gameplay", options=(
    ("a", "Publish the memorandum officially.", R(stab(0.02)), 100),
    ("b", "Keep it as an internal record.", R(pp(25)), 30),
), picture="assembly")

E(5, "The Directorate", [
    "The declaration is read at noon on every federal channel. A continental emergency exists. Under the emergency statute, executive authority passes to a directorate formed around Unified Command. The presidency will continue its ceremonial and diplomatic duties. The Assembly will continue to sit, and may debate whatever it wishes, but it will not govern until the directorate returns the authority it has taken.",
    "Within the hour the directorate's first orders reach the ministries. Movement permits for the evacuation zones will be issued by district commanders. Requisition orders for transport take effect immediately rather than after a thirty-day notice period. Public announcements about the emergency will come from a single information board. The orders are clear, numbered and signed, and in the ministries that have spent years arguing over who signs what, some officials are quietly relieved.",
    "Others are not. Two regional governments issue statements reserving their constitutional rights. A newspaper prints the forty pages of the statute on its front page under a single word: Read. In the Assembly, the opposition demands to know when the emergency will end. The directorate's answer is that it will end when the danger has passed, and that it will say so.",
    "Abroad, the treaty partners are informed before the declaration is read, and their governments respond with careful statements: they note the emergency, they trust that the Federation's commitments are unchanged and they look forward to working with whatever authority now speaks for it. Erusea says nothing at all in public. In the directorate's first briefing, an intelligence officer reports that Erusean diplomats have asked their counterparts in three capitals whether the Federation's army now governs it, and that nobody has yet given them a satisfying answer.",
    "Outside the capital, life continues. The trains run. The schools open. A great many people discover that the government has changed and that their day has not.",
], GAME, ALT_NOTE + "; the directorate is an unnamed office, not a new person", options=(
    ("a", "The directorate governs.", R(ws(0.02)), 0),
), picture="directorate")

E(6, "The Directorate Review", [
    "The statute required a review once the emergency eased, and the drafters wrote that clause to be inconvenient. The directorate must report to the Assembly in open session: what it decided, what it spent, whom it detained and why the emergency should continue, if it should.",
    "The report is long and, by the standards of emergency governments, honest. Stonehenge is complete. The evacuation plans are written, rehearsed and funded. The districts that went silent during the coup of 1997 are back under federal administration. Against this the opposition lays its own list: the newspapers that were warned, the officers removed without hearings, the regional governments overruled. Both lists are true.",
    "The debate runs for three days. The directorate's officers answer every question put to them, which surprises the members who expected to be ignored. On the third evening the Assembly's speaker reads the statute's final article aloud: the authority taken in an emergency may be returned by the directorate, or it may be extended by the directorate, and the Assembly may only advise.",
    "Ulysses will arrive in a year. The directorate must now decide what kind of government will meet it.",
], GAME, ALT_NOTE, options=(
    ("a", "Take the Assembly's advice under consideration.", R(stab(0.01)), 0),
), picture="directorate")

E(7, "Authority Returned", [
    "The directorate's last order is three lines long. The continental emergency declared under the statute is ended. Executive authority returns to the presidency and the Assembly. The staff of the directorate will return to Unified Command within thirty days.",
    "The handover is undramatic by design. Ministers who have spent years carrying out orders sit down again at the cabinet table to issue their own. The district councils are dissolved, and the regional governments resume the duties they had before. The information board is closed, and the newspapers go back to asking questions first. The evacuation plans the directorate wrote stay in force, because they are good plans, and the incoming cabinet has no wish to rewrite them a year before the impact.",
    "The officers go back to their headquarters. Some are bitter, convinced that they have been dismissed on the eve of the emergency they prepared for. More are relieved. Unified Command was built to fight, not to govern, and several of its senior officers say privately that they never want to sign a ration order again.",
    "The opposition's leaders, invited to the handover, are given the directorate's files in full: every order it issued, every requisition, every detention and every warning sent to a newspaper. The files run to thousands of pages, and the opposition's researchers find in them both less than they feared and more than they would like. Most of the directorate's work was administrative, dull and competent. Some of it was not, and those pages will be read aloud in the Assembly for months.",
    "In the Assembly the opposition, which has spent the directorate's whole tenure demanding this moment, finds that it has nothing left to demand. The speaker calls the first ordinary session in years. It begins, as ordinary sessions do, with a quarrel about the agenda.",
], GAME, ALT_NOTE + "; the restored presidency is the mod's 1991 government", options=(
    ("a", "The Federation governs itself again.", R(stab(0.02)), 0),
), picture="assembly")

E(8, "The Directorate Extended", [
    "The renewal is announced as a technical matter. The emergency has not passed; Ulysses has not yet arrived; therefore, under the statute, the directorate remains. The announcement is two sentences long and contains no date.",
    "The reaction is not technical. The Assembly passes a resolution, by a large majority, asking the directorate to state when it will return authority. The directorate replies that it will do so when the debris has fallen and the evacuees are home, and that it cannot know when that will be. Both the resolution and the reply are printed in every newspaper, and the newspapers are not warned for printing them, which some commentators take as a sign of restraint and others as a sign of confidence.",
    "Inside the ministries the extension changes little. The district councils go on meeting. The evacuation timetables go on being rehearsed. What changes is the mood in the officer corps. Officers who joined the directorate as a temporary duty begin to talk about it as a career, and officers who opposed it begin to keep their opinions to themselves.",
    "Abroad, the extension is noticed. The treaty partners, who accepted the directorate as an emergency measure, begin to ask in private how long an emergency can last. Their questions are polite, and the directorate answers them politely, but the partners' liaison officers report home that the Federation's government has stopped describing itself as temporary. That observation travels, as observations do, and by the end of the year it has reached capitals far beyond the treaty.",
    "The directorate's own staff has drafted a further review for the year after the impact. Nobody outside the directorate has seen it.",
], GAME, ALT_NOTE, options=(
    ("a", "The emergency continues.", R(ws(0.02), stab(-0.01)), 0),
), picture="directorate")

E(9, "The Unity Government", [
    "The new cabinet is sworn in at a ceremony that runs an hour longer than planned, because every party wanted its ministers to read their oaths in full. The government of national unity has twice as many parties as any cabinet in the Federation's recent memory and a programme that fits on a single page.",
    "The page has five commitments. Prepare the Federation for whatever comes. Share the cost of preparation fairly between the regions. Keep the Treaty Organization's commitments. Govern openly, with the Assembly consulted before announcements. Hold the unity government together until the emergency has passed, and not a day longer.",
    "The last commitment is the one the commentators quote. Unity governments, they observe, tend to end in recrimination; this one has written its own expiry into its founding document. The ministers, asked about it at their first press conference, give the same answer in five different party accents: they did not join to stay.",
    "Abroad, the treaty partners welcome the new cabinet with a warmth that surprises the federal diplomats. A Federation governed by all its parties, one partner's ambassador observes, is a Federation whose commitments will not change at the next election. Erusea's statement is shorter and more guarded: it notes that the Federation's government has changed, and it hopes that the Federation's policy has not. The cabinet chooses to read both statements as compliments.",
    "The former majority accepts its reduced share of the cabinet with more grace than expected. The office that now leads the Federation answers to the whole Assembly, and in the first week every party discovers how slow consensus is. In the second week they discover how difficult it is to oppose a government that includes you.",
], GAME, ALT_NOTE + "; the unity cabinet is an unnamed office, not a new person", options=(
    ("a", "The unity government takes office.", R(stab(0.02)), 0),
), picture="assembly")

E(10, "The Unity Mandate", [
    "The unity government's founding page said it would last until the emergency had passed. The emergency has not passed: the impact is still ahead, and after the impact there will be years of debris and recovery. The parties must decide whether their promise to leave in time still binds them.",
    "The debate is held in the Assembly, not in the cabinet, because the cabinet has learned that its own members argue more honestly in public. The regional parties want to stay: the burden-sharing formula is theirs, and they do not trust a single-party government to keep it. The former majority wants to stay as well, because it no longer holds a majority on its own. The smallest parties, which have gained the most from sharing power, are the most anxious to show that they can give it up.",
    "In the end the Assembly renews the mandate through the years of the impact by a margin larger than any single party could have produced. The renewal carries a condition, written by the smallest party in the cabinet: an open review of the unity government's record, held in public, when the debris has fallen.",
    "The cabinet accepts the condition. The newspapers note that it is the first time in the Federation's history a government has written its own audit into its mandate.",
], GAME, ALT_NOTE, options=(
    ("a", "Renew the mandate with the review.", R(stab(0.02), pp(10)), 0),
), picture="assembly")

E(11, "The Federal Settlement", [
    "Every emergency leaves laws behind. The decade that brought the southern rebellion, the Ulysses announcement, the coup and the completion of Stonehenge has left more than most: emergency statutes, temporary agencies, requisition orders that were never formally withdrawn and regional agreements signed in a hurry by people who have since left office. The cabinet commissions a single document to account for all of them.",
    "The settlement sorts the decade's laws into three piles. The first will expire on schedule: the requisition orders, the movement permits, the temporary levies. The second will be made permanent because they worked: the evacuation registers, the continuity sites, the regional emergency boards. The third pile is the hardest, the powers that worked and that no government should keep, and the settlement proposes that the Assembly vote on each of them separately, in public, so that nobody can say later that they were kept by accident.",
    "The vote takes most of a session. Some powers survive by narrow margins; others are struck down with applause. The government that proposed the settlement loses two votes it wanted to win and accepts both results.",
    "The commentators agree on one thing. Whatever government carries the Federation into the new century will inherit a shorter statute book than the one it might have had.",
], GAME, "the settlement is provisional gameplay; the dated events it lists are Chronicle, 1995 / 12.31 to 1998 / 06.19", options=(
    ("a", "Hold the votes in public.", R(stab(0.02)), 100),
    ("b", "Keep the third pile in force for one more year.", R(pp(30), stab(-0.01)), 20),
), picture="assembly")

E(12, "Chair of the Treaty", [
    "The Usean Treaty Organization meets this year, as it does every year, under Central Usea's chair. The Federation's presidency of the treaty is written into its founding arrangements, and its leadership of the faction the partners joined is older than most of the ministers attending. Nobody at the table questions that the Federation will lead. The question is how.",
    "The partners arrive with familiar complaints. Their liaison officers spend more time waiting for federal decisions than making joint ones. The treaty's plans are drafted in the federal capital and sent out for comment rather than written together. The common budget is mostly federal money, which means the federal treasury decides what the treaty can afford. They are not asking the Federation to lead less, they say; they are asking it to lead as a partner rather than as a landlord.",
    "Across the frontier, the standoff in western Usea between Erusean and treaty forces continues as it has for years: patrols that watch each other, exercises that are announced carefully and incidents that are settled quietly. The treaty's purpose, as most of its members understand it, is to keep that standoff from becoming anything worse.",
    "The federal delegation listens, takes notes and promises proposals before the next meeting.",
], MOD, "the Usean Treaty Organization, the Federation's presidency of it and the 1991 western standoff come from the mod's 1991 bookmark and country history, not from the Chronicle", options=(
    ("a", "Promise a partnership of equals.", R(stab(0.01), pp(-10)), 100),
    ("b", "Promise efficiency first.", R(pp(15)), 40),
), picture="treaty")

E(13, "The Burden Question", [
    "The treaty secretariat's accounts are three hundred pages long and say one thing clearly: Central Usea pays for most of everything. The common staff, the exercises, the liaison offices, the shared radars and the reserve stores are funded overwhelmingly from the federal treasury, and the partners' contributions, while real, would not keep the treaty running for a month without the Federation.",
    "In the Assembly the accounts are read two ways. One reading says the Federation is being taken advantage of: its taxpayers fund the defence of partners who contribute little and complain often. The other says the Federation is buying something cheaply: a treaty whose plans it writes, whose staff it leads and whose members follow its lead in every crisis. Both readings appear in the same newspaper on the same day.",
    "The partners, asked for their view, are cautious. They would accept a shared scale if it were fair and phased in slowly. They would also accept the present arrangement, and they would not object if the Federation chose to keep paying. What they would resent is a demand to pay more combined with no greater voice in how the money is spent.",
    "The cabinet must choose before the next budget. Either answer will be defended in the Assembly as prudent and attacked as naive.",
], MOD, "the treaty and its costs are mod provenance; the accounts and the choice are provisional gameplay", options=(
    ("a", "Prepare both proposals for the cabinet.", R(pp(10)), 100),
), picture="treaty")

E(14, "A Decade of the Treaty", [
    "The Treaty Organization marks the end of the decade with a short ceremony and a long report. The ceremony is a flag raised at the secretariat, a speech by each member's representative and a reception that ends early because the staff have exercises the next morning. The report is the part that matters.",
    "It records what the treaty survived. A rebellion in the southern islands that ended within a day of the year's end. The announcement that Ulysses would strike, and the years of shared preparation that followed. A coup that broke out across Usea and was defeated, with the treaty members exchanging what they knew while it was still under way. The completion of Stonehenge by an international project led from the Federation. None of these was the war the treaty was founded to deter, and the treaty met all of them anyway.",
    "It records what the treaty learned. Shared radars are worth more than separate ones. Liaison officers who live in a partner's capital understand it better than those who visit. A secretariat that keeps its own records remembers what the ministers forget.",
    "The report ends with a sentence the members argued over for a week: the treaty enters the next century with its purpose unchanged and its members closer than they were. Nobody at the ceremony says what everyone is thinking, that the next century will test that sentence.",
], MOD, "the treaty is mod provenance; the dated events in its report are Chronicle, 1995 / 12.31 to 1998 / 06.19", options=(
    ("a", "Adopt the report.", R(stab(0.02), pp(10)), 100),
), picture="treaty")

E(15, "The Skully Islands", [
    "The report reaches the capital on the last day of 1995. Robert Tyler, commanding the FCU Army Southern District, has eliminated a rebel base in the Skully Islands. Unified Command has defeated the rebel forces there through the actions of Scarface Squadron. The operation is over before most of the cabinet has learned it began.",
    "The official record of the action is short, and the cabinet decides to keep it that way. It names the islands, the Southern District, Unified Command and the squadron, because those are the facts the commanders reported. It does not name a wider conspiracy, because nobody has shown one. It does not move any border or claim that anything has changed hands. Far to the north, on the same day, other forces attack the facilities at Avalon Dam; this report does not concern them, and the cabinet is careful not to connect the two.",
    "What happens next is the cabinet's to decide. The southern islands have been part of the Federation's map for a long time and part of its attention for much less. The Southern District wants a permanent garrison. The regional government wants roads and clinics. The courts want the surviving rebels. All three requests are on the cabinet table before the new year's first session.",
    "The islanders, for their part, want to know whether the Federation will still be paying attention next year.",
], OFFICIAL, "Chronicle, 1995 / 12.31. The aftermath choices are provisional gameplay; the Belkan war chain is not called", options=(
    ("a", "Record the Southern District action.", R(army(5)), 100),
    ("b", "Ask the Southern District for its recommendations.", R(pp(10)), 50),
), picture="islands")

# ------------------------------------------------------------------ the warning and the evacuation
E(16, "Ulysses", [
    "On 20 April 1996 Central Usea announces that the asteroid Ulysses will strike the Earth. The announcement comes from the Federation, and with it a burden: a government that knows something like this has no right to keep it, and no excuse for being unready.",
    "The days that follow are the strangest in the Federation's history. Markets close and reopen. Churches stay open all night. The roads out of the coastal cities fill on the first weekend and empty on the second, as people realise that the impact is years away and that they have jobs to go back to. The telephone lines to every ministry are jammed with callers asking the same question: what is the government going to do?",
    "The honest answer, for the first week, is that the government does not yet know. It knows the date the fragments will arrive. It does not know where they will fall, how many there will be or how large. It knows that the Federation has three years, and that three years is both a long time and no time at all to move people, build shelters and prepare a continent for a sky that will fall.",
    "Abroad, the announcement lands differently in every capital. Some governments confirm it within hours. Some ask for the Federation's figures before they say anything at all. Across Usea, the treaty partners ask the same question the Federation's own citizens are asking, and receive the same honest answer: nobody yet knows where the fragments will fall, and every government on the continent will have to prepare as though they might fall anywhere. For the first time in a generation, every country on the continent faces the same enemy, and it is not one another.",
    "The cabinet meets every day that week. By the end of it, the first orders have been written: count everyone, plan every route, stock every depot. The age of preparation has begun.",
], OFFICIAL, "Chronicle, 1996 / 04.20. The public reaction and the federal response are provisional gameplay; impact sites are not invented", options=(
    ("a", "Prepare the Federation.", R(stab(-0.02), ws(0.03)), 100),
    ("b", "Speak to the nation first.", R(stab(0.01), pp(-15)), 40),
), picture="warning")

E(17, "The Census", [
    "The evacuation census sends a federal enumerator to every household in the threatened districts, and a great many outside them. Each household answers the same questions: how many people live here, how many could walk ten kilometres, how many need a hospital bed, where would they go if they had to leave and how would they get there.",
    "The answers are more useful than anyone in the ministries expected, and more alarming. Hundreds of thousands of people have nowhere to go: no relatives inland, no car, no money for a train ticket. Entire districts depend on a single bridge or a single rail line. The coastal hospitals hold more patients who cannot be moved than the interior hospitals have beds to receive them. Old people living alone are counted, sometimes for the first time, and the enumerators' notes are full of addresses where nobody had visited in years.",
    "The census also measures something the ministries did not ask about. People were willing to answer. Enumerators report that doors opened, that coffee was offered and that families wanted to talk about their plans. A government that announced the end of the world and then came to count its citizens has, it seems, been believed.",
    "Every plan written in the next three years will begin with these numbers.",
], GAME, "the census follows the official 1996 / 04.20 announcement; its findings are provisional gameplay", options=(
    ("a", "Publish the census totals.", R(stab(0.01)), 100),
    ("b", "Keep the district figures confidential.", R(pp(15)), 30),
), picture="evacuation")

E(18, "The Drill", [
    "At ten in the morning the sirens sound across the threatened districts. For the next twelve hours the Federation rehearses its evacuation: buses arrive at assembly points, trains leave on the numbered timetables, reception towns open their schools and gymnasiums, and millions of people walk through the plan they have read about for a year.",
    "Much of it works. The rail timetables run within an hour of schedule. Most assembly points are staffed. The reception towns feed more people than they expected and run out of blankets only in the evening. Some of it fails. Three bridges jam for hours. One district's buses never arrive, because the requisition order went to a company that had sold them. A hospital discovers that its evacuation route passes through a tunnel too low for its ambulances.",
    "Every failure is written down. The drill's purpose, the organisers remind the press, is to find these problems now, while there is time to fix them and nobody is in danger. The newspapers print the failures anyway, and some of the headlines are unkind.",
    "The public's verdict is mixed. Some families complain about a lost day of work. More say that they now know where to go. In one reception town the children of evacuees and the children of residents play football in the school yard until dark, and the photograph is on every front page the next morning.",
], GAME, "the drill follows the official 1996 / 04.20 announcement; its conduct is provisional gameplay", options=(
    ("a", "Fix the failures and drill again.", R(ready(2), pp(-15)), 100),
    ("b", "Fix the failures quietly.", R(pp(10)), 30),
), picture="evacuation")

E(19, "The Final Count", [
    "The impact is months away. The evacuation staff go back over every number they have: seats on every train, places in every reception town, litres in every fuel reserve, beds in every hospital. For three years the numbers have grown. Now the question is whether they are large enough.",
    "The final count is presented to the cabinet as a single table, district by district. Where the column is green, the plan can move everyone it needs to move. Where it is amber, it can move most people if nothing else goes wrong. Where it is red, some people will not be moved in time, and the table says how many. There are fewer red rows than there were a year ago, and there are still too many.",
    "The cabinet's choices are narrow now. It can order more requisitions and spend the money it was saving for the recovery. It can ask the treaty partners for transport. It can decide which districts to evacuate first and which to protect in place. Or it can accept the table as it stands and hope that the fragments fall where the columns are green.",
    "Nobody at the table believes in that hope. The table goes back to the ministries with instructions to turn every red row amber before the summer.",
], GAME, "the impact date is official (Chronicle, 1999 / 07.08); the count and its districts are provisional gameplay and invent no impact sites", options=(
    ("a", "Spend the recovery reserve now.", R(ready(4), pp(-25)), 100),
    ("b", "Ask the treaty partners for transport.", R(ready(3), stab(-0.01)), 40),
), picture="evacuation")

# ------------------------------------------------------------------ Stonehenge
E(20, "The Stonehenge Project", [
    "The proposal comes from the Federation's engineers, but it is not a federal project alone. Central Usea will lead an international effort to build a battery of railguns large enough to destroy the fragments of Ulysses before they reach the ground. Other governments will contribute money, scientists and components. The battery will stand in a desert region of San Salvacion, a neutral country, so that no single state's territory holds the world's defence.",
    "The engineers' presentation to the cabinet is careful about what it promises. Eight guns. Enormous power. Fire control that can track fragments falling faster than any aircraft. A site remote enough to be safe and accessible enough to be built. It promises nothing about schedules, because the engineers do not yet know how long the work will take, and they have learned not to guess in front of ministers.",
    "The cabinet's questions are about everything else. Who will pay, and how much? Who will command the battery once it is built? What happens to it after Ulysses has passed? The engineers answer the first question with estimates, the second with a proposal and the third with silence.",
    "The consortium is founded before the questions are settled. There is no time to settle them first.",
], OFFICIAL, "Chronicle, 1998 / 06.19; Super Weapons, Stonehenge (an FCU-led international project of eight railguns in a desert region of neutral San Salvacion). No construction dates are given; the consortium's decisions are provisional gameplay", options=(
    ("a", "Found the consortium.", R(pp(-15)), 100),
), picture="stonehenge")

E(21, "Stonehenge Completed", [
    "On 19 June 1998 Central Usea completes Stonehenge. In a desert region of San Salvacion, eight railguns stand ready to fire at the sky.",
    "The ceremony at the site is short, because the engineers are still working. The dignitaries see the guns from a distance, hear a speech about the international effort that built them and leave before the afternoon heat. The engineers stay. For them the completion is a milestone, not an ending: the guns must be calibrated, the fire control tested, the crews trained and the power plants brought to full load. The fragments will not wait for a second ceremony.",
    "In the Federation the news is received with something close to joy. For two years the public has heard about evacuation routes, shelter programmes and fuel reserves: all the ways to survive the impact. Stonehenge is the first answer that promises to fight it. The newspapers print the guns on their front pages. Children draw them. A popular song about them is on the radio within a month.",
    "In the cabinet room the mood is more measured. Stonehenge will not stop every fragment, and nobody honest has claimed that it will. And the questions the cabinet could not settle two years ago, who commands the battery and what happens to it afterwards, have not gone away.",
], OFFICIAL, "Chronicle, 1998 / 06.19; Super Weapons, Stonehenge. The public reaction is provisional gameplay", options=(
    ("a", "Celebrate the engineers.", R(stab(0.02)), 100),
    ("b", "Keep expectations measured.", R(pp(15)), 40),
), picture="stonehenge")

# ------------------------------------------------------------------ the coup
E(22, "The Coup Inquiry", [
    "On 30 May 1997 a coup broke out all across Usea. Unified Command answered it, and Scarface 1 flew. The cabinet has the reports of what happened. It does not yet have an explanation.",
    "The inquiry's terms of reference are written to avoid the mistake every government makes after a coup: deciding the answer before asking the question. The inquiry will establish which commands went silent and when. It will establish what orders were given, and by whom. It will establish what warnings existed and why they were missed. It will not assume a wider conspiracy, and it will not publish names until the evidence supports them.",
    "The officer corps watches the inquiry with dread and relief in equal measure. Dread, because the inquiry will look into every command, including those that did nothing wrong. Relief, because an inquiry with rules is better than a purge without them. Several senior officers ask to give evidence before they are summoned.",
    "Abroad, the treaty partners ask to share what the inquiry finds. They lived through the same day, and some of their own commands went quiet too. The cabinet agrees to share the inquiry's findings with them, provided they share their own.",
], OFFICIAL, "Chronicle, 1997 / 05.30 (a coup across Usea, defeated by Unified Command through Scarface 1). The inquiry is provisional gameplay; no rebel country list or wider conspiracy is asserted", options=(
    ("a", "Open the inquiry in public.", R(stab(0.01), pp(-10)), 100),
    ("b", "Hold the first hearings in closed session.", R(pp(15)), 40),
), picture="coup")

E(23, "The Lessons of 30 May", [
    "The inquiry's report runs to six volumes. The first five are evidence: timelines, signal logs, orders, interviews and maps of which commands went silent and when. The sixth, the one the newspapers read, is twenty pages long and contains its findings.",
    "It finds no single hidden hand. The coup broke out across Usea at once, and the inquiry can show how it was coordinated, but it cannot show who coordinated it beyond the officers already identified, and it says so plainly. What it can show is why the coup spread as far as it did before Unified Command stopped it. Commands that had not been visited in years had grown loyal to their own officers rather than to any government. Promotion lists had been decided by those same officers. Signals between districts went through a few hubs, and the plotters knew which ones to silence.",
    "The report's recommendations are practical rather than dramatic: rotate commanders more often, review promotions centrally, add redundancy to the signal network and make sure that someone in the capital notices when a garrison stops talking.",
    "The report ends with a sentence that is quoted for years afterwards: the coup failed because enough officers kept their oaths, and the Federation should not rely on that again.",
], GAME, "the coup is official (Chronicle, 1997 / 05.30); the inquiry's findings are provisional gameplay and assert no wider conspiracy", options=(
    ("a", "Adopt the recommendations.", R(army(10)), 100),
), picture="coup")

E(24, "The Coup Settlement", [
    "The cabinet closes the coup file at a single meeting. The file is thick. It holds the inquiry's six volumes, the tribunal records or the reconciliation transcripts, the officer corps review, the new rules for command and the memorial's list of the dead.",
    "The settlement is a short statement that sets out what has changed and what has not. Officers who led the coup have been tried or heard and, where the evidence required it, punished. Officers who followed them have been dealt with according to what they did rather than which command they served in. The rules that let commands drift away from the government have been rewritten. The memorial is open, and it does not carry the names of the plotters.",
    "What has not changed is the Federation's view of its own forces. The settlement says, in its final paragraph, that the soldiers, sailors and aircrews who answered on 30 May are the reason the coup failed, and that the government's trust in its armed forces is undiminished. The paragraph was rewritten nine times.",
    "The officer corps reads the statement closely. Most of it reads as fair. The final paragraph, several senior officers say, is the first time in years that a government has thanked them in writing.",
], GAME, "the coup is official (Chronicle, 1997 / 05.30); its settlement is provisional gameplay", options=(
    ("a", "Close the coup file.", R(stab(0.02)), 100),
), picture="coup")

# ------------------------------------------------------------------ the impact
E(25, "Impact Night", [
    "On 8 July 1999 Ulysses passes the Roche limit and breaks apart. The fragments fall across the world.",
    "In the Federation's operations rooms the night is measured in reports. Tracking stations call out fragments. Stonehenge fires. District commanders report what they can see from their windows and what their radios tell them. Some reports are of nothing at all: sirens, a sky full of light and then silence. Others are of fires, collapsed buildings, roads cut and towns without power. The evacuation plans written over three years are tested in a single night, and the staff in the operations rooms will remember for the rest of their lives which districts they were responsible for.",
    "By morning the shape of the night is clear, if not its full cost. Some districts were spared. Some were not. The reception towns are full. The hospitals that were moved are working; some that could not be moved are not. The fragments have not stopped falling, and will not for years.",
    "Abroad, the same night has fallen on every country. The treaty partners report their own damage in the hours after the impact, and the first relief requests reach the Federation before its own count is complete. Across the frontier, Erusea has its own fires and its own dead. The radio carries reports from places the Federation's ministers have never visited, and the reports all sound alike. For a few days, the impact makes the continent's quarrels seem very small.",
    "The cabinet meets at dawn. There is one item on the agenda: relief. Who will run it, with what and for how long? The plans for this moment were written months ago. Now they must be chosen.",
], OFFICIAL, "Chronicle, 1999 / 07.08. The Federation's night is provisional gameplay; no impact sites, casualty figures or province damage are invented", options=(
    ("a", "Begin the relief effort.", R(stab(-0.02), ws(0.02)), 100),
), picture="impact")

E(26, "The Count After the Impact", [], GAME, "the readiness index and its outcomes are provisional gameplay; no impact sites or casualty figures are invented", options=(
    ("a", "Publish the count.", R(stab(0.01)), 100),
), picture="impact", variants=[
    ("has_country_flag = FCU_ud_impact_prepared", [
        "Two weeks after the impact the federal statistics office delivers its first count. It is incomplete, as first counts always are, but it is enough to tell the cabinet that the Federation's preparations held.",
        "In district after district the plans worked as written. The timetables ran. The reception towns received the people they were built for. The shelters closed on time and opened again in the morning. The fuel reserve was enough, the hospitals that moved arrived intact, and the stay-behind reports or the empty towns told the operations rooms what they needed to know. The damage is real and the dead are counted, but the count is far smaller than the planners feared in 1996.",
        "Abroad, the treaty partners ask to see the Federation's plans, and the cabinet sends them without hesitation. If the Federation's preparations worked, they are worth sharing; the debris will keep falling for years, and the continent will need every plan that held.",
        "The cabinet reads the count district by district, in silence, and then the minister responsible for the evacuation asks for a moment to thank the staff who wrote the plans. Nobody objects. The Federation met the impact prepared, and it begins the recovery with its institutions intact and its people trusting them.",
    ]),
    ("has_country_flag = FCU_ud_impact_strained", [
        "Two weeks after the impact the federal statistics office delivers its first count. It is incomplete, as first counts always are, but it is enough to tell the cabinet that the Federation's preparations bent and did not break.",
        "Where the plans were finished they worked. Where they were not, the gaps showed. Some timetables ran late; some reception towns filled beyond capacity; some districts waited a day or more for relief that the plans said would arrive in hours. The count of the dead is larger than it should have been, and the cabinet knows which unfinished plans account for it.",
        "The opposition demands an inquiry and the cabinet agrees to one, on the condition that it reports after the recovery rather than during it. The relief staff, already exhausted, are told that their work will be judged later and that, for now, it must simply continue.",
        "The cabinet reads the count district by district, in silence. There is no thanksgiving and no blame, not yet. The Federation met the impact strained, and its recovery will begin with crowded camps, tired staff and a public that wants to know why the preparations were not finished in time.",
    ]),
    ("has_country_flag = FCU_ud_impact_overwhelmed", [
        "Two weeks after the impact the federal statistics office delivers its first count. It is incomplete, as first counts always are, but it is enough to tell the cabinet that the Federation's preparations were overwhelmed.",
        "Too few of the plans were finished. Timetables existed on paper but not in the depots. Reception towns were designated but not built. Shelters stood half-complete, and districts that should have been evacuated were not. The count of the dead is the number every minister feared in 1996, and in some districts it is still rising as the rescuers reach them.",
        "Abroad, the treaty partners send what they can, though many have their own dead to count. Relief convoys cross the borders within days. For a government that prepared too little, the help of neighbours is both a rescue and a reproach, and the cabinet accepts it as both.",
        "The cabinet reads the count district by district, in silence. Then it begins the hardest work of the decade: a relief effort far larger than any plan prepared for, under a public whose trust has been spent. The Federation will recover. It will take longer, and it will remember why.",
    ]),
])

E(27, "The Federal Economy", [
    "Central Usea's treasury is the largest on the continent, and its economy is larger than those of its treaty partners combined. That size is both an advantage and an argument. The Federation can afford things its neighbours cannot, which means that every question about the economy becomes a question about what the Federation owes the continent and what the continent owes it.",
    "Two schools of thought divide the economic ministries. The first holds that the Federation grows richest by trading: lower tariffs for treaty partners, open ports, contracts awarded to the cheapest bidder across Usea. Prosperity shared, this school argues, is the best defence a treaty can have. The second holds that the Federation must be able to provide for itself in an emergency: steel, engineering, aircraft and power produced at home, with federal credit directed to the plants that matter. Self-reliance, this school argues, is the only insurance that never lapses.",
    "Neither school is new, and both have been in government before. What is new is the sense, shared by both, that the decade ahead will test whichever choice the cabinet makes. The ministers do not know yet what that test will be. They know only that a federation this large should not meet it unprepared.",
    "The cabinet asks for both programmes in writing. It will choose between them before the next budget.",
], GAME, "the economic programmes are provisional gameplay", options=(
    ("a", "Ask for both programmes.", R(pp(10)), 100),
), picture="economy")

E(28, "The Federal Forces", [
    "The Federation's forces have no declared enemy. The standoff in western Usea is managed, not fought. The treaty partners are allies. The defence estimates are still large, and every year the Assembly asks what they are for.",
    "This year the forces review offers an answer in three parts. The first is treaty defence: the commitments the Federation has made to its partners, which must be credible to be worth anything. The second is the long watch in the west, where Erusean and treaty patrols have watched each other for years without incident and must go on doing so. The third is the part the Assembly least expects: disaster relief. A federation this large, the review argues, will face floods, fires and storms every year, and the forces are the only institution with the trucks, aircraft and discipline to answer them at scale.",
    "The review then asks the question that will shape the decade's budgets. Should the Federation fund its air arm first, because aircraft reach the edges of a large country fastest? Or should it fund the services in proportion, so that none is starved to feed another?",
    "The Assembly's defence committee reads the review twice. For once, it has no objection to the question.",
], GAME, "the review is provisional gameplay; the western standoff is mod provenance from the 1991 bookmark", options=(
    ("a", "Accept the review.", R(army(5)), 100),
), picture="forces")

E(29, "The Southern Lessons", [
    "The Southern District's report on the Skully Islands is not written for the newspapers. It is written for the officers who will hold the district next, and it reads like it: plain, specific and occasionally harsh about the people who wrote it.",
    "It records what went right. When the rebel base was found, the Southern District moved quickly, and when Unified Command was asked to support it, Scarface Squadron answered. The operation ended the rebellion in the islands before it could spread. The report is careful to say no more than that, because the Chronicle of the action says no more than that.",
    "It records what went wrong, too. Reports from the islands had been arriving for months and had been filed rather than read. The district's patrol craft were too few and too slow for the distances involved. The islanders had been asking for roads, clinics and harbours for years, and the rebels had been happy to promise them. None of this caused the rebellion, the report says, but all of it made the district slower to see it.",
    "The report ends with a list of recommendations that the Southern District will carry out whether or not the capital funds them. The capital, reading it, decides to fund them.",
], GAME, "the action is official (Chronicle, 1995 / 12.31); the district's report is provisional gameplay", options=(
    ("a", "Fund the recommendations.", R(pp(-15), army(5)), 100),
), picture="islands")

E(30, "The Ledger of the Decade", [
    "The calendar turns to December 1999 and the cabinet closes the books on a decade it will never forget. The Federation that began the 1990s chairing a treaty and managing a standoff ends them with debris still falling, reception towns still full and a continent that has changed in ways no planner foresaw in 1991.",
    "The ledger is long. On one side stand the things the Federation did: the census, the timetables, the shelters, the reserves, the consortium that built Stonehenge, the forces that answered the coup and the government that, in whatever form it took, held together. On the other stand the things it did not finish: plans that remained on paper when the fragments fell, relief lanes still running when the decade ended, promises made to districts that are still waiting.",
    "Those unfinished things do not vanish because the calendar has turned. Relief work begun in the summer continues into the winter. Plans that proved themselves in July become permanent in December. Whatever government the Federation chose in the 1990s carries its choices into the new century, together with the trust, or the suspicion, they earned.",
    "The forces, too, carry the decade into the new century. The officers who answered the rebellion in the southern islands and the coup of 1997 are now senior commanders. The air arm that rehearsed interceptions for Stonehenge has learned to fly under a falling sky. The treaty's liaison officers, who spent the decade planning evacuations and relief, know their partners' capitals better than any diplomat. None of them knows what the new century will ask of them. All of them know that it will ask something.",
    "Across the frontier, Erusea is counting its own losses, and the refugees who cannot go home are beginning to look for somewhere else to go. The cabinet adds a final line to the ledger: the decade of preparation is over, and the years of consequence have begun.",
], GAME, "the transition follows the official impact (Chronicle, 1999 / 07.08); the ledger and its carry-over are provisional gameplay", options=(
    ("a", "Carry the decade forward.", R(pp(20)), 100),
), picture="warning")

# ------------------------------------------------------------------ 2000-2003
E(31, "The Long Aftermath", [
    "The new century begins under a broken sky. Fragments of Ulysses still fall, less often than in the first weeks and far less predictably. A town that escaped the impact night can be struck on an ordinary Tuesday. Farmers plough around craters. Schools hold debris drills the way they once held fire drills.",
    "The Federation's institutions, tested in 1999, are now asked to do something harder than surviving a single night: to go on working for years in conditions nobody designed them for. The reception towns are still full, because many evacuees have no homes to go back to. The relief budget, meant for months, is entering its second year. Ministries that were reorganised for the emergency must decide whether to reorganise back.",
    "Beyond the Federation, the continent is changing. Erusea has its own losses and its own refugees. The treaty partners, some of them badly hit, look to the Federation for help it can only partly give. The Stonehenge battery, built to defend the world, stands in neutral San Salvacion and is now the most important weapon on the continent, whether anyone intended that or not.",
    "The cabinet's first meeting of the year has no single item on its agenda. It has dozens, and every one of them is urgent.",
], GAME, "the debris and refugee context follows the official impact (Chronicle, 1999 / 07.08); the Federation's response is provisional gameplay", options=(
    ("a", "Take the agenda one item at a time.", R(stab(0.01)), 100),
), picture="impact")

E(32, "The Border Closes", [
    "On 21 April 2000 Erusea stops taking in refugees. The decision is announced in a single statement and enforced the same day. People who reached the Erusean border that morning are turned back; people still on the roads toward it learn of the closure from the radio and stop where they are.",
    "Many of them turn east, toward the Federation and its partners. Within a week the federal reception towns nearest the frontier report arrivals they did not plan for: families who have walked for days, with the documents of three or four different countries and no particular reason to be welcomed by any of them. The camps built for federal evacuees are not large enough for them as well.",
    "In the cabinet room the question is stark. The Federation can open its camps to everyone who arrives and accept the cost, in money and in strain on districts that are themselves still recovering. Or it can ask the treaty partners to share the arrivals by agreed quotas, which spreads the burden and the resentment more evenly but takes time to negotiate.",
    "The cabinet does not condemn Erusea's decision in public. Privately, several ministers note that the Federation's own choice will be watched across the continent, and remembered.",
], OFFICIAL, "Chronicle, 2000 / 04.21 (Erusea stops taking in refugees). Refugee numbers and the federal response are provisional gameplay", options=(
    ("a", "Prepare both options for the cabinet.", R(pp(10)), 100),
    ("b", "Issue a statement of regret.", R(stab(0.01), pp(-10)), 30),
), picture="evacuation")

E(33, "Forward Deterrence", [
    "The orders are signed on a Monday and the movements begin on Wednesday. Federal units take up positions closer to the western frontier, inside federal territory and in plain view. The treaty partners are informed in advance. Erusea is informed by the movements themselves.",
    "The logic of the decision is old and simple. The continent is tense: refugees are crowding the borders, Erusea has closed its own, and the most powerful weapon on Usea stands in a neutral country with no army to speak of. In a moment like this, the Federation's planners argue, ambiguity is dangerous. If every government on the continent can see exactly what the treaty will defend, none of them will be tempted to test it.",
    "The critics' logic is just as old. Units moved forward look like preparation, whatever their orders say. A neighbour that sees troops at its border may decide that it is safer to move first than to wait. The opposition asks in the Assembly whether the government has considered how this looks from the other side of the frontier, and the defence minister answers that the government has considered little else.",
    "The units dig in. The patrols begin. Across the frontier, nothing visible changes, which is either reassuring or not.",
], GAME, "the posture is provisional gameplay; it does not change Erusea's grievance or the Continental War's start", options=(
    ("a", "Hold the forward line.", R(army(10)), 100),
), picture="forces")

E(34, "Continental Restraint", [
    "The cabinet's decision is to do less, and to be seen doing less. Federal units stay in their garrisons. Exercises near the frontier are postponed. The treaty's posture is described in public as defensive, and in private the defence ministry is told to make sure that every movement it orders can be explained to a suspicious neighbour.",
    "Restraint is not the same as weakness, the cabinet insists. The Federation's forces are ready; they are simply not displayed. The government's view is that the continent's tension comes from the impact, the refugees and the closed borders, not from armies, and that adding armies to the mix would only give the tension somewhere to go.",
    "The policy has critics on both sides. Some officers argue that a neighbour who sees no troops will assume there are none. Some partners worry that restraint means the Federation will not defend them. The government answers both with the same assurance: the treaty's commitments are unchanged, and the Federation will keep them.",
    "Whether restraint changes anything on the other side of the frontier, the cabinet cannot know. It knows only that the Federation will not be the one to start what comes next.",
], GAME, "the posture is provisional gameplay; it does not change Erusea's grievance or the Continental War's start", options=(
    ("a", "Keep the units at home.", R(stab(0.01)), 100),
), picture="treaty")

E(35, "The Summer of 2003", [
    "In the summer of 2003 Erusea invades neutral San Salvacion and seizes Stonehenge. The battery built to defend the world from Ulysses is turned on aircraft.",
    "The news reaches the cabinet in pieces. First, reports of movement across the San Salvacion border. Then the silence of the battery's communications. Then the first confirmed loss of an aircraft over the desert, brought down by a weapon designed to strike falling rock. By evening the shape of the day is clear, and so is what it means: the war the treaty was founded to deter has begun, and the enemy holds the most powerful weapon on the continent.",
    "The Federation's choices in the decade of preparation now matter in ways nobody intended. The forces trained for disaster relief must fight. The radar networks built to track fragments must track aircraft. The railways timetabled for evacuation must carry troops. And the engineers who built Stonehenge, many of whom still live at the site with their families, are now in Erusean hands.",
    "Across the Federation, the news arrives on the radio during an ordinary summer evening. In the reception towns, families who were evacuated in 1999 and never went home listen in silence. In the factories, the night shifts hear it from their supervisors. In the treaty partners' capitals, governments that have spent four years recovering from the impact realise that the recovery is over and something worse has begun. Nobody anywhere on the continent has any illusion about what a battery that can destroy falling rock can do to aircraft.",
    "The cabinet meets through the night. By morning it has made the only decision available: the Federation will demand that Erusea withdraw from San Salvacion and from Stonehenge, and it will prepare to make that demand good.",
], OFFICIAL, "Chronicle, 2003 / SUMMER. The exact start day and the cabinet's night are provisional gameplay", options=(
    ("a", "Demand Erusea's withdrawal.", R(ws(0.03)), 100),
), picture="stonehenge")

E(36, "The Home Front", [
    "Two years into the war, and six years after the first fragment fell, the home front is still working. Factories run shifts around the clock. Reception towns that were built for evacuees now house war workers too. Rationing is accepted, not loved. The debris drills continue, and so do the air-raid drills, and children have stopped asking which is which.",
    "The government's home front councils, formed in every region at the start of the war, have become the Federation's most trusted institutions. They decide who gets fuel, which schools close and which factories run. Their decisions are not always popular, but they are made locally, by people the districts know, and that has turned out to matter more than anyone expected.",
    "There are strains. Some regions feel they give more than others. Some families have lost too many people to the impact and the war together. The newspapers, which the government has not censored, print the complaints alongside the casualty lists, and the government answers them in the Assembly rather than ignoring them.",
    "The war's outcome is not yet known. The cabinet notes in its weekly minute that whatever the outcome, the Federation that comes out of it will be one whose people were asked to carry a great deal and did.",
], GAME, "the home front is provisional gameplay", options=(
    ("a", "Thank the councils.", R(stab(0.02)), 100),
), picture="economy")

E(37, "The Federal Question Returns", [
    "In 1991 the cabinet asked how the Federation should govern itself in an emergency. Eight years and several emergencies later, the question is back on the table, because the answer the Federation gave in the 1990s must now be carried into a new century.",
    "If the presidency and the Assembly held their course through the decade, they enter the new century with the trust of having kept their own rules, and with the knowledge that the rules were slow. If a directorate governed, it enters the new century still in power, with an emergency that has passed and critics who say so every day. If a unity government governed, it enters the new century with a mandate written for an emergency that is now a recovery, and parties that are beginning to remember their differences.",
    "Whatever the government, the problems are the same: refugees, debris, a tense frontier and a battery in a neutral country that has become the most important weapon on the continent. The government that solves them will need the confidence of the people it governs. The government that fails will not keep it.",
    "The cabinet meets with the 1991 file open on the table. Someone has written in its margin: still unanswered.",
], GAME, "the 1991 government is mod provenance; the directorate and unity paths are " + ALT_NOTE, options=(
    ("a", "Govern as the Federation chose.", R(pp(10)), 100),
), picture="assembly")

E(38, "The Wartime Constitution", [
    "War demands decisions faster than any constitution was written to provide them. The Federation's government, whatever form it has taken, must now decide how it will make those decisions without losing the legitimacy it needs to keep making them.",
    "The wartime constitution is not a new document. It is a set of agreements written into law: which decisions the war cabinet may take alone, which require the Assembly, which require the regions and which may never be taken at all. It sets a schedule for the Assembly to review the war powers every six months. It guarantees that courts stay open, that newspapers are not closed and that no election is cancelled without a vote.",
    "The agreements are not easy. The officers want speed; the Assembly wants oversight; the regions want to be consulted about what happens on their territory. Every article is a compromise, and every compromise is attacked by someone. The final text satisfies nobody completely, which the government's lawyers point out is usually the sign of a fair document.",
    "The Assembly adopts it by a large majority. The war cabinet begins work under its rules the next morning, and the first review date is circled in red on every minister's calendar.",
], GAME, "the wartime arrangements are provisional gameplay; where the directorate or unity government still governs, the situation is " + ALT_NOTE, options=(
    ("a", "Govern under the agreed rules.", R(stab(0.02)), 100),
), picture="assembly")

E(39, "ISAF", [
    "On 22 August 2003 FCU President Robert Sinclair establishes ISAF. Erusea has refused the Federation's demand to withdraw from San Salvacion and from Stonehenge, and the governments that share the Federation's view of that refusal will now fight together.",
    "The founding is a ceremony and a negotiation at once. The ceremony is brief: the members' representatives sign the charter, the flags are raised and the President speaks about a continent that will not accept conquest. The negotiation is longer and continues long after the ceremony ends. Every article of the charter has to be turned into practice: who commands, who supplies, who pays and who decides when the war is won.",
    "The members bring different things. Some bring armies, some bring bases, some bring money and some bring only their votes and their territory. The Federation brings the most of everything, and the charter's drafters are careful to make sure that this does not make ISAF merely a federal army with foreign flags.",
    "At the founding, the President's speech is deliberately short. It speaks about San Salvacion, a neutral country that asked for none of this, and about Stonehenge, a battery built by many nations to protect all of them and now turned against the nations that built it. It speaks about the alliance's purpose, which is to restore what has been taken, and about its limits, which are that it will take nothing for itself. The words are written for the members, but the speech is broadcast across the continent, and it is heard in Farbanti too.",
    "The war has already begun badly. Stonehenge is firing, and the first weeks will be hard. But ISAF exists now, and that is the first thing that has gone right since the summer.",
], OFFICIAL, "Chronicle, 2003 / 08.22. ISAF is built from the existing faction (mod provenance). The charter's negotiation is provisional gameplay", options=(
    ("a", "Sign the charter.", R(ws(0.03), pp(10)), 100),
), picture="isaf")

E(40, "Los Canas", [
    "On 14 September 2003 Stonehenge pushes ISAF back to Los Canas, and the alliance's first offensive against the battery fails. Aircraft sent to strike the guns are brought down before they reach them. Ground forces sent to support them cannot advance under the battery's cover. The retreat to Los Canas is orderly, but it is a retreat.",
    "In the war cabinet the news is received without surprise and with considerable anger. Everyone knew that Stonehenge was dangerous; nobody knew it would be this dangerous against aircraft, because it was never built to fight aircraft. The engineers who designed it, many of them federal citizens, are being asked by Erusea to keep it running, and nobody in the war cabinet knows what they are doing or what choice they have.",
    "The question now is what Los Canas is for. It can be held at any cost, buying time for the reserves and showing the partners that the Federation will not abandon the continent. Or it can be a waystation, a line from which the army withdraws in good order to rebuild somewhere the battery cannot reach.",
    "The war cabinet debates it for a night. By morning it has decided only that the decision cannot wait another night.",
], OFFICIAL, "Chronicle, 2003 / 09.14. The war cabinet's debate is provisional gameplay; no territorial result is forced", options=(
    ("a", "Decide the line's purpose.", R(army(5)), 100),
), picture="isaf")

E(41, "North Point", [
    "On 16 September 2004 ISAF establishes its headquarters in North Point. The alliance has been driven from the continent. Its army, air wings and staff are now on the islands, rebuilding.",
    "The exile is not comfortable. North Point's facilities were never built for an alliance headquarters, and everything from fuel storage to barracks must be expanded at once. Aircraft that escaped the continent need maintenance depots that do not exist yet. Ships that carried the army across the water need harbours that are already full. The islanders, who did not ask for any of this, accept it with a patience that the federal officers find humbling.",
    "But the exile has advantages that the continent did not. The islands are beyond Stonehenge's reach. The training grounds are free of debris. The staff, for the first time since the summer of 2003, have time to think rather than react. Plans are written, discarded and rewritten. Crews train until they can fly in their sleep. The partners who stayed with ISAF through the retreat are now its most experienced members.",
    "Every officer at North Point knows that the exile is temporary, or the war is lost. The question in every staff meeting is not whether ISAF will return to the continent, but how.",
], OFFICIAL, "Chronicle, 2004 / 09.16. North Point's role belongs to the NPT package; this event is the Federation's view, and its details are provisional gameplay", options=(
    ("a", "Rebuild at North Point.", R(army(5), air(5)), 100),
), picture="exile")

E(42, "Plans for the Return", [
    "The staff at North Point have been planning the return to the continent since the day they arrived. Now the plans are being finalised, and the war cabinet must approve them.",
    "The planners have learned from the war's first year. They will not attack Stonehenge head-on again until the battery's reach has been measured and its weaknesses understood. They will not land where the enemy expects them. They will not move faster than their supplies can follow. And they will not forget that the continent they are returning to is full of people who have lived under Erusean occupation for a year, and who will judge ISAF by how it behaves when it arrives.",
    "The war cabinet's questions are the ones war cabinets always ask: how many will die, how long will it take and what happens if it fails. The planners answer the first two with estimates and the third with honesty. If the landing fails, there will not be a second one for a long time.",
    "The war cabinet approves the plans. The date is not written down anywhere the enemy might read it.",
], GAME, "the planning is provisional gameplay; the landing itself is Chronicle, 2005 / 01.24", options=(
    ("a", "Approve the plans.", R(army(10)), 100),
), picture="landing")

# ------------------------------------------------------------------ the air wings
E(43, "The Air Wings", [
    "The federal air arm enters the new century with a problem no air force has faced before. The sky is not empty. Fragments of Ulysses still fall, unpredictably, and every flight plan must account for them. Training sorties are cancelled when the debris forecast is bad. Aircraft are lost not to enemies but to rock.",
    "The air wings review is the air arm's attempt to decide what it is for in these conditions. It considers three doctrines. The first holds that air superiority comes first: an air arm that controls the sky can do everything else. The second holds that precision strikes matter most: an air arm that can destroy the right targets at the right time decides wars. The third holds that the future belongs to electronic warfare: an air arm that can blind the enemy's radars can fly wherever it wants.",
    "Each doctrine has its champions among the senior officers, and each has costs. Fighters, strike aircraft and jamming aircraft cannot all be bought in the numbers each doctrine demands. The review must choose, and the choice will shape the air arm for a decade.",
    "Nobody involved in the review knows yet that the decade will include a war. The review is written as if it might.",
], GAME, "the doctrines are provisional gameplay", options=(
    ("a", "Choose a doctrine.", R(air(5)), 100),
), picture="air")

E(44, "The Battery Turned", [
    "Stonehenge was designed to destroy fragments of rock falling from orbit. It turns out to be just as capable of destroying aircraft. Erusea holds the battery now and uses it against ISAF's air wings with a precision its designers never intended.",
    "The air arm's first response is to stop flying where the battery can reach. That is not a strategy, because the battery can reach a very great deal. The second response is to study it: which altitudes, which approaches, which speeds give an aircraft the best chance of surviving a crossing of the battery's arcs. The engineers who built Stonehenge are in Erusean hands, but its design documents are not, and the air arm's analysts read them with an attention their authors would have found flattering under other circumstances.",
    "The training that results is brutal. Crews fly profiles that push their aircraft and themselves to the limits. Some fly low, under the battery's reach and under the radars that guide it. Others fly high and fast, crossing the arcs before the guns can track them. Both approaches lose aircraft in training. Both save more in combat than they cost.",
    "The pilots who complete the course are the best the Federation has ever trained. They know, better than anyone, what their own country built in the desert.",
], OFFICIAL, "Chronicle, 2003 / SUMMER (Stonehenge used against aircraft). The training is provisional gameplay", options=(
    ("a", "Train every crew.", R(air(10)), 100),
), picture="air")

E(45, "The Air Supremacy Campaign", [
    "ISAF is back on the continent. The landing succeeded, and now the war in the air must be won over the beachheads, the roads inland and the cities the ground forces are advancing on.",
    "The air supremacy campaign is the culmination of everything the federal air arm has learned since 1999. Crews trained against debris and against Stonehenge now fly against Erusean fighters, and they fly well. Tankers keep them in the air longer. Early-warning aircraft show them the enemy first. Maintenance depots on the islands and, increasingly, on the continent return damaged aircraft to the line within days. Rescue crews bring back pilots who would have been lost a year ago.",
    "The campaign is not cheap. Every day brings losses, and the air arm's casualty lists are read in the Assembly every week. But the sky over the beachheads belongs to ISAF, and the ground forces below it advance under a protection they did not have in 2003.",
    "The air arm's commanders are careful, in their reports to the war cabinet, not to claim more than they have achieved. The sky is not yet won everywhere. But for the first time since the summer of 2003, it is being won.",
], GAME, "the landing is official (Chronicle, 2005 / 01.24); the air campaign is provisional gameplay", options=(
    ("a", "Press the campaign.", R(air(10), ws(0.02)), 100),
), picture="air")

# ------------------------------------------------------------------ counteroffensive and liberation
E(46, "The Return to Usea", [
    "On 24 January 2005 ISAF lands on the Usean continent. After more than a year at North Point, the alliance is back.",
    "The landing is the largest operation in the Federation's history, and it goes better than the planners dared to hope. The beaches are taken. The beachheads are linked. Supplies come ashore faster than the enemy can interfere with them. By the end of the first week, ISAF holds ground on the continent that it can defend and expand.",
    "For the soldiers coming ashore, many of whom left the continent in the retreat of 2003 and 2004, the return is personal. Some land near towns they know. Some meet civilians who remember them. The war cabinet's instructions, read to every unit before it embarked, are clear about how they are to behave: the people of the continent are not the enemy, their property is not plunder and their towns are not prizes.",
    "Behind the beaches, the first towns ISAF reaches have lived under occupation for more than a year. Their people come out cautiously, then all at once. Some have food to share and some need food. Some have information about the enemy's positions and some only want to know whether their relatives in the Federation are alive. The civil affairs officers who came ashore with the first wave are overwhelmed within hours, and the war cabinet's careful instructions are tested by thousands of small decisions made by tired soldiers far from any headquarters.",
    "In the war cabinet, the mood is cautious relief. The landing has succeeded. The war is not won. Stonehenge still stands, Erusea's army is still in the field and the road to Farbanti is long. But for the first time, the Federation's maps show ISAF's lines moving in the right direction.",
], OFFICIAL, "Chronicle, 2005 / 01.24. The landing's conduct is provisional gameplay; no territorial result is forced", options=(
    ("a", "Advance inland.", R(army(10), ws(0.02)), 100),
), picture="landing")

E(47, "Liberation, Not Annexation", [
    "The war cabinet's directive is one sentence long, and every ISAF officer is required to read it: every place ISAF frees goes back to the government it belongs to. The Federation will take no territory in this war and redraw no border.",
    "The directive is not only principle. It is strategy. ISAF's members joined to defend the continent, not to enlarge the Federation, and some of them watch Central Usea's power with as much caution as they watch Erusea's. A Federation that annexed liberated ground would lose its partners before it won the war. A Federation that returned every town to its rightful government would be trusted, and trust is a weapon the enemy cannot match.",
    "In practice the directive raises a hundred questions. Who governs a liberated town before its own government can return? Who restores the water and the power? Who decides when refugees may go home? The war cabinet's answer is that ISAF will do what must be done to keep people alive and nothing more, and that every decision will be handed to the rightful authorities as soon as they can take it.",
    "The directive is printed on cards and issued to every soldier. Most of them keep the card.",
], GAME, "provisional gameplay; no territory, core or border changes hands in this package", options=(
    ("a", "Issue the directive.", R(stab(0.02)), 100),
), picture="liberation")

E(48, "The Engineers' Escape", [
    "On 14 March 2005 the engineers who built Stonehenge, and their families, escape from Erusean custody. They have been held at the site since the summer of 2003, kept working on the battery that their own country now wants destroyed.",
    "The escape is the end of a long ordeal and the beginning of a delicate one. The engineers must be received, sheltered and cared for: some are ill, all are exhausted and the children have spent nearly two years in a war zone. They must also be heard, because they know the battery better than anyone alive, and ISAF needs that knowledge.",
    "The Federation's handling of the engineers is watched closely. They are federal citizens and the citizens of other consortium nations. They were held against their will, and some of them were forced to do work they found abhorrent. The war cabinet insists that they are to be treated as rescued civilians, not as defectors or prisoners, and that nobody is to suggest otherwise in public.",
    "The engineers, once rested, offer their help freely. Several of them say the same thing to the officers who interview them: we built it to save the world, and we would like to see it stopped.",
], OFFICIAL, "Chronicle, 2005 / 03.14. The reception and interviews are provisional gameplay", options=(
    ("a", "Receive them as rescued civilians.", R(stab(0.02)), 100),
), picture="stonehenge")

E(49, "Stonehenge Silenced", [
    "On 2 April 2005 ISAF destroys Stonehenge. The battery built to defend the world from Ulysses, seized by Erusea and turned against the aircraft of the nations that built it, will not fire again.",
    "The news is received in the Federation with a feeling nobody quite knows how to name. It is victory: the greatest obstacle to ISAF's advance is gone, and the war's outcome is no longer in doubt in the way it was. It is also loss. Stonehenge was the Federation's proudest achievement of the 1990s, an international project led from Central Usea that stood between the world and the sky. Children who drew it in 1998 are teenagers now, and some of them are serving in the forces that destroyed it.",
    "The Super Weapons record notes that seven of the eight batteries were destroyed. What happens to the site now is a question for the end of the war and for San Salvacion, on whose ground it stands. The war cabinet's view is clear: the ruins belong to San Salvacion, not to the Federation.",
    "In the engineers' camp, the news is received in silence. Then one of them asks whether, when the war is over, anyone will remember what the battery was built for.",
], OFFICIAL, "Chronicle, 2005 / 04.02; Super Weapons, Stonehenge (seven of eight batteries destroyed). The reaction is provisional gameplay", options=(
    ("a", "Remember what it was built for.", R(stab(0.02), ws(0.02)), 100),
), picture="stonehenge")

E(50, "San Salvacion Liberated", [
    "On 10 July 2005 San Salvacion is liberated. After two years of occupation, the neutral country that hosted Stonehenge is free.",
    "The war cabinet's directive is tested here more than anywhere. San Salvacion is where the war began, where the battery stood and where the Federation's interest is most obvious. Some voices, in the press and even in the Assembly, suggest that the Federation should keep a presence: to guard the battery site, to protect against another invasion, to make sure the investment of the 1990s is not lost. The war cabinet's answer is the same as it has been since the landing: San Salvacion belongs to San Salvacion.",
    "Its government returns to its capital. ISAF units that took part in the liberation parade through the streets with their own colours and the republic's, and then withdraw to positions agreed with the returning authorities. The relief that follows is organised through those authorities, not around them.",
    "For the people of San Salvacion, the liberation is the end of the worst two years in their history. For the Federation, it is something else as well: proof, watched across the continent, that the war was fought for the reasons the Federation said it was.",
], OFFICIAL, "Chronicle, 2005 / 07.10. San Salvacion's ownership is unchanged; the parade and relief are provisional gameplay", options=(
    ("a", "Return the republic to its government.", R(stab(0.03)), 100),
), picture="liberation")

# ------------------------------------------------------------------ postwar
E(51, "Victory in Usea", [
    "On 19 September 2005 Farbanti falls and Erusea surrenders. The Usean Continental War is over.",
    "The news spreads across the Federation in hours. There are celebrations in every city, quiet ones in the towns that lost the most and loud ones everywhere else. Church bells ring. Factories stop work for an hour. In the reception towns, families who were displaced by the impact in 1999 and again by the war in 2003 listen to the radio and wonder whether, this time, they will finally go home.",
    "In the war cabinet the mood is subdued. The war has been won; the peace has not. Erusea must be governed by someone, and the terms of surrender say only that it will be overseen by ISAF while it forms a government of its own. The continent must be rebuilt, and the impact's debris is still falling. The alliance that won the war must decide whether it will hold together in peace.",
    "Abroad, the surrender is received with relief and with questions. ISAF's members want to know how long the oversight will last and who will pay for it. Governments beyond Usea want to know whether the Federation, now plainly the continent's leading power, intends to use that power as it promised. The Federation's diplomats answer every question the same way: the war was fought to restore what was taken, and nothing more will be taken now that it is won.",
    "The cabinet's first act after the surrender is to repeat the war's founding principle: the Federation will take no territory and impose no government. Its second is to send the relief convoys that have been waiting at the frontier since the summer.",
], OFFICIAL, "Chronicle, 2005 / 09.19. The celebrations and the cabinet's response are provisional gameplay", options=(
    ("a", "Win the peace.", R(stab(0.03)), 100),
), picture="postwar")

E(52, "After Megalith", [
    "On 26 September 2005 young Erusean officers seize Megalith, a fortress built to bring down orbiting fragments of Ulysses. ISAF destroys it. Erusea forms a provisional autonomous government under ISAF oversight.",
    "The seizure is the war's last spasm, and for a few days it is frightening. Megalith was built, like Stonehenge, to answer the sky, and nobody outside it knows what its new holders intend. Its destruction ends the danger and closes the war's last open question.",
    "What remains is the work of peace. Erusea's provisional government must be formed by Eruseans, overseen by ISAF and recognised by the continent. The Federation's role in that oversight will define its relationship with Erusea for a generation. It can be heavy or light, intrusive or respectful, but it cannot be absent.",
    "The oversight council's first meeting is held within a week, and its agenda is practical rather than political: food, power, water and the return of prisoners. The Eruseans who attend are officials, not victors or vanquished, and the council's federal members are instructed to treat them that way.",
    "The cabinet's instructions to its representatives in the oversight council are brief. Oversee, do not govern. Advise, do not command. Remember that the Eruseans who will form this government are the people the Federation will live beside for the rest of the century.",
], OFFICIAL, "Chronicle, 2005 / 09.26; Super Weapons, Megalith. Erusea's provisional government is never a forced government swap; the instructions are provisional gameplay", options=(
    ("a", "Oversee, do not govern.", R(stab(0.02)), 100),
), picture="postwar")

E(53, "The Federation Endures", [
    "In this provisional outcome the war has been lost. Erusea holds what it took, and ISAF has not been able to take it back. The Federation must now live with a defeat that the Chronicle does not record and that its people did not believe possible.",
    "The government's first task is to make sure that the Federation itself survives. Its armies have come home, diminished. Its partners are shaken, and some are looking for terms of their own. Its people, who carried the impact and the war together, are exhausted and angry, and they want to know who is responsible.",
    "There are two paths forward, and the cabinet debates them for weeks. The Federation can rebuild its army and wait for the moment when the war can be reopened. Or it can accept the peace, however bitter, and spend the next decade on the recovery that the impact demanded and the war postponed.",
    "Either way, the Federation endures. Its institutions survived the impact and the war, its government still governs and its people are still its people. That, the cabinet reminds itself, is not nothing.",
], GAME, "Erusean victory is a provisional alternative to the official ISAF victory (Chronicle, 2005 / 09.19). No borders change in this package", options=(
    ("a", "Hold the Federation together.", R(stab(0.03)), 100),
), picture="postwar")

E(54, "The Armistice Line", [
    "In this provisional outcome the war ends in an armistice. Neither side has won; neither has lost. A line on the map divides the continent, and on either side of it armies watch each other across ground that neither can take.",
    "The armistice is not peace. It is a promise to stop fighting, renewable and revocable, with no settlement of the questions that started the war. San Salvacion's status, the battery site, the refugees and the grievances of both sides remain exactly where they were, frozen in place by an agreement that both governments signed because they could not afford to keep fighting.",
    "For the Federation, the armistice is a relief and a disappointment at once. Its soldiers are coming home. Its war is over, for now. But the war's purpose has not been achieved, and the line on the map is a daily reminder of that.",
    "The cabinet must decide how to live beside the line. It can keep its army at the line and its air arm on alert, ready for the day the armistice fails. Or it can propose a demilitarised zone, watched by neutral observers, and bet that a peace nobody signed can still become one.",
], GAME, "the armistice is a provisional alternative to the official ISAF victory (Chronicle, 2005 / 09.19). No borders change in this package", options=(
    ("a", "Decide how to live beside the line.", R(stab(0.02)), 100),
), picture="postwar")

E(55, "The War That Was Not", [
    "In this provisional outcome the continental accord has averted the war. Erusea did not invade San Salvacion. Stonehenge was not seized. The summer of 2003 passed like any other summer, and the Chronicle's war happened only in the planning documents of the staffs that had prepared for it.",
    "The Federation's leaders know how close it came. The refugee crisis, the closed borders, the battery in a neutral country and the tensions of a continent still recovering from the impact were all real. That the war did not come is a credit to the diplomats who negotiated the accord and to the governments that signed it, and it is also luck.",
    "The task now is to make the accord last. Peace that is merely the absence of war can collapse at the first crisis. The Federation's choice is how to build something firmer: by guaranteeing the accord with forces kept ready but at home, or by binding the continent together through trade, shared reconstruction and common prosperity.",
    "The cabinet's view is that both are needed, and that the order matters. It begins the debate on which to choose first.",
], GAME, "the averted war is a provisional alternative to the official Continental War (Chronicle, 2003 / SUMMER onward)", options=(
    ("a", "Build a peace that lasts.", R(stab(0.03)), 100),
), picture="treaty")

E(56, "The Usean Order", [
    "The war is over, one way or another, and Usea must decide what kind of continent it will be. The Federation, as its largest power, will have more say in that decision than anyone else. It must decide how to use that say.",
    "The questions are many. What happens to ISAF, the alliance that fought the war, in peacetime? Does it become a standing organisation, with headquarters and staff and plans for the next crisis? Or does it dissolve, its officers returning to their own services, its lessons kept in archives rather than institutions? What happens to the veterans, many of them wounded, who fought it? What happens to the refugees who are still in camps, and the debris that is still falling?",
    "The Federation's partners watch its answers closely. Some want a strong, permanent alliance led by the Federation. Some want the Federation's power limited, now that the threat that justified it has passed. All of them want to be consulted.",
    "The cabinet's working paper on the Usean order is titled, simply, After. Its first sentence is: the continent we build now will outlast every government in this room.",
], GAME, "the postwar order is provisional gameplay; no events after 2005 are asserted", options=(
    ("a", "Consult the partners.", R(stab(0.01), pp(10)), 100),
), picture="postwar")

E(57, "The Order of 2005", [
    "The Federation records the settlement it has helped to build. The document is not a treaty: the treaties have been signed elsewhere, by the governments concerned. It is the Federation's own account of what it did and why, written for the Assembly, the archives and the citizens who paid for it.",
    "It begins with the impact of 1999 and the decade of preparation that came before it. It records the war of 2003 to 2005 in whatever form the Federation lived it: victory, defeat, armistice or the war that never came. It lists the choices the Federation made: the government it chose, the alliance it led, the principles it kept and the ones it bent. It does not claim that every choice was right.",
    "It ends with a paragraph that the cabinet argued over for a month. The Federation's purpose in the decade past was to protect its people and its partners from a sky that fell and a war that followed. Whatever comes next, it says, the Federation will face it with the institutions it built, the partners it kept and the trust it earned.",
    "The authored chronology of this campaign ends here. Nothing after 2005 is asserted.",
], GAME, "the closing record is provisional gameplay; the campaign's authored chronology ends in 2005", options=(
    ("a", "Record the settlement.", R(stab(0.02), pp(20)), 100),
), picture="postwar")

E(58, "The Federal Question Answered", [
    "The question the cabinet asked in 1991, how the Federation should govern itself in an emergency, has now been answered by events. The Federation has lived through a rebellion, an announcement, a coup, an impact and a war. Whatever government it chose, it has seen that government tested in every way a government can be.",
    "Now that government must give an account. Not to history, which will take its time, but to the Assembly and to the voters, who will not. The account must say what the government did, what it promised and what it delivered. It must say what it would do differently. And it must say what it intends to do now that the emergencies are, for the moment, over.",
    "If the presidency and the Assembly held their course, the account is a defence of ordinary government under extraordinary pressure. If a directorate governed, it is an explanation of why emergency rule was needed and whether it has ended. If a unity government governed, it is the open review its own mandate demanded.",
    "The Assembly receives the account in silence and debates it for a week. Then it votes, and the Federation's government is either renewed or replaced by the means the constitution provides.",
], GAME, "the account is provisional gameplay; the directorate and unity paths are " + ALT_NOTE, options=(
    ("a", "Give the account.", R(stab(0.02)), 100),
), picture="assembly")

E(59, "Civilian Rule Restored", [
    "The directorate ends its tenure before the war can test it. Its last order returns executive authority to the presidency and the Assembly, and its staff go back to Unified Command within the month.",
    "The timing is deliberate. The directorate was built for an emergency, and the emergency it was built for, Ulysses and its aftermath, has passed its worst. A war, if one comes, will need a government whose legitimacy is not in question, and a directorate formed under an emergency statute has a legitimacy that its critics question every day. Better, the directorate's own officers argue, to hand back authority now, in calm, than to have it taken from them later, in crisis.",
    "The handover is orderly. The presidency resumes its executive duties. The Assembly resumes its legislative ones. The regional governments recover the powers they ceded. The newspapers, which were never closed, go on printing what they printed before, and the opposition, for the first time in years, has no directorate to oppose.",
    "Abroad, the treaty partners welcome the restoration with visible relief. They had accepted the directorate as an emergency measure, but as the emergency faded their governments had grown uneasy at allying themselves with a federation governed by its army. Now the Federation they deal with is the one they signed the treaty with. If war comes, its partners will face it beside a government whose legitimacy nobody in their own capitals questions.",
    "The officers go back to their headquarters. If war comes, they will fight it under civilian orders, as the constitution intended.",
], GAME, ALT_NOTE + "; the restored presidency is the mod's 1991 government", options=(
    ("a", "Civilian rule resumes.", R(stab(0.03)), 0),
), picture="assembly")

E(60, "A Vote for the Charter", [
    "The unity government puts the ISAF charter to a vote in the Assembly. It does not have to: the cabinet could have signed it on its own authority. But a government of all the parties, the cabinet argues, should not take the Federation to war without all the parties voting for it.",
    "The debate is the most serious the Assembly has held since the unity government was formed. Every party speaks. Some speakers support the charter without reservation. Others support it with conditions: that ISAF will not annex territory, that it will return every liberated town to its rightful government and that the Assembly will review the war every six months. A few oppose it, arguing that the Federation should seek terms rather than fight.",
    "The vote, when it comes, is overwhelming. Every party in the unity government votes for the charter, and most of the opposition does too. The few who vote against are heard with respect and not punished for their votes.",
    "The cabinet signs the charter the next morning. The commentators note that ISAF, whatever its founding ceremony says, now has the support of a Federation that voted for it.",
], GAME, "ISAF's founding is official (Chronicle, 2003 / 08.22); the unity government's vote is " + ALT_NOTE, options=(
    ("a", "Sign the charter.", R(ws(0.03), stab(0.02)), 0),
), picture="isaf")
