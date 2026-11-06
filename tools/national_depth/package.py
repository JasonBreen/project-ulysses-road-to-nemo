"""Build or check every bespoke country tree.

Specs live in two roots:
  tools/usea_depth/<package>/countries/<TAG>.py    Usean countries (IDs <TAG>_ud_*)
  tools/world_depth/<tag>/content.py               every other country (IDs <TAG>_wd_*)

    python -B tools/national_depth/package.py            # write mod files, budgets and asset manifests
    python -B tools/national_depth/package.py --check    # compare without writing (DDS by decoded pixels)
    python -B tools/national_depth/package.py --only CHO # one country

Every spec is linted strictly (lint.py) before anything is written.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(HERE))
import art  # noqa: E402
from compile import compile_country, names  # noqa: E402
import lint as linting  # noqa: E402


def load(path):
    path = Path(path).resolve()
    spec = importlib.util.spec_from_file_location('national_depth_spec_' + re.sub(r'\W', '_', str(path.relative_to(ROOT))), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover():
    paths = sorted((ROOT / 'tools/usea_depth').glob('*/countries/*.py'), key=lambda p: p.as_posix())
    paths += sorted((ROOT / 'tools/world_depth').glob('*/content.py'), key=lambda p: p.as_posix())
    return [p for p in paths if not p.name.startswith('_')]


def mod_focus_texts(exclude=()):
    """(title, description) of every focus already in the mod, for the similarity and title rules."""
    sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
    import focus_layout
    keys = {}
    for path in (MOD / 'localisation').rglob('*.yml'):
        for line in path.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            match = re.match(r'\s*([A-Za-z0-9_.\-]+):\d*\s*"(.*)"\s*$', line)
            if match:
                keys[match[1]] = match[2]
    focus_ids = {f for nodes in focus_layout.resolved_tree_positions().values() for f in nodes}
    return [(keys.get(f, ''), keys.get(f + '_desc', '')) for f in sorted(focus_ids)
            if not any(f.startswith(prefix) for prefix in exclude) and keys.get(f + '_desc')]


def package_dir(module, path):
    return path.parent.parent if module.COUNTRY.root == 'usea' else path.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--only')
    args = parser.parse_args()
    art.require_pinned_pillow()
    specs = [(p, load(p)) for p in discover()]
    if args.only:
        specs = [(p, m) for p, m in specs if m.COUNTRY.tag == args.only]
    own_prefixes = tuple('%s_%s_' % (m.COUNTRY.tag, names(m.COUNTRY)['infix']) for _, m in specs)
    existing = mod_focus_texts(own_prefixes)
    problems, packages, produced = [], {}, {}
    texts = {m.COUNTRY.tag: [(f.title, f.desc) for b in m.BRANCHES for f in b.focuses] for _, m in specs}
    for path, module in specs:
        tag = module.COUNTRY.tag
        folder = package_dir(module, path).name
        if module.COUNTRY.package != folder or (module.COUNTRY.root == 'usea') != ('usea_depth' in path.parts):
            raise SystemExit('%s: package %r must match its folder %r and root' % (path, module.COUNTRY.package, folder))
        if module.COUNTRY.root == 'usea' and path.stem != tag:
            raise SystemExit('%s: a Usean spec file is named after its tag' % path)
        others = existing + [row for other, rows in texts.items() if other != tag for row in rows]
        problems += linting.lint(module, others)
        outputs, budget, assets, _ = compile_country(module)
        produced.update(outputs)
        row = packages.setdefault(package_dir(module, path), {'budgets': [], 'assets': [], 'root': module.COUNTRY.root,
                                                              'package': module.COUNTRY.package})
        row['budgets'].append(budget)
        row['assets'] += assets
    if problems:
        raise SystemExit('Lint failed:\n' + '\n'.join(problems))
    stale = []
    for relative, data in sorted(produced.items()):
        target = MOD / relative
        if args.check:
            if not target.exists():
                stale.append(relative)
            elif relative.endswith('.dds'):
                if not art.same_pixels(target.read_bytes(), data):
                    stale.append(relative)
            elif target.read_bytes().replace(b'\r\n', b'\n') != data:
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    for folder, row in packages.items():
        budget = dict(package=row['package'], focuses={b['tag']: b['own_focuses'] for b in row['budgets']},
                      trees={b['tree']: b['own_focuses'] for b in row['budgets']}, events=sum(b['events'] for b in row['budgets']),
                      shared_institutional_focuses_per_tree=36, countries=row['budgets'], native_acceptance=False)
        if row['root'] == 'usea':
            budget['marker'] = None
        for name, data in (('budget.json', budget), ('assets.json', dict(schema=1, generator='tools/national_depth', pillow='11.3.0',
                                                                         assets=row['assets']))):
            text = json.dumps(data, indent=1) + '\n'
            target = folder / name
            if args.check:
                if not target.exists() or target.read_text(encoding='utf-8').replace('\r\n', '\n') != text:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.write_text(text, encoding='utf-8', newline='\n')
    if stale:
        raise SystemExit('Stale national-depth output:\n' + '\n'.join(stale[:40]))
    total = sum(b['own_focuses'] for row in packages.values() for b in row['budgets'])
    print('National depth: %d countries, %d own focuses, %d files %s' % (len(specs), total, len(produced),
                                                                         'consistent' if args.check else 'written'))


if __name__ == '__main__':
    main()
