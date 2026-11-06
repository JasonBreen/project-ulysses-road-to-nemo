# The Belkan War and the 1990s: source ledger

Status: **sources, dispositions and reference briefs.** This ledger compiles the
official 1991–1999 entries that no earlier ledger cited. The inherited archive
owns most of the Belkan War, so for those rows the archive stays **mod
provenance** and the official date is a reference anchor, never a trigger to
force. Since 5 November 2026 the Belkan War record (`tools/content_waves/belkan_record.py`,
namespace `ac_bwr`) publishes thirteen **reference briefs** beside the archive:
each is a news event that fires once, only on observed state and inside its
window, writes only `ac_bwr_*` flags, and is marked skipped (never fired later)
when its window closes first, as on a late save. The windows and observed
conditions are provisional gameplay.

Primary sources, read 4 November 2026: the [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/)
(*Chronicle, YYYY / MM.DD*), [Super Weapons](https://acecombat.jp/en/chronicle/weapons/)
and [Abstracts](https://acecombat.jp/en/chronicle/). Every 1991–2020 statement,
its hash, coverage evidence and conflicts are in the
[official lore record](research/STRANGEREAL_LORE_1991_2020.md) and
[index](research/CHRONICLE_INDEX.md). Entries are paraphrased.

Already compiled elsewhere: 1991 / 08.29 and 1995 / 03.25, 06.01–04, 06.20 in
[FATO_SOUTH_BELKA.md](FATO_SOUTH_BELKA.md); 1994 / 12.10, 1996 / 04.20,
1998 / 07.29, 09.20 and 1999 / 07.08 in [ANEA_CAMPAIGNS.md](ANEA_CAMPAIGNS.md);
1995 / 06.20, 12.25, 12.31, 1996 / 01.17, 1998 / 06.19 in
[PEACE_WE_INHERIT.md](PEACE_WE_INHERIT.md); 1994 / 12.23, 1995 / 05.17, 12.31,
1997 / 05.30, 1998 / 06.19, 1999 / 10.08 in
[USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md).

## 1991–1994

| Claim | Exact source | Covered by | Disposition and conflicts |
| --- | --- | --- | --- |
| The Osean Maritime Defense Force orders the Kestrel, the seventh Hubert-class carrier | Chronicle, 1991 / 07.29 | `ac_bwr.1` | Implemented as a dated brief (window to 28 August 1991); no ship is built |
| The Great Lakes Resource Development Company, jointly financed by Osea and Belka, is found to have covered up operating at a loss | Chronicle, 1991 / 08.16 | inherited `BLK_GLRDC`, `BLK_osean_prop`, `osea_glrdc.*` | Mod provenance owner. The archive creates the company only after Belka sells land; officially the discovery (08.16) precedes the sales (08.29) |
| Scinfaxi-class submarines are announced at a political convention in Cinigrad, Yuktobania; Osean Foreign Minister Howards belittles them | Chronicle, 1991 / 09.02 | `ac_bwr.2` | Implemented as a dated brief; Howards and Cinigrad are named in its text only |
| Belkan borders are redrawn | Chronicle, 1991 / 12.16 | inherited `belka.9`; `ac_bwr.3` | Brief fires once the archive's sale (`BLK_sell_the_land`) has happened and the date has passed (window to the end of 1992). The archive transfers states at the sale itself; the brief moves no border |
| The Belkan Liberal Democratic Party wins a single-party majority | Chronicle, 1992 / 02.24 | inherited `BLK_dlp_victory`, `BLK_DLP_won_flag` | Mod provenance owner. The archive calls it the "Democratic Liberal Party" (DLP) in IDs and text |
| Asteroid 1994XF04 is discovered by researchers at Seals Bridge University | Chronicle, 1994 / 10.04 | README "Historical coordinates" only | Reference only |

## 1995: the Belkan War

| Claim | Exact source | Covered by | Disposition and conflicts |
| --- | --- | --- | --- |
| An assault on Model, a Gebetian border city, on Belka's eastern front | Chronicle, 1995 / 03.27 | `ac_bwr.4` | Brief fires only while the archive's war runs and Belka is at war with Gebet. Model stays unmapped; inherited `gebet_belkan_war.*` describes a different raid |
| Nearly all of Ustio falls under Belkan control; Belkan and Ustian air forces clash over Monte Rosa | Chronicle, 1995 / 03.30 | inherited war simulation, `belka_dlp_war.102`; `ac_bwr.5` | Mod provenance owner. The brief fires only when Belka actually holds Directus (state 335) or Ustio has capitulated; Monte Rosa stays absent |
| Ustio allies with Osea and begins its resistance | Chronicle, 1995 / 04.01 | inherited `belka_dlp_war.2`, `ustio.2`, `ustio.3`; `ac_bwr.6` | Mod provenance owner. The brief fires only when Ustio is in a faction with Osea. The archive's "Allied Forces" faction includes Sapin; the sentence names only Ustio and Osea |
| The Osean Army begins its resistance | Chronicle, 1995 / 04.03 | inherited `belka_dlp_war.1`, `osea.75`–`.77`; `ac_bwr.7` | Mod provenance owner. The brief fires only when Osea is at war with Belka. The archive has Belka cross into Osea on day one |
| Offensive Campaign No. 4101 to drive Belka from Futuro Canal and secure a sea supply line; the carrier Kestrel's test voyage | Chronicle, 1995 / 04.24 | `ac_bwr.8` | Brief fires only while Osea is at war with Belka in the archive's war; no operation is scripted |
| The Allied Forces liberate Ustio's capital, Directus | Chronicle, 1995 / 05.13 | `ac_bwr.9` | Brief fires only when Ustio controls Directus (state 335) again after the record saw Belka hold it (`ac_bwr_directus_occupied`) |
| The independent country is restored to its prewar state | Chronicle, 1995 / 05.14 | `ac_bwr.9` (cited) | Cited in the Directus brief as the record's next-day entry; only Directus is observed. The sentence's subject is not expanded to a name |
| The Allied Forces destroy Excalibur | Chronicle, 1995 / 05.23 | inherited `BLK_excalibur` decisions; `ac_sp_excalibur` reads `excalibur_destroyed` | Mod provenance owner. The archive destroys it on a war-day timer, not on the date |
| Southern Belkan cities declare themselves demilitarized open cities | Chronicle, 1995 / 06.04 (the range 06.01–04 is compiled in FATO_SOUTH_BELKA.md) | inherited `belka_dlp_war.99`, `.101` and the South Belka release | Mod provenance owner. The archive models a South Belka country tag defecting; the source says only that cities declared themselves open |
| The Battle of Waldreich; the Osean Wizard and Sorcerer squadrons leave the front and contact is lost | Chronicle, 1995 / 06.05 | `ac_bwr.10` | Brief fires only while the archive's war runs (window to 31 July 1995); the squadrons are named in text only. The archive's "Wacht am Waldreich" branch is a different, Belkan last-stand mechanic |
| The Belkan Army uses seven nuclear devices in the Waldreich Mountains; Larry Foulke of Galm Team disappears | Chronicle, 1995 / 06.06 | inherited `BLK_cook_nukes_timer_dec`, `belka_dlp_war.100`, `ac_news_event.8`, `AWW_larry_foulke` | Mod provenance owner. `ac_news_event.8` places detonations around North Belka as well; the source names only the Waldreich Mountains |
| Espada Team disappears from a base of the Kingdom of Sapin | Chronicle, 1995 / 10.18 | `ac_bwr.11` | Implemented as a dated brief |
| Hresvelgr: a heavy command cruiser secretly developed by the South Belka Munitions Factory during the Belkan War | Super Weapons, Hresvelgr | inherited `BLK_south_belka_munitions_monopoly` names the factory | Not covered as a weapon. The page calls A World With No Boundaries an insurgent group; the archive makes it a country (`AWW`) |

## 1996–1999

| Claim | Exact source | Covered by | Disposition and conflicts |
| --- | --- | --- | --- |
| The FCU Army announces that Commander Robert Tyler (54) will replace the Riass Armed Forces Chief of Staff, who died on 20 March | Chronicle, 1996 / 04.18 | `ac_ur.1` names Tyler for 1995 / 12.31; `ac_bwr.12` | Implemented as a dated brief; no officeholder changes. "Riass" is recorded as written |
| The Osean carrier Kestrel is commissioned | Chronicle, 1999 / 09.16 | `ac_bwr.13` | Implemented as a dated brief |

## Citations for rows the archive already reports

These four rows stay with their inherited owners; the record adds no second
event for them. 1992 / 02.24 (the Liberal Democratic Party's majority) is
reported by `BLK_dlp_victory` and the archive's election events; 1995 / 05.23
(Excalibur destroyed) by the `BLK_excalibur` decisions and `ac_sp_excalibur`;
1995 / 06.04 (southern cities declared open) by `belka_dlp_war.99`/`.101` and the
South Belka release; 1995 / 06.06 (seven nuclear devices in the Waldreich
Mountains) by `belka_dlp_war.100` and `ac_news_event.8`. Hresvelgr stays
reference only.

## Archive defect: fixed 6 November 2026

`belka_lost_belkan_war` is read by `events/ac_continuation.txt` and by
`common/decisions/ac_belkan_campaign.txt`, but its only setter,
`belka_dlp_war.103` (`events/Belka.txt`), has no caller. Every Belkan defeat in
play runs through the nuclear ending (`belka_dlp_war.99` a, the 14-day timer,
`.100`, `.101`), so a defeat never recorded the flag, and the postwar router took
its unclassified option.

The reviewed repair (mod provenance, not archive text):
`tools/release_foundations/author.py` appends
`set_global_flag = belka_lost_belkan_war` to `.101`'s option as a reviewed
suffix, which `event_contract.py` accepts and nothing else; `event_inputs.json`
is not recaptured. `world_event.2` (`events/ac_world_events.txt`) sets the same
flag when the nuclear ending's wait flag is still present, for saves in which
`.101` fired before the repair. The defeat now reaches `ac_continuation.1.c`
(Osea as guarantor) and The Peace We Inherit's defeat lane, and the war
council stays closed after a defeat. `.103` stays dormant by decision; wiring a
conventional surrender to it would need guards against the nuclear timer and
the hash-pinned `ac_on_actions.txt`. Static/offline only; native confirmation
is playtest O3 (#8).

## Rules for any later use

- None of these rows moves a border, creates a unit or names an officeholder in
  the game. Model, Monte Rosa, Futuro Canal, Directus, Waldreich and Cinigrad
  stay unmapped unless a reviewed geography decision maps them.
- Where the archive already owns an event, it stays the owner; a later package
  may add a sourced reference brief beside it, never a second trigger.
- Named pilots and squadrons (Galm, Larry Foulke, Wizard, Sorcerer, Espada)
  stay text.
