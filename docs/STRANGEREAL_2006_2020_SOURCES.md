# Strangereal 2006–2020: source ledger (Gate 0)

Status: **sources and dispositions only.** This ledger gates every dated
participant, place, leader or weapon scripted for 2006–2020, as
[USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md) gated 1994–2005. A row here
does not mean the content is implemented; the disposition column says what is.

Primary sources, read 3 November 2026:

- [Official ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), cited as *Chronicle, YYYY / MM.DD*.
- [Official ACES Chronicle — Super Weapons](https://acecombat.jp/en/chronicle/weapons/), cited as *Super Weapons, &lt;name&gt;*.

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
| The Lyes Faction, later the Lyes United Front (LUF), seizes the Estovakian capital | Chronicle, 2007 / 04.03 | B | Owner stage `ac_ecw`; no tag or government change |
| The LUF suppresses cities that resist; other factions revolt and the civil war begins | Chronicle, 2007 / 06.30 | B | Owner stage; civil war is tagless |
| Estovakia's Eastern Faction takes and restores northeastern oil platforms held by a public corporation | Chronicle, 2008 / 07.15 | B | Owner stage and the Estovakian oil lane; no state or resource transfer |
| The Republic of Anea Initiative is put on hold because of internal strife in Estovakia | Chronicle, 2008 / 10.23 | B | New record flag only; the existing `ac_anea` bureau state is read, never written |
| Emmeria ends aid for the LUF's reconstruction programme because the LUF suppresses all opposition | Chronicle, 2010 / 02.19 | B | Emmerian aid lane; the historical route ends the aid, an earned conditional alternative continues it |
| Emmeria ends aid for Estovakia's reconstruction | Chronicle, 2011 / 05.09 | B | Emmerian aid lane |
| The Eastern Faction and the LUF clash; the LUF loses 80% of its territory in one week to new weapons and elite aviation units | Chronicle, 2013 / 01.15 | B | Owner stage (authority falls); no territory changes hands on the map |
| The LUF fights on but is defeated near the Emmerian border; General Lyes is killed and the civil war ends | Chronicle, 2013 / 10.29 | B | Historical outcome; earned negotiated settlement and provisional prolonged instability are alternatives |
| Estovakian Foreign Minister Isaac Arensky, former air marshal of the Northern Highlands Faction, is attacked; fifteen former LUF soldiers are arrested a week later | Chronicle, 2013 / 11.25 | B | Aftermath news only |
| Arensky dies; the death is withheld from the public | Chronicle, 2013 / 12.02 | B | Aftermath news only |
| The pilot Talisman joins the Republic of Emmeria Air Force and defends Gracemeria | Chronicle, 2013 / 12.23 | Reference only | Named pilot; not scripted |
| Arensky's death is announced; Antonina Koznick, a former Eastern Faction navy captain, succeeds him | Chronicle, 2014 / 02.03 | B | Aftermath news only; no character or leader is created |
| Former LUF members attack a relief-supply storage facility in the western city of Vistoc | Chronicle, 2014 / 02.04 | B | Aftermath news only |

## 2008: the Arkbird Summit

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| The Arkbird Summit is held | Chronicle, 2008 / 08.21 | C | Context for the Circum-Pacific War owner; not yet scripted |

## 2010: the Circum-Pacific War

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Unidentified aircraft appear at Cape Landers; Osea's Wardog Squadron engages and two aircraft survive | Chronicle, 2010 / 09.23 | C | Pending |
| An unidentified SR-71 appears over Osea and is hit by a coastal surface-to-air missile | Chronicle, 2010 / 09.24 | C | Pending |
| Wardog Squadron engages unidentified aircraft; Yuktobania declares war on Osea and attacks Port Saint Hewlett; the war begins | Chronicle, 2010 / 09.27 | C | Pending; the declaration is owned by the future `ac_cpw` owner |
| The submarine Scinfaxi sees first use; the carriers Vulture and Buzzard are sunk at the Eaglin Straits; Osea sends the Arkbird to the front | Chronicle, 2010 / 09.30 | C | Pending |
| Scinfaxi is sunk at Sand Island | Chronicle, 2010 / 10.04 | C | Pending |
| The Akerson Hill Incident | Chronicle, 2010 / 10.22 | C | Pending; the source gives the name only |
| Smuggled explosives destroy the Arkbird's engines | Chronicle, 2010 / 10.25 | C | Pending; interacts with `ac_sp_arkbird` |
| Osea invades the southeastern Yuktobanian mainland on the Bastok Peninsula | Chronicle, 2010 / 11.01 | C | Pending |
| Osean aircraft fire on an engineering college in Dresdene, killing several people | Chronicle, 2010 / 11.02 | C | Pending |
| Yuktobanian special forces use nerve gas in Bana and attack Apito International Airport | Chronicle, 2010 / 11.04 | C | Pending |
| The submarine Hrimfaxi is sunk in the Razgriz Straits | Chronicle, 2010 / 11.14 | C | Pending |
| Yuktobanian aircraft attack a peace ceremony in November City | Chronicle, 2010 / 11.29 | C | Pending |
| Osean forces bring down Cruik Fortress, Yuktobania's last defensive stronghold | Chronicle, 2010 / 12.06 | C | Pending |
| Peter N. Beagle and Albert Genette help suspected Wardog members flee; all are shot down by Captain Marcus Snow | Chronicle, 2010 / 12.07 | Reference only | Named individuals; not scripted |
| President Harling is rescued from Stier Castle in Belka; Razgriz Squadron forms under the president | Chronicle, 2010 / 12.09 | C | Pending |
| The Arkbird, carrying a nuclear weapon, attempts an attack on Okchabursk and is shot down by Razgriz Squadron | Chronicle, 2010 / 12.19 | C | Pending; `ac_sp_arkbird` stays non-weapon until this row is implemented |
| Former Prime Minister Seryozha Viktrovich Nikanor is rescued from imprisonment by the Yuktobanian military | Chronicle, 2010 / 12.23 | C | Pending |
| The Battle of Ceres Ocean | Chronicle, 2010 / 12.29 | C | Pending |
| The carrier Kestrel is sunk; Harling and Nikanor jointly ask their militaries to disarm; a mixed force inspects Gründer Industries in Sudentor, North Osea | Chronicle, 2010 / 12.30 | C | Pending |
| The SOLG is seen falling; Razgriz Squadron destroys the former Belkan Grabacr and Ofnir squadrons and the SOLG; the war ends | Chronicle, 2010 / 12.31 | C | Pending; end news must follow actual cessation |

## 2015–2016: the Emmeria–Estovakia War

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Yuktobanian spy satellites see a massive aircraft signature off Estovakia's southeast coast | Chronicle, 2015 / 04.21 | E | Pending |
| Ed Alverez takes command of the Gavial tank battalion; hostilities break out | Chronicle, 2015 / 06.10 | Reference only | Named individual; not scripted |
| Estovakia invades and seizes Gracemeria; the Aigaion cannot be countered; Emmerian forces retreat west and the war begins | Chronicle, 2015 / 08.30 | E | Pending |
| Freddie Durand (Avalanche) leads the 2nd Strike Fighter Squadron | Chronicle, 2015 / 09.12 | Reference only | Named pilot; not scripted |
| Witnesses see giant fireballs attacking retreating Emmerian forces | Chronicle, 2015 / 11.XX | E | Pending; day unknown |
| Emmerian forces at Campagna Airport intercept bombers sent toward Vitoze on Khesed Island | Chronicle, 2015 / 11.24 | E | Pending |
| Emmerian ground forces break through at Sipli Field | Chronicle, 2015 / 11.27 | E | Pending |
| Bartolomeo Fortress falls; Emmeria controls Khesed Island | Chronicle, 2015 / 12.27 | E | Pending |
| Emmeria lands at Rargom Beach | Chronicle, 2016 / 01.26 | E | Pending |
| Emmerian forces advance along the Selumna Peaks | Chronicle, 2016 / 02.12 | E | Pending |
| Emmeria captures Cavallia Air Force Base in San Loma | Chronicle, 2016 / 02.15 | E | Pending |
| The Emmerian Air Force destroys the Aerial Fleet | Chronicle, 2016 / 02.20 | E | Pending |
| Emmeria strikes Ragno Fortress in Grageo Canyon | Chronicle, 2016 / 03.06 | E | Pending |
| Battle in the Moloch Desert; Estovakia retreats | Chronicle, 2016 / 03.25 | E | Pending |
| Emmeria assaults Fort Norton and stops transport of weapons catalysts | Chronicle, 2016 / 03.26 | E | Pending |
| Gracemeria is liberated; cruise missiles fired at it that night are shot down | Chronicle, 2016 / 03.31 | E | Pending |
| The Chandelier on Sonne Island is destroyed; Gustav Dvornik dies; an antigovernment coup in Estovakia leads to a ceasefire | Chronicle, 2016 / 04.01 | E | Pending |

## 2019: the Lighthouse War and the Leasath civil war

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Drone strikes hit four Osean naval ports; Erusea declares war on Osea and captures the International Space Elevator; the Lighthouse War begins | Chronicle, 2019 / 05.15 | F1 | Pending |
| Osea and the IUN Peacekeeping Force begin Operation Eastern Wind | Chronicle, 2019 / 05.17 | F1 | Pending |
| A two-pronged offensive on Chopinburg airspace and Farbanti fails; the carrier Kestrel II is sunk | Chronicle, 2019 / 05.30 | F1 | Pending |
| Former president Vincent Harling dies in a rescue attempt at the space elevator | Chronicle, 2019 / 06.06 | F1 | Pending; news only |
| Osea forms the Long Range Strategic Strike Group | Chronicle, 2019 / 08.10 | F1 | Pending |
| Osea reactivates a Stonehenge battery and shoots down the Arsenal Bird Liberty | Chronicle, 2019 / 08.19 | F1 | Pending; interacts with `ac_sp_stonehenge` |
| Osea attacks Farbanti; destroying military satellites cuts communications across Usea | Chronicle, 2019 / 09.19 | F1 | Pending |
| Shilage and other small nations annexed by Erusea declare independence; Erusea refuses and internal conflict follows | Chronicle, 2019 / 10.01 | F1 | Pending; uses the existing Shilage release contracts only after review |
| General Édouard Labarthe is killed by Osean forces | Chronicle, 2019 / 10.10 | F1 | Pending; news only |
| Osean and Erusean forces clash at the space elevator; the Arsenal Bird Justice is shot down | Chronicle, 2019 / 10.31 | F1 | Pending |
| Osea and Erusea sign a ceasefire at the Expo City Conference | Chronicle, 2019 / 12.01 | F1 | Pending |
| The Leasath civil war ends after ten years of fighting | Chronicle, 2019 / XX.XX | F2 | Day and month unknown. Derived: the war began about 2009. Aurelia's foundation refers to it from 2010 as context only |

## 2020: the Aurelia–Leasath war

Every 2020 entry gives a month at most.

| Claim | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Leasath declares war on the Federal Republic of Aurelia, citing years of exploitation; the Gleipnir helps it occupy all of Aurelia except Aubrey Base | Chronicle, 2020 / 10.XX | F2 | Pending crisis lanes. "Years of exploitation" is recorded as Leasath's stated cause, not as fact |
| Aurelia's Gryphus Squadron repels an attack on Aubrey Base | Chronicle, 2020 / 10.XX | F2 | Pending |
| Aurelia retakes Port Patterson | Chronicle, 2020 / 11.XX | F2 | Pending |
| Aurelia disables Gleipnir's stealth and shoots it down; Santa Elva is liberated | Chronicle, 2020 / 11.XX | F2 | Pending |
| Aurelia retakes Sachana Air Base in the Raven Woods | Chronicle, 2020 / 12.XX | F2 | Pending |
| Aurelia retakes its capital, Griswall; Leasathian forces regroup at Archelon Fortress | Chronicle, 2020 / XX.XX | F2 | Pending. Griswall is named as the capital, so it may appear in Aurelian text |
| Archelon Fortress is destroyed; Leasath's commander Diego Navarro is removed from office and the war ends | Chronicle, 2020 / 12.XX | F2 | Pending |

## Super Weapons active in the period

| Weapon | Exact source | Wave | Disposition |
| --- | --- | --- | --- |
| Chandelier: Estovakian railgun built against Ulysses fragments, incomplete when the asteroid arrived, later weaponized in the Emmeria–Estovakia War and destroyed | Super Weapons, Chandelier | B (custody only), E | Already recorded as incomplete by the Anea campaign. Wave B keeps the research team in custody only; weaponization belongs to Wave E |
| Arkbird: Osean–Yuktobanian low-orbit spacecraft for clearing Ulysses fragments | Super Weapons, Arkbird | C | `ac_sp_arkbird` stays a non-weapon project until the 2010 rows are implemented |
| SOLG: Osean Cold War orbital railgun, abandoned after the Belkan War, revived by the Gray Men with a V2 warhead | Super Weapons, SOLG | C | Pending; the Gray Men are named only as the source names them |
| Scinfaxi and Hrimfaxi: Yuktobanian nuclear-powered submarine carriers | Super Weapons, Scinfaxi & Hrimfaxi | C | Pending |
| Aigaion, Gyges, Kottos: Estovakian heavy command cruiser and support platforms of the Aerial Fleet Initiative (P/F-X), based on Belkan technology | Super Weapons, Aigaion; Gyges; Kottos | E | Pending; no construction date is given, so any timing is provisional |
| Arsenal Birds Liberty and Justice: Osean unmanned aircraft defending the International Space Elevator | Super Weapons, Arsenal Birds | F1 | Pending |
| Alicorn: Erusean Royal Navy submarine aviation cruiser | Super Weapons, Alicorn | F1 | Pending |
| Gleipnir and its prototype Gandr: Leasathian aerial fortress and prototype | Super Weapons, Gleipnir | F2 | Pending; not used in Aurelia's foundation |
| Nevera Jammer: originally an Aurelian weather observation radar in the Nevera mountains, converted by Leasath into a jamming station protecting Griswall and the Monte Breeze Industrial Area | Super Weapons, Nevera Jammer | F2 | The pre-war Aurelian weather radar may appear in Aurelia's foundation as a civil service; its construction date is unknown and is not scripted. The jammer belongs to the crisis lanes |
| Meson Cannons: particle-beam point defence built into the Atmos Ring in Aurelia's capital | Super Weapons, Meson Cannons | F2 | Pending; no construction date is given |
| Archelon Fortress: secret Leasathian manufacturing complex for the Fenrir on Sentry Island in the Danern Straits | Super Weapons, Archelon Fortress | F2 | Pending |

## Open research gaps

- Precise territorial extents of the Estovakian factions and of occupied areas in
  2010, 2015–2016, 2019 and 2020. Nothing is mapped to states without a separate
  geography review.
- Officeholders and terms for 2006–2020 beyond those named above.
- Force structures and equipment availability; the conventional research
  programmes remain provisional gameplay.
- The start of the Leasath civil war is derived, not stated.
