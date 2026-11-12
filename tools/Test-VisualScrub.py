"""Static regressions for generated visual-scrub news bindings."""
import json
import hashlib
import re
import unittest
from unittest import mock
from visual_scrub import build_fallthroughs as scrub


class NewsBindingsTests(unittest.TestCase):
    def test_archived_globe_assets_are_preserved(self):
        scrub.validate_globe_assets()

    def test_frontend_keeps_all_original_animation_tiles(self):
        source = scrub.ROOT / 'tools/usea_expansion/frontend_background_original.gui'
        manifest = json.loads(scrub.GLOBE_MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest(), manifest['layout_sha256'])
        gui = (scrub.MOD / 'interface/frontendmainview.gui').read_text(encoding='utf-8')
        self.assertIn(source.read_text(encoding='utf-8').strip(), gui)
        tiles = re.findall(r'quadTextureSprite\s*=\s*"GFX_frontend_bg_tile_(\d+)"', gui)
        self.assertCountEqual(tiles, [f'{index:02}' for index in range(1, 36)])

    def test_placeholder_generation_never_overwrites_the_globe(self):
        with mock.patch.object(scrub, 'save_dds') as saved, mock.patch.object(scrub, 'EARTH_BACKGROUNDS', {}):
            scrub.write_placeholders()
        self.assertNotIn(scrub.MOD / scrub.MENU_FALLBACK,
                         [call.args[0] for call in saved.call_args_list])

    def inventory(self):
        return json.loads(scrub.INVENTORY.read_text(encoding="utf-8"))["sprites"]

    def test_bookmark_picture_fits_the_bookmark_entry(self):
        # Native N004: the 780 x 620 briefing window background was bound to the
        # 232 x 211 bookmark entry and covered the scenario screen.
        texture, frames, _ = scrub.choose("GFX_select_date_1936")
        self.assertEqual((texture, frames), (scrub.BOOKMARK_PICTURE, 1))
        with scrub.Image.open(scrub.MOD / texture) as image:
            self.assertEqual(image.size, (180, 104))
        gui = (scrub.MOD / "interface/frontendgamesetupview.gui").read_text(encoding="utf-8")
        entry = gui[gui.index('name = "bookmark_entry"'):gui.index('name = "spirit_idea_entry"')]
        self.assertEqual(tuple(map(int, re.search(r"width = (\d+)\s+height = (\d+)", entry).groups())), scrub.BOOKMARK_ENTRY_SIZE)
        icon = entry[entry.index('spriteType = "GFX_select_date_1936"'):]
        self.assertEqual(tuple(map(int, re.search(r"x = (\d+)\s+y = (\d+)", icon).groups())), scrub.BOOKMARK_ICON_OFFSET)
        scrub.validate_presentation(self.inventory())

    def test_window_sized_bookmark_picture_is_rejected(self):
        row = {"name": "GFX_select_date_1936", "texture": "gfx/interface/ac_briefing/select_date.dds", "frames": 1}
        with self.assertRaisesRegex(SystemExit, "Bookmark picture overflows"):
            scrub.validate_presentation([row])

    def test_backdrops_behind_controls_carry_no_label(self):
        # Native N005: labelled panels were drawn over research trees and doctrine cards.
        paths = scrub.backdrop_paths()
        self.assertIn(scrub.PANEL, paths)
        self.assertTrue(set(scrub.EARTH_BACKGROUNDS) <= set(paths))
        for relative in paths:
            with self.subTest(path=relative), scrub.Image.open(scrub.MOD / relative) as image:
                self.assertEqual(image.convert("RGBA").getcolors(maxcolors=2), [(image.width * image.height, scrub.NAVY)])

    def test_labelled_backdrop_is_rejected(self):
        labelled = scrub.panel(959, 715, "INFANTRY TAB")
        opened = mock.MagicMock()
        opened.__enter__.return_value = labelled
        with mock.patch.object(scrub.Image, "open", return_value=opened):
            with self.assertRaisesRegex(SystemExit, "unlabelled navy backdrop"):
                scrub.validate_presentation([])

    def test_every_installed_doctrine_sprite_resolves_inside_the_mod(self):
        bound = {row["name"]: row for row in self.inventory()}
        defined = {name.lower() for name in scrub.defined_sprites()}
        text = scrub.GFX_OUT.read_text(encoding="utf-8-sig")
        self.assertGreaterEqual(len(scrub.DOCTRINE_SPRITES), 134)
        for name, expected in scrub.DOCTRINE_SPRITES.items():
            with self.subTest(name=name):
                if name.lower() in defined:
                    self.assertNotIn(name, bound)
                    continue
                row = bound[name]
                self.assertEqual(row["frames"], expected["frames"])
                self.assertIn(scrub.sprite_block(name, row["texture"], row["frames"]), text)
                with scrub.Image.open(scrub.MOD / row["texture"]) as image:
                    if expected["role"] == "icon" and expected["frames"] == 1:
                        self.assertLessEqual(image.size, (expected["width"], expected["height"]))
                    else:
                        self.assertEqual(image.size, (expected["width"], expected["height"]))

    def test_doctrine_frame_mismatch_is_rejected(self):
        name = "GFX_doctrine_decor_land"
        row = {"name": name, "texture": scrub.DOCTRINE_DECOR, "frames": 1}
        with self.assertRaisesRegex(SystemExit, "frame count differs"):
            scrub.validate_presentation([row])

    def test_news_variants_use_news_format(self):
        for name in ("GFX_news_event_009", "GFX_news_event_civil_war", "GFX_news_event_election"):
            with self.subTest(name=name):
                texture, frames, _ = scrub.choose(name)
                self.assertEqual((texture, frames), (scrub.NEWS_DEFAULT, 1))
                with scrub.Image.open(scrub.MOD / texture) as image:
                    self.assertEqual(image.size, (397, 153))

    def test_country_reports_keep_country_art(self):
        for suffix, expected in (("parliament", scrub.EVENT_PARLIAMENT), ("army", scrub.EVENT_ARMY), ("bad_news", scrub.EVENT_NEWS)):
            self.assertEqual(scrub.choose("GFX_report_event_" + suffix)[:2], (expected, 1))

    def test_generated_news_bindings_match_inventory(self):
        rows = json.loads(scrub.INVENTORY.read_text(encoding="utf-8"))["sprites"]
        news = [row for row in rows if row["name"].lower().startswith("gfx_news_event_")]
        self.assertTrue(news)
        scrub.validate_bindings(scrub.GFX_OUT.read_text(encoding="utf-8-sig"), news)
        for row in news:
            self.assertEqual(row["texture"], scrub.NEWS_DEFAULT)

    def test_stale_country_binding_is_rejected(self):
        row = {"name": "GFX_news_event_009", "texture": scrub.NEWS_DEFAULT, "frames": 1}
        stale = scrub.sprite_block(row["name"], scrub.EVENT_NEWS, 1)
        with self.assertRaisesRegex(SystemExit, "Stale sprite binding"):
            scrub.validate_bindings(stale, [row])

    def test_country_sized_news_is_rejected_even_when_binding_matches(self):
        row = {"name": "GFX_news_event_009", "texture": scrub.EVENT_NEWS, "frames": 1}
        with self.assertRaisesRegex(SystemExit, "Invalid news picture dimensions"):
            scrub.validate_bindings(scrub.sprite_block(row["name"], row["texture"], 1), [row])


if __name__ == "__main__":
    unittest.main()
