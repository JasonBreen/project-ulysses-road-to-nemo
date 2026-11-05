"""Focus-tree layout geometry shared by generators, tests and review images.

Positions are resolved from the shipped focus files; the node footprint and the
continuous-focus panel are read from interface/nationalfocusview.gui and the
sprite records in ui_assets.json. Everything here is offline geometry, not a
native rendering claim.
"""
import json
from collections import defaultdict
from pathlib import Path

try:
    from script import parse, get, walk
except ImportError:  # imported as usea_expansion.focus_layout
    from .script import parse, get, walk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
GAP = 3          # focus columns between the rightmost top-band node and the panel
CLEARANCE = 32   # minimum pixels between the panel and any node footprint


def _named(tree, name):
    return next(node for _, node in walk(tree) if get(node, 'name', '').strip('"') == name)


def _point(node):
    position = get(node, 'position')
    return int(get(position, 'x')), int(get(position, 'y'))


def _size(node):
    size = get(node, 'size')
    return int(get(size, 'width')), int(get(size, 'height'))


def gui_geometry(mod=MOD):
    """Return the pitch, the panel size and the node footprint in pixels.

    The footprint is the union of every national_focus_item child whose size is
    known: the centred 96-px icon, the caption frame, the glows, the historical
    marker and the viewing-flag frame. It is relative to the node origin
    (x * pitch_x, y * pitch_y) in the same canvas as continuous_focus_position.
    """
    gui = parse((mod / 'interface/nationalfocusview.gui').read_text(encoding='utf-8-sig'))
    specs = {row['name']: row for row in json.loads((HERE / 'ui_assets.json').read_text())}
    pitch = _point(_named(gui, 'focus_spacing'))
    panel = _size(_named(gui, 'continuous_focus_window'))
    item = _named(gui, 'national_focus_item')
    item_w, item_h = _size(item)
    rects = []
    for kind, _, child in item:
        if not isinstance(child, list) or not get(child, 'name'):
            continue
        name = get(child, 'name').strip('"')
        x, y = _point(child)
        if name == 'symbol':
            # centerposition: the 96-px icon is centred on the item, then offset.
            top = item_h // 2 + y - 48
            left = item_w // 2 - 48
            rects.append((left, top, left + 96, top + 96))
            continue
        if name == 'name':
            rects.append((x, y, x + int(get(child, 'maxWidth')), y + int(get(child, 'maxHeight'))))
            continue
        sprite = (get(child, 'spriteType') or get(child, 'quadTextureSprite') or '').strip('"')
        spec = specs.get(sprite)
        if spec:
            rects.append((x, y, x + spec['width'] // spec['frames'], y + spec['height']))
    left = min(r[0] for r in rects); top = min(r[1] for r in rects)
    right = max(r[2] for r in rects); bottom = max(r[3] for r in rects)
    return {'pitch': pitch, 'panel': panel, 'footprint': (left, top, right, bottom)}


def node_rect(x, y, geometry):
    (px, py), (left, top, right, bottom) = geometry['pitch'], geometry['footprint']
    return (x * px + left, y * py + top, x * px + right, y * py + bottom)


def panel_rect(position, geometry):
    width, height = geometry['panel']
    return (position[0], position[1], position[0] + width, position[1] + height)


def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def band_nodes(positions, geometry, top=16):
    """Nodes whose footprint meets the horizontal band the panel occupies."""
    band = (float('-inf'), top, float('inf'), top + geometry['panel'][1])
    return {ident: xy for ident, xy in positions.items() if intersects(node_rect(*xy, geometry), band)}


def panel_position(positions, geometry=None, gap=GAP, top=16):
    """Top-aligned beside the first rows: rows appended below never move it."""
    geometry = geometry or gui_geometry()
    band = band_nodes(positions, geometry, top)
    right = max(x for x, _ in band.values())
    return int((right + gap) * geometry['pitch'][0]), top


def overlaps(positions, position, geometry=None):
    """Nodes whose footprint intersects the declared panel."""
    geometry = geometry or gui_geometry()
    panel = panel_rect(position, geometry)
    return sorted(ident for ident, xy in positions.items() if intersects(node_rect(*xy, geometry), panel))


def clearance(positions, position, geometry=None):
    """Horizontal pixels between the panel and the nearest band node to its left."""
    geometry = geometry or gui_geometry()
    band = band_nodes(positions, geometry, position[1])
    lefts = [node_rect(*xy, geometry)[2] for xy in band.values() if node_rect(*xy, geometry)[2] <= position[0]]
    return position[0] - max(lefts) if lefts else None


def tree_definitions(mod=MOD):
    """Each focus_tree's id, file and declared continuous_focus_position."""
    result = {}
    for path in sorted((mod / 'common/national_focus').glob('*.txt'), key=lambda p: p.as_posix()):
        for kind, _, node in parse(path.read_text(encoding='utf-8-sig')):
            if kind != 'focus_tree':
                continue
            position = get(node, 'continuous_focus_position')
            declared = (int(get(position, 'x')), int(get(position, 'y'))) if position else None
            result[get(node, 'id')] = {'file': path.relative_to(mod).as_posix(), 'panel': declared}
    return result


def resolved_tree_positions(mod=MOD):
    """Resolve explicit imports, their shared descendants and relative anchors.

    Descendant closure is deliberately conservative: it also checks shared
    children inherited from imported roots, even if a particular branch is not
    currently available. Availability does not hide a focus caption.
    """
    shared = {}; trees = []; children = defaultdict(set)
    for path in sorted((mod / 'common/national_focus').glob('*.txt'), key=lambda p: p.as_posix()):
        for kind, _, node in parse(path.read_text(encoding='utf-8-sig')):
            if kind == 'shared_focus' and isinstance(node, list):
                shared[get(node, 'id')] = node
            if kind == 'focus_tree':
                trees.append(node)
    for ident, node in shared.items():
        for kind, _, child in node:
            if kind == 'prerequisite':
                for key, _, value in child:
                    if key == 'focus':
                        children[value].add(ident)
    result = {}
    for tree in trees:
        ident = get(tree, 'id')
        nodes = {get(node, 'id'): node for kind, _, node in tree if kind == 'focus' and isinstance(node, list)}
        pending = [node for kind, _, node in tree if kind == 'shared_focus' and isinstance(node, str)]
        while pending:
            ref = pending.pop()
            if ref in nodes:
                continue
            if ref not in shared:
                raise AssertionError('Missing shared focus import: ' + ident + ':' + ref)
            nodes[ref] = shared[ref]
            pending.extend(children[ref])
        positions = {}

        def resolve(ref, stack=()):
            if ref in positions:
                return positions[ref]
            if ref in stack:
                raise AssertionError('Cyclic relative focus position: ' + str(stack + (ref,)))
            node = nodes.get(ref, shared.get(ref))
            if node is None:
                raise AssertionError('Missing relative focus anchor: ' + ident + ':' + ref)
            x = float(get(node, 'x', '0')); y = float(get(node, 'y', '0'))
            parent = get(node, 'relative_position_id')
            if parent:
                px, py = resolve(parent, stack + (ref,)); x += px; y += py
            positions[ref] = (x, y)
            return x, y
        result[ident] = {ref: resolve(ref) for ref in nodes}
    return result
