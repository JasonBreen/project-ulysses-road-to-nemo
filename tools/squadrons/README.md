# Original squadron campaigns

The six casts in `campaigns.json` are user-approved original supporting fiction.
They do not establish official individuals, replace national officeholders or
extend the protected private continuity. National governments, wars, territories
and special projects retain their existing owners.

Each host receives twenty core chapters, four recurring cast members and three
personal conclusions. Chapter choices persist as namespaced flags and bounded
cohesion/credibility values; callbacks use previous choices. A chapter is a scene
with people and dialogue, rather than another cabinet report or a flight-game
mission pretending to observe individual HOI4 airframes.

## Chapter source format

`chapters/TAG.json` contains `chapters` and `endings`. Each chapter has an integer
`id` (1–20), an authored `earliest` date, `title`, substantive `text`, and two or
three `options`. Each option has `label`, a narrative `reply`, a unique short
`flag`, and signed `cohesion` / `credibility` consequences within -8..8.
An optional `callback` has the short `flag` of a previous option and supplemental
`text`. Optional `war_text` or `capitulated_text` replaces the base scene only
under the corresponding actual host condition. They must not assert fixed war
outcomes, compulsory historical battles or a claimed exact Ulysses impact time.

Optional `condition_variants` supply a safe `id`, an actual owner-state `trigger`
and a substantive replacement `text`. They follow a capitulation continuation,
then take priority in source order before generic war/base text. Each event
captures exactly one text context and its callback at delivery, so its archive
cannot be rewritten by a later alliance, territorial or project change.

Dates and personal incidents are authored gameplay/fiction. Official chronology
anchors are recorded separately; preparation, war and recovery state is read
from the established campaign owners. Chapter-to-illustration slots are recorded
in the art plan. The last act remains eligible for a campaign already in progress
when prerequisite or calendar delays carry it beyond 2005. Late initialization
does not replay expired preparation or grant its rewards.
Late initialization after January1991 skips the opening dispatch. An unanswered
dispatch reservation expires once after30days and is marked missed without
applying its choice. A missed dispatch is not represented as a completed reading.

## Art sources

`sources/portraits/<id>.png` and its JSON record retain each original master,
exact prompt, generator, dimensions, hash and visual review. These are narrative
cast portraits, not government portraits. Keep the approved official AC8
collection separate. Sources are copied into the project; the generator cache
is not a build dependency.

Original narrative and loading compositions use the same source-record protocol.
DDS crop/frame bindings and reproducible packaging are separate from these
editable masters. Native appearance and gameplay remain untested while native
testing is paused.
