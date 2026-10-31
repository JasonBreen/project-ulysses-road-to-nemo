# Faction source and adaptation record

Private scope reference: the user conversation supplied with the 25 October 2026 delegation requests joinable diplomatic/military blocs, internal country and corporate factions, applicable DLC integration and “sub pacts,” corrected from “subpack.” The delegation requires OEM inspection, 1995–2065 scope, strict Project Aces lore and noninterference with installed games.

## OEM reference actually examined

Project: JasonBreen/Millennium-Dawn-OEM. Existing local worktree ending sub-pacts-within-pacts-761d52, branch oem/intermarium-phase3, immutable HEAD **7dde07e71d**. Relevant files were clean against that HEAD. Reading the existing worktree does not use the Claude service. No OEM file, branch, setting or worktree was changed.

| Path | Inspected SHA-256 |
| --- | --- |
| LICENSE | 23EE78C8BAE49CF08EA2F0C84945C66B987EBE4520881FB51B3DAD4FB43D07C2 |
| common/scripted_effects/01_IMP_effects.txt | 0A57D21A1BB37F876D6C399B4E114BC1FD24A408B1E474BF9F33564AD813ABDF |
| common/scripted_triggers/01_IMP_triggers.txt | 4F2266A50717B937AFE53035895B2951B97521341FD96AD0EE885C94076880DE |
| common/decisions/IMP_decisions.txt | 75DFEB01FBC36A80572571DECE127B7B9DC1BF221A78FCE386CD565F740E0135 |
| events/IMP_events.txt | 7ABA18C5B4AC5D8CE4A1B13EE55B1BD6F5BB244D7D71BB52664A1918740FBE85 |

Also read common/ideas/IMP_ideas.txt and the attribution notice. OEM implements an Intermarium council inside NATO, full/associate eligibility, pending invitations, chair replacement/dissolution, epoch-bound formal votes, a shared fund and invested-member program stages, with research sharing at procurement stage 2.

The adaptation rewrites these concepts using ac_ IDs, multiple host-scoped councils, identity/epoch checks, explicit chair transfer, no global membership arrays, no shared fund, and investment consent. Native faction membership remains separate. No NATO/Earth tags, geopolitical claims, GDP figures, equipment, GUI or art were imported. Existing Ulysses fiscal state supplies optional treasury debits, and PP is the base fallback. No global technology group joins unrelated alliances.

Credit: Millennium Dawn and Millennium Dawn OEM contributors, including authors of the pinned Intermarium Council work. Source license: **Creative Commons Attribution-ShareAlike 4.0 International**; existing verbatim text at [MD-CC-BY-SA-4.0.txt](licenses/MD-CC-BY-SA-4.0.txt). The following new adaptation files are offered under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- New ac_factions*.txt files in the mod's game rules, triggers, effects, modifiers, on_actions, BOP, decisions/categories and factions directories.
- events/ac_factions_events.txt and localisation/english/ac_factions_l_english.yml.
- tools/Test-UlyssesFactions.py and tools/Run-UlyssesFactionChecks.ps1.
- docs/FACTIONS.md, FACTIONS_PROVENANCE.md and FACTIONS_VALIDATION.md.

Retain attribution, source revision, license link/text and modification notice when sharing an adaptation. This scope does not relicense inherited Ulysses, Paradox material, Project Aces names/art or other third-party assets. No endorsement or public distribution authorization is implied.

## Canon ledger

| Claim/IDs | Source layer and exact reference | Status |
| --- | --- | --- |
| ac_fac_ blocs, goals/rules and national interests | Provisional gameplay; private 25 October faction request above | Authored; no canonical alliance asserted; native unrun |
| ac_corp_ engineering/operations/board pool | Provisional gameplay; same private request; existing MIO roster without new company/history | Authored aggregate governance; named per-company content open |
| ac_sub_ membership/programs and ac_factions.1–.3 invitations | Provisional gameplay; same request and pinned OEM source above | Rewritten/scoped attribution; no NATO lore; native unrun |
| Existing FCU bloc, Belkan/Sapin outcomes and BOPs | Mod provenance at base 2c728e9625fd12d9474a40c6b811539369a603b8, corresponding history/event/BOP files | Preserved byte-for-byte |
| 1995 activation / 2065 horizon | User scope and existing engineering contract | No bookmark/end-date change or invented future history |

No new official Project Aces factual claim is needed by generic mechanics. Joker 1, future corporate history and unresolved geography remain outside this patch.
