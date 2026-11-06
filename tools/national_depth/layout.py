"""Compact, visible placement for a bespoke tree.

Each branch is a contiguous lane: its focuses sit in tiers by prerequisite depth,
two columns apart (the 96 px pitch is narrower than a 147 px caption), ordered
under their parents. Lanes are packed left to right within the country's column
limit and wrap into bands top to bottom. The shared 36-focus institutional block
keeps its own coordinates (columns 0-20, rows 0-10), so the country's lanes start
at row 12 and the tree's top band stays narrow enough for the continuous-focus
panel to sit inside the primary view.
"""

START_ROW = 12
GAP = 1          # an extra empty column between lanes


def tiers(branch):
    keys = [f.key for f in branch.focuses]
    local = set(keys)
    depth = {}

    def level(focus):
        if focus.key in depth:
            return depth[focus.key]
        parents = [p for p in (*focus.after, *focus.after_any) if p in local]
        depth[focus.key] = 0 if not parents else 1 + max(level(by_key[p]) for p in parents)
        return depth[focus.key]
    by_key = {f.key: f for f in branch.focuses}
    for focus in branch.focuses:
        level(focus)
    rows = {}
    for focus in branch.focuses:
        rows.setdefault(depth[focus.key], []).append(focus)
    return [rows[i] for i in sorted(rows)]


def place(branches, max_columns, start_row=START_ROW):
    """Return {focus key: (x, y)} and the lane boxes [(branch key, x0, y0, x1, y1)]."""
    positions, lanes = {}, []
    cursor, band_y, band_height = 0, start_row, 0
    for branch in branches:
        rows = tiers(branch)
        widest = max(len(r) for r in rows)
        width = 2 * widest - 1
        if width - 1 > max_columns:
            raise ValueError('Branch %s has %d focuses in one tier; at most %d fit' % (branch.key, widest, max_columns // 2 + 1))
        if cursor and cursor + width - 1 > max_columns:
            band_y += band_height + 1
            cursor, band_height = 0, 0
        for depth, row in enumerate(rows):
            def anchor(focus):
                parents = [positions[p][0] for p in (*focus.after, *focus.after_any) if p in positions]
                return sum(parents) / len(parents) if parents else 0
            if depth:
                row = sorted(row, key=lambda f: (anchor(f), [x.key for x in branch.focuses].index(f.key)))
            offset = (width - (2 * len(row) - 1)) // 2
            for i, focus in enumerate(row):
                positions[focus.key] = (cursor + offset + 2 * i, band_y + depth)
        lanes.append((branch.key, cursor, band_y, cursor + width - 1, band_y + len(rows) - 1))
        band_height = max(band_height, len(rows))
        cursor += width + 1 + GAP
    return positions, lanes
