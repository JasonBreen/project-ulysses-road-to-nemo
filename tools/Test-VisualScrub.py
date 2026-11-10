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
