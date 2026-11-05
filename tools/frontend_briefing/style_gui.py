"""Reapply briefing visuals when regenerating the original 1.19 GUI layout.

tools/port_1_19/restore_original_gui.py calls style() while rebuilding the GUI
from the installed game. --apply applies the same remap to the committed GUI
(idempotent); --check fails if any remapped engine sprite is still bound.
"""
import argparse
import re
from pathlib import Path

GUI = Path(__file__).resolve().parents[2] / 'mod/2985041246/interface/frontendgamesetupview.gui'

SPRITES = {
    'country_selection_bg':'country_selection', 'select_date_bg':'select_date',
    'button_148x34':'button148', 'button_221x34':'button221',
    'button_123x34':'button123', 'button_261x34':'button261',
    'mini_country_selector':'mini_selector',
    'country_selection_minor_entry':'country_entry',
    'bookmark_entry_bg':'bookmark_entry',
    'minor_portrait_overlay':'portrait_frame', 'pol_factions_strip':'political_strip',
    'lobby_right_sidepanel_bg':'lobby_info',
    'lobby_lower_right_sidepanel_bg':'lobby_settings',
    # Lobby restyle and hide (5 November 2026; lobby_sprites.json).
    'tiled_frontend_upper_bar':'lobby_upper_bar', 'tiled_frontend_lower_bar':'lobby_lower_bar',
    'tiled_window2_1b_border':'lobby_window', 'tiled_window_1b_thin_border':'lobby_thin_window',
    'tiled_header_1':'lobby_header', 'tiled_generic_bg_1':'lobby_row',
    'no_frame_special_bg':'lobby_list', 'game_settings_bg':'lobby_settings_bg',
    'small_pol_piechart_frame':'lobby_hidden', 'small_pol_piechart_overlay':'lobby_hidden',
    'load_save_top_screen':'lobby_hidden', 'load_save_bottom_screen':'lobby_hidden',
}

OVERLAY = '''
		# Cosmetic layer over the fixed bookmark map; transparent value apertures
		# retain its country-specific figures. Never intercept map or flag input.
		iconType = {
			name = "ac_briefing_map_statistics"
			spriteType = "GFX_ac_briefing_map_statistics_overlay"
			position = { x = 975 y = -300 }
			alwaystransparent = yes
		}
'''


def style(text):
    for old,new in SPRITES.items():
        text = text.replace('"GFX_'+old+'"', '"GFX_ac_briefing_'+new+'"')
    text = re.sub(r'"(Aces(?:12|14|16))_black"',r'"\1"',text)
    # The legacy statistics were baked into oversized inline map images and
    # have no live engine binding. The bounded overview author owns this area.
    text = re.sub(r'\s*iconType\s*=\s*\{\s*name\s*=\s*"ac_briefing_map_statistics".*?alwaystransparent\s*=\s*yes\s*\}', '', text, flags=re.S)
    return text


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--apply', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = GUI.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    styled = style(text)
    if args.check:
        left = sorted({old for old in SPRITES if '"GFX_'+old+'"' in text})
        if left or styled != text:
            raise SystemExit('Briefing remap not applied: ' + ', '.join(left))
        print('Briefing remap applied: %d sprite mappings' % len(SPRITES))
    elif styled != text:
        GUI.write_bytes((b'\xef\xbb\xbf' if bom else b'') + styled.encode('utf-8'))
        print('Briefing remap written to ' + GUI.name)
    else:
        print('Briefing remap already applied')


if __name__ == '__main__':
    main()
