# The Belkan War and the 1990s: source ledger

Status: **sources and dispositions only.** This ledger compiles the official
1991–1999 entries that no earlier ledger cited. It changes no content. The
inherited archive owns most of the Belkan War, so for those rows the archive
stays **mod provenance** and the official date is a reference anchor, never a
trigger to force.

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
| The Osean Maritime Defense Force orders the Kestrel, the seventh Hubert-class carrier | Chronicle, 1991 / 07.29 | nothing | Not covered. The ship appears only at its 2010 sinking (`ac_cpw.34`) |
| The Great Lakes Resource Development Company, jointly financed by Osea and Belka, is found to have covered up operating at a loss | Chronicle, 1991 / 08.16 | inherited `BLK_GLRDC`, `BLK_osean_prop`, `osea_glrdc.*` | Mod provenance owner. The archive creates the company only after Belka sells land; officially the discovery (08.16) precedes the sales (08.29) |
| Scinfaxi-class submarines are announced at a political convention in Cinigrad, Yuktobania; Osean Foreign Minister Howards belittles them | Chronicle, 1991 / 09.02 | nothing for 1991 | Not covered. Howards is named nowhere; the class appears only in 2010 (`ac_cpw_yuk_submarine_carrier(s)`) |
| Belkan borders are redrawn | Chronicle, 1991 / 12.16 | inherited `belka.9` | Not covered as a dated row. The archive transfers states at the sale itself; officially the sales and the redrawing are separate dates. No border change follows from this row |
| The Belkan Liberal Democratic Party wins a single-party majority | Chronicle, 1992 / 02.24 | inherited `BLK_dlp_victory`, `BLK_DLP_won_flag` | Mod provenance owner. The archive calls it the "Democratic Liberal Party" (DLP) in IDs and text |
| Asteroid 1994XF04 is discovered by researchers at Seals Bridge University | Chronicle, 1994 / 10.04 | README "Historical coordinates" only | Reference only |

## 1995: the Belkan War

| Claim | Exact source | Covered by | Disposition and conflicts |
| --- | --- | --- | --- |
| An assault on Model, a Gebetian border city, on Belka's eastern front | Chronicle, 1995 / 03.27 | nothing names Model | Not covered. Inherited `gebet_belkan_war.*` describes a different raid |
| Nearly all of Ustio falls under Belkan control; Belkan and Ustian air forces clash over Monte Rosa | Chronicle, 1995 / 03.30 | inherited war simulation, `belka_dlp_war.102` | Mod provenance owner; the occupation is not scripted and Monte Rosa is absent |
| Ustio allies with Osea and begins its resistance | Chronicle, 1995 / 04.01 | inherited `belka_dlp_war.2`, `ustio.2`, `ustio.3` | Mod provenance owner. The archive's "Allied Forces" faction includes Sapin; the sentence names only Ustio and Osea |
| The Osean Army begins its resistance | Chronicle, 1995 / 04.03 | inherited `belka_dlp_war.1`, `osea.75`–`.77` | Mod provenance owner. The archive has Belka cross into Osea on day one |
| Offensive Campaign No. 4101 to drive Belka from Futuro Canal and secure a sea supply line; the carrier Kestrel's test voyage | Chronicle, 1995 / 04.24 | Futuro Canal as map geography only | Not covered |
| The Allied Forces liberate Ustio's capital, Directus | Chronicle, 1995 / 05.13 | `UST` history and the war simulation | Not covered as a scripted row |
| The independent country is restored to its prewar state | Chronicle, 1995 / 05.14 | nothing | Not covered. The sentence's subject is "the independent country"; it is not expanded to a name here |
| The Allied Forces destroy Excalibur | Chronicle, 1995 / 05.23 | inherited `BLK_excalibur` decisions; `ac_sp_excalibur` reads `excalibur_destroyed` | Mod provenance owner. The archive destroys it on a war-day timer, not on the date |
| Southern Belkan cities declare themselves demilitarized open cities | Chronicle, 1995 / 06.04 (the range 06.01–04 is compiled in FATO_SOUTH_BELKA.md) | inherited `belka_dlp_war.99`, `.101` and the South Belka release | Mod provenance owner. The archive models a South Belka country tag defecting; the source says only that cities declared themselves open |
| The Battle of Waldreich; the Osean Wizard and Sorcerer squadrons leave the front and contact is lost | Chronicle, 1995 / 06.05 | nothing | Not covered. The archive's "Wacht am Waldreich" branch is a different, Belkan last-stand mechanic |
| The Belkan Army uses seven nuclear devices in the Waldreich Mountains; Larry Foulke of Galm Team disappears | Chronicle, 1995 / 06.06 | inherited `BLK_cook_nukes_timer_dec`, `belka_dlp_war.100`, `ac_news_event.8`, `AWW_larry_foulke` | Mod provenance owner. `ac_news_event.8` places detonations around North Belka as well; the source names only the Waldreich Mountains |
| Espada Team disappears from a base of the Kingdom of Sapin | Chronicle, 1995 / 10.18 | nothing | Not covered |
| Hresvelgr: a heavy command cruiser secretly developed by the South Belka Munitions Factory during the Belkan War | Super Weapons, Hresvelgr | inherited `BLK_south_belka_munitions_monopoly` names the factory | Not covered as a weapon. The page calls A World With No Boundaries an insurgent group; the archive makes it a country (`AWW`) |

## 1996–1999

| Claim | Exact source | Covered by | Disposition and conflicts |
| --- | --- | --- | --- |
| The FCU Army announces that Commander Robert Tyler (54) will replace the Riass Armed Forces Chief of Staff, who died on 20 March | Chronicle, 1996 / 04.18 | `ac_ur.1` names Tyler for 1995 / 12.31 | Not covered. "Riass" appears nowhere else; it is recorded as written |
| The Osean carrier Kestrel is commissioned | Chronicle, 1999 / 09.16 | nothing | Not covered |

## Rules for any later use

- None of these rows moves a border, creates a unit or names an officeholder in
  the game. Model, Monte Rosa, Futuro Canal, Directus, Waldreich and Cinigrad
  stay unmapped unless a reviewed geography decision maps them.
- Where the archive already owns an event, it stays the owner; a later package
  may add a sourced reference brief beside it, never a second trigger.
- Named pilots and squadrons (Galm, Larry Foulke, Wizard, Sorcerer, Espada)
  stay text.
