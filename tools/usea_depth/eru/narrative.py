"""Long-form events for the Erusea package (namespace ac_ud_eru).

Each event has at least three paragraphs and 180 words, ends with a source-layer
line built by seams.event_text() and uses straight quotes only. Chronicle people
appear in text only, exactly as the Chronicle names them. Options never reach a
government change; options that lower Erusean grievance carry an AI weight of 0.
"""

EVENTS = {}


def E(number, title, picture, layer, citation, paragraphs, options):
    if number in EVENTS:
        raise ValueError("Duplicate event %d" % number)
    EVENTS[number] = dict(title=title, picture=picture, layer=layer, citation=citation,
                          paragraphs=[" ".join(p.split()) for p in paragraphs], options=options)


MOD_HISTORY = ("the 1991 Erusean monarchy, its ruling house and its party names come from the inherited history file "
               "(history/countries/ERU - Erusea.txt); the court's reforms are provisional gameplay")
NO_SOURCE = "no official source describes Erusean politics before 2003; this is a provisional gameplay branch"

# ------------------------------------------------------------------ the court and the political paths
E(1, "The Court of Erusea", "court", "Mod provenance", MOD_HISTORY, [
    """The register of offices arrives at the palace in four leather volumes, each thicker than the last. The first
    lists the royal household: chamberlains, equerries, the keepers of the seals and the archive. The second lists the
    chancery secretariats, seven of them, each with its own clerks and its own way of numbering a decree. The third
    lists the ministries and the men who actually run them. The fourth, the thinnest, lists the general staff's
    liaison officers in every one of those offices, and nobody in the palace remembers authorizing it.""",
    """The opening reviews of the decade were about districts, railways and reserve exercises. They were the easy
    part. The court is harder, because the court is where Erusea decides who decides. A royal audience can settle a
    question in an afternoon. What happens to the answer between the audience and the district office is a matter of
    secretaries, rivalries and the general staff's patience.""",
    """Outside the palace, the country is changing faster than its institutions. The towns have newspapers that do
    not wait for the court gazette. The universities have clubs that call themselves liberal, and some that call
    themselves worse. The officer corps reads the same newspapers and draws its own conclusions about the age of the
    men at the top.""",
    """The monarch reads the ledger through twice and asks for a clean copy, with one change: the fourth volume is to
    be bound into the first, so that the general staff's offices are listed among the Crown's, where they belong.""",
], [("Begin with the chancery.", "add_political_power = 20", 60),
    ("Begin with the council.", "add_stability = 0.01", 40)])

E(2, "The Crown's Question", "court", "Provisional gameplay", NO_SOURCE, [
    """The privy councillors are called to the long room before dawn, which has not happened since the last
    succession. On the table are the court ledger, the succession statute and three documents that have been
    circulating in Farbanti for a month without anyone admitting to having read them.""",
    """The first is a note from the palace secretaries. It says that Erusea has always been governed by the Crown's
    prerogative and should continue to be, through a modern cabinet of royal secretaries, provincial intendants and
    an officer corps sworn to the throne. It is careful, confident and slightly bored, as if the question it answers
    were not really a question.""",
    """The second is a draft charter, written by a circle of jurists and liberal deputies from the old advisory
    chambers. It proposes an elected assembly, a cabinet responsible to it and a monarchy that reigns without ruling.
    It is earnest, long and full of footnotes. Its authors have signed it, which is either courage or a
    miscalculation.""",
    """The third is a memorandum from the general staff. It is short. It says the ministries are failing, that
    Erusea faces a decade of danger and that only a regency council of serving officers, governing in the Crown's
    name, can carry the country through. It is unsigned. Everybody knows whose typewriter it came from.""",
    """The monarch listens to all three readings, asks no questions and adjourns the council until the evening. The
    question has been asked. What remains is to choose which of the three answers the Crown can live with, and which
    of the three factions it can afford to disappoint.""",
], [("The Crown has asked. The Crown will answer.", "add_political_power = 15", 80),
    ("Let every faction make its case in public.", "add_stability = -0.01\nadd_popularity = { ideology = democratic popularity = 0.02 }", 20)])

E(3, "Rule by Prerogative", "court", "Provisional gameplay", NO_SOURCE, [
    """The palace answers its own question in the language it knows best. A royal message is read in every district
    town: Erusea will be governed as it has always been governed, by the Crown, through ministers who serve at the
    Crown's pleasure. There will be reform, the message says, but it will be the reform of a household putting its
    rooms in order, not the reform of tenants rewriting the lease.""",
    """The secretaries receive their new commissions within the week. The cabinet is to become a cabinet of royal
    secretaries, each answerable to the chancery. The districts will receive intendants with real authority. The
    officers will be asked to renew an oath that most of them have never taken. The court gazette is to be printed
    daily.""",
    """The reaction is quieter than the reformers hoped and louder than the palace expected. The liberal clubs hold
    meetings that end early because nobody knows what to propose next. The general staff sends a letter of
    congratulation so warm that the chancery reads it three times looking for the threat. In the provinces, where the
    Crown has always been more popular than the capital, the message is read in the churches and the market halls
    and applauded.""",
    """The palace has chosen continuity. It now has to prove that continuity can govern a country facing the decade
    that is coming.""",
], [("The Crown governs.", "add_stability = 0.02", 70),
    ("Reassure the reformers that the door is not locked.", "add_political_power = -10\nadd_popularity = { ideology = democratic popularity = 0.01 }", 30)])

E(4, "Toward a Constitution", "assembly", "Provisional gameplay", NO_SOURCE, [
    """The monarch's answer is printed on the front page of every newspaper in Erusea, including the ones the palace
    has never liked. The Crown will give the country a constitution. A drafting commission will be convened. There
    will be an elected assembly and a cabinet responsible to it, and the monarchy will stand above the parties as the
    guardian of the charter rather than its author.""",
    """In the university towns the clubs spill into the streets. In the capital the old advisory chambers, which have
    met for decades to give advice nobody took, find themselves besieged by petitioners asking how to stand for
    election. The liberal party's organizers, who expected to spend another ten years in back rooms, discover that
    they need offices, printers and candidates by spring.""",
    """The palace secretaries are courteous and unhelpful. Several resign. The general staff issues no statement at
    all, which is noticed. In the officers' clubs the reaction is mixed: the younger officers, many of them educated
    abroad, are curious; the senior ones remind each other that assemblies cannot fight wars and that this one has
    not yet been asked to.""",
    """Nobody knows what an Erusean constitution will look like. The monarch has made one thing clear. It will be
    written while the Crown still has the authority to see it written, and not later, by somebody else, in a worse
    year.""",
], [("Convene the commission.", "add_popularity = { ideology = democratic popularity = 0.04 }", 70),
    ("Ask the general staff for its assurance.", "add_political_power = -15\nadd_stability = 0.02", 30)])

E(5, "The General Staff Steps In", "command", "Provisional gameplay", NO_SOURCE, [
    """The memorandum was never formally answered. It did not need to be. Over a long weekend, staff officers took up
    liaison posts in every ministry in Farbanti, with copies of every file and keys to every room. On Monday morning
    the civil servants found colonels at the end of their corridors, polite, punctual and impossible to ignore.""",
    """The palace was informed rather than consulted. The chief of staff came to the long room with a short
    proposal: a regency council of serving officers would govern in the Crown's name until the country was secure,
    reorganizing the ministries as a command administration. The Crown would remain. The court would remain. The
    decisions would be made elsewhere.""",
    """There were no shots. The liberal clubs called meetings and found the halls closed for inspection. The palace
    guard was told to stand down and did, after an hour that nobody who was there talks about. The newspapers printed
    the announcement exactly as it was delivered to them, and the next morning printed the weather.""",
    """In the provinces the reaction is not anger so much as weary recognition: the army has always been the country's
    most organized institution, and now it has decided to be its government. Whether the officers can govern as well
    as they plan is a question the next decade will answer, one way or the other.""",
], [("Order has been restored.", "add_war_support = 0.03", 70),
    ("Order has been imposed.", "add_stability = -0.02\nadd_political_power = 25", 30)])

E(6, "The Royal Progress", "court", "Provisional gameplay", "an invented royal tour illustrating the court reforms; no official source", [
    """The royal train leaves the capital at dawn with eleven carriages, two of them for the newspapers. The route was
    argued over for a month: the chancery wanted the prosperous river towns, the general staff wanted the frontier
    garrisons and the household wanted anywhere with a good hotel. In the end the monarch chose the route personally,
    by drawing a line on a railway map.""",
    """In the river towns there are bands and children with flags. In the mining valleys there are fewer flags and
    more questions, shouted from the back of the crowd and printed the next day by the papers that were not invited.
    In the frontier towns the garrison commanders turn out their regiments and the mayors turn out their complaints:
    the roads, the hospital, the price of fuel.""",
    """The monarch listens. Whether listening changes anything is a question for the chancery, which receives a
    notebook full of promises at the end of the month and is asked to keep them.""",
    """The progress has done what it was meant to do. The Crown has been seen. The provinces have been heard, at least
    for an afternoon. The court has learned that the country is larger and angrier than the long room suggests, and
    that a photograph of the monarch in a mining valley is worth more than a decree.""",
], [("Print the photographs.", "add_war_support = 0.01", 60),
    ("Print the complaints.", "add_stability = 0.01\nadd_political_power = -10", 40)])

E(7, "The Rail Question", "industry", "Provisional gameplay", "Erusean economic policy in the 1990s has no official source", [
    """The rail ministry's ledger is the most honest document the government has produced in a decade. Every line is
    listed with its age, its traffic and its condition. Every bridge has an inspection date, many of them alarming.
    Every locomotive has a mileage, and some of the mileages are older than the engineers who drive them.""",
    """The ledger ends with a question nobody in the ministry was willing to answer. Erusea's railways need more
    investment than the treasury can provide on its own. Either the state finds the money and keeps the railways, as
    one national trust with a timetable for the army, or it leases the main lines to private operators who will
    invest in exchange for thirty years of fares.""",
    """The arguments are predictable and still bitter. The general staff wants the trust: a railway that answers to
    the government will move divisions when asked. The shipping and manufacturing firms want the concessions:
    private operators will build terminals beside their factories. The unions want whichever option keeps the
    workshops open. The treasury wants whichever option costs less this year.""",
    """The decision will shape where Erusea's factories are built and how fast its army can move for a generation.
    The rail minister asks for it in writing.""",
], [("Put the question to the cabinet.", "add_political_power = 15", 60),
    ("Commission an independent survey first.", "add_political_power = -10\nadd_stability = 0.01", 40)])

E(8, "Steel or Shoes", "industry", "Provisional gameplay", "Erusean economic policy in the 1990s has no official source", [
    """The machine-tool bureau's first annual report is two hundred pages long and ends with a chart that the
    minister of industry has pinned to the wall of the cabinet room. It shows where Erusea's factories get their
    machines, their spare parts and their engineers. Almost every arrow points abroad.""",
    """The bureau can change that, slowly, but only if it knows what Erusea wants to make. Heavy industry would put
    the bureau's money into steel mills, armour plate and engine works, with guaranteed prices for the mills and
    priority for coal and power. Light industry would put it into the textile mills, furniture shops and radio
    assemblers that employ half the district towns, and wait for demand to call the mills back to life.""",
    """The general staff, as usual, has an opinion. So do the unions, the banks and the district mayors, whose
    opinions depend entirely on what their own towns make. The treasury points out that either choice will cost
    more than it has.""",
    """The minister of industry tells the cabinet that a country can make steel or shoes first, but not both at once,
    and asks which.""",
], [("A country is built on steel.", "add_war_support = 0.01", 70),
    ("A country is built on its households.", "add_stability = 0.01", 30)])

E(9, "The Defence Review", "command", "Provisional gameplay", "Erusean defence planning in the 1990s has no official source", [
    """The reserve exercises ended with a report that the general staff did not enjoy writing. The reservists turned
    up; their rifles did not. The trains ran; the trucks at the other end were missing. The coastal watch saw
    everything and could tell nobody, because its radios were tuned to the wrong frequencies.""",
    """The defence review is the government's answer. For three months the army, the air arm and the navy present
    their cases to a board of senior officers and treasury officials. The army wants divisions and the reservists to
    fill them. The air arm wants a charter of its own, separate from the army, and pilots trained to modern
    standards. The navy wants a fleet, a real one, with hulls large enough to matter in Usean waters.""",
    """Each service believes that the others are asking for too much. Each service is right. The treasury's
    representatives sit through every session and say almost nothing, which the officers find more alarming than any
    speech.""",
    """The review's conclusions will shape Erusea's armed forces for the decade. They will also decide which of the
    three services the government trusts most, a question that in Erusea has never been purely military.""",
], [("All three services will be rebuilt, in order.", "army_experience = 5", 60),
    ("The treasury sets the limits.", "add_political_power = 15", 40)])

E(10, "The Aegir Fleet Plan", "fleet", "Provisional gameplay",
  "the official chronology names the Aegir fleet only at its loss in 2004 (ACES Chronicle, 2004 / 11.23); its 1990s plan and timing are a gameplay abstraction", [
    """The navy's plan arrives in a locked case with a name already printed on the cover: the Aegir fleet. It is the
    most ambitious naval programme Erusea has ever drafted. A modern fleet, built in Erusean yards, crewed by
    Erusean sailors trained in Erusean schools, able to defend the coast and to be taken seriously by anyone who
    sails near it.""",
    """The plan is honest about the cost. The national yards need new slipways and covered halls. The naval school
    needs to double its intake. The fleet needs a home anchorage with defences against aircraft and submarines. And
    the treasury needs to commit money for a decade, because a fleet is the one weapon that cannot be bought in a
    hurry.""",
    """The army's representatives on the defence board point out that every hull is a division that will not be
    raised. The air arm's point out that every hull is a target. The navy's answer is that an island continent's
    neighbour without a fleet is a neighbour who negotiates on other people's terms.""",
    """The plan is approved in principle and funded for its first years. The name stays on the cover. Whatever the
    Aegir fleet becomes, it begins here, as a line in a budget and a promise to the shipyards.""",
], [("Lay the foundations in the yards.", "navy_experience = 10", 70),
    ("Train the officers before building the hulls.", "add_political_power = 10", 30)])

E(11, "The Air Arm Charter", "air", "Provisional gameplay", "Erusean air force history in the 1990s has no official source", [
    """For twenty years Erusea's military aviators have served as a branch of the army, flying the missions the army
    asked for, with aircraft the army bought, under officers who had never flown. For twenty years they have asked
    for a charter of their own. The defence review finally gives it to them.""",
    """The charter creates an air arm with its own staff, its own budget, its own schools and its own uniform. The
    uniform matters more than anyone outside the service understands. The pilots' mess in the capital stays open
    until dawn on the night the charter is signed, and the bill is sent, by tradition, to the army.""",
    """The charter does not tell the air arm what it is for. The interceptor faction wants it to own Erusean skies:
    fast aircraft, ground radar and pilots trained to fight outnumbered. The strike faction wants it to serve the
    army in the field. Both factions agree that they need a pilot academy before anything else, and that the
    academy must be the best on the continent.""",
    """The air arm is young, proud and impatient. It will need all three qualities, and the government will need to
    decide how much of each it can afford.""",
], [("Build the academy first.", "air_experience = 10", 70),
    ("Buy aircraft first.", "add_political_power = -10\nair_experience = 15", 30)])

E(12, "The Continental Desk", "diplomacy", "Provisional gameplay", "Erusean foreign policy before 2003 has no official source", [
    """The continental desk began as three diplomats in a corridor of the foreign ministry, collecting newspapers
    from the neighbouring capitals. It has become a directorate, with an ambassador's office for every Usean country
    and a budget to match. The question it now has to answer is the one the corridor never did: what does Erusea want
    from its neighbours?""",
    """The answers on offer are older than the directorate. One school says that the Federation of Central Usea is the
    continent's largest power and that Erusea's interest is to be its confidant, never its rival. Another says that
    Erusea is large enough to keep its own counsel, to trade with everyone and to sign nothing that binds its hands.
    A third school, smaller and louder, says that Erusea's neighbours have never done it a favour and never will.""",
    """The directorate's first task is less grand. It opens embassies where Erusea has only consulates, sends trade
    missions to the continental fairs and learns, capital by capital, who answers the telephone.""",
    """The directorate's first report observes that diplomacy is mostly the art of remembering who helped you. It
    ends with a request for a larger filing cabinet.""",
], [("Open the embassies.", "add_political_power = 10", 60),
    ("Send the trade missions first.", "add_stability = 0.01", 40)])

E(13, "The Stonehenge Question", "battery", "Official",
  "ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge. Erusea's position is provisional gameplay", [
    """The official chronology records that Central Usea completed Stonehenge on 19 June 1998, in a desert region of
    neutral San Salvacion. It is a battery of eight railguns, built under the Federation's leadership as an
    international project, to destroy the fragments of Ulysses before they reach the ground.""",
    """In the foreign ministry the question is not whether the battery is useful. Everyone agrees it is. The question
    is what Erusea says about the most powerful gun ever built on the continent, built on neutral soil, under the
    leadership of the continent's largest power, with Erusea's name nowhere on the list of decision-makers.""",
    """The directorate drafts three statements. The first welcomes the battery and asks for a seat on whatever body
    oversees it. The second welcomes it and asks for nothing, which the general staff calls weakness. The third
    welcomes it in one sentence and spends four paragraphs on the principle that the defence of a continent should
    be decided by the continent. The minister reads all three aloud to the cabinet, and the room goes quiet at the
    fourth paragraph of the third.""",
    """Whatever Erusea says will be remembered, by its neighbours and by its own people. The fragments are coming
    either way.""",
], [("Welcome the battery and ask for a seat.", "add_political_power = -10\nadd_stability = 0.02", 30),
    ("Welcome the battery in one sentence.", "add_war_support = 0.02\nset_country_flag = ERU_ud_stonehenge_protested", 70)])

# ------------------------------------------------------------------ official era transitions
E(14, "Rebels in the Skully Islands", "security", "Official",
  "ACES Chronicle, 1995 / 12.31. The Erusean reaction is provisional gameplay", [
    """The official chronology records that on 31 December 1995 Robert Tyler of the Federation of Central Usea's Army
    Southern District eliminated a rebel base in the Skully Islands, and that Unified Command defeated those rebels
    with Scarface Squadron. The news reaches Farbanti on a New Year's Eve when most of the government is at the
    opera.""",
    """The facts are thin, and the Erusean intelligence service has few of its own. Somewhere in the south of the
    continent armed men were organized enough to hold a base, and the Federation was organized enough to destroy
    it. What the rebels wanted, who supplied them and whether they had friends elsewhere are questions the reports
    do not answer, and the cabinet is warned not to guess.""",
    """The general staff's interest is professional. It notes the speed of the Federation's response and the
    unusual prominence of a single air squadron in the reports. The foreign ministry's interest is diplomatic: it
    drafts a message of congratulation to the Federation and debates for a day whether to send it.""",
    """In the officers' clubs, the conversation turns to a less comfortable question. If armed men can organize in
    the Skully Islands, what are they organizing elsewhere? Nobody has an answer. The new year begins with the
    question still on the table.""",
], [("Send the congratulations.", "add_political_power = 10", 50),
    ("Ask the intelligence service for more.", "add_stability = 0.01", 50)])

E(15, "Ulysses", "sky", "Official",
  "ACES Chronicle, 1996 / 04.20. Erusea's response is provisional gameplay", [
    """The official chronology records that on 20 April 1996 the Federation of Central Usea announced that the
    asteroid Ulysses will strike the Earth. The announcement is read on every radio in Erusea before the cabinet
    has seen it. In the capital people stop in the street to listen; in the district towns they gather at the
    windows of the shops that sell televisions.""",
    """By evening the astronomers have explained what the announcement means, which is worse and stranger than the
    first reports suggested. Ulysses will not arrive as one body. It will break apart as it nears the Earth, and its
    fragments will fall over years, not days, in places nobody can yet predict. There is time to prepare. There is no
    way to know what preparation will be enough.""",
    """The cabinet meets until dawn. The interior ministry wants shelters. The treasury wants to know who pays for
    them. The general staff wants authority over the districts in an emergency, and says so with a frankness that
    makes the civilians uneasy. The foreign ministry reports that every government on the continent is holding the
    same meeting, and that the Federation is talking about a response that would require a battery of guns larger
    than anything ever built.""",
    """Erusea's decade has a new shape. Whatever was planned for the railways, the fleet and the court must now be
    planned again, with the sky in mind.""",
    """In the morning the newspapers print a photograph of the night sky over Farbanti. Ulysses is not visible in it.
    Everybody looks for it anyway.""",
], [("Prepare the country.", "add_stability = 0.02\nadd_political_power = -15", 60),
    ("Prepare the government first.", "add_political_power = 20", 40)])

E(16, "The Coup Across Usea", "security", "Official",
  "ACES Chronicle, 1997 / 05.30. Erusea's response is provisional gameplay", [
    """The official chronology records that on 30 May 1997 a coup broke out across Usea, and that Unified Command
    defeated it with Scarface 1. In Farbanti the first reports arrive by teleprinter in fragments, contradicting one
    another: barracks seized here, a broadcasting station there, a government that has fled or has not.""",
    """For two days the Erusean cabinet does not know how far the coup reaches. The foreign ministry cannot reach half
    its embassies. The intelligence service has lists of names, most of them out of date. The general staff reports
    that every Erusean garrison is quiet, and the cabinet notices that the general staff is the only body in a
    position to say so.""",
    """That is the real lesson of the coup for Erusea, whatever happened to its neighbours. A government's safety
    depends on the loyalty of the men with the guns, and loyalty is a thing nobody can inspect from the capital.
    The palace, the cabinet and the officers' clubs all reach this conclusion at once, and each of them draws a
    different conclusion from it.""",
    """By the end of the week the coup has been defeated. The questions it raised in Erusea have not.""",
], [("Thank the garrisons for their loyalty.", "army_experience = 5\nadd_stability = 0.01", 60),
    ("Ask the garrisons to prove their loyalty.", "add_stability = 0.02\nadd_war_support = -0.01", 40)])

E(17, "Stonehenge", "battery", "Official",
  "ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge. Erusea's response is provisional gameplay", [
    """The official chronology records that on 19 June 1998 the Federation of Central Usea completed Stonehenge in a
    desert region of neutral San Salvacion: eight railguns, built as an international project under the Federation's
    leadership, to shoot down the fragments of Ulysses before they strike.""",
    """The newsreels show the guns from a distance, each one longer than a city block, aimed at an empty sky. In
    Erusea the pictures are watched with relief and with something less comfortable. The battery will save lives,
    perhaps millions of them. It is also the most powerful weapon ever built on the continent, built on neutral soil
    by Erusea's largest neighbour, and nobody in Farbanti was asked where it should go or who should control it.""",
    """The general staff's engineers study the published specifications and say little in public. The foreign
    ministry's diplomats say a great deal in public and little that anyone remembers. In the newspapers the debate is
    simple and loud: the battery is a shield, or the battery is a gun pointed at the sky that could be pointed
    anywhere.""",
    """The official position, for now, is gratitude. Whether gratitude is what Erusea feels is a question the
    government would rather not ask its citizens, and one that the next years will answer for it.""",
], [("Erusea is grateful.", "add_stability = 0.02", 40),
    ("Erusea is grateful, and is watching.", "add_war_support = 0.02", 60)])

E(18, "The Night of the Fragments", "sky", "Official",
  "ACES Chronicle, 1999 / 07.08. Erusean relief measures are provisional gameplay; no impact sites are scripted", [
    """The official chronology records that on 8 July 1999 Ulysses passed the Earth's Roche limit and broke apart.
    For a decade the government has planned for this night. Now it learns which plans were real.""",
    """Across the world the fragments fall where the astronomers said they might, and some where they said they
    would not. Stonehenge fires into the sky above San Salvacion. The radios carry reports from every continent,
    then from fewer, then only the national stations reading lists of the districts that have lost contact. Erusea's
    shelters fill and empty. Its trains run on the emergency timetable. Its hospitals take whoever comes.""",
    """In the weeks that follow the scale of the catastrophe becomes clear, and so does its shape. The fragments have
    killed, burned and flooded across the continent. Harvests are lost. Whole towns are homeless. And the displaced
    are moving, in columns of cars, carts and people on foot, toward any border where the lights are still on.
    Erusea's lights are on.""",
    """The government has done what it prepared to do. It now faces something it did not prepare for: the arrival,
    at its border and in its towns, of a continent's worth of people who have nowhere else to go.""",
    """The cabinet meets every day. The decade that began with a court ledger ends with a refugee register.""",
], [("Open the relief stores.", "add_stability = 0.03\nadd_political_power = -20", 60),
    ("Guard the relief stores.", "add_war_support = 0.02", 40)])

# ------------------------------------------------------------------ Crown path
E(19, "The Officers' Oath", "court", "Provisional gameplay", NO_SOURCE, [
    """The ceremony takes place in the palace courtyard on a grey morning, with the regimental colours lowered and the
    general staff in the front rank. Each officer steps forward, uncovers and swears, in the old words, to
    serve the Crown and the Crown alone. The old words have not been used in living memory. The chancery found them
    in the archive.""",
    """Nobody pretends the ceremony is merely traditional. The oath binds the officers to the throne, not to the
    general staff, and certainly not to any constitution the country might one day write. Every officer who swears
    it understands this. So does every officer who finds a reason to be on leave that week.""",
    """The general staff makes no objection. Its chief swears first, in a clear voice, and is photographed shaking the
    monarch's hand. The photograph appears in the court gazette and in every officers' mess, and some of the younger
    officers are seen looking at it for a long time.""",
    """An oath is a promise. The palace has collected several thousand of them. Whether they will be kept depends on
    what is asked of the men who made them, and when.""",
], [("Publish the list of those who swore.", "add_stability = 0.02", 60),
    ("Note quietly who did not.", "add_political_power = 15", 40)])

E(20, "The Royal Ulysses Commission", "sky", "Official",
  "ACES Chronicle, 1996 / 04.20. The royal commission is provisional gameplay", [
    """The royal commission meets for the first time in the palace library, among the old survey maps, with the
    official chronology's single terrible sentence pinned to the door: on 20 April 1996 Central Usea announced that
    Ulysses would strike the Earth.""",
    """The commission's powers are broad. It may requisition land, materials and labour. It may order shelters built,
    grain bought and evacuation routes surveyed. It answers to the palace alone, which means it can move faster than
    any ministry and that any failure will carry the Crown's name.""",
    """Its members are chosen by the chancery: engineers from the royal academies, two retired generals, a banker,
    a bishop and the director of the national observatory, who arrives with a briefcase of orbital calculations and
    no patience for speeches. In the first session he explains that the fragments will fall over years, unevenly,
    and that the commission's job is not to stop them but to make sure the country is still standing when they
    stop.""",
    """The commission's first decree orders a shelter in every district town. Its second orders the palace granaries
    filled. The court notices that the decrees are signed by the monarch personally, every one.""",
], [("The Crown will build the shelters.", "add_stability = 0.02", 60),
    ("The Crown will fill the granaries.", "add_political_power = 10", 40)])

E(21, "The Loyal Regiments", "security", "Official",
  "ACES Chronicle, 1997 / 05.30. The Crown's measures are provisional gameplay", [
    """The official chronology records that a coup broke out across Usea on 30 May 1997. In Farbanti the palace does
    not wait to learn how far it reaches. Before the first night is over the chancery has drawn up a list, compiled
    from the oath registers, the garrison reports and the household guard's own files, of the regiments whose
    officers can be trusted absolutely.""",
    """The list is short. It is meant to be. The loyal regiments are moved to the capital's barracks within the week,
    and their commanders are received at the palace one by one. They are thanked, decorated and told, without anyone
    saying so directly, that the Crown now depends on them.""",
    """The regiments that are not on the list notice. Some of their officers write letters protesting their loyalty.
    Others say nothing and are watched more closely for it. In the officers' clubs a new phrase circulates, half
    joke and half complaint: the list. Who is on the list, who has fallen off it, who might be added after the
    next manoeuvres.""",
    """The palace has made itself safer by dividing the army into those it trusts and those it does not. It will now
    have to decide what to do with the men on the wrong side of that line, and with the ones who plotted with
    neighbours abroad.""",
], [("Reward the loyal.", "army_experience = 10", 60),
    ("Watch the rest.", "add_stability = 0.02\nadd_political_power = -10", 40)])

E(22, "The Crown's Protest", "battery", "Official",
  "ACES Chronicle, 1998 / 06.19. The Erusean protest is provisional gameplay with no official source", [
    """The Crown's statement is read by the chancellor from the palace steps, which has not been done for a foreign
    affair in living memory. Erusea welcomes any measure that protects the peoples of Usea from the fragments of
    Ulysses. Erusea notes, however, that Stonehenge was planned, sited and built under the leadership of a single
    power, on neutral soil, without the participation of the continent's other great nation.""",
    """The statement goes on for four more paragraphs, each one more courteous and more pointed than the last. It
    asks for nothing specific. It does not need to. Its purpose is to put on the record that Erusea was not asked,
    and that Erusea minds.""",
    """In the capital the newspapers that support the palace print the statement in full under a photograph of the
    railguns. The others print it under a photograph of the palace steps. In the Federation's capital the statement
    is received with diplomatic silence, which the Erusean ambassador reports as anger.""",
    """The protest costs Erusea nothing today. It has, however, given a royal voice to a feeling that was already
    loose in the country: that the continent's future is being decided elsewhere, by people who do not count Erusea
    among the deciders. That feeling will outlast the fragments.""",
], [("Erusea has said what it needed to say.", "add_war_support = 0.02", 70),
    ("Send a private note of reassurance.", "add_political_power = -15\nadd_stability = 0.01", 30)])

E(23, "The Unbroken Crown", "court", "Provisional gameplay", NO_SOURCE, [
    """The decade's last royal audience is held in the long room where the Crown's question was first asked. On the
    table are the documents that answered it: the decree register, the intendants' reports, the oath lists, the
    commission's shelter census and the accounts of the palace granaries, opened to the districts when the sky fell.""",
    """The palace has governed Erusea through the hardest decade in its history, and it has done so by prerogative.
    The ministries answer to the chancery. The districts answer to the intendants. The officers have sworn to the
    throne and, so far, kept their word. When the fragments came, the relief carried the palace's name, and the
    country remembers it.""",
    """Not everything has gone well. The liberal clubs are quieter, not gone. The general staff is loyal, but it has
    learned to think of itself as the Crown's most indispensable servant, which is a dangerous thing for a servant
    to think. And the country is angry: at the fragments, at the camps on the border, at the neighbours who built a
    battery without asking. Anger, the chancellor reminds the room, is easier to borrow than to repay.""",
    """The monarch closes the audience with one sentence for the minutes. The Crown has kept Erusea whole. It intends
    to keep it whole in the decade to come, whatever that decade asks.""",
], [("The Crown endures.", "add_stability = 0.02", 70),
    ("The Crown remembers who stood by it.", "add_political_power = 25", 30)])

# ------------------------------------------------------------------ constitutional path
E(24, "The Drafting Commission", "assembly", "Provisional gameplay", NO_SOURCE, [
    """Forty-one people sit around the commission's table: jurists, district notables, two palace secretaries, a
    union organizer, a bishop and three professors who have been writing constitutions for Erusea in their spare time
    for twenty years and are finally being asked to read them aloud.""",
    """The first week is spent agreeing on the order of business. The second is spent on the preamble, which every
    member wants to write and nobody wants to vote on. In the third week the commission discovers the questions that
    matter: whether the monarch keeps a veto, whether the assembly controls the army's budget, whether the districts
    elect their own governors and whether the franchise includes everyone over twenty-one or only those who pay
    taxes.""",
    """Outside the hall the country follows the debates in the newspapers, which print the minutes in full. The
    liberal clubs hold rallies for a broad franchise. The landed families hold dinners for a narrow one. The general
    staff holds nothing at all and lets it be known that it is watching the clause on military appointments.""",
    """The commission's chair, an elderly jurist with a famously short temper, tells the press that a constitution
    is a treaty between people who do not trust each other. Erusea, the chair says, has plenty of material.""",
], [("A broad franchise.", "add_popularity = { ideology = democratic popularity = 0.03 }\nadd_stability = -0.01", 50),
    ("A cautious franchise.", "add_stability = 0.02", 50)])

E(25, "The First Assembly", "assembly", "Provisional gameplay",
  "an alternate-history government change with no official source; the cabinet is an unnamed office", [
    """Erusea votes on a spring day, in schools, church halls and railway waiting rooms, in queues that stretch around
    the block in the cities and across the square in the villages. Many voters have never cast a ballot before. Some
    bring their children to watch. The count takes three days, and on the fourth the results are posted on the
    palace gates.""",
    """No party has won outright. The liberals are the largest group; the monarchist leagues are close behind; the
    rest are scattered among labour societies, district lists and a handful of nationalists who campaigned against
    the constitution itself and won seats under it anyway. The assembly will have to govern by coalition from its
    first day.""",
    """The monarch receives the leaders of the largest groups one after another and asks the liberals to form a
    cabinet responsible to the assembly. It is the first time in Erusea's history that a government owes its
    office to votes rather than to the palace. The palace secretaries hand over their keys with formal courtesy.
    Several of them are hired by the new ministers the following week, because nobody else knows where the files
    are.""",
    """The general staff issues a statement pledging its loyalty to the Crown and the charter, in that order. The
    new defence minister reads it carefully and keeps it in a drawer.""",
    """Erusea is now a constitutional monarchy. Its assembly is untested, its parties are young and its decade is
    about to get much harder. But it has chosen its government, and that cannot be unchosen without someone
    breaking a promise the whole country watched being made.""",
], [("Open the first session.", "add_stability = 0.02", 60),
    ("Invite the opposition into the cabinet.", "add_political_power = -15\nadd_stability = 0.03", 40)])

E(26, "The Ulysses Committee", "sky", "Official",
  "ACES Chronicle, 1996 / 04.20. The assembly's committee is provisional gameplay", [
    """The official chronology records that on 20 April 1996 Central Usea announced that Ulysses will strike the
    Earth. Erusea's assembly hears the news in session. The speaker suspends the debate on the fisheries bill, and
    for an hour nobody says anything useful.""",
    """By the evening sitting the parties have agreed, for the first time in the assembly's short life, on something
    important. A standing committee with members from every group will plan for the fragments, in public, with
    published numbers. It will have authority to commission shelters, buy grain and coordinate the provincial
    relief boards, and it will report to the assembly every month.""",
    """The committee's hearings become the most watched programme on Erusean television. Astronomers explain orbits.
    Engineers explain concrete. District officials explain why their shelter is behind schedule, and are asked by
    deputies from the other parties why their district's contractor is the mayor's cousin. It is slow, quarrelsome
    and, to the surprise of the general staff, effective.""",
    """The palace watches the hearings too. So do the officers' clubs, where the conversation is less admiring. A
    country that plans its survival by committee, one colonel remarks, had better hope the sky is patient.""",
], [("Publish every figure.", "add_stability = 0.02\nadd_political_power = -10", 60),
    ("Keep the evacuation routes confidential.", "add_political_power = 10", 40)])

E(27, "Defend the Assembly", "assembly", "Official",
  "ACES Chronicle, 1997 / 05.30. Events in Erusea are provisional gameplay", [
    """The official chronology records that a coup broke out across Usea on 30 May 1997. In Farbanti the news arrives
    during an evening sitting of the assembly. Within an hour there are rumours of troop movements near the capital,
    of officers meeting in a hotel, of a broadcasting station that has stopped broadcasting.""",
    """The speaker refuses to adjourn. The cabinet calls the police and the garrisons whose commanders it trusts, and
    then, because it does not know how far the trust extends, it calls the public. By midnight there are thousands of
    people in the square outside the chamber: students, union men, shopkeepers, veterans, families who brought
    blankets. Nobody organized them. They simply came.""",
    """No troops arrive. Perhaps none were ever coming; perhaps the crowd changed some minds. In the morning the
    general staff reports that every garrison has remained at its post, and the cabinet thanks it formally and
    privately asks the intelligence service for the names of the officers who met in the hotel.""",
    """The assembly survived the coup year without a shot fired in Erusea. It now has to decide what to do with the
    officers who considered firing them, and how to make sure that next time nobody needs to bring a blanket.""",
], [("Thank the crowd.", "add_stability = 0.02\nadd_popularity = { ideology = democratic popularity = 0.02 }", 60),
    ("Find the officers from the hotel.", "add_political_power = 15", 40)])

E(28, "The Stonehenge Debate", "assembly", "Official",
  "ACES Chronicle, 1998 / 06.19. The assembly's debate and vote are provisional gameplay", [
    """The official chronology records that Central Usea completed Stonehenge on 19 June 1998. In Erusea's assembly
    the news begins a three-day debate that the newspapers later call the best the chamber has ever held and the
    worst for anyone's nerves.""",
    """The nationalist deputies want a protest. Erusea, they say, has been excluded from the defence of its own
    continent, and a battery that can shoot at the sky can shoot at anything. The liberal and labour benches want
    a welcome: the battery will save lives, perhaps Erusean lives, and the country's dignity is not worth the
    fragments it will stop. The monarchist leagues propose a compromise that satisfies no one: welcome the battery and
    ask, politely, for a seat on whatever body oversees it.""",
    """The compromise passes, narrowly, with an amendment from the opposition that the government report every six
    months on the battery's operation and on Erusea's requests. The general staff's observer in the gallery leaves
    before the vote.""",
    """The debate settles nothing about the battery. It settles something about Erusea: that its great questions are
    now decided by vote, in public, by people who disagree. Whether that is strength or weakness, the chamber will be
    asked again.""",
], [("Erusea welcomes the battery.", "add_stability = 0.02", 60),
    ("Erusea welcomes it, and keeps the amendment's promise.", "add_political_power = -10\nadd_stability = 0.03", 40)])

E(29, "The Constitutional Settlement", "assembly", "Provisional gameplay", NO_SOURCE, [
    """At the end of the decade the assembly holds a short ceremony that nobody planned. The constitution's original
    copy is brought out of the archive and laid on the speaker's table, and the deputies file past it in silence:
    liberals, monarchists, labour men, district notables, even the nationalists who campaigned against it and now
    sit under its protection.""",
    """The charter has survived a coup year without a shot fired, a fragment year without a famine and a refugee
    crisis without a riot. The courts stand apart from the ministers. The districts have elected boards. The monarchy
    stands above the parties and is more popular than any of them. It is not a perfect settlement. It is a working
    one, which in Erusea is rarer.""",
    """The settlement is untested in one respect. The assembly has never had to decide on a war. The camps on the
    border are full, the continent is broken and the grievances in the country are real. The peace caucus says the
    charter will hold. The general staff says nothing, and has learned to say nothing in a way the deputies find
    louder than speeches.""",
    """The speaker closes the ceremony with a line from the preamble that the commission spent a week arguing over:
    that Erusea's government belongs to those who will live under it. The deputies applaud. Outside, the camps wait.""",
], [("The charter holds.", "add_stability = 0.03", 60),
    ("The charter must be defended.", "add_war_support = 0.02", 40)])

# ------------------------------------------------------------------ regency path
E(30, "The Regency Ordinance", "command", "Provisional gameplay",
  "an alternate-history government change with no official source; the regency is an unnamed office", [
    """The ordinance is signed in the long room on a Tuesday afternoon, with the chief of staff standing at the
    monarch's shoulder and the palace secretaries waiting outside. It runs to two pages. A regency council of serving
    officers will govern in the Crown's name. The ministries will be reorganized as directorates of a command
    administration. The council will report to the throne, which will remain the head of state and the source of
    all legitimacy, in principle.""",
    """The council's members are not named in the ordinance. They are known by their offices: the chief of staff, the
    commanders of the army, the air arm and the navy, the director of military intelligence and two colonels from the
    staff college who drafted most of the memorandum. Their first act is to confirm every civil servant in post, which
    reassures the ministries more than any proclamation could.""",
    """The country receives the news with the same weary recognition it showed when the colonels first appeared in
    the corridors. There are no demonstrations, because demonstrations require permits and the permits office now
    belongs to a directorate. The liberal clubs close. Some of their members leave the country. Most stay, and wait.""",
    """The regency has promised order, efficiency and security in a dangerous decade. It now has to deliver them, with
    no assembly to blame and no palace to hide behind.""",
], [("The council governs.", "add_war_support = 0.03", 60),
    ("The council governs in the Crown's name.", "add_stability = 0.02\nadd_political_power = -10", 40)])

E(31, "The Requisition Boards", "command", "Provisional gameplay", NO_SOURCE, [
    """The first requisition board sits in a former customs house in the capital, three officers at a long table with
    a stamp, a ledger and a sentry at the door. By the end of the month there is one in every district. They may
    requisition trucks, warehouses, fuel and labour for national purposes, with receipts redeemable after the
    emergency.""",
    """The receipts become a currency of their own. Shopkeepers trade them, banks discount them and a satirical
    weekly prints its own, redeemable 'after the regency'. The weekly is closed. The receipts keep circulating.""",
    """The boards work, in the narrow sense that the directorates get what they ask for when they ask for it. Arms
    plants receive steel before furniture makers. Trains move the army's freight first. The general staff's
    logisticians, who have spent careers explaining why things take time, discover that most of the time was spent
    asking permission.""",
    """In the districts the boards are feared and, more quietly, admired. They are the regency's real face: efficient,
    unaccountable and very hard to argue with. The council's economists warn that a country run on receipts will
    eventually be asked to pay them.""",
], [("The receipts will be honoured.", "add_stability = 0.02\nadd_political_power = -10", 40),
    ("The receipts will be honoured later.", "army_experience = 5", 60)])

E(32, "Civil Defence Command", "sky", "Official",
  "ACES Chronicle, 1996 / 04.20. The regency's command is provisional gameplay", [
    """The official chronology records that on 20 April 1996 Central Usea announced that Ulysses will strike the
    Earth. The regency answers within a day, in the way it knows best. A Civil Defence Command is created with a
    general at its head, a staff in the old war ministry and every district placed under its orders.""",
    """The command's first directive is twelve pages long and contains no adjectives. Every town will have a shelter.
    Every district will hold grain for ninety days. Every road out of every city will have an evacuation timetable.
    Every school will practise its drills twice a year. The directive gives deadlines, names responsible officers and
    lists the penalties for missing them.""",
    """The country grumbles, digs and complies. The drills are resented: sirens at dawn, soldiers at the crossroads,
    children marched to shelters in their nightclothes. They are also fast, faster every time, and the newspapers
    that are still allowed to print figures print them with something like pride.""",
    """The regency's critics, abroad and in the closed clubs, say that a government that treats its citizens as
    soldiers will one day ask them to be soldiers. The command's general, asked about this by a foreign journalist,
    answers that the fragments do not care about the distinction.""",
], [("Every district will be ready.", "add_stability = 0.02\nadd_political_power = -10", 60),
    ("Every district will be inspected.", "army_experience = 5", 40)])

E(33, "Martial Law", "command", "Official",
  "ACES Chronicle, 1997 / 05.30. The regency's ordinances are provisional gameplay", [
    """The official chronology records that a coup broke out across Usea on 30 May 1997. The regency council meets
    within the hour, with the director of military intelligence reading the teleprinter reports aloud as they
    arrive. By midnight the council has signed a set of martial law ordinances that the staff college drafted three
    years ago and never expected to use.""",
    """There is a certain irony in the situation, which the council's members notice and do not discuss. The regency
    is the one government on the continent that cannot be overthrown by its own army, because it is its own army. It
    is not afraid of a coup. It is afraid of contagion: of plotters abroad with friends in Erusean barracks, of
    junior officers who look at a council of generals and see a precedent.""",
    """The ordinances close the borders to unregistered travel, put the broadcasting stations under military guard
    and give the intelligence service authority to detain any officer who has corresponded with foreign plotters.
    Several dozen are detained in the first week. Most are released. A few are not.""",
    """By the end of the week the coup abroad has been defeated. The ordinances remain in force for a year, because a
    regency that has learned to fear its own officers does not unlearn it quickly.""",
], [("Order is maintained.", "add_stability = 0.02", 60),
    ("Release those detained in error.", "add_stability = 0.01\nadd_political_power = -10", 40)])

E(34, "The Railgun Study", "battery", "Official",
  "ACES Chronicle, 1998 / 06.19, and Super Weapons, Stonehenge. The staff study is provisional gameplay, not a record of Erusean planning", [
    """The official chronology records that Central Usea completed Stonehenge on 19 June 1998: eight railguns in a
    desert region of neutral San Salvacion, built to shoot down the fragments of Ulysses. The regency's general staff
    asks its engineers a question that the rest of the continent is too polite to ask aloud: what else could those
    guns do?""",
    """The study takes four months. It uses only published specifications, newspaper photographs and the calculations
    of the national observatory, and it is classified at the highest level the regency possesses. Its conclusions
    are technical and cautious. A battery that can reach fragments in orbit can, in principle, reach aircraft at
    altitude. Its fire would be decisive over a wide area. Its owner would control the sky above much of the
    continent.""",
    """The council reads the study in silence. Nobody proposes anything. Nobody needs to. The study is filed, and its
    conclusions are taught at the staff college the following year as an exercise in strategic geography, with the
    names of the countries removed.""",
    """The regency's official position on Stonehenge is gratitude, expressed in a short telegram. Its unofficial
    position is a file in a safe in the old war ministry, and the knowledge that the most powerful weapon on the
    continent belongs to someone else.""",
], [("File the study.", "army_experience = 5", 60),
    ("Teach the study.", "add_war_support = 0.02", 40)])

E(35, "The Regency's Mandate", "command", "Provisional gameplay", NO_SOURCE, [
    """The council's statement is broadcast at noon on the last day of the decade, read by an announcer in uniform.
    The regency, it says, has carried Erusea through the most dangerous decade in its history. It built the shelters
    on time. It kept the army loyal in the coup year. It fed the displaced when the fragments came. It has earned
    the mandate it was given, and it will keep that mandate for as long as Erusea needs it.""",
    """There is no mention of the Crown's seals, or of the date the council once published for returning them. The
    palace issues no statement. The officers who believed in the date say nothing in public. In private, some of them
    begin to keep diaries.""",
    """The country's reaction is the familiar one. The regency is efficient, unloved and, for now, unchallenged. The
    camps on the border are run by the army. So are the railways, the broadcasting stations and the grain stores.
    The council's critics have mostly gone abroad or gone quiet.""",
    """The regency enters the new decade with more power than any Erusean government has held since the monarchy's
    founding, and with one problem it cannot order away: a government that justifies itself by danger needs the
    danger to continue.""",
], [("The mandate stands.", "add_war_support = 0.03", 70),
    ("Promise a review of the mandate.", "add_stability = 0.02\nadd_political_power = -15", 30)])

E(36, "The Seals Returned", "peace", "Provisional gameplay",
  "an alternate-history government change with no official source; the restored council is an unnamed office", [
    """The ceremony is brief. The chief of staff enters the long room with the seals of office in a leather case,
    places them on the table in front of the monarch and steps back. The council's members follow, one by one, and
    lay their commissions beside the seals. Then they salute, turn and leave by the side door, and the palace
    secretaries come in by the front.""",
    """The council has kept its promise. The fragments have fallen, the camps are run by civilians and the seals have
    returned to the Crown. The monarch governs through a restored Crown Council, and the officers return to their
    barracks with a decade of governing behind them and, for most of them, considerable relief.""",
    """Not all of them. Some officers believe the regency was right to govern and wrong to stop. Some believe it
    should never have begun. A few believe that the Crown, having been rescued by the army once, can be rescued
    again, and that next time the rescue need not end. The restored council is aware of all three groups and has no
    plan for any of them yet.""",
    """In the streets the reaction is relief, cautious and quiet. People have learned not to celebrate too loudly in
    front of soldiers. They have also learned that the soldiers can be persuaded to leave, which is a lesson no
    Erusean government will be able to unteach.""",
], [("The Crown governs again.", "add_stability = 0.03", 60),
    ("Thank the council publicly.", "army_experience = 5\nadd_stability = 0.01", 40)])

E(37, "The Crown's Acceptance", "battery", "Official",
  "ACES Chronicle, 1998 / 06.19. The Crown's acceptance is provisional gameplay", [
    """The official chronology records that Central Usea completed Stonehenge on 19 June 1998. The Crown's statement
    is short, warm and read from the chancery rather than the palace steps. Erusea welcomes the battery as the
    continent's shield against the fragments, thanks the nations that built it and asks only to be kept informed of
    its operation.""",
    """The general staff calls it weakness in a memorandum that reaches the newspapers within a day. The court
    gazette calls it statesmanship. The Federation's ambassador calls at the palace with a personal letter of thanks
    from the Federation's government, which the chancery frames and hangs in the corridor outside the long room.""",
    """In the country the statement is received with relief by people who wanted the fragments stopped and with
    resentment by people who wanted Erusea to be asked. Both groups are large. The palace has chosen to speak for the
    first, knowing the second will not forget.""",
    """The acceptance has bought Erusea goodwill in the continental capitals and a quiet border for the fragment
    years. Whether it has bought anything at home, the next decade will tell.""",
], [("Erusea keeps its word.", "add_stability = 0.02", 60),
    ("Ask the general staff to keep its opinions private.", "add_political_power = -10\narmy_experience = -5", 40)])

E(38, "The Relief Trains", "industry", "Official",
  "ACES Chronicle, 1999 / 07.08. The relief timetable is provisional gameplay; no impact sites are scripted", [
    """The official chronology records that Ulysses passed the Roche limit on 8 July 1999. Within a day the rail
    ministry has pulled the military timetable out of its safe and put it into force for a purpose its authors never
    imagined: relief.""",
    """The trains run day and night. Outward, they carry tents, water tanks, field kitchens, medicine and engineers.
    Inward, they carry the injured, the orphaned and the displaced, many of them from beyond Erusea's borders, to
    hospitals and schools in the undamaged districts. The station masters keep their own registers, because nobody
    else is keeping any.""",
    """The railway workers are the heroes of the fragment months. They work double shifts without being asked, sleep
    in signal boxes and drive engines that the ledger said should have been retired years ago. A locomotive driver
    who runs a relief train through a burning valley becomes, for one week, the most famous person in Erusea. The
    rail ministry refuses to release the driver's name, at the driver's request.""",
    """When the trains finally return to the ordinary timetable, the country has learned what its railways are for.
    It has also learned how many people are now living in the camps at the end of the line.""",
], [("Thank the railway workers.", "add_stability = 0.02", 60),
    ("Keep the relief timetable in force.", "add_political_power = -10\nadd_stability = 0.01", 40)])

# ------------------------------------------------------------------ the tree switch: one era transition per path
CARRY = "the 1990s path is provisional gameplay; ACES Chronicle, 1999 / 07.08 and 2000 / 04.21 are the official anchors"
E(40, "A Kingdom After Ulysses", "court", "Official", CARRY, [
    """The decade of the court ledger is over. Ulysses passed the Roche limit on 8 July 1999, as the official
    chronology records, and the world it fell on is not the world the palace planned for. Erusea enters the new
    decade as a kingdom governed by prerogative, with its regiments sworn to the throne and its relief stores
    carrying the Crown's name.""",
    """The kingdom has survived. Its neighbours, some of them, have not survived intact. The continent is full of
    ruined harvests, broken towns and people walking toward any border where the lights are on, and Erusea's lights
    are on. The camps at the frontier grow by the week. The palace's granaries, which fed the districts through the
    fragment months, are nearly empty.""",
    """In the long room the conversation has changed. The questions of the 1990s were about who governs. The questions
    of the new decade are about what Erusea is owed and by whom. The court gazette prints letters from district towns
    that took in the displaced and want to know who will pay. It prints editorials about the battery in San
    Salvacion, built by others, aimed at the sky, guarding a continent that did not ask Erusea's opinion. It prints
    nothing about the general staff, which is busier than it has been in years.""",
    """The Crown governs a country that is proud, frightened and angry, and it has spent a decade teaching that
    country to look to the throne for answers. The throne will now be asked for them.""",
    """The official chronology records what comes next for Erusea's border on 21 April 2000. What comes after that
    depends, in part, on what the Crown chooses to say.""",
], [("The Crown will speak for the nation.", "add_to_variable = { ac_ucw_grievance = 2 }\nac_ucw_bound = yes\nadd_war_support = 0.02", 70),
    ("The Crown will speak for calm.", "add_stability = 0.02", 30)])

E(41, "An Assembly After Ulysses", "assembly", "Official", CARRY, [
    """The constitutional decade ends with the assembly in emergency session. The official chronology records that
    Ulysses passed the Roche limit on 8 July 1999. Erusea's charter survived the fragment months; the question now is
    whether it can survive their consequences.""",
    """The reception camps opened by the relief act are full, and still the columns arrive. The provincial boards are
    exhausted and the treasury warns that the next supplementary budget will not pass. In the gallery, every day,
    sit the mayors of the border towns, who voted for the charter and now want to know why their schools are
    dormitories.""",
    """The parties have begun to divide along a line the constitution never anticipated. The liberal and labour
    benches insist that Erusea keep its doors open and its promises. The monarchist leagues want quotas. The
    nationalist deputies, who campaigned against the charter and now sit under it, want the border closed and the
    continent made to pay for a disaster it caused Erusea to share. Their speeches are the most reported in the
    country.""",
    """The official chronology records that Erusea stopped taking in refugees on 21 April 2000. Under this charter
    that decision, or any other, will be taken by vote, in public, by people who will have to explain it to the
    voters at the next election. The assembly has never been asked a harder question. It has never been better
    placed to answer it honestly.""",
], [("The charter will answer.", "add_stability = 0.02", 60),
    ("Ask the peace caucus to lead the debate.", "add_to_variable = { ac_ucw_grievance = -3 }\nac_ucw_bound = yes\nadd_war_support = -0.02", 0)])

E(42, "A Regency After Ulysses", "command", "Official", CARRY, [
    """The regency enters the new decade with the fragments behind it and its mandate in front. The official
    chronology records that Ulysses passed the Roche limit on 8 July 1999. The council's directorates fed the
    displaced, ran the trains and kept order, and the council has told the country so every evening since.""",
    """The camps at the frontier are run by the army. So are the crossings, the roads behind them and the registers
    of who is allowed through. The council's border command reports that the columns are growing, that the camps
    cannot be expanded indefinitely and that the neighbouring governments have stopped answering letters about who
    will pay.""",
    """The council's propaganda office has found its theme. Erusea, it says, prepared for the fragments when others
    did not, and is now asked to carry the cost of their failure. The battery in San Salvacion, built by others,
    could not stop the sky from falling on Erusea's neighbours; it stands now as a monument to a continent that
    decided Erusea's future without Erusea. The theme is popular in the barracks and, more worryingly for the
    council's critics, in the towns.""",
    """A government that justifies itself by danger needs the danger to continue. The regency's danger has changed
    shape. The official chronology records what Erusea does about its border on 21 April 2000, and what it does
    about its neighbours in the summer of 2003. The council has filed studies for both.""",
], [("The army will hold the border.", "add_to_variable = { ac_ucw_grievance = 3 }\nac_ucw_bound = yes\narmy_experience = 5", 70),
    ("The directorates will run the camps.", "add_to_variable = { ac_ucw_pressure = -3 }\nac_ucw_bound = yes", 30)])

# ------------------------------------------------------------------ home front
E(43, "The Camps Along the Border", "refugees", "Official",
  "ACES Chronicle, 2000 / 04.21 is the official anchor for the border; camp administration is provisional gameplay", [
    """The camps began as a few fields of tents beside the frontier crossings in the summer of the fragments. They are
    now towns without names: rows of tents and huts, water tankers, latrines, a clinic, a school that meets in the
    open, a market where the displaced sell what they carried to the people who carried nothing.""",
    """Nobody planned them. The district authorities put up the first tents because people were arriving and it was
    raining. The army dug the first drains because the district authorities asked. The charities came next, then the
    journalists, then the officials from the capital with clipboards and questions about who was responsible.""",
    """The official chronology records that Erusea stopped taking in refugees on 21 April 2000. Whatever happens at
    the frontier, the people already inside it are here and will be here for years. Someone must register them,
    feed them, keep the disease out of the camps and the anger out of the towns next to them. Someone must decide
    whether the camps are a waiting room or a beginning.""",
    """The interior ministry asks the cabinet to choose. The cabinet asks for a week. The camps do not wait.""",
], [("Register every person.", "add_to_variable = { ac_ucw_pressure = -2 }\nac_ucw_bound = yes", 60),
    ("Guard every crossing.", "add_to_variable = { ac_ucw_grievance = 2 }\nac_ucw_bound = yes\nadd_war_support = 0.01", 40)])

E(44, "The Home Front Council", "industry", "Provisional gameplay",
  "Erusean domestic administration from 2000 to 2003 has no official source", [
    """The council meets for the first time in the old stock exchange, the only hall in the capital large enough for
    everyone who claimed a seat. Ministries, districts, unions, employers, the charities from the camps and the
    general staff's logisticians sit at tables arranged in a square, so that nobody is at the head.""",
    """Its mandate is practical. The camps need food that the farms are struggling to grow. The factories need hands
    that the camps can supply, if the unions agree and the law allows. The railways need coal that the mines are
    short of men to dig. Every problem touches every other problem, and for two years each ministry has solved its
    own by making somebody else's worse.""",
    """The council solves very little in its first month. In its second it agrees on a single register of labour,
    food and transport, the first time Erusea has counted all three in one book. In its third it begins, cautiously,
    to make decisions that stick.""",
    """The general staff's representatives take careful notes on everything. When a journalist asks one of them why
    the army is so interested in rations and train schedules, the officer answers that the army is interested in
    everything that keeps a country standing. The answer is printed. It is read in several capitals.""",
], [("One register for everything.", "add_stability = 0.02", 60),
    ("Let the army chair the transport committee.", "army_experience = 5\nadd_war_support = 0.01", 40)])

E(45, "The Casualty Lists", "refugees", "Official",
  "ACES Chronicle, 2003 / SUMMER: Erusea is at war. The lists are provisional gameplay; no casualty figures are scripted", [
    """The lists are posted every Friday at noon, on boards outside every town hall in Erusea. They are printed in
    small type, alphabetically, by district: killed, wounded, missing. On the first Friday the boards are half
    empty. By the autumn the town halls need second boards.""",
    """People gather before noon and wait in silence. When the clerk pins up the new sheets, the crowd moves forward,
    and for a few minutes the only sound is people reading. Then someone finds a name. The others step back to give
    them room, and go on reading.""",
    """The government argued for a month about whether to publish the lists at all. The general staff wanted them
    withheld until the end of each campaign. The interior ministry warned that rumours would be worse than names. In
    the end the lists were published because the families demanded them, and because a country at war needs to know
    what the war is costing even when the knowledge hurts.""",
    """The lists change the country. They make the war real in every district, every Friday. They make the
    communiques harder to believe and the speeches harder to make. And they make Erusea's families, more than its
    ministers, the judges of whether the war was worth fighting.""",
], [("Keep the lists public.", "add_stability = 0.01\nadd_war_support = -0.02", 50),
    ("Print the decorations beside the lists.", "add_war_support = 0.02", 50)])

# ------------------------------------------------------------------ the three governments at war
WAR_START = "ACES Chronicle, 2003 / SUMMER: Erusea invades San Salvacion and seizes Stonehenge. The government's conduct is provisional gameplay"
E(46, "The Crown at War", "court", "Official", WAR_START, [
    """The official chronology records that in the summer of 2003 Erusea invaded neutral San Salvacion and seized
    Stonehenge, turning its railguns against aircraft. The order went out under royal decree, as the Crown's
    mobilization laws require. The palace is now at war, and everything it does is war policy.""",
    """The Privy Council sits every day, with the chiefs of staff at the table and the minutes kept secret for the
    first time since the decade of the court ledger. The household guard has been expanded to a brigade. The court
    gazette prints the communiques beside the royal decrees, and the decrees grow longer.""",
    """The monarch visits the forward airfields and the field hospitals and is photographed at both. The photographs
    are popular. So, for the first months, is the war: the grievance that the Crown spoke for has become a
    campaign, and the campaign is going well. In the officers' clubs the toasts are to the throne.""",
    """The chancery's oldest secretaries have seen enough reigns to be uneasy. A Crown that leads a war is judged by
    the war. Victories add to the throne's prestige; defeats subtract from it, and a defeat large enough subtracts
    the throne itself. The secretaries keep their worries out of the minutes. They begin, quietly, to put the palace
    archive in order.""",
], [("For the Crown and the nation.", "add_war_support = 0.03", 70),
    ("The Crown will share every hardship.", "add_stability = 0.02\nadd_political_power = -10", 30)])

E(47, "The Assembly at War", "assembly", "Official", WAR_START, [
    """The official chronology records that in the summer of 2003 Erusea invaded neutral San Salvacion and seized
    Stonehenge. Under the charter, the decision passed through the assembly. The debate lasted two days and the vote
    was closer than the government admits; the peace caucus voted against, and three of its members resigned their
    seats rather than vote at all.""",
    """The assembly is now a war council. It sits every day and votes on every major supply bill, and its committee
    of inquiry examines every significant loss in public, with the generals as witnesses. The generals hate the
    hearings. The families of the soldiers watch every one of them.""",
    """Erusea is the only country in the war that fights it with a free press and an opposition in the chamber, and
    the government is not sure whether this is a strength or a weakness. The communiques are checked against the
    correspondents' reports. The casualty lists are read aloud at the start of every sitting. Every month the peace
    caucus tables a motion asking the cabinet to seek terms, and every month it fails by a smaller margin.""",
    """The charter was written for a country at peace. It is now being tested by the one thing its authors feared
    most, and the test will be judged, as everything in the new Erusea is judged, by vote.""",
], [("The assembly will see this through.", "add_war_support = 0.02", 60),
    ("The assembly will hear every objection.", "add_stability = 0.02\nadd_war_support = -0.02", 40)])

E(48, "The Regency at War", "command", "Official", WAR_START, [
    """The official chronology records that in the summer of 2003 Erusea invaded neutral San Salvacion and seized
    Stonehenge, turning its railguns against aircraft. For the regency council, the war is the plan it filed a
    decade ago, updated, approved and executed by the same officers who drafted it.""",
    """There is no assembly to persuade and no palace to consult. The council issues orders, the directorates carry
    them out and the propaganda office explains them afterwards. The army fights the war the general staff has
    studied for twenty years, against an enemy it has war-gamed for ten, and in the first months it fights it very
    well.""",
    """The council's problem is not at the front. It is in the country, which has been governed by soldiers for so
    long that it no longer distinguishes between the war and the government. Every shortage is the regency's.
    Every casualty is the regency's. Every rumour from the front is a rumour about the regency, and the propaganda
    office's denials are believed less with every Friday's lists.""",
    """The council has always said it governs because Erusea is in danger. Erusea is now in the greatest danger of
    its history, and the council is responsible for it in every sense of the word.""",
], [("The council will win this war.", "add_war_support = 0.03\narmy_experience = 5", 70),
    ("The council will account for this war.", "add_stability = 0.01", 30)])

# ------------------------------------------------------------------ the Aegir fleet, the air arm and Megalith
E(49, "Aegir Fleet Command", "fleet", "Official",
  "ACES Chronicle, 2004 / 11.23 names the Aegir fleet. Its command, doctrine and timing here are provisional gameplay", [
    """The Aegir fleet has a commander, a staff, a home anchorage and a name that the official chronology will one
    day record. What it does not yet have is a doctrine for the war it may be asked to fight: a war against a
    coalition of continental powers that between them control the sea lanes, the ports and, if they can take it
    back, the sky.""",
    """The fleet's officers divide along the old lines. The battle-line school wants to find the enemy's main force
    and destroy it in one engagement, before the coalition's greater numbers can tell. The fleet-in-being school
    wants the Aegir fleet to stay in harbour under strong defences, forcing the enemy to guard against it everywhere,
    and to sail only when the odds are certain.""",
    """Both schools agree on the fleet's weaknesses. Its home anchorage can be found. Its escorts are too few. Its
    sailors are well trained and inexperienced. And a fleet, unlike an army, cannot be rebuilt in a season: whatever
    is lost is lost for a decade.""",
    """The fleet commander's staff presents both doctrines to the government and asks for a decision. The government
    asks the commander for a recommendation. The commander, who has read history, recommends whichever doctrine
    keeps the most ships afloat.""",
], [("The fleet will be ready to fight.", "navy_experience = 10", 60),
    ("The fleet will be ready to survive.", "add_stability = 0.01", 40)])

E(50, "After Comberth Harbor", "fleet", "Official",
  "ACES Chronicle, 2004 / 11.23. No naval losses are scripted by this event", [
    """The official chronology records that on 23 November 2004 ISAF sank the Aegir fleet at Comberth Harbor. The news
    reaches the capital in a single signal from the harbour's naval station, and then nothing more for six hours.""",
    """When the reports finally come, they come all at once: the strike, the fires, the hulls settling in the harbour,
    the crews swimming for the quays. The fleet that was planned in the 1990s and built over a decade, the fleet whose
    name the country learned from the newspapers and the recruiting posters, is gone in a morning.""",
    """In the naval ministry the officers count what is left. Some escorts were at sea. Some submarines were on
    patrol. Some sailors were ashore, on leave, in hospital, at training schools inland. They will need ships, or
    other duties, or simply to be told what happened by someone who was not on the quay.""",
    """In the country the loss is felt as a wound to pride as much as to strength. The Aegir fleet was a promise that
    Erusea could stand among the great powers. The government must decide what to say about it, and what to do with
    the sailors who survived it.""",
], [("Gather the survivors.", "navy_experience = 5\nadd_stability = 0.01", 60),
    ("Honour the fleet.", "add_war_support = 0.02", 40)])

E(51, "The Air Doctrine Board", "air", "Official",
  "ACES Chronicle, 2003 / SUMMER: Erusea used Stonehenge's railguns against aircraft. The board and its doctrines are provisional gameplay", [
    """The air arm's commanders meet in a bunker under the capital's main airfield, where the ventilation hums and the
    coffee is terrible. On the wall is a map of the continent with Stonehenge's range drawn on it in red, a circle
    wider than most of the countries inside it.""",
    """The official chronology records that Erusea seized the battery and turned its railguns against aircraft. The
    question for the board is how the air arm fights alongside it. One faction wants to concentrate the best pilots
    in elite squadrons and win the sky the old way, aircraft against aircraft. The other wants to fight under the
    battery's umbrella, drawing the enemy into the railguns' reach and letting the battery do the work that pilots
    would otherwise die doing.""",
    """Both factions are right about the other's weakness. Elite squadrons can be worn down by numbers. An umbrella
    lasts only as long as the battery stands, and the enemy knows exactly where the battery is.""",
    """The board's chair, who flew interceptors in the 1990s and has buried more pilots than most officers have
    commanded, writes the decision in one line and signs it. The air arm will fight the war it can win, for as long
    as it can win it.""",
], [("Concentrate the best pilots.", "air_experience = 10", 50),
    ("Fight under the battery.", "add_war_support = 0.02", 50)])

E(52, "The Megalith Directorate", "megalith", "Official",
  "Super Weapons, Megalith: an Erusean fortress built to bring down orbiting Ulysses fragments. No construction date is given or implied", [
    """The official record describes Megalith as an Erusean fortress built to bring down orbiting Ulysses fragments.
    The directorate created to answer for it inherits a site, a staff of engineers, a budget that appears in no
    published estimate and a question that its first director asks aloud at the first meeting: what is Megalith for,
    now?""",
    """Its original purpose was a defence against the sky. Fragments of Ulysses still orbit the Earth, decaying slowly,
    and some will fall. A fortress that can bring them down safely is a service to Erusea and to everyone downrange.
    The engineers who built it believe in that purpose, and many of them chose this work because of it.""",
    """But Erusea is at war, and in war everything is weighed for its military use. The general staff has asked for
    the site's specifications twice. Military intelligence has placed counter-intelligence officers in the
    engineers' quarters. The directorate's budget is now approved by a committee that includes two generals and no
    astronomers.""",
    """The directorate's first report states the facts and avoids the question. It lists the staff, the security
    arrangements and the scientific programme. In its final paragraph it notes, without comment, that a fortress
    able to bring down fragments is a fortress that someone may one day ask to do something else.""",
], [("Megalith serves the sky.", "add_stability = 0.01", 50),
    ("Megalith serves Erusea.", "add_war_support = 0.02", 50)])

E(53, "The Young Officers", "megalith", "Official",
  "ACES Chronicle, 2005 / 09.26 records that young Erusean officers seized Megalith. The surveillance reports are provisional gameplay", [
    """The counter-intelligence officers at Megalith file their reports every Monday. Most of them are routine: who
    visited the engineers' quarters, which telephone lines were used, how many crates arrived and how many left. In
    the autumn, the reports begin to include something else.""",
    """Some of the young officers in the site's garrison talk, late at night, about what they would do if the war
    were lost. They do not talk about surrender. They talk about honour, about the fragments still in orbit and about
    the fortress they are guarding. Their conversations are recorded and transcribed and sent to the capital, where
    they are read, filed and not acted upon.""",
    """The official chronology records that after Erusea's surrender young officers seized Megalith. The reports on
    the director's desk do not predict that. They describe a mood: young officers who have given years to a war, posted
    to a place nobody is allowed to know about, beginning to believe that the place itself is the last thing they can
    defend.""",
    """The director must decide what to do with the reports. Transfers would scatter the group. Arrests would make
    martyrs. Doing nothing would leave a garrison of believers guarding the most dangerous site in Erusea.""",
], [("Transfer the loudest of them.", "add_stability = 0.01\narmy_experience = -5", 50),
    ("File the reports and watch.", "add_political_power = 10", 50)])

E(54, "The Occupation Authority", "occupation", "Official",
  "ACES Chronicle, 2003 / SUMMER. Occupation administration is provisional gameplay; no ownership, core or border changes are scripted", [
    """The official chronology records that Erusea invaded neutral San Salvacion and seized Stonehenge in the summer
    of 2003. Behind the advancing columns lie towns, roads, farms and people who did not choose this war and now live
    under Erusean guns.""",
    """The occupation authority is created by decree in the first week. Its mandate is to govern what the army holds,
    under the laws of war, without annexing anything. Erusea claims no territory, the decree says; it holds ground
    for the duration. The distinction matters to the lawyers in the foreign ministry and to the diplomats in the
    neutral capitals. Whether it matters to a farmer whose truck has been requisitioned is another question.""",
    """The authority's officials face the same choices every occupying power has faced. Military administration is
    fast and firm, and it makes enemies. Civil commissioners are slower and more acceptable, and they need the army's
    protection anyway. Curfews keep the streets quiet and the resentment loud. Food distribution keeps people alive
    and makes them dependent.""",
    """Erusea's soldiers did not train to govern foreign towns. They are learning, under the eyes of the neutral
    relief agencies, the foreign press and the people they govern, all of whom are keeping records.""",
], [("Govern firmly.", "army_experience = 5", 60),
    ("Govern correctly.", "add_stability = 0.01\nadd_political_power = -10", 40)])

# ------------------------------------------------------------------ postwar lanes
E(55, "Under Oversight", "peace", "Official",
  "ACES Chronicle, 2005 / 09.19 and 09.26. The provisional government is shown through flags and ideas; there is no forced government swap", [
    """The official chronology records that Farbanti fell and Erusea surrendered on 19 September 2005, and that on 26
    September young officers seized Megalith, which ISAF destroyed. In the weeks that followed, Erusea formed a
    provisional autonomous government under ISAF oversight.""",
    """The government is Erusean. Its ministers are Erusean, its civil servants are the same people who ran the
    ministries before the war and its decisions are made in Farbanti. But every decision is reviewed by the
    oversight commission, every weapon is registered, every unit's demobilization is inspected and every budget is
    read by officials from the countries Erusea fought.""",
    """The country receives the arrangement with exhaustion more than anger. The war is over. The casualty lists have
    stopped. The prisoners are coming home by train, and the stations are full of families who have waited two
    years. Most people want work, food, heating for the winter and a government that will not ask them to fight
    again. The provisional government can offer most of that, if the commission allows.""",
    """Not everyone accepts the surrender. Officers who believed in the war are leaving the army with bitterness and
    their service pistols. Veterans' leagues are meeting in back rooms. The government knows all this, and must
    decide whether to cooperate fully with its supervisors or to give them as little as it can.""",
], [("Cooperate, and be judged by the record.", "add_stability = 0.02", 70),
    ("Comply, and remember.", "add_war_support = 0.02", 30)])

E(56, "A Provisional Order", "assembly", "Provisional gameplay",
  "the postwar administration from 2005 onward is a provisional gameplay branch on the official 2005 / 09.26 anchor", [
    """A year after the surrender the provisional government has something it did not have at the start: a working
    order. The disarmament registry is complete. The conscripts have been discharged and most of them have found
    work. The veterans' pensions are paid, late and short but paid. The oversight commission's reports have become
    routine, which is the highest praise a supervisor can give.""",
    """It is not sovereignty in the old sense. Erusea cannot raise an army beyond the limits the commission sets,
    cannot sign treaties without review and cannot forget, for a single day, that it lost. But the ministries work,
    the trains run and the schools have reopened, including the ones in the border towns that were dormitories for
    the displaced a decade ago.""",
    """The government watches the veterans' leagues closely. Most of their members want pensions, medals and to be
    left alone. A few want another war, and some of those have found each other. The government's intelligence
    officers read their newsletters and attend their meetings, and send reports to a government that has learned to
    take reports seriously.""",
    """The provisional order is fragile, imperfect and supervised. It is also functioning, which a year ago few
    people in Farbanti believed it could.""",
], [("Build on the order.", "add_stability = 0.02", 70),
    ("Prepare for those who reject it.", "add_political_power = 15", 30)])

E(57, "The Victor's Peace", "peace", "Provisional gameplay",
  "an alternative outcome; in the official chronology Erusea surrendered on 19 September 2005", [
    """In this alternative history the war ends with Erusea's armies holding the field. The coalition's governments
    have asked for terms. Erusea's negotiators arrive at the conference with maps, demands and a mandate from a
    country that has paid for its victory in casualty lists posted every Friday for two years.""",
    """Erusea annexes nothing. Its garrisons stay in the occupied districts as guarantors of the peace, under
    published terms, and the general staff insists that they stay until the treaties are signed and kept. The
    defeated governments remain in office, humiliated and resentful, and the neutral capitals watch Erusea for any
    sign that its peace is an empire by another name.""",
    """At home the victory is celebrated and then, quickly, counted. The war cost more than the propaganda admitted.
    The camps are still full. The factories that ran three shifts for the war need new orders. The veterans want
    work, and some of them want parades.""",
    """The government must decide what kind of victor Erusea will be. A magnanimous peace would buy goodwill and
    leave the country's grievances unanswered. A hard peace would answer them and buy a generation of enemies. The
    general staff, the assembly or the palace, whichever governs, will be remembered for the choice.""",
], [("A victor can afford to be generous.", "add_stability = 0.02", 30),
    ("A victor sets the terms.", "add_war_support = 0.02", 70)])

E(58, "The Continental Order", "diplomacy", "Provisional gameplay",
  "an alternative outcome; in the official chronology Erusea surrendered on 19 September 2005", [
    """Two years after the victory, the shape of Erusea's peace is clear on the map, though no border on it has moved.
    Erusean garrisons sit in the neighbours' capitals and at their railway junctions. Treaties limit the neighbours'
    armies and guarantee Erusea's trade. Debts, of one kind or another, run toward Farbanti from every direction.""",
    """The foreign ministry calls it the continental order. The neighbours' newspapers, where they are allowed to,
    call it an occupation. The neutral capitals call it an arrangement and wonder how long it will last.""",
    """Inside Erusea the order is popular and expensive. The garrisons need regiments that the economy needs as
    workers. The treaties need inspectors. The debts need collecting, and the collectors are not welcome. The
    general staff warns that resentment is growing in every capital where Erusean soldiers stand, and that a peace
    held by garrisons is a peace that ends when the garrisons leave.""",
    """Erusea has won the war that the official chronology says it lost. It now faces the problem that every victor in
    history has faced: winning was the easy part.""",
], [("Hold the order.", "army_experience = 5\nadd_war_support = 0.01", 60),
    ("Begin to withdraw the garrisons.", "add_stability = 0.02", 40)])

E(59, "The Line Holds", "peace", "Provisional gameplay",
  "an alternative outcome to the official chronology, in which the war ends with Erusea's surrender in 2005", [
    """The fighting has stopped without a decision, or never began. Erusea's army and its neighbours' face each other
    across a line drawn by the armistice or by the accord: on the maps it is a dotted line, on the ground it is
    wire, trenches, watchtowers and an empty field that nobody farms any more.""",
    """Nobody has agreed to call the line a border. The armistice commission meets monthly and settles incidents:
    a patrol that strayed, a shot fired at night, a farmer who crossed to fetch a cow. The prisoner lists are
    exchanged and compared, and the names of the missing are read on both sides.""",
    """At home the armistice leaves everyone dissatisfied. Those who wanted the war won feel cheated. Those who wanted
    it never fought feel vindicated and bitter. The army stays on the line at a cost the treasury cannot sustain
    forever, and the reservists who man it want to go home to farms and factories that need them.""",
    """The government must decide whether to keep the line manned at full strength until a treaty is signed, or to
    thin it and send the reservists home to rebuild. Either choice is a bet on the other side's patience.""",
], [("Keep the army on the line.", "army_experience = 5", 60),
    ("Trust the armistice.", "add_stability = 0.02", 40)])

E(60, "The Long Armistice", "peace", "Provisional gameplay",
  "an alternative outcome to the official chronology, in which the war ends with Erusea's surrender in 2005", [
    """The armistice line has held for another year, and then another. The watchtowers are still manned. The wire is
    still there. But the field between the lines is being farmed again, by both sides, under an informal
    arrangement that the commission pretends not to know about.""",
    """The prisoners have come home. The missing have been counted, and the counting has ended, which is its own kind
    of grief. The reservists rotate through the line every two years and complain about the food, which the
    officers take as a sign that morale is normal.""",
    """In the capital the arguments have changed. The question is no longer whether the war will resume but what
    the armistice should become. Some deputies, officers and ministers want a treaty, a border and an end. Others
    want the line kept as it is, a permanent reminder of an account not yet settled. A few want the account settled
    by other means, and say so in public, and are watched.""",
    """An armistice that lasts long enough starts to look like a peace. Erusea must decide whether it wants it to
    become one.""",
], [("Seek a treaty.", "add_stability = 0.02", 50),
    ("Keep the line, and the account.", "add_war_support = 0.02", 50)])

E(61, "After the Megalith", "megalith", "Official",
  "ACES Chronicle, 2005 / 09.26. The handover of the directorate's records is provisional gameplay", [
    """The official chronology records that on 26 September 2005 young Erusean officers seized Megalith, and that ISAF
    destroyed it. In the days that follow, the directorate that answered for the fortress has nothing left to answer
    for but its records.""",
    """They fill a lorry: personnel files, budgets, engineering logs, the counter-intelligence reports that described
    the young officers' mood a year before they acted. The director delivers them to the provisional government in
    person and asks that they be kept, not destroyed. Somebody, the director says, will want to know how this
    happened, and the answer is in the files.""",
    """The engineers who built Megalith to bring down the fragments of Ulysses are scattered: some detained, some
    questioned and released, some simply gone home to towns where nobody knows what they did. Many of them still
    believe that the fortress could have been what they built it to be. The ruins say otherwise.""",
    """The provisional government files the records and does not publish them. Not yet. A country that has just
    surrendered has enough to explain. But the files exist, and in time they will be read.""",
], [("Keep the records sealed.", "add_stability = 0.02", 60),
    ("Open the records to the commission.", "add_political_power = -10\nadd_stability = 0.01", 40)])
