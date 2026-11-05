"""The Belkan War record, 1991-1999: reference briefs beside the inherited archive.

Owner only; no focuses, decisions or ideas. Each brief is a news event that
fires once, on observed state, never as a second trigger for anything the
archive already owns. A brief fires only inside its window; a brief whose
window closes first (a late save, a war that never came, a route the record
does not describe) is marked skipped and never fires afterwards.

Source layers
-------------
Official (ACES Chronicle, read 4 November 2026; compiled in
docs/BELKAN_WAR_SOURCES.md): 1991 / 07.29, 09.02, 12.16; 1995 / 03.27, 03.30,
04.01, 04.03, 04.24, 05.13, 05.14, 06.05, 10.18; 1996 / 04.18; 1999 / 09.16.
Named people, squadrons, places and ships appear only in event text, as the
Chronicle names them; none is mapped, created or scripted.

Mod provenance, read only: the archive's Belkan War (`belkan_war_is_happening`,
`BLK_sell_the_land`), the factions and wars it creates and Ustio's capital,
state 335 (Directus).

Provisional gameplay: the windows and the observed conditions that stand in
for places the map does not have.

The archive's own events for 1992 / 02.24, 1995 / 05.23, 06.04 and 06.06 stay
their owners; the ledger records their citations instead of a second event.
"""
from content_waves.framework import Wave, block, guard

P = "ac_bwr"
WAVE = Wave(
    prefix=P, infix="bwr", label="The Belkan War Record", source="tools/content_waves",
    countries={}, eligible="", branches=(), layout={}, openings={}, finals={}, final_ready={},
    themes={}, extra_tags=("BLK", "OSE", "UST"),
)

WAR = "has_global_flag = belkan_war_is_happening country_exists = BLK"
DIRECTUS = 335

# (name, number, "date >" anchor, last day of the window, observed condition, title, prose, option, picture)
BRIEFS = (
    ("kestrel_ordered", 1, "1991.7.28", "1991.8.28", "",
     "Osea Orders the Kestrel",
     "The Osean Maritime Defense Force has ordered the Kestrel, the seventh Hubert-class aircraft carrier (ACES Chronicle, 1991 / 07.29).\n\nThe record gives the order and the class; this campaign builds no ship from it.",
     "Note the order.", "ac_bwr_news_kestrel"),
    ("cinigrad", 2, "1991.9.1", "1991.10.2", "",
     "Submarines Announced at Cinigrad",
     "Scinfaxi-class submarines have been announced at a political convention in Cinigrad, Yuktobania, and Osean Foreign Minister Howards has belittled them (ACES Chronicle, 1991 / 09.02).\n\nCinigrad is not on this map, and the class enters this campaign only in 2010.",
     "Note the announcement.", "ac_bwr_news_cinigrad"),
    ("borders_redrawn", 3, "1991.12.15", "1992.12.31", "country_exists = BLK BLK = { has_completed_focus = BLK_sell_the_land }",
     "Belkan Borders Redrawn",
     "The ACES Chronicle records that Belkan borders were redrawn on 16 December 1991 (1991 / 12.16), after Belka sold land to its neighbours.\n\nIn this campaign the land sales themselves moved the states when Belka made them. This brief records the official date and changes no border.",
     "Note the new map.", "ac_bwr_news_borders"),
    ("model", 4, "1995.3.26", "1995.12.31", f"{WAR} BLK = {{ has_war_with = GEB }}",
     "Assault on Model",
     "The ACES Chronicle records an assault on Model, a Gebetian border city, on Belka's eastern front (1995 / 03.27).\n\nModel is not on this map. This brief reports the record because Belka and Gebet are actually at war; the archive's own raids are separate events.",
     "Note the eastern front.", "ac_bwr_news_model"),
    ("monte_rosa", 5, "1995.3.29", "1995.12.31",
     f"{WAR} OR = {{ AND = {{ country_exists = UST UST = {{ has_capitulated = yes }} }} BLK = {{ controls_state = {DIRECTUS} }} }}",
     "Ustio Under Belkan Control",
     "Nearly all of Ustio has fallen under Belkan control, and Belkan and Ustian air forces have clashed over Monte Rosa (ACES Chronicle, 1995 / 03.30).\n\nMonte Rosa is not on this map. This brief reports the record because Belkan forces actually hold Directus, or Ustio has actually capitulated; no state was moved by script.",
     "Note the occupation.", "ac_bwr_news_monte_rosa"),
    ("ustio_allies", 6, "1995.3.31", "1995.12.31",
     f"{WAR} country_exists = UST country_exists = OSE UST = {{ is_in_faction_with = OSE }}",
     "Ustio Allies with Osea",
     "Ustio has allied with Osea and begun its resistance (ACES Chronicle, 1995 / 04.01).\n\nThis brief reports the record because Ustio is actually in a faction with Osea. The record names only Ustio and Osea; the archive's own alliance events stay their owners.",
     "The resistance begins.", "ac_bwr_news_ustio"),
    ("osean_army", 7, "1995.4.2", "1995.12.31", f"{WAR} country_exists = OSE OSE = {{ has_war_with = BLK }}",
     "The Osean Army Resists",
     "The Osean Army has begun its resistance (ACES Chronicle, 1995 / 04.03).\n\nThis brief reports the record because Osea is actually at war with Belka; how the war reached Osea is the archive's own course.",
     "Note the front.", "ac_bwr_news_osean_army"),
    ("futuro_canal", 8, "1995.4.23", "1995.12.31", f"{WAR} country_exists = OSE OSE = {{ has_war_with = BLK }}",
     "Offensive Campaign No. 4101",
     "The Allied Forces have begun Offensive Campaign No. 4101 to drive Belka from Futuro Canal and secure a sea supply line, and the Osean carrier Kestrel has made its test voyage (ACES Chronicle, 1995 / 04.24).\n\nFuturo Canal is map geography here; no operation is scripted.",
     "Note the campaign.", "ac_bwr_news_futuro"),
    ("directus", 9, "1995.5.12", "1995.12.31",
     f"has_global_flag = ac_bwr_directus_occupied country_exists = UST UST = {{ controls_state = {DIRECTUS} }}",
     "Directus Liberated",
     "The Allied Forces have liberated Ustio's capital, Directus (ACES Chronicle, 1995 / 05.13). The Chronicle records that the independent country was restored to its prewar state the next day (1995 / 05.14).\n\nThis brief reports the record because Ustio actually controls Directus again after Belkan occupation. It observes Directus only; no state was moved by script.",
     "Directus is free.", "ac_bwr_news_directus"),
    ("waldreich", 10, "1995.6.4", "1995.7.31", f"{WAR}",
     "The Battle of Waldreich",
     "The ACES Chronicle records the Battle of Waldreich (1995 / 06.05). The Osean Wizard and Sorcerer squadrons left the front, and contact with them was lost.\n\nThe archive's Wacht am Waldreich branch is a different, Belkan mechanic; this brief adds nothing to it.",
     "Note the record.", "ac_bwr_news_waldreich"),
    ("espada", 11, "1995.10.17", "1995.11.17", "",
     "Espada Team Missing",
     "Espada Team has disappeared from a base of the Kingdom of Sapin (ACES Chronicle, 1995 / 10.18).\n\nThe record gives the disappearance only, and this campaign adds nothing to it.",
     "Note the record.", "ac_bwr_news_espada"),
    ("tyler", 12, "1996.4.17", "1996.5.18", "",
     "A New Chief of Staff",
     "The FCU Army has announced that Commander Robert Tyler, 54, will replace the Riass Armed Forces Chief of Staff, who died on 20 March (ACES Chronicle, 1996 / 04.18).\n\nThe Chronicle's wording is kept as written. No officeholder changes in this campaign.",
     "Note the appointment.", "ac_bwr_news_tyler"),
    ("kestrel_commissioned", 13, "1999.9.15", "1999.10.16", "",
     "The Kestrel Commissioned",
     "The Osean carrier Kestrel has been commissioned (ACES Chronicle, 1999 / 09.16).\n\nThe record gives the commissioning; this campaign builds no ship from it.",
     "Note the commissioning.", "ac_bwr_news_kestrel"),
)


def owner():
    effects, triggers, loc, events = {}, {}, {}, []
    tick = ""
    # Directus is remembered as occupied while the war runs and Belka holds it.
    tick += guard(f"NOT = {{ has_global_flag = ac_bwr_directus_occupied }} {WAR} date > 1995.3.29 date < 1996.1.1 BLK = {{ controls_state = {DIRECTUS} }}",
                  "set_global_flag = ac_bwr_directus_occupied")
    for name, number, after, last, condition, title, prose, option, picture in BRIEFS:
        flag = f"ac_bwr_{name}"
        observed = f"date < {last}" + (" " + condition if condition else "")
        tick += guard(f"date > {after} NOT = {{ has_global_flag = {flag} }} NOT = {{ has_global_flag = {flag}_skipped }}",
                      guard(observed, f"set_global_flag = {flag}\nnews_event = {{ id = {P}.{number} days = 1 }}") +
                      block("else_if", block("limit", f"NOT = {{ date < {last} }}") + f"set_global_flag = {flag}_skipped"))
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, option
        events.append(block("news_event", f"id = {P}.{number}\ntitle = {P}.{number}.t\ndesc = {P}.{number}.d\npicture = GFX_{picture}\n"
                            "is_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" + block("option", f"name = {P}.{number}.a")))
        loc[flag] = "Belkan War record: " + title
        loc[flag + "_skipped"] = "Belkan War record: " + title + " (window passed; not reported)"
    loc["ac_bwr_directus_occupied"] = "Belkan War record: Directus was under Belkan control"
    effects["ac_bwr_tick"] = tick
    # Either principal's weekly pulse observes; the flags make a second call a no-op.
    hooks = {"on_weekly_OSE": "ac_bwr_tick = yes", "on_weekly_BLK": "ac_bwr_tick = yes", "on_weekly_UST": "ac_bwr_tick = yes"}
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=[], events=events, custom="",
                categories=[], decisions={}, hooks=hooks)


# Registry declarations ------------------------------------------------------
KEY = "BW"
NAME = "belkan_record"
LEDGER = "docs/BELKAN_WAR_SOURCES.md"
SOURCES = {"official": ["Chronicle 1991 / 07.29, 09.02, 12.16", "Chronicle 1995 / 03.27-06.05 and 10.18",
                        "Chronicle 1996 / 04.18 and 1999 / 09.16"],
           "mod_provenance": "The archive's Belkan War, factions, land sale and Ustio's capital, read only",
           "provisional_gameplay": "The windows and the observed conditions that stand in for unmapped places"}
COUNTRIES = {}
NEWS_ART = (("ac_bwr_news_kestrel", ("carrier", "navy"), "The Kestrel", "OSE"),
            ("ac_bwr_news_cinigrad", ("submarine", "assembly"), "Submarines Announced at Cinigrad", "YUK"),
            ("ac_bwr_news_borders", ("document", "scales"), "Belkan Borders Redrawn", "BLK"),
            ("ac_bwr_news_model", ("gate", "command"), "Assault on Model", "GEB"),
            ("ac_bwr_news_monte_rosa", ("air", "radar"), "Ustio Under Belkan Control", "UST"),
            ("ac_bwr_news_ustio", ("diplomacy", "air"), "Ustio Allies with Osea", "UST"),
            ("ac_bwr_news_osean_army", ("command", "security"), "The Osean Army Resists", "OSE"),
            ("ac_bwr_news_futuro", ("logistics", "navy"), "Offensive Campaign No. 4101", "OSE"),
            ("ac_bwr_news_directus", ("peace", "civil"), "Directus Liberated", "UST"),
            ("ac_bwr_news_waldreich", ("air", "telescope"), "The Battle of Waldreich", "BLK"),
            ("ac_bwr_news_espada", ("air", "document"), "Espada Team Missing", "SAP"),
            ("ac_bwr_news_tyler", ("assembly", "document"), "A New Chief of Staff", "FCU"))
EVENT_ART = ()
OWNER_ART = {}
