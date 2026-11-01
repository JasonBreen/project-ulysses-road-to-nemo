# Factions, internal councils and subpacts

The ac_fac_, ac_corp_, ac_sub_ IDs and ac_factions.1 through .3 events are provisional gameplay systems, not assertions of Project Aces history. The user requested joinable diplomatic/military blocs, internal country/corporate factions, applicable DLC integration and OEM-style subpacts. No canon alliance, border, country, company or future war was added.

## Campaign entry and player controls

The **Councils and charters** game rule defaults to enabled. Systems begin on 1 January 1995 and remain available through the existing 2065 horizon. The inherited 1991 bookmarks and every campaign outcome remain unchanged. Countries initialize on startup when eligible, or on their first monthly pulse after 1995/creation.

- **Alliance Diplomacy**: create a compact, invite independent countries, withdraw at peace, dissolve a player-created compact at peace, and use supported DLC actions.
- **National and Corporate Councils**: inspect/adjust domestic interests and corporate divisions.
- **Alliance Councils**: establish a subpact within a military bloc, invite full/associate members, transfer the chair, invest in programs, authorize them, leave or dissolve.

A charter costs 100 political power. Each invitation costs 25 and requires the recipient's consent. No geopolitical membership is seeded. Native diplomacy handles joining existing inherited blocs; their setup/rules are not rewritten. The native faction screen retains ordinary military participation, leadership and further upgrades. Scripted invitation/dissolution is restricted to charters created through the Ulysses decision; native template-picker creation continues through native diplomacy.

## Actual engine and DLC mapping

Read-only reference: HOI4 **Operation Postern 1.19.3.0.c01a (5632)**, Steam build **25205862**, from installed launcher settings and appmanifest. Installed descriptors and script documentation were examined. Installed files do not prove a running playset's entitlement/activation; runtime has_dlc is authoritative.

| System | Native interface actually used | Requirement and fallback |
| --- | --- | --- |
| Country bloc | create_faction, add_to_faction, leave_faction, dismantle_faction | Base engine. Creates a legacy named faction without NCNS; one native faction per country. |
| Expanded alliance | create_faction_from_template; custom manifest, goals and rules; initiative/influence | No Compromise, No Surrender (NCNS). Without it, legacy blocs and custom councils still function. No Earth templates/content/art imported. |
| Joint research/operations | set_faction_research_unlocked, set_faction_military_unlocked | NCNS. Parent leader authorizes each for 75 PP after a council establishes research/mobility. Further upgrades retain normal native costs. |
| Intelligence coordinator | Allied target country: set_faction_spymaster = yes | La Resistance and an existing target agency. No agency or substitute spymaster bonus is conjured without DLC. |
| Industrial workshop | Country every_military_industrial_organization; MIO-scope add_mio_funds = 25 | Arms Against Tyranny (AAT), a visible organization, corporate engineering >=40. 50 PP / 180 days. Without AAT, corporate policy modifiers still work; MIO actions are absent. |
| Civil/security mandate display | set_power_balance, add_power_balance_value | By Blood Alone (BBA). Generic BOP never assigned to BLK/SAP; active inherited BOPs preserved. Ranges add no duplicate bonuses. Without BBA, the influence panel/effects remain. |
| Country/corporate interests | Custom bounded influence and dynamic modifier | Base scripting. These are internal interests, not additional native factions or ruling ideologies. Corporate divisions form an aggregate governance council for participating firms; no per-company story/roster is asserted. |
| Subpact | Custom chair, identity/epoch-bound seats, consent and programs | Base scripting, inside an existing faction. Never creates a second native faction, calls war, transfers land or changes ideology. |

Primary installed references: common/factions/_documentation.md, templates/rules/goals, documentation/{effects,triggers,dynamic_variables,modifiers}_documentation.md, and the four DLC descriptors. The [official NCNS release](https://www.paradoxinteractive.com/media/press-releases/paradox-interactive/win-the-pacific-war-in-major-hearts-of-iron-iv-expansion) confirms expanded faction rules and alliance goals. Installed 1.19 scripts provide exact syntax.

## Internal influence and corporations

National interests start at civil administration 40, security 35, industry 25. Corporate divisions start at engineering 40, operations 35, board 25. Each pool totals 100. A 40 PP support decision transfers up to five from each donor to the selected interest. Pools remain integral, bounded and reversible at zero. Each pool has a separate 30-day cooldown.

Per influence point: civil stability +0.05%, security organization +0.03%, industrial construction +0.03%, corporate engineering research +0.02%, operations efficiency growth +0.05%, board factory output +0.02%. Any interest above 70 imposes one 5% political power gain penalty. Coefficients are provisional balance, not canon.

BOP actions adjust only the generic civil/security mandate, preserving Belka's Rald/Lehmann and Sapin's monarchy/republic contracts. Corporate interests interact with national procurement through influence prerequisites, and AAT adds actual existing-MIO funds. Individual company histories, rivalries and rosters require source-backed content decisions. No geopolitical role or date for Grunder, Neucom or General Resource was fabricated.

## Subpact lifecycle

An independent, non-capitulated native faction member with another eligible ally may spend 75 PP to found a council. A country holds at most one seat. Multiple councils may coexist, including within one parent faction. The founder chairs its council and holds a full seat.

Full members remain independent members of the chair's native faction. Associates remain independent and either factionless or in the chair's faction. Accepting an associate seat does not join a military bloc. To upgrade an associate, leave and accept a new full invitation after joining the parent bloc through diplomacy.

Invitations store sender country ID and council generation, remain pending for 31 days, deliver after one day, and allow 20 days to respond. The first/default option declines. A second invitation cannot replace a pending offer. Acceptance rechecks identity, generation, chair and current eligibility. Dissolution, transfer, faction changes and expiration invalidate stale offers.

The chair may transfer to a current full member for 25 PP. Programs and eligible seats transfer; stale seats and old invitations do not. The old chair remains a full member. Withdrawal/dissolution never refunds investment or changes the parent faction. Chair annexation, subjugation, capitulation or loss of its faction invalidates benefits immediately and removes seats during monthly cleanup. There is no automatic unsourced successor. Civil-war clones cannot inherit identity-bound seats/chairs; the old country retains its own council if valid.

Dynamic modifier enable conditions recheck eligibility before monthly cleanup. Monthly country pulses refresh displays/target rosters. State uses persistent variables/flags rather than transient global event targets; actual native save/reload is untested. Disabling the rule removes custom modifiers/BOP/seats at cleanup while preserving negotiated native blocs.

## Programs, consent and economy

Each single-level program needs **the chair's investment and another current full member's investment**, followed by 50 PP authorization. Every investment costs 35 PP. If ac_econ_ready is true it also debits exactly 2 existing fiscal units, requires treasury >=2 and zero arrears, and never borrows or writes debt. Fiscal-off investment does not mutate treasury. One investment per track/membership; leaving discards it without refund.

| Program | Influence required | Full benefit | Associate benefit |
| --- | --- | --- | --- |
| Mobility | National security >=30 | Supply consumption -3% | -1.5% |
| Procurement | National industry >=30 | Efficiency growth +5% | +2.5% |
| Research | Corporate engineering >=30 | Research speed +2% | +1% |

Live availability and enactment rechecks prevent a departed supporter from authorizing a program or charging for a no-op. A voluntary investment is the member's consent. This intentionally adapts rather than duplicates OEM's formal ballots, shared fund and staged programs. No NATO membership, Earth region whitelist, GDP fund or shared global research group links unrelated blocs.

AI can accept/decline using opinion-weighted consent. Invited AI full members may invest and support industry until procurement eligibility; an AI chair may authorize funded programs. AI never creates or invites new blocs/councils through this bundle. Native AI timing/balance remains untested.

NCNS coordination sessions cost 35 PP / 90 days, give 10 initiative and 5 influence, and advance the current leader's three-session goal. Another goal needs all three council programs. These belong only to the new template. Native facilities, doctrine sharing, intelligence departments, commanders and unrelated DLC country content retain their normal systems; this bundle does not pretend to implement them as new custom mechanics.

## Validation and integration

Run tools/Run-UlyssesFactionChecks.ps1 with -ReferenceGameRoot and optionally -IncludeCampaign. The separate runner avoids the shared static wrapper concurrently owned by visual/economy PR #23; CI registers the offline faction suite as its own step. The game bundle is additive: existing focus, history, campaign, economy, GUI and asset files are unchanged.

See [provenance](FACTIONS_PROVENANCE.md) and [validation](FACTIONS_VALIDATION.md). Offline state copying/long-horizon checks are not native saves or a played campaign. Native parser/UI/diplomacy/AI/precision/save/reload acceptance remains required. The active MD playtest must not be interrupted, and no installed content, playset, save or setting may change in this session.

Named alliance rosters, per-company stories and changes to inherited campaign start/outcomes remain source/owner decisions. These generic systems function without making those decisions.

## Meaning and limits of DLC integration

The bundle connects its actual entry points to supported engine APIs; it does not claim every DLC feature has received new Ulysses content. NCNS receives one authored template, joining/war-call rules, a manifest, two goals, initiative/influence contributions and gated research/operations unlocks. La Resistance supplies existing agency/spymaster behavior; no custom espionage operations are added. AAT supplies existing MIO progression funds; no new canon companies, MIO trait trees or international-market transactions are added. BBA is a conservative presentation gate for the generic native BOP; it is not a claim that all BOP script access itself is DLC-exclusive. The existing country BOPs are preserved.

Internal interests and subpacts are custom script systems rather than extra native country factions. OEM formal ballots, automatic chair succession, a central GDP fund and a global research group are intentionally not copied. Per-company political histories and canonical alliance rosters are not invented. No custom Thunder at Our Gates HQ/captain mechanics, Gotterdammerung projects, country focus-pack content, or other unrelated DLC content is claimed. Existing native facilities, doctrine sharing, commanders, market and intelligence panels retain their engine behavior and prerequisites.

No new visual asset is supplied; the new template/BOP references existing Ulysses art. This is not a claim that every native DLC screen or engine fallback icon has been reskinned, nor that native UI rendering has passed acceptance. Those require a later approved native review. The active MD playtest remains untouched.
