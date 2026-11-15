"""Bounded grand-doctrine reference repair for the observed HOI4 1.19.4.2 schema.

These are technical identifiers from installed common/doctrines/grand_doctrines,
not technology IDs or new gameplay choices. Captured source inputs stay immutable.
"""
from pathlib import Path
import argparse
import re

FOLDERS = {
    'new_mobile_warfare': 'land', 'superior_firepower': 'land',
    'grand_battleplan': 'land', 'mass_assault': 'land',
    'new_fleet_in_being': 'naval', 'new_convoy_raiding': 'naval',
    'new_base_strike': 'naval', 'new_strategic_destruction': 'air',
    'new_battlefield_support': 'air', 'new_operational_integrity': 'air',
    'special_forces_quantity': 'special_forces',
    'special_forces_quality': 'special_forces',
}
REPLACEMENTS = {
    'mobile_warfare': 'new_mobile_warfare',
    'new_superior_firepower': 'superior_firepower',
    'new_grand_battleplan': 'grand_battleplan',
    'new_mass_assault': 'mass_assault',
    'fleet_in_being': 'new_fleet_in_being',
    'trade_interdiction': 'new_convoy_raiding',
    'convoy_raiding': 'new_convoy_raiding',
    'base_strike': 'new_base_strike',
    'strategic_destruction': 'new_strategic_destruction',
    'battlefield_support': 'new_battlefield_support',
    'operational_integrity': 'new_operational_integrity',
}
DEFAULTS = ('set_grand_doctrine = superior_firepower\n'
            'set_grand_doctrine = new_fleet_in_being\n'
            'set_grand_doctrine = new_operational_integrity\n')
# Consume strings/comments first, so only real effect assignments can change.
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\n]*|'
                    r'\bset_grand_doctrine\s*=\s*(?P<ident>\w+)\b')


def normalize(text):
    def replace(match):
        ident = match.group('ident')
        if ident not in REPLACEMENTS:
            return match.group(0)
        return match.group(0)[:-len(ident)] + REPLACEMENTS[ident]
    return TOKENS.sub(replace, text)


def invalid_references(mod):
    errors = []
    for path in Path(mod).rglob('*.txt'):
        for match in TOKENS.finditer(path.read_text(encoding='utf-8-sig')):
            ident = match.group('ident')
            if ident and ident not in FOLDERS:
                errors.append(f'{path.relative_to(mod)}: invalid grand doctrine {ident}')
    return errors


def verify_reference(reference):
    actual = {}
    directory = Path(reference) / 'common/doctrines/grand_doctrines'
    for path in directory.glob('*.txt'):
        # Read declaration headers only; native bodies also contain template
        # syntax outside the small lossless parser's supported script subset.
        headers = re.findall(r'(?m)^(\w+)\s*=\s*\{\s*\n\s*folder\s*=\s*(\w+)',
                             path.read_text(encoding='utf-8-sig'))
        actual.update(headers)
    errors = [f'Installed doctrine {ident}: expected folder {folder}, got {actual.get(ident)}'
              for ident, folder in FOLDERS.items() if actual.get(ident) != folder]
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mod-root', type=Path, required=True)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.reference:
        errors = verify_reference(args.reference)
        if errors:
            raise SystemExit('\n'.join(errors))
    changed = []
    if args.write:
        for path in (args.mod_root / 'history/countries').glob('*.txt'):
            raw = path.read_bytes()
            revised = normalize(raw.decode('utf-8')).encode('utf-8')
            if revised != raw:
                path.write_bytes(revised)
                changed.append(path.name)
    errors = invalid_references(args.mod_root)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Grand-doctrine references valid; {len(changed)} histories repaired (static).')


if __name__ == '__main__':
    main()
