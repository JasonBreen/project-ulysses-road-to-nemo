# Strangereal 2006–2020: source ledger (Gate 0)

Status: **sources and dispositions only.** This ledger gates every dated
participant, place, leader or weapon scripted for 2006–2020, as
[USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md) gated 1994–2005. A row here
does not mean the content is implemented; the disposition column says what is.

Primary sources, read 3 November 2026 and re-read for the 2010 and 2019 rows on 4 November 2026:

- [Official ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), cited as *Chronicle, YYYY / MM.DD*.
- [Official ACES Chronicle — Super Weapons](https://acecombat.jp/en/chronicle/weapons/), cited as *Super Weapons, &lt;name&gt;*.
- [Official ACES Chronicle — Abstracts](https://acecombat.jp/en/chronicle/), one narrative per title, cited as *Abstracts, &lt;title&gt;*.
- [Official ACES product pages](https://acecombat.jp/en/product/), cited as *Product, &lt;title&gt;* for the lore statements in the title blurbs.

The [official lore record](research/STRANGEREAL_LORE_1991_2020.md) lists every statement on these pages with its coverage, conflicts and unknowns.


Entries are paraphrased. `XX` marks a day or month the source does not give; it
stays unknown in script. "Derived" marks a value computed from a source sentence
rather than stated by it. Waves follow [CONTENT_PLAN_2006_2020.md](CONTENT_PLAN_2006_2020.md):
A Free Erusea, B Estovakian civil war, C Circum-Pacific War, E Emmeria–Estovakia
War, F1 Lighthouse War, F2 Aurelia and Leasath.

Rules carried over from the canon policy: dates are reference anchors, not forced
outcomes; earned alternatives stay explicit; named people appear only as the
source names them and gain no biography, portrait or leader role; named
squadrons and pilots are not added as units; places are not mapped to states
without a separate reviewed geography decision.

## 2005, after the Continental War

The 2005 entries through 26 September are already cited in
[USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md) and implemented by `ac_ucw`.

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| The documentary *Warriors and the Belkan War* airs on Osea's OBC network | Chronicle, 2005 / 09.26 | Reference only | Not scripted |

## 2006: Free Erusea

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Free Erusea begins an armed insurrection | Chronicle, 2006 / 09.26 | A | Implemented as `ac_fe.1` |
| Free Erusea is defeated by Mobius 1 | Chronicle, 2006 / 09.26 (same entry) | A | The historical route (Central Usean response) records the defeat; a prolonged insurrection is a labelled provisional alternative. Mobius 1 is named only in text and is not a unit |

## 2007–2014: Estovakia's civil war and its aftermath

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| The Lyes Faction, later the Lyes United Front (LUF), seizes the Estovakian capital | Chronicle, 2007 / 04.03 | B | Implemented: `ac_ecw.1`; no tag or government change |
| The LUF suppresses cities that resist; other factions revolt and the civil war begins | Chronicle, 2007 / 06.30 | B | Implemented: `ac_ecw.2`; the civil war is tagless |
| Estovakia's Eastern Faction takes and restores northeastern oil platforms held by a public corporation | Chronicle, 2008 / 07.15 | B | Implemented: `ac_ecw.3` and the Estovakian oil lane; no state or resource transfer |
| The Republic of Anea Initiative is put on hold because of internal strife in Estovakia | Chronicle, 2008 / 10.23 | B | Implemented: `ac_ecw.4` and flag `ac_ecw_anea_initiative_on_hold`; the existing `ac_anea` bureau state is read, never written |
| Emmeria ends aid for the LUF's reconstruction programme because the LUF suppresses all opposition | Chronicle, 2010 / 02.19 | B | Implemented: `ac_ecw.5`; the historical option ends the aid, an earned conditional alternative continues it |
| Emmeria ends aid for Estovakia's reconstruction | Chronicle, 2011 / 05.09 | B | Implemented: `ac_ecw.6` |
| The Eastern Faction and the LUF clash; the LUF loses 80% of its territory in one week to new weapons and elite aviation units | Chronicle, 2013 / 01.15 | B | Implemented: `ac_ecw.7` (authority falls); no territory changes hands on the map |
| The LUF fights on but is defeated near the Emmerian border; General Lyes is killed and the civil war ends | Chronicle, 2013 / 10.29 | B | Implemented: `ac_ecw.9`; earned negotiated settlement (`ac_ecw.14`) and provisional prolonged war (`ac_ecw.8`, `.13`) are alternatives |
| Estovakian Foreign Minister Isaac Arensky, former air marshal of the Northern Highlands Faction, is attacked; fifteen former LUF soldiers are arrested a week later | Chronicle, 2013 / 11.25 | B | Implemented: aftermath news only |
| Arensky dies; the death is withheld from the public | Chronicle, 2013 / 12.02 | B | Implemented: aftermath news only |
| The pilot Talisman joins the Republic of Emmeria Air Force and defends Gracemeria | Chronicle, 2013 / 12.23 | Reference only | Named pilot; not scripted |
| Arensky's death is announced; Antonina Koznick, a former Eastern Faction navy captain, succeeds him | Chronicle, 2014 / 02.03 | B | Implemented: aftermath news only; no character or leader is created |
| Former LUF members attack a relief-supply storage facility in the western city of Vistoc | Chronicle, 2014 / 02.04 | B | Implemented: aftermath news only |

## 2008: the Arkbird Summit

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| The Arkbird Summit is held | Chronicle, 2008 / 08.21 | C | Implemented: `ac_cpw.14` news, only if the Arkbird project is complete. The Chronicle gives no agenda or result and none is asserted |

## 2010: the Circum-Pacific War

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Unidentified aircraft appear at Cape Landers, Osea; the Osean Air Defense Force's Wardog Squadron engages, but only two aircraft survive | Chronicle, 2010 / 09.23 | C | Implemented: `ac_cpw.1` news; the aircraft are not identified |
| An unidentified SR-71 appears over Osea and is hit by a coastal surface-to-air missile | Chronicle, 2010 / 09.24 | C | Implemented: `ac_cpw.2` news; no owner is named |
| Wardog Squadron engages unidentified aircraft; Yuktobania declares war on Osea and attacks Port Saint Hewlett; the war begins | Chronicle, 2010 / 09.27 | C | Implemented: the owner's declaration `ac_cpw_declare` (Yuktobanian decision event `ac_cpw.5`, AI always) and news `ac_cpw.3`. The Chronicle gives no reason and none is asserted. Earned alternatives: the reciprocal exchange (`ac_cpw.4`) and the withheld declaration (`ac_cpw.7`) |
| Scinfaxi, the first of Yuktobania's Scinfaxi-class submarines, sees its first use in war; the Osean Maritime Defense Force aircraft carriers Vulture and Buzzard are sunk at Eaglin Straits; Osea sends the Arkbird to the front line | Chronicle, 2010 / 09.30 | C | Implemented: `ac_cpw.20`; the Arkbird goes to the front only if `ac_sp_arkbird_complete` and Osea sends it (`ac_cpw.6`, `ac_cpw.15`) |
| Scinfaxi is sunk at Sand Island | Chronicle, 2010 / 10.04 | C | Implemented: `ac_cpw.21`; one submarine-carrier idea remains |
| The Akerson Hill Incident | Chronicle, 2010 / 10.22 | C | Implemented: `ac_cpw.22`, name only |
| Smuggled explosives destroy the Arkbird's engines | Chronicle, 2010 / 10.25 | C | Implemented: `ac_cpw.23`, only if the Arkbird was committed; `ac_sp_arkbird` is read, never completed or revived |
| Osea invades the southeastern Yuktobanian mainland on the Bastok Peninsula | Chronicle, 2010 / 11.01 | C | Implemented: `ac_cpw.24`, only once Osean forces actually control Yuktobanian territory; no state is moved and the peninsula is not mapped |
| Osean aircraft fire on an engineering college in the Yuktobanian city of Dresdene, with multiple fatalities | Chronicle, 2010 / 11.02 | C | Implemented: `ac_cpw.25`, after the Bastok row |
| Yuktobanian special forces use nerve gas in a terrorist attack in the Osean Federation's college city of Bana; Yuktobanian forces make a surprise attack on Apito International Airport in the Osean Federation | Chronicle, 2010 / 11.04 | C | Implemented: `ac_cpw.26` |
| The submarine Hrimfaxi is sunk in the Razgriz Straits | Chronicle, 2010 / 11.14 | C | Implemented: `ac_cpw.27`; the last submarine-carrier idea is removed |
| Yuktobanian aircraft attack during a peace ceremony in the Osean Federation's November City | Chronicle, 2010 / 11.29 | C | Implemented: `ac_cpw.28` |
| Osean forces bring down Cruik Fortress, Yuktobania's final defensive stronghold | Chronicle, 2010 / 12.06 | C | Implemented: `ac_cpw.29`, gated like the Bastok row; the fortress is not mapped |
| Peter N. Beagle and Albert Genette help suspected Wardog members flee; all are shot down by Captain Marcus Snow | Chronicle, 2010 / 12.07 | Reference only | Named individuals; not scripted |
| President Harling is rescued from imprisonment at Stier Castle in the Principality of Belka; Razgriz Squadron forms and serves directly under the president | Chronicle, 2010 / 12.09 | C | Implemented: `ac_cpw.30` news only; the president is named as the Chronicle names him and no character, leader or portrait changes |
| The Arkbird, carrying a nuclear weapon, uses atmospheric friction to manoeuvre towards an attack on the Yuktobanian city of Okchabursk and is shot down by Razgriz Squadron | Chronicle, 2010 / 12.19 | C | Implemented: `ac_cpw.31`, only if the Arkbird was committed. The Arkbird is recorded as lost (`ac_cpw_arkbird_lost`) and its two project ideas are removed; the project itself is never weaponized by script |
| Former Prime Minister Seryozha Viktrovich Nikanor, who was imprisoned by the Yuktobanian military, is rescued; the rescuer is not named | Chronicle, 2010 / 12.23 | C | Implemented: `ac_cpw.32` news only |
| The Battle of Ceres Ocean | Chronicle, 2010 / 12.29 | C | Implemented: `ac_cpw.33`, name only |
| The Osean aircraft carrier Kestrel is sunk; President Harling and Prime Minister Nikanor make a televised address asking their militaries to disarm; a joint force inspects Gründer Industries facilities in the Osean trust territory of Sudentor, North Osea | Chronicle, 2010 / 12.30 | C | Implemented: `ac_cpw.34`; the appeal weighs on both countries' war support but ends nothing by script |
| Astronomers spot the SOLG falling; Razgriz Squadron shoots down the Grabacr and Ofnir squadrons of the former Belkan Air Force and destroys the SOLG; the war ends | Chronicle, 2010 / 12.31 | C | Implemented: `ac_cpw.35` reports the SOLG; the end (`ac_cpw.10`–`.13`) is recorded only when the fighting between Osea and Yuktobania actually stops, never on the anchor |

## 2015–2016: the Emmeria–Estovakia War

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Yuktobanian spy satellites see a massive aircraft signature off Estovakia's southeast coast | Chronicle, 2015 / 04.21 | E | Implemented: `ac_eew.16`, news only inside its window; the signature is not attributed |
| Ed Alverez takes command of the Gavial tank battalion; hostilities break out | Chronicle, 2015 / 06.10 | Reference only | Named individual; not scripted |
| Estovakia invades and seizes Gracemeria; the Aigaion cannot be countered; Emmerian forces retreat west and the war begins | Chronicle, 2015 / 08.30 | E | Implemented: `ac_eew_declare` (Estovakian decision event `ac_eew.5`, AI always), news `ac_eew.1`; the capital's fall (`ac_eew.20`) only when Estovakia controls Emmeria's capital. Needs the Eastern Faction's civil-war victory; earned withholding, divergent and unreachable routes |
| Freddie Durand (Avalanche) leads the 2nd Strike Fighter Squadron | Chronicle, 2015 / 09.12 | Reference only | Named pilot; not scripted |
| Witnesses see giant fireballs attacking retreating Emmerian forces | Chronicle, 2015 / 11.XX | E | Implemented: `ac_eew.21` inside November 2015, skipped if the month passes; no cause is asserted |
| Emmerian forces at Campagna Airport intercept bombers sent toward Vitoze on Khesed Island | Chronicle, 2015 / 11.24 | E | Implemented: `ac_eew.22`, news only |
| Emmerian ground forces break through at Sipli Field | Chronicle, 2015 / 11.27 | E | Implemented: `ac_eew.23`, news only |
| Bartolomeo Fortress falls; Emmeria controls Khesed Island | Chronicle, 2015 / 12.27 | E | Implemented: `ac_eew.24`, timed Emmerian idea; Khesed Island unmapped |
| Emmeria lands at Rargom Beach | Chronicle, 2016 / 01.26 | E | Implemented: `ac_eew.25`, news only |
| Emmerian forces advance along the Selumna Peaks | Chronicle, 2016 / 02.12 | E | Implemented: `ac_eew.26`, news only |
| Emmeria captures Cavallia Air Force Base in San Loma | Chronicle, 2016 / 02.15 | E | Implemented: `ac_eew.27`, news only |
| The Emmerian Air Force destroys the Aerial Fleet | Chronicle, 2016 / 02.20 | E | Implemented: `ac_eew.28` only if `ac_sp_aerial_fleet` was completed; its reward is removed |
| Emmeria strikes Ragno Fortress in Grageo Canyon | Chronicle, 2016 / 03.06 | E | Implemented: `ac_eew.29`, news only |
| Battle in the Moloch Desert; Estovakia retreats | Chronicle, 2016 / 03.25 | E | Implemented: `ac_eew.30`, timed Estovakian idea |
| Emmeria assaults Fort Norton and stops transport of weapons catalysts | Chronicle, 2016 / 03.26 | E | Implemented: `ac_eew.31`, news only |
| Gracemeria is liberated; cruise missiles fired at it that night are shot down | Chronicle, 2016 / 03.31 | E | Implemented: `ac_eew.32` only when Emmeria controls its capital again after the observed fall |
| The Chandelier on Sonne Island is destroyed; Gustav Dvornik dies; an antigovernment coup in Estovakia leads to a ceasefire | Chronicle, 2016 / 04.01 | E | Implemented: the coup `ac_eew.33` (timed idea; no politics changed), the Chandelier's destruction `ac_eew.34` only if `ac_sp_chandelier` was completed, and the scripted ceasefire `ac_eew.6`/`ac_eew_sign_ceasefire`, written only if the engine ended the war. Dvornik is named in text only |

## 2019: the Lighthouse War and the Leasath civil war

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Drone strikes hit four Osean naval ports; Erusea declares war on Osea and captures the International Space Elevator; the Lighthouse War begins | Chronicle, 2019 / 05.15; Abstracts, ACE COMBAT 7 (Erusea seizes control of the Arsenal Birds with the elevator; the war opens with terrorist drones); Product, ACE COMBAT 7 (Erusea accuses Osea of massive overreach in their joint international projects) | F1 | Implemented: the owner's declaration `ac_lhw_declare` (Erusean decision event `ac_lhw.5`, AI always), news `ac_lhw.1`; the seized birds (`ac_lhw.29`) only if `ac_sp_arsenal_birds` was completed. The stated grievance is quoted as the source states it; the earned alternative is the withheld declaration (`ac_lhw.2`). The route needs the ISAF victory |
| Osea and the IUN Peacekeeping Force begin Operation Eastern Wind | Chronicle, 2019 / 05.17 | F1 | Implemented: `ac_lhw.20`; no force or faction is created |
| A two-pronged offensive on Chopinburg airspace and Farbanti fails; the carrier Kestrel II is sunk | Chronicle, 2019 / 05.30 | F1 | Implemented: `ac_lhw.21`; no ship is represented |
| Former president Vincent Harling dies in a rescue attempt at the space elevator | Chronicle, 2019 / 06.06; Abstracts, ACE COMBAT 7 ("a botched attempt") | F1 | Implemented: `ac_lhw.22`, news only |
| Osea forms the Long Range Strategic Strike Group | Chronicle, 2019 / 08.10 | F1 | Implemented: Osean decision `OSE_lw_strike_group` and `ac_lhw.23`; no unit is created |
| Osea reactivates a Stonehenge battery and shoots down the Arsenal Bird Liberty | Chronicle, 2019 / 08.19 | F1 | Implemented: `ac_lhw.24`, only if Stonehenge was ever built (`ac_ucw_stonehenge_operational`); the Liberty is lost only if the birds were seized |
| Osea attacks Farbanti; destroying military satellites cuts communications across Usea | Chronicle, 2019 / 09.19 | F1 | Implemented: `ac_lhw.25`, only once Osean forces control an Erusean core; the blackout idea on the seven Continental War participants. Whose operation it was is not stated |
| Shilage and other small nations annexed by Erusea declare independence; Erusea refuses and internal conflict follows | Chronicle, 2019 / 10.01 | F1 | Implemented: `ac_lhw.26` and the Erusean secession lane; the release flags are read for text only and nothing is released, cored or moved |
| General Édouard Labarthe is killed by Osean forces | Chronicle, 2019 / 10.10 | F1 | Implemented: `ac_lhw.27`, news only |
| Osean and Erusean forces clash at the space elevator; the Arsenal Bird Justice is shot down | Chronicle, 2019 / 10.31; Abstracts, ACE COMBAT 7 (a voluntary coalition of Osean forces and a traditionalist sect of the Erusean Army; the radicals surrender) | F1 | Implemented: `ac_lhw.28`; the coalition and the sect are named in text only |
| Osea and Erusea sign a ceasefire at the Expo City Conference | Chronicle, 2019 / 12.01; Abstracts, ACE COMBAT 7 | F1 | Implemented as the only scripted peace (user decision 7): `ac_lhw.6` (AI always signs), `ac_lhw_sign_ceasefire`, `ac_lhw.7`; recorded only if the engine ended the war. Alternatives: the earned early ceasefire (`ac_lhw.8`) and fighting on (`ac_lhw.13`) |
| The Leasath civil war ends after ten years of fighting | Chronicle, 2019 / XX.XX | F2 | Implemented (F2a): the tagless owner `ac_lcw` starts in 2009 (derived from "ten years") and ends within 2019 only on the government's own authority (`ac_lcw.2`); prolonged (`ac_lcw.3`, `.4`) and earned negotiated (`ac_lcw.5`) alternatives. No tag, border or winner |

## 2020: the Aurelia–Leasath war

Every 2020 entry gives a month at most.

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Leasath declares war on the Federal Republic of Aurelia, citing years of exploitation; the Gleipnir helps it occupy all of Aurelia except Aubrey Base | Chronicle, 2020 / 10.XX | F2 | Implemented (F2b): `ac_alc_declare` (Leasathian decision event `ac_alc.5` in October, AI always), `ac_alc.1`; the Gleipnir (`ac_alc.15`) only if built; the occupation (`ac_alc.20`) only when Leasath controls Griswall (state 120). The cause is quoted as Leasath's stated claim |
| Aurelia's Gryphus Squadron repels an attack on Aubrey Base | Chronicle, 2020 / 10.XX | F2 | Implemented: `ac_alc.21` inside October 2020; the squadron and base are text only |
| Aurelia retakes Port Patterson | Chronicle, 2020 / 11.XX | F2 | Implemented: `ac_alc.22` inside November 2020, after the observed occupation |
| Aurelia disables Gleipnir's stealth and shoots it down; Santa Elva is liberated | Chronicle, 2020 / 11.XX | F2 | Implemented: `ac_alc.23` inside November 2020, only if `ac_sp_gleipnir` was built |
| Aurelia retakes Sachana Air Base in the Raven Woods | Chronicle, 2020 / 12.XX | F2 | Implemented: `ac_alc.24` inside December 2020, after the observed occupation |
| Aurelia retakes its capital, Griswall; Leasathian forces regroup at Archelon Fortress | Chronicle, 2020 / XX.XX | F2 | Implemented: `ac_alc.25` when Aurelia controls Griswall (state 120) again after the observed occupation; no month asserted |
| Archelon Fortress is destroyed; Leasath's commander Diego Navarro is removed from office and the war ends | Chronicle, 2020 / 12.XX | F2 | Implemented: the removal `ac_alc.26` (timed idea; no politics changed) and Archelon `ac_alc.27` only if built, inside December 2020; the scripted ceasefire `ac_alc.6`/`ac_alc_sign_ceasefire`, written only if the engine ended the war. Navarro is named in text only |

## Super Weapons active in the period

| Weapon | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Chandelier: Estovakian railgun built against Ulysses fragments, incomplete when the asteroid arrived, later weaponized in the Emmeria–Estovakia War and destroyed | Super Weapons, Chandelier | B (custody only), E | Already recorded as incomplete by the Anea campaign. Wave B keeps the research team in custody only; weaponization belongs to Wave E |
| Arkbird: Osean–Yuktobanian low-orbit spacecraft for clearing Ulysses fragments | Super Weapons, Arkbird | C | `ac_sp_arkbird` stays a non-weapon project. The 2010 rows are implemented as `ac_cpw` states that need the completed project and never create, revive, weaponize or complete it |
| SOLG: Osean Cold War orbital railgun, abandoned after the Belkan War, revived by the Gray Men with a V2 warhead | Super Weapons, SOLG | C | Named in `ac_cpw.35` text only, with the Gray Men as the source names them; no project or weapon is created |
| Scinfaxi and Hrimfaxi: Yuktobanian nuclear-powered submarine carriers | Super Weapons, Scinfaxi & Hrimfaxi | C | Implemented as the Yuktobanian wartime ideas `ac_cpw_yuk_submarine_carriers` and `ac_cpw_yuk_submarine_carrier`, removed on the sourced sinkings; no ship is created |
| Aigaion, Gyges, Kottos: Estovakian heavy command cruiser and support platforms of the Aerial Fleet Initiative (P/F-X), based on Belkan technology | Super Weapons, Aigaion; Gyges; Kottos | E | Pending; no construction date is given, so any timing is provisional |
| Arsenal Birds Liberty and Justice: Osean unmanned aircraft defending the International Space Elevator | Super Weapons, Arsenal Birds | F1 | Implemented as project `ac_sp_arsenal_birds` (user decision 8) in a generator-owned file; seized, lost and never rebuilt on the sourced dates |
| Alicorn: Erusean Royal Navy submarine aviation cruiser | Super Weapons, Alicorn | F1 | Implemented as project `ac_sp_alicorn` (user decision 8), gated on the Erusean custody lane; built and held, never deployed |
| Gleipnir and its prototype Gandr: Leasathian aerial fortress and prototype | Super Weapons, Gleipnir | F2 | Implemented: project `ac_sp_gleipnir` (LEA); Gandr stays reference only; not used in Aurelia's foundation |
| Nevera Jammer: originally an Aurelian weather observation radar in the Nevera mountains, converted by Leasath into a jamming station protecting Griswall and the Monte Breeze Industrial Area | Super Weapons, Nevera Jammer | F2 | Reference only: no conversion date and no mapped place; the crisis lanes do not script it |
| Meson Cannons: particle-beam point defence built into the Atmos Ring in Aurelia's capital | Super Weapons, Meson Cannons | F2 | Reference only: no construction date and no mapped place |
| Archelon Fortress: secret Leasathian manufacturing complex for the Fenrir on Sentry Island in the Danern Straits | Super Weapons, Archelon Fortress | F2 | Implemented: project `ac_sp_archelon` (LEA); Sentry Island unmapped; the Fenrir stays reference only |

## Statements only the abstracts and product pages carry

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Osea and Yuktobania improved relations after the Belkan War, agreed to reduce their armies and weapons of mass destruction and worked together on international space development | Abstracts, ACE COMBAT 5 | C | Context; the Arkbird co-operation is already sourced (1999 / 10.08). Not scripted |
| The Gray Men, renegade survivors of the Belkan War, secretly abducted Harling and Nikanor; Sea Goblin and Wardog rescued them; the two leaders exposed the conspiracy at a joint press conference and pro-peace factions joined Razgriz | Abstracts, ACE COMBAT 5 | C | Reference only. `ac_cpw.35` names the Gray Men as the Super Weapons row does; the abduction, rescue unit and factions are not scripted |
| Wardog is the Osean Air Defense Force 108th Tactical Fighter Squadron; Sand Island lies in the Ceres Ocean between Osea and Yuktobania | Product, ACE COMBAT 5 | C | Text only; not mapped |
| Estovakia's military regime collapsed in a coup and a ceasefire ended the Emmeria–Estovakia War | Abstracts, ACE COMBAT 6 | E | Pending with the 2016 / 04.01 row |
| Garuda Team is the 28th Fighter Squadron of the Emmerian Air Force's 8th Air Division | Abstracts and Product, ACE COMBAT 6 | E | Text only |
| Erusea proclaimed a "clean war"; Osean targeting blunders turned public opinion toward Erusea; a voluntary coalition of Osean forces and a traditionalist sect of the Erusean Army forced the surrender of the Erusean Army radicals; the ceasefire was signed in Expo City | Abstracts, ACE COMBAT 7 | F1 | Implemented in text: `ac_lhw.7`, `.22`, `.28`, the drones lane. No coalition, sect or faction is created |
| Erusea accuses Osea of massive overreach in their joint international projects | Product, ACE COMBAT 7 | F1 | Implemented in text: `ac_lhw.1`, `ac_lhw.5` |
| Leasath, just emerged from a civil war, cites "years of exploitation by Aurelia"; Aurelia lies on the southern tip of South Osea; the war ends in December 2020 with Navarro's downfall | Abstracts and Product, ACE COMBAT X | F2 | Implemented across `ac_lcw` and `ac_alc`. The cause is recorded as Leasath's stated claim, not fact |

## Open research gaps

- Precise territorial extents of the Estovakian factions and of occupied areas in
  2010, 2015–2016, 2019 and 2020. Nothing is mapped to states without a separate
  geography review.
- Officeholders and terms for 2006–2020 beyond those named above.
- Force structures and equipment availability; the conventional research
  programmes remain provisional gameplay.
- The start of the Leasath civil war is derived, not stated.
