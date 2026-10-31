"""Bound the engine-owned country history text without changing other controls.

The original control is a captured compatibility contract. Ordinary generation
and --check require no installed game. The historical frontend fingerprint is
verified after restoring only this exact, validated intentional transformation.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
TARGET = MOD / 'interface/frontendgamesetupview.gui'
CONTRACT = HERE / 'briefing_control.json'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import get, parse, render, setv, walk, xy


def control_span(text):
    starts = list(re.finditer(r'\binstantTextBoxType\s*=\s*\{\s*name\s*=\s*"history"', text, re.I))
    if len(starts) != 1:
        raise ValueError('Expected exactly one engine country-selection history control')
    start = starts[0].start()
    depth = 0
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]', text[start:]):
        value = token[0]
        if value == '{':
            depth += 1
        elif value == '}':
            depth -= 1
            if depth == 0:
                return start, start + token.end()
    raise ValueError('Unclosed country-selection history control')


def country_window(text):
    matches = [node for kind, node in walk(parse(text))
               if kind.lower() == 'containerwindowtype'
               and get(node, 'name', '').strip('"') == 'gamesetup_interesting_countries_window']
    if len(matches) != 1:
        raise ValueError('Country-selection window is missing or duplicated')
    window = matches[0]
    controls = {get(node, 'name', '').strip('"'): node for _, node in walk(window)}
    required = ('history', 'history_title', 'back_button', 'select_button',
                'minor_country_leader', 'countries_mini')
    for name in required:
        if name not in controls:
            raise ValueError('Missing required country-selection control: ' + name)
    if get(controls['select_button'], 'shortcut', '').strip('"') != 'RETURN':
        raise ValueError('Country-selection Return shortcut changed')
    if get(controls['back_button'], 'shortcut', '').strip('"') != 'ESCAPE':
        raise ValueError('Country-selection Escape shortcut changed')
    return window, controls


def repaired_node(contract):
    row = copy.deepcopy(contract['original_node'])
    node = row[2]
    setv(node, 'position', xy(35, 485))
    setv(node, 'maxHeight', '145')
    setv(node, 'scrollbarType', '"ac_exp_standardtext_slider"')
    return row


def validate_bounds(text, contract):
    window, controls = country_window(text)
    start, end = control_span(text)
    actual = parse(text[start:end])[0]
    if actual != repaired_node(contract):
        raise ValueError('Country history differs from the bounded scrolling contract')
    history = controls['history']
    title = controls['history_title']
    title_bottom = int(get(get(title, 'position'), 'y')) + int(get(title, 'maxHeight'))
    top = int(get(get(history, 'position'), 'y'))
    bottom = top + int(get(history, 'maxHeight'))
    window_height = int(get(get(window, 'size'), 'height'))
    buttons_top = min(window_height + int(get(get(controls[name], 'position'), 'y'))
                      for name in ('back_button', 'select_button'))
    if not title_bottom < top < bottom < buttons_top:
        raise ValueError('Country history overlaps its heading or navigation buttons')
    if get(history, 'maxWidth') != '380':
        raise ValueError('Country history width changed')
    sliders = [(kind, node) for kind, node in walk(parse((MOD / 'interface/nationalfocusview.gui').read_text(encoding='utf-8-sig')))
               if kind.lower() == 'scrollbartype' and get(node, 'name', '').strip('"') == 'ac_exp_standardtext_slider']
    if len(sliders) != 1:
        raise ValueError('Required authored text scrollbar is missing or duplicated')
    return start, end


def normalize_for_fingerprint(text):
    """Restore only the known repair after validating its complete effective node."""
    contract = json.loads(CONTRACT.read_text())
    start, end = validate_bounds(text, contract)
    return text[:start] + contract['original_raw'] + text[end:]


def build(text):
    contract = json.loads(CONTRACT.read_text())
    country_window(text)
    start, end = control_span(text)
    current = parse(text[start:end])[0]
    expected = repaired_node(contract)
    if current not in (contract['original_node'], expected):
        raise ValueError('Refusing to overwrite an unrecognised history-control change')
    # Keep the surrounding file byte-for-byte; only this control is rendered.
    replacement = render([expected], depth=2).lstrip('\t')
    result = text[:start] + replacement + text[end:]
    validate_bounds(result, contract)
    return result


def capture(text):
    if CONTRACT.exists():
        raise ValueError('The original history contract already exists; do not recapture a repair')
    country_window(text)
    start, end = control_span(text)
    original = parse(text[start:end])[0]
    node = original[2]
    if (get(get(node, 'position'), 'x'), get(get(node, 'position'), 'y'),
            get(node, 'maxWidth'), get(node, 'maxHeight')) != ('35', '455', '380', '30'):
        raise ValueError('The inherited history geometry is not the expected original')
    if get(node, 'scrollbarType') is not None:
        raise ValueError('The original country history unexpectedly has a scrollbar')
    contract = dict(schema=1, source_commit='cf8fec41abe5080b1af66eb86189b35c7af522f6',
                    source_file='mod/2985041246/interface/frontendgamesetupview.gui',
                    parent='gamesetup_interesting_countries_window', control='history',
                    original_raw=text[start:end], original_node=original,
                    deliberate_changes=dict(position=dict(x=35, y=485), maxHeight=145,
                                            scrollbarType='ac_exp_standardtext_slider'),
                    bounds=dict(heading_bottom=480, narrative_top=485,
                                narrative_bottom=630, navigation_top=665))
    CONTRACT.write_text(json.dumps(contract, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture-contract', action='store_true',
                        help='One-time capture of the inherited control before the repair')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = TARGET.read_text(encoding='utf-8-sig')
    if args.capture_contract:
        capture(text)
    result = build(text)
    if args.check:
        if result != text:
            raise SystemExit('Country-selection brief GUI differs from authoring source')
    else:
        TARGET.write_text(result, encoding='utf-8')
    print('Country-selection briefs: 380×145 scrolling area, y485–630; heading and navigation remain clear.')


if __name__ == '__main__':
    main()
