"""Shared seams for the Usea Depth packages. Frozen after the seams PR.

Owner generators keep foreign import blocks with foreign_import_blocks() and
reinsert(); a content package adds or replaces only its own block with
attach_file(). The remaining helpers keep layout, art, long-form events and
office leaders consistent across the six content packages.
"""
import importlib.util
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mod/2985041246"
FOCUS = MOD / "common/national_focus"

# Same contract as preserved_imports() in tools/build_continental_war.py.
IMPORTS = re.compile(r"(?m)^\t# BEGIN ([A-Z][A-Z ]*) IMPORTS\n(?:\tshared_focus = \w+\n)+\t# END \1 IMPORTS\n")
BEGIN = re.compile(r"(?m)^[ \t]*# BEGIN ([A-Z][A-Z ]*) IMPORTS[ \t]*$")
CAMPAIGNS = "AC CAMPAIGNS"
CAMPAIGN_ANCHOR = "\t# BEGIN AC CAMPAIGNS IMPORTS\n"

# Marker names and wrapper files each package may touch.
MARKERS = {
    "eru": ("USEA DEPTH ERUSEA", ("ERU_opening.txt", "ERU.txt")),
    "fcu": ("USEA DEPTH CENTRAL USEA", ("FCU_opening.txt", "FCU.txt")),
    "npt": ("USEA DEPTH NORTH POINT", ("NPT.txt",)),
    "partners": ("USEA DEPTH PARTNERS", ("SNS.txt", "AMB.txt", "UGE.txt", "DEL.txt")),
}


def normal(text):
    return text.lstrip("\ufeff").replace("\r\n", "\n")


def import_blocks(source):
    """Return (name, ids, text) for each well-formed block, in file order."""
    source = normal(source)
    found = [(m[1], re.findall(r"shared_focus = (\w+)", m[0]), m[0]) for m in IMPORTS.finditer(source)]
    if len(BEGIN.findall(source)) != len(found):
        raise ValueError("Malformed focus import block")
    names = [name for name, _, _ in found]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate focus import block: " + ", ".join(sorted({n for n in names if names.count(n) > 1})))
    return found


def foreign_import_blocks(path, own=()):
    """Blocks in an existing wrapper that its owner generator does not write."""
    path = Path(path)
    if not path.exists():
        return []
    return [text for name, _, text in import_blocks(path.read_text(encoding="utf-8-sig")) if name not in own]


def tree_close(text):
    """Index of the first focus_tree's closing brace, ignoring comments and strings."""
    masked = re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*', lambda m: " " * len(m[0]), text)
    match = re.search(r"\bfocus_tree\s*=\s*\{", masked)
    if not match:
        raise ValueError("Missing focus tree")
    depth, cursor = 1, match.end()
    while depth and cursor < len(masked):
        depth += {"{": 1, "}": -1}.get(masked[cursor], 0)
        cursor += 1
    if depth:
        raise ValueError("Unbalanced focus tree")
    return cursor - 1


def reinsert(text, blocks):
    """Insert blocks before the campaign imports, or before the tree's closing brace."""
    if not blocks:
        return text
    text = normal(text)
    names = {IMPORTS.match(block)[1] for block in blocks}
    for name, _, old in import_blocks(text):
        if name in names:
            text = text.replace(old, "", 1)
    at = text.find(CAMPAIGN_ANCHOR)
    if at < 0:
        at = tree_close(text)
    joined = "".join(blocks)
    if at and text[at - 1] != "\n":
        joined = "\n" + joined
    return text[:at] + joined + text[at:]


def import_block(name, ids):
    ids = list(ids)
    if not re.fullmatch(r"[A-Z][A-Z ]*", name) or name == CAMPAIGNS:
        raise ValueError("Invalid import block name: " + name)
    if not ids or len(set(ids)) != len(ids) or not all(re.fullmatch(r"\w+", i) for i in ids):
        raise ValueError("Import block needs unique focus IDs: " + name)
    rows = "".join("\tshared_focus = %s\n" % i for i in ids)
    return "\t# BEGIN %s IMPORTS\n%s\t# END %s IMPORTS\n" % (name, rows, name)


def attach(source, name, ids):
    """Replace this package's block in place, or add it before the campaign imports."""
    source = normal(source)
    block = import_block(name, ids)
    for found, _, old in import_blocks(source):
        if found == name:
            return source.replace(old, block, 1)
    return reinsert(source, [block])


def attach_file(path, name, ids, check=False):
    """Attach to a wrapper on disk, keeping its BOM and line endings.

    Returns True when the file already matched. With check=True nothing is written.
    Re-run the wrapper's owner generator afterwards (see MARKERS and the README).
    """
    path = Path(path)
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    crlf = b"\r\n" in data
    current = normal(data.decode("utf-8-sig"))
    result = attach(current, name, ids)
    if result == current:
        return True
    if not check:
        out = result.replace("\n", "\r\n") if crlf else result
        path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + out.encode("utf-8"))
    return False


def shared_nodes(ids):
    """Resolve shared_focus definitions by ID across every national focus file."""
    from usea_expansion.script import parse, get
    wanted, nodes = set(ids), {}
    for path in sorted(FOCUS.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig")
        if not any("id = " + i in text for i in wanted - set(nodes)):
            continue
        for kind, _, node in parse(text):
            if kind == "shared_focus" and isinstance(node, list) and get(node, "id") in wanted:
                nodes[get(node, "id")] = node
    missing = wanted - set(nodes)
    if missing:
        raise ValueError("Imported shared focuses are not defined: " + ", ".join(sorted(missing)))
    return nodes


def _screen():
    spec = importlib.util.spec_from_file_location("ulysses_focus_screen", ROOT / "tools/Test-FocusScreenRepairs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tree_positions():
    """Every tree's resolved node positions, as checked by Test-FocusScreenRepairs."""
    return _screen().resolved_tree_positions()


def band_violations(positions, ids, xmin, xmax, ymin=0):
    """IDs placed outside a package's allowed band, or missing from the tree."""
    return sorted(i for i in ids if i not in positions or not (xmin <= positions[i][0] <= xmax and positions[i][1] >= ymin))


def title_fits(text, width=147, lines=3):
    screen = _screen()
    _, advances = screen.font_metrics()
    return len(screen.wrapped_lines(text, width, advances)) <= lines


def glyph_library():
    """The shared Ulysses glyph library, loaded read-only.

    Use glyph(image, subject, (x, y, w, h), colour) and the NAVY/EDGE/WHITE/CYAN/GOLD
    constants. Never call its save(), build_focuses() or main().
    """
    spec = importlib.util.spec_from_file_location("ulysses_depth_glyphs", ROOT / "tools/usea_expansion/build_art.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUBJECTS = frozenset({
    "industry", "logistics", "air", "navy", "carrier", "submarine", "assembly", "ballot", "science", "radar",
    "diplomacy", "economy", "civil", "rebuild", "communications", "training", "command", "meteor", "missile",
    "gate", "refugees", "medical", "shelter", "rail", "tools", "telescope", "satellite", "document", "scales",
    "peace", "fishing", "runway", "bridge", "medal", "security",
})


def encoded(image, format="DDS"):
    stream = io.BytesIO()
    image.save(stream, format=format)
    return stream.getvalue()


def focus_sprites(package, ident):
    """Sprite lines for one focus icon; the shine reuses the same mod texture."""
    texture = "gfx/AC_usea_depth/%s/focus/%s.dds" % (package, ident)
    name = "GFX_ac_ud_focus_" + ident
    return [
        'spriteType = { name = "%s" texturefile = "%s" }' % (name, texture),
        'spriteType = { name = "%s_shine" texturefile = "%s" }' % (name, texture),
    ]


# Long-form ("TNO-style") event text: several paragraphs and a labelled source line.
EVENT_MIN_WORDS = 180
EVENT_MIN_PARAGRAPHS = 3
LAYERS = ("Official", "Mod provenance", "Provisional gameplay")


def event_text(paragraphs, layer, citation=""):
    if layer not in LAYERS:
        raise ValueError("Unknown source layer: " + layer)
    note = layer + (": " + citation if citation else "") + "."
    return "\n\n".join(p.strip() for p in paragraphs) + "\n\n" + note


def event_problems(text):
    """Reasons an event body is too short for the package's long-form rule."""
    body = text.rsplit("\n\n", 1)[0] if any(text.rsplit("\n\n", 1)[-1].startswith(layer) for layer in LAYERS) else text
    problems = []
    paragraphs = [p for p in body.split("\n\n") if p.strip()]
    if len(paragraphs) < EVENT_MIN_PARAGRAPHS:
        problems.append("fewer than %d paragraphs" % EVENT_MIN_PARAGRAPHS)
    if len(body.split()) < EVENT_MIN_WORDS:
        problems.append("fewer than %d words" % EVENT_MIN_WORDS)
    if not any(text.rsplit("\n\n", 1)[-1].startswith(layer) for layer in LAYERS):
        problems.append("no source-layer line")
    if any(c in text for c in "\u201c\u201d\u2018\u2019"):
        problems.append("curly quotes")
    return problems


def office_character(tag, slug, sub_ideology, portrait):
    """An unnamed office leader card for a provisional government, e.g. ERU_ud_crown_council_office."""
    ident = "%s_ud_%s_office" % (tag, slug)
    body = (
        "%s = {\n name = %s\n portraits = { civilian = { large = \"%s\" } }\n"
        " country_leader = { ideology = %s traits = { } expire = \"2066.1.1.1\" desc = %s_desc }\n}\n"
    ) % (ident, ident, portrait, sub_ideology, ident)
    return ident, body


def regime_effect(package, slug, ruling_party, character, sub_ideology, elections_allowed=False, popularities=None):
    """The only allowed form of a government change: ac_ud_<package>_regime_<slug>."""
    name = "ac_ud_%s_regime_%s" % (package, slug)
    lines = ["set_politics = { ruling_party = %s elections_allowed = %s }" % (ruling_party, "yes" if elections_allowed else "no")]
    if popularities:
        lines.append("set_popularities = { %s }" % " ".join("%s = %d" % item for item in popularities.items()))
    lines.append("if = { limit = { NOT = { has_character = %s } } recruit_character = %s }" % (character, character))
    lines.append("promote_character = { character = %s ideology = %s }" % (character, sub_ideology))
    return name, name + " = {\n\t" + "\n\t".join(lines) + "\n}\n"


BANNED = (
    "transfer_state", "annex_country", "declare_war_on", "add_state_core", "remove_state_core", "set_owner",
    "set_state_controller", "create_wargoal", "add_to_faction", "remove_from_faction", "dismantle_faction",
    "set_global_flag = ac_ucw_", "clr_global_flag = ac_ucw_", "launch_nuke",
)


def banned_uses(text):
    return [token for token in BANNED if token in text]


def political_violations(effects_text):
    """set_politics/set_popularities outside ac_ud_*_regime_* effects."""
    problems = []
    depth, owner = 0, None
    for line in normal(effects_text).split("\n"):
        code = line.split("#", 1)[0]
        if depth == 0:
            match = re.match(r"\s*(\w+)\s*=\s*\{", code)
            owner = match[1] if match else None
        if re.search(r"\bset_(politics|popularities)\b", code) and not (owner and re.fullmatch(r"ac_ud_\w+_regime_\w+", owner)):
            problems.append(owner or "<top level>")
        depth += code.count("{") - code.count("}")
    return problems
