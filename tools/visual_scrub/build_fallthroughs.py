#!/usr/bin/env python3
"""Rebind player-visible vanilla/Earth sprite names to packaged mod art.

This does not copy installed HOI4 pixels. Sprite names that the engine still
resolves from an unreplaced interface file are redefined here, in a file whose
name sorts after the vanilla interface files, and pointed at textures already
shipped by the mod or at generated placeholders marked as such.

Run from the repository root:

    python3 -B tools/visual_scrub/build_fallthroughs.py
    python3 -B tools/visual_scrub/build_fallthroughs.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mod" / "2985041246"
GFX_OUT = MOD / "interface" / "zz_ac_visual_scrub.gfx"
INVENTORY = Path(__file__).resolve().parent / "inventory.json"
NAME_RE = re.compile(r'\bname\s*=\s*"?(GFX_[A-Za-z0-9_]+)', re.I)

NAVY = (7, 20, 34, 255)
CYAN = (62, 200, 216, 255)
INK = (222, 237, 243, 255)

# Existing Strangereal/mod textures. Reuse is preferred over new pixels.
IDEA_AIR = "gfx/interface/ac_briefing/idea_air.dds"
IDEA_NAVY = "gfx/interface/ac_briefing/idea_navy.dds"
IDEA_LAND = "gfx/interface/ac_briefing/idea_military.dds"
IDEA_INDUSTRY = "gfx/interface/ac_briefing/idea_industry.dds"
IDEA_ASSEMBLY = "gfx/interface/ac_briefing/idea_assembly.dds"
IDEA_ECONOMY = "gfx/interface/ac_briefing/idea_economy.dds"
IDEA_SECURITY = "gfx/interface/ac_briefing/idea_security.dds"
IDEA_RADAR = "gfx/interface/ac_briefing/idea_radar.dds"
IDEA_WORLD = "gfx/interface/ac_briefing/idea_world.dds"
MBT = "gfx/AC_land/research/mbt_2006.dds"
INFANTRY = "gfx/AC_land/research/infantry_2006.dds"
ARTILLERY = "gfx/AC_land/research/tracked_artillery_2006.dds"
FIGHTER = "gfx/AC_air/research/fighter_2006.dds"
CARRIER = "gfx/AC_naval/blueprints/carrier_2006.dds"
SUBMARINE = "gfx/AC_naval/blueprints/submarine_2006.dds"
ESCORT = "gfx/AC_naval/blueprints/escort_2006.dds"
CRUISER = "gfx/AC_naval/blueprints/cruiser_2006.dds"
NAVAL_MODULE = "gfx/AC_naval/modules/light_engine_2006.dds"
LAND_MODULE = "gfx/AC_land/modules/powertrain_2006.dds"
BUILDINGS = "gfx/interface/ac_expansion/ui/GFX_ac_ui_buildings_strip.dds"
SPEC_AIR = "gfx/interface/ac_expansion/ui/GFX_technology_specialization_air.dds"
SPEC_LAND = "gfx/interface/ac_expansion/ui/GFX_technology_specialization_land.dds"
SPEC_NAVAL = "gfx/interface/ac_expansion/ui/GFX_technology_specialization_naval.dds"
SPEC_NUCLEAR = "gfx/interface/ac_expansion/ui/GFX_technology_specialization_nuclear.dds"
ALBUM = "gfx/interface/topbar/musicplayer/superevent_station_album_art.dds"
EVENT_ARMY = "gfx/event_pictures/report_event_army_issues_1.dds"
EVENT_PARLIAMENT = "gfx/event_pictures/report_event_blk_parliament.dds"
EVENT_NEWS = "gfx/event_pictures/report_event_bad_news_1.dds"
NEWS_DEFAULT = "gfx/AC_event_style/news_default.dds"
PANEL = "gfx/interface/ac_visual_scrub/panel_placeholder.dds"
PORTRAIT = "gfx/interface/ac_visual_scrub/portrait_placeholder.dds"
AGENCY = "gfx/interface/ac_visual_scrub/agency_placeholder.dds"
SCRUB_DIR = "gfx/interface/ac_visual_scrub/"
DOCTRINE_DECOR = SCRUB_DIR + "doctrine_decor.dds"
MENU_FALLBACK = "gfx/animated_textures/frontend_background/menu_fallback.dds"
MENU = MENU_FALLBACK
GLOBE_MANIFEST = ROOT / 'tools/usea_expansion/frontend_globe_original.json'
LOGO = "gfx/interface/logo_game.dds"
# The archive's own 180 x 104 bookmark picture. The 780 x 620 briefing window
# background must never be bound here: the bookmark entry is only 232 x 211.
BOOKMARK_PICTURE = "gfx/interface/select_date_1936.dds"
BOOKMARK_ENTRY_SIZE = (232, 211)
BOOKMARK_ICON_OFFSET = (27, 28)
ARTILLERY_BG = "gfx/interface/techtree/artillery_techtree_bg.dds"

CONTENT_PREFIXES = (
    "GFX_idea_",
    "GFX_generic_mio_",
    "GFX_report_event_",
    "GFX_news_event_",
    "GFX_portrait_",
    "GFX_Portrait_",
    "GFX_goal_",
    "GFX_focus_",
    "GFX_TC_",
    "GFX_TM_",
    "GFX_SD_tv_",
    "GFX_SM_",
    "GFX_doctrine_",
    "GFX_ability_",
)

# Earth photographs shipped at vanilla technology-background paths. The sprite
# that displays them lives in the unreplaced countrytechnologyview.gfx, so the
# file at that path is what the player sees. Artillery is kept: it is a
# futuristic gun illustration already in the mod, not a vanilla photograph.
# The engine draws these behind interactive research trees, so they are plain
# navy backdrops; the names below only record which tab each one sits behind.
EARTH_BACKGROUNDS = {
    "gfx/interface/techtree/infantry_techtree_bg.dds": "INFANTRY TAB",
    "gfx/interface/techtree/air_techtree_bg.dds": "AIR TAB",
    "gfx/interface/techtree/naval_techtree_bg.dds": "NAVAL TAB",
    "gfx/interface/techtree/industry_techtree_bg.dds": "INDUSTRY TAB",
    "gfx/interface/techtree/support_techtree_bg.dds": "SUPPORT TAB",
    "gfx/interface/armortech_bg.dds": "ARMOUR TAB",
}

CONTINUOUS = {
    "continuous_naval_production": "gfx/interface/ac_expansion/continuous/continuous_naval_production.dds",
    "continuous_air_production": "gfx/interface/ac_expansion/continuous/continuous_air_production.dds",
    "continuous_non_factory_construct": "gfx/interface/ac_expansion/continuous/continuous_non_factory_construct.dds",
    "continuous_reduce_training_time": "gfx/interface/ac_expansion/continuous/continuous_reduce_training_time.dds",
    "continuous_suppression": "gfx/interface/ac_expansion/continuous/continuous_suppression.dds",
    "continuous_repair": "gfx/interface/ac_expansion/continuous/continuous_repair.dds",
    "continuous_repairments": "gfx/interface/ac_expansion/continuous/continuous_repair.dds",
    "continuous_tech_share": "gfx/interface/ac_expansion/continuous/continuous_tech_share.dds",
    "continuous_research": "gfx/interface/ac_expansion/continuous/continuous_tech_share.dds",
    "continuous_boost_freedom": "gfx/interface/ac_expansion/continuous/continuous_boost_freedom.dds",
    "continuous_restrict_freedom": "gfx/interface/ac_expansion/continuous/continuous_restrict_freedom.dds",
    "continuous_increase_nu": "gfx/interface/ac_expansion/continuous/continuous_boost_freedom.dds",
    "continuous_def_against_influence": "gfx/interface/ac_expansion/continuous/continuous_restrict_freedom.dds",
    "continuous_armor_production": "gfx/interface/ac_expansion/continuous/continuous_naval_production.dds",
    "DEN_undermine_overlord_continuous_focus": "gfx/interface/ac_expansion/continuous/DEN_undermine_overlord_continuous_focus.dds",
    "ETH_strengthen_the_black_lions": "gfx/interface/ac_expansion/continuous/ETH_strengthen_the_black_lions.dds",
    "ETH_supporting_the_arbegnoch": "gfx/interface/ac_expansion/continuous/ETH_supporting_the_arbegnoch.dds",
    "ETH_continuous_strengthen_the_black_lions": "gfx/interface/ac_expansion/continuous/ETH_strengthen_the_black_lions.dds",
    "ETH_continuous_supporting_the_arbegnoch": "gfx/interface/ac_expansion/continuous/ETH_supporting_the_arbegnoch.dds",
}

GRAND_DOCTRINES = [
    "mobile_warfare", "superior_firepower", "grand_battleplan", "grand_battle_plan",
    "mass_assault", "fleet_in_being", "trade_interdiction", "base_strike",
    "strategic_destruction", "battlefield_support", "operational_integrity",
    "new_mobile_warfare", "new_superior_firepower", "new_grand_battleplan",
    "new_mass_assault", "new_fleet_in_being", "new_trade_interdiction",
    "new_base_strike", "new_strategic_destruction", "new_battlefield_support",
    "new_operational_integrity",
]

# Sprite names, roles, frame counts and sizes that the installed 1.19 doctrine
# definitions request (see extract_doctrine_sprites.py). Names and dimensions
# only; no installed pixels are read by this generator.
DOCTRINE_SPRITES = json.loads((Path(__file__).resolve().parent / "doctrine_sprites.json").read_text(encoding="utf-8"))["sprites"]
BRANCH_ART = {"land": IDEA_LAND, "sea": IDEA_NAVY, "air": IDEA_AIR, "special_forces": IDEA_SECURITY}

TAGS = ("eng", "fra", "ger", "ita", "jap", "sov", "usa")
TANK_WEIGHTS = ("light", "medium", "heavy")
TANK_ROLES = ("", "aa", "artillery", "destroyer")
TANK_SLOTS = ("armor_type_slot", "engine_type_slot")


def font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fitted(draw: ImageDraw.ImageDraw, text: str, start: int, max_width: int) -> ImageFont.ImageFont:
    size = start
    while size > 8:
        used = font(size)
        box = draw.textbbox((0, 0), text, font=used)
        if box[2] - box[0] <= max_width:
            return used
        size -= 1
    return font(8)


def panel(width: int, height: int, label: str) -> Image.Image:
    image = Image.new("RGBA", (width, height), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 2, width - 3, height - 3), outline=CYAN, width=max(2, min(width, height) // 80))
    margin = max(8, width // 16)
    face = fitted(draw, "MOD PLACEHOLDER", max(14, min(width, height) // 14), width - margin * 2)
    small = fitted(draw, label, max(12, min(width, height) // 22), width - margin * 2)
    note = fitted(draw, "Not official art", max(11, min(width, height) // 26), width - margin * 2)
    lines = ["MOD PLACEHOLDER", label, "Not official art"]
    faces = [face, small, note]
    heights = []
    for line, used in zip(lines, faces):
        box = draw.textbbox((0, 0), line, font=used)
        heights.append(box[3] - box[1])
    gap = max(6, height // 40)
    total = sum(heights) + gap * (len(lines) - 1)
    y = max(8, (height - total) // 2)
    for line, used, line_height in zip(lines, faces, heights):
        box = draw.textbbox((0, 0), line, font=used)
        x = max(8, (width - (box[2] - box[0])) // 2)
        draw.text((x, y), line, font=used, fill=INK)
        y += line_height + gap
    return image


def backdrop(width: int, height: int) -> Image.Image:
    """Unlabelled navy fill for art the engine draws behind interactive content."""
    return Image.new("RGBA", (width, height), NAVY)


def doctrine_backdrop(width: int, height: int) -> str:
    return f"{SCRUB_DIR}doctrine_backdrop_{width}x{height}.dds"


def doctrine_milestone(branch: str) -> str:
    return f"{SCRUB_DIR}doctrine_milestone_{branch}.dds"


def doctrine_binding(name: str) -> tuple[str, int, str]:
    row = DOCTRINE_SPRITES[name]
    if row["role"] == "background":
        return doctrine_backdrop(row["width"], row["height"]), 1, "Doctrine track background rebound to an unlabelled navy backdrop of the engine card size."
    if row["role"] == "icon_frame":
        return DOCTRINE_DECOR, row["frames"], "Doctrine track ornament rebound to a plain generated rule with the engine frame count."
    if row["frames"] != 1:
        return doctrine_milestone(row["branch"]), row["frames"], "Doctrine milestone badge rebound to existing mod branch art with the engine frame count."
    return BRANCH_ART[row["branch"]], 1, "Subdoctrine icon rebound to existing mod branch art."


def milestone_strip(branch: str, width: int, height: int, frames: int) -> Image.Image:
    """Existing branch icon centred in each engine frame; earlier frames are dimmed."""
    strip = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cell = width // frames
    with Image.open(MOD / BRANCH_ART[branch]) as source:
        icon = source.convert("RGBA")
    for index in range(frames):
        used = icon
        if index < frames - 1:
            red, green, blue, alpha = icon.split()
            dimmed = [band.point(lambda value: value * 11 // 20) for band in (red, green, blue)]
            used = Image.merge("RGBA", (*dimmed, alpha))
        strip.alpha_composite(used, (index * cell + (cell - icon.width) // 2, (height - icon.height) // 2))
    return strip


def decor_strip(width: int, height: int, frames: int) -> Image.Image:
    """Transparent ornament strip with one thin rule per frame."""
    strip = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(strip)
    cell = width // frames
    for index in range(frames):
        colour = CYAN if index == frames - 1 else (CYAN[0] * 11 // 20, CYAN[1] * 11 // 20, CYAN[2] * 11 // 20, 255)
        draw.rectangle((index * cell + 24, height - 6, (index + 1) * cell - 25, height - 5), fill=colour)
    return strip


def save_dds(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="DDS")


def defined_sprites() -> set[str]:
    found: set[str] = set()
    for path in MOD.rglob("*.gfx"):
        if path.resolve() == GFX_OUT.resolve():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        active = "\n".join(line.split("#", 1)[0] for line in text.splitlines())
        found.update(NAME_RE.findall(active))
    return found


def choose(name: str) -> tuple[str, int, str]:
    """Return texture, frames, and why this sprite was rebound."""
    lowered = name.lower()
    if name == "GFX_buildings_strip":
        return BUILDINGS, 31, "1.15+ and older building icons share this strip; the mod already has a 31-frame geometric replacement."
    if name == "GFX_naval_headquarter_buildings_bg":
        return PANEL, 1, "Naval headquarters card background is an unreplaced engine sprite."
    if name in ("GFX_axis_album_art", "GFX_allied_faceplate", "GFX_comintern_album_art"):
        return ALBUM, 2, "WWII faction music-player art replaced with the mod superevent album."
    if name == "GFX_dam_icon_small":
        return IDEA_INDUSTRY, 1, "Dam icon rebound to existing mod industry art."
    if name == "GFX_canal_icon_small":
        return IDEA_NAVY, 1, "Canal icon rebound to existing mod navy art."
    if name == "GFX_raid_unit_icon_nuclear_raids":
        return IDEA_RADAR, 1, "Nuclear raid icon rebound to existing mod radar art."
    if name == "GFX_intelligence_agency_logo_ger":
        return AGENCY, 2, "Belka was still using the German agency logo sprite."
    if name == "GFX_frontend_bg":
        return MENU, 1, "Original archived globe fallback; the animated Ulysses tile assets are preserved."
    if name == "GFX_frontend_game_logo":
        return LOGO, 1, "Main-menu logo rebound to the existing Project Ulysses wordmark."
    if name == "GFX_select_date_1936":
        return BOOKMARK_PICTURE, 1, "Both 1991 bookmarks keep this sprite name; bound to the archive's own bookmark picture so the lookup stays in the mod."
    if name == "GFX_leader_unknown" or name.startswith("GFX_portrait") or name.startswith("GFX_Portrait"):
        return PORTRAIT, 1, "Earth or unknown leader portrait rebound to a marked placeholder."
    if lowered.startswith("gfx_news_event_"):
        return NEWS_DEFAULT, 1, "Earth news photograph rebound to the mod news-format picture (397 x 153)."
    if "report_event" in lowered:
        if any(word in lowered for word in ("parliament", "treaty", "election")):
            return EVENT_PARLIAMENT, 1, "Earth news photograph rebound to the existing Belkan parliament picture."
        if any(word in lowered for word in ("soldier", "army", "civil_war", "war")):
            return EVENT_ARMY, 1, "Earth war photograph rebound to an existing mod army picture."
        return EVENT_NEWS, 1, "Earth news photograph rebound to an existing mod news picture."
    if lowered.startswith("gfx_goal_continuous") or lowered.startswith("gfx_idea_continuous") or lowered.startswith("gfx_focus_continuous") or "continuous_focus" in lowered:
        token = name
        for prefix in ("GFX_goal_", "GFX_idea_", "GFX_focus_", "GFX_"):
            if token.startswith(prefix):
                token = token[len(prefix):]
                break
        texture = CONTINUOUS.get(token, CONTINUOUS["continuous_naval_production"])
        return texture, 1, "Vanilla continuous-focus sprite name aliased to the existing mod icon."
    if name.startswith("GFX_specialization_"):
        branch = name.removeprefix("GFX_specialization_")
        return {
            "air": SPEC_AIR,
            "land": SPEC_LAND,
            "naval": SPEC_NAVAL,
            "nuclear": SPEC_NUCLEAR,
        }.get(branch, SPEC_LAND), 1, "Facility specialisation icon aliased to the mod special-project icon."
    if "doctrine" in lowered or any(key in lowered for key in GRAND_DOCTRINES) or lowered.endswith("_bg") and any(key in lowered for key in ("warfare", "firepower", "battleplan", "assault", "fleet", "interdiction", "base_strike", "destruction", "battlefield", "integrity")):
        if lowered.endswith("_bg") or "_bg_" in lowered:
            return PANEL, 1, "Grand-doctrine illustration rebound to an unlabelled navy backdrop."
        if any(word in lowered for word in ("naval", "fleet", "ship", "carrier", "submarine", "base_strike", "trade_interdiction")):
            return IDEA_NAVY, 1, "Naval doctrine icon rebound to existing mod navy art."
        if any(word in lowered for word in ("air", "strategic_destruction", "battlefield", "operational")):
            return IDEA_AIR, 1, "Air doctrine icon rebound to existing mod air art."
        return IDEA_LAND, 1, "Land doctrine icon rebound to existing mod military art."
    if lowered.startswith("gfx_sd_tv_"):
        if "carrier" in lowered:
            return CARRIER, 1, "Ship-designer television icon rebound to the mod carrier blueprint."
        if "submarine" in lowered:
            return SUBMARINE, 1, "Ship-designer television icon rebound to the mod submarine blueprint."
        if "cruiser" in lowered or "heavy" in lowered:
            return CRUISER, 1, "Ship-designer television icon rebound to the mod cruiser blueprint."
        return ESCORT, 1, "Ship-designer television icon rebound to the mod escort blueprint."
    if lowered.startswith("gfx_sm_"):
        return NAVAL_MODULE, 1, "Ship-designer module icon rebound to an existing mod naval module."
    if lowered.startswith("gfx_tc_large_plane"):
        return FIGHTER, 1, "Aircraft-designer airframe icon rebound to the mod fighter research card."
    if lowered.startswith("gfx_tc_") or lowered.startswith("gfx_tm_"):
        if "artillery" in lowered:
            return ARTILLERY, 1, "Tank-designer artillery icon rebound to the mod artillery research card."
        if "engine" in lowered:
            return LAND_MODULE, 1, "Tank-designer module icon rebound to an existing mod land module."
        return MBT, 1, "Tank-designer chassis icon rebound to the mod main-battle-tank research card."
    if any(word in lowered for word in ("air", "plane", "fighter", "bomber", "cas")):
        return IDEA_AIR, 1, "Air idea or manufacturer icon rebound to existing mod air art."
    if any(word in lowered for word in ("naval", "navy", "ship", "submarine", "carrier")):
        return IDEA_NAVY, 1, "Naval idea or manufacturer icon rebound to existing mod navy art."
    if any(word in lowered for word in ("tank", "armor", "armour", "artillery", "infantry", "army")):
        return IDEA_LAND, 1, "Land idea or manufacturer icon rebound to existing mod military art."
    if any(word in lowered for word in ("industry", "factory", "production", "build", "infra", "mine")):
        return IDEA_INDUSTRY, 1, "Industry idea icon rebound to existing mod industry art."
    if any(word in lowered for word in ("econom", "trade", "tax", "bank")):
        return IDEA_ECONOMY, 1, "Economy idea icon rebound to existing mod economy art."
    if any(word in lowered for word in ("nuclear", "radar", "rocket", "raid")):
        return IDEA_RADAR, 1, "Facility or raid icon rebound to existing mod radar art."
    return IDEA_ASSEMBLY, 1, "Remaining Earth/generic idea icon rebound to existing mod assembly art."


def in_scope(name: str) -> bool:
    """Content pictures only. Buttons, flags, scrollbars and Paradox chrome stay."""
    if name in {"GFX_frontend_bg", "GFX_frontend_game_logo", "GFX_select_date_1936", "GFX_leader_unknown"}:
        return True
    if name.startswith(CONTENT_PREFIXES) or name in DOCTRINE_SPRITES:
        return True
    if name in {
        "GFX_buildings_strip", "GFX_naval_headquarter_buildings_bg",
        "GFX_axis_album_art", "GFX_allied_faceplate", "GFX_comintern_album_art",
        "GFX_specialization_air", "GFX_specialization_land", "GFX_specialization_naval",
        "GFX_specialization_nuclear", "GFX_dam_icon_small", "GFX_canal_icon_small",
        "GFX_infantry_techtree_bg", "GFX_air_techtree_bg", "GFX_naval_techtree_bg",
        "GFX_industry_techtree_bg", "GFX_support_techtree_bg", "GFX_artillery_techtree_bg",
        "GFX_armortech_bg", "GFX_intelligence_agency_logo_ger", "GFX_raid_unit_icon_nuclear_raids",
        "GFX_mob_warfare_bg", "GFX_sup_firepower_bg", "GFX_grand_battleplan_bg", "GFX_mass_assault_bg",
    }:
        return True
    for key in GRAND_DOCTRINES:
        if name == "GFX_" + key or name.startswith("GFX_" + key + "_"):
            return True
    return False


def content_sprite_names() -> set[str]:
    """Sprite names the mod asks for that no mod gfx file defines."""
    defined = {name.lower() for name in defined_sprites()}
    names: set[str] = set()
    roots = [MOD / "common", MOD / "interface", MOD / "history", MOD / "events", MOD / "portraits"]
    gfx_re = re.compile(r"\b(GFX_[A-Za-z0-9_]+)\b")
    picture_re = re.compile(r"(?m)^\s*picture\s*=\s*([A-Za-z0-9_]+)\s*(?:#.*)?$")
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix.lower() not in {".txt", ".gui", ".yml"}:
                continue
            lines = []
            for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                out = []
                quoted = False
                for char in line:
                    if char == '"':
                        quoted = not quoted
                    if char == "#" and not quoted:
                        break
                    out.append(char)
                lines.append("".join(out))
            active = "\n".join(lines)
            for match in gfx_re.finditer(active):
                names.add(match.group(1))
            for match in picture_re.finditer(active):
                token = match.group(1)
                if not token.lower().startswith("gfx_"):
                    names.add("GFX_idea_" + token)
    # Chrome the dependency samples and the 1.19 building/doctrine/focus screens
    # still request from unreplaced interface files.
    names.update([
        "GFX_buildings_strip",
        "GFX_naval_headquarter_buildings_bg",
        "GFX_axis_album_art",
        "GFX_allied_faceplate",
        "GFX_comintern_album_art",
        "GFX_goal_generic_trade",
        "GFX_raid_unit_icon_nuclear_raids",
        "GFX_specialization_air",
        "GFX_specialization_land",
        "GFX_specialization_naval",
        "GFX_specialization_nuclear",
        "GFX_dam_icon_small",
        "GFX_canal_icon_small",
        "GFX_infantry_techtree_bg",
        "GFX_air_techtree_bg",
        "GFX_naval_techtree_bg",
        "GFX_industry_techtree_bg",
        "GFX_support_techtree_bg",
        "GFX_artillery_techtree_bg",
        "GFX_armortech_bg",
        "GFX_intelligence_agency_logo_ger",
        "GFX_frontend_bg",
        "GFX_frontend_game_logo",
        "GFX_select_date_1936",
        "GFX_leader_unknown",
    ])
    for key, _texture in CONTINUOUS.items():
        names.add("GFX_goal_" + key)
        names.add("GFX_idea_" + key)
        names.add("GFX_focus_" + key)
    for key in GRAND_DOCTRINES:
        names.update([
            "GFX_" + key,
            "GFX_" + key + "_medium",
            "GFX_doctrine_" + key,
            "GFX_doctrine_icon_" + key,
            "GFX_" + key + "_bg",
            "GFX_doctrine_bg_" + key,
        ])
    names.update([
        "GFX_mob_warfare_bg", "GFX_sup_firepower_bg", "GFX_grand_battleplan_bg", "GFX_mass_assault_bg",
    ])
    names.update(DOCTRINE_SPRITES)
    for weight in TANK_WEIGHTS:
        for role in TANK_ROLES:
            role_bit = f"_{role}" if role else ""
            for tag in ("",) + TAGS:
                suffix = f"_{tag}" if tag else ""
                names.add(f"GFX_TC_{weight}_tank{role_bit}_chassis{suffix}")
                for slot in TANK_SLOTS:
                    names.add(f"GFX_TM_{weight}_tank{role_bit}_chassis_{slot}{suffix}")
    for index in range(4):
        names.add(f"GFX_TC_large_plane_airframe_{index}")
        for tag in TAGS:
            names.add(f"GFX_TC_large_plane_airframe_{index}_{tag}")
    for kind in ("carrier", "cruiser", "heavy", "light", "submarine", "super_heavy"):
        names.add(f"GFX_SD_tv_{kind}")
    names.update([
        "GFX_SM_carrier_hull_armor",
        "GFX_SM_cruiser_hull_armor",
        "GFX_SM_heavy_hull_armor",
        "GFX_SM_light_hull_anti_air",
        "GFX_SM_submarine_anechoic_tiles",
    ])
    return {name for name in names if name.lower() not in defined and in_scope(name)}


def backdrop_paths() -> list[str]:
    """Every generated texture that sits behind controls and so carries no label."""
    doctrine = {doctrine_backdrop(row["width"], row["height"]) for row in DOCTRINE_SPRITES.values() if row["role"] == "background"}
    return sorted({PANEL, *EARTH_BACKGROUNDS, *doctrine})


def write_placeholders() -> None:
    save_dds(MOD / PANEL, backdrop(959, 715))
    # Labelled placeholders depend on the host font, so existing files are kept.
    if not (MOD / PORTRAIT).exists():
        save_dds(MOD / PORTRAIT, panel(156, 210, "PORTRAIT"))
    if not (MOD / AGENCY).exists():
        agency = Image.new("RGBA", (234, 119), (0, 0, 0, 0))
        agency.paste(panel(117, 119, "AGENCY"), (0, 0))
        agency.paste(panel(117, 119, "AGENCY"), (117, 0))
        save_dds(MOD / AGENCY, agency)
    for relative in EARTH_BACKGROUNDS:
        path = MOD / relative
        with Image.open(path) as current:
            width, height = current.size
        save_dds(path, backdrop(width, height))
    for row in DOCTRINE_SPRITES.values():
        if row["role"] == "background":
            save_dds(MOD / doctrine_backdrop(row["width"], row["height"]), backdrop(row["width"], row["height"]))
        elif row["role"] == "icon_frame":
            save_dds(MOD / DOCTRINE_DECOR, decor_strip(row["width"], row["height"], row["frames"]))
        elif row["frames"] != 1:
            save_dds(MOD / doctrine_milestone(row["branch"]), milestone_strip(row["branch"], row["width"], row["height"], row["frames"]))


def sprite_block(name: str, texture: str, frames: int) -> str:
    frame = f"\n\t\tnoOfFrames = {frames}" if frames != 1 else ""
    return (
        "\tspriteType = {\n"
        f'\t\tname = "{name}"\n'
        f'\t\ttexturefile = "{texture}"{frame}\n'
        "\t}"
    )


def validate_bindings(text: str, rows: list[dict]) -> None:
    for row in rows:
        if sprite_block(row["name"], row["texture"], row["frames"]) not in text:
            raise SystemExit("Stale sprite binding: " + row["name"])
        if row["name"].lower().startswith("gfx_news_event_"):
            with Image.open(MOD / row["texture"]) as image:
                if image.size != (397, 153) or row["frames"] != 1:
                    raise SystemExit("Invalid news picture dimensions: " + row["name"])


def validate_presentation(rows: list[dict]) -> None:
    """Size and frame contracts that a sprite-name match alone does not prove."""
    for relative in backdrop_paths():
        with Image.open(MOD / relative) as image:
            colours = image.convert("RGBA").getcolors(maxcolors=2)
        if colours is None or [colour for _count, colour in colours] != [NAVY]:
            raise SystemExit(f"{relative} must be an unlabelled navy backdrop")
    by_name = {row["name"]: row for row in rows}
    bookmark = by_name.get("GFX_select_date_1936")
    if bookmark:
        with Image.open(MOD / bookmark["texture"]) as image:
            fits = all(offset + size <= limit for offset, size, limit in zip(BOOKMARK_ICON_OFFSET, image.size, BOOKMARK_ENTRY_SIZE))
        if not fits:
            raise SystemExit("Bookmark picture overflows the bookmark entry: " + bookmark["texture"])
    for name, expected in DOCTRINE_SPRITES.items():
        row = by_name.get(name)
        if row is None:
            continue
        if row["frames"] != expected["frames"]:
            raise SystemExit(f"Doctrine sprite frame count differs from the engine definition: {name}")
        if expected["role"] != "icon" or expected["frames"] != 1:
            with Image.open(MOD / row["texture"]) as image:
                if image.size != (expected["width"], expected["height"]):
                    raise SystemExit(f"Doctrine sprite size differs from the engine definition: {name}")


def validate_globe_assets() -> None:
    """Never classify the owner's archived globe as replaceable placeholder art."""
    original = json.loads(GLOBE_MANIFEST.read_text(encoding='utf-8'))
    for relative, expected in original['assets'].items():
        path = MOD / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit('Archived Ulysses globe asset changed: ' + relative)


def build(check_only: bool) -> int:
    validate_globe_assets()
    if not check_only:
        write_placeholders()
    defined = defined_sprites()
    rows = []
    for name in sorted(content_sprite_names(), key=str.lower):
        if name in defined or name.lower() in {item.lower() for item in defined}:
            continue
        texture, frames, reason = choose(name)
        if name in DOCTRINE_SPRITES:
            texture, frames, reason = doctrine_binding(name)
        if name == "GFX_artillery_techtree_bg":
            texture, frames, reason = ARTILLERY_BG, 1, "Kept the existing futuristic artillery illustration and bound the sprite in the mod."
        if name in ("GFX_infantry_techtree_bg", "GFX_air_techtree_bg", "GFX_naval_techtree_bg", "GFX_industry_techtree_bg", "GFX_support_techtree_bg", "GFX_armortech_bg"):
            texture = {
                "GFX_infantry_techtree_bg": "gfx/interface/techtree/infantry_techtree_bg.dds",
                "GFX_air_techtree_bg": "gfx/interface/techtree/air_techtree_bg.dds",
                "GFX_naval_techtree_bg": "gfx/interface/techtree/naval_techtree_bg.dds",
                "GFX_industry_techtree_bg": "gfx/interface/techtree/industry_techtree_bg.dds",
                "GFX_support_techtree_bg": "gfx/interface/techtree/support_techtree_bg.dds",
                "GFX_armortech_bg": "gfx/interface/armortech_bg.dds",
            }[name]
            reason = "Earth photograph at the vanilla technology-background path replaced with an unlabelled navy backdrop."
        path = MOD / texture
        if not path.exists():
            raise SystemExit(f"Missing texture for {name}: {texture}")
        rows.append({"name": name, "texture": texture, "frames": frames, "reason": reason})
    if check_only:
        if not GFX_OUT.exists():
            raise SystemExit("Missing generated interface/zz_ac_visual_scrub.gfx")
        text = GFX_OUT.read_text(encoding="utf-8-sig")
        validate_bindings(text, rows)
        validate_presentation(rows)
        if json.loads(INVENTORY.read_text(encoding="utf-8"))["sprites"] != rows:
            raise SystemExit("Stale visual scrub inventory")
        present = set(NAME_RE.findall(text))
        expected = {row["name"] for row in rows}
        missing = sorted(expected - present)
        if missing:
            raise SystemExit("Scrub gfx is missing sprites:\n" + "\n".join(missing[:20]))
        overlap = sorted(present & defined)
        if overlap:
            raise SystemExit("Scrub gfx overrides sprites the mod already defines:\n" + "\n".join(overlap[:20]))
        if "Bundesnachrichtendienst" in (MOD / "history/countries/BLK - Belka.txt").read_text(encoding="utf-8-sig"):
            raise SystemExit("Belka history still shows the Earth agency name")
        if 'noOfFrames = 31' not in text.split('GFX_buildings_strip', 1)[1][:200]:
            raise SystemExit("Building strip frame count is not 31")
        for row in rows:
            if not (MOD / row["texture"]).exists():
                raise SystemExit("Missing texture " + row["texture"])
        print(f"Visual scrub check passed: {len(rows)} rebound sprites.")
        return 0
    body = [
        "spriteTypes = {",
        "\t# Player-visible vanilla and Earth sprite names rebound to mod art or marked placeholders.",
        "\t# The file name sorts after unreplaced engine interface files so these definitions win.",
        "\t# Placeholders are provisional presentation, not official Project Aces art.",
    ]
    current = None
    for row in rows:
        group = row["reason"]
        if group != current:
            body.append(f"\t# {group}")
            current = group
        body.append(sprite_block(row["name"], row["texture"], row["frames"]))
    body.append("}")
    # LF on every host, matching .gitattributes, so hashes do not depend on where this ran.
    GFX_OUT.write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")
    INVENTORY.write_text(json.dumps({
        "sprite_count": len(rows),
        "replaced_earth_backgrounds": sorted(EARTH_BACKGROUNDS),
        "kept_artillery_background": ARTILLERY_BG,
        "sprites": rows,
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {GFX_OUT.relative_to(ROOT)} with {len(rows)} sprites.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(build(args.check))


if __name__ == "__main__":
    main()
