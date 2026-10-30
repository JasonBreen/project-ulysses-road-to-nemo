# Five-country expansion development ledger

Implementation base: verified main `8f503d1`, 30 October 2026. The campaign arc
ends in 2005; completing its recovery assessments may extend beyond year-end.
This ledger distinguishes official chronology, inherited mod contracts
and newly authored alternatives. Native acceptance is recorded separately in
`evidence/usea-expansion/ACCEPTANCE.md`.

## Content inventory

| Country | Existing | Added | Total | Structure |
| --- | ---: | ---: | ---: | --- |
| Erusea | 24 | 30 | 54 | Separate 18-focus 1991 opening; 36-focus later tree |
| Central Usea | 21 | 33 | 54 | Separate 18-focus 1991 opening; 36-focus later tree |
| North Point | 15 | 15 | 30 | Island administration, readiness, neutrality and ISAF support |
| Recta | 13 | 11 | 24 | Existing postwar entry and settlement; deeper domestic recovery |
| Yuktobania | 14 | 16 | 30 | Industrial/logistics capacity, reform/intervention and civilian science |
| Total | 87 | 105 | 192 | Counts include alternative branches |

Each country receives an opening brief, two policy choices and a concluding
assessment in `ac_expansion`: ERU 1–4, FCU 11–14, NPT 21–24, REC 31–34,
YUK 41–44. The two choices concern administrative accountability and reserve
allocation; each has country-specific narrative and consequences. Nineteen
national spirits implement mutually exclusive administrative policies and a
standing recovery service. Five continuing recovery exercises cost 45 political
power and have a 180-day cooldown. They require an active owning recovery
system. No fiscal-system dependency is introduced.

New focuses default to 35 days. Major commitments use 70 days. Industrial
programmes grant bounded, one-use research bonuses rather than repeated free
factories. The durable civil policy trades stability for political attention;
the directive policy trades civilian confidence for organisation; the standing
service trades civilian capacity for lower supply consumption. Research,
experience, manpower, recovery and relief consequences are mixed across the
branches. Numerical balance is provisional pending natural progression tests.

`tools/usea_expansion/content.py` is the complete row-level ledger of new IDs,
prerequisites, coordinates, descriptions, costs, availability and rewards.
`focus_art.json` joins all 192 existing/new focus IDs to their artwork.

## Source layers

**Official chronology:** the established Ulysses and Continental War chronology
continues to use the [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/)
and [official superweapon chronology](https://acecombat.jp/en/chronicle/weapons/).
Exact dated citations and the inherited authoring decisions remain in
`USEAN_CONTINENTAL_WAR.md`: Ulysses, refugee closure, the Continental War,
North Point's ISAF headquarters, the 2005 settlement and Arkbird cooperation.
No additional historical claim is introduced by the new administrative trees.

**Inherited mod content:** 1991 governments, existing country tags and flags,
existing actor-tree IDs, Belkan aftermath and Recta's settlement remain owned
by their current scripts. Recta's political history is mod provenance, not a
new claim about the official chronology. The new artwork retains existing
flags, maps, named leaders and portraits.

**Authored alternatives:** every new opening institution, administrative
compact, contribution formula, domestic reserve allocation, policy tradeoff,
recovery office and assessment is provisional gameplay. Victory, defeat,
armistice and avoided-war additions follow the established owning outcome;
they do not assert another canonical outcome. Event descriptions include a
short framing sentence; detailed provenance stays here.

**AC8 artwork:** official promotional scenes and eight named portraits are a
separate presentation collection. They establish no 1991–2005 chronology or
leader assignment. Exact URLs, credits and source hashes are recorded in
`tools/usea_expansion/official_art.json`.

## Campaign and save contracts

The ERU/FCU opening trees receive selection weight only before 1 December 1999
and before the Usean calendar starts. The established calendar loads the
existing later tree IDs. Existing focus IDs, events and outcome flags remain
stable. Completed opening focuses and national policy ideas are not cleared.

`ac_exp_apply_opening` runs after the existing Usean initializer has established
its starting variables. It applies civil/logistics/readiness recovery and relief
pressure consequences once, then uses `ac_ucw_bound`. An old save with no
preparation flags receives no preparation reward. Re-entering initialization,
late loading or acquiring a preparation flag afterwards cannot replay it.

All 105 new completion rewards have once guards and revalidate their
availability at completion, including capitulation. New diplomatic publication
requires both countries to exist, remain independent and uncapitulated, remain
at peace with each other, and still have the Arkbird partnership. Domestic
branches do not require a foreign response to reach a conclusion. Faction,
war, territorial and special-project states remain with their owning effects.

Weekly narrative dispatch uses country-specific on-actions. Opening briefs
expire before the later calendar (Recta before 2000); the earlier policy events
retain their end-of-2005 deadline. The five concluding assessments instead
require their completion flag without a calendar cutoff. Erusea's ISAF-defeat
reconstruction chain takes 112 days after the settlement, so a 26 September
2005 start reaches its assessment on 16 January 2006, before the next weekly
dispatch and one-day event delay. This completes the existing recovery route;
it adds no post-2005 war arc. Sent and answered flags prevent repeat dispatch
and duplicate options. Capitulation eligibility still applies.
Ordinary old saves receive eligible future additions rather than replaying an
opening brief merely because the mod was updated.

## Interface and packaging decisions

Both normal and continuous detail views retain the required engine control
names, including the engine's `coninuous_focus_detail_view` spelling. Narrative
and rewards have separate scrollable bounds; prerequisites remain scrollable.
The engine focus-state GFX file is replaced by the generated compatible file:
an early-sorted additive file was insufficient in native testing. The focus
canvas, captions, detail panels, progress, search and continuous panel use
original navy/cyan artwork and readable DINish briefing text.

The initial 323 unresolved authored references in research, naval counters and
aircraft strips are replaced. The strengthened audit also found two progress
textures omitted by the former single-`texturefile` regex, and the engine GUI
dependency audit identified further research/scrollbar references. These are
explicitly bound to authored sprites. Shader dependencies are recorded and
remain engine functionality, while dynamic flags use the existing mod flags.

The original 35-tile main-menu background did not cover the ultrawide viewport.
It now uses the engine's dynamic background catalogue on an aspect-preserving
canvas and restores the selectable background control, including four official
AC8 images. Original illustration masters, named portrait sources, frame
metadata, packaging instructions and audit outputs are retained.

The later user-directed work on fiscal/event GUI failures, FCU policy choices,
starting leaders and inherited-mechanic removal is recorded in
[the implementation addendum](USEA_INTERFACE_FCU_ADDENDUM.md). This includes
the explicitly provisional 1991 Sinclair assignment and office representations;
the earlier description of unchanged leader assignments refers to the AC8
portrait collection, not those subsequently requested repairs.
