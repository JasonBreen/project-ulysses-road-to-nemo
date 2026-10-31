"""Actual-script ledger/carry and independent bitmap/UI geometry regressions.

Decimal accounting, bitmap bounds and deepcopy reloads are offline evidence.
They do not prove HOI4 fixed-point precision, rounding, native save behavior or
rendered GUI acceptance at any resolution.
"""
import copy
from datetime import date
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]; MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools/economy_v2'), str(ROOT / 'tools/usea_expansion')]
from harness import World, Country
from script import parse, get, walk


def position(country, accrual=False):
    v = country.variables
    result = v['ac_macro_cash'] + v['ac_macro_replacement_escrow'] - v['ac_macro_debt'] - v['ac_macro_arrears']
    if accrual:
        result += (v['ac_macro_revenue_carry_milli'] - v['ac_macro_bill_carry_milli']) / 1000
    return result


def history(country):
    return {key: value for key, value in country.variables.items()
            if key.startswith(('ac_macro_history_', 'ac_macro_graph_', 'ac_macro_last_')) or key.endswith('_carry_milli')}


def dated_month(world, tag, index):
    # index0 is February1991, the first allowed settlement boundary.
    absolute = 1991 * 12 + 1 + index
    world.month(tag, absolute // 12, absolute % 12 + 1)


class Ledger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = World(); cls.base.action('on_startup')

    def world(self, tag='SNS'):
        world = copy.deepcopy(self.base)
        return world, world.countries[tag]

    def assertNear(self, first, second):
        self.assertLess(abs(first - second), D('1e-18'))

    def test_opening_has_no_fabricated_history_and_only_monthly_owner_records(self):
        world, country = self.world()
        self.assertEqual(0, country.variables['ac_macro_history_count'])
        self.assertEqual(0, country.variables['ac_macro_history_last_recorded'])
        for _ in range(3):
            world.run('ac_macro_quote', 'SNS'); world.run('ac_macro_record_ledger', 'SNS')
            world.run('ac_macro_settle_month', 'SNS'); world.action('on_startup')
        self.assertEqual(0, country.variables['ac_macro_history_count'])
        world.month('SNS')
        self.assertEqual(1, country.variables['ac_macro_history_count'])
        self.assertEqual(1, country.variables['ac_macro_history_0_sequence'])
        self.assertGreater(country.variables['ac_macro_history_0_real'], 0)
        self.assertFalse('ac_macro_ledger_authorized' in country.flags)
        saved = copy.deepcopy(country)
        world.run('ac_macro_record_ledger', 'SNS'); world.action('on_monthly', ['SNS'])
        world.action('on_startup')
        self.assertEqual(saved, country)

    def test_twelve_records_keep_actual_values_and_newest_sequence_without_zero_padding(self):
        world, country = self.world(); observed = {}
        for index in range(15):
            before = position(country, True)
            quoted = country.variables['ac_macro_real_gdp']
            dated_month(world, 'SNS', index)
            v = country.variables
            self.assertEqual(quoted, v['ac_macro_last_real_gdp'])
            self.assertNear(position(country, True) - before,
                            (v['ac_macro_last_revenue_accrued_milli'] - v['ac_macro_last_bill_accrued_milli']) / 1000)
            observed[index + 1] = {field: v[source] for field, source in {
                'real': 'ac_macro_last_real_gdp', 'revenue': 'ac_macro_last_revenue',
                'bill': 'ac_macro_last_bill', 'paid': 'ac_macro_last_paid',
                'cash': 'ac_macro_cash', 'debt': 'ac_macro_debt', 'arrears': 'ac_macro_arrears',
                'revenue_carry_milli': 'ac_macro_revenue_carry_milli',
                'bill_carry_milli': 'ac_macro_bill_carry_milli'}.items()}
            self.assertEqual(min(12, index + 1), v['ac_macro_history_count'])
        for slot in range(12):
            self.assertEqual(15 - slot, country.variables[f'ac_macro_history_{slot}_sequence'])
            for field, expected in observed[15 - slot].items():
                self.assertEqual(expected, country.variables[f'ac_macro_history_{slot}_{field}'])
            for field in ('output', 'net_positive', 'net_negative'):
                self.assertIn(country.variables[f'ac_macro_graph_{slot}_{field}'], range(1, 34))

    def test_forecast_and_every_tab_never_shift_records_or_carries(self):
        world, country = self.world(); world.month('SNS')
        logic = get(get(parse((MOD / 'common/scripted_guis/ac_macro_economy.txt').read_text()), 'scripted_gui'), 'ac_macro_economy_screen')
        effects = {key: body for key, _, body in get(logic, 'effects')}
        before = history(country); financial = position(country, True)
        for _ in range(3):
            for page in range(5):
                world.execute(effects[f'macro_tab_{page}_click'], country)
                world.execute(effects['macro_refresh_click'], country)
        self.assertEqual(before, history(country)); self.assertEqual(financial, position(country, True))

    def test_offline_reload_and_same_boundary_replay_preserve_history_carry_and_stock(self):
        world, _ = self.world()
        for index in range(4): dated_month(world, 'SNS', index)
        reloaded = copy.deepcopy(world)
        reloaded.action('on_startup')
        for candidate in (world, reloaded):
            candidate.action('on_monthly', ['SNS']); candidate.run('ac_macro_quote', 'SNS')
            dated_month(candidate, 'SNS', 4)
        self.assertEqual(world.countries['SNS'], reloaded.countries['SNS'])
        self.assertEqual(world.states, reloaded.states)

    def test_clone_clears_private_guard_and_does_not_copy_receipts_or_state_output(self):
        world, original = self.world()
        for index in range(3): dated_month(world, 'SNS', index)
        clone = copy.deepcopy(original); clone.tag = 'D01'; clone.identity = 900
        clone.flags['ac_macro_ledger_authorized'] = None
        world.countries['D01'] = clone
        state = next(state for state in world.states.values() if state.owner == 'SNS')
        output = state.variables['ac_macro_real_output']; state.owner = state.controller = 'D01'
        original_history = history(original)
        world.run('ac_macro_initialize', 'D01')
        self.assertEqual(0, clone.variables['ac_macro_history_count'])
        self.assertEqual(0, clone.variables['ac_macro_revenue_carry_milli'])
        self.assertEqual(0, clone.variables['ac_macro_bill_carry_milli'])
        self.assertNotIn('ac_macro_ledger_authorized', clone.flags)
        world.run('ac_macro_record_ledger', 'D01')
        self.assertEqual(0, clone.variables['ac_macro_history_count'])
        self.assertEqual(output, state.variables['ac_macro_real_output'])
        self.assertEqual(original_history, history(original))
        before = sum(s.variables['ac_macro_real_output'] for s in world.states.values())
        world.run('ac_macro_quote', 'SNS'); world.run('ac_macro_quote', 'D01')
        self.assertEqual(before, sum(s.variables['ac_macro_real_output'] for s in world.states.values()))
        world.month('D01', 1991, 5)
        self.assertEqual(1, clone.variables['ac_macro_history_count'])
        self.assertEqual(1, clone.variables['ac_macro_history_0_sequence'])

    def test_late_release_first_record_has_no_invented_opening_or_historical_rows(self):
        world, _ = self.world(); world.today = date(1998, 6, 30).toordinal()
        released = Country('NSO', 901); world.countries['NSO'] = released
        state = next(s for s in world.states.values() if s.owner == 'DEL')
        state.owner = state.controller = 'NSO'; output = state.variables['ac_macro_real_output']
        world.action('on_startup')
        self.assertEqual(0, released.variables['ac_macro_history_count'])
        self.assertEqual(0, released.variables['ac_macro_cash']); self.assertEqual(0, released.variables['ac_macro_debt'])
        self.assertEqual(output, state.variables['ac_macro_real_output'])
        world.month('NSO', 1998, 7)
        self.assertEqual(1, released.variables['ac_macro_history_count'])
        self.assertEqual(1, released.variables['ac_macro_history_0_sequence'])
        self.assertEqual(0, released.variables['ac_macro_history_1_sequence'])

    def test_underfunding_then_arrears_payment_are_distinct_recorded_flows(self):
        world, country = self.world()
        country.variables.update(ac_macro_cash=D(0), ac_macro_debt=D(140), ac_macro_commitments_annual=D(3000))
        before = position(country, True); world.month('SNS'); v = country.variables
        self.assertLess(v['ac_macro_history_0_paid'], v['ac_macro_history_0_bill'])
        self.assertGreater(v['ac_macro_history_0_arrears_added'], 0)
        self.assertEqual(v['ac_macro_arrears'], v['ac_macro_history_0_arrears'])
        self.assertNear(position(country, True) - before, (v['ac_macro_last_revenue_accrued_milli'] - v['ac_macro_last_bill_accrued_milli']) / 1000)
        world.run('ac_macro_receive', 'SNS', {'ac_macro_transaction_amount': D(10000)})
        previous_history = history(country)
        world.run('ac_macro_quote', 'SNS'); self.assertEqual(previous_history, history(country))
        world.month('SNS', 1991, 3)
        self.assertGreater(v['ac_macro_history_0_arrears_paid'], 0)
        self.assertEqual(0, v['ac_macro_history_0_arrears'])
        self.assertEqual(2, v['ac_macro_history_0_sequence'])

    def test_sub_quantum_commitment_accumulates_instead_of_becoming_free(self):
        world, country = self.world()
        for state in world.states.values():
            if state.controller == 'SNS': state.variables['ac_macro_real_output'] = D(0)
        country.variables.update(ac_macro_cash=D('.1'), ac_macro_debt=D(0), ac_macro_commitments_annual=D('.00005'))
        world.run('ac_macro_quote', 'SNS')
        self.assertGreater(country.variables['ac_macro_bill_milli'], 0)
        accrued = D(0); settled = D(0)
        for index in range(241):
            dated_month(world, 'SNS', index); v = country.variables
            accrued += v['ac_macro_last_bill_accrued_milli'] / 1000
            settled += v['ac_macro_last_bill']
            self.assertGreaterEqual(v['ac_macro_bill_carry_milli'], 0)
            self.assertLess(v['ac_macro_bill_carry_milli'], 1)
        self.assertGreaterEqual(settled, D('.001'))
        self.assertNear(accrued, settled + country.variables['ac_macro_bill_carry_milli'] / 1000)
        self.assertNear(D('.1') - country.variables['ac_macro_cash'], settled)
        # A public upfront purchase cannot report success for a payment below
        # the declared quantum. It grants neither a reward nor a free debit.
        before = country.variables['ac_macro_cash']
        country.flags['ac_macro_transaction_succeeded'] = None
        world.run('ac_macro_try_spend', 'SNS', {'ac_macro_transaction_amount': D('.0005')})
        self.assertNotIn('ac_macro_transaction_succeeded', country.flags)
        self.assertEqual(before, country.variables['ac_macro_cash'])

    def test_largest_profile_2020_scenario_remains_finite_and_keeps_conservation(self):
        world, country = self.world('OSE'); country.ai = True
        max_flow = D(0)
        for index in range(359):
            before = position(country, True); dated_month(world, 'OSE', index); v = country.variables
            self.assertNear(position(country, True) - before, (v['ac_macro_last_revenue_accrued_milli'] - v['ac_macro_last_bill_accrued_milli']) / 1000)
            max_flow = max(max_flow, v['ac_macro_revenue_milli'], v['ac_macro_bill_milli'])
            self.assertTrue(all(value.is_finite() for value in v.values()))
            for key in ('ac_macro_revenue_carry_milli', 'ac_macro_bill_carry_milli'):
                self.assertGreaterEqual(v[key], 0); self.assertLess(v[key], 1)
        self.assertEqual(12, country.variables['ac_macro_history_count'])
        self.assertEqual(359, country.variables['ac_macro_history_0_sequence'])
        # A bound on this explicitly synthetic Decimal scenario, not a claim
        # that the engine supports this range or a fully mobilized native OOB.
        self.assertLess(max_flow, D(2000000))


class LedgerUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gui = parse((MOD / 'interface/ac_macro_economy.gui').read_text())
        cls.nodes = {get(node, 'name', '').strip('"'): node for _, node in walk(cls.gui) if get(node, 'name')}
        cls.logic = get(get(parse((MOD / 'common/scripted_guis/ac_macro_economy.txt').read_text()), 'scripted_gui'), 'ac_macro_economy_screen')
        cls.triggers = {key: body for key, _, body in get(cls.logic, 'triggers')}
        cls.local = {match[1]: match[2] for match in re.finditer(r'^\s*([\w.]+):0 "(.*)"',
                    (MOD / 'localisation/english/ac_macro_l_english.yml').read_text(encoding='utf-8-sig'), re.M)}

    def test_five_required_pages_and_meaningful_conditional_visibility(self):
        self.assertEqual(['Overview', 'Budget', 'Industry', 'Debt / contracts', 'Ledger'],
                         [self.local[get(self.nodes[f'macro_tab_{i}'], 'buttonText').strip('"')] for i in range(5)])
        world = World(); world.action('on_startup'); country = world.countries['SNS']
        country.variables['ac_macro_ui_page'] = D(4)
        self.assertTrue(world.trigger(self.triggers['ledger_empty_visible'], country))
        self.assertFalse(world.trigger(self.triggers['ledger_0_sequence_visible'], country))
        world.month('SNS')
        self.assertFalse(world.trigger(self.triggers['ledger_empty_visible'], country))
        self.assertTrue(world.trigger(self.triggers['ledger_0_sequence_visible'], country))
        self.assertFalse(world.trigger(self.triggers['ledger_1_sequence_visible'], country))
        properties = {key: get(value, 'frame') for key, _, value in get(self.logic, 'properties')}
        self.assertEqual(36, len(properties))
        for i in range(12):
            for kind in ('output', 'net_positive', 'net_negative'):
                self.assertEqual(f'ac_macro_graph_{i}_{kind}', properties[f'ledger_graph_{i}_{kind}'])
        country.variables['ac_macro_ui_page'] = D(0)
        for state, expected in [('healthy', 'economy_healthy'), ('warning', 'economy_warning'), ('crisis', 'economy_crisis')]:
            country.flags.pop('ac_macro_warning', None); country.flags.pop('ac_macro_crisis', None)
            if state != 'healthy': country.flags['ac_macro_warning'] = None
            if state == 'crisis': country.flags['ac_macro_crisis'] = None
            visible = [name for name in ('economy_healthy', 'economy_warning', 'economy_crisis')
                       if world.trigger(self.triggers[name + '_visible'], country)]
            self.assertEqual([expected], visible)

    def test_real_font_advances_and_glyph_ink_fit_the_700_pixel_layout(self):
        window = self.nodes['ac_macro_economy_screen']; size = get(window, 'size')
        fonts = {}
        self.assertEqual(('860', '700'), (get(size, 'width'), get(size, 'height')))
        # These are the three requested logical viewports, not rendered tests.
        for width, height, scale in ((3440, 1440, 1), (1920, 1080, 1), (2560, 1440, 1.25)):
            self.assertLessEqual(860, width / scale); self.assertLessEqual(700, height / scale)
        for name, node in self.nodes.items():
            if name == 'ac_macro_economy_screen': continue
            pos = get(node, 'position')
            if not pos: continue
            x, y = int(get(pos, 'x')), int(get(pos, 'y'))
            width = int(get(node, 'maxWidth', '36' if name == 'macro_close' else '140'))
            height = int(get(node, 'maxHeight', '36'))
            if name.startswith('ledger_graph_'): width, height = 20, 96 if name.endswith('_output') else 48
            self.assertGreaterEqual(x, 0); self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + width, 860, name); self.assertLessEqual(y + height, 700, name)
            key = get(node, 'text', get(node, 'buttonText', '')).strip('"')
            if key not in self.local: continue
            def example(match):
                if '%' in match[0]: return '100%'
                if '|.0' in match[0]: return '999,999'
                if '|.1' in match[0]: return '999,999.9'
                if '|.2' in match[0]: return '999,999.99'
                return '999,999.999'
            text = re.sub(r'\[\?[^\]]+\]', example, self.local[key])
            font = get(node, 'font', get(node, 'buttonFont', 'ACBriefing16')).strip('"')
            if font not in fonts:
                raw = (MOD / 'gfx/fonts' / (font + '.fnt')).read_text()
                line_height = int(re.search(r'lineHeight=(\d+)', raw)[1])
                glyphs = {int(fields['id']): fields for fields in
                          (dict(re.findall(r'(\w+)=(-?\d+)', line)) for line in raw.splitlines() if line.startswith('char '))}
                atlas_name = re.search(r'page id=0 file="([^"]+)"', raw)[1]
                ink_bounds = {}
                with Image.open(MOD / 'gfx/fonts' / atlas_name) as atlas:
                    for code, values in glyphs.items():
                        glyph = {key: int(value) for key, value in values.items()}
                        crop = atlas.crop((glyph['x'], glyph['y'], glyph['x'] + glyph['width'], glyph['y'] + glyph['height'])).convert('RGBA')
                        ink_bounds[code] = crop.getchannel('A').getbbox()
                fonts[font] = line_height, glyphs, ink_bounds
            line_height, glyphs, ink_bounds = fonts[font]
            self.assertTrue(all(ord(char) in glyphs for char in text), name)
            lines = ['']
            for word in text.split():
                candidate = (lines[-1] + ' ' + word).strip()
                if lines[-1] and sum(int(glyphs[ord(char)]['xadvance']) for char in candidate) > width:
                    lines.append(word)
                else: lines[-1] = candidate
            self.assertLessEqual(len(lines) * line_height, height, (name, lines))
            self.assertTrue(all(sum(int(glyphs[ord(char)]['xadvance']) for char in line) <= width for line in lines), name)
            # Inspect actual atlas ink, including yoffset; metadata lineHeight
            # alone can conceal descenders clipped by a tight numeric row.
            for row, line in enumerate(lines):
                for char in line:
                    ink = ink_bounds[ord(char)]
                    if ink:
                        self.assertLessEqual(row * line_height + int(glyphs[ord(char)]['yoffset']) + ink[3], height, (name, char))

    def test_graph_textures_have_33_bounded_frames_and_opposite_signed_bars(self):
        manifest = json.loads((MOD / 'gfx/interface/ac_macro/manifest.json').read_text())
        rows = {Path(row['file']).stem: row for row in manifest['assets']}
        for name, height in [('graph_output', 96), ('graph_net_positive', 48), ('graph_net_negative', 48)]:
            row = rows[name]; self.assertEqual(33, row['frames']); self.assertEqual((660, height), (row['width'], row['height']))
            path = MOD / row['file']; self.assertEqual(row['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as image:
                image = image.convert('RGBA'); counts = []
                for frame in range(33):
                    tile = image.crop((frame * 20, 0, (frame + 1) * 20, height))
                    color = (149, 179, 221, 255) if name == 'graph_net_negative' else (93, 208, 223, 255)
                    pixels = [(x, y) for y in range(height) for x in range(20) if tile.getpixel((x, y)) == color]
                    counts.append(len(pixels))
                    self.assertTrue(all(3 <= x <= 16 for x, _ in pixels))
                    if frame:
                        ys = [y for _, y in pixels]
                        self.assertEqual(1 if name == 'graph_net_negative' else height - 2, min(ys) if name == 'graph_net_negative' else max(ys))
                self.assertEqual(0, counts[0]); self.assertEqual(sorted(counts), counts)
                self.assertEqual(33, len(set(counts)))
                self.assertGreater(counts[-1], counts[1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
