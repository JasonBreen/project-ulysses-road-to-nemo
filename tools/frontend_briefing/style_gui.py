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
    if 'name = "ac_briefing_map_statistics"' not in text:
        # Match this unique existing control rather than numeric source lines.
        marker = re.search(r'\t\tinstantTextBoxType = \{\s*name = "history".*?\n\t\t\}',text,re.S)
        if not marker:raise ValueError('Country-selection history control missing')
        text = text[:marker.end()]+'\n'+OVERLAY+text[marker.end():]
    return text
