# Usean partner national campaigns

This Package 2 content supplies persistent national programmes for San Salvacion,
Amber, Ugellas and Delarus. It depends on the Package 1 world foundation,
institutional-capacity owner and fiscal compatibility API. It does not replace
those foundations or the existing Continental War owner. Native acceptance is
pending; the offline evidence below must not be read as a game playtest.

## Delivered authoring budget

| Country | Persistent focuses | Four acts | Enduring policy alternatives | National choice events | Decisions |
|---|---:|---|---:|---:|---:|
| San Salvacion | 72 | 18 + 18 + 18 + 18 | 8 | 6 | 15 |
| Amber | 60 | 15 + 15 + 15 + 15 | 8 | 6 | 13 |
| Ugellas | 48 | 12 + 12 + 12 + 12 | 8 | 6 | 15 |
| Delarus | 48 | 12 + 12 + 12 + 12 | 8 | 6 | 11 |
| Total | **228** | Administration / preparedness / response / settlement | **32** | **24** | **54** |

There are four further FCU reply events, one per national offer. Mutually
exclusive alternatives are included in the counts. Each country chooses one
policy from each of four pairs and one of two settlement routes. The final
assessment accepts either settlement route. All four trees are persistent;
there is no new tree handoff that could erase completed policy choices.

Routine focuses take 35 days. Enduring policy commitments and concluding
service milestones take 70 days. The three service indices per country grant
bounded, gradually earned capabilities with a continuing consumer-goods factor
cost. They do not print factories, money or equipment. Programme milestones
also unlock concrete national services, raise finite capacity limits, or reduce
the institutional cost of subsequent authorisations.

## Four different service systems

- **San Salvacion:** the continuity network and civil protection service renew
  for 180 days at a funded cost. A project-burden review reads the existing
  Stonehenge state and supports local continuity after the complex is lost. It
  never constructs, transfers, activates or destroys the project. Relevant
  focus work must first authorize the network, protection and review.
- **Amber:** a funded reserve service earns one spare slot after completion.
  A domestic transport service, domestic reassignment, or founding FCU offer
  spends a recorded slot. Completed service milestones raise the funded ceiling
  from two to six. Refused, expired or invalid offers return a committed slot
  once, while political, institutional and fiscal costs remain spent.
- **Ugellas:** four different 180-day leases compete for two simultaneous
  slots; completed reserve milestones raise the limit to three and then four.
  Early release frees the selected lease's slot without refund or completion
  credit. A new lease still needs a new paid authorisation and an allocation
  interval. Dispersal, mobility, receiving and readiness provide different
  benefits and opportunity costs.
- **Delarus:** inspection completions create verified cases. A command service
  creates an outstanding obligation which survives its expiry or displacement.
  Each outstanding obligation adds a 0.2% consumer-goods factor burden. Three
  unresolved obligations block another command service. A funded verified docket
  consumes a case and an obligation and restores one institutional capacity;
  it does not erase or replace the owning national mandate.

All funded services cost 25 political power and two institutional capacity,
reduced to one after authorisation reform. The shared fiscal programme charge
applies only when `ac_econ_ready` is true: two legacy fiscal units or 0.002 full
economy units under the owning API. With the fiscal system disabled the
political, institutional, time and standing-modifier costs remain playable.
The completion effect rechecks eligibility and affordability immediately before
charging; no reward is granted by a stale decision button.

## Operational scopes and the focus-purpose audit

An independent review identified117 focuses whose original mechanical effect
was only an index increment: SNS42, AMB33, UGE20 and DEL22. These now contribute
specific, nonfungible capabilities to **29 curated operational scopes**:
SNS10, AMB8, UGE5 and DEL6. Each scope names the actual procedures it requires,
offers a distinct temporary benefit/opportunity-cost combination, and consumes a
finite national resource. The authoring table is `tools/usean_partners/scopes.py`;
its executable consumers are in `scope_rules.py`.

SNS spends verified continuity or protection records earned only from completed
national services. AMB spends a funded spare slot. UGE occupies one simultaneous
slot for90 days, competing with its longer leases. DEL spends an inspection case
that could instead close a command obligation. One operational scope may run
at a time, lasts90 days, and pays the usual programme cost. Expiry returns only
the occupied Ugellan slot; consumed records/cases/Amber slots are not refunded.
Capitulation or annexation interrupts the allocation and forfeits paid costs.

Examples include signed dispatch-chain inspection, staffed shelter-water
turnover, supplier replacement reserves, bounded depot reopening and verified
settlement appeals. Domestic and post-settlement scopes remain useful after a
refused or invalid foreign agreement. Warning-era capabilities cannot be
retroactively earned by bypassing expired preparation.

`purposes.json` records the primary consumers for all228 focuses and the exact
baseline/remaining counts. **Remaining sole-axis nodes: zero in all four trees.**
The source regression removes each of the117 required focus capabilities in
turn, proves its linked paid action is unavailable, executes that focus's actual
reward, and proves the same action becomes eligible. This establishes a real
consumer rather than crediting prose or a merely repeated flag as a purpose.

Each country can earn one bounded offer to FCU. Both participants must exist,
retain their own tags, remain independent and uncapitulated, and not be at war
with each other. The recipient has sixty days to answer. No focus depends on
acceptance. Acceptance grants limited existing-owner recovery work and a
reciprocal opinion modifier; it does not create or join a faction. Expiry,
refusal, war, subject status, capitulation and annexation close or suspend the
relationship. Returning countries do not revive a stale agreement or repeat its
recovery reward.

Verified annexation, immediate capitulation, subject and war-relation callbacks
also interrupt old offers before a rapid restoration can revive them. These
handlers preserve paid costs and only return Amber's already-defined pending
slot once. The [integration review](USEAN_PARTNER_INTEGRATION.md) records the
captured primary scope contracts, actual regressions and the limitation for
custom transitions that emit no observable callback.

## Calendar, outcomes and saves

Only the third preparedness lane requires the April 1996 warning. It bypasses
after the July 1999 boundary without awarding preparation. The other domestic
lanes remain useful when played late. The third response lane begins after
that boundary. Settlement work accepts the owning war-over or avoided-war state,
or a peaceful campaign after 2005 where no Continental War began. Independent
recovery and recovery under external constraints have distinct prerequisites;
an assessment remains accessible when prior work finishes after 2005.

Verified preparation is added once, after `ac_ucw_country_start` has initialized
the existing recovery and pressure variables. Its maximum effect is +6 recovery
and -6 pressure, followed by `ac_ucw_bound`. Ongoing service recovery also uses
the owning bound. This package never writes an outcome flag, faction, calendar,
project owner, border, core, leader, starting OOB or physical equipment.

Old saves preserve completed content. The national-tree adoption decision waits
for generic, regional and continuous work to finish through the owning
`ac_pol_previous_tree_idle` interface and uses `keep_completed = yes`.
Initialization preserves existing programme variables, skips expired 1991 and
warning events, and supplies no starting forces, industry or retroactive
preparation. Capitulation removes temporary services and active policy spirits;
earned policy choices return when the country can operate again. Outstanding
Delarusan obligations and inspection records remain records to resolve.

## Source ledger

| ID / subject | Source layer and exact owning source | Disposition |
|---|---|---|
| Warning-gated `*_up_*` preparedness lane; `ac_up.3/.13/.23/.33` | Official chronology: [ACES Chronicle](https://acecombat.jp/en/chronicle/details/), 1996-04-20 entry | The FCU impact announcement supplies a date gate; the national administrative response is original gameplay. |
| Crisis boundary and preparation accounting | Official chronology: same page, 1999-07-08 entry | Used as the inherited Ulysses boundary; no invented precise damage map or casualty figure. |
| SNS project-burden and liaison focuses/review | Official chronology: same page, 1998-06-19 and summer 2003 entries | The chronology places Stonehenge in San Salvacion. National support procedures are authored; project ownership remains inherited. |
| Settlement assessments and differentiated recovery | Official chronology: same page, 2005-09-19 and 2005-09-26 entries; implementation: `common/scripted_triggers/ac_ucw.txt` and `common/scripted_effects/ac_ucw.txt` | Official chronology informs the historical route. Avoided war, Erusean victory and armistice remain established gameplay alternatives owned by the existing system. |
| Existing country tags, coalition and leaders | Mod provenance: `common/country_tags/00_countries.txt`; `history/countries/{SNS,AMB,UGE,DEL,FCU} - *.txt`; `common/characters/DEL.txt`; `common/characters/ac_starting_governments.txt` | Preserve the inherited Clarkson and government-office identities. Inherited 1991 coalition membership is a mod arrangement; SNS membership is not recast as a new official neutrality claim. |
| Every `SNS_up_*`, `AMB_up_*`, `UGE_up_*`, `DEL_up_*` focus and programme; `ac_up.1–6/.11–16/.21–26/.31–36`; offers `.101–104` | Original provisional gameplay: `tools/usean_partners/content.py`, `programmes.py`, `narrative.py`, `build.py` | All domestic offices, compacts, choices, service indices, policy modifiers, event incidents and balances are authored fiction/mechanics, not additional official history. |
| All new focus, idea, modifier, decision and category textures | Original code-native artwork: `tools/usean_partners/build_art.py`, per-focus subject pairs in `content.py`, existing editable glyph geometry in `tools/usea_expansion/build_art.py` | No downloaded official art, installed-game pixels, invented portraits, baked focus captions or added watermark. |

The new content's official dependency is deliberately narrow. Amber, Ugellas
and Delarus do not acquire invented official domestic chronologies. Detailed
source and implementation notes stay here rather than expanding game text with
citations. The inherited event illustration is reused for these national
administrative events; new squadron story art belongs to the separate narrative
package and is not claimed as delivered here.

## Artwork and reproduction

The package includes **311 RGBA DDS textures**: 228 distinct 96×96 focus
compositions, 32 enduring policy, 10 temporary programme and29 operational-scope images plus four
national modifier images at 75×75, and eight category/decision textures at
100×100 and 32×32. Every texture has one deliberate frame. Focus shine bindings
reuse their matching composition. Country frame geometry, subject matter and
supporting instruments distinguish the content. Transparent apertures are
recorded, rather than inferred from the file extension.

`tools/usean_partners/assets.json` records dimensions, frame width/count, alpha
extrema, sprite, SHA-256 and authoring-source hashes. `focus_art.json` maps each
focus title and semantic subject pair to its rendered composition. Editable
geometry and tables are the artwork source. Use Python 3.12 and the CI renderer
pins (`Pillow==11.3.0`, `numpy==2.2.6`); other Pillow versions can produce
different raster bytes.

```powershell
python -B tools/usean_partners/build.py
python -B tools/usean_partners/build_art.py
python -B tools/usean_partners/build.py --check --require-dependencies
python -B tools/usean_partners/test_content.py --require-dependencies
python -B tools/audit_visual_dependencies.py --strict-all
```

The source-art [contact sheet](evidence/usean-partners/focus-contact-sheet.png),
[operational-scope sheet](evidence/usean-partners/scope-contact-sheet.png)
and [filterable review gallery](evidence/usean-partners/artwork-gallery.html)
are packaged alongside the assets. Source rendering has been inspected.
Native node states, zoom/search, detail windows and readability at all required
display configurations remain pending an authorized isolated native test.

## Integrated owner review

The [combined review](USEAN_PARTNER_INTEGRATION.md) records execution against the
actual fiscal and institution owners, source tree priorities, Erusean/world
generator composition and the paid-spirit civil-war inheritance guard. Retained
pre-integration evidence describes its original component checkpoint; the new
integration results report the combined candidate separately. Native acceptance
and remote exact-head CI remain distinct.
