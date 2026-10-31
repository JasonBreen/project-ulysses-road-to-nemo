"""Offline decision-control, artwork and effective-consumer regressions."""
from collections import Counter
import hashlib
import json
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/overhaul"))
from build_decisions_ui import CONTRACT, MOD, SCROLLBAR, build, get, parse, scalar, walk
from audit_consumers import Audit, EffectiveFiles


def named(tree, name):
    return next(node for _, node in walk(tree) if scalar(get(node, "name")) == name)


class DecisionUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text())
        cls.tree = parse((MOD / "interface/countrydecisionview.gui").read_text())
        cls.manifest = json.loads((CONTRACT.parent / "decisions_assets.json").read_text())

    def test_required_control_identities_and_keyboard_binding(self):
        # Compare each engine template, including repeated child names in their
        # original parent. A global set would miss a control moved to a sibling.
        for kind, _, node in self.contract["gui"][0][2]:
            name = scalar(get(node, "name"))
            replacement = named(self.tree, name)
            self.assertEqual(Counter((k.lower(), scalar(get(n, "name", ""))) for k, n in walk([[kind, "=", node]])),
                             Counter((k.lower(), scalar(get(n, "name", ""))) for k, n in walk([[kind, "=", replacement]])), name)
        self.assertEqual('"ESCAPE"', get(named(self.tree, "close_button"), "shortcut"))
        for name in ("decision_grid", "category_header", "decision_category_desc", "custom_icon_item", "event_header", "event_item",
                     "decision_item", "targeted_decision_item", "timed_decision_item", "on_map_decision_locator_item"):
            self.assertIsNotNone(named(self.tree, name))

    def test_scroll_dynamic_geometry_and_flags_are_preserved(self):
        main = named(self.tree, "countrydecisionview")
        self.assertEqual("100%%", get(get(main, "size"), "height"))
        grid = named(self.tree, "decision_grid_container")
        self.assertEqual('"' + SCROLLBAR + '"', get(grid, "verticalScrollbar"))
        self.assertEqual("yes", get(grid, "smooth_scrolling"))
        self.assertEqual("-10", get(get(grid, "size"), "height"))
        bar = named(self.tree, SCROLLBAR)
        for control in ("Background", "Slider", "Track", "Decrease", "Increase"):
            self.assertIsNotNone(named([["bar", "=", bar]], control))
        for template in ("decision_item", "timed_decision_item", "targeted_decision_item"):
            node = named(self.tree, template)
            self.assertIsNotNone(named([["entry", "=", node]], "target_flag"))

    def test_names_costs_timers_and_actions_have_separate_bounds(self):
        for template in ("decision_item", "timed_decision_item", "targeted_decision_item"):
            node = named(self.tree, template)
            controls = {scalar(get(n, "name")): n for _, n in walk([["item", "=", node]])}
            title = controls["name_text"]; cost = controls["cost_and_timer_text"]
            title_end = int(get(get(title, "position"), "x")) + int(get(title, "maxWidth"))
            cost_x = int(get(get(cost, "position"), "x"))
            cost_end = cost_x + int(get(cost, "maxWidth"))
            self.assertLess(int(get(get(title, "position"), "y")) + int(get(title, "maxHeight")),
                            int(get(get(cost, "position"), "y")))
            self.assertEqual("104", get(get(node, "size"), "height"))
            progress = controls["btn_progress_good"]
            self.assertLess(int(get(get(title, "position"), "y")) + int(get(title, "maxHeight")),
                            int(get(get(progress, "position"), "y")))
            if "timer_text" in controls:
                timer = controls["timer_text"]
                self.assertLess(cost_end, int(get(get(timer, "position"), "x")))
            if "track_decision_checkbox" in controls:
                self.assertLess(title_end, int(get(get(controls["track_decision_checkbox"], "position"), "x")))
        for _, node in walk(self.tree):
            for field in ("font", "buttonFont"):
                if get(node, field): self.assertIn(scalar(get(node, field)), ("ACBriefing16", "ACBriefing20"))

    def test_actual_localized_titles_and_dynamic_country_state_names_fit(self):
        spec = importlib.util.spec_from_file_location('decision_focus_metrics', ROOT / 'tools/Test-FocusScreenRepairs.py')
        metrics = importlib.util.module_from_spec(spec); spec.loader.exec_module(metrics)
        line_height, advances = metrics.font_metrics()
        loc = {}
        import re
        for path in sorted((MOD / 'localisation/english').rglob('*.yml')):
            loc.update(re.findall(r'^\s*([^\s:#]+):\d*\s+"((?:\\.|[^"\\])*)"', path.read_text(encoding='utf-8-sig'), re.M))
        ideology = get(parse((MOD / 'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig')), 'ideologies')
        groups = [key for key, _, _ in ideology]
        country_keys = {tag + suffix for path in (MOD / 'history/countries').glob('*.txt') for tag in [path.name[:3]]
                        for suffix in ['', '_DEF'] + ['_' + group + ending for group in groups for ending in ('', '_DEF')]}
        state_keys = {scalar(get(get(parse(path.read_text(encoding='utf-8-sig')), 'state'), 'name'))
                      for path in (MOD / 'history/states').glob('*.txt')}
        names = [loc[key] for key in country_keys | state_keys if key in loc
                 and '[' not in loc[key] and '$' not in loc[key] and '\\n' not in loc[key]]
        self.assertGreater(len(names), 500)
        title = named([['item', '=', named(self.tree, 'timed_decision_item')]], 'name_text')
        width, height = int(get(title, 'maxWidth')), int(get(title, 'maxHeight'))
        checked = set()
        for path in (MOD / 'common/decisions').glob('*.txt'):
            for _, _, group in parse(path.read_text(encoding='utf-8-sig')):
                if not isinstance(group, list): continue
                for ident, _, node in group:
                    if not isinstance(node, list) or ident not in loc: continue
                    # The shipped digits have unequal advances. Measure the
                    # original 1991 case and every year through the retained
                    # campaign ceiling rather than assuming 2020 is widest.
                    texts = [loc[ident].replace('[GetYear]',str(year)) for year in range(1991,2066)] if '[GetYear]' in loc[ident] else [loc[ident]]
                    variants = []
                    for text in texts:
                        text = text.replace('[FROM.GetMobilizationDivisionCount]', '9999')
                        variants.extend([re.sub(r'\[FROM\.(?:owner\.)?Get(?:NameDef|Name|NonIdeologyName)\]', name, text) for name in names] if '[FROM.' in text else [text])
                    for value in variants:
                        self.assertNotIn('[', value, ident)
                        lines = metrics.wrapped_lines(value, width, advances)
                        self.assertLessEqual(len(lines)*line_height, height, (ident, value, lines))
                        self.assertTrue(all(sum(advances.get(ord(c), 8) for c in line) <= width for line in lines), ident)
                    checked.add(ident)
        self.assertIn('OSE_award_research_grants_house_vote', checked)
        self.assertIn('OSE_award_research_grants_senate_vote', checked)
        self.assertGreaterEqual(len(checked), 250)

    def test_filled_and_empty_timer_textures_remain_visually_distinct(self):
        tree = parse((MOD / 'interface/countrydecisionview.gfx').read_text())
        count = 0
        for kind, node in walk(tree):
            if kind.lower() != 'progressbartype': continue
            filled, empty = [MOD / scalar(get(node, key)) for key in ('textureFile1', 'textureFile2')]
            with Image.open(filled) as a, Image.open(empty) as b:
                self.assertNotEqual(a.convert('RGBA').tobytes(), b.convert('RGBA').tobytes())
            count += 1
        self.assertEqual(2, count)

    def test_generated_files_are_reproducible(self):
        outputs, manifest = build(self.contract)
        self.assertEqual(manifest, self.manifest)
        for relative, data in outputs.items():
            self.assertEqual(data, (MOD / relative).read_bytes(), relative)

    def test_texture_dimensions_frames_hashes_and_flag_aperture(self):
        for row in self.manifest["assets"]:
            path = MOD / row["file"]
            self.assertEqual(row["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), row["file"])
            with Image.open(path) as image:
                self.assertEqual((row["width"], row["height"]), image.size)
                self.assertEqual(0, image.width % row["frames"], row["sprite"])
                self.assertEqual(row["alpha"], list(image.getchannel("A").getextrema()))
                if row["sprite"] == "GFX_ac_dec_flag_small" and "_0_" in row["file"]:
                    self.assertEqual(0, image.getpixel((image.width//2, image.height//2))[3])
                if "select_icon_strip" in row["sprite"]:
                    frames = {image.crop((f*row["frame_width"], 0, (f+1)*row["frame_width"], image.height)).tobytes()
                              for f in range(row["frames"])}
                    self.assertEqual(row["frames"], len(frames))


class EffectiveConsumers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.mod = self.root / "mod"; self.engine = self.root / "engine"
        self.mod.mkdir(); self.engine.mkdir()

    def put(self, base, relative, text):
        target = base / relative; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text)

    def sprite(self, base, name, path="gfx/panel.dds", filename="interface/panel.gfx"):
        self.put(base, filename, 'spriteTypes = { spriteType = { name = "' + name + '" texturefile = "' + path + '" } }')
        self.put(base, path, "test texture payload")

    def test_same_path_override_and_descriptor_isolation(self):
        self.sprite(self.engine, "GFX_old")
        self.sprite(self.mod, "GFX_new")
        self.put(self.mod, "descriptor.mod", 'replace_path="common/decisions"')
        self.put(self.engine, "common/decisions/earth.txt", "old = {}")
        self.put(self.mod, "common/decisions/usea.txt", "new = {}")
        audit = Audit(self.mod, self.engine)
        self.assertNotIn("GFX_old", audit.definitions["sprite"])
        self.assertEqual("mod_resolved", audit.resolve("sprite", "GFX_new")["status"])
        self.assertEqual(["common/decisions/usea.txt"], [r for r, _, _ in audit.vfs.files("common/decisions")])

    def test_engine_scrollbar_dependencies_cannot_hide_engine_imagery(self):
        self.sprite(self.mod, "GFX_panel")
        self.sprite(self.engine, "GFX_engine_thumb", "gfx/thumb.dds", "interface/thumb.gfx")
        self.put(self.mod, "interface/countrydecisionview.gui", 'guiTypes={containerWindowType={name="countrydecisionview" verticalScrollbar="engine_bar" iconType={name="bg" spriteType="GFX_panel"}}}')
        self.put(self.engine, "interface/core.gui", 'guiTypes={extendedScrollbarType={name="engine_bar" slider={name="Slider" quadTextureSprite="GFX_engine_thumb"}}}')
        screen = Audit(self.mod, self.engine).screen("countrydecisionview.gui")
        self.assertTrue(any("GFX_engine_thumb:engine_fallback" in f for f in screen["failures"]))

    def test_shader_alias_uses_original_path_after_source_relative_probe(self):
        self.put(self.engine, "gfx/fx/buttonstate.shader", "engine shader service")
        resource = EffectiveFiles(self.mod, self.engine).resource(
            "gfx/fx/buttonstate.lua", "interface/nationalfocusview.gfx")
        self.assertEqual("engine_service", resource["status"])
        self.assertEqual("gfx/fx/buttonstate.shader", resource["path"])
        self.assertEqual("gfx/fx/buttonstate.lua", resource["legacy_alias"])

    def test_runtime_decision_icons_are_in_the_screen_gate(self):
        self.sprite(self.mod, "GFX_panel")
        self.put(self.mod, "interface/countrydecisionview.gui", 'guiTypes={containerWindowType={name="countrydecisionview" iconType={name="bg" spriteType="GFX_panel"}}}')
        self.put(self.mod, "common/decisions/choices.txt", "category={choice={icon=unbound}}")
        screen = Audit(self.mod, self.engine).screen("countrydecisionview.gui", True)
        self.assertTrue(any("GFX_decision_unbound:missing_definition" in f for f in screen["failures"]))

    def test_every_repeated_conditional_icon_key_enters_the_gate(self):
        self.sprite(self.mod, 'GFX_panel')
        self.sprite(self.mod, 'GFX_decision_first')
        self.put(self.mod, 'interface/countrydecisionview.gui', 'guiTypes={containerWindowType={name="countrydecisionview" iconType={name="bg" spriteType="GFX_panel"}}}')
        self.put(self.mod, 'common/decisions/choices.txt', 'category={choice={icon={key=first trigger={check_variable={var=control value=0 compare=equals}}} icon={key=missing trigger={always=no}} icon={key=GFX_explicit trigger={always=yes}}}}')
        audit = Audit(self.mod, self.engine)
        icons = audit.decision_consumers()
        self.assertEqual({'GFX_decision_first', 'GFX_decision_missing', 'GFX_explicit', 'GFX_decision_unknown'}, {row['name'] for row in icons})
        failures = audit.screen('countrydecisionview.gui', True)['failures']
        self.assertTrue(any('GFX_decision_missing:missing_definition' in row for row in failures))
        self.assertTrue(any('GFX_explicit:missing_definition' in row for row in failures))

    def test_conditional_and_empty_icons_do_not_hide_runtime_defaults(self):
        self.sprite(self.mod,'GFX_decision_first')
        self.sprite(self.engine,'GFX_decision_unknown',path='gfx/engine_default.dds',filename='interface/default.gfx')
        self.put(self.mod,'common/decisions/choices.txt', 'category={conditional={icon={key=first trigger={always=no}}} empty={icon=""} no_icon={}}')
        audit=Audit(self.mod,self.engine);rows=audit.decision_consumers()
        defaults=[row for row in rows if row['name']=='GFX_decision_unknown']
        self.assertEqual({'conditional','empty','no_icon'},{row['owner'] for row in defaults})
        self.assertTrue(all(row['status']=='engine_fallback' for row in defaults))
        self.assertFalse(any(row['name'].endswith('_no') for row in rows))

    def test_cross_file_conflicts_fail_even_when_both_textures_are_local(self):
        self.sprite(self.mod, "GFX_same")
        self.sprite(self.mod, "GFX_same", "gfx/other.dds", "interface/other.gfx")
        self.assertEqual("conflicting_definitions", Audit(self.mod, self.engine).resolve("sprite", "GFX_same")["status"])

    def test_model_clone_mesh_and_animation_follow_engine_ownership(self):
        self.put(self.mod, "gfx/entities/national.asset", 'entity={name="national_entity" clone="engine_entity"}')
        self.put(self.engine, "gfx/entities/base.asset", 'entity={name="engine_entity" pdxmesh="engine_mesh"}')
        self.put(self.engine, "gfx/entities/base.gfx", 'objectTypes={pdxmesh={name="engine_mesh" file="gfx/base.mesh" animation={id="idle" type="engine_idle"}} animation={name="engine_idle" file="gfx/base.anim"}}')
        self.put(self.engine, "gfx/base.mesh", "mesh"); self.put(self.engine, "gfx/base.anim", "animation")
        result = Audit(self.mod, self.engine).resolve("entity", "national_entity")
        self.assertEqual("engine_fallback", result["status"])
        self.assertEqual("engine_mesh", result["dependencies"][0]["dependencies"][0]["name"])

    def test_mio_inheritance_and_missing_parent_are_not_silenced(self):
        self.sprite(self.mod, "GFX_factory")
        self.put(self.mod, "common/military_industrial_organization/organizations/national.txt", 'national={include=missing_parent icon=GFX_factory}')
        result = Audit(self.mod, self.engine).resolve("mio", "national")
        self.assertEqual("missing_asset_or_dependency", result["status"])
        self.assertTrue(any(d["name"] == "missing_parent" for d in result["dependencies"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
