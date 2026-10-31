### Changes

Emmeria and Estovakia currently have no dedicated campaigns, industry, supply networks or military rosters, and Estovakia's capital points to Nordennavic. This expansion makes both countries usable from the 1991 start and adds connected 1991–2005 campaigns about sustaining civilian recovery and military readiness.

The work is organised into three review packages:

1. **Playable foundation:** exact industry budgets, owned capitals and ports, internal supply networks, national forces, technology/variant prerequisites, production, replacement stockpiles, fuel and AI. Borders, province IDs, cores and inherited manpower remain stable. Placements, resources and force strengths are explicitly provisional gameplay calibration.
2. **Campaigns and presentation:** 108 focuses, 31 national policy spirits, 16 substantive narrative events, shared aid/recovery mechanics, original art, minor-country bookmark entries, established office portraits, and separately bounded scrolling country briefs.
3. **Integration and evidence:** generators, 64 focused regressions, independent CI steps, source/provenance ledgers, artwork gallery, exact candidate payload hashes and the separate native-acceptance checklist.

| Country | Focuses | Starting CIV / MIL / dockyards | Starting forces |
| --- | ---: | --- | --- |
| Emmeria | 54 | 24 / 14 / 6 | 12 divisions, 220 aircraft, 9 ships |
| Estovakia (`EVA`) | 54 | 20 / 16 / 4 | 14 divisions, 240 aircraft, 8 ships |

Each persistent tree contains 18 foundation, 18 warning/preparation and 18 recovery focuses, including exclusive alternatives. Most take 35 days; major commitments take 70. Civil preparedness and recovery remain distinct from military readiness. Chandelier content concerns unfinished research, redirection and civilian technical value; no operational strategic weapon or later war is added.

The bilateral owner validates the founding offer, separately paid 180-day services, three 60-day deliveries, 180-day cooldowns, monitored distribution, suspension, interruption and renewal. Conditional Emmerian policy requires an audit; Estovakian self-reliance withdraws cooperation. The sanctions review follows actual policy and completed work. Audited distribution, two monitored services, recovery of at least 40 and a live accord can earn an alternate outcome; later verified reform can lift sanctions.

The 2004 consultative bureau supports civilian coordination, with an optional Nordennavic invitation. It creates no merged state, forced faction or border changes. Anea owns its variables and leaves the existing Belkan/Usean war, faction and special-project owners intact. Fiscal and faction rules can each be disabled. Old saves receive eligible future content without retroactive armies, factories or preparedness, and opt into the tree after their active generic/continuous focus has ended.

Artwork includes 108 distinct focus compositions, eight original narrative illustrations, two independent original loading scenes, all spirit/category artwork and office cards using established flags. The ten image-generation masters, full prompts, hashes, frame/alpha contracts and reproducible packaging are retained. The AC8 portrait collection remains separate from 1991 governments.

### Validation

All **22 recorded static/offline groups passed**, including the existing campaign, economy, faction, aftermath, Continental War, supporting-country, special-project, interface, briefing, typography, generated-output, map/reference and asset checks.

- New focused suites: **64 tests** — foundation 11, campaigns 8, systems 21, integrated routes 5, artwork 8, presentation 11.
- Foundation geometry is derived from the actual province raster; all BBA/legacy aircraft and MTG/legacy navy combinations are checked. Effective technology/module definitions were inspected against the installed read-only reference.
- Strict authored assets: **5,081 sprite definitions, 934 focus bindings, zero missing texture references**.
- Effective repaired-screen dependency audit: zero missing dependencies or conflicting sprite definitions, including the new country-history scrollbar. The frontend extension certifies that control, rather than the entire unchanged frontend.
- The baseline/installed-reference no-vanilla comparison passed. Generated output and full-diff whitespace checks pass.
- Delivered DDS, manifests and bindings reproduce exactly under CI's Pillow 11.3.0. Review PNGs compare identical pixels across compression-library versions.

Commands, logs and payload hashes are in [the acceptance record](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/evidence/anea/ACCEPTANCE.md) and [static results](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/evidence/anea/static-results.json). CI is configured to test each new suite independently; final run status is available in this PR's checks.

### Dependencies and scope

Based on merged PR #29 at `cf8fec41abe5080b1af66eb86189b35c7af522f6`. The ordinary installation, launcher playset and user saves are not synchronized. No release is published or merge requested by automation. Related tracking remains #4, #5, #6, #7 and #8; this PR does not close their remaining acceptance work.

The optional installed Mod Builder was opened for a scratch check, but window capture failed twice. No import/export or project edit occurred. Repository authoring remains reproducible without it. All desktop interaction stopped when the user requested their PC back; subsequent work was headless.

### Runtime status

**No native HOI4 launch was performed for this expansion.** Starting-force execution, actual supply/fuel, GUI rendering, AI selection, natural progression, balance and engine save serialization remain unverified. Offline preferred-choice fixtures and state copies are not native campaign or save/load evidence.

The separate acceptance checklist covers both countries, the three display configurations, all available aircraft/naval DLC combinations, historical and alternate aid/sanctions routes, interrupted partners, 2005/2006 assessments and natural checkpoints through 2005. PR #29's remaining final-candidate native gaps stay separately recorded.

See [the expansion ledger](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/ANEA_EXPANSION_LEDGER.md), [foundation](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/ANEA_FOUNDATION.md), [campaigns](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/ANEA_CAMPAIGNS.md), [artwork](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/ANEA_ART.md) and [gallery](https://github.com/JasonBreen/project-ulysses-road-to-nemo/blob/codex/anea-burden-of-recovery/docs/evidence/anea/artwork-gallery.html).
