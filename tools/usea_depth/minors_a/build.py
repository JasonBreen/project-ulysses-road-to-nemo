"""Compile the Usea Depth minor states A package (CHO PLA FRU ALR DOR SCA BLD).

python -B tools/usea_depth/minors_a/build.py            write the script and localisation outputs
python -B tools/usea_depth/minors_a/build.py --check    compare them with the committed files; never writes
python -B tools/usea_depth/minors_a/build.py --validate [TAG]   authoring checks only; never writes

Each state owns one new focus tree, ac_ud_<tag>_tree, that outranks the shared
regional tree for that tag. Governments change only through the package's
ac_ud_minors_a_regime_* effects. Art is compiled separately by build_art.py.
"""
import argparse
import json
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import content as C  # noqa: E402
from content import seams  # noqa: E402

MOD = C.MOD
ROOT = C.ROOT
NOTE = "# Usea Depth minor states A: provisional gameplay; source tools/usea_depth/minors_a (owner: build.py).\n"
OWN_LOC = "localisation/english/ac_ud_minors_a_l_english.yml"
FILES = {
    "events": "events/ac_ud_minors_a.txt",
    "ideas": "common/ideas/ac_ud_minors_a.txt",
    "effects": "common/scripted_effects/ac_ud_minors_a.txt",
    "decisions": "common/decisions/ac_ud_minors_a.txt",
    "characters": "common/characters/ac_ud_minors_a.txt",
}


def focus_file(tag):
    return "common/national_focus/ac_ud_minor_%s.txt" % tag.lower()


def block(key, body):
    lines = body.strip("\n").splitlines()
    return key + " = {\n" + "".join(("\t" + line if line else "") + "\n" for line in lines) + "}\n"


# ------------------------------------------------------------------ helpers

def event_numbers(state):
    base = C.EVENT_BASE[state.tag]
    return {event.slug: base + index + 1 for index, event in enumerate(state.events)}


def event_body(event):
    return seams.event_text(event.paragraphs, event.layer, event.citation)


def office(state, gov):
    return C.office_id(state.tag, gov.slug)


def portrait_sprite(ident):
    return "GFX_ac_ud_portrait_" + ident


def event_picture(tag, kind):
    return "GFX_ac_ud_event_%s_%s" % (tag.lower(), kind)


def existing_localisation():
    keys = {}
    folder = MOD / "localisation/english"
    for path in sorted(folder.rglob("*.yml")):
        if path.relative_to(MOD).as_posix() == OWN_LOC:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for match in re.finditer(r'^\s*([\w.\-]+):\d*\s+"', text, re.M):
            keys.setdefault(match[1], path.relative_to(MOD).as_posix())
    return keys


def modifier_whitelist():
    keys = set()
    for path in sorted((MOD / "common/ideas").glob("*.txt")):
        if path.name == Path(FILES["ideas"]).name:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for match in re.finditer(r"\bmodifier\s*=\s*\{([^{}]*)\}", text):
            keys.update(re.findall(r"(\w+)\s*=\s*-?[\d.]+", match[1]))
    return keys - {"add", "factor", "disabled_ideas"}


def modifier_pairs(text):
    return re.findall(r"(\w+)\s*=\s*(-?[\d.]+)", text)


# ------------------------------------------------------------------ validation

def authored_texts(state):
    """(kind:slug, text) for every authored string; only event bodies may hold paragraph breaks."""
    yield "tree", state.tree_title + " " + state.tree_desc
    for focus in state.focuses:
        yield "focus:" + focus.slug, focus.title + " " + focus.desc
    for idea in state.ideas:
        yield "spirit:" + idea.slug, idea.title + " " + idea.desc
    for gov in state.governments:
        yield "government:" + gov.slug, gov.title + " " + gov.desc
    for event in state.events:
        yield "event:" + event.slug, event.title + "\n\n" + "\n\n".join(event.paragraphs)
        for text, _ in event.options:
            yield "option:" + event.slug, text
    for slug, text in state.flags.items():
        yield "flag:" + slug, text
    for slug, text in state.tooltips.items():
        yield "tooltip:" + slug, text
    for party, text in state.country_names.items():
        yield "name:" + party, text


def validate_state(state, whitelist=None, existing=None):
    problems = []
    tag = state.tag

    def need(condition, message):
        if not condition:
            problems.append("%s: %s" % (tag, message))

    focuses = {f.slug: f for f in state.focuses}
    need(len(focuses) == len(state.focuses), "duplicate focus slugs")
    need(55 <= len(state.focuses) <= 66, "focus count %d outside 55-66" % len(state.focuses))
    need(state.root in focuses, "root focus missing")
    ideas = {i.slug: i for i in state.ideas}
    govs = {g.slug: g for g in state.governments}
    events = {e.slug: e for e in state.events}
    need(2 <= len(govs) <= 3, "needs two or three political paths")
    need(len(events) >= len(focuses) // 5, "needs about one event per five focuses (%d for %d)" % (len(events), len(focuses)))
    whitelist = whitelist if whitelist is not None else modifier_whitelist()
    focus_ids = {C.fid(tag, f.slug) for f in state.focuses}
    idea_ids = {C.idea_id(tag, i.slug): i.slug for i in state.ideas}
    flag_ids = {C.fid(tag, s) for s in state.flags} | {C.fid(tag, "programme_adopted")}
    tip_ids = {C.fid(tag, s) + "_tt" for s in state.tooltips}
    known = focus_ids | set(idea_ids) | flag_ids | tip_ids
    every = (list(focus_ids) + list(idea_ids) + list(flag_ids) + list(tip_ids)
             + [C.office_id(tag, g.slug) for g in state.governments])
    clashes = sorted(k for k, n in Counter(i.lower() for i in every).items() if n > 1)
    need(not clashes, "IDs or localisation keys collide: " + ", ".join(clashes))
    for slug in state.tooltips:
        need(slug in focuses, "tooltip %s does not name a focus" % slug)

    for focus in state.focuses:
        ident = C.fid(tag, focus.slug)
        need(re.fullmatch(r"[a-z][a-z0-9_]*", focus.slug) is not None, "bad slug " + focus.slug)
        need(0 <= focus.x <= C.MAX_X and focus.y >= 0, ident + " outside x 0-23")
        need(focus.cost in (5, 10), ident + " cost must be 5 or 10")
        need(focus.era in C.ERAS, ident + " unknown era " + focus.era)
        need(len(focus.icon) == 2 and focus.icon[0] != focus.icon[1] and set(focus.icon) <= C.SUBJECTS, ident + " icon subjects")
        need(seams.title_fits(focus.title), ident + " title does not fit three caption lines")
        need(len(focus.desc.split()) >= 18, ident + " description under 18 words")
        if focus.slug == state.root:
            need(not focus.req, "root has prerequisites")
        else:
            need(bool(focus.req), ident + " has no prerequisite")
        for group in C.requirement_groups(focus):
            for ref in group:
                need(ref in focuses, ident + " requires unknown " + ref)
                if ref in focuses:
                    need(focuses[ref].y < focus.y, ident + " sits above its prerequisite " + ref)
        for ref in focus.excl:
            need(ref in focuses and ref != focus.slug, ident + " excludes unknown " + ref)
        if focus.event:
            need(focus.event in events, ident + " fires unknown event " + focus.event)
        if focus.regime:
            need(focus.regime in govs, ident + " applies unknown government " + focus.regime)
        reward = focus.reward
        need(not seams.banned_uses(reward), ident + " banned effect " + str(seams.banned_uses(reward)))
        need("set_politics" not in reward and "set_popularities" not in reward, ident + " changes politics outside a regime effect")
        need("ac_ud_minors_a_regime_" not in reward, ident + " calls a regime effect directly; use regime=")
        need(not re.search(r"\bac_ucw_\w+\s*=", reward.replace("has_global_flag = ac_ucw_", "")), ident + " writes ac_ucw state")
        for token in re.findall(r"\b(%s_ud_\w+)" % tag, reward + "\n" + focus.avail):
            need(token in known, ident + " references undefined " + token)
        for other in re.findall(r"\b([A-Z]{3})_ud_", reward + focus.avail):
            need(other == tag, ident + " touches another package's IDs " + other)
        for state_id in re.findall(r"\b(\d{1,3})\s*=\s*\{|\bstate\s*=\s*(\d{1,3})\b", reward):
            number = int(state_id[0] or state_id[1])
            need(number in state.owned_states, ident + " scopes a state it does not own: %d" % number)
        need(not re.search(r"\b(?:random_owned_state|every_owned_state|random_state|every_state|capital_scope)\b", reward),
             ident + " uses an unscoped state iterator; name an owned state instead")
    factories = sum(f.reward.count("type = %s " % kind) for f in state.focuses for kind in C.FACTORIES)
    need(factories <= 3, "%d factory buildings; at most three, so no factory filler" % factories)
    # Every focus is reachable from the root.
    reach = {state.root}
    changed = True
    while changed:
        changed = False
        for focus in state.focuses:
            if focus.slug not in reach and focus.req and all(any(ref in reach for ref in group) for group in C.requirement_groups(focus)):
                reach.add(focus.slug)
                changed = True
    need(reach == set(focuses), "unreachable focuses " + ", ".join(sorted(set(focuses) - reach)))
    # Caption geometry: the shipped focus row pitch (96 x 160) against a 147 x 54 caption.
    for a, b in combinations(state.focuses, 2):
        if abs(a.x - b.x) * 96 < 147 and abs(a.y - b.y) * 160 < 54:
            need(False, "caption overlap %s (%d,%d) and %s (%d,%d)" % (a.slug, a.x, a.y, b.slug, b.x, b.y))
    # Governments: each applied by exactly one focus.
    applied = Counter(f.regime for f in state.focuses if f.regime)
    for slug, gov in govs.items():
        need(applied[slug] == 1, "government %s applied by %d focuses" % (slug, applied[slug]))
        need(gov.party in ("democratic", "communism", "fascism", "neutrality", "monarchism"), slug + " unknown party")
        need(sum(gov.popularities.values()) == 100 and gov.popularities.get(gov.party, 0) >= 40, slug + " popularities must total 100 with the ruling party at 40+")
        need(gov.icon in C.SUBJECTS, slug + " office icon subject")
        need(seams.title_fits(gov.title, 200, 2), slug + " office title too long")
    regime_focuses = [f for f in state.focuses if f.regime]
    for a, b in combinations(regime_focuses, 2):
        need(b.slug in a.excl or a.slug in b.excl, "political paths %s and %s are not mutually exclusive" % (a.slug, b.slug))
    # Ideas: each is granted somewhere and uses only modifiers already used by mod spirits.
    granted = Counter()
    for text in [f.reward for f in state.focuses] + [effects for event in state.events for _, effects in event.options]:
        for token in re.findall(r"(?:add_ideas = |add_idea = |idea = )(%s_ud_\w+)" % tag, text):
            granted[token] += 1
    for ident, slug in idea_ids.items():
        idea = ideas[slug]
        need(granted[ident] > 0, "idea %s is never granted" % slug)
        need(len(idea.icon) == 2 and set(idea.icon) <= C.SUBJECTS and idea.icon[0] != idea.icon[1], "idea %s icon subjects" % slug)
        pairs = modifier_pairs(idea.modifier)
        need(bool(pairs), "idea %s has no modifier" % slug)
        names = [k for k, _ in pairs]
        need(len(names) == len(set(names)), "idea %s repeats a modifier" % slug)
        for name in names:
            need(name in whitelist, "idea %s uses unchecked modifier %s" % (slug, name))
    # Every flag that is set or read is one of this state's labelled flags.
    for text in [f.reward + "\n" + f.avail for f in state.focuses] + [effects for event in state.events for _, effects in event.options]:
        for name in re.findall(r"(?:has|set|clr)_country_flag = (\w+)", text):
            need(name in flag_ids, "unlabelled country flag " + name)
        need("has_global_flag" not in text or not re.search(r"has_global_flag = (?!ac_ucw_|ac_sp_)", text), "reads an unlabelled global flag")
    # Events. Branch openers (a focus whose children are mutually exclusive) and
    # political turns run well past the long-form minimum.
    fired = Counter(f.event for f in state.focuses if f.event)
    for focus in state.focuses:
        if not focus.event or focus.event not in events:
            continue
        children = [f for f in state.focuses if any(focus.slug in group for group in C.requirement_groups(f))]
        opener = focus.regime or any(child.excl for child in children)
        words = len(" ".join(events[focus.event].paragraphs).split())
        if opener:
            need(words >= C.OPENER_WORDS, "event %s opens a branch or political turn and needs %d+ words (has %d)" % (focus.event, C.OPENER_WORDS, words))
    for slug, event in events.items():
        need(fired[slug] == 1, "event %s fired by %d focuses" % (slug, fired[slug]))
        need(event.picture in C.PICTURES, "event %s picture kind" % slug)
        need(1 <= len(event.options) <= 3, "event %s needs one to three options" % slug)
        need(seams.title_fits(event.title, 400, 2), "event %s title too long" % slug)
        for problem in seams.event_problems(event_body(event)):
            need(False, "event %s: %s" % (slug, problem))
        for text, effects in event.options:
            need(not seams.banned_uses(effects) and "regime" not in effects and "set_politics" not in effects, "event %s option effect not allowed" % slug)
            need(len(text) <= 110, "event %s option text too long" % slug)
            for token in re.findall(r"\b(%s_ud_\w+)" % tag, effects):
                need(token in known, "event %s option references undefined %s" % (slug, token))
    # Text hygiene.
    for slug, text in authored_texts(state):
        need(not any(c in text for c in "\u201c\u201d\u2018\u2019"), slug + " curly quotes")
        need(text.isascii(), slug + " uses non-ASCII characters the shipped fonts may lack")
        need("\u00a7" not in text and "$" not in text and "[" not in text, slug + " uses formatting or scripted text")
        for phrase in C.IMPACT_GEOGRAPHY:
            need(phrase not in text.lower(), "%s states where Ulysses fragments fell: '%s'" % (slug, phrase))
        for name in C.CHRONICLE_PLACES + C.PLACEHOLDER_NAMES:
            need(not re.search(r"\b%s\b" % re.escape(name), text), "%s mentions %s" % (slug, name))
        need("\n" not in text or slug.startswith("event:"), slug + " contains a raw line break")
    # Country names for each regime party exist, or are supplied here.
    existing = existing if existing is not None else existing_localisation()
    for gov in state.governments:
        key = "%s_%s" % (tag, gov.party)
        need(key in existing or gov.party in state.country_names, "missing country name " + key)
        if gov.party in state.country_names:
            need(key not in existing, "country name %s already exists in %s" % (key, existing.get(key)))
    return problems


def validate(states):
    whitelist = modifier_whitelist()
    existing = existing_localisation()
    problems = []
    for state in states:
        problems.extend(validate_state(state, whitelist, existing))
    return problems


# ------------------------------------------------------------------ compilation

def compile_state(state, loc):
    tag = state.tag
    rewards_note = []
    numbers = event_numbers(state)
    excludes = {f.slug: set(f.excl) for f in state.focuses}
    for focus in state.focuses:
        for ref in focus.excl:
            excludes.setdefault(ref, set()).add(focus.slug)
    max_x = max(f.x for f in state.focuses)
    nodes = []
    for focus in state.focuses:
        ident = C.fid(tag, focus.slug)
        body = "id = %s\nicon = GFX_ac_ud_focus_%s\nx = %d\ny = %d\ncost = %d\n" % (ident, ident, focus.x, focus.y, focus.cost)
        for group in C.requirement_groups(focus):
            body += block("prerequisite", "\n".join("focus = " + C.fid(tag, ref) for ref in group))
        if excludes.get(focus.slug):
            body += block("mutually_exclusive", "\n".join("focus = " + C.fid(tag, ref) for ref in sorted(excludes[focus.slug])))
        available = " ".join(part for part in (C.ERAS[focus.era], focus.avail.strip()) if part)
        if focus.regime:
            available = (available + " has_capitulated = no").strip()
        if available:
            body += block("available", available)
        weight = 0 if focus.regime else focus.ai
        body += "ai_will_do = { factor = %d }\n" % weight
        reward = focus.reward.strip("\n")
        if focus.regime:
            reward = (C.regime_name(tag, focus.regime) + " = yes\n" + reward).strip("\n")
        if focus.event:
            reward += "\ncountry_event = { id = %s.%d }" % (C.NAMESPACE, numbers[focus.event])
        body += block("completion_reward", reward.strip("\n") or "add_stability = 0")
        nodes.append(block("focus", body))
        loc[ident] = focus.title
        loc[ident + "_desc"] = focus.desc
    tree = C.tree_id(tag)
    header = ("id = %s\ncountry = { factor = 0 modifier = { add = %d tag = %s original_tag = %s } }\ndefault = no\nreset_on_civilwar = no\n"
              "continuous_focus_position = { x = %d y = 16 }\ninitial_show_position = { focus = %s }\n"
              % (tree, C.WEIGHT, tag, tag, (max_x + 4) * 96, C.fid(tag, state.root)))
    loc[tree] = state.tree_title
    loc[tree + "_desc"] = state.tree_desc
    text = NOTE + block("focus_tree", header + "\n".join(nodes))
    return text


def compile_ideas(states, loc):
    rows = []
    for state in states:
        for idea in state.ideas:
            ident = C.idea_id(state.tag, idea.slug)
            rows.append(block(ident, "picture = %s\nallowed = { always = no }\nallowed_civil_war = { always = yes }\nremoval_cost = -1\n%s"
                              % (C.idea_picture(state.tag, idea.slug), block("modifier", idea.modifier))))
            loc[ident] = idea.title
            loc[ident + "_desc"] = idea.desc
    return NOTE + block("ideas", block("country", "\n".join(rows)))


def compile_characters(states, loc):
    bodies = []
    for state in states:
        for gov in state.governments:
            ident, body = seams.office_character(state.tag, gov.slug, gov.sub, portrait_sprite(office(state, gov)))
            bodies.append(body)
            loc[ident] = gov.title
            loc[ident + "_desc"] = gov.desc
    return NOTE + "characters = {\n" + "".join(bodies) + "}\n"


def compile_effects(states):
    rows = []
    for state in states:
        for gov in state.governments:
            name, effect = seams.regime_effect(C.PACKAGE, state.tag.lower() + "_" + gov.slug, gov.party, office(state, gov), gov.sub,
                                               gov.elections, gov.popularities)
            if name != C.regime_name(state.tag, gov.slug):
                raise ValueError("Regime effect name drift: " + name)
            rows.append(effect)
    return NOTE + "\n".join(rows)


def compile_events(states, loc):
    rows = ["add_namespace = " + C.NAMESPACE]
    for state in states:
        numbers = event_numbers(state)
        for event in state.events:
            key = "%s.%d" % (C.NAMESPACE, numbers[event.slug])
            body = ("id = %s\ntitle = %s.t\ndesc = %s.d\npicture = %s\nis_triggered_only = yes\n"
                    % (key, key, key, event_picture(state.tag, event.picture)))
            body += block("trigger", "original_tag = %s" % state.tag)
            weights = [60, 40, 20]
            for index, (text, effects) in enumerate(event.options):
                letter = "abc"[index]
                option = "name = %s.%s\nai_chance = { factor = %d }\n%s" % (key, letter, weights[index] if len(event.options) > 1 else 1, effects.strip("\n"))
                body += block("option", option)
                loc["%s.%s" % (key, letter)] = text
            rows.append(block("country_event", body))
            loc[key + ".t"] = event.title
            loc[key + ".d"] = event_body(event)
    return NOTE + "\n".join(rows)


def compile_decisions(states, loc):
    rows = []
    for state in states:
        tag = state.tag
        ident = "ac_ud_minors_a_adopt_%s_decision" % tag.lower()
        tree = C.tree_id(tag)
        body = ("icon = ac_pol_institutions\nallowed = { original_tag = %s }\n" % tag
                + block("visible", "original_tag = %s ac_pol_active = yes NOT = { has_focus_tree = %s }" % (tag, tree))
                + block("available", "ac_pol_previous_tree_idle = yes")
                + "cost = 0\nfire_only_once = no\ndays_re_enable = 7\nai_will_do = { base = 1 }\n"
                + block("complete_effect", "load_focus_tree = { tree = %s keep_completed = yes }\nset_country_flag = %s" % (tree, C.fid(tag, "programme_adopted"))))
        rows.append(block(ident, body))
        loc[ident] = "Adopt the %s" % state.tree_title
        loc[ident + "_desc"] = ("Replace the shared regional or generic programme with %s's own national programme once no focus is in progress. "
                                "Completed focuses are kept. Nothing is granted for switching, and no historical reward is replayed. "
                                "This is provisional gameplay for saves begun before the programme existed." % state.name)
        loc[C.fid(tag, "programme_adopted")] = "%s adopted its national programme from an older save" % state.name
    return NOTE + block("ac_pol_institutions", "\n".join(rows))


def localisation(loc):
    if len({key.lower() for key in loc}) != len(loc):
        raise ValueError("Localisation keys differ only by case")
    lines = ["l_english:"]
    for key in sorted(loc):
        value = loc[key].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        lines.append(' %s:0 "%s"' % (key, value))
    return ("\n".join(lines) + "\n").encode("utf-8-sig")


class Loc(dict):
    """Localisation table that refuses to overwrite a key."""

    def __setitem__(self, key, value):
        if key in self:
            raise ValueError("Duplicate localisation key " + key)
        super().__setitem__(key, value)


def outputs(states=None):
    states = states or C.load_states()
    loc = Loc()
    out = {}
    for state in states:
        out[focus_file(state.tag)] = compile_state(state, loc)
        for slug, label in state.flags.items():
            loc[C.fid(state.tag, slug)] = label
        for slug, text in state.tooltips.items():
            loc[C.fid(state.tag, slug) + "_tt"] = text
        for party, name in state.country_names.items():
            loc["%s_%s" % (state.tag, party)] = name
            loc["%s_%s_DEF" % (state.tag, party)] = name
    out[FILES["ideas"]] = compile_ideas(states, loc)
    out[FILES["characters"]] = compile_characters(states, loc)
    out[FILES["effects"]] = compile_effects(states)
    out[FILES["events"]] = compile_events(states, loc)
    out[FILES["decisions"]] = compile_decisions(states, loc)
    data = {path: text.encode("utf-8") for path, text in out.items()}
    data[OWN_LOC] = localisation(loc)
    return data


ANCHORS = [
    ("ulysses", "FCU announces that Ulysses will strike the Earth", "ACES Chronicle, 1996 / 04.20"),
    ("coup", "A coup breaks out across Usea", "ACES Chronicle, 1997 / 05.30"),
    ("stonehenge", "Stonehenge is completed", "ACES Chronicle, 1998 / 06.19"),
    ("impact", "Ulysses passes the Roche limit and breaks up", "ACES Chronicle, 1999 / 07.08"),
    ("refugee", "Erusea stops taking in refugees", "ACES Chronicle, 2000 / 04.21"),
    ("war", "Erusea invades San Salvacion and seizes Stonehenge (read through ac_ucw_war_started)", "ACES Chronicle, 2003 / SUMMER"),
    ("isaf", "ISAF is founded (read through ac_ucw_isaf_formed)", "ACES Chronicle, 2003 / 08.22"),
    ("postwar", "Erusea surrenders (read through the ac_ucw outcome flags)", "ACES Chronicle, 2005 / 09.19"),
]


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


def ledger(states):
    lines = [
        "# Usea Depth: minor states A (Chopinburg, Platania, Ferustia, Albard, Dorondo, Scandia, Bulgurdarest)",
        "",
        "Generated by `python -B tools/usea_depth/minors_a/build.py`; do not edit by hand. Native status: not tested in HOI4. Native acceptance remains under #8.",
        "",
        "No official source covers any of these seven states. Their geography, names, resources and starting spirits are **mod provenance** "
        "(`history/countries`, `history/states`, `common/ideas/ferustia.txt`); everything authored for them here is **provisional gameplay**. "
        "Official Chronicle anchors are used only as dates, and every national response to them is provisional. "
        "No new named people: each provisional government is an unnamed office with a generated card. No place is mapped to a state. "
        "No `transfer_state`, cores, claims, borders, wars, annexation or faction changes exist in this package, and nothing writes an `ac_ucw_*` flag.",
        "",
        "## Package rows",
        "",
        "| Claim or identifier | Source layer | Exact citation | Affected IDs and files | Status |",
        "| --- | --- | --- | --- | --- |",
        "| Seven national trees `ac_ud_<tag>_tree`, weighted +45 for their own tag over the regional tree's +5 | provisional gameplay | `docs/usea_depth/README.md` (package contract) | `common/national_focus/ac_ud_minor_<tag>.txt` | implemented; static-validated |",
        "| Old saves switch through an idle-gated adoption decision | provisional gameplay | `ac_pol_previous_tree_idle` in `common/scripted_triggers/ac_politics.txt` | `ac_ud_minors_a_adopt_<tag>_decision` in `common/decisions/ac_ud_minors_a.txt` | implemented; static-validated |",
        "| Institutional gains use the public capacity effect | provisional gameplay | `ac_pol_change_capacity` in `common/scripted_effects/ac_politics.txt` | every `R.cap` reward | implemented; static-validated |",
        "| The treaty council is the mod's Central Usean Treaty Council (CNEA membership) | mod provenance | `CNEA_member_idea` in `common/ideas/_ac_generic.txt`; `CNEA_parliament_decisions_category` localisation | treaty-council lanes in all seven trees (Ferustia is not a member) | referenced only; membership is never changed |",
        "| Provisional governments change only through `ac_ud_minors_a_regime_*` effects with AI weight 0 | provisional gameplay | `seams.regime_effect()` and `seams.office_character()` | `common/scripted_effects/ac_ud_minors_a.txt`, `common/characters/ac_ud_minors_a.txt` | implemented; static-validated; the AI keeps its 1991 governments |",
    ]
    for era, claim, citation in ANCHORS:
        users = ", ".join("%s (%d)" % (s.tag, sum(1 for f in s.focuses if f.era == era)) for s in states if any(f.era == era for f in s.focuses))
        lines.append("| %s | official date; national response provisional gameplay | %s | era `%s` focuses: %s | implemented as a date or read-only flag gate |"
                     % (cell(claim), citation, era, users or "none"))
    for state in states:
        lines.append("| %s geography, resources and neighbours | mod provenance | `history/countries/%s`, `history/states` %s | `%s` | adapted as provisional gameplay |"
                     % (state.name, cell(next(p.name for p in (MOD / "history/countries").glob(state.tag + " - *.txt"))),
                        ", ".join(str(s) for s in state.owned_states), C.tree_id(state.tag)))
        for claim, layer, citation, ids, status in state.ledger:
            lines.append("| %s | %s | %s | %s | %s |" % (cell(claim), layer, cell(citation), cell(ids), cell(status)))
        for gov in state.governments:
            lines.append("| %s: %s (%s / %s, elections %s) | provisional gameplay | no source; unnamed office | `%s`, `%s` | implemented; player-only path (AI weight 0) |"
                         % (state.name, cell(gov.title), gov.party, gov.sub, "allowed" if gov.elections else "suspended",
                            C.regime_name(state.tag, gov.slug), C.office_id(state.tag, gov.slug)))
        for party, name in state.country_names.items():
            lines.append("| `%s_%s` country name \"%s\" (plain name; no state form invented) | provisional gameplay | no source | `localisation/english/ac_ud_minors_a_l_english.yml` | implemented |"
                         % (state.tag, party, cell(name)))
    lines += ["", "## Events", "", "| Event | Title | Source layer | Citation | Fired by |", "| --- | --- | --- | --- | --- |"]
    for state in states:
        numbers = event_numbers(state)
        fired = {f.event: C.fid(state.tag, f.slug) for f in state.focuses if f.event}
        for event in state.events:
            lines.append("| `%s.%d` | %s | %s | %s | `%s` |" % (C.NAMESPACE, numbers[event.slug], cell(event.title), event.layer.lower(),
                                                          cell(event.citation), fired.get(event.slug, "")))
    lines += ["", "## Counts", "", "| State | Tree | Focuses | Events | Spirits | Governments |", "| --- | --- | --- | --- | --- | --- |"]
    for state in states:
        lines.append("| %s | `%s` | %d | %d | %d | %s |" % (state.name, C.tree_id(state.tag), len(state.focuses), len(state.events), len(state.ideas),
                                                       ", ".join(g.title for g in state.governments)))
    lines.append("| **Total** | | %d | %d | %d | %d |" % (sum(len(s.focuses) for s in states), sum(len(s.events) for s in states),
                                                     sum(len(s.ideas) for s in states), sum(len(s.governments) for s in states)))
    return ("\n".join(lines) + "\n").encode("utf-8")


def budget(states):
    return {
        "package": C.PACKAGE,
        "marker": None,
        "focuses": {s.tag: len(s.focuses) for s in states},
        "trees": {C.tree_id(s.tag): len(s.focuses) for s in states},
        "events": sum(len(s.events) for s in states),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--validate", nargs="?", const="ALL")
    args = parser.parse_args()
    if args.validate:
        sys.path.insert(0, str(HERE))
        import importlib
        tags = C.TAGS if args.validate == "ALL" else (args.validate.upper(),)
        states = [importlib.import_module(t.lower()).STATE for t in tags]
        problems = validate(states)
        for state in states:
            print("%s: %d focuses, %d events, %d ideas, %d governments" % (state.tag, len(state.focuses), len(state.events), len(state.ideas), len(state.governments)))
        if problems:
            raise SystemExit("Authoring problems:\n- " + "\n- ".join(problems))
        print("Authoring checks passed.")
        return
    states = C.load_states()
    problems = validate(states)
    if problems:
        raise SystemExit("Authoring problems:\n- " + "\n- ".join(problems))
    data = outputs(states)
    data["budget"] = (json.dumps(budget(states), indent=2) + "\n").encode("utf-8")
    data["ledger"] = ledger(states)
    special = {"budget": HERE / "budget.json", "ledger": ROOT / "docs/usea_depth/MINORS_A.md"}
    differs = []
    for relative, payload in data.items():
        path = special.get(relative, MOD / relative)
        if args.check:
            current = path.read_bytes().replace(b"\r\n", b"\n") if path.exists() else None
            if current != payload:
                differs.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    if differs:
        raise SystemExit("Minor states A output differs: " + ", ".join(differs))
    print("Minor states A: %d focuses in %d trees, %d events, %d outputs %s" % (
        sum(len(s.focuses) for s in states), len(states), sum(len(s.events) for s in states), len(data), "verified" if args.check else "written"))


if __name__ == "__main__":
    main()
