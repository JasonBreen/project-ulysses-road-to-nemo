"""Generate the native playtest case list for the wiring repairs and the national-depth trees.

    python -B tools/wiring/playtest_cases.py           # write docs/native_evidence/wiring_depth/cases.csv
    python -B tools/wiring/playtest_cases.py --check   # fail if the list is stale or names a missing id

The cases are a plan for a native run that the repository owner approves and runs by hand
(docs/PLAYTEST_WIRING_AND_DEPTH.md). Every case starts NOT_RUN; this script never launches the
game, and a static check never counts as a native result. Each case names the ids it exercises,
and --check fails when one of them no longer exists in the mod, so the packet keeps in step with
the content as waves land.
"""
import argparse
import csv
import io
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
OUT = ROOT / 'docs/native_evidence/wiring_depth/cases.csv'
sys.path.insert(0, str(ROOT / 'tools/national_depth'))

# (case id, group, route, what to do and check, ids that must exist in the mod)
FIXED = [
    ('preflight-candidate', 'Preflight', 'static',
     'Record the candidate SHA, payload hash and descriptor checksum; HOI4 build and DLC; static suite result with Linux-only failures listed apart.', ()),
    ('preflight-isolation', 'Preflight', 'static',
     'tools/Test-NativeLaunchConfig.ps1 passes for the isolated profile; before/after hashes of normal saves and configs recorded.', ()),
    ('preflight-control-log', 'Preflight', 'native',
     'Launch a no-mod control to the main menu in the same copied engine; keep its error.log for attribution.', ()),
    ('launch-1991', 'Launch', 'natural',
     'Start 1 January 1991; error.log has no new parser, localisation or missing-sprite lines from national-depth, Usea Depth, world-campaign or wiring-repair files compared with the control.', ()),
    ('lobby-restyle-geometry', 'Launch', 'natural',
     'Country selection at 1920x1080 and the owner UI scale: restyled lobby tiles render, the responsive geometry holds, no control is clipped.',
     ('GFX_ac_briefing_lobby_window', 'GFX_ac_briefing_country_entry')),
    ('era-gates-refresh', 'Focus screens', 'natural',
     'As ERU from 1991: the campaign lane is hidden at start and appears after 1 January 2000 once the weekly layout refresh runs.',
     ('ERU_camp_0_register',)),
    ('wire-release-network-hidden', 'Wiring repairs', 'forced',
     'Release AWW and SER (separate saves): the Restore owned domestic connections decision never shows; no political power is spent.',
     ('ac_release_AWW_repair_network', 'ac_release_SER_repair_network')),
    ('wire-sapin-demobilise', 'Wiring repairs', 'natural',
     'As SAP in a defensive war, mobilise one state national guard; after peace, Demobilize The Royal Army appears and removes the units.',
     ('SAP_mobilize_state_national_guard', 'SAP_demobilize', 'SAP_has_mobilized')),
    ('wire-sapin-chain-ends', 'Wiring repairs', 'forced',
     'Fire sapin_civil_war.1 in a diagnostic save: sap_political_crisis_over is set (list_flags) and no further sapin_politics.3 parliament events fire.',
     ('sapin_civil_war.1', 'sapin_civil_war.2', 'sap_political_crisis_over')),
    ('wire-sapin-civil-war-category', 'Wiring repairs', 'forced',
     'During the Sapin civil war the civil-war category is visible and the state recruitment decision can target a controlled core state.',
     ('SAP_civil_war', 'SAP_civil_war_recruitment')),
    ('wire-hoffnung-achievement', 'Wiring repairs', 'forced',
     'As BLK during Wacht am Wal with Excalibur land strikes unlocked, strike Hoffnung (state 602): used_excalibur_on_hoffnung_achievement is set.',
     ('BLK_fire_excalibur', 'used_excalibur_on_hoffnung_achievement', 'wacht_am_wal_is_happening')),
    ('wire-excalibur-aa', 'Wiring repairs', 'forced',
     'BLK_excalibur_fire_aa still starts the 30-day BLK_excalibur_fire_during_aa mission and then the cooling mission.',
     ('BLK_excalibur_fire_aa', 'BLK_excalibur_fire_during_aa', 'BLK_excalibur_cooling_after_aa')),
    ('wire-dead-idea-references', 'Wiring repairs', 'forced',
     'Complete BLK_south_belka_munitions_monopoly and the Sapin bomber university focus: no error.log line about an unknown idea.',
     ('BLK_south_belka_munitions_monopoly',)),
    ('wire-live-event-text', 'Wiring repairs', 'forced',
     'belka.8, belka.9, belka_dlp.5, belka_dlp_coup.8 (option b), osea.80 and ustio.19 show readable tooltips and option text, not raw keys.',
     ('belka.8', 'belka.9', 'belka_dlp.5', 'belka_dlp_coup.8', 'osea.80', 'ustio.19')),
    ('belkan-defeat-flag', 'Wiring repairs', 'natural',
     'On the natural defeat route (#70 O3), belka_dlp_lost.7 sets belka_lost_belkan_war and ac_continuation.1 hands off once.',
     ('belka_dlp_lost.7', 'belka_lost_belkan_war', 'ac_continuation.1')),
    ('ai-observer-1991-2004', 'Long run', 'natural',
     'Observer from 1991 to 2004: AI completes national-depth focuses, never takes regime focuses, economies stay bounded, the 2003 Usean war starts; record days per second and save size against the parent commit.', ()),
    ('save-reload-checkpoints', 'Long run', 'natural',
     'Save and reload at 1991 start, 1992, 1996, 2000 and 2004; flags, ideas and focus progress persist.', ()),
]


def mod_text():
    parts = []
    for folder in ('common', 'events', 'interface', 'history'):
        for path in sorted((MOD / folder).rglob('*')):
            if path.suffix in ('.txt', '.gfx', '.gui'):
                parts.append(path.read_text(encoding='utf-8-sig', errors='replace'))
    return '\n'.join(parts)


def depth_cases():
    """Cases for every compiled national-depth tree, from its spec."""
    import package
    from compile import names
    rows = []
    for path in package.discover():
        module = package.load(path)
        c = module.COUNTRY
        n = names(c)
        prefix = '%s_%s_' % (c.tag, n['infix'])
        regime = [f for b in module.BRANCHES for f in b.focuses if any(type(r).__name__ == 'Regime' for r in f.reward)]
        rows.append(('depth-%s-screen' % c.tag.lower(), 'National depth', 'natural',
                     '%s focus screen at 1920x1080 and the owner UI scale: no node off screen, the continuous panel clear, '
                     'icons and three-line titles fit; compare with docs/evidence/national-depth/%s.png.' % (c.name, c.tag.lower()),
                     (n['tree'],)))
        rows.append(('depth-%s-play' % c.tag.lower(), 'National depth', 'natural',
                     '%s 1991-1996: take one regime path (%s) and one exclusive economic path; ideas apply, buildings land in '
                     'own states, no focus stalls.' % (c.name, prefix + regime[0].key if regime else 'none'),
                     tuple(prefix + f.key for f in regime[:1])))
        for e in module.EVENTS:
            index = [x.key for x in module.EVENTS].index(e.key) + 1
            ident = '%s.%d' % (n['base'], index)
            rows.append(('depth-%s-event-%d' % (c.tag.lower(), index), 'National depth', 'natural',
                         '%s fires once with readable text and its options apply (%s).' % (ident, e.title), (ident,)))
        if getattr(module, 'DECISIONS', ()):
            rows.append(('depth-%s-decisions' % c.tag.lower(), 'National depth', 'natural',
                         '%s decisions appear only for %s, respect cost and cooldown, and once-only ones vanish after use.' % (
                             c.name, c.tag), (n['base'] + '_decisions',)))
    return rows


def usea_cases():
    """Main's Usea Depth content: one case per adopt-decision file and one per import marker block."""
    rows = []
    for path in sorted((MOD / 'common/decisions').glob('ac_ud_*.txt')):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        loaders = re.findall(r'load_focus_tree = \{ tree = (ac_ud_(\w{3})_tree)', text)
        if loaders:
            tags = ', '.join(t.upper() for _, t in loaders)
            rows.append(('usea-adopt-%s' % path.stem.replace('ac_ud_', ''), 'Usea Depth', 'natural',
                         'For one of %s: once the previous tree is idle, the adopt decision loads the national tree with completed '
                         'focuses kept, and the screen fits.' % tags, (loaders[0][0],)))
    blocks = {}
    for path in sorted((MOD / 'common/national_focus').glob('*.txt')):
        for name in re.findall(r'# BEGIN (USEA DEPTH [A-Z ]+?) IMPORTS', path.read_text(encoding='utf-8-sig', errors='replace')):
            blocks.setdefault(name, []).append(path.stem)
    for name, files in sorted(blocks.items()):
        slug = name.lower().replace('usea depth ', '').replace(' ', '-')
        rows.append(('usea-imports-%s' % slug, 'Usea Depth', 'natural',
                     'The %s branches appear in %s at their opening date and none overlaps the inherited tree or panel.' % (
                         name.title(), ', '.join(files)), ()))
    return rows


def cases():
    text = mod_text()
    rows = FIXED[:4] + FIXED[4:6] + usea_cases() + depth_cases() + FIXED[6:]
    missing = []
    for case, _, _, _, ids in rows:
        for ident in ids:
            if not re.search(r'(?<![\w.])' + re.escape(ident) + r'(?![\w])', text):
                missing.append('%s: %s' % (case, ident))
    if missing:
        raise SystemExit('Playtest cases name ids missing from the mod:\n' + '\n'.join(missing))
    out = io.StringIO()
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(('Case', 'Group', 'Route', 'Status', 'Evidence', 'Notes'))
    for case, group, route, note, _ in rows:
        writer.writerow((case, group, route, 'NOT_RUN', '', note))
    return out.getvalue(), len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text, count = cases()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding='utf-8').replace('\r\n', '\n') != text:
            raise SystemExit('Playtest case list is stale; run python -B tools/wiring/playtest_cases.py')
        print('Playtest cases: %d consistent (all NOT_RUN until a native run is approved)' % count)
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding='utf-8', newline='\n')
    print('Playtest cases: %d written' % count)


if __name__ == '__main__':
    main()
