# FATO and South Belka: national campaign source ledger

This packet adds **54 FATO focuses and 42 South Belkan focuses**, with a persistent tree for each country, ten substantive scenes per country, consented equipment warrants, a finite civil docket and eight original narrative illustrations. It consumes the existing financial, institutional, release, war, faction and reconstruction owners. It does not introduce a war, a border settlement, a leader change or a force grant.

The implementation parent is `172b0726e0170012cc60650994ea3d3fe9c07551`: fresh verified `origin/main` `3810d1a`, the reviewed SNP source `ebf8ae8177ba58b2d227d83a7a65fe53c3794b3e`, and legitimate-release component `578db157220c38a1b0ece2e1470d2ad6eae902d0`. The separate release and SNP worktrees remain clean handoffs. LAND observations/equipment and later font work are not silently imported into this component.

## Source layers and boundaries

| Claim or authored material | Layer and exact reference | Affected content | Status |
|---|---|---|---|
| Belka sold northern territory to FATO on 29 August 1991 | Official context only: [ACES Chronicle, 1991 / 08.29](https://acecombat.jp/en/chronicle/details/), read 31 October 2026 | Context for existing border administration; `FAT_nat_border_book` and scene `ac_fsb.2` | Verified sentence; no sale, state transfer or map change scheduled here. The inherited January 1991 map already has its own territorial timing. |
| Belkan War began 25 March 1995; southern open cities were demilitarised on 1–4 June; the Lumen treaty ended the war on 20 June | Official context: [ACES Chronicle, 1995 / 03.25, 06.01–04, 06.20](https://acecombat.jp/en/chronicle/details/) | Existing Belkan events remain the owners; new national scenes observe current war/peace/subject status | Verified contextual dates do not establish a canonical South Belkan government, release footprint, constitution or post-2005 policy. |
| FAT's January 1991 states, capital, industrial placement, roster, law and character identities | Mod provenance: `history/countries/FAT - FATO.txt`, `common/characters/FAT.txt`, `common/ai_strategy/FAT.txt`, existing World/Legacy owners | All `FAT_nat_*`, national conditions and recipient eligibility | Preserved. Jaroslav Dvořák's inherited placeholder identity is not promoted to an official biography or term claim. |
| South Belkan collapse, treaty, subject, faction and reintegration routes | Mod provenance: `events/South_Belka.txt`, `events/Belka.txt`, `common/on_actions/ac_on_actions.txt`; release ledger `tools/release_foundations/README.md` | `SBK_nat_*`, `ac_fsb_*` cleanup | Preserved native operation signatures. No new territory, core, manpower, transfer fraction or faction permission. |
| South Belkan government-office identity | User-approved unknown-officeholder representation, inherited `SBK_ac_government_office` in `common/characters/ac_starting_governments.txt` | All new SBK content | Preserved; no invented individual, portrait or biography. |
| Administrative procedures, all 96 focus purposes, 20 dialogues, quantities, dates of later reviews, benefits and costs | Provisional authored fiction/gameplay: `tools/fato_south_belka/content.py`, `programmes.py`, `obligations.py`, `narrative.py`; per-focus `purposes.json` | `FAT_nat_*`, `SBK_nat_*`, namespace `ac_fsb` | Implemented source, separately validated offline; no official policy or chronology claim. |
| Eight scene paintings | Original imagegen artwork, eight independent retained PNG masters and exact prompts in `source/artwork/fato_south_belka/`; dimensions, transforms, hashes and sprite bindings in `tools/fato_south_belka/assets.json` | `GFX_ac_fsb_event_*` | Individually visually inspected; original anonymous fictional people, no leader portraits, text, flags, logos or added watermarks. |
| Focus, idea, category and compact row art | Original code-native technical compositions, `build_art.py` and existing original Ulysses glyph library | 96 distinct focus compositions and matching policy/case art | Pinned Pillow 11.3.0 packaging; this does not establish native scale/visibility. |

Every focus has an explicit purpose and a real consumer: policy, paid action, substantive dialogue or a permission used by a current eligibility condition. `purposes.json` records each ID, prerequisite group, exclusive alternative, duration, date, source layer and status. No sole-axis increment is used to pad the count. Shared regional36 focuses are separate and remain available to their other eligible countries.

## Campaign shape and pacing

| Country | Persistent tree | First act | Middle act | Renewal |
|---|---|---|---|---|
| FAT | `fat_national_campaign`, 54 definitions | 18 authorisations, with 1991/1992/1993 checkpoints | 18 obligations and domestic consequences, with 1995/1997/2000/2003 checkpoints | 18 reviews and conclusions, with 2006/2008/2010/2012–2013 checkpoints |
| SBK | `sbk_civil_recovery_campaign`, 42 definitions | 14 contemporary foundation focuses after legitimate release/adoption | 14 settlement-practice focuses from 1997/1999/2001/2003 | 14 renewal focuses from 2006/2008/2010, final assessment from 2013 |

The date gates are authored pacing choices. A later legitimate release gets contemporary civil work; it does not receive backdated 1995 relief. FAT's expired early briefs are archived and pay no retroactive preparation. All prerequisites must still be completed normally. Default focuses last 35 days and major commitments 70 days. Exclusive alternatives count in the definition totals.

`pacing.py` executes earliest legal focus schedules across all 24 exclusive-policy combinations, with the actual generated prerequisites and date conditions. This is a bounded source calendar test, **not natural progression or AI evidence**. Date waits are deliberate: paid domestic allocations, maintenance, institutional audits and eligible stock warrants continue between milestones. Native AI selection, affordability over a real campaign, competition with other mandates, player pacing and time spent in continuous focuses remain acceptance work.

The source schedules finish on 25 June 2013 for all sixteen FAT policy paths and 16 April 2013 for all eight SBK paths. The SBK calendar fixture starts on 21 June 1995 with a registered administration; it does not claim a naturally executed treaty route. They require 1,995 and 1,575 focus-days respectively, with at most 956 calendar days waiting for a later focus milestone. Those waits are not a claim of continuous focus content. The repeatable domestic systems remain available; their natural AI use and balance need native testing.

Both national trees have explicit exact-current-tag/original-tag selection guards and a continuous panel beside the tree's upper edge. Only FAT and SBK's regional-tree dispositions change. An existing save can adopt the new tree only through the real `ac_pol_previous_tree_idle` trigger. Selected zero-progress, progressing generic/regional and continuous focuses block adoption. Unknown bespoke trees are not overwritten. Completed content is retained; adoption grants no physical or fiscal start setup.

Resolved positions use prerequisite depth and separate act bands: every parent is strictly above its child, and no two nodes share a position. The offline review schematics are `tools/fato_south_belka/FAT-focus-layout.svg` and `SBK-focus-layout.svg`; they use real artwork and declared node positions with schematic spacing, not a reconstructed native screenshot. Hover titles describe each purpose. Civil-war reset is disabled for the persistent original-country trees; exact tag/original-tag guards reject clones.

## FATO: consented obligations and industrial allocation

The country has **one open-warrant slot**, expandable through earned focuses to two and then three. Pending and accepted warrants both occupy a slot. No fourth slot is possible. Offers name a fixed consignment: 300 infantry equipment, 150 in the smaller reserve alternative, 30 support equipment or 20 motor vehicles. These are provisional gameplay quantities, not historical production or assistance claims.

An offer costs 15 political power, one institutional capacity and the public programme fee. It lasts 30 days, or 90 after the consent clause, with a 180-day per-recipient/type request cooldown. Gebet, Recta and Osea receive decisions to accept, decline, request an earned joint inspection, or revoke an accepted permission before dispatch. Recta is absent at the 1991 start: its valid future cooperation depends on an existing legitimate release. No country is spawned to make a national branch work.

**Consent moves no equipment and grants no alignment.** Dispatch rechecks both exact identities, existence, independence, capitulation, bilateral war, live permission and stock. It transfers actual equipment using the installed primary `send_equipment` contract. The sender keeps at least 300 infantry, ten support or ten motor vehicles at home; the reserve-floor policy raises the infantry margin to 600. Delivery closes permission before any later attempt can repeat it. The receiving training benefit is for a completed physical shipment, not an ongoing faction guarantee. A joint inspection is a separate paid receiver choice, available only after both audit and inspection permissions are earned.

Responses use live decisions rather than queued diplomatic events, so an old reply cannot consume a later offer generation. Expiry, war, subject status, annexation, capitulation and invalid identity close unfulfilled permissions and free slots without a delivery award or refund. FATO's own supervision blocks foreign offers while leaving domestic maintenance, training, reception, repairs and production choices useful. Refusal permits a freshly paid domestic use of real stores when earned; it never mints compensation.

Industrial policies replace earlier policies in the same family. They exchange civilian construction, output, consumer requirements, stability and political discretion. Temporary extra shifts, rest, line continuity and skill retention share a mutually bounded shift family and real cooldown. Transport allocations reserve a civilian factory. There are no interchangeable political-power/factory reward chains and no hidden expansion of the physical production budget.

## South Belka: a finite civil docket

The campaign waits for **`ac_release_administration_registered`**, which the existing legitimate-release/adoption owner establishes. A dormant tag cannot initialise the campaign merely because the compiler knows its name. Both collapse routes and the two treaty footprints retain their original state/capital and transfer contracts. Civil scenes refer to present authority, not an assumed independence guarantee.

Six specific files can be opened: property, utilities, stores, security, resident access and archives. They have different resolutions and permissions. Opening costs ten political power, one institutional capacity and the public programme fee; a file holds one of at most two earned slots for up to 120 days. Resolution is a separate choice, normally costing 15 political power, two capacity, the programme fee and any listed real stores. Verified receipts and a checked common archive each save one capacity after payment. Local witnesses, security review, interim-service consent and standing work orders enable particular alternatives rather than a generic national score.

Property can protect possession or record an interim arrangement. Utility work can spend support stores on a verified repair or conserve current service under an earned interim procedure. Stores may be consumed for maintenance or sealed under inspection. Security can narrow a remit or fund supervision. Resident access remains useful on non-core treaty states without granting cores or population. Archive reconstruction can use earned witnesses or protect uncertainty. Their temporary benefits have explicit countervailing costs. Standing work orders lengthen **future resolved** utility/access arrangements; unfinished files receive no completion bonus.

Each resolved case permits **one costed appeal**, if earned. An appeal removes the previous arrangement before reopening the file, so benefits cannot stack. Expiry, occupation, capitulation and reintegration close current work without refund or completion. An obsolete file may close without an award. Closed unresolved work may later be opened at its full cost; a resolved file needs its unique appeal.

Osean technical advice is a separate limited-consent arrangement. Independent SBK, or SBK actually subject to Osea, may request it from eligible Osea. A country subject to another power uses the domestic inspection route. Acceptance costs the receiver political power and capacity and permits a 120-day technical visit, with a visible staffing burden. War, invalid status and interruption remove the active visit. Refusal leaves the paid domestic workshop inspection available. No advice changes a faction, subject relation, autonomy level or territorial settlement.

`south_belka.5` remains unchanged: BLK annexes SBK with the inherited troop-transfer setting. The verified `on_annex` ROOT-winner/FROM-annexed callback clears this campaign's cases, permissions and policies. It never blocks annexation. There is no removal of `SBK_demob_idea`: the inherited definition has no observed active application, so a fictional demobilisation reward would be misleading.

## Public accounts and save continuity

All new upfront cash uses `ac_econ_can_pay_programme` and `ac_econ_pay_programme`, with a fresh success check in full mode. The calibrated public fee is 0.002 abstract billion in full mode and two legacy fiscal units in experimental mode; those are separate game-unit calibrations, not an exchange rate. Disabled fiscal rules require no cash. Political, institutional, stock and national-modifier costs remain in effect.

Five removable standing administrative accounts each add **nominal GDP / 2000 annually** in full mode through `ac_macro_change_commitment`. The owner records the exact applied sum. A reconciliation subtracts its previous exact snapshot before adding the newly authorised amount; repeated weekly observations cannot duplicate it. Earlier legacy contracts and the public account's stocks remain owned by P1. Annual staff overhead is distinct from the one-time authorisation fee and from P1's separately selected national mandate.

Removal or annexation clears this campaign's standing flags. If land loss makes the macro account unready, the exact subtraction remains dirty and deferred until the same account is valid again. No treasury, debt, arrears, historical ledger or state GDP is seeded or rewritten by this national owner. A later release retains its completed content and can pay to authorise a standing account again. The latest earned governance policy in a family may be reinstated through a costed review; earlier superseded acts cannot stack their former policies.

Scene options recheck current identity, deadline, presence and their own pending/seen flags. Funded options have real costs and temporary policy tradeoffs. A low-resource country can close a scene without an award. Repeated, expired or interrupted selections are inert. Native event-window scheduling and save serialisation still require isolated acceptance.

## Artwork and reproducible delivery

`source/artwork/fato_south_belka/prompts.json` retains each exact creative prompt and original generation path. Eight independent PNG masters are retained byte-for-byte; none is a crop of another master. The deliberate mapping uses four paintings per country across its ten scenes. No national leader or canonical location is invented by those pictures.

`tools/fato_south_belka/assets.json` records master and compiler hashes, dimensions, alpha ranges, one-frame sprite bindings and packaging transforms. Narrative DDS images are 450×150, opaque, fitted with Lanczos and centered navy padding when needed. Focus art is 96×96 with transparent outer apertures; policy/case art is 75×75; categories are 100×100. **Decision-row art is independently packaged at 26×29**, never aliased to a category image. The global source reconstruction measures all three repaired row templates.

Use the CI-pinned Python/Pillow environment:

```powershell
python -B tools/fato_south_belka/build.py
python -B tools/fato_south_belka/build_art.py
python -B tools/fato_south_belka/pacing.py
python -B tools/institutions/build.py
python -B tools/world_foundation/registry.py --output tools/world_foundation/country_registry.json
python -B tools/decision_row_art/render_review.py
python -B tools/fato_south_belka/run_checks.py --broad
```

Every generator has a read-only `--check` mode. The runner checks every subprocess return code independently; the CI step cannot hide an earlier failure behind a later successful command. Primary-source hashes are checked separately when `--reference` points at the read-only installed game. `engine_contract.json` pins fifteen inherited owner sources and the other 67 institutional profiles. No engine-provided GUI closure claim follows from the authored-art audit alone.

## Acceptance status

See `docs/evidence/fato-south-belka/RESULTS.md` for exact source gates and receipts. This component is delivered for source review. CI has not been run on a published component branch because publication belongs to the parent integration task. **Native acceptance remains paused**, including 3440×1440 at 1.0, 1920×1080 at 1.0, 2560×1440 at 1.25, actual focus states/search/zoom/continuous panels, event picture/text crops, stock-model selection and delivery, financial precision, event windows, natural AI, war/peace/subject progression, reintegration and save/reload. Normal installation, profiles, user saves and the desktop were untouched.
