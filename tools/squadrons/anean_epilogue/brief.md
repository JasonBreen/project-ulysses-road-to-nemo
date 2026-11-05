# Anean continuations, 2015-2016: writer brief

Locked planning brief for two six-chapter epilogues under
`epilogue_contract.py` (namespace `ac_sqa`). Original supporting fiction, not
official lore. Each continues one of the pinned initial stories, which is read
and never edited:

| Host | Epilogue | Base | Continues |
| --- | --- | ---: | --- |
| EMM | `open_corridor_after` | 100 | *The Open Corridor* (`tools/squadrons/chapters/EMM.json`): Anika Reeve, Jonas Mercer, Sera Vale, Dario Keene |
| EVA | `last_serviceable_after` | 200 | *The Last Serviceable Aircraft* (`tools/squadrons/chapters/EVA.json`): Nadia Orlov, Pavel Kresin, Vera Dolin, Milan Sarek |

The original stories end around 2005 with one of three recorded personal
conclusions (trusted, compromised, fractured). An epilogue is admitted only
for the conclusion the player actually reached, ten years later, as the
Emmeria-Estovakia War (2015-2016) begins or is avoided. The four are now in
their forties or older: instructors, coordinators, a maintenance chief who
trains others.

## Hard rules (enforced by `epilogue_contract.py`)

- `cast_by_ending`: `trusted` keeps all four (in the original order);
  `compromised` permits whoever that conclusion leaves working together;
  `fractured` permits at most two, chosen from the original fractured ending
  (who still speaks to whom). A conclusion's scene may name only its permitted
  cast. Callbacks and option text are shared by every conclusion, so they may
  name only the cast every conclusion permits.
- Six chapters, ids 1-6, `earliest` ordered, at least 35 days apart, between
  2015.4.20 and 2016.12.31.
- `texts` has exactly three scenes per chapter, keyed `trusted`,
  `compromised`, `fractured`, each at least 80 words (aim 100-130), each
  continuing that conclusion's relationships honestly: the trusted four can
  still disagree; the compromised four still keep a private folder; the
  fractured pair are not reunited, though they may find one honest exchange.
- `contexts`: one or more `{id, trigger, text}` national paragraphs (at least
  40 words, naming no cast member) plus a `default_context` (at least 40
  words) used when none matches. The first matching context is shown after the
  scene. Triggers may use only `has_capitulated`, `has_war`,
  `has_war_with = <counterpart>`, `ac_sq_air_capable`,
  `has_global_flag = <published ac_eew flag>`, `NOT`, `OR`, `AND`.
- Two or three options per chapter: `label`, `reply` (at least 8 words), unique
  `flag`. Options record personal choices only; there are no scores, rewards
  or national effects. At least three later chapters carry a `callback`
  `{flag, text}` recalling an earlier epilogue choice (at least 12 words).
- ASCII only; the same forbidden official names as the southern brief
  (`tools/squadrons/southern/brief.md`), and no cast from any other story.
- `scene_subjects`: three wide grounded scenes (slot 1 -> chapters 1-2,
  slot 2 -> 3-4, slot 3 -> 5-6), at least 30 words each, under the same art
  rules: no airborne combat, explosion, readable text, insignia, flag,
  identifiable aircraft or landmark. Portraits are the original masters.

## Useful published flags

`ac_eew_started` (Estovakia declared war, 2015), `ac_eew_declaration_withheld`
(the declaration was withheld), `ac_eew_route_divergent` (Estovakia took the
negotiated road; no war), `ac_eew_route_unreachable` (the civil war was still
running), `ac_eew_stage_gracemeria` (Gracemeria, Emmeria's capital, fell),
`ac_eew_stage_liberation` (Emmeria retook it), `ac_eew_stage_coup` (the
Estovakian coup), `ac_eew_ceasefire_signed`, `ac_eew_emm_fallen`,
`ac_eew_eva_fallen`, `ac_eew_outcome_emmerian_victory`,
`ac_eew_outcome_estovakian_victory`, `ac_eew_outcome_ceasefire`.

Content rules: all principals live; no official character, unit or weapon as a
character; officials unnamed; no battle won on the page; the story owns no
outcome, so a scene must be true whether or not the war came, and the
national paragraph carries the difference. Estovakian characters are people,
not villains; Emmerian characters are not saints.
