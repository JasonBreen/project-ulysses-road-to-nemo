"""Reviewed English research typography; all glyph pixels remain mod-authored."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    name: str
    atlas: str
    color: str
    purpose: str


BINDINGS = {
    'Main_14_black': Binding('ACResearchCloseDark', 'ACBriefing16', '0xff081621',
        'Retain the unused close-button dark-text role; its authored icon supplies the visible close mark.'),
    'vic_18': Binding('ACResearchClose', 'ACBriefing16', '0xffdaedf2',
        'Close-button text role; the existing icon, shortcut and tooltip remain unchanged.'),
    'hoi_16mbs': Binding('ACResearchBody', 'ACBriefing16', '0xffdaedf2',
        'Descriptions and bonuses use readable light body text, retaining all original inline state-color codes.'),
    'hoi_18mbs': Binding('ACResearchResource', 'ACBriefing16', '0xffdaedf2',
        'Resource values retain their eighteen-pixel line budget using the authored sixteen-point atlas.'),
    'hoi_20b': Binding('ACResearchAction', 'ACBriefing20', '0xffdaedf2',
        'Research actions and the time label retain a prominent light-text role inside the existing controls.'),
    'hoi_20bs': Binding('ACResearchName', 'ACBriefing16', '0xffdaedf2',
        'Inherited item names have twenty-pixel rectangles; the eighteen-pixel briefing line fits without moving them.'),
    'hoi4_typewriter16': Binding('ACResearchLabel', 'ACBriefing16', '0xffa9c7d4',
        'Former black-on-paper stat labels become secondary light labels on the existing navy panels.'),
    'hoi4_typewriter16_inverted': Binding('ACResearchValue', 'ACBriefing16', '0xffdaedf2',
        'Amounts and differences remain brighter than stat labels, with their original inline state colors.'),
    'hoi4_typewriter22': Binding('ACResearchCategory', 'ACBriefing16', '0xffa9c7d4',
        'Category labels have twenty-pixel rectangles despite a previous twenty-two-pixel font; fit the actual rectangle.'),
    'hoi_36header': Binding('ACResearchHeader', 'ACBriefing20', '0xffdaedf2',
        'Year and category headers fit the inherited thirty-two-pixel minimum height instead of exceeding it.'),
    'hoi_22tech': Binding('ACResearchSubtitle', 'ACBriefing20', '0xff82afc2',
        'Technical subtitles remain subordinate in muted cyan while becoming readable on navy.'),
    'hoi_33': Binding('ACResearchHeading', 'ACBriefing20', '0xff82afc2',
        'Section headings retain the subordinate color role and use the established briefing heading size.'),
}
