# Southern squadron stories: writer brief

Locked planning brief for two new original supporting stories, admitted under
`story_contract.py` (`southern_story_v1`). They are **original supporting
fiction**: incidents, dates, dialogue and personnel are authored; they are not
official ACE COMBAT history and claim no official biography. They continue the
house style of the eight existing stories (`tools/squadrons/chapters/*.json`):
quiet, specific, interpersonal scenes about how four people keep faith with one
another and with the truth, told in plain past-tense prose without melodrama.

| Host | Story | Base | Cast (id: name, role) |
| --- | --- | ---: | --- |
| AUR | **Kept in Repair** (`kept_in_repair`) | 900 | `ciro_avellan`: Ciro Avellan, pilot; `lucia_ferro`: Lucia Ferro, wingman; `ines_carvalho`: Ines Carvalho, crew chief; `hector_mendaro`: Hector Mendaro, coast and airfield controller |
| LEA | **Orders in Two Hands** (`orders_in_two_hands`) | 1000 | `mateo_salvaterra`: Mateo Salvaterra, pilot; `noemi_arcos`: Noemi Arcos, wingman; `gabriel_tenorio`: Gabriel Tenorio, maintenance chief; `sofia_landa`: Sofia Landa, controller and operations clerk |

## Hard rules (enforced by `story_contract.py`)

- Twenty chapters, ids 1-20, `earliest` dates (`YYYY.M.D`, no leading zeros)
  ordered, at least 35 days apart, inside the act for that chapter:
  chapters 1-5 in 1991.1.1-1999.12.31, 6-10 in 2000.1.1-2008.12.31,
  11-15 in 2009.1.1-2019.6.30, 16-20 in 2019.7.1-2020.12.31. Chapter 1 is
  `1991.1.1`.
- Every scene (base `text`, `capitulated_text`, each `condition_variants[].text`)
  is at least 80 words; aim for 100-140. Twenty distinct titles.
- Two or three options per chapter. Each option: `label` (a first-person or
  imperative choice, under ~12 words), `reply` (one or two sentences, at least
  8 words, showing what the choice does to the people), `flag` (unique
  snake_case, 3-40 chars, never reused in the story), `cohesion` and
  `credibility` both non-zero integers between -8 and 8. Choices trade privacy,
  loyalty and comfort (cohesion) against an honest shared account
  (credibility); make both directions tempting. The ending is trusted when both
  scores end at 65 or more (start 50/50), fractured when cohesion ends below 45,
  otherwise compromised; all three must be reachable.
- At least twelve chapters (aim for 15-17) carry a `callback`
  `{flag, text}`: `flag` is an option flag from an earlier chapter, `text` one or
  two sentences (at least 12 words) recalling that earlier choice. Callback text
  is shown in every context of its chapter, so it must not assume a war.
- Options and callbacks are shown in every context of their chapter, so their
  wording must make sense in peace, in war and after a capitulation.
- Three endings in the order trusted, compromised, fractured, each at least 100
  words (aim 130-160): personal assessments of the four, never a national
  victory, defeat, peace treaty, occupation or border.
- Each of the four first names appears in at least five chapters' scenes.
- ASCII only: straight quotes, `--` not em dashes, no accented letters.
- Never name: Gryphus, Talisman, Shamrock, Lampert, Navarro, Gaspar, Varcolac,
  Cuervo, Nemo, Mobius, Scarface, Garuda, Galm, Razgriz, Strigon, Pasternak,
  Antares, Gleipnir, Archelon, Nevera, Meson, Chandelier, Arkbird, Stonehenge,
  Megalith, Excalibur, Aigaion, Kei, Nagase, Bartlett, or any cast member of the
  other stories (listed by `story_contract.other_cast_names()`).

## Content rules (reviewed, not all machine-checked)

- All four principals remain alive. A loss may happen outside the four.
- No government leader, general or official squadron appears as a character;
  officials stay unnamed ("the minister", "the base commander", "the new
  commander"). No national leader is appointed or replaced by the story.
- The stories never fight a battle on the page as a victory: flying, if any, is
  training, weather, rescue, ferry or patrol seen from the cockpit or the
  radio room, and only in a variant gated on `ac_sq_air_capable = yes`.
- The story owns no outcome. A base `text` must be true whatever the national
  record did; wartime and occupation scenes go in `condition_variants` that read
  the published record. Leasath's "years of exploitation" is Leasath's stated
  claim, voiced by Leasathian characters as their view, never asserted by the
  narration. Neither story glorifies invasion or demonises ordinary people on
  either side.
- Places: you may name the capitals Griswall (Aurelia) and Alendal (Leasath).
  Bases, towns and coasts stay unnamed ("the southern field", "the coast
  station", "the hill airfield"). No real-world Earth place.
- The 1991 bookmark is the start: chapter 1 is an arrival, not a war.

## Conditional scenes

`condition_variants` is an ordered list of `{id, trigger, text}`; the first
matching trigger wins (after `capitulated_text`, when present, which wins when
the host has capitulated); the base `text` is the fallback. Triggers may use
only `has_capitulated`, `has_war`, `has_war_with = <counterpart>`,
`ac_sq_air_capable`, `has_global_flag = <published flag>`, `NOT`, `OR`, `AND`.
The context is frozen when the chapter is delivered. Useful published flags:

| Flag | Meaning |
| --- | --- |
| `ac_lcw_started` | Leasath's civil war began (2009) |
| `ac_lcw_ended` | it ended, any way |
| `ac_lcw_historical_end` | it ended in 2019 on its historical course |
| `ac_lcw_negotiated` | it ended by a negotiated settlement |
| `ac_lcw_prolonged` | it ran past 2019 (no 2020 war follows) |
| `ac_alc_started` | Leasath declared war on Aurelia (October 2020) |
| `ac_alc_declaration_withheld` | Leasath withheld the declaration (earned peace) |
| `ac_alc_route_unreachable` | the 2020 war could not happen (civil war still running) |
| `ac_alc_stage_overrun` | Leasath holds Griswall |
| `ac_alc_stage_griswall` | Aurelia retook Griswall |
| `ac_alc_stage_removal` | Leasath's commander was removed |
| `ac_alc_ceasefire_signed` | the scripted ceasefire was signed |
| `ac_alc_outcome_aurelian_victory`, `ac_alc_outcome_leasathian_victory`, `ac_alc_outcome_ceasefire`, `ac_alc_outcome_cessation` | how the war's record closed |

Examples: `has_capitulated = no has_war_with = LEA has_global_flag = ac_alc_started`;
`has_war = no has_global_flag = ac_alc_declaration_withheld`;
`has_capitulated = no has_war = no ac_sq_air_capable = yes` (a peacetime
training or rescue flight); `has_global_flag = ac_lcw_started NOT = { has_global_flag = ac_lcw_ended }`.
Chapters 16-20 should each carry two to four variants that cover the war, the
withheld or unreachable route, occupation and return; at least one late
chapter carries a `capitulated_text`. Act 3 chapters (2009-2019) should vary on
the civil-war record. Aim for 12-18 variants per story in total.

## Art subjects (metadata)

Art slots map chapters to eight scene masters: slot 1 -> chapters 1, 2, 6;
slot 2 -> 3, 7, 12, 16; slot 3 -> 4, 8, 13, 17; slot 4 -> 5, 9, 11, 14, 18;
slot 5 -> 10, 15, 19, 20; slots 6/7/8 -> the trusted / compromised / fractured
endings. Write chapters so each slot's single picture fits all its chapters.
Each scene subject (at least 30 words) is a grounded, wide 16:9 moment: no
airborne combat, explosion, readable text, insignia, flag, identifiable
aircraft type or recognizable landmark; faces may be partly turned away. The
loading subject (at least 30 words) is a calm establishing view of the
story's base. Portrait notes (at least 15 words) give the 1991 age band,
skin, hair, eyes, build and plain unmarked clothing, as in
`tools/squadrons/pacific_art/brief.md`. Bios start `1991 personnel file.` and
run at least 40 words: what the person wants and what they fear.

## The two arcs

**Kept in Repair (Aurelia).** A small southern air arm in a country that
prefers repairing things to replacing them and does not expect a war. Ciro
mends what he breaks before anyone sees it; Lucia promises everyone something
and keeps most of it; Ines keeps a ledger of what did not work and why; Hector
smooths the base's relations with the coast and the civil airport. Act 1:
arrival, thin budgets, borrowed parts, a sea rescue (variant). Act 2: the
modest modernisation, an injury, a family, a posting offered in Griswall. Act
3: the neighbour's civil war across the water -- refugees, an unscheduled
landing, a question of what to report. Act 4: the neighbour's war ends; in
October 2020 the invasion comes or does not; occupation, the last base,
the return. The personal question: can people who keep things working in
private also keep an honest public account of what broke?

**Orders in Two Hands (Leasath).** A Leasathian air base, 1991-2020, in a
country that tells itself a story of grievance against its northern neighbour.
Mateo wants to belong to something larger and fears being thought disloyal;
Noemi is wry and sceptical, with family on the other side of a line that has
not been drawn yet; Gabriel keeps aircraft flying for whoever pays; Sofia
writes the reports and learns what commanders want them to say. Act 1:
hardship and speeches. Act 2: the officers' politics, a petition, a promotion.
Act 3: the civil war (2009-2019) divides the base's loyalties. Act 4: the end
of the civil war; the October 2020 war on Aurelia, or its withholding; the
commander's removal; the account the four will give. The personal question:
whose orders, and whose account, when the country itself has two hands?
