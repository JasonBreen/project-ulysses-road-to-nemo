"""Source, artwork and actual-script offline regressions for every content wave.

The runtime half executes the generated scripted effects with the real P1
political and fiscal owners (tools/Test-SharedSystems.py). The adapter only
supplies dates, focus completion, scope switching and engine observations.
Decimal execution and deepcopy reloads are offline evidence, not native saves.
"""
import copy
from datetime import date, timedelta
from decimal import Decimal as D
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]
spec = importlib.util.spec_from_file_location("content_waves_shared", ROOT / "tools/Test-SharedSystems.py")
shared = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = shared
spec.loader.exec_module(shared)
parse, fields = shared.parse, shared.fields

from content_waves.framework import focus_id, branch_id, service_id  # noqa: E402
from content_waves import aurelia, circum_pacific, estovakia, free_erusea, lighthouse, nordennavic  # noqa: E402
from content_waves.registry import MODULES  # noqa: E402
from event_picture_fit import audit as picture_audit  # noqa: E402

FE, NC, EB, AU, CP, LH = free_erusea.WAVE, nordennavic.WAVE, estovakia.WAVE, aurelia.WAVE, circum_pacific.WAVE, lighthouse.WAVE
NAMES = {m.WAVE.prefix: m.NAME for m in MODULES}
WAVES = tuple((m.WAVE, m.NAME) for m in MODULES)
PREFIX_BY_KEY = {m.KEY: m.WAVE.prefix for m in MODULES}
STEMS = tuple(f"{tag}_{m.WAVE.infix}" for m in MODULES for tag in (*m.WAVE.countries, *m.WAVE.extra_tags))
OWNED_RE = "|".join(sorted(NAMES) + sorted(STEMS))
OWNED_FILES = [f"{folder}/ac_{name}.txt" for name in NAMES.values() for folder in (
    "common/national_focus", "common/scripted_effects", "common/scripted_triggers", "common/ideas", "common/ai_strategy",
    "common/decisions", "common/decisions/categories", "common/on_actions", "common/custom_localization", "events",
    "common/special_projects/projects", "common/special_projects/project_tags")
    if (MOD / f"{folder}/ac_{name}.txt").exists()]
# The only wars and peaces the content waves may script, each sourced and each in exactly one owner.
DECLARATIONS = {"circum_pacific": ["declare_war_on = { target = OSE type = topple_government }"],
                "lighthouse": ["declare_war_on = { target = OSE type = topple_government }"]}
PEACES = {"lighthouse": ["white_peace = OSE"], "circum_pacific": ["white_peace = YUK", "white_peace = OSE"]}
EXPECTED = {"ERU": 90, "FCU": 48, "NEC": 42, "EVA": 30, "EMM": 18, "AUR": 54}
STORY_FLAGS = ("ac_cpw_started", "ac_cpw_tainted", "ac_cpw_prevented", "ac_cpw_declaration_withheld")


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def localization():
    keys = {}
    for path in (MOD / "localisation/english").glob("*.yml"):
        for match in re.finditer(r'^ ([^\s:#]+):\d* "(.*)"$', path.read_text(encoding="utf-8-sig"), re.M):
            keys.setdefault(match[1], []).append(path.name)
    return keys


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loc = localization()
        cls.manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        cls.assets = {row["sprite"]: row for row in json.loads((HERE / "assets.json").read_text(encoding="utf-8"))["assets"]}

    def test_generators_and_foreign_tree_import_blocks_are_consistent(self):
        for script in ("build.py", "build_art.py"):
            result = subprocess.run([sys.executable, "-B", str(HERE / script), "--check"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        sys.path.insert(0, str(ROOT / "tools/anea"))
        owners = {"ERU": load_module("cw_preserve", ROOT / "tools/build_continental_war.py"),
                  "EVA": load_module("anea_preserve", ROOT / "tools/anea/build_campaign.py")}
        owners["FCU"], owners["EMM"] = owners["ERU"], owners["EVA"]
        # A tree extended by several waves preserves every block, in registry order.
        expected = {}
        for module in MODULES:
            for tag, name in getattr(module, "IMPORTS", {}).items():
                ids = [focus_id(module.WAVE, b, i) for b in module.WAVE.branches if b.tag == tag for i in range(6)]
                expected[tag] = expected.get(tag, "") + f"# BEGIN {name} IMPORTS\n" + "".join(f"shared_focus = {i}\n" for i in ids) + f"# END {name} IMPORTS\n"
        for tag, blocks in expected.items():
            with self.subTest(tag=tag):
                self.assertEqual(blocks, owners[tag].preserved_imports(tag))

    def test_approved_budgets_and_globally_unique_ids(self):
        self.assertEqual(EXPECTED, self.manifest["counts"])
        self.assertEqual(sum(EXPECTED.values()), self.manifest["total"])
        defined = []
        for path in (MOD / "common/national_focus").glob("*.txt"):
            defined += re.findall(r"^\s*id\s*=\s*(\w+)", path.read_text(encoding="utf-8-sig"), re.M)
        for ident in {row["id"] for row in self.manifest["focuses"]}:
            self.assertEqual(1, defined.count(ident), ident)
        for tag in ("NEC", "AUR"):
            tree = parse(text(f"common/national_focus/{tag}.txt"))
            imports = [v for k, _, v in fields(tree)["focus_tree"] if k == "shared_focus"]
            self.assertEqual(sorted(r["id"] for r in self.manifest["focuses"] if r["tag"] == tag), sorted(imports))

    def test_every_focus_is_localized_iconed_and_has_a_real_consumer(self):
        for row in self.manifest["focuses"]:
            ident = row["id"]
            with self.subTest(focus=ident):
                self.assertIn(ident, self.loc)
                self.assertIn(ident + "_desc", self.loc)
                sprite = self.assets["GFX_" + PREFIX_BY_KEY[row["wave"]] + "_focus_" + ident]
                self.assertEqual((96, 96), (sprite["width"], sprite["height"]))
        for wave, name in WAVES:
            effects = text(f"common/scripted_effects/ac_{name}.txt")
            for b in wave.branches:
                for i in (1, 2):
                    self.assertIn(f"add_ideas = {focus_id(wave, b, i)}_spirit", effects)
                stem = focus_id(wave, b, 0)[:-len("_register")]
                self.assertIn(f"has_country_flag = {stem}_service_completed", text(f"common/national_focus/ac_{name}.txt"))

    def test_exclusive_policies_are_symmetric(self):
        for wave, name in WAVES:
            if not wave.branches:
                self.assertFalse((MOD / f"common/national_focus/ac_{name}.txt").exists(), name)
                continue
            focuses = {fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"}
            for b in wave.branches:
                a, c = focus_id(wave, b, 1), focus_id(wave, b, 2)
                self.assertEqual(c, fields(fields(focuses[a])["mutually_exclusive"])["focus"])
                self.assertEqual(a, fields(fields(focuses[c])["mutually_exclusive"])["focus"])

    def test_localization_keys_resolve_once_and_files_have_bom(self):
        ours = tuple(f"ac_{name}" for name in NAMES.values())
        for name in NAMES.values():
            raw = (MOD / f"localisation/english/ac_{name}_l_english.yml").read_bytes()
            self.assertTrue(raw.startswith(b"\xef\xbb\xbfl_english:\n"))
        duplicates = {k: v for k, v in self.loc.items() if len(v) > 1 and any(n.startswith(ours) for n in v)}
        self.assertEqual({}, duplicates)
        for relative in OWNED_FILES:
            if "custom_localization" in relative:
                continue
            for key in re.findall(r"\b(?:title|desc|name)\s*=\s*([\w.]+)", text(relative)):
                if key.startswith(tuple(NAMES)):
                    self.assertTrue(key in self.loc, relative + ": " + key)

    def test_every_called_owned_effect_and_trigger_is_defined(self):
        defined = set()
        for folder in ("scripted_effects", "scripted_triggers"):
            for path in (MOD / "common" / folder).glob("*.txt"):
                defined |= set(re.findall(r"^(\w+)\s*=\s*\{", path.read_text(encoding="utf-8-sig"), re.M))
        pattern = re.compile(r"\b((?:" + OWNED_RE + r")_\w+|ac_econ_\w+|ac_macro_\w+|ac_pol_\w+) = yes")
        for relative in OWNED_FILES:
            for call in pattern.findall(text(relative)):
                self.assertTrue(call in defined, relative + ": " + call)

    def test_artwork_bindings_exist_and_event_pictures_fit_native_apertures(self):
        gfx = (MOD / "interface/ac_content_waves.gfx").read_text(encoding="utf-8")
        sprites = dict(re.findall(r'name = "(\w+)" texturefile = "([^"]+)"', gfx))
        prefixes = "|".join(sorted(NAMES))
        for relative in OWNED_FILES:
            source = text(relative)
            for sprite in re.findall(r"\b(GFX_(?:" + prefixes + r")_\w+)", source):
                self.assertIn(sprite, sprites, sprite)
            for ident in re.findall(r"^\t\t(\w+) = \{\n\t\t\tpicture = (\w+)", source, re.M):
                self.assertIn("GFX_idea_" + ident[1], sprites)
            for icon in re.findall(r"\bicon = ((?:" + prefixes + r")_\w+)", source):
                self.assertIn("GFX_decision_" + icon, sprites)
        for sprite, relative in sprites.items():
            if sprite.endswith("_shine"):
                continue
            with Image.open(MOD / relative) as image:
                row = self.assets[sprite]
                self.assertEqual((row["width"], row["height"]), image.size)
                if row["role"] == "decision row":
                    self.assertEqual((26, 29), image.size)
        report = picture_audit.audit([f"events/ac_{name}.txt" for name in NAMES.values()])
        # A: 24 narrative + owner .2/.4/.5; D: 16 narrative; B: 20 narrative + Emmerian aid events .5/.6;
        # Aurelia: 20 narrative; C: the Yuktobanian declaration .5, the Osean Arkbird decision .6 and the peace offer .16;
        # F1: 30 narrative + the Erusean declaration .5 and ceasefire .6.
        # News: A .1/.3/.6; B .1-.4, .7-.14; C .1-.4, .7-.15, the peace .17 and the sixteen stages .20-.35;
        # F1 .1-.4, .7-.13, the nine stages .20-.28 and .29; the Belkan War record's thirteen briefs .1-.13.
        self.assertEqual({"country_event": 27 + 16 + 22 + 20 + 3 + 32, "news_event": 3 + 12 + 30 + 21 + 13}, report["counts"])
        for row in report["consumers"]:
            self.assertLessEqual(row["bounds"][2], 215 if row["event_type"] == "country_event" else 456)
            self.assertLessEqual(row["bounds"][3], 181 if row["event_type"] == "country_event" else 244)

    def test_no_forbidden_world_changes_and_honest_chronology(self):
        combined = "\n".join(text(r) for r in OWNED_FILES)
        for forbidden in ("transfer_state", "add_state_core", "remove_state_core", "start_civil_war", "create_country", "annex_country",
                          "set_cosmetic_tag", "add_to_faction", "create_faction", "create_wargoal", "add_wargoal",
                          "add_manpower", "create_unit", "add_equipment_to_stockpile", "set_politics", "create_country_leader",
                          "recruit_character", "add_country_leader_role", "launch_nuke", "set_owner", "set_state_controller"):
            self.assertNotIn(forbidden, combined, forbidden)
        # Only a sourced conflict owner declares a war or signs a peace, each exactly as its source records it.
        for keyword, allowed in (("declare_war_on", DECLARATIONS), ("white_peace", PEACES)):
            for relative in OWNED_FILES:
                owner = next((n for n in allowed if n in relative), None)
                found = re.findall(keyword + r" = (?:\{[^}]*\}|\w+)", text(relative))
                self.assertEqual(allowed[owner] if owner and relative.startswith("common/scripted_effects/") else [], found, relative)
        effects = text("common/scripted_effects/ac_free_erusea.txt")
        self.assertIn("date > 2006.9.25", effects)
        self.assertIn("date < 2007.9.26", effects)
        self.assertIn("ac_fe_late_start_skipped", effects)
        loc = (MOD / "localisation/english/ac_free_erusea_l_english.yml").read_text(encoding="utf-8-sig")
        self.assertIn("ACES Chronicle records that Mobius 1 defeated the insurrection on 26 September 2006 (2006 / 09.26)", loc)
        self.assertIn("defeat by Mobius 1 on 26 September 2006 (2006 / 09.26)", loc)
        self.assertIn("is provisional gameplay", loc)
        self.assertNotIn("no end date is claimed", loc)
        ecw = text("common/scripted_effects/ac_estovakia.txt")
        for anchor in ("date > 2007.4.2", "date > 2007.6.29", "date > 2008.7.14", "date > 2008.10.22", "date > 2010.2.18",
                       "date > 2011.5.8", "date > 2013.1.14", "date > 2013.10.28", "date < 2008.4.3"):
            self.assertIn(anchor, ecw)
        ecw_loc = (MOD / "localisation/english/ac_estovakia_l_english.yml").read_text(encoding="utf-8-sig")
        for citation in ("2007 / 04.03", "2007 / 06.30", "2008 / 07.15", "2008 / 10.23", "2010 / 02.19", "2011 / 05.09",
                         "2013 / 01.15", "2013 / 10.29", "2013 / 11.25", "2014 / 02.03", "2014 / 02.04"):
            self.assertIn(citation, ecw_loc)
        self.assertNotRegex(ecw, r"\b(?:set|clr)_(?:global|country)_flag = ac_anea_")
        aurelian = "\n".join(text(r) for r in OWNED_FILES if "ac_aurelia" in r) + (MOD / "localisation/english/ac_aurelia_l_english.yml").read_text(encoding="utf-8-sig")
        for name in ("Navarro", "Gleipnir", "Gandr", "Aubrey", "Archelon", "Nevera", "Griswall", "Gryphus", "exploitation"):
            self.assertNotIn(name, aurelian, name)

    def test_circum_pacific_owner_honours_the_published_consumer_contract(self):
        effects = text("common/scripted_effects/ac_circum_pacific.txt")
        triggers = text("common/scripted_triggers/ac_circum_pacific.txt")
        loc = (MOD / "localisation/english/ac_circum_pacific_l_english.yml").read_text(encoding="utf-8-sig")
        # The four flags the Pacific squadron stories already read are the only route observations.
        for flag in STORY_FLAGS:
            self.assertIn("set_global_flag = " + flag, effects, flag)
        for relative in ("tools/squadrons/chapters/OSE.json", "tools/squadrons/chapters/YUK.json"):
            story = (ROOT / relative).read_text(encoding="utf-8")
            for flag in set(re.findall(r"has_global_flag = (ac_cpw_\w+)", story)):
                self.assertIn(flag, STORY_FLAGS, relative + ": " + flag)
        # Its own calendar: the opening, the anchor, the late-save limit and every sourced stage.
        for anchor in ("date > 2010.8.31", "date > 2010.9.26", "date < 2010.9.27", "date < 2010.10.25", "date > 2008.8.20", "date > 2010.9.22", "date > 2010.9.23",
                       "date > 2010.9.29", "date > 2010.10.3", "date > 2010.10.21", "date > 2010.10.24", "date > 2010.10.31", "date > 2010.11.1",
                       "date > 2010.11.3", "date > 2010.11.13", "date > 2010.11.28", "date > 2010.12.5", "date > 2010.12.8", "date > 2010.12.18",
                       "date > 2010.12.22", "date > 2010.12.28", "date > 2010.12.29", "date > 2010.12.30", "ac_cpw_late_start_skipped"):
            self.assertIn(anchor, effects, anchor)
        for citation in ("2008 / 08.21", "2010 / 09.23", "2010 / 09.24", "2010 / 09.27", "2010 / 09.30", "2010 / 10.04", "2010 / 10.22", "2010 / 10.25",
                         "2010 / 11.01", "2010 / 11.02", "2010 / 11.04", "2010 / 11.14", "2010 / 11.29", "2010 / 12.06", "2010 / 12.09", "2010 / 12.19",
                         "2010 / 12.23", "2010 / 12.29", "2010 / 12.30", "2010 / 12.31", "Super Weapons, Scinfaxi & Hrimfaxi", "provisional gameplay"):
            self.assertIn(citation, loc, citation)
        # The only peace is decision 6's earned route, inside its own effect; no assumed end date, no faction
        # veto, pre-existing wars inspected, third parties observed.
        self.assertEqual(2, effects.count("white_peace"))
        make_peace = re.search(r"(?ms)^ac_cpw_make_peace = \{.*?^\}", effects)[0]
        self.assertEqual(["white_peace = YUK", "white_peace = OSE"], re.findall(r"white_peace = \w+", make_peace))
        self.assertNotIn("date > 2010.12.31", effects)
        self.assertNotIn("is_in_faction", effects + triggers)
        self.assertNotIn("has_guaranteed", effects + triggers)
        self.assertIn("ac_cpw_third_party_present", triggers)
        self.assertIn("NOT = { is_subject_of = OSE } NOT = { is_subject_of = YUK }", triggers)
        self.assertIn("OR = { has_war = yes OSE = { has_war = yes } }", effects)
        self.assertIn("ac_cpw_declaration_refused", effects)
        self.assertIn("AND = { tag = OSE original_tag = OSE } AND = { tag = YUK original_tag = YUK }", effects)
        # Foreign owners are read, never written: the only project state touched is the sourced loss of the Arkbird.
        self.assertNotRegex(effects, r"\b(?:set|clr)_(?:global|country)_flag = ac_(?:snc|snp|sp|anea|ucw|yuk)_")
        self.assertNotRegex(effects, r"\b(?:set|add_to|subtract_from)_variable = \{ ac_(?:snc|snp|sp)_")
        self.assertEqual({"ac_sp_arkbird_joint_operations", "ac_sp_arkbird_debris_clearing"}, set(re.findall(r"remove_ideas = (ac_sp_\w+)", effects)))
        self.assertNotRegex(effects, r"add_ideas = ac_sp_")
        self.assertNotIn("ac_sp_arkbird_complete_effect", effects)
        # Named canon appears only in event text; nothing becomes a character, unit or leader.
        self.assertNotRegex("\n".join(text(r) for r in OWNED_FILES if "circum_pacific" in r), r"Harling|Nikanor|Razgriz|Wardog|Snow|Genette|Beagle")
        for name in ("Snow", "Genette", "Beagle", "Talisman"):
            self.assertNotIn(name, loc, name)

    def test_lighthouse_owner_honours_the_published_contract(self):
        effects = text("common/scripted_effects/ac_lighthouse.txt")
        triggers = text("common/scripted_triggers/ac_lighthouse.txt")
        loc = (MOD / "localisation/english/ac_lighthouse_l_english.yml").read_text(encoding="utf-8-sig")
        projects = text("common/special_projects/projects/ac_lighthouse.txt")
        # Its own calendar: the opening, the anchor, the late-save limit, the Expo City date and every sourced stage.
        for anchor in ("date > 2019.1.31", "date > 2019.5.14", "date < 2019.5.15", "date > 2019.11.30", "date > 2019.5.16", "date > 2019.5.29",
                       "date > 2019.6.5", "date > 2019.8.18", "date > 2019.9.18", "date > 2019.9.30", "date > 2019.10.9", "date > 2019.10.30",
                       "ac_lhw_late_start_skipped", "ac_lhw_route_unreachable", "ac_lhw_declaration_refused", "ac_lhw_ceasefire_not_made"):
            self.assertIn(anchor, effects, anchor)
        for citation in ("2019 / 05.15", "2019 / 05.17", "2019 / 05.30", "2019 / 06.06", "2019 / 08.10", "2019 / 08.19", "2019 / 09.19",
                         "2019 / 10.01", "2019 / 10.10", "2019 / 10.31", "2019 / 12.01", "Super Weapons, Arsenal Birds", "Super Weapons, Alicorn",
                         "Abstracts, ACE COMBAT 7", "provisional gameplay"):
            self.assertIn(citation, loc, citation)
        # No assumed end date, no faction veto, pre-existing wars inspected, third parties observed, subjects exempt.
        self.assertNotIn("date > 2019.12.1", effects)
        self.assertNotIn("is_in_faction", effects + triggers)
        self.assertNotIn("has_guaranteed", effects + triggers)
        self.assertIn("NOT = { is_subject_of = ERU } NOT = { is_subject_of = OSE }", triggers)
        self.assertIn("OR = { has_war = yes OSE = { has_war = yes } }", effects)
        self.assertIn("AND = { tag = ERU original_tag = ERU } AND = { tag = OSE original_tag = OSE }", effects)
        # The only peace the content waves script, and the only place it lives.
        self.assertEqual(1, effects.count("white_peace = OSE"))
        self.assertIn("white_peace = OSE", fields(parse(effects))["ac_lhw_sign_ceasefire"] and effects)
        # Foreign owners are read, never written: the only writes outside ac_lhw are the two projects' completion flags.
        self.assertEqual({"ac_sp_arsenal_birds_complete", "ac_sp_alicorn_complete"},
                         set(re.findall(r"\bset_global_flag = (ac_(?:ucw|sp|release|fe|snc|anea|cpw|ecw)_\w+)", effects)))
        self.assertNotRegex(effects, r"\b(?:set|clr)_country_flag = ac_(?:ucw|sp|release|fe|snc)_")
        self.assertNotRegex(effects, r"\b(?:set|add_to|subtract_from)_variable = \{ ac_(?:ucw|sp|release|fe|snc)_")
        self.assertEqual({"ac_sp_arsenal_birds_elevator_screen"}, set(re.findall(r"remove_ideas = (ac_sp_\w+)", effects)))
        self.assertEqual({"ac_sp_arsenal_birds_elevator_screen", "ac_sp_alicorn_cruiser"}, set(re.findall(r"add_ideas = (ac_sp_\w+)", effects)))
        self.assertNotIn("SHI = {", effects)
        self.assertNotIn("transfer_state", effects + projects)
        # The projects live in generator-owned files; the hash-pinned Track C files are untouched.
        pinned = json.loads((ROOT / "tools/air_program/preserved_sources.json").read_text(encoding="utf-8"))["sources"]
        import hashlib
        for relative, digest in pinned.items():
            if "special_projects" in relative or relative.endswith("ac_special_projects.txt"):
                self.assertEqual(digest, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), relative)
        for ident in ("ac_sp_arsenal_birds", "ac_sp_alicorn"):
            self.assertIn(f"{ident}_complete_effect = yes", projects)
            self.assertIn(f"NOT = {{ has_global_flag = {ident}_complete }}", projects)
        self.assertIn("NOT = { has_global_flag = ac_lhw_arsenal_birds_lost }", projects)
        # Named canon appears only in event and idea text; nothing becomes a character, unit, leader, state or tag.
        scripts = "\n".join(text(r) for r in OWNED_FILES if "lighthouse" in r)
        self.assertNotRegex(scripts, r"Harling|Labarthe|Torres|Trigger|Mihaly|Expo City|Chopinburg|Farbanti|Shilage")
        for name in ("Torres", "Trigger", "Mihaly", "Strider", "Cyclops", "Rosa", "Cossette"):
            self.assertNotIn(name, loc, name)



class World(shared.World):
    # Owned variables, the existing Anea recovery variable that Wave B reads and the
    # Pacific national-continuation records that the Circum-Pacific War owner reads.
    PREFIXES = tuple(p + "_" for p in NAMES) + tuple(s + "_" for s in STEMS) + ("ac_anea_", "ac_snc_", "ac_snp_")

    def __init__(self, mode="full"):
        super().__init__(mode)
        self.wave_actions = {}
        self.focuses = {}
        self.messages = {}
        self.wars = set()
        self.factions = {}     # tag -> faction leader, for is_in_faction_with
        for name in NAMES.values():
            for folder, library in (("scripted_effects", self.effects), ("scripted_triggers", self.triggers)):
                if not (MOD / f"common/{folder}/ac_{name}.txt").exists():
                    continue    # an owner without triggers (the Belkan War record) writes no file
                for key, _, value in parse(text(f"common/{folder}/ac_{name}.txt")):
                    if key in library:
                        raise ValueError("Conflicting owner " + key)
                    library[key] = value
            self.wave_actions[name] = fields(parse(text(f"common/on_actions/ac_{name}.txt")))["on_actions"]
            if (MOD / f"common/national_focus/ac_{name}.txt").exists():
                self.focuses.update({fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"})
            self.messages.update({next(x for key, _, x in v if key == "id"): v for k, _, v in parse(text(f"events/ac_{name}.txt")) if k in ("country_event", "news_event")})
        # The real Osean and Yuktobanian continuation records; their programme owner is observed as active.
        for name in ("ac_snc_ose", "ac_snc_yuk"):
            for key, _, value in parse(text(f"common/scripted_triggers/{name}.txt")):
                self.triggers.setdefault(key, value)
        self.triggers.setdefault("ac_snp_active", [("always", "=", "yes")])
        # Cores come from the real state history, so is_core_of is not approximated by ownership.
        cores = {}
        for path in (MOD / "history/states").glob("*.txt"):
            source = path.read_text(encoding="utf-8-sig", errors="replace")
            ident = re.search(r"^\s*id\s*=\s*(\d+)", source, re.M)
            if ident:
                cores[int(ident[1])] = frozenset(re.findall(r"\badd_core_of\s*=\s*(\w+)", source))
        for ident, state in self.states.items():
            state.cores = cores.get(ident, frozenset())
        for c in self.countries.values():
            c.completed = set()
            c.timed_ideas = {}
            c.stability = D("0.6")
            c.trees = set()
            c.subject = False

    def number(self, value, context, temp, root, previous):
        if value.startswith(self.PREFIXES):
            return temp.get(value, context.variables.get(value, D(0)))
        return super().number(value, context, temp, root, previous)

    def trigger(self, nodes, context, temp=None, root=None, previous=None):
        results = []
        for key, op, value in nodes:
            if key == "has_completed_focus":
                answer = value in context.completed
            elif key == "country_exists":
                answer = value in self.countries and any(s.owner == value for s in self.states.values())
            elif key == "has_stability":
                answer = {"<": context.stability < D(value), ">": context.stability > D(value)}[op]
            elif key == "has_war_with":
                answer = frozenset((context.tag, value)) in self.wars
            elif key == "has_war":
                answer = (context.war or any(context.tag in pair for pair in self.wars)) == (value == "yes")
            elif key == "is_subject":
                answer = context.subject == (value == "yes")
            elif key == "is_subject_of":
                answer = getattr(context, "overlord", None) == value
            elif key in ("FROM", "PREV", "ROOT"):
                target = root if key == "ROOT" else previous
                answer = target is not None and self.trigger(value, target, temp, root, context)
            elif key == "any_country":
                answer = any(self.trigger(value, c, temp, root, context) for c in self.countries.values()
                             if any(s.owner == c.tag for s in self.states.values()))
            elif key == "controls_state":
                answer = self.states[int(value)].controller == context.tag
            elif key == "is_in_faction_with":
                answer = context.tag in self.factions and self.factions[context.tag] == self.factions.get(value)
            elif key == "any_controlled_state":
                answer = any(self.trigger(value, s, temp, root, context) for s in self.states.values() if s.controller == context.tag)
            elif key == "is_core_of":
                answer = value in context.cores
            elif key == "has_focus_tree":
                answer = value in context.trees
            elif key in self.countries:
                answer = self.trigger(value, self.countries[key], temp, root, context)
            else:
                answer = super().trigger([(key, op, value)], context, temp, root, previous)
            results.append(answer)
        return all(results)

    def execute(self, nodes, context, temp=None, root=None, previous=None):
        temp = {} if temp is None else temp
        root = context if root is None else root
        branch = None
        for key, op, value in nodes:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise ValueError("Orphan branch")
                condition = key == "else" or self.trigger(next(v for k, _, v in value if k == "limit"), context, temp, root, previous)
                if not branch and condition:
                    self.execute([r for r in value if r[0] != "limit"], context, temp, root, previous)
                    branch = True
                continue
            branch = None
            name = value[0][0] if isinstance(value, list) and value and isinstance(value[0], tuple) else None
            if key in ("set_variable", "add_to_variable", "subtract_from_variable", "set_temp_variable", "add_to_temp_variable",
                       "subtract_from_temp_variable") and name and name.startswith(self.PREFIXES):
                _, _, operand = value[0]
                amount = self.number(operand, context, temp, root, previous)
                target = temp if "temp_variable" in key else context.variables
                before = target.get(name, D(0))
                target[name] = amount if key.startswith("set_") else before + amount if key.startswith("add_") else before - amount
            elif key == "add_timed_idea":
                data = fields(value)
                context.ideas.add(data["idea"])
                context.timed_ideas[data["idea"]] = self.today + int(data["days"])
            elif key == "remove_ideas":
                context.ideas.discard(value)
                context.timed_ideas.pop(value, None)
            elif key in ("country_event", "news_event"):
                data = fields(value)
                self.events.append((context.tag, data["id"], self.today + int(data.get("days", 0))))
            elif key == "load_focus_tree":
                context.trees.add(fields(value)["tree"])
            elif key == "declare_war_on":
                # `refuse_war` models an engine that does not create the war (a truce, the same faction).
                if not getattr(self, "refuse_war", False):
                    self.wars.add(frozenset((context.tag, fields(value)["target"])))
            elif key == "white_peace":
                # `refuse_peace` models an engine that keeps the war (the other side is in a faction war with us).
                if not getattr(self, "refuse_peace", False):
                    self.wars.discard(frozenset((context.tag, value)))
            elif key in self.countries or key in ("FROM", "ROOT"):
                target = previous if key == "FROM" else root if key == "ROOT" else self.countries[key]
                self.execute(value, target, temp, root, context)
            else:
                super().execute([(key, op, value)], context, temp, root, previous)

    def advance(self, days):
        self.today += days
        for c in self.countries.values():
            for ident, expiry in list(c.timed_ideas.items()):
                if expiry <= self.today:
                    c.ideas.discard(ident)
                    c.timed_ideas.pop(ident)

    def wave_action(self, name, action, tag=None, other=None):
        node = fields(fields(self.wave_actions[name])[action])["effect"]
        self.execute(node, self.countries.get(tag), root=self.countries.get(tag), previous=self.countries.get(other))

    def complete(self, ident, tag):
        c = self.countries[tag]
        node = self.focuses[ident]
        if not self.trigger(fields(node)["available"], c):
            raise AssertionError("Unavailable focus " + ident)
        self.execute(fields(node)["completion_reward"], c)
        c.completed.add(ident)

    def available(self, ident, tag):
        return self.trigger(fields(self.focuses[ident])["available"], self.countries[tag])

    def option(self, event, letter, tag):
        """Choose an option as the engine would: the event's and the option's own triggers must hold for the acting country."""
        node = self.messages[event]
        c = self.countries[tag]
        gate = next((v for k, _, v in node if k == "trigger"), None)
        if gate is not None and not self.trigger(gate, c):
            raise AssertionError(f"{event} is not available to {tag}")
        option = next(v for k, _, v in node if k == "option" and next(x for key, _, x in v if key == "name") == f"{event}.{letter}")
        own = next((v for k, _, v in option if k == "trigger"), None)
        if own is not None and not self.trigger(own, c):
            raise AssertionError(f"{event}.{letter} is not available to {tag}")
        self.execute([r for r in option if r[0] not in ("name", "ai_chance", "trigger")], c)


def world(mode="full", today=date(2006, 10, 1)):
    w = World(mode).initialize_both()
    w.today = today.toordinal()
    for name in NAMES.values():
        if "on_startup" in fields(w.wave_actions[name]):
            w.wave_action(name, "on_startup")
    for tag in EXPECTED:
        c = w.countries[tag]
        c.variables["ac_pol_capacity"] = D(40)
        if mode == "experimental":
            c.flags["ac_econ_initialized"] = None
            c.variables.update(ac_econ_treasury=D(100), ac_econ_arrears=D(0))
    return w


class Runtime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines = {mode: world(mode) for mode in ("full", "experimental", "disabled")}

    def fresh(self, mode="full"):
        return copy.deepcopy(self.baselines[mode])

    def ready(self, wave=None, mode="full"):
        """A world in which the wave's countries are eligible and initialized."""
        w = self.fresh(mode)
        opens = re.search(r"date > (\d+)\.(\d+)\.(\d+)", wave.eligible if wave else "")
        if opens and date(*map(int, opens.groups())) >= date.fromordinal(w.today):
            w.today = (date(*map(int, opens.groups())) + timedelta(days=1)).toordinal()
            for tag in wave.countries:
                w.run(f"{wave.prefix}_initialize", tag)
        return w

    def test_every_service_pays_real_owners_once_and_completes_after_ninety_days(self):
        for wave in (FE, NC, EB, AU, LH):
            for b in wave.branches:
                for n in range(2):
                    for mode in ("full", "experimental", "disabled"):
                        with self.subTest(branch=branch_id(b), service=n, mode=mode):
                            w = self.ready(wave, mode)
                            c = w.countries[b.tag]
                            c.completed.add(focus_id(wave, b, 0 if n == 0 else 3))
                            ident = service_id(wave, b, n)
                            before = copy.deepcopy(c)
                            w.run(ident + "_start", b.tag)
                            self.assertEqual(before.pp - 35, c.pp)
                            self.assertEqual(36, c.variables["ac_pol_capacity"])
                            if mode == "full":
                                self.assertEqual(before.variables["ac_macro_cash"] - D(".002"), c.variables["ac_macro_cash"])
                            elif mode == "experimental":
                                self.assertEqual(before.variables["ac_econ_treasury"] - 2, c.variables["ac_econ_treasury"])
                            self.assertIn(ident + "_spirit", c.ideas)
                            snapshot = copy.deepcopy(c)
                            w.run(ident + "_start", b.tag)
                            self.assertEqual(snapshot, c)
                            w.advance(89)
                            w.run(ident + "_finish", b.tag)
                            self.assertNotIn(ident + "_completed", c.flags)
                            w.advance(1)
                            w.run(ident + "_finish", b.tag)
                            self.assertIn(ident + "_completed", c.flags)
                            self.assertIn(focus_id(wave, b, 0)[:-len("_register")] + "_service_completed", c.flags)
                            self.assertNotIn(ident + "_spirit", c.ideas)

    def test_shortfalls_never_authorize_a_service(self):
        b = NC.branches[0]
        for reason in ("pp", "capacity", "war", "not_unlocked"):
            w = self.fresh()
            c = w.countries["NEC"]
            c.completed.add(focus_id(NC, b, 0))
            if reason == "pp":
                c.pp = D(34)
            elif reason == "capacity":
                c.variables["ac_pol_capacity"] = D(3)
            elif reason == "war":
                c.war = True
            else:
                c.completed.clear()
            before = copy.deepcopy(c)
            w.run(service_id(NC, b, 0) + "_start", "NEC")
            self.assertEqual(before, c, reason)

    def prepare(self, wave, b):
        """A world in which the branch's register is available: its gate's flags set and its dates passed."""
        w = self.ready(wave)
        w.globals |= set(re.findall(r"(?<!NOT = \{ )has_global_flag = (\w+)", b.gate))
        for year, month, day in re.findall(r"date > (\d+)\.(\d+)\.(\d+)", b.gate):
            w.today = max(w.today, (date(int(year), int(month), int(day)) + timedelta(days=153)).toordinal())
        w.countries[b.tag].completed |= set(b.entry)
        return w

    def test_branch_policies_exclude_review_needs_service_and_settlement_improves(self):
        for wave in (FE, NC, EB, AU, LH):
            for b in wave.branches:
                for choice in (1, 2):
                    with self.subTest(branch=branch_id(b), choice=choice):
                        w = self.prepare(wave, b)
                        c = w.countries[b.tag]
                        w.complete(focus_id(wave, b, 0), b.tag)
                        w.complete(focus_id(wave, b, choice), b.tag)
                        self.assertFalse(w.available(focus_id(wave, b, 3 - choice), b.tag))
                        w.complete(focus_id(wave, b, 3), b.tag)
                        self.assertFalse(w.available(focus_id(wave, b, 4), b.tag))
                        ident = service_id(wave, b, 1)
                        w.run(ident + "_start", b.tag)
                        w.advance(90)
                        w.run(ident + "_finish", b.tag)
                        w.complete(focus_id(wave, b, 4), b.tag)
                        w.complete(focus_id(wave, b, 5), b.tag)
                        policy = focus_id(wave, b, choice) + "_spirit"
                        self.assertNotIn(policy, c.ideas)
                        self.assertIn(policy + "_settled", c.ideas)
                        snapshot = copy.deepcopy(c)
                        w.run(focus_id(wave, b, 5) + "_apply", b.tag)
                        self.assertEqual(snapshot, c)

    def test_nordennavic_stages_wait_for_dates_and_earlier_settlements(self):
        late = {k: focus_id(NC, next(b for b in NC.branches if b.key == k), 0) for k in nordennavic.STAGE_2 + nordennavic.STAGE_3}
        w = self.fresh()
        w.today = date(2005, 6, 1).toordinal()
        c = w.countries["NEC"]
        c.completed.add("NEC_nc_harbours_settlement")
        self.assertFalse(w.available(late["technical_reserve"], "NEC"))
        w.today = date(2006, 1, 1).toordinal()
        self.assertTrue(w.available(late["technical_reserve"], "NEC"))
        self.assertFalse(w.available(late["neutral_waters"], "NEC"))
        c.completed.add("NEC_nc_northern_routes_settlement")
        self.assertFalse(w.available(late["neutral_waters"], "NEC"))
        w.today = date(2014, 1, 1).toordinal()
        self.assertTrue(w.available(late["neutral_waters"], "NEC"))

    def test_aurelia_stages_wait_for_dates_and_earlier_settlements(self):
        first = {k: focus_id(AU, next(b for b in AU.branches if b.key == k), 0) for k in aurelia.STAGE_2 + aurelia.STAGE_3}
        w = self.fresh()
        w.today = date(2005, 6, 1).toordinal()
        c = w.countries["AUR"]
        self.assertFalse(w.available(first["finance"], "AUR"))
        c.completed.add("AUR_au_trade_settlement")
        self.assertFalse(w.available(first["finance"], "AUR"))
        w.today = date(2006, 1, 1).toordinal()
        self.assertTrue(w.available(first["finance"], "AUR"))
        self.assertFalse(w.available(first["leasath_war"], "AUR"))
        w.today = date(2010, 1, 1).toordinal()
        self.assertTrue(w.available(first["leasath_war"], "AUR"))
        self.assertFalse(w.available(first["relations"], "AUR"))
        c.completed.add("AUR_au_exports_settlement")
        self.assertFalse(w.available(first["relations"], "AUR"))
        w.today = date(2014, 1, 1).toordinal()
        self.assertTrue(w.available(first["relations"], "AUR"))

    def test_aurelia_adoption_and_hand_off_flags(self):
        w = self.prepare(AU, next(b for b in AU.branches if b.key == "relations"))
        c = w.countries["AUR"]
        decision = fields(fields(parse(text("common/decisions/ac_aurelia.txt")))["ac_aur_aur_services"])["AUR_au_adopt_campaign"]
        w.execute(fields(decision)["complete_effect"], c)
        self.assertIn(aurelia.TREE_ID, c.trees)
        w.complete("AUR_au_relations_register", "AUR")
        w.complete("AUR_au_relations_policy_a", "AUR")
        self.assertIn("AUR_au_relations_policy_a_done", c.flags)
        self.assertFalse(w.available("AUR_au_relations_policy_b", "AUR"))

    def ecw(self, today=date(2007, 4, 3)):
        w = self.ready(EB)
        w.today = today.toordinal()
        return w, w.countries["EVA"]

    def weekly_at(self, w, day):
        w.today = day.toordinal()
        w.wave_action("estovakia", "on_weekly_EVA", "EVA")

    def news(self, w):
        return [e for _, e, _ in w.events if e.startswith("ac_ecw.")]

    def test_civil_war_starts_on_the_anchor_and_late_saves_never_replay_it(self):
        w, c = self.ecw(date(2007, 4, 2))
        w.wave_action("estovakia", "on_weekly_EVA", "EVA")
        self.assertNotIn("ac_ecw_capital_seized", w.globals)
        self.weekly_at(w, date(2007, 4, 3))
        self.assertIn("ac_ecw_capital_seized", w.globals)
        self.assertEqual(D(75), c.variables["ac_ecw_luf_authority"])
        self.assertEqual(D(20), c.variables["ac_ecw_eastern_strength"])
        self.assertIn("ac_ecw_luf_holds_capital", c.ideas)
        self.assertEqual(["ac_ecw.1"], self.news(w))
        late, lc = self.ecw(date(2008, 5, 1))
        late.wave_action("estovakia", "on_weekly_EVA", "EVA")
        self.assertIn("ac_ecw_late_start_skipped", late.globals)
        self.assertNotIn("ac_ecw_capital_seized", late.globals)
        self.assertNotIn("ac_ecw_luf_authority", lc.variables)
        # A capitulated Estovakia that still owns land cannot start the civil war.
        fallen, fc = self.ecw()
        fc.capitulated = True
        fallen.wave_action("estovakia", "on_weekly_EVA", "EVA")
        self.assertNotIn("ac_ecw_capital_seized", fallen.globals)
        self.assertNotIn("ac_ecw_luf_authority", fc.variables)
        self.assertEqual([], self.news(fallen))

    def test_historical_chain_fires_each_anchor_once_and_ends_in_2013(self):
        w, c = self.ecw()
        w.globals.add("ac_anea_bureau")
        anea_before = {g for g in w.globals if g.startswith("ac_anea_")}
        eva_anea_before = {k: v for k, v in c.flags.items() if k.startswith(("ac_anea_", "EVA_an_"))}
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        self.assertIn("ac_ecw_war_running", w.globals)
        self.assertEqual(D(70), c.variables["ac_ecw_luf_authority"])
        self.weekly_at(w, date(2008, 7, 15))
        self.assertEqual((D(65), D(35)), (c.variables["ac_ecw_luf_authority"], c.variables["ac_ecw_eastern_strength"]))
        self.weekly_at(w, date(2008, 10, 23))
        self.assertIn("ac_ecw_anea_initiative_on_hold", w.globals)
        self.weekly_at(w, date(2010, 2, 19))
        self.assertIn(("EMM", "ac_ecw.5"), [(t, e) for t, e, _ in w.events])
        w.option("ac_ecw.5", "a", "EMM")
        self.assertIn("ac_ecw_emm_aid_ended_luf", w.globals)
        self.assertEqual(D(60), c.variables["ac_ecw_luf_authority"])
        self.weekly_at(w, date(2011, 5, 9))
        w.option("ac_ecw.6", "a", "EMM")
        self.assertIn("ac_ecw_emm_aid_ended_all", w.globals)
        self.weekly_at(w, date(2013, 1, 15))
        self.assertEqual(D(20), c.variables["ac_ecw_luf_authority"])
        self.assertIn("ac_ecw_luf_in_retreat", c.ideas)
        self.weekly_at(w, date(2013, 10, 29))
        self.assertTrue({"ac_ecw_ended", "ac_ecw_eastern_victory", "ac_ecw_historical_end"} <= w.globals)
        self.assertFalse(any(i in c.ideas for i in ("ac_ecw_luf_holds_capital", "ac_ecw_divided_country", "ac_ecw_luf_in_retreat")))
        self.assertIn("ac_ecw_civil_war_ended", c.ideas)
        for day in (date(2013, 11, 25), date(2014, 2, 3), date(2014, 2, 4), date(2014, 3, 1)):
            self.weekly_at(w, day)
        self.assertEqual(["ac_ecw.1", "ac_ecw.2", "ac_ecw.3", "ac_ecw.4", "ac_ecw.5", "ac_ecw.6", "ac_ecw.7", "ac_ecw.9",
                          "ac_ecw.10", "ac_ecw.11", "ac_ecw.12"], self.news(w))
        self.assertEqual(anea_before, {g for g in w.globals if g.startswith("ac_anea_")})
        self.assertEqual(eva_anea_before, {k: v for k, v in c.flags.items() if k.startswith(("ac_anea_", "EVA_an_"))})

    def test_emmerian_alternatives_need_the_conditional_aid_policy_and_ai_follows_history(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_ecw.5"] if k == "option"}
        condition = fields(options["ac_ecw.5.b"])["trigger"]
        self.assertFalse(w.trigger(condition, w.countries["EMM"]))
        w.countries["EMM"].flags["EMM_ecw_aid_policy_a_done"] = None
        self.assertTrue(w.trigger(condition, w.countries["EMM"]))
        self.assertEqual("100", fields(fields(options["ac_ecw.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(options["ac_ecw.5.b"])["ai_chance"])["factor"])
        pp = w.countries["EMM"].pp
        w.option("ac_ecw.5", "b", "EMM")
        self.assertIn("ac_ecw_emm_aid_conditional", w.globals)
        self.assertEqual(pp - 25, w.countries["EMM"].pp)

    def test_negotiated_settlement_is_earned_not_free(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        decision = fields(fields(parse(text("common/decisions/ac_estovakia.txt")))["ac_ecw_eva_services"])["EVA_ecw_negotiate"]
        self.assertFalse(w.trigger(fields(decision)["available"], c))
        c.flags.update({"EVA_ecw_talks_policy_a_done": None, "EVA_ecw_capital_policy_a_done": None})
        self.assertFalse(w.trigger(fields(decision)["available"], c))
        w.globals.add("ac_ecw_emm_aid_conditional")
        self.assertTrue(w.trigger(fields(decision)["available"], c))
        pp = c.pp
        w.execute(fields(decision)["complete_effect"], c)
        self.assertTrue({"ac_ecw_ended", "ac_ecw_negotiated"} <= w.globals)
        self.assertNotIn("ac_ecw_historical_end", w.globals)
        self.assertEqual(pp - 50, c.pp)
        self.assertIn("ac_ecw_negotiated_peace", c.ideas)
        self.assertEqual("ac_ecw.14", self.news(w)[-1])
        self.weekly_at(w, date(2013, 1, 15))
        self.weekly_at(w, date(2013, 10, 29))
        self.assertNotIn("ac_ecw.9", self.news(w))

    def test_weak_eastern_faction_gives_the_provisional_prolonged_war(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        c.flags["EVA_ecw_oil_policy_b_done"] = None
        self.weekly_at(w, date(2008, 7, 15))
        self.assertEqual(D(25), c.variables["ac_ecw_eastern_strength"])
        self.weekly_at(w, date(2013, 1, 15))
        self.assertIn("ac_ecw_prolonged", w.globals)
        self.assertIn("ac_ecw.8", self.news(w))
        before = c.variables["ac_ecw_luf_authority"]
        self.weekly_at(w, date(2013, 10, 29))
        self.assertNotIn("ac_ecw_ended", w.globals)
        self.assertLess(c.variables["ac_ecw_luf_authority"], before)
        c.variables["ac_ecw_luf_authority"] = D("20.05")
        self.weekly_at(w, date(2015, 3, 1))
        self.assertTrue({"ac_ecw_ended", "ac_ecw_eastern_victory"} <= w.globals)
        self.assertNotIn("ac_ecw_historical_end", w.globals)
        self.assertEqual("ac_ecw.13", self.news(w)[-1])
        self.assertFalse({"ac_ecw.10", "ac_ecw.11", "ac_ecw.12"} & set(self.news(w)))

    def test_policies_shift_the_balance_and_annexation_closes_the_owner(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        w.complete("EVA_ecw_capital_register", "EVA")
        w.complete("EVA_ecw_capital_policy_b", "EVA")
        self.assertEqual((D(83), D(25)), (c.variables["ac_ecw_luf_authority"], c.variables["ac_ecw_eastern_strength"]))
        w.wave_action("estovakia", "on_annex", "EMM", "EVA")
        self.assertIn("ac_ecw_closed", w.globals)
        self.assertFalse(any(i.startswith("ac_ecw_luf") or i == "ac_ecw_divided_country" for i in c.ideas))

    def test_erusea_routes_follow_the_actual_continental_war_outcome(self):
        routes = {"ac_ucw_outcome_isaf_victory": {"oversight", "return"}, "ac_ucw_outcome_erusean_victory": {"victor", "return"},
                  "ac_ucw_outcome_stalemate": {"armistice", "return"}, "ac_ucw_war_averted": {"ordinary", "return"}}
        for flag, expected in routes.items():
            with self.subTest(route=flag):
                w = self.fresh()
                w.globals.add(flag)
                c = w.countries["ERU"]
                c.completed |= {b.entry[0] for b in FE.branches if b.tag == "ERU"}
                open_ = {b.key for b in FE.branches if b.tag == "ERU" and w.available(focus_id(FE, b, 0), "ERU")}
                self.assertEqual(expected, open_)
                f = w.countries["FCU"]
                f.completed.add("FCU_ucw_exp_settlement_assessment")
                open_fcu = {b.key for b in FE.branches if b.tag == "FCU" and w.available(focus_id(FE, b, 0), "FCU")}
                self.assertEqual({"oversight", "partners"} if "isaf" in flag else {"drawdown", "partners"}, open_fcu)

    def test_openings_describe_the_actual_route_not_an_assumed_victory(self):
        custom = parse(text("common/custom_localization/ac_free_erusea.txt"))
        loc = dict(re.findall(r'^ ([^\s:#]+):0 "(.*)"$', (MOD / "localisation/english/ac_free_erusea_l_english.yml").read_text(encoding="utf-8-sig"), re.M))
        for tag in ("ERU", "FCU"):
            node = next(v for k, _, v in custom if k == "defined_text" and next(x for key, _, x in v if key == "name") == f"{tag}_fe_route_context")
            for flag in ("ac_ucw_outcome_isaf_victory", "ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_stalemate", "ac_ucw_war_averted", None):
                with self.subTest(tag=tag, route=flag):
                    w = self.fresh()
                    if flag:
                        w.globals.add(flag)
                    chosen = next(fields(v)["localization_key"] for k, _, v in node
                                  if k == "text" and w.trigger(fields(v).get("trigger", []), w.countries[tag]))
                    value = loc[chosen]
                    self.assertEqual(flag == "ac_ucw_outcome_isaf_victory", "oversight" in value, value)
            opening = loc[f"ac_fe.{10 + list(FE.countries).index(tag)}.d"]
            self.assertIn(f"[{tag}_fe_route_context]", opening)
            self.assertNotIn("surrender", opening)

    # Wave C: the Circum-Pacific War owner ------------------------------------------
    def cpw(self, today=date(2010, 9, 22)):
        w = self.fresh()
        w.today = today.toordinal()
        return w, w.countries["YUK"], w.countries["OSE"]

    def tick(self, w, day, tag="YUK", module="circum_pacific"):
        days = day.toordinal() - w.today
        if days > 0:
            w.advance(days)      # timed ideas and flags expire as the calendar moves
        else:
            w.today = day.toordinal()
        w.wave_action(module, f"on_weekly_{tag}", tag)

    def defined_text(self, w, module, name, tag):
        """Resolve a defined text as the engine would: the first entry whose trigger holds for the viewing country."""
        custom = parse(text(f"common/custom_localization/ac_{module}.txt"))
        entries = next(v for k, _, v in custom if k == "defined_text" and next(x for key, _, x in v if key == "name") == name)
        for k, _, v in entries:
            if k != "text":
                continue
            condition = next((x for key, _, x in v if key == "trigger"), None)
            if condition is None or w.trigger(condition, w.countries[tag]):
                return self.loc_of(module)[next(x for key, _, x in v if key == "localization_key")]
        raise AssertionError("no text for " + name)

    def status(self, w, module="circum_pacific", tag="YUK"):
        prefix = next(p for p, n in NAMES.items() if n == module)
        return self.defined_text(w, module, f"{prefix}_status_text", tag)

    def loc_of(self, module):
        cache = self.__dict__.setdefault("_loc_cache", {})
        if module not in cache:
            cache[module] = dict(re.findall(r'^ ([^\s:#]+):\d* "(.*)"$', (MOD / f"localisation/english/ac_{module}_l_english.yml").read_text(encoding="utf-8-sig"), re.M))
        return cache[module]

    @property
    def cpw_loc(self):
        return self.loc_of("circum_pacific")

    def records(self, w):
        """The foreign Pacific records the owner may read but never write."""
        return {t: ({k: v for k, v in w.countries[t].flags.items() if k.startswith(("ac_snc_", "ac_snp_", "ac_sp_"))},
                    {k: v for k, v in w.countries[t].variables.items() if k.startswith(("ac_snc_", "ac_snp_", "ac_sp_"))})
                for t in ("OSE", "YUK")}

    def cpw_news(self, w):
        return [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.5", "ac_cpw.6")]

    def earn(self, w, tag, record):
        """Satisfy the real ac_snc_* trigger for one record, as the national package defines it."""
        c = w.countries[tag]
        c.flags[f"ac_snc_{tag.lower()}_initialized"] = None
        c.variables[f"ac_snc_{tag.lower()}_identity"] = D(c.identity)
        if (tag, record) == ("YUK", "verification"):
            c.flags.update({"YUK_snc_field_answers_settlement_done": None, "YUK_snc_field_answers_civil_done": None, "ac_snc_yuk_message_10_public": None})
            c.ideas.add("yuk_reformed_field_command")
            c.completed.add("YUK_army_reform_complete")
            c.variables["ac_snp_yuk_civil"] = D(60)
        elif (tag, record) == ("YUK", "channel"):
            c.flags["YUK_snc_scientific_custody_settlement_done"] = None
        elif (tag, record) == ("OSE", "verification"):
            c.flags.update({"OSE_snc_contact_verification_settlement_done": None, "OSE_snc_contact_verification_civil_done": None, "ac_snc_ose_message_11_public": None})
        else:
            c.flags["OSE_snc_pacific_channel_settlement_done"] = None

    def anchor(self, w):
        """Open the calendar before the anchor, then observe the anchor day itself."""
        self.tick(w, date(2010, 9, 22))
        self.tick(w, date(2010, 9, 27))

    def declare(self, w):
        self.anchor(w)
        w.option("ac_cpw.5", "a", "YUK")
        self.assertIn("ac_cpw_started", w.globals)
        return w

    def test_arkbird_summit_needs_the_completed_project_and_fires_once(self):
        w, y, o = self.cpw(date(2008, 8, 21))
        self.tick(w, date(2008, 8, 21))
        self.assertEqual([], self.cpw_news(w))
        self.assertFalse({"ac_cpw_summit_held", "ac_cpw_summit_skipped"} & w.globals)
        w.globals.add("ac_sp_arkbird_complete")
        self.tick(w, date(2008, 8, 28))
        self.tick(w, date(2008, 9, 4))
        self.assertEqual(["ac_cpw.14"], self.cpw_news(w))
        self.assertIn("ac_cpw_summit_held", w.globals)
        late, _, _ = self.cpw(date(2009, 9, 1))
        late.globals.add("ac_sp_arkbird_complete")
        self.tick(late, date(2009, 9, 1))
        self.assertIn("ac_cpw_summit_skipped", late.globals)
        self.assertEqual([], self.cpw_news(late))

    def test_prelude_and_declaration_follow_the_anchor_and_late_saves_never_replay(self):
        w, y, o = self.cpw()
        self.tick(w, date(2010, 9, 22))
        self.assertIn("ac_cpw_calendar_started", w.globals)
        self.assertEqual([], self.cpw_news(w))
        self.tick(w, date(2010, 9, 23))
        self.tick(w, date(2010, 9, 24))
        self.tick(w, date(2010, 9, 26))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2"], self.cpw_news(w))
        self.assertNotIn("ac_cpw_started", w.globals)
        self.tick(w, date(2010, 9, 27))
        self.assertIn(("YUK", "ac_cpw.5", w.today + 1), w.events)
        self.assertTrue({"ac_cpw_declaration_asked", "ac_cpw_declaration_pending", "ac_cpw_declaration_window"} <= set(y.flags))
        self.assertEqual(set(), w.wars)
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_cpw.5"] if k == "option"}
        self.assertEqual("100", fields(fields(options["ac_cpw.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(options["ac_cpw.5.b"])["ai_chance"])["factor"])
        self.assertEqual("ac_cpw_mandate_earned = yes", " ".join(f"{k} = {v}" for k, _, v in fields(options["ac_cpw.5.b"])["trigger"]))
        w.option("ac_cpw.5", "a", "YUK")
        self.assertEqual({frozenset(("YUK", "OSE"))}, w.wars)
        self.assertIn("ac_cpw_started", w.globals)
        self.assertFalse({"ac_cpw_tainted", "ac_cpw_pre_existing_war"} & w.globals)
        self.assertTrue({"ac_cpw_yuk_war_footing", "ac_cpw_yuk_submarine_carriers"} <= y.ideas)
        self.assertIn("ac_cpw_ose_war_footing", o.ideas)
        self.assertNotIn("ac_cpw_declaration_pending", y.flags)
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3"], self.cpw_news(w))
        # The tick never asks twice and never declares twice.
        self.tick(w, date(2010, 9, 28))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3"], self.cpw_news(w))
        for first in (date(2010, 9, 27), date(2010, 10, 15), date(2011, 10, 1)):
            late, _, _ = self.cpw(first)
            self.tick(late, first)
            self.assertTrue({"ac_cpw_closed", "ac_cpw_late_start_skipped"} <= late.globals, first)
            self.assertNotIn("ac_cpw_calendar_started", late.globals)
            self.tick(late, date(2011, 1, 7))
            self.assertEqual([], self.cpw_news(late))
            self.assertEqual(set(), late.wars)
        gone, _, _ = self.cpw()
        for state in gone.states.values():
            if state.owner == "OSE":
                state.owner = state.controller = "BLK"
        self.tick(gone, date(2010, 9, 22))
        self.assertTrue({"ac_cpw_closed", "ac_cpw_principal_missing"} <= gone.globals)

    def test_declaration_window_falls_back_to_history_and_withholding_needs_the_mandate(self):
        w, y, o = self.cpw()
        self.anchor(w)
        self.tick(w, date(2010, 10, 4))
        self.assertNotIn("ac_cpw_started", w.globals)
        self.tick(w, date(2010, 10, 12))
        self.assertIn("ac_cpw_started", w.globals)
        self.assertEqual({frozenset(("YUK", "OSE"))}, w.wars)
        w2, y2, o2 = self.cpw()
        self.anchor(w2)
        # The withhold option is gated by its own trigger; without the mandate the engine never offers it,
        # and the effect behind it is guarded in the same way.
        with self.assertRaises(AssertionError):
            w2.option("ac_cpw.5", "b", "YUK")
        w2.run("ac_cpw_withhold", "YUK")
        self.assertNotIn("ac_cpw_declaration_withheld", w2.globals)
        self.assertIn("ac_cpw_declaration_pending", y2.flags)
        self.earn(w2, "YUK", "verification")
        w2.option("ac_cpw.5", "b", "YUK")
        self.assertIn("ac_cpw_declaration_withheld", w2.globals)
        self.assertIn("ac_cpw_yuk_mandate_kept", y2.ideas)
        self.assertNotIn("ac_cpw_declaration_pending", y2.flags)
        self.assertEqual(set(), w2.wars)
        for day in (date(2010, 9, 30), date(2010, 10, 25), date(2010, 12, 31), date(2011, 3, 1)):
            self.tick(w2, day)
        self.assertEqual(["ac_cpw.5", "ac_cpw.7"], [e for _, e, _ in w2.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2")])
        self.assertFalse({"ac_cpw_started", "ac_cpw_closed"} & w2.globals)

    def test_unable_principals_and_refused_declarations_close_the_owner(self):
        for fault in ("yuk_capitulated", "yuk_subject", "ose_capitulated", "ose_subject"):
            with self.subTest(fault=fault):
                w, y, o = self.cpw()
                target = y if fault.startswith("yuk") else o
                setattr(target, "capitulated" if fault.endswith("capitulated") else "subject", True)
                self.anchor(w)
                self.assertTrue({"ac_cpw_closed", "ac_cpw_principal_unable"} <= w.globals)
                self.assertFalse({"ac_cpw_started", "ac_cpw_prevented"} & w.globals)
                self.assertNotIn(("YUK", "ac_cpw.5", w.today + 1), w.events)
                self.assertEqual(set(), w.wars)
                self.tick(w, date(2010, 9, 30))
                self.assertNotIn("ac_cpw_stage_eaglin", w.globals)
        # The engine may not create the war; the owner then writes no war state and closes.
        refused, y, o = self.cpw()
        refused.refuse_war = True
        self.anchor(refused)
        refused.option("ac_cpw.5", "a", "YUK")
        self.assertTrue({"ac_cpw_closed", "ac_cpw_declaration_refused"} <= refused.globals)
        self.assertFalse({"ac_cpw_started", "ac_cpw_pre_existing_war", "ac_cpw_ended"} & refused.globals)
        self.assertFalse({"ac_cpw_yuk_war_footing", "ac_cpw_yuk_submarine_carriers"} & y.ideas)
        self.assertNotIn("ac_cpw_ose_war_footing", o.ideas)
        self.assertNotIn("ac_cpw_declaration_pending", y.flags)
        self.tick(refused, date(2010, 9, 30))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2"], self.cpw_news(refused))

    def test_status_text_and_historical_course_follow_the_actual_route(self):
        pending, _, _ = self.cpw()
        self.tick(pending, date(2010, 9, 22))
        self.assertTrue(self.status(pending).startswith("Pending"))
        closed, _, _ = self.cpw(date(2010, 10, 15))
        self.tick(closed, date(2010, 10, 15))
        self.assertTrue(self.status(closed).startswith("Closed"))
        prevented, _, _ = self.cpw()
        for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "verification"), ("YUK", "channel")):
            self.earn(prevented, tag, record)
        self.anchor(prevented)
        self.assertTrue(self.status(prevented).startswith("Prevented"))
        withheld, _, _ = self.cpw()
        self.anchor(withheld)
        self.earn(withheld, "YUK", "verification")
        withheld.option("ac_cpw.5", "b", "YUK")
        self.assertTrue(self.status(withheld).startswith("Withheld"))
        running, _, _ = self.cpw()
        self.declare(running)
        self.assertTrue(self.status(running).startswith("Running on the official course"))
        running.wars.add(frozenset(("YUK", "BLK")))
        self.tick(running, date(2010, 9, 30))
        self.assertTrue(self.status(running).startswith("Running under external observation: other fighting"))
        running.wars.clear()
        self.tick(running, date(2010, 10, 7))
        self.assertTrue(self.status(running).startswith("Ended: the fighting stopped while the owner observed"))
        existing, _, _ = self.cpw()
        existing.wars.add(frozenset(("OSE", "YUK")))
        self.anchor(existing)
        self.assertTrue(self.status(existing).startswith("Running under external observation: Osea and Yuktobania were already at war"))
        # An untainted cessation before the SOLG stage is an early end, not the official course.
        early, _, _ = self.cpw()
        self.declare(early)
        early.wars.clear()
        self.tick(early, date(2010, 10, 4))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation"} <= early.globals)
        self.assertNotIn("ac_cpw_historical_course", early.globals)
        self.assertIn(("OSE", "ac_cpw.10", early.today + 1), early.events)
        self.assertTrue(self.status(early).startswith("Ended: the fighting stopped without capitulation before the official course"))
        victory, y, o = self.cpw()
        self.declare(victory)
        y.capitulated = True
        victory.wave_action("circum_pacific", "on_capitulation_immediate", "YUK", "OSE")
        self.assertTrue(self.status(victory).startswith("Ended: Yuktobania capitulated"))

    def test_reciprocal_exchange_prevents_the_declaration_and_is_earned(self):
        w, y, o = self.cpw()
        for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "verification"), ("YUK", "channel")):
            self.earn(w, tag, record)
        self.anchor(w)
        self.assertIn("ac_cpw_prevented", w.globals)
        self.assertNotIn("ac_cpw_started", w.globals)
        self.assertNotIn(("YUK", "ac_cpw.5", w.today + 1), w.events)
        self.assertEqual(set(), w.wars)
        self.assertIn("ac_cpw_yuk_exchange_standing", y.ideas)
        self.assertIn("ac_cpw_ose_exchange_standing", o.ideas)
        self.assertEqual(["ac_cpw.4"], [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2")])
        partial, _, _ = self.cpw()
        for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "channel")):
            self.earn(partial, tag, record)
        self.anchor(partial)
        self.assertNotIn("ac_cpw_prevented", partial.globals)
        self.assertIn(("YUK", "ac_cpw.5", partial.today + 1), partial.events)
        # Routes settled while the declaration is still being asked clear the pending state.
        for settled in ("prevented", "observed", "closed"):
            with self.subTest(settled=settled):
                asked, ya, oa = self.cpw()
                self.anchor(asked)
                self.assertTrue({"ac_cpw_declaration_asked", "ac_cpw_declaration_pending", "ac_cpw_declaration_window"} <= set(ya.flags))
                if settled == "prevented":
                    for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "verification"), ("YUK", "channel")):
                        self.earn(asked, tag, record)
                elif settled == "observed":
                    asked.wars.add(frozenset(("OSE", "YUK")))
                else:
                    ya.subject = True
                self.tick(asked, date(2010, 10, 4))
                self.assertIn({"prevented": "ac_cpw_prevented", "observed": "ac_cpw_existing_war_observed", "closed": "ac_cpw_principal_unable"}[settled], asked.globals)
                self.assertFalse({"ac_cpw_declaration_pending", "ac_cpw_declaration_window"} & set(ya.flags))
                self.assertIn("ac_cpw_declaration_asked", ya.flags)
                with self.assertRaises(AssertionError):
                    asked.option("ac_cpw.5", "a", "YUK")
                self.tick(asked, date(2011, 3, 1))
                self.assertEqual(set() if settled != "observed" else {frozenset(("OSE", "YUK"))}, asked.wars)
                self.assertNotIn("ac_cpw.3", [e for _, e, _ in asked.events])
                self.assertFalse({"ac_cpw_yuk_war_footing"} & ya.ideas)

    def test_historical_course_fires_each_stage_once_and_ends_on_observed_cessation(self):
        w, y, o = self.cpw()
        w.globals.add("ac_sp_arkbird_complete")
        o.ideas |= {"ac_sp_arkbird_debris_clearing", "ac_sp_arkbird_joint_operations"}
        y.ideas.add("ac_sp_arkbird_joint_operations")
        self.earn(w, "YUK", "channel")
        records_before = self.records(w)
        self.declare(w)
        self.tick(w, date(2010, 9, 30))
        self.assertIn("ac_cpw_stage_eaglin", w.globals)
        self.assertIn("ac_cpw_ose_carrier_losses", o.ideas)
        self.assertIn(("OSE", "ac_cpw.6", w.today + 1), w.events)
        w.option("ac_cpw.6", "a", "OSE")
        self.assertIn("ac_cpw_arkbird_committed", w.globals)
        self.assertIn("ac_cpw_ose_arkbird_at_the_front", o.ideas)
        self.tick(w, date(2010, 10, 4))
        self.assertNotIn("ac_cpw_yuk_submarine_carriers", y.ideas)
        self.assertIn("ac_cpw_yuk_submarine_carrier", y.ideas)
        self.tick(w, date(2010, 10, 22))
        self.tick(w, date(2010, 10, 25))
        self.assertIn("ac_cpw_arkbird_sabotaged", w.globals)
        self.assertIn("ac_cpw_ose_arkbird_grounded", o.ideas)
        self.tick(w, date(2010, 11, 1))
        self.assertNotIn("ac_cpw_stage_bastok", w.globals)
        # State 515 is Yuktobanian-owned but not a Yuktobanian core; holding it is not the foothold.
        self.assertEqual(("YUK", False), (w.states[515].owner, "YUK" in w.states[515].cores))
        w.states[515].controller = "OSE"
        self.tick(w, date(2010, 11, 1))
        self.assertNotIn("ac_cpw_stage_bastok", w.globals)
        w.states[515].controller = "YUK"
        # State 125 is a Yuktobanian core; Osean control of it is the observed foothold.
        self.assertIn("YUK", w.states[125].cores)
        w.states[125].controller = "OSE"
        self.tick(w, date(2010, 11, 1))
        self.assertIn("ac_cpw_stage_bastok", w.globals)
        self.assertIn("ac_cpw_ose_expeditionary_strain", o.ideas)
        self.tick(w, date(2010, 11, 2))
        self.assertIn("ac_cpw_ose_dresdene_inquiry", o.ideas)
        self.tick(w, date(2010, 11, 4))
        self.assertIn("ac_cpw_ose_home_front_alert", o.ideas)
        self.tick(w, date(2010, 11, 14))
        self.assertFalse({"ac_cpw_yuk_submarine_carriers", "ac_cpw_yuk_submarine_carrier"} & y.ideas)
        self.tick(w, date(2010, 11, 29))
        self.tick(w, date(2010, 12, 6))
        self.assertIn("ac_cpw_yuk_stronghold_lost", y.ideas)
        self.tick(w, date(2010, 12, 9))
        self.assertIn("ac_cpw_ose_president_returns", o.ideas)
        self.tick(w, date(2010, 12, 19))
        self.assertIn("ac_cpw_arkbird_lost", w.globals)
        self.assertFalse({"ac_sp_arkbird_debris_clearing", "ac_sp_arkbird_joint_operations"} & (o.ideas | y.ideas))
        self.assertFalse({"ac_cpw_ose_arkbird_at_the_front", "ac_cpw_ose_arkbird_grounded"} & o.ideas)
        self.assertIn("ac_sp_arkbird_complete", w.globals)
        self.tick(w, date(2010, 12, 23))
        self.assertIn("ac_cpw_yuk_leadership_question", y.ideas)
        self.tick(w, date(2010, 12, 29))
        # The ninety-day carrier-losses spirit added on 30 September has expired by now.
        self.assertNotIn("ac_cpw_ose_carrier_losses", o.ideas)
        self.tick(w, date(2010, 12, 30))
        self.assertIn("ac_cpw_appeal_made", w.globals)
        self.assertTrue("ac_cpw_disarmament_appeal" in y.ideas and "ac_cpw_disarmament_appeal" in o.ideas)
        self.tick(w, date(2010, 12, 31))
        self.assertNotIn("ac_cpw_ended", w.globals)
        self.tick(w, date(2011, 1, 7))
        self.assertNotIn("ac_cpw_ended", w.globals)
        w.wars.clear()
        self.tick(w, date(2011, 1, 14))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation", "ac_cpw_historical_course"} <= w.globals)
        self.assertFalse(any(i.startswith("ac_cpw_") and i.endswith(("_war_footing", "_carriers", "_carrier", "_appeal")) for i in y.ideas | o.ideas))
        self.tick(w, date(2011, 1, 21))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3", "ac_cpw.20", "ac_cpw.15", "ac_cpw.21", "ac_cpw.22", "ac_cpw.23", "ac_cpw.24", "ac_cpw.25",
                          "ac_cpw.26", "ac_cpw.27", "ac_cpw.28", "ac_cpw.29", "ac_cpw.30", "ac_cpw.31", "ac_cpw.32", "ac_cpw.33", "ac_cpw.34", "ac_cpw.35",
                          "ac_cpw.10"], self.cpw_news(w))
        self.assertEqual(records_before, self.records(w))
        self.assertTrue(self.status(w).startswith("Ended: the fighting stopped without capitulation after the official course"))

    def test_arkbird_stages_need_the_completed_project_and_the_commitment(self):
        w, y, o = self.cpw()
        self.declare(w)
        for day in (date(2010, 9, 30), date(2010, 10, 25), date(2010, 12, 19)):
            self.tick(w, day)
        self.assertNotIn(("OSE", "ac_cpw.6"), [(t, e) for t, e, _ in w.events])
        self.assertFalse({"ac_cpw_stage_arkbird_sabotage", "ac_cpw_stage_arkbird_lost"} & w.globals)
        self.assertIn("ac_cpw_stage_eaglin", w.globals)
        held, y2, o2 = self.cpw()
        held.globals.add("ac_sp_arkbird_complete")
        self.declare(held)
        self.tick(held, date(2010, 9, 30))
        held.option("ac_cpw.6", "b", "OSE")
        self.assertIn("ac_cpw_arkbird_held_back", held.globals)
        for day in (date(2010, 10, 7), date(2010, 10, 25), date(2010, 12, 19)):
            self.tick(held, day)
        self.assertEqual(1, [e for _, e, _ in held.events].count("ac_cpw.6"))
        self.assertFalse({"ac_cpw_arkbird_committed", "ac_cpw_stage_arkbird_sabotage", "ac_cpw_stage_arkbird_lost"} & held.globals)
        # An answer left until the sabotage row has passed holds the Arkbird back instead of replaying its fate.
        late, y3, o3 = self.cpw()
        late.globals.add("ac_sp_arkbird_complete")
        self.declare(late)
        self.tick(late, date(2010, 9, 30))
        self.tick(late, date(2010, 10, 25))
        late.option("ac_cpw.6", "a", "OSE")
        self.assertIn("ac_cpw_arkbird_held_back", late.globals)
        self.assertNotIn("ac_cpw_arkbird_committed", late.globals)
        self.assertNotIn("ac_cpw_ose_arkbird_at_the_front", o3.ideas)
        self.tick(late, date(2010, 12, 19))
        self.assertFalse({"ac_cpw_stage_arkbird_sabotage", "ac_cpw_stage_arkbird_lost"} & late.globals)

    def test_pre_existing_or_third_party_wars_move_the_crisis_to_external_observation(self):
        w, y, o = self.cpw()
        w.wars.add(frozenset(("OSE", "BLK")))
        self.declare(w)
        self.assertTrue({"ac_cpw_tainted", "ac_cpw_pre_existing_war"} <= w.globals)
        self.tick(w, date(2010, 9, 30))
        self.assertNotIn("ac_cpw_stage_eaglin", w.globals)
        w.wars.discard(frozenset(("YUK", "OSE")))
        self.tick(w, date(2010, 10, 7))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation"} <= w.globals)
        self.assertNotIn("ac_cpw_historical_course", w.globals)
        self.assertEqual(["ac_cpw.3", "ac_cpw.9", "ac_cpw.13"], [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2", "ac_cpw.5")])
        later, y2, o2 = self.cpw()
        self.declare(later)
        self.tick(later, date(2010, 9, 30))
        self.assertIn("ac_cpw_stage_eaglin", later.globals)
        later.wars.add(frozenset(("YUK", "BLK")))
        self.tick(later, date(2010, 10, 4))
        self.assertIn("ac_cpw_tainted", later.globals)
        self.assertNotIn("ac_cpw_stage_sand_island", later.globals)
        self.assertIn("ac_cpw.9", [e for _, e, _ in later.events])
        self.assertIn("ac_cpw_yuk_war_footing", y2.ideas)
        # A war the pair already fights is started but not expanded; the course is not asserted and a reload adds nothing.
        existing, y3, o3 = self.cpw()
        existing.wars.add(frozenset(("OSE", "YUK")))
        self.anchor(existing)
        self.assertTrue({"ac_cpw_started", "ac_cpw_existing_war_observed"} <= existing.globals)
        self.assertNotIn("ac_cpw_tainted", existing.globals)
        self.assertNotIn(("YUK", "ac_cpw.5", existing.today + 1), existing.events)
        self.assertNotIn("ac_cpw_yuk_war_footing", y3.ideas)
        self.assertIn("ac_cpw.8", [e for _, e, _ in existing.events])
        existing.wave_action("circum_pacific", "on_startup")
        self.assertFalse({"ac_cpw_yuk_war_footing", "ac_cpw_ose_war_footing"} & (y3.ideas | o3.ideas))
        self.tick(existing, date(2010, 9, 30))
        self.assertNotIn("ac_cpw_stage_eaglin", existing.globals)
        existing.wars.clear()
        self.tick(existing, date(2010, 10, 7))
        self.assertIn("ac_cpw_ended", existing.globals)
        self.assertNotIn("ac_cpw_historical_course", existing.globals)
        self.assertIn("ac_cpw.13", [e for _, e, _ in existing.events])
        # A principal's own subject joining its war is not a third party; anyone else is.
        vassal, y4, o4 = self.cpw()
        self.declare(vassal)
        vassal.countries["BLK"].overlord = "OSE"
        vassal.wars.add(frozenset(("BLK", "YUK")))
        self.tick(vassal, date(2010, 9, 30))
        self.assertNotIn("ac_cpw_tainted", vassal.globals)
        self.assertIn("ac_cpw_stage_eaglin", vassal.globals)
        vassal.countries["BLK"].overlord = None
        self.tick(vassal, date(2010, 10, 4))
        self.assertIn("ac_cpw_tainted", vassal.globals)
        self.assertNotIn("ac_cpw_stage_sand_island", vassal.globals)

    def test_capitulation_and_annexation_record_the_actual_outcome(self):
        w, y, o = self.cpw()
        w.globals.add("ac_sp_arkbird_complete")
        self.declare(w)
        self.tick(w, date(2010, 9, 30))
        w.option("ac_cpw.6", "a", "OSE")
        self.assertIn("ac_cpw_ose_arkbird_at_the_front", o.ideas)
        y.capitulated = True
        w.wave_action("circum_pacific", "on_capitulation_immediate", "YUK", "OSE")
        self.assertTrue({"ac_cpw_yuk_fallen", "ac_cpw_ended", "ac_cpw_outcome_osean_victory"} <= w.globals)
        # The end news is scheduled by the surviving principal, never by the fallen scope.
        self.assertIn(("OSE", "ac_cpw.11", w.today + 1), w.events)
        # Every untimed owner idea leaves with the war, including the Arkbird deployment.
        self.assertFalse({i for i in o.ideas | y.ideas if i.startswith("ac_cpw_") and i not in ("ac_cpw_ose_carrier_losses",)})
        w2, y2, o2 = self.cpw()
        self.declare(w2)
        w2.wave_action("circum_pacific", "on_annex", "YUK", "OSE")
        self.assertTrue({"ac_cpw_ose_fallen", "ac_cpw_ended", "ac_cpw_outcome_yuktobanian_victory"} <= w2.globals)
        self.assertIn(("YUK", "ac_cpw.12", w2.today + 1), w2.events)
        # A breakaway that shares a principal's original tag is not the principal.
        split, y5, o5 = self.cpw()
        self.declare(split)
        breakaway = copy.deepcopy(o5)
        breakaway.tag = "D01"
        breakaway.capitulated = True
        split.countries["D01"] = breakaway
        split.wave_action("circum_pacific", "on_capitulation_immediate", "D01", "OSE")
        self.assertFalse({"ac_cpw_ended", "ac_cpw_ose_fallen", "ac_cpw_yuk_fallen"} & split.globals)
        # A principal annexed by a third party is not the other principal's victory, and the
        # survivor's later observation never re-attributes it.
        for fallen, annexer, victory, news in (("YUK", "BLK", "ac_cpw_outcome_osean_victory", "ac_cpw.11"), ("OSE", "BLK", "ac_cpw_outcome_yuktobanian_victory", "ac_cpw.12")):
            with self.subTest(fallen=fallen):
                third, y6, o6 = self.cpw()
                self.declare(third)
                third.wave_action("circum_pacific", "on_annex", annexer, fallen)
                self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation", "ac_cpw_tainted", "ac_cpw_external_fall", f"ac_cpw_{fallen.lower()}_fallen"} <= third.globals)
                self.assertNotIn(victory, third.globals)
                survivor = "OSE" if fallen == "YUK" else "YUK"
                self.assertIn((survivor, "ac_cpw.13", third.today + 1), third.events)
                self.assertNotIn(news, [e for _, e, _ in third.events])
                for state in third.states.values():
                    if state.owner == fallen:
                        state.owner = state.controller = annexer
                self.tick(third, date(2010, 10, 4), survivor)
                self.assertNotIn(victory, third.globals)
                self.assertTrue(self.status(third).startswith("Ended: the fighting stopped while the owner observed"))
        # A capitulation after the pair has already made peace is not a victory either.
        race, y7, o7 = self.cpw()
        self.declare(race)
        race.wars.clear()
        y7.capitulated = True
        race.wave_action("circum_pacific", "on_capitulation_immediate", "YUK", "OSE")
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation", "ac_cpw_external_fall"} <= race.globals)
        self.assertNotIn("ac_cpw_outcome_osean_victory", race.globals)
        self.assertIn(("OSE", "ac_cpw.13", race.today + 1), race.events)
        # A capitulation to a third party, or a subject annexed by a third overlord, is not the
        # other principal's victory either; the hooks dispatch on the winner in FROM.
        for hook, fallen, winner, victory in (("on_capitulation_immediate", "YUK", "BLK", "ac_cpw_outcome_osean_victory"),
                                              ("on_subject_annexed", "OSE", "BLK", "ac_cpw_outcome_yuktobanian_victory")):
            with self.subTest(hook=hook):
                w8, y8, o8 = self.cpw()
                self.declare(w8)
                (y8 if fallen == "YUK" else o8).capitulated = hook == "on_capitulation_immediate"
                w8.wave_action("circum_pacific", hook, fallen, winner)
                self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation", "ac_cpw_external_fall", f"ac_cpw_{fallen.lower()}_fallen"} <= w8.globals)
                self.assertNotIn(victory, w8.globals)
        overlord, y9, o9 = self.cpw()
        self.declare(overlord)
        overlord.wave_action("circum_pacific", "on_subject_annexed", "YUK", "OSE")
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_osean_victory"} <= overlord.globals)
        self.assertNotIn("ac_cpw_external_fall", overlord.globals)
        w3, y3, o3 = self.cpw()
        self.declare(w3)
        for state in w3.states.values():
            if state.owner == "YUK":
                state.owner = state.controller = "OSE"
        self.tick(w3, date(2010, 10, 4), "OSE")
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_osean_victory"} <= w3.globals)

    def test_crisis_decisions_cost_once_and_follow_the_phase(self):
        rows = {k: v for category in parse(text("common/decisions/ac_circum_pacific.txt")) for k, _, v in category[2]}
        for tag in ("OSE", "YUK"):
            with self.subTest(tag=tag):
                w, y, o = self.cpw()
                c = w.countries[tag]
                home, record = rows[f"{tag}_cpw_home_front"], rows[f"{tag}_cpw_war_record"]
                self.assertFalse(w.trigger(fields(home)["available"], c))
                self.declare(w)
                self.assertTrue(w.trigger(fields(home)["available"], c))
                self.assertFalse(w.trigger(fields(record)["available"], c))
                # The engine charges `cost` once; the effects must not charge it again.
                self.assertEqual(("50", "25"), (fields(home)["cost"], fields(record)["cost"]))
                self.assertEqual(("yes", "yes"), (fields(home)["fire_only_once"], fields(record)["fire_only_once"]))
                pp = c.pp
                w.execute(fields(home)["complete_effect"], c)
                self.assertEqual(pp, c.pp)
                self.assertIn(f"ac_cpw_{tag.lower()}_home_front", c.ideas)
                self.assertFalse(w.trigger(fields(home)["available"], c))
                snapshot = copy.deepcopy(c)
                w.execute(fields(home)["complete_effect"], c)
                self.assertEqual(snapshot, c)
                w.wars.clear()
                self.tick(w, date(2010, 10, 4))
                self.assertTrue(w.trigger(fields(record)["available"], c))
                w.execute(fields(record)["complete_effect"], c)
                self.assertEqual(pp, c.pp)
                self.assertIn(f"ac_cpw_{tag.lower()}_war_record", c.ideas)
        self.assertNotIn("add_political_power", text("common/scripted_effects/ac_circum_pacific.txt"))

    def test_circum_pacific_peace_is_earned_after_the_appeal(self):
        rows = {k: v for category in parse(text("common/decisions/ac_circum_pacific.txt")) for k, _, v in category[2]}
        offer = {tag: rows[f"{tag}_cpw_accept_appeal"] for tag in ("OSE", "YUK")}
        w, y, o = self.cpw()
        self.declare(w)
        self.earn(w, "OSE", "verification")
        self.tick(w, date(2010, 12, 1))
        # Before the appeal the offer is neither shown nor available, even with the record.
        self.assertFalse(w.trigger(fields(offer["OSE"])["visible"], o))
        self.assertFalse(w.trigger(fields(offer["OSE"])["available"], o))
        self.tick(w, date(2010, 12, 30))
        self.assertIn("ac_cpw_appeal_made", w.globals)
        self.assertTrue(w.trigger(fields(offer["OSE"])["visible"], o))
        self.assertTrue(w.trigger(fields(offer["OSE"])["available"], o))
        # Yuktobania has not earned its own verification record.
        self.assertTrue(w.trigger(fields(offer["YUK"])["visible"], y))
        self.assertFalse(w.trigger(fields(offer["YUK"])["available"], y))
        self.assertEqual("50", fields(offer["OSE"])["cost"])
        pp = o.pp
        w.execute(fields(offer["OSE"])["complete_effect"], o)
        self.assertEqual(pp, o.pp)
        self.assertIn(("YUK", "ac_cpw.16"), [(t, e) for t, e, _ in w.events])
        self.assertFalse(w.trigger(fields(offer["OSE"])["available"], o))
        # A refusal keeps the war; the offer can be renewed after thirty days.
        w.option("ac_cpw.16", "b", "YUK")
        self.assertIn("ac_cpw_peace_refused", w.globals)
        self.assertEqual({frozenset(("OSE", "YUK"))}, w.wars)
        self.tick(w, date(2011, 1, 7))
        self.assertFalse(w.trigger(fields(offer["OSE"])["available"], o))
        self.tick(w, date(2011, 1, 31))
        self.assertTrue(w.trigger(fields(offer["OSE"])["available"], o))
        w.execute(fields(offer["OSE"])["complete_effect"], o)
        records_before = self.records(w)
        w.option("ac_cpw.16", "a", "YUK")
        self.assertEqual(set(), w.wars)
        self.assertTrue({"ac_cpw_peace_made", "ac_cpw_ended", "ac_cpw_outcome_peace"} <= w.globals)
        self.assertFalse({"ac_cpw_outcome_cessation", "ac_cpw_historical_course", "ac_cpw_outcome_osean_victory"} & w.globals)
        self.assertEqual("ac_cpw.17", self.cpw_news(w)[-1])
        self.assertEqual(records_before, self.records(w))
        self.assertFalse(any(i.startswith("ac_cpw_") and i.endswith(("_war_footing", "_appeal")) for i in y.ideas | o.ideas))
        self.assertTrue(self.status(w).startswith("Ended: peace on the terms of the joint appeal"))
        self.assertFalse(w.trigger(fields(offer["OSE"])["visible"], o))
        # The stories' four route flags are unchanged by the peace.
        self.assertEqual({"ac_cpw_started"}, set(STORY_FLAGS) & w.globals)

    def test_circum_pacific_peace_is_written_only_if_the_engine_ends_the_war(self):
        rows = {k: v for category in parse(text("common/decisions/ac_circum_pacific.txt")) for k, _, v in category[2]}
        w, y, o = self.cpw()
        self.declare(w)
        self.earn(w, "YUK", "verification")
        self.tick(w, date(2010, 12, 30))
        w.execute(fields(rows["YUK_cpw_accept_appeal"])["complete_effect"], y)
        self.assertIn(("OSE", "ac_cpw.16"), [(t, e) for t, e, _ in w.events])
        w.refuse_peace = True
        w.option("ac_cpw.16", "a", "OSE")
        self.assertEqual({frozenset(("OSE", "YUK"))}, w.wars)
        self.assertIn("ac_cpw_peace_not_made", w.globals)
        self.assertFalse({"ac_cpw_peace_made", "ac_cpw_ended", "ac_cpw_outcome_peace"} & w.globals)
        self.assertTrue(self.status(w).startswith("Running: a peace on the appeal's terms was accepted, but the engine kept the war"))
        # No further offer; the end is recorded when the fighting actually stops.
        self.assertFalse(w.trigger(fields(rows["OSE_cpw_accept_appeal"])["available"], o))
        w.wars.clear()
        self.tick(w, date(2011, 1, 7))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation"} <= w.globals)
        self.assertNotIn("ac_cpw_outcome_peace", w.globals)
        # The offer never reaches a tainted or observed war: the appeal stage needs the official course.
        tainted, y2, o2 = self.cpw()
        self.declare(tainted)
        self.earn(tainted, "OSE", "verification")
        tainted.globals.add("ac_cpw_tainted")
        self.tick(tainted, date(2010, 12, 30))
        self.assertNotIn("ac_cpw_appeal_made", tainted.globals)
        self.assertFalse(tainted.trigger(fields(rows["OSE_cpw_accept_appeal"])["visible"], o2))

    # The Belkan War record: reference briefs on observed state ------------------------
    def bwr_run(self, w, start, end, before_tick=None):
        """Advance week by week from `start` to `end`, observing on Osea's weekly pulse."""
        day = start
        while day <= end:
            if before_tick:
                before_tick(w, day)
            self.tick(w, day, "OSE", "belkan_record")
            day += timedelta(days=7)
        return [e for _, e, _ in w.events if e.startswith("ac_bwr.")]

    def bwr_world(self, today):
        w = self.fresh()
        w.today = today.toordinal()
        return w

    def test_belkan_record_writes_only_its_own_flags_and_fires_each_brief_from_one_place(self):
        effects = text("common/scripted_effects/ac_belkan_record.txt")
        self.assertEqual(set(), {f for f in re.findall(r"set_global_flag = (\w+)", effects) if not f.startswith("ac_bwr_")})
        self.assertNotRegex(effects, r"set_country_flag|set_variable|add_to_variable|add_ideas|add_timed_idea|clr_global_flag|transfer_state|declare_war_on")
        for number in range(1, 14):
            self.assertEqual(1, effects.count(f"news_event = {{ id = ac_bwr.{number} days = 1 }}"), number)
        loc = self.loc_of("belkan_record")
        for citation in ("1991 / 07.29", "1991 / 09.02", "1991 / 12.16", "1995 / 03.27", "1995 / 03.30", "1995 / 04.01", "1995 / 04.03",
                         "1995 / 04.24", "1995 / 05.13", "1995 / 05.14", "1995 / 06.05", "1995 / 10.18", "1996 / 04.18", "1999 / 09.16"):
            self.assertIn(citation, "\n".join(loc.values()), citation)
        # Owners the archive keeps are cited in the ledger, never fired again here.
        for date_text in ("1992 / 02.24", "1995 / 05.23", "1995 / 06.04", "1995 / 06.06"):
            self.assertNotIn(date_text, "\n".join(loc.values()))
        self.assertFalse((MOD / "common/scripted_triggers/ac_belkan_record.txt").exists())

    def test_belkan_record_date_briefs_fire_once_inside_their_windows(self):
        w = self.bwr_world(date(1991, 1, 4))
        news = self.bwr_run(w, date(1991, 1, 4), date(1999, 12, 31))
        # No war, no land sale: only the dated, state-free rows report.
        self.assertEqual(["ac_bwr.1", "ac_bwr.2", "ac_bwr.11", "ac_bwr.12", "ac_bwr.13"], news)
        for name in ("borders_redrawn", "model", "monte_rosa", "ustio_allies", "osean_army", "futuro_canal", "directus", "waldreich"):
            self.assertIn(f"ac_bwr_{name}_skipped", w.globals, name)
            self.assertNotIn(f"ac_bwr_{name}", w.globals, name)
        self.assertNotIn("ac_bwr_directus_occupied", w.globals)

    def test_belkan_record_land_sale_brief_waits_for_the_sale(self):
        sold = self.bwr_world(date(1991, 12, 1))
        def sell(w, day):
            if day >= date(1992, 3, 1):
                w.countries["BLK"].completed.add("BLK_sell_the_land")
        news = self.bwr_run(sold, date(1991, 12, 1), date(1992, 4, 1), sell)
        self.assertEqual(["ac_bwr.3"], news)
        late = self.bwr_world(date(1991, 12, 1))
        late.countries["BLK"].completed.add("BLK_sell_the_land")
        self.bwr_run(late, date(1991, 12, 1), date(1991, 12, 14))
        self.assertNotIn("ac_bwr_borders_redrawn", late.globals)     # never before the record's date
        self.bwr_run(late, date(1991, 12, 21), date(1991, 12, 21))
        self.assertIn("ac_bwr_borders_redrawn", late.globals)

    def test_belkan_record_war_briefs_follow_the_observed_war(self):
        w = self.bwr_world(date(1995, 3, 1))
        directus = w.states[335]
        def course(w, day):
            if day >= date(1995, 3, 25):
                w.globals.add("belkan_war_is_happening")
                w.wars |= {frozenset(("BLK", "GEB")), frozenset(("BLK", "OSE"))}
                w.factions.update(OSE="OSE", UST="OSE")
            directus.controller = "BLK" if date(1995, 3, 28) <= day < date(1995, 5, 10) else "UST"
            if day >= date(1995, 6, 20):
                w.globals.discard("belkan_war_is_happening")
                w.wars.clear()
        news = self.bwr_run(w, date(1995, 3, 1), date(1995, 12, 31), course)
        self.assertEqual(["ac_bwr.4", "ac_bwr.5", "ac_bwr.6", "ac_bwr.7", "ac_bwr.8", "ac_bwr.9", "ac_bwr.10", "ac_bwr.11"], news)
        self.assertIn("ac_bwr_directus_occupied", w.globals)
        # Nothing the briefs observe was changed by them.
        self.assertEqual(("UST", "UST"), (directus.owner, directus.controller))

    def test_belkan_record_needs_the_state_it_reports(self):
        # Ustio never occupied and never capitulated: no occupation or liberation brief.
        held = self.bwr_world(date(1995, 3, 1))
        def war(w, day):
            w.globals.add("belkan_war_is_happening")
            w.wars.add(frozenset(("BLK", "OSE")))
        news = self.bwr_run(held, date(1995, 3, 1), date(1996, 1, 10), war)
        self.assertNotIn("ac_bwr.5", news)
        self.assertNotIn("ac_bwr.9", news)
        self.assertNotIn("ac_bwr.4", news)      # no war with Gebet
        self.assertNotIn("ac_bwr.6", news)      # Ustio in no faction with Osea
        self.assertTrue({"ac_bwr_monte_rosa_skipped", "ac_bwr_directus_skipped", "ac_bwr_model_skipped"} <= held.globals)
        # A capitulated Ustio is reported as the occupation.
        fallen = self.bwr_world(date(1995, 3, 1))
        def capitulate(w, day):
            war(w, day)
            w.countries["UST"].capitulated = day >= date(1995, 4, 10)
        self.assertIn("ac_bwr.5", self.bwr_run(fallen, date(1995, 3, 1), date(1995, 4, 30), capitulate))
        # Without Belka the war rows never report, even with the flag set.
        absent = self.bwr_world(date(1995, 3, 1))
        for state in absent.states.values():
            if state.owner == "BLK":
                state.owner = state.controller = "OSE"
        news = self.bwr_run(absent, date(1995, 3, 1), date(1995, 12, 31), lambda w, d: w.globals.add("belkan_war_is_happening"))
        self.assertFalse({"ac_bwr.4", "ac_bwr.5", "ac_bwr.8", "ac_bwr.10"} & set(news))

    def test_belkan_record_late_save_reports_nothing_already_past(self):
        w = self.bwr_world(date(1996, 6, 1))
        news = self.bwr_run(w, date(1996, 6, 1), date(1999, 12, 31))
        self.assertEqual(["ac_bwr.13"], news)
        for name in ("kestrel_ordered", "cinigrad", "borders_redrawn", "model", "waldreich", "espada", "tyler"):
            self.assertIn(f"ac_bwr_{name}_skipped", w.globals, name)

    # Wave F1: the Lighthouse War owner -------------------------------------------------
    FOREIGN = ("ac_ucw_", "ac_sp_", "ac_release_", "ac_fe_", "ac_snc_")

    def lhw(self, today=date(2019, 1, 25), history="ac_ucw_outcome_isaf_victory"):
        w = self.fresh()
        w.today = today.toordinal()
        if history:
            w.globals.add(history)
        return w, w.countries["ERU"], w.countries["OSE"]

    def ltick(self, w, day, tag="ERU"):
        self.tick(w, day, tag, "lighthouse")

    def lanchor(self, w):
        self.ltick(w, date(2019, 2, 1))
        self.ltick(w, date(2019, 5, 15))

    def ldeclare(self, w):
        self.lanchor(w)
        w.option("ac_lhw.5", "a", "ERU")
        self.assertIn("ac_lhw_started", w.globals)
        return w

    def lnews(self, w):
        return [e for _, e, _ in w.events if e.startswith("ac_lhw.") and e not in ("ac_lhw.5", "ac_lhw.6")]

    def lstatus(self, w):
        return self.status(w, "lighthouse", "ERU")

    def foreign(self, w):
        return ({t: ({k: v for k, v in w.countries[t].flags.items() if k.startswith(self.FOREIGN)},
                     {k: v for k, v in w.countries[t].variables.items() if k.startswith(self.FOREIGN)},
                     {i for i in w.countries[t].ideas if i.startswith(self.FOREIGN)}) for t in ("ERU", "OSE", "FCU")},
                {g for g in w.globals if g.startswith(self.FOREIGN)})

    def test_lighthouse_calendar_needs_the_isaf_history_and_late_saves_never_replay(self):
        w, e, o = self.lhw()
        self.ltick(w, date(2019, 1, 31))
        self.assertNotIn("ac_lhw_calendar_started", w.globals)
        self.ltick(w, date(2019, 2, 1))
        self.assertIn("ac_lhw_calendar_started", w.globals)
        self.assertEqual([], self.lnews(w))
        self.ltick(w, date(2019, 5, 14))
        self.assertNotIn(("ERU", "ac_lhw.5", w.today + 1), w.events)
        self.ltick(w, date(2019, 5, 15))
        self.assertIn(("ERU", "ac_lhw.5", w.today + 1), w.events)
        self.assertEqual(set(), w.wars)
        for first in (date(2019, 5, 15), date(2019, 7, 1), date(2020, 3, 1)):
            late, _, _ = self.lhw(first)
            self.ltick(late, first)
            self.assertTrue({"ac_lhw_closed", "ac_lhw_late_start_skipped"} <= late.globals, first)
            self.ltick(late, date(2020, 6, 1))
            self.assertEqual([], self.lnews(late))
            self.assertEqual(set(), late.wars)
        for history in ("ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_stalemate", "ac_ucw_war_averted", None):
            with self.subTest(history=history):
                other, _, _ = self.lhw(history=history)
                self.lanchor(other)
                self.assertTrue({"ac_lhw_closed", "ac_lhw_route_unreachable"} <= other.globals)
                self.assertNotIn("ac_lhw_calendar_started", other.globals)
                self.ltick(other, date(2019, 12, 2))
                self.assertEqual([], self.lnews(other))
                self.assertEqual(set(), other.wars)
                self.assertTrue(self.lstatus(other).startswith("Closed: the Continental War"))
        gone, _, _ = self.lhw()
        for state in gone.states.values():
            if state.owner == "OSE":
                state.owner = state.controller = "BLK"
        self.ltick(gone, date(2019, 2, 1))
        self.assertTrue({"ac_lhw_closed", "ac_lhw_principal_missing"} <= gone.globals)

    def test_lighthouse_declaration_window_withholding_and_refusals(self):
        w, e, o = self.lhw()
        self.lanchor(w)
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_lhw.5"] if k == "option"}
        self.assertEqual("100", fields(fields(options["ac_lhw.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(options["ac_lhw.5.b"])["ai_chance"])["factor"])
        self.assertTrue({"ac_lhw_declaration_asked", "ac_lhw_declaration_pending", "ac_lhw_declaration_window"} <= set(e.flags))
        with self.assertRaises(AssertionError):
            w.option("ac_lhw.5", "b", "ERU")
        w.run("ac_lhw_withhold", "ERU")
        self.assertNotIn("ac_lhw_declaration_withheld", w.globals)
        self.ltick(w, date(2019, 5, 22))
        self.assertNotIn("ac_lhw_started", w.globals)
        self.ltick(w, date(2019, 5, 30))
        self.assertIn("ac_lhw_started", w.globals)
        self.assertEqual({frozenset(("ERU", "OSE"))}, w.wars)
        self.assertTrue({"ac_lhw_eru_war_footing", "ac_lhw_eru_elevator_held"} <= e.ideas)
        self.assertTrue({"ac_lhw_ose_war_footing", "ac_lhw_ose_ports_struck"} <= o.ideas)
        # The same weekly pulse that declared also delivers the stages whose dates have passed.
        self.assertEqual(["ac_lhw.1", "ac_lhw.20", "ac_lhw.21"], self.lnews(w))
        self.assertNotIn("ac_lhw_declaration_pending", e.flags)
        self.assertTrue(self.lstatus(w).startswith("Running on the official course"))
        # The withheld declaration is earned by the oversight file and the obligations kept as policy.
        kept, e2, o2 = self.lhw()
        e2.flags.update({"ERU_fe_oversight_settlement_done": None, "ERU_lw_sovereignty_policy_a_done": None})
        self.lanchor(kept)
        kept.option("ac_lhw.5", "b", "ERU")
        self.assertIn("ac_lhw_declaration_withheld", kept.globals)
        self.assertIn("ac_lhw_eru_restraint_kept", e2.ideas)
        self.assertEqual(set(), kept.wars)
        for day in (date(2019, 5, 30), date(2019, 8, 19), date(2019, 12, 2), date(2020, 3, 1)):
            self.ltick(kept, day)
        # The sovereignty policy flag also opens that branch's narrative scene (.60); the owner's own news is .2 alone.
        self.assertEqual(["ac_lhw.2"], [n for n in self.lnews(kept) if int(n.split(".")[1]) < 50])
        self.assertFalse({"ac_lhw_started", "ac_lhw_closed"} & kept.globals)
        self.assertTrue(self.lstatus(kept).startswith("Withheld"))
        for fault in ("eru_capitulated", "eru_subject", "ose_capitulated", "ose_subject"):
            with self.subTest(fault=fault):
                u, eu, ou = self.lhw()
                setattr(eu if fault.startswith("eru") else ou, "capitulated" if fault.endswith("capitulated") else "subject", True)
                self.lanchor(u)
                self.assertTrue({"ac_lhw_closed", "ac_lhw_principal_unable"} <= u.globals)
                self.assertNotIn(("ERU", "ac_lhw.5", u.today + 1), u.events)
                self.assertEqual(set(), u.wars)
        refused, er, orr = self.lhw()
        refused.refuse_war = True
        self.lanchor(refused)
        refused.option("ac_lhw.5", "a", "ERU")
        self.assertTrue({"ac_lhw_closed", "ac_lhw_declaration_refused"} <= refused.globals)
        self.assertFalse({"ac_lhw_started", "ac_lhw_pre_existing_war"} & refused.globals)
        self.assertFalse({"ac_lhw_eru_war_footing", "ac_lhw_eru_elevator_held"} & er.ideas)
        self.assertNotIn("ac_lhw_ose_war_footing", orr.ideas)
        self.ltick(refused, date(2019, 5, 30))
        self.assertEqual([], self.lnews(refused))

    def test_lighthouse_course_fires_each_stage_once_and_ends_at_expo_city(self):
        w, e, o = self.lhw()
        w.globals.add("ac_ucw_stonehenge_operational")
        w.countries["FCU"].flags["ac_fe_response_window"] = None
        before = self.foreign(w)
        self.ldeclare(w)
        self.ltick(w, date(2019, 5, 17))
        self.assertIn("ac_lhw_stage_eastern_wind", w.globals)
        self.assertIn("ac_lhw_ose_eastern_wind", o.ideas)
        self.ltick(w, date(2019, 5, 30))
        self.assertIn("ac_lhw_ose_kestrel_ii_lost", o.ideas)
        self.ltick(w, date(2019, 6, 6))
        self.assertIn("ac_lhw_stage_harling", w.globals)
        self.ltick(w, date(2019, 8, 19))
        self.assertTrue({"ac_lhw_stage_stonehenge", "ac_lhw_stonehenge_battery_reactivated"} <= w.globals)
        self.assertIn("ac_lhw_ose_stonehenge_battery", o.ideas)
        self.assertNotIn("ac_lhw_liberty_lost", w.globals)
        # Farbanti waits for an observed Osean foothold on an Erusean core; an Erusean-owned non-core state is not one.
        self.ltick(w, date(2019, 9, 19))
        self.assertNotIn("ac_lhw_stage_farbanti", w.globals)
        borrowed = next(i for i, s in w.states.items() if s.owner == "SNS")
        w.states[borrowed].owner, w.states[borrowed].controller = "ERU", "OSE"
        self.assertNotIn("ERU", w.states[borrowed].cores)
        self.ltick(w, date(2019, 9, 19))
        self.assertNotIn("ac_lhw_stage_farbanti", w.globals)
        w.states[borrowed].owner = w.states[borrowed].controller = "SNS"
        self.assertIn("ERU", w.states[240].cores)
        w.states[240].controller = "OSE"
        self.ltick(w, date(2019, 9, 19))
        self.assertTrue({"ac_lhw_stage_farbanti", "ac_lhw_usea_blackout"} <= w.globals)
        self.assertIn("ac_lhw_eru_capital_attacked", e.ideas)
        dark = {t for t, c in w.countries.items() if "ac_lhw_usea_blackout" in c.ideas}
        self.assertEqual({"ERU", "FCU", "SNS", "AMB", "UGE", "DEL", "NPT"}, dark)
        self.ltick(w, date(2019, 10, 1))
        self.assertIn("ac_lhw_eru_internal_conflict", e.ideas)
        self.ltick(w, date(2019, 10, 10))
        self.ltick(w, date(2019, 10, 31))
        self.assertTrue({"ac_lhw_stage_elevator_clash", "ac_lhw_arsenal_birds_lost"} <= w.globals)
        self.ltick(w, date(2019, 11, 30))
        self.assertNotIn(("ERU", "ac_lhw.6"), [(t, n) for t, n, _ in w.events])
        self.ltick(w, date(2019, 12, 1))
        self.assertIn(("ERU", "ac_lhw.6", w.today + 1), w.events)
        self.assertTrue({"ac_lhw_ceasefire_asked", "ac_lhw_ceasefire_pending", "ac_lhw_ceasefire_window"} <= set(e.flags))
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_lhw.6"] if k == "option"}
        self.assertEqual(("100", "0"), tuple(fields(fields(options[f"ac_lhw.6.{c}"])["ai_chance"])["factor"] for c in "ab"))
        w.option("ac_lhw.6", "a", "ERU")
        self.assertEqual(set(), w.wars)
        self.assertTrue({"ac_lhw_ceasefire_signed", "ac_lhw_ended", "ac_lhw_outcome_ceasefire", "ac_lhw_historical_course"} <= w.globals)
        self.assertIn(("ERU", "ac_lhw.7", w.today + 1), w.events)
        self.assertFalse({i for i in e.ideas | o.ideas if i in lighthouse.WAR_IDEAS})
        self.assertNotIn("ac_lhw_ceasefire_pending", e.flags)
        self.ltick(w, date(2019, 12, 8))
        self.assertEqual(["ac_lhw.1", "ac_lhw.20", "ac_lhw.21", "ac_lhw.22", "ac_lhw.24", "ac_lhw.25", "ac_lhw.26", "ac_lhw.27", "ac_lhw.28", "ac_lhw.7"], self.lnews(w))
        self.assertEqual(before, self.foreign(w))
        self.assertTrue(self.lstatus(w).startswith("Ended: the ceasefire was signed after the official course"))
        # Without Stonehenge the reactivation never fires; the fourteen-day ceasefire window signs on its own.
        plain, ep, op = self.lhw()
        self.ldeclare(plain)
        for day in (date(2019, 8, 19), date(2019, 9, 19), date(2019, 12, 1), date(2019, 12, 8)):
            self.ltick(plain, day)
        self.assertNotIn("ac_lhw_stage_stonehenge", plain.globals)
        self.assertNotIn("ac_lhw_ended", plain.globals)
        self.ltick(plain, date(2019, 12, 16))
        self.assertTrue({"ac_lhw_ceasefire_signed", "ac_lhw_outcome_ceasefire", "ac_lhw_historical_course"} <= plain.globals)
        self.assertEqual(set(), plain.wars)

    def test_lighthouse_arsenal_birds_follow_the_osean_project(self):
        w, e, o = self.lhw()
        self.ldeclare(w)
        self.assertNotIn("ac_lhw_birds_over_elevator", w.globals)
        self.assertNotIn("ac_lhw.29", self.lnews(w))
        self.assertEqual("In this campaign no Arsenal Bird project was completed. The Chronicle's Liberty is recorded as the source names it; no airframe is represented.",
                         self.defined_text(w, "lighthouse", "ac_lhw_liberty_text", "ERU"))
        built, eb, ob = self.lhw()
        built.run("ac_sp_arsenal_birds_complete_effect", "OSE")
        self.assertIn("ac_sp_arsenal_birds_complete", built.globals)
        self.assertIn("ac_sp_arsenal_birds_elevator_screen", ob.ideas)
        built.globals.add("ac_ucw_stonehenge_operational")
        self.ldeclare(built)
        self.assertIn("ac_lhw_birds_over_elevator", built.globals)
        self.assertNotIn("ac_sp_arsenal_birds_elevator_screen", ob.ideas)
        self.assertIn("ac_lhw_eru_arsenal_birds_two", eb.ideas)
        self.assertIn("ac_lhw.29", self.lnews(built))
        self.ltick(built, date(2019, 8, 19))
        self.assertIn("ac_lhw_liberty_lost", built.globals)
        self.assertNotIn("ac_lhw_eru_arsenal_birds_two", eb.ideas)
        self.assertIn("ac_lhw_eru_arsenal_bird_one", eb.ideas)
        self.assertTrue(self.defined_text(built, "lighthouse", "ac_lhw_liberty_text", "ERU").startswith("In this campaign the Arsenal Birds were completed"))
        self.ltick(built, date(2019, 10, 31))
        self.assertIn("ac_lhw_arsenal_birds_lost", built.globals)
        self.assertFalse({"ac_lhw_eru_arsenal_birds_two", "ac_lhw_eru_arsenal_bird_one"} & eb.ideas)
        # The project never completes after the sourced loss, and the owner never writes the completion flag itself.
        again, ea, oa = self.lhw()
        again.globals.add("ac_lhw_arsenal_birds_lost")
        again.run("ac_sp_arsenal_birds_complete_effect", "OSE")
        self.assertNotIn("ac_sp_arsenal_birds_complete", again.globals)
        self.assertNotIn("ac_sp_arsenal_birds_elevator_screen", oa.ideas)
        again.run("ac_sp_alicorn_complete_effect", "ERU")
        self.assertIn("ac_sp_alicorn_complete", again.globals)
        self.assertIn("ac_sp_alicorn_cruiser", ea.ideas)
        snapshot = copy.deepcopy(ea)
        again.run("ac_sp_alicorn_complete_effect", "ERU")
        self.assertEqual(snapshot, ea)
        # Without Stonehenge the Liberty is not lost at the August anchor and both birds fall at the clash.
        two, e2, o2 = self.lhw()
        two.run("ac_sp_arsenal_birds_complete_effect", "OSE")
        self.ldeclare(two)
        self.ltick(two, date(2019, 8, 19))
        self.assertNotIn("ac_lhw_liberty_lost", two.globals)
        self.assertIn("ac_lhw_eru_arsenal_birds_two", e2.ideas)
        self.ltick(two, date(2019, 10, 31))
        self.assertFalse({"ac_lhw_eru_arsenal_birds_two", "ac_lhw_eru_arsenal_bird_one"} & e2.ideas)

    def test_lighthouse_ceasefire_alternatives_are_earned_or_observed(self):
        refused, e, o = self.lhw()
        self.ldeclare(refused)
        refused.refuse_peace = True
        self.ltick(refused, date(2019, 12, 1))
        refused.option("ac_lhw.6", "a", "ERU")
        self.assertEqual({frozenset(("ERU", "OSE"))}, refused.wars)
        self.assertTrue({"ac_lhw_ceasefire_not_made", "ac_lhw_tainted"} <= refused.globals)
        self.assertFalse({"ac_lhw_ceasefire_signed", "ac_lhw_ended"} & refused.globals)
        self.assertTrue(self.lstatus(refused).startswith("Running under external observation: the ceasefire was signed but"))
        self.ltick(refused, date(2019, 12, 8))
        self.assertEqual(1, [n for _, n, _ in refused.events].count("ac_lhw.6"))
        refused.wars.clear()
        self.ltick(refused, date(2019, 12, 15))
        self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_cessation"} <= refused.globals)
        self.assertNotIn("ac_lhw_outcome_ceasefire", refused.globals)
        self.assertIn("ac_lhw.12", self.lnews(refused))
        fights, e2, o2 = self.lhw()
        self.ldeclare(fights)
        self.ltick(fights, date(2019, 12, 1))
        fights.option("ac_lhw.6", "b", "ERU")
        self.assertIn("ac_lhw_ceasefire_refused", fights.globals)
        self.assertIn("ac_lhw_eru_fought_on", e2.ideas)
        self.assertIn("ac_lhw.13", self.lnews(fights))
        self.assertTrue(self.lstatus(fights).startswith("Running past the Expo City date"))
        for day in (date(2019, 12, 8), date(2020, 2, 1)):
            self.ltick(fights, day)
        self.assertEqual(1, [n for _, n, _ in fights.events].count("ac_lhw.6"))
        self.assertNotIn("ac_lhw_ended", fights.globals)
        fights.wars.clear()
        self.ltick(fights, date(2020, 2, 8))
        self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_cessation"} <= fights.globals)
        self.assertNotIn("ac_lhw_tainted", fights.globals)
        self.assertIn("ac_lhw.11", self.lnews(fights))
        self.assertTrue(self.lstatus(fights).startswith("Ended: the fighting stopped without a ceasefire"))
        # The early ceasefire is a decision earned by the elevator kept running as policy.
        rows = {k: v for category in parse(text("common/decisions/ac_lighthouse.txt")) for k, _, v in category[2]}
        early, e3, o3 = self.lhw()
        self.ldeclare(early)
        self.ltick(early, date(2019, 8, 19))
        decision = rows["ERU_lw_early_ceasefire"]
        self.assertFalse(early.trigger(fields(decision)["available"], e3))
        early.run("ac_lhw_early_ceasefire", "ERU")
        self.assertNotIn("ac_lhw_ended", early.globals)
        e3.flags["ERU_lw_lighthouse_policy_b_done"] = None
        self.assertTrue(early.trigger(fields(decision)["available"], e3))
        self.assertEqual("50", fields(decision)["cost"])
        pp = e3.pp
        early.execute(fields(decision)["complete_effect"], e3)
        self.assertEqual(pp, e3.pp)
        self.assertEqual(set(), early.wars)
        self.assertTrue({"ac_lhw_ceasefire_early", "ac_lhw_ceasefire_signed", "ac_lhw_ended", "ac_lhw_outcome_ceasefire"} <= early.globals)
        self.assertNotIn("ac_lhw_historical_course", early.globals)
        self.assertIn(("ERU", "ac_lhw.8", early.today + 1), early.events)
        self.assertTrue(self.lstatus(early).startswith("Ended: an early ceasefire"))
        self.ltick(early, date(2019, 12, 1))
        self.assertNotIn("ac_lhw.6", [n for _, n, _ in early.events])
        self.assertFalse(early.trigger(fields(decision)["available"], e3))

    def test_lighthouse_external_observation_and_falls(self):
        w, e, o = self.lhw()
        w.wars.add(frozenset(("OSE", "BLK")))
        self.ldeclare(w)
        self.assertTrue({"ac_lhw_tainted", "ac_lhw_pre_existing_war"} <= w.globals)
        self.ltick(w, date(2019, 5, 17))
        self.assertNotIn("ac_lhw_stage_eastern_wind", w.globals)
        w.wars.discard(frozenset(("ERU", "OSE")))
        self.ltick(w, date(2019, 5, 24))
        self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_cessation"} <= w.globals)
        self.assertEqual(["ac_lhw.1", "ac_lhw.4", "ac_lhw.12"], self.lnews(w))
        later, e2, o2 = self.lhw()
        self.ldeclare(later)
        self.ltick(later, date(2019, 5, 17))
        later.wars.add(frozenset(("ERU", "BLK")))
        self.ltick(later, date(2019, 5, 30))
        self.assertIn("ac_lhw_tainted", later.globals)
        self.assertNotIn("ac_lhw_stage_kestrel_ii", later.globals)
        self.assertIn("ac_lhw.4", self.lnews(later))
        self.assertTrue(self.lstatus(later).startswith("Running under external observation: other fighting"))
        vassal, e3, o3 = self.lhw()
        self.ldeclare(vassal)
        vassal.countries["BLK"].overlord = "OSE"
        vassal.wars.add(frozenset(("BLK", "ERU")))
        self.ltick(vassal, date(2019, 5, 17))
        self.assertNotIn("ac_lhw_tainted", vassal.globals)
        self.assertIn("ac_lhw_stage_eastern_wind", vassal.globals)
        existing, e4, o4 = self.lhw()
        existing.wars.add(frozenset(("OSE", "ERU")))
        self.lanchor(existing)
        self.assertTrue({"ac_lhw_started", "ac_lhw_existing_war_observed"} <= existing.globals)
        self.assertNotIn("ac_lhw_tainted", existing.globals)
        self.assertNotIn("ac_lhw_eru_war_footing", e4.ideas)
        self.assertIn("ac_lhw.3", self.lnews(existing))
        existing.wave_action("lighthouse", "on_startup")
        self.assertFalse({"ac_lhw_eru_war_footing", "ac_lhw_ose_war_footing"} & (e4.ideas | o4.ideas))
        self.ltick(existing, date(2019, 5, 17))
        self.assertNotIn("ac_lhw_stage_eastern_wind", existing.globals)
        self.assertTrue(self.lstatus(existing).startswith("Running under external observation: Osea and Erusea were already"))
        # Falls: only a fall to the other principal in their own war is that principal's victory.
        victory, e5, o5 = self.lhw()
        self.ldeclare(victory)
        e5.capitulated = True
        victory.wave_action("lighthouse", "on_capitulation_immediate", "ERU", "OSE")
        self.assertTrue({"ac_lhw_eru_fallen", "ac_lhw_ended", "ac_lhw_outcome_osean_victory"} <= victory.globals)
        self.assertIn(("OSE", "ac_lhw.9", victory.today + 1), victory.events)
        self.assertFalse({i for i in e5.ideas | o5.ideas if i in lighthouse.WAR_IDEAS})
        self.assertTrue(self.lstatus(victory).startswith("Ended: Erusea capitulated"))
        annexed, e6, o6 = self.lhw()
        self.ldeclare(annexed)
        annexed.wave_action("lighthouse", "on_annex", "ERU", "OSE")
        self.assertTrue({"ac_lhw_ose_fallen", "ac_lhw_outcome_erusean_victory"} <= annexed.globals)
        self.assertIn(("ERU", "ac_lhw.10", annexed.today + 1), annexed.events)
        for hook, fallen, winner, victory_flag in (("on_annex", "BLK", "ERU", "ac_lhw_outcome_osean_victory"),
                                                   ("on_capitulation_immediate", "OSE", "BLK", "ac_lhw_outcome_erusean_victory"),
                                                   ("on_subject_annexed", "ERU", "BLK", "ac_lhw_outcome_osean_victory")):
            with self.subTest(hook=hook, fallen=fallen):
                third, e7, o7 = self.lhw()
                self.ldeclare(third)
                if hook == "on_annex":
                    third.wave_action("lighthouse", hook, fallen, winner)   # ROOT annexer BLK, FROM annexed ERU
                    lost = winner
                else:
                    (o7 if fallen == "OSE" else e7).capitulated = hook == "on_capitulation_immediate"
                    third.wave_action("lighthouse", hook, fallen, winner)
                    lost = fallen
                self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_cessation", "ac_lhw_external_fall", f"ac_lhw_{lost.lower()}_fallen"} <= third.globals)
                self.assertNotIn(victory_flag, third.globals)
                self.assertIn("ac_lhw.12", [n for _, n, _ in third.events])
        overlord, e8, o8 = self.lhw()
        self.ldeclare(overlord)
        overlord.wave_action("lighthouse", "on_subject_annexed", "ERU", "OSE")
        self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_osean_victory"} <= overlord.globals)
        split, e9, o9 = self.lhw()
        self.ldeclare(split)
        breakaway = copy.deepcopy(e9)
        breakaway.tag, breakaway.capitulated = "D01", True
        split.countries["D01"] = breakaway
        split.wave_action("lighthouse", "on_capitulation_immediate", "D01", "OSE")
        self.assertFalse({"ac_lhw_ended", "ac_lhw_eru_fallen"} & split.globals)
        alone, e10, o10 = self.lhw()
        self.ldeclare(alone)
        for state in alone.states.values():
            if state.owner == "ERU":
                state.owner = state.controller = "OSE"
        self.ltick(alone, date(2019, 5, 24), "OSE")
        self.assertTrue({"ac_lhw_ended", "ac_lhw_outcome_osean_victory"} <= alone.globals)

    def test_lighthouse_osean_decisions_shilage_text_and_branch_gates(self):
        rows = {k: v for category in parse(text("common/decisions/ac_lighthouse.txt")) for k, _, v in category[2]}
        w, e, o = self.lhw()
        strike, ports, record = rows["OSE_lw_strike_group"], rows["OSE_lw_repair_ports"], rows["OSE_lw_war_record"]
        self.assertEqual(("50", "25", "25"), tuple(fields(r)["cost"] for r in (strike, ports, record)))
        self.assertFalse(w.trigger(fields(strike)["available"], o))
        self.ldeclare(w)
        self.assertTrue(w.trigger(fields(ports)["available"], o))
        pp = o.pp
        w.execute(fields(ports)["complete_effect"], o)
        self.assertEqual(pp, o.pp)
        self.assertNotIn("ac_lhw_ose_ports_struck", o.ideas)
        self.assertFalse(w.trigger(fields(ports)["available"], o))
        self.ltick(w, date(2019, 8, 9))
        self.assertFalse(w.trigger(fields(strike)["available"], o))
        self.ltick(w, date(2019, 8, 10))
        self.assertTrue(w.trigger(fields(strike)["available"], o))
        w.execute(fields(strike)["complete_effect"], o)
        self.assertEqual(pp, o.pp)
        self.assertTrue({"ac_lhw_ose_strike_group"} <= o.ideas)
        self.assertIn("ac_lhw_lrssg_formed", w.globals)
        self.assertIn("ac_lhw.23", self.lnews(w))
        self.assertFalse(w.trigger(fields(strike)["available"], o))
        snapshot = copy.deepcopy(o)
        w.execute(fields(strike)["complete_effect"], o)
        self.assertEqual(snapshot, o)
        self.assertFalse(w.trigger(fields(record)["available"], o))
        w.wars.clear()
        self.ltick(w, date(2019, 8, 17))
        self.assertNotIn("ac_lhw_ose_strike_group", o.ideas)
        self.assertTrue(w.trigger(fields(record)["available"], o))
        w.execute(fields(record)["complete_effect"], o)
        self.assertIn("ac_lhw_ose_war_record", o.ideas)
        # The engine charges the decisions' `cost`; the owner's effects never charge political power again.
        owned = {k: v for k, _, v in parse(text("common/scripted_effects/ac_lighthouse.txt"))
                 if k.startswith("ac_lhw_") and k not in ("ac_lhw_pay_programme",)}
        self.assertFalse(any("add_political_power" in str(v) for v in owned.values()))
        # Shilage is read for text only: nothing is released, annexed, cored or moved.
        for flags, expected in ((set(), "Whether Shilage exists"), ({"ac_release_SHI_was_absent"}, "Shilage is not a country"),
                                ({"ac_release_SHI_annexed"}, "Shilage was released and later annexed")):
            with self.subTest(flags=flags):
                s, es, os_ = self.lhw()
                s.globals |= flags
                self.assertTrue(self.defined_text(s, "lighthouse", "ac_lhw_shilage_text", "ERU").startswith(expected))
        exists, ex, ox = self.lhw()
        state = next(i for i, st in exists.states.items() if st.owner == "SNS")
        exists.states[state].owner = exists.states[state].controller = "SHI"
        self.assertTrue(self.defined_text(exists, "lighthouse", "ac_lhw_shilage_text", "ERU").startswith("Shilage exists as a country"))
        # Branch gates follow the actual history and the owner's state.
        isaf, ei, oi = self.lhw(date(2017, 6, 1))
        isaf.run("ac_lhw_initialize", "ERU")
        isaf.run("ac_lhw_initialize", "FCU")
        ei.completed.add("ERU_ucw_exp_settlement_assessment")
        opened = {b.key for b in LH.branches if b.tag == "ERU" and isaf.available(focus_id(LH, b, 0), "ERU")}
        self.assertEqual({"sovereignty", "elevator", "alicorn", "drones"}, opened)
        other, eo, oo = self.lhw(date(2017, 6, 1), "ac_ucw_outcome_stalemate")
        other.run("ac_lhw_initialize", "ERU")
        eo.completed.add("ERU_ucw_exp_settlement_assessment")
        self.assertEqual({"standing", "elevator", "alicorn", "drones"}, {b.key for b in LH.branches if b.tag == "ERU" and other.available(focus_id(LH, b, 0), "ERU")})
        ei.completed |= {"ERU_lw_elevator_settlement", "ERU_lw_sovereignty_settlement"}
        self.assertFalse(any(isaf.available(focus_id(LH, b, 0), "ERU") for b in LH.branches if b.key in ("lighthouse", "capital", "ceasefire", "secession")))
        isaf.globals.add("ac_lhw_started")
        self.assertTrue(all(isaf.available(focus_id(LH, b, 0), "ERU") for b in LH.branches if b.key in ("lighthouse", "capital")))
        self.assertFalse(any(isaf.available(focus_id(LH, b, 0), "ERU") for b in LH.branches if b.key in ("ceasefire", "secession")))
        isaf.globals |= {"ac_lhw_ended", "ac_lhw_stage_secession"}
        self.assertTrue(all(isaf.available(focus_id(LH, b, 0), "ERU") for b in LH.branches if b.key in ("ceasefire", "secession")))
        f = isaf.countries["FCU"]
        f.completed.add("FCU_ucw_exp_settlement_assessment")
        isaf.globals -= {"ac_lhw_started", "ac_lhw_ended", "ac_lhw_stage_secession"}
        self.assertEqual(set(), {b.key for b in LH.branches if b.tag == "FCU" and isaf.available(focus_id(LH, b, 0), "FCU")})
        isaf.today = date(2019, 1, 2).toordinal()
        self.assertEqual({"airspace"}, {b.key for b in LH.branches if b.tag == "FCU" and isaf.available(focus_id(LH, b, 0), "FCU")})
        isaf.globals |= {"ac_lhw_started", "ac_lhw_stage_farbanti", "ac_lhw_ended"}
        self.assertEqual({"airspace", "corridor", "blackout", "settlement"}, {b.key for b in LH.branches if b.tag == "FCU" and isaf.available(focus_id(LH, b, 0), "FCU")})
        # The capital's second service and the federation's first clear the blackout idea when they complete.
        numbers = [service_id(LH, b, n) for b in LH.branches for n in range(2)]
        for tag, ident, clears in (("ERU", "ERU_lw_capital_service_1", False), ("ERU", "ERU_lw_capital_service_2", True),
                                   ("FCU", "FCU_lw_blackout_service_2", False), ("FCU", "FCU_lw_blackout_service_1", True)):
            with self.subTest(service=ident):
                c = isaf.countries[tag]
                c.ideas.add("ac_lhw_usea_blackout")
                c.flags.update({"ac_lhw_service_active": None, ident + "_active": None})
                c.flags.pop("ac_lhw_service_window", None)
                c.variables["ac_lhw_current_service"] = D(numbers.index(ident) + 1)
                isaf.run(ident + "_finish", tag)
                self.assertIn(ident + "_completed", c.flags)
                self.assertEqual(not clears, "ac_lhw_usea_blackout" in c.ideas)
                c.ideas.discard("ac_lhw_usea_blackout")


    def owner(self, today=date(2006, 9, 26)):
        w = self.fresh()
        w.globals.add("ac_ucw_outcome_isaf_victory")
        w.today = today.toordinal()
        return w, w.countries["ERU"]

    def test_insurrection_starts_on_the_anchor_only_after_an_isaf_victory(self):
        w, c = self.owner(date(2006, 9, 25))
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w.globals)
        w.today = date(2006, 9, 26).toordinal()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_insurrection_started", w.globals)
        self.assertEqual(D(55) + D("0.4"), c.variables["ac_fe_pressure"])
        self.assertIn("ac_fe_pressure_active", c.ideas)
        self.assertIn(("ERU", "ac_fe.1", w.today + 1), w.events)
        self.assertIn(("FCU", "ac_fe.5", w.today + 1), w.events)
        self.assertIn("ac_fe_response_window", c.flags)
        self.assertNotIn("ac_fe_prolonged", w.globals)
        w2 = self.fresh()
        w2.today = date(2006, 10, 1).toordinal()
        w2.globals.add("ac_ucw_outcome_stalemate")
        w2.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w2.globals)
        # A capitulated Erusea that still owns land cannot start the insurrection.
        w3, c3 = self.owner()
        c3.capitulated = True
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w3.globals)
        self.assertNotIn("ac_fe_pressure", c3.variables)
        self.assertEqual([], [e for _, e, _ in w3.events if e.startswith("ac_fe.")])

    def test_historical_route_records_the_defeat_by_mobius_1(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        option = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_fe.5"] if k == "option"}
        self.assertEqual("100", fields(fields(option["ac_fe.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(option["ac_fe.5.b"])["ai_chance"])["factor"])
        w.events.clear()
        w.option("ac_fe.5", "a", "FCU")
        self.assertIn("ac_fe_insurrection_defeated", w.globals)
        self.assertNotIn("ac_fe_prolonged", w.globals)
        self.assertEqual(["ac_fe.6"], [e for _, e, _ in w.events])
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))
        frozen = c.variables["ac_fe_pressure"]
        for _ in range(8):
            w.advance(7)
            w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.run("ac_fe_relief_major", "ERU")
        self.assertEqual(frozen, c.variables["ac_fe_pressure"])
        self.assertEqual(["ac_fe.6"], [e for _, e, _ in w.events])
        self.assertNotIn("ac_fe_prolonged", w.globals)
        # The aftermath branches stay open after the historical defeat.
        c.completed.add("ERU_ucw_exp_settlement_assessment")
        self.assertTrue(w.available("ERU_fe_insurrection_register", "ERU"))

    def test_central_usea_must_still_be_able_to_respond_when_it_answers(self):
        for fault in ("capitulated", "at_war_with_erusea"):
            with self.subTest(fault=fault):
                w, c = self.owner()
                w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
                self.assertIn(("FCU", "ac_fe.5", w.today + 1), w.events)
                if fault == "capitulated":
                    w.countries["FCU"].capitulated = True
                else:
                    w.wars.add(frozenset(("FCU", "ERU")))
                with self.assertRaises(AssertionError):
                    w.option("ac_fe.5", "a", "FCU")
                before = (copy.deepcopy(c.ideas), copy.deepcopy(c.variables), set(w.globals))
                w.run("ac_fe_defeat", "FCU")
                self.assertNotIn("ac_fe_insurrection_defeated", w.globals)
                self.assertEqual(before, (c.ideas, c.variables, set(w.globals)))
                w.advance(31)
                w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
                self.assertIn("ac_fe_prolonged", w.globals)

    def test_prolonged_route_is_provisional_and_needs_no_central_usean_answer(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.option("ac_fe.5", "b", "FCU")
        self.assertIn("ac_fe_prolonged", w.globals)
        before = c.variables["ac_fe_pressure"]
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(before + D("0.4"), c.variables["ac_fe_pressure"])
        w.run("ac_fe_defeat", "FCU")
        self.assertNotIn("ac_fe_insurrection_defeated", w.globals)
        # Central Usea cannot answer: the prolonged route starts at once.
        w2, c2 = self.owner()
        for state in w2.states.values():
            if state.owner == "FCU":
                state.owner = state.controller = "ERU"
        w2.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_prolonged", w2.globals)
        self.assertNotIn("ac_fe.5", [e for _, e, _ in w2.events])
        # An unanswered response window falls back to the prolonged route.
        w3, c3 = self.owner()
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w3.advance(31)
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_prolonged", w3.globals)

    def test_late_first_observation_never_replays_the_outbreak(self):
        w, c = self.owner(date(2008, 3, 1))
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w.globals)
        self.assertIn("ac_fe_insurrection_closed", w.globals)
        self.assertIn("ac_fe_late_start_skipped", w.globals)
        self.assertNotIn("ac_fe_pressure", c.variables)

    def test_policies_and_services_contain_the_insurrection_state_based(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        start = c.variables["ac_fe_pressure"]
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(start + D("0.4"), c.variables["ac_fe_pressure"])
        c.ideas.add("ERU_fe_insurrection_policy_b_spirit")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(start + D("0.4") - D("0.5"), c.variables["ac_fe_pressure"])
        f = w.countries["FCU"]
        f.completed.add("FCU_fe_security_operations")
        ident = service_id(FE, next(b for b in FE.branches if b.tag == "FCU" and b.key == "security"), 1)
        w.run(ident + "_start", "FCU")
        w.advance(90)
        before = c.variables["ac_fe_pressure"]
        w.run(ident + "_finish", "FCU")
        self.assertEqual(before - 6, c.variables["ac_fe_pressure"])
        c.variables["ac_fe_pressure"] = D("5.3")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_insurrection_contained", w.globals)
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))
        frozen = c.variables["ac_fe_pressure"]
        w.run("ac_fe_relief_major", "ERU")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(frozen, c.variables["ac_fe_pressure"])

    def test_crisis_review_fires_once_per_year_and_options_have_bounded_effects(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        c.variables["ac_fe_pressure"] = D(90)
        c.stability = D("0.2")
        w.events.clear()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(["ac_fe.2"], [e for _, e, _ in w.events])
        self.assertIn("ac_fe_pressure_severe", c.ideas)
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(["ac_fe.2"], [e for _, e, _ in w.events])
        w.option("ac_fe.2", "a", "ERU")
        self.assertIn(("FCU", "ac_fe.4"), [(t, e) for t, e, _ in w.events])
        f = w.countries["FCU"]
        pp = f.pp
        before = c.variables["ac_fe_pressure"]
        w.option("ac_fe.4", "a", "FCU")
        self.assertEqual(pp - 40, f.pp)
        self.assertIn("ac_fe_partner_assistance", c.ideas)
        self.assertEqual(before - 6, c.variables["ac_fe_pressure"])

    def test_annexation_closes_the_owner_without_touching_other_state(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.wave_action("free_erusea", "on_annex", "FCU", "ERU")
        self.assertIn("ac_fe_insurrection_closed", w.globals)
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))

    def test_nordennavic_adoption_and_anean_callback_read_only(self):
        w = self.fresh()
        c = w.countries["NEC"]
        decision = fields(fields(parse(text("common/decisions/ac_nordennavic.txt")))["ac_nec_nec_services"])["NEC_nc_adopt_campaign"]
        w.execute(fields(decision)["complete_effect"], c)
        self.assertIn(nordennavic.TREE_ID, c.trees)
        custom = parse(text("common/custom_localization/ac_nordennavic.txt"))
        node = next(v for k, _, v in custom if k == "defined_text" and next(x for key, _, x in v if key == "name") == "NEC_nc_anean_record")
        def pick():
            for key, _, value in node:
                if key == "text" and w.trigger(fields(value).get("trigger", []), c):
                    return fields(value)["localization_key"]
        self.assertEqual("NEC_nc_anean_none", pick())
        w.globals.add("ac_anea_nec_participates")
        self.assertEqual("NEC_nc_anean_participates", pick())


if __name__ == "__main__":
    unittest.main(verbosity=2)
