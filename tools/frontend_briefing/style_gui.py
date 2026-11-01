"""Reapply briefing visuals when regenerating the original 1.19 GUI layout."""
import re

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
