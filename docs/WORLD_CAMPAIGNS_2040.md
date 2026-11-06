# National campaigns, 1991–2040

Approval: the private user request of 6 November 2026, “PLEASE IMPLEMENT THIS
PLAN: National campaigns for everyone, 1991–2040, plus country-screen and
ultrawide UI repairs.” This supersedes the authored 2020 horizon as a target,
without rewriting the historical 1,028-focus approval or subsequent addenda.
**Implementation is in progress. The full world expansion is not delivered.**

## Coverage and accounting

`tools/world_campaigns/manifest.json` lists all 61 active countries and seven
legitimate emergent countries, with three allocations each: 1991–2005,
2006–2020, 2021–2040. Principal countries receive at least 240 definitions per
era, regional countries 120, and other active/emergent countries 80. The floor
is 22,920. PLH is excluded. Existing larger campaigns remain larger.

The frozen baseline records actual IDs and their imports at main `38c978d0`.
The resolver follows shared descendants, de-duplicates imports across trees,
and excludes orphan definitions and generic/regional fallback content from
national credit. Existing era attribution follows literal lower date bounds
and prerequisite ancestry; ambiguous inherited context stays an explicitly
documented accounting estimate, never a canon/reachability assertion.

The six Usea Depth PRs #77–#82 are preserved as reservations with exact heads
and budget receipts. A reservation does not increase `delivered_count` or
decrease `remaining_actual`. `unreserved_authoring_gap` is a separate planning
figure. Regenerate with `python -B tools/world_campaigns/coverage.py`; use
`--check` in validation. Never recapture the frozen baseline to erase debt.

## Delivered opening contract: Sotoa and Central Sotoa

Sotoa has 240 focuses in 24 original discussions; Central Sotoa has 80 in eight.
Each discussion opens a choice among three specific programmes, each with a
three-focus development path. There are 32 national choice events, three
bilateral request events, 101 decisions, six recurring original staff members,
and 36 original technical insignia/scene masters plus 18 compact row icons. The exact ID/source ledger
is `tools/world_campaigns/sotoa_content.json`; authoring rows are `content.py`.

Sotoa's initial alternatives are civilian republic, strategic state and military
ascendancy. Other dilemmas concern courts, appropriations, apprenticeships,
delivery liabilities, supplier independence, freight bottlenecks, district
distribution, fuel rotation, pilot instruction, airworthiness, dispersal,
reservists, field repair, command authority, merchant crews, coastal reporting,
fleet sustainment, liaison, secure networks, procurement safeguards, neighboring
governments, Central Usea and bounded relief. Choices do not replace inherited
leaders or governments. Their receipts persist for later authored consumers.

Central Sotoa's distinct problems concern local consultation, technical
succession, small deliveries, a maintainable guard, a limited air service,
assistance conditions, materials skills and speaking to Sotoa independently.
No naval capability, unification, new border or canonical constitution is
inferred from the inherited map or country name.

Opening a discussion pays nothing. The first two selected focuses establish
its programme and preparation. A separate operation pays 25 PP plus 0.02
fictional billion through the real ready macro owner, then requires 90 days.
Disabled and experimental fiscal modes retain the PP cost and do not activate
or mutate macro accounts. Full-mode unready/arrears/insufficient cash fails
closed. Interruption retains costs and gives no completion result; a paid retry
is possible. The final focus requires the actual result and grants a 365-day
service. Sector alternatives replace one another rather than stacking.
Renewal after expiry pays the same costs. Effects recheck receipts and eligibility.
No factories, equipment, armies, manpower, borders, factions or wars are granted.

Sotoa can invite Central Sotoa and Central Usea; Central Sotoa can invite Sotoa.
The invitations cost 25 PP and expire after 45 days. Both original independent
governments must control territory, remain uncapitulated, and be at peace with
one another at dispatch and reply. Acceptance grants reciprocal +10 opinion for
one year; refusal and silence grant nothing. The domestic programme does not
require acceptance. Replies are once-only and invalid replies close harmlessly.

New campaigns select the dedicated trees. Existing generic/regional saves may
adopt them only while normal and continuous focuses are idle; completed content
is retained and no starting grant or fiscal account is reseeded. Bespoke saved
trees are never silently replaced. All UI changes are separately documented in
[the screenshot repair record](WORLD_CAMPAIGNS_UI.md).

## Source layers

| Content | Layer and exact reference | Affected IDs/status |
|---|---|---|
| Country identities, inherited states, forces and starting offices | Mod provenance: main `38c978d0`, the SOA/CSO histories and world registry | Read-only context; no geography/history edits |
| National dilemmas, all staff names, political routes, programme terms, dialogue and coefficients | Approved original fiction/provisional gameplay: private 6 November approval above; exact authoring row in `tools/world_campaigns/content.py` | `SOA_wc_e1_*`, `CSO_wc_e1_*`, `ac_wc_soa.*`, `ac_wc_cso.*`; source implemented, offline checks; native pending |
| Reciprocal invitations and opinion | Same private approval; `build.py:relations` | `ac_wc_relations.1`–`.3`, `*_wc_contact_*`; fictional, not official treaties |
| Insignia and scene diagrams | Original procedural artwork: `build_art.py`; assets manifest records byte hashes and dimensions | `GFX_*_wc_*`; geometric primitives, no borrowed pixels |
| 2029 Sotoa–FCU conflict | Official ACES product synopsis, https://acecombat.jp/en/product/ | Future owner pending; not established by opening focuses |
| Electrosphere organizations/chronology | Official ACES Chronicle, https://acecombat.jp/en/chronicle/ and https://acecombat.jp/en/chronicle/details/ | National/corporate integration pending; no new tags/partition |

The staff are original fictional supporting characters, not official politicians,
portraits or replacements for inherited 1991 officeholders. Joker 1's separate
uncompiled outline is untouched. Neither a future target nor an inherited
territory supplies missing official history.

## Validation and remaining delivery

`test_campaigns.py` executes all 96 opening programme alternatives against the
actual macro and institutional owners, including exact payments, the timed
result, duplicate effects, arrears, an unready owner, disabled/experimental
rules, expired dialogues, ownership loss, capitulation, foreign refusal,
subjects, war, stale replies and idle-save migration. Other gates check emitted
references/localization, focus geometry, sprite bindings and deterministic
source/artwork generation. These are static/offline checks, not native parsing,
timer dispatch, rendering, balancing, AI or save serialization acceptance.

The remaining global era allocations, Sotoa/CSO later eras, shared 2029 war
owner and corporate-era systems remain pending in the manifest. The engine's
2065 cutoff is unchanged. Native work remains under #8; no game launch, normal
profile change, automatic merge or release is part of this content delivery.
