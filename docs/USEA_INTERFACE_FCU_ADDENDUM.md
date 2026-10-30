# Screenshot, FCU and starting-government addendum

User direction: 30 October 2026. Implementation base remains verified main
`8f503d1de6b434031fcb110a6dd1dd7f26622a78`, rechecked against the remote during
this repair pass. All statements below describe the candidate source; native
acceptance is separately recorded in `evidence/usea-expansion/ACCEPTANCE.md`.

## Starting governments and provenance

The [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/)
identifies Robert Sinclair as FCU president at ISAF's founding on 22 August
2003. It does not establish a 1991 term. The user explicitly approved Sinclair
at the 1991 start with that earlier term labeled provisional mod chronology.
`FCU_robert_sinclair` is recruited in FCU history, has a democratic/centrist
gameplay role, no invented biography or trait bonuses, and an office image
using the existing FCU flag. This is separate from the later AC8 portraits.

The user also approved office leaders where a 1991 individual is unknown.
The audit covers 69 histories: 18 retain an existing active leader setup; 51
missing roles receive Sinclair plus 50 office representations. The row ledger
is `tools/usea_expansion/leaders.json`. Offices represent government in the
engine; they do not assert a newly invented council, person or constitution.
Fifty images retain an existing national flag. Seterano (SET) has no shipped
flag, so its image is a labeled office card, not a new flag or coat of arms.
New-campaign history recruitment never replaces a saved leader on startup.

| Claim | Source layer | Evidence | Status |
| --- | --- | --- | --- |
| Robert Sinclair is FCU president in 2003 | Official | ACES Chronicle, 2003 / 08.22 | Source-verified |
| Sinclair leads FCU in January 1991 | User-approved provisional gameplay | User reply: “Use Sinclair; label the 1991 term provisional” | Implemented; native start pending |
| Unknown 1991 officeholders use office representations | User-approved provisional gameplay | User reply: “Use office leaders where the individual is unknown” | 50 roles implemented; no invented biographies |
| Existing identities and flags | Mod provenance | Main 8f503d1 country histories, characters and flag assets | Retained; source hashes in leader asset manifest |

## Central Usea's choices

FCU retains 54 focuses and all existing IDs. `fcu_content.py` refines the
shared authoring rows with these country-specific choices:

| Choice | First path | Second path | Later consequence |
| --- | --- | --- | --- |
| Contribution formula, `ac_expansion.12` | Equal-member compact: stability +4%, daily PP -0.08 | Needs-based fund: construction +4%, consumer-goods factor +2%, stability -1% | Coalition-burden review eases pressure and builds confidence, or accelerates recovery at a war-support cost |
| Transport allocation, `ac_expansion.13` | Protected convoys: supply consumption -4%, war support -2% | Dual-use reserve: planning speed +8%, consumer-goods factor +1% | Transport-board and escort rewards read the saved choice |
| Settlement, `ac_expansion.14` | Permanent recovery secretariat with an enduring civilian cost | Release the reserve for immediate recovery and stability | Follows the owning victory, defeat, armistice or avoided-war outcome |

The first two choices each unlock a mutually exclusive concluding focus.
All four combinations can reach the opening assessment. The later liaison
rotation and common air picture are one-year programmes with costs. Policies
survive the tree handoff; answered event options cannot replay. Nineteen spirits
now serve the five-country package, including FCU's four additional policies.
No new faction, territorial settlement or war owner is introduced.

FCU mediation now calls the owning `ac_ucw_offer_mediation` effect in the
Continental War generator. Both governments must remain independent,
uncapitulated and at peace with each other. A 30-day pending mandate prevents
duplicate offers. Replies revalidate both participants, consume the mandate
once, and give an invalid/expired offer a harmless closing option. Refusal
leaves the readiness route to the allied-command branch available.

## Confirmed interface defects

Steam `20261030181039_1.jpg` shows the fiscal Overview, Budget and Credit pages
overlapping, a partial background, clipped button labels, an empty CNEA
category and news text behind its acknowledgment button. The before screenshot
is retained as `2560-economy-before.jpg`.

Fiscal controls are now direct children with individual page-visibility rules.
The opaque background is 860×640; action buttons are 160×40 with four frames;
the footer has separate bounds. At UI scale 1.25 the window occupies 1075×800.
When fiscal records are unavailable, an explanatory page replaces the account
controls. Opening the window does not activate fiscal mechanics or move money.

Country/news descriptions scroll within their own bounds. Engine control names,
option grids and minimize actions are preserved. Country-event illustrations
are 200×160; original wide masters remain available. Operative/leader event
layouts remain compatibility layouts outside this visual repair's claim.
All nine authored scripted GUIs are checked for their window, click-target
and dynamic-list template bindings. These source checks do not prove native
visibility, input handling or z-order.

## Defined vanilla-removal scope

All descriptors isolate decisions, national focuses, continuous focuses,
scripted GUIs and MIO organizations. Engine WWII country branches/overlays and
decision families no longer merge into those authored systems. Thirty-one
copied generic decisions and Swiss-only continuous focuses are retired. The
unfinished CNEA parliament placeholder is hidden and has a readable name.

The mod's Osean congress, Belkan Excalibur, custom decisions/missions, generic
MIO parents, faction owners and project owners remain. All authored mission
references and MIO parent references resolve after isolation.

Removing crisis decisions alone would strand draft-dodging, strike and mutiny
penalties. Generic political/crisis event IDs are therefore retained as hidden,
non-random harmless handlers. A bounded startup cleanup removes only the nine
retired crisis spirits and their three missions. It changes no government,
territory, focus progress or treasury and pays no reward. Queued old crisis
events call the same idempotent cleanup. The rest of engine on-actions/events
is not replaced wholesale; no claim of a complete engine-mechanic rewrite is made.

The manifests `vanilla_cleanup.json` and `retired_event_contract.json` record
retired IDs, source hashes and preserved boundaries. Source archives/baseline
and the normal installed mod are not edited by these changes.
