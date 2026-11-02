"""Execute shipped partner scripts offline, distinct from native acceptance.

The national scripts and ac_ucw owner are real source ASTs. Politics/fiscal
calls are explicit contract adapters here; those owners have separate suites.
--require-dependencies additionally requires their shipped definitions.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "tools"))
from content import COUNTRIES, FOCUSES, PHASES
from scopes import SCOPES, CAPABILITIES
import build
from economy_script import parse, fields

spec = importlib.util.spec_from_file_location("partners_ucw_owner", ROOT / "tools/Test-ContinentalWar.py")
ucw = importlib.util.module_from_spec(spec); sys.modules[spec.name] = ucw; spec.loader.exec_module(ucw)

parser = argparse.ArgumentParser()
parser.add_argument("--require-dependencies", action="store_true")
parser.add_argument("--engine", type=Path)
args, remainder = parser.parse_known_args()


def load(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


def get(body, key, default=None):
    return next((v for k, _, v in body if k == key), default)


class World(ucw.World):
    def __init__(self, when="1991.1.1", mode="off"):
        super().__init__(when)
        self.mode = mode; self.temps = {}
        self.from_country = None
        for country in self.countries.values():
            country.original = country.tag; country.pp = 500; country.cash = 10 if mode == "legacy" else .02
            country.arrears = 0; country.politics = True; country.generic_busy = False; country.dynamic = set()
            country.variables["ac_pol_capacity"] = 50
        self.effects.update(ucw.mapping(load("common/scripted_effects/ac_usean_partners.txt")))
        self.triggers.update(ucw.mapping(load("common/scripted_triggers/ac_usean_partners.txt")))
        self.events.update({get(v, "id"): (k, v) for k, _, v in load("events/ac_usean_partners.txt") if k == "country_event"})
        self.focuses = {}
        for tag in COUNTRIES:
            tree = load("common/national_focus/" + tag + ".txt")[0][2]
            self.focuses.update({get(v, "id"): v for k, _, v in tree if k == "focus"})
        self.decisions = {k: v for _, _, category in load("common/decisions/ac_usean_partners.txt") for k, _, v in category}
        for tag in COUNTRIES:
            self.run("ac_up_initialize", tag)

    def number(self, value, country):
        if (country.tag, value) in self.temps:
            return self.temps[country.tag, value]
        return super().number(value, country)

    def trigger(self, body, country):
        results = []
        for key, op, value in body:
            if key in ("tag", "original_tag"):
                result = (country.tag if key == "tag" else country.original) == value
            elif key == "political_power":
                result = self.compare(country.pp, op, float(value))
            elif key == "check_variable":
                var, operation, operand = value[0]
                result = self.compare(self.number(var, country), operation, self.number(operand, country))
            elif key == "ac_pol_active":
                result = (country.politics and country.exists and not country.capitulated) == (value == "yes")
            elif key in ("ac_econ_ready", "ac_econ_enabled"):
                # This coarse campaign suite models only enabled/off modes.
                # test_integration executes the real owner's unready accounts.
                result = (self.mode != "off") == (value == "yes")
            elif key == "ac_econ_can_pay_programme":
                result = (self.mode != "off" and not country.arrears and country.cash >= (2 if self.mode == "legacy" else .002)) == (value == "yes")
            elif key == "has_dynamic_modifier":
                result = fields(value)["modifier"] in country.dynamic
            elif key == "has_focus_tree":
                result = country.tree == value
            elif key == "ac_pol_previous_tree_idle":
                result = (not country.generic_busy) == (value == "yes")
            else:
                result = super().trigger([(key, op, value)], country)
            results.append(result)
        return all(results)

    @staticmethod
    def compare(left, op, right):
        return {"=": left == right, ">": left > right, "<": left < right,
                ">=": left >= right, "<=": left <= right}[op]

    def execute(self, body, country):
        branch = None
        for key, op, value in body:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise AssertionError("Orphaned branch " + key)
                if not branch and (key == "else" or self.trigger(get(value, "limit"), country)):
                    self.execute([n for n in value if n[0] != "limit"], country); branch = True
                continue
            branch = None
            if key in ("set_temp_variable", "multiply_temp_variable"):
                name, _, operand = value[0]; number = self.number(operand, country)
                self.temps[country.tag, name] = number if key == "set_temp_variable" else self.temps[country.tag, name] * number
            elif key in ("multiply_variable", "subtract_from_variable"):
                name, _, operand = value[0]; number = self.number(operand, country)
                country.variables[name] = country.variables[name] * number if key == "multiply_variable" else country.variables[name] - number
            elif key == "add_political_power":
                country.pp += float(value)
            elif key == "hidden_effect":
                self.execute(value, country)
            elif key == "effect_tooltip":
                pass  # The native effect preview executes no gameplay action.
            elif key == "FROM":
                if self.from_country is None: raise AssertionError("Missing annexed-country scope")
                self.execute(value, self.from_country)
            elif key == "ac_pol_change_capacity":
                self.assert_contract(self.trigger([("ac_pol_active", "=", "yes")], country), "unguarded politics API")
                delta = self.temps[country.tag, "ac_pol_capacity_delta"]
                country.variables["ac_pol_capacity"] = min(100, max(0, country.variables["ac_pol_capacity"] + delta))
            elif key == "ac_econ_pay_programme":
                self.assert_contract(self.trigger([("ac_econ_can_pay_programme", "=", "yes")], country), "unfunded fiscal API")
                country.cash -= 2 if self.mode == "legacy" else .002
            elif key == "add_dynamic_modifier":
                country.dynamic.add(fields(value)["modifier"])
            elif key in ("add_opinion_modifier", "remove_opinion_modifier"):
                data = fields(value)
                self.assert_contract(data["modifier"] == "ac_up_practical_services", "unexpected opinion modifier")
                if key == "add_opinion_modifier":
                    country.opinions.append(data)
                else:
                    country.opinions = [o for o in country.opinions if o != data]
            else:
                super().execute([(key, op, value)], country)

    @staticmethod
    def assert_contract(value, label):
        if not value:
            raise AssertionError(label)

    def choose(self, ident, option=0, tag="SNS"):
        if self.trigger(get(self.events[ident][1], "trigger", []), self.countries[tag]):
            super().choose(ident, option, tag)

    def owner_start(self):
        self.run("ac_ucw_world_start", "SNS")
        for tag in COUNTRIES:
            self.run("ac_ucw_country_start", tag)
        self.run("ac_ucw_country_start", "FCU")

    def earn_programmes(self, tag, offer=False):
        """Shortcut fixture: execute actual national rewards, not natural pacing."""
        for suffix in set(build.LEASE_UNLOCKS[tag].values()):
            self.run(tag + "_up_" + suffix + "_reward", tag)
        if offer:
            self.run(tag + "_up_" + build.OFFER_UNLOCKS[tag] + "_reward", tag)


class PartnerTests(unittest.TestCase):
    def test_generation_and_optional_dependency_gate(self):
        for relative, text in build.outputs().items():
            self.assertEqual((MOD / relative).read_text(encoding="utf-8"), text, relative)
        if args.require_dependencies:
            build.check_dependencies()

    def test_exact_counts_positions_prerequisites_and_mutual_paths(self):
        w = World()
        self.assertEqual(Counter(r.tag for r in FOCUSES), Counter({"SNS": 72, "AMB": 60, "UGE": 48, "DEL": 48}))
        seen = set()
        for ident, body in w.focuses.items():
            coordinate = (ident[:3], get(body, "x"), get(body, "y"))
            self.assertNotIn(coordinate, seen); seen.add(coordinate)
            self.assertIn(get(body, "cost"), ("5", "10"))
            for key, _, rows in body:
                if key in ("prerequisite", "mutually_exclusive"):
                    for _, _, target in rows:
                        self.assertIn(target, w.focuses)
                        if key == "prerequisite":
                            self.assertLess(int(get(w.focuses[target], "y")), int(get(body, "y")))
                        else:
                            reciprocal = [v for k, _, group in w.focuses[target] if k == "mutually_exclusive" for _, _, v in group]
                            self.assertIn(ident, reciprocal)

    def test_chronological_focus_courses_all_policy_combinations_remain_reachable(self):
        # This advances actual focus costs/prerequisites and dates. It is an
        # offline pacing model; it does not claim native AI or war progression.
        for tag in COUNTRIES:
            rows = [r for r in FOCUSES if r.tag == tag]
            for choices in product((0, 1), repeat=4):
                w = World(); c = w.countries[tag]; initialized_owner = False
                assessment = rows[-1]
                for _ in range(120):
                    if w.today >= ucw.day("1999.7.8") and not initialized_owner:
                        w.owner_start(); initialized_owner = True
                    for row in rows:
                        if row.id not in c.focuses and w.trigger(get(w.focuses[row.id], "bypass", [("always", "=", "no")]), c):
                            c.focuses.add(row.id)  # Native bypass grants no reward.
                    if assessment.id in c.focuses:
                        break
                    available = []
                    for row in rows:
                        body = w.focuses[row.id]
                        if row.id in c.focuses:
                            continue
                        prerequisites = [v for k, _, group in body if k == "prerequisite" for _, _, v in group]
                        exclusions = [v for k, _, group in body if k == "mutually_exclusive" for _, _, v in group]
                        if prerequisites and not any(p in c.focuses for p in prerequisites):
                            continue
                        if any(p in c.focuses for p in exclusions):
                            continue
                        if row.row == 1 and row.lane < 2 and row.lane != choices[PHASES.index(row.phase)]:
                            continue
                        if w.trigger(get(body, "available"), c):
                            available.append(row)
                    if available:
                        row = available[0]; w.today += row.cost * 7
                        if w.trigger(get(w.focuses[row.id], "available"), c):
                            w.execute(get(w.focuses[row.id], "completion_reward"), c)
                            c.focuses.add(row.id)
                    else:
                        future = [ucw.day(d) for d in ("1996.4.20", "1999.7.8", "2005.12.31") if ucw.day(d) > w.today]
                        self.assertTrue(future, (tag, choices, sorted(c.focuses)))
                        w.today = min(future)
                self.assertIn(assessment.id, c.focuses, (tag, choices))
                self.assertLess(w.today, ucw.day("2009.1.1"), (tag, choices))

    def test_continuous_panels_clear_resolved_tree_extents_and_fit_primary_view(self):
        def walk(nodes):
            for key, _, value in nodes:
                if isinstance(value, list):
                    yield key, value
                    yield from walk(value)
        sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
        from script import parse as gui_parse
        sys.path.pop(0)
        gui = gui_parse((MOD / "interface/nationalfocusview.gui").read_text(encoding="utf-8-sig"))
        named = lambda name: next(node for _, node in walk(gui) if get(node, "name") == '"' + name + '"')
        pitch = get(named("focus_spacing"), "position")
        panel = get(named("continuous_focus_window"), "size")
        for tag in COUNTRIES:
            tree = load("common/national_focus/" + tag + ".txt")[0][2]
            position = get(tree, "continuous_focus_position")
            x, y = int(get(position, "x")), int(get(position, "y"))
            focuses = [node for key, _, node in tree if key == "focus"]
            right = max(int(get(node, "x")) * int(get(pitch, "x")) + 169 for node in focuses)
            self.assertGreater(x, right + 32); self.assertLess(y, 100)
            self.assertLessEqual(50 + x + int(get(panel, "width")), 3440)
            self.assertLessEqual(78 + 47 + 66 + y + int(get(panel, "height")), 1440)

    def test_all_228_rewards_are_once_and_refuse_capitulation_or_clone_tags(self):
        for row in FOCUSES:
            when = "1997.1.1" if row.phase == "preparedness" else "2006.1.1" if row.phase == "settlement" else "2001.1.1"
            w = World(when); c = w.countries[row.tag]; c.flags["ac_up_was_displaced"] = None
            w.globals.add("ac_ucw_outcome_isaf_victory")
            reward = row.id + "_reward"
            c.capitulated = True; before = copy.deepcopy(c); w.run(reward, row.tag); self.assertEqual(before, c, row.id)
            c.capitulated = False; c.tag = "D01"; before = copy.deepcopy(c); w.run(reward, row.tag); self.assertEqual(before, c, row.id)
            c.tag = row.tag; w.run(reward, row.tag)
            self.assertIn(row.id + "_done", c.flags, row.id)
            after = copy.deepcopy(c); w.run(reward, row.tag); self.assertEqual(after, c, row.id)

    def test_policies_are_exclusive_and_restore_after_displacement(self):
        for tag in COUNTRIES:
            w = World("1997.1.1"); c = w.countries[tag]
            a = build.row_at(tag, "administration", 1, 0); b = build.policy_other(a)
            w.run(a.id + "_reward", tag); before = copy.deepcopy(c)
            w.run(b.id + "_reward", tag); self.assertEqual(before, c)
            c.capitulated = True; w.run("ac_up_suspend", tag)
            self.assertNotIn(a.id + "_spirit", c.ideas)
            self.assertIn("ac_up_was_displaced", c.flags)
            c.capitulated = False; w.run("ac_up_" + tag.lower() + "_restore_policies", tag)
            self.assertIn(a.id + "_spirit", c.ideas); self.assertNotIn(b.id + "_spirit", c.ideas)

    def test_preparation_applies_after_owner_once_and_late_work_does_not_backdate(self):
        for tag in COUNTRIES:
            w = World("1997.1.1"); c = w.countries[tag]
            c.variables["ac_up_preparedness"] = 20
            w.run("ac_up_apply_preparation", tag)
            self.assertNotIn("ac_ucw_recovery", c.variables)
            w.today = ucw.day("1999.12.1"); w.owner_start(); w.run("ac_up_apply_preparation", tag)
            self.assertEqual(c.variables["ac_ucw_recovery"], 51); self.assertEqual(c.variables["ac_ucw_pressure"], 34)
            saved = copy.deepcopy(w); saved.run("ac_up_apply_preparation", tag); self.assertEqual(c, saved.countries[tag])
            late = World("2004.1.1"); target = late.countries[tag]; late.owner_start()
            row = build.row_at(tag, "preparedness", 2, 0)
            late.run(row.id + "_reward", tag)
            self.assertEqual(target.variables["ac_up_preparedness"], 0)
            warning = build.row_at(tag, "preparedness", 0, 2)
            late.run(warning.id + "_reward", tag)
            self.assertNotIn(warning.id + "_done", target.flags)
            self.assertTrue(late.trigger(get(late.focuses[warning.id], "bypass"), target))
            late.run("ac_up_apply_preparation", tag)
            self.assertEqual(target.variables["ac_ucw_recovery"], 45)

    def test_funding_modes_recheck_stale_buttons_and_charge_once(self):
        for mode in ("off", "legacy", "full"):
            for efficient in (False, True):
                w = World(mode=mode); c = w.countries["SNS"]
                w.earn_programmes("SNS")
                if efficient:
                    c.flags["ac_up_efficient_authorisations"] = None
                before_cash = c.cash
                w.run("SNS_up_network_programme_start", "SNS")
                self.assertEqual(c.pp, 475)
                self.assertEqual(c.variables["ac_pol_capacity"], 49 if efficient else 48)
                self.assertAlmostEqual(c.cash, before_cash - (0 if mode == "off" else 2 if mode == "legacy" else .002))
                after = copy.deepcopy(c); w.run("SNS_up_network_programme_start", "SNS"); self.assertEqual(after, c)
                denied = World(mode=mode); d = denied.countries["SNS"]
                denied.earn_programmes("SNS")
                if mode == "off":
                    d.variables["ac_pol_capacity"] = 1
                else:
                    d.cash = 0
                before = copy.deepcopy(d); denied.run("SNS_up_network_programme_start", "SNS"); self.assertEqual(before, d)

    def test_lease_completes_once_and_capitulation_forfeits_reward(self):
        for tag in COUNTRIES:
            kind = build.LEASES[tag][0][0]; ident = tag + "_up_" + kind + "_programme"
            w = World("2001.1.1"); w.owner_start(); c = w.countries[tag]
            w.earn_programmes(tag)
            w.run(ident + "_start", tag); after_payment = copy.deepcopy(c)
            w.run(ident + "_finish", tag); self.assertEqual(after_payment, c)
            w.today += 181; w.run(ident + "_finish", tag); after = copy.deepcopy(c)
            w.run(ident + "_finish", tag); self.assertEqual(after, c)
            interrupted = World("2001.1.1"); interrupted.owner_start(); d = interrupted.countries[tag]
            interrupted.earn_programmes(tag)
            interrupted.run(ident + "_start", tag); d.capitulated = True; interrupted.run("ac_up_suspend", tag)
            interrupted.today += 181; d.capitulated = False; interrupted.run(ident + "_finish", tag)
            self.assertEqual(d.variables["ac_ucw_recovery"], 45)
            self.assertNotIn(ident + "_active", d.flags)

    def test_amber_capacity_is_funded_and_spent_not_an_infinite_stock(self):
        w = World("2001.1.1"); w.owner_start(); c = w.countries["AMB"]
        w.earn_programmes("AMB")
        before = copy.deepcopy(c); w.run("AMB_up_transport_programme_start", "AMB"); self.assertEqual(before, c)
        w.run("AMB_up_reserve_programme_start", "AMB"); w.today += 181
        w.run("AMB_up_reserve_programme_finish", "AMB"); self.assertEqual(c.variables["ac_up_amber_slots"], 1)
        w.run("AMB_up_transport_programme_start", "AMB"); self.assertEqual(c.variables["ac_up_amber_slots"], 0)
        w.today += 181; w.run("AMB_up_transport_programme_finish", "AMB")
        self.assertEqual(c.variables["ac_ucw_recovery"], 47)

    def test_ugellas_slots_limit_choices_and_release_has_no_completion_credit(self):
        w = World("2001.1.1"); w.owner_start(); c = w.countries["UGE"]
        w.earn_programmes("UGE")
        self.assertEqual(c.variables["ac_up_uge_limit"], 2)
        w.run("UGE_up_dispersal_programme_start", "UGE"); w.today += 31
        w.run("UGE_up_mobility_programme_start", "UGE"); w.today += 31
        before = copy.deepcopy(c); w.run("UGE_up_receiving_programme_start", "UGE"); self.assertEqual(before, c)
        w.run("UGE_up_dispersal_programme_release", "UGE")
        self.assertEqual(c.variables["ac_up_uge_used"], 1); self.assertEqual(c.variables["ac_ucw_recovery"], 45)
        w.run("UGE_up_dispersal_programme_release", "UGE"); self.assertEqual(c.variables["ac_up_uge_used"], 1)
        c.variables["ac_up_uge_reserve_level"] = 4; w.run("ac_up_recalculate", "UGE")
        self.assertEqual(c.variables["ac_up_uge_limit"], 4)
        w.run("UGE_up_receiving_programme_start", "UGE"); self.assertEqual(c.variables["ac_up_uge_used"], 2)

    def test_delarus_verified_cases_resolve_actual_obligations(self):
        w = World("2001.1.1"); c = w.countries["DEL"]
        w.run("DEL_up_verification_rules_reward", "DEL")
        c.flags.pop("ac_up_efficient_authorisations", None)
        c.variables["ac_up_del_cases"] = 1; c.variables["ac_up_del_obligations"] = 1
        before_capacity = c.variables["ac_pol_capacity"]
        w.run("DEL_up_resolve_docket_apply", "DEL")
        self.assertEqual(c.variables["ac_up_del_cases"], 0); self.assertEqual(c.variables["ac_up_del_obligations"], 0)
        self.assertEqual(c.variables["ac_pol_capacity"], before_capacity - 1)
        after = copy.deepcopy(c); w.run("DEL_up_resolve_docket_apply", "DEL"); self.assertEqual(after, c)

    def test_delarus_obligations_accumulate_and_survive_displacement_until_reviewed(self):
        w = World("2001.1.1"); w.owner_start(); w.earn_programmes("DEL"); c = w.countries["DEL"]
        for count in range(1, 4):
            w.run("DEL_up_command_programme_start", "DEL")
            self.assertEqual(c.variables["ac_up_del_obligations"], count)
            w.today += 181; w.run("DEL_up_command_programme_finish", "DEL")
            self.assertEqual(c.variables["ac_up_del_obligations"], count)
        before = copy.deepcopy(c); w.run("DEL_up_command_programme_start", "DEL"); self.assertEqual(before, c)
        c.capitulated = True; w.run("ac_up_suspend", "DEL")
        self.assertEqual(c.variables["ac_up_del_obligations"], 3)
        c.capitulated = False; w.run("DEL_up_inspection_programme_start", "DEL")
        w.today += 181; w.run("DEL_up_inspection_programme_finish", "DEL")
        self.assertEqual(c.variables["ac_up_del_cases"], 1)
        w.run("DEL_up_verification_rules_reward", "DEL"); w.run("DEL_up_resolve_docket_apply", "DEL")
        self.assertEqual(c.variables["ac_up_del_obligations"], 2)
        w.run("DEL_up_command_programme_start", "DEL"); self.assertEqual(c.variables["ac_up_del_obligations"], 3)

    def test_four_reciprocal_offers_terminal_modes_and_duplicate_replies(self):
        for index, tag in enumerate(COUNTRIES):
            for mode in ("accept", "refuse", "expire", "war", "sender_subject", "recipient_subject", "sender_capitulated", "recipient_capitulated", "sender_annexed", "recipient_annexed"):
                with self.subTest(tag=tag, mode=mode):
                    w = World("2001.1.1"); w.owner_start(); c = w.countries[tag]; p = w.countries["FCU"]
                    w.earn_programmes(tag, offer=True)
                    if tag == "AMB":
                        c.variables["ac_up_amber_slots"] = 1
                    w.run(tag + "_up_send_offer", tag); self.assertIn("ac_up_offer_pending", c.flags)
                    if mode == "expire": w.today += 61
                    elif mode == "war": w.wars.add(frozenset((tag, "FCU")))
                    elif mode == "sender_subject": c.subject = True
                    elif mode == "recipient_subject": p.subject = True
                    elif mode == "sender_capitulated": c.capitulated = True
                    elif mode == "recipient_capitulated": p.capitulated = True
                    elif mode == "sender_annexed": c.exists = False
                    elif mode == "recipient_annexed": p.exists = False
                    if mode in ("accept", "refuse"):
                        w.choose("ac_up." + str(101 + index), 0 if mode == "accept" else 1, "FCU")
                    else:
                        w.run("ac_up_fcu_cleanup", "FCU")
                        if c.exists and not c.capitulated:
                            w.run("ac_up_diplomacy_tick", tag)
                        w.choose("ac_up." + str(101 + index), 0, "FCU")
                    snapshot = copy.deepcopy(w.countries)
                    w.choose("ac_up." + str(101 + index), 0, "FCU")
                    self.assertEqual(snapshot, w.countries)
                    self.assertEqual(c.variables["ac_ucw_recovery"], 47 if mode == "accept" else 45)
                    self.assertEqual(len(c.opinions), 1 if mode == "accept" else 0)
                    self.assertNotIn("ac_up_" + tag.lower() + "_pending", p.flags)
                    if tag == "AMB" and c.exists:
                        self.assertEqual(c.variables["ac_up_amber_slots"], 0 if mode == "accept" else 1)

    def test_accepted_service_stops_when_country_disappears_or_capitulates(self):
        for tag in COUNTRIES:
            w = World("2001.1.1"); w.owner_start(); c = w.countries[tag]; p = w.countries["FCU"]
            w.earn_programmes(tag, offer=True)
            c.variables["ac_up_amber_slots"] = 1
            w.run(tag + "_up_send_offer", tag); w.run(tag + "_up_accept_offer", "FCU")
            self.assertTrue(c.opinions and p.opinions)
            c.capitulated = True; w.run("ac_up_fcu_cleanup", "FCU")
            self.assertFalse(c.opinions); self.assertFalse(p.opinions)
            self.assertNotIn("ac_up_partner_active", c.flags)
            self.assertEqual(c.variables["ac_ucw_recovery"], 47)

    def test_recipient_annexation_does_not_revive_a_stale_agreement_on_return(self):
        for tag in COUNTRIES:
            w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag, offer=True)
            c = w.countries[tag]; p = w.countries["FCU"]
            c.variables["ac_up_amber_slots"] = 1
            w.run(tag + "_up_send_offer", tag); w.run(tag + "_up_accept_offer", "FCU")
            p.exists = False; w.run("ac_up_diplomacy_tick", tag)
            self.assertNotIn("ac_up_partner_active", c.flags); self.assertFalse(c.opinions)
            # No FCU weekly tick can run while annexed. Its historical marker and
            # opinion survive in this fixture until its actual country returns.
            self.assertIn("ac_up_" + tag.lower() + "_partner_active", p.flags)
            p.exists = True; w.run("ac_up_fcu_cleanup", "FCU")
            self.assertNotIn("ac_up_" + tag.lower() + "_partner_active", p.flags)
            self.assertFalse(p.opinions); self.assertEqual(c.variables["ac_ucw_recovery"], 47)

    def test_known_annex_capitulation_and_subject_hooks_prevent_rapid_return_revival(self):
        actions = get(load("common/on_actions/ac_usean_partners.txt"), "on_actions")
        names = ("on_annex", "on_capitulation_immediate", "on_subject_annexed",
                 "on_puppet", "on_subject_free", "on_subject_autonomy_level_change")
        for offset, tag in enumerate(COUNTRIES):
            for accepted in (False, True):
                for recipient in (False, True):
                    for name in names:
                        timings = (False, True) if name in ("on_annex", "on_capitulation_immediate", "on_puppet") else (True,)
                        for flag_already_changed in timings:
                            with self.subTest(tag=tag, accepted=accepted, recipient=recipient,
                                              hook=name, status_set=flag_already_changed):
                                w = World("2001.1.1", mode="full"); w.owner_start(); w.earn_programmes(tag, offer=True)
                                c = w.countries[tag]; p = w.countries["FCU"]
                                c.variables["ac_up_amber_slots"] = 1
                                w.run(tag + "_up_send_offer", tag)
                                if accepted: w.run(tag + "_up_accept_offer", "FCU")
                                affected = p if recipient else c
                                if name == "on_annex": affected.exists = not flag_already_changed
                                if name == "on_capitulation_immediate": affected.capitulated = flag_already_changed
                                if name in ("on_puppet", "on_subject_autonomy_level_change"): affected.subject = flag_already_changed
                                after_cost = (c.pp, c.cash)
                                body = get(get(actions, name), "effect")
                                if name == "on_annex":
                                    w.from_country = affected; w.execute(body, w.countries["ERU"])
                                else:
                                    w.from_country = w.countries["ERU"]; w.execute(body, affected)
                                # Restore inside the original sixty-day reply
                                # window, with NO weekly observer in between.
                                affected.exists = True; affected.capitulated = False; affected.subject = False
                                w.today += 1
                                w.choose("ac_up." + str(101 + offset), 0, "FCU")
                                w.run("ac_up_fcu_cleanup", "FCU"); w.run("ac_up_diplomacy_tick", tag)
                                self.assertNotIn("ac_up_offer_pending", c.flags)
                                self.assertNotIn("ac_up_partner_active", c.flags)
                                self.assertNotIn("ac_up_" + tag.lower() + "_pending", p.flags)
                                self.assertNotIn("ac_up_" + tag.lower() + "_partner_active", p.flags)
                                self.assertFalse(c.opinions); self.assertFalse(p.opinions)
                                self.assertEqual(47 if accepted else 45, c.variables["ac_ucw_recovery"])
                                self.assertEqual(after_cost, (c.pp, c.cash))
                                if tag == "AMB": self.assertEqual(0 if accepted else 1, c.variables["ac_up_amber_slots"])
                                saved = copy.deepcopy((c, p))
                                # A repeated callback/reply cannot refund twice.
                                w.choose("ac_up." + str(101 + offset), 0, "FCU")
                                w.run("ac_up_status_diplomacy_interrupt", affected.tag)
                                self.assertEqual(saved, (c, p))

    def test_new_bilateral_war_relation_closes_once_but_other_wars_do_not(self):
        body = get(get(get(load("common/on_actions/ac_usean_partners.txt"), "on_actions"),
                       "on_war_relation_added"), "effect")
        for offset, tag in enumerate(COUNTRIES):
            for accepted in (False, True):
                for reverse in (False, True):
                    w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag, offer=True)
                    c = w.countries[tag]; p = w.countries["FCU"]; c.variables["ac_up_amber_slots"] = 1
                    w.run(tag + "_up_send_offer", tag)
                    if accepted: w.run(tag + "_up_accept_offer", "FCU")
                    w.wars.add(frozenset((tag, "FCU")))
                    w.from_country = c if reverse else p; w.execute(body, p if reverse else c)
                    w.wars.clear(); w.today += 1
                    w.choose("ac_up." + str(101 + offset), 0, "FCU")
                    self.assertNotIn("ac_up_offer_pending", c.flags); self.assertNotIn("ac_up_partner_active", c.flags)
                    self.assertFalse(c.opinions); self.assertFalse(p.opinions)
                    self.assertEqual(47 if accepted else 45, c.variables["ac_ucw_recovery"])
                    if tag == "AMB": self.assertEqual(0 if accepted else 1, c.variables["ac_up_amber_slots"])
            for combatant in (tag, "FCU"):
                w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag, offer=True)
                c = w.countries[tag]; c.variables["ac_up_amber_slots"] = 1; w.run(tag + "_up_send_offer", tag)
                w.wars.add(frozenset((combatant, "ERU")))
                w.from_country = w.countries["ERU"]; w.execute(body, w.countries[combatant])
                self.assertIn("ac_up_offer_pending", c.flags)
                w.choose("ac_up." + str(101 + offset), 0, "FCU")
                self.assertIn("ac_up_partner_active", c.flags)

    def test_immediate_capitulation_cancels_services_before_liberation_without_a_weekly_tick(self):
        body = get(get(get(load("common/on_actions/ac_usean_partners.txt"), "on_actions"),
                       "on_capitulation_immediate"), "effect")
        for tag in COUNTRIES:
            w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag)
            c = w.countries[tag]; first = tag + "_up_" + build.LEASES[tag][0][0] + "_programme"
            w.run(first + "_start", tag); self.assertIn(first + "_active", c.flags)
            w.from_country = w.countries["ERU"]; w.execute(body, c)
            c.capitulated = False; w.today += 181; w.run(first + "_finish", tag)
            self.assertNotIn(first + "_active", c.flags); self.assertNotIn(first + "_spirit", c.ideas)
            self.assertEqual(45, c.variables["ac_ucw_recovery"])

    def test_programmes_and_offers_require_earned_focuses_and_capacity_milestones(self):
        for tag in COUNTRIES:
            w = World("2001.1.1"); c = w.countries[tag]
            for kind in build.LEASE_UNLOCKS[tag]:
                before = copy.deepcopy(c); w.run(tag + "_up_" + kind + "_programme_start", tag)
                self.assertEqual(before, c)
            before = copy.deepcopy(c); w.run(tag + "_up_send_offer", tag); self.assertEqual(before, c)
            w.earn_programmes(tag)
            first = next(iter(build.LEASE_UNLOCKS[tag]))
            w.run(tag + "_up_" + first + "_programme_start", tag)
            self.assertIn(tag + "_up_" + first + "_programme_active", c.flags)
        w = World(); c = w.countries["AMB"]
        self.assertEqual(c.variables["ac_up_amber_limit"], 2)
        c.variables["ac_up_amb_service_level"] = 4; w.run("ac_up_recalculate", "AMB")
        self.assertEqual(c.variables["ac_up_amber_limit"], 6)

    def test_initialization_preserves_preexisting_national_record_and_stays_once(self):
        w = World("2004.1.1"); c = w.countries["SNS"]
        c.flags.pop("ac_up_initialized"); c.variables["ac_up_sns_continuity"] = 23
        c.variables["ac_up_sns_continuity_level"] = 2; c.variables["ac_up_preparedness"] = 7
        w.run("ac_up_initialize", "SNS")
        self.assertEqual(c.variables["ac_up_sns_continuity"], 23)
        self.assertEqual(c.variables["ac_up_sns_continuity_level"], 2)
        self.assertEqual(c.variables["ac_up_preparedness"], 7)
        after = copy.deepcopy(c); w.run("ac_up_initialize", "SNS"); self.assertEqual(after, c)

    def scope_fixture(self, scope, when="2006.1.1"):
        w = World(when); c = w.countries[scope.tag]; w.globals.add("ac_ucw_outcome_isaf_victory")
        for suffix in scope.requirements: c.flags[scope.tag + "_up_" + suffix + "_done"] = None
        resource = {"contacts":"ac_up_sns_contact_records", "protection":"ac_up_sns_protection_records", "slots":"ac_up_amber_slots", "cases":"ac_up_del_cases"}.get(scope.resource)
        if resource: c.variables[resource] = 1
        return w, c, resource

    def test_all_117_curated_focus_capabilities_change_actual_paid_action_eligibility(self):
        inventory = build.purpose_inventory()
        self.assertEqual({"SNS":42,"AMB":33,"UGE":20,"DEL":22}, inventory["original_sole_axis_counts"])
        self.assertEqual({tag:0 for tag in COUNTRIES}, inventory["remaining_sole_axis_counts"])
        self.assertEqual(inventory, json.loads((HERE / "purposes.json").read_text()))
        for ident, scope in CAPABILITIES.items():
            row = next(row for row in FOCUSES if row.id == ident)
            when = "1997.1.1" if row.phase == "preparedness" and row.lane == 2 else "2006.1.1"
            w, c, _ = self.scope_fixture(scope, when); c.flags.pop(ident + "_done")
            self.assertFalse(w.available(scope.id, scope.tag), ident)
            w.run(ident + "_reward", scope.tag)
            self.assertTrue(w.available(scope.id, scope.tag), ident)
            before = c.pp; w.take(scope.id, scope.tag)
            self.assertEqual(before - 25, c.pp); self.assertIn(scope.id + "_spirit", c.ideas)

    def test_all_29_scopes_have_real_costs_finite_resources_and_once_cleanup(self):
        for scope in SCOPES:
            w, c, resource = self.scope_fixture(scope)
            w.take(scope.id, scope.tag)
            self.assertEqual(475,c.pp); self.assertEqual(48,c.variables["ac_pol_capacity"])
            self.assertEqual(0,c.variables[resource]) if resource else self.assertEqual(1,c.variables["ac_up_uge_used"])
            saved = copy.deepcopy(c); w.run(scope.id + "_start", scope.tag); self.assertEqual(saved,c)
            w.today += 91; w.run("ac_up_scope_tick", scope.tag)
            self.assertNotIn(scope.id + "_active",c.flags); self.assertNotIn(scope.id + "_spirit",c.ideas)
            if scope.resource == "occupied_slot": self.assertEqual(0,c.variables["ac_up_uge_used"])
            saved = copy.deepcopy(c); w.run("ac_up_scope_tick",scope.tag); self.assertEqual(saved,c)
            interrupted, target, resource = self.scope_fixture(scope)
            interrupted.take(scope.id,scope.tag); target.capitulated = True; interrupted.run("ac_up_suspend",scope.tag)
            target.capitulated = False; interrupted.today += 91; interrupted.run("ac_up_scope_tick",scope.tag)
            self.assertNotIn(scope.id + "_active",target.flags); self.assertNotIn(scope.id + "_spirit",target.ideas)
            self.assertEqual(475,target.pp)
            if resource: self.assertEqual(0,target.variables[resource])
            else: self.assertEqual(0,target.variables["ac_up_uge_used"])

    def test_sns_scope_records_are_earned_by_completed_service_not_focus_grants(self):
        w = World("2001.1.1"); c = w.countries["SNS"]; w.earn_programmes("SNS")
        self.assertEqual(0,c.variables["ac_up_sns_contact_records"])
        w.run("SNS_up_network_programme_start","SNS"); w.today += 181
        w.run("SNS_up_network_programme_finish","SNS"); self.assertEqual(1,c.variables["ac_up_sns_contact_records"])
        w.run("SNS_up_network_programme_finish","SNS"); self.assertEqual(1,c.variables["ac_up_sns_contact_records"])

    def test_annexation_hook_forfeits_active_scopes_and_service_completion_rewards(self):
        hook = get(get(load("common/on_actions/ac_usean_partners.txt"), "on_actions"), "on_annex")
        for scope in SCOPES:
            w, c, resource = self.scope_fixture(scope); w.take(scope.id, scope.tag)
            w.from_country = c; w.execute(get(hook,"effect"),w.countries["ERU"])
            c.exists = False; w.today += 181; c.exists = True
            w.run("ac_up_scope_tick",scope.tag)
            self.assertNotIn(scope.id + "_active",c.flags); self.assertNotIn(scope.id + "_spirit",c.ideas)
            self.assertEqual(475,c.pp)
            if resource: self.assertEqual(0,c.variables[resource])
            else: self.assertEqual(0,c.variables["ac_up_uge_used"])
        for tag in COUNTRIES:
            w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag); c = w.countries[tag]
            ident = tag + "_up_" + build.LEASES[tag][0][0] + "_programme"
            w.run(ident + "_start",tag); w.from_country = c
            w.execute(get(hook,"effect"),w.countries["ERU"])
            c.exists = False; w.today += 181; c.exists = True; w.run(ident + "_finish",tag)
            self.assertEqual(45,c.variables["ac_ucw_recovery"])
            self.assertNotIn(ident + "_active",c.flags)
        for offset, tag in enumerate(COUNTRIES):
            for accepted in (False,True):
                w = World("2001.1.1"); w.owner_start(); w.earn_programmes(tag,offer=True)
                c=w.countries[tag]; p=w.countries["FCU"]; c.variables["ac_up_amber_slots"]=1
                w.run(tag+"_up_send_offer",tag)
                if accepted: w.run(tag+"_up_accept_offer","FCU")
                w.from_country=c; w.execute(get(hook,"effect"),w.countries["ERU"])
                c.exists=False; w.today+=2; c.exists=True
                w.choose("ac_up."+str(101+offset),0,"FCU")
                self.assertEqual(47 if accepted else 45,c.variables["ac_ucw_recovery"])
                self.assertNotIn("ac_up_offer_pending",c.flags)
                self.assertNotIn("ac_up_partner_active",c.flags); self.assertFalse(c.opinions); self.assertFalse(p.opinions)
    def test_events_skip_expired_history_and_each_choice_is_once(self):
        late = World("2004.1.1"); late.owner_start()
        for tag in COUNTRIES:
            late.countries[tag].flags.update(ac_up_event_1_ready=None, ac_up_event_3_ready=None)
            late.run("ac_up_narrative_tick", tag)
        self.assertFalse([event for event in late.queue if event[2].startswith("ac_up.")])
        for offset, tag in enumerate(COUNTRIES):
            for index in range(1, 7):
                when = "1991.1.2" if index == 1 else "1997.1.1" if index in (2, 3) else "2006.1.1"
                w = World(when); c = w.countries[tag]
                c.flags[f"ac_up_event_{index}_ready"] = None; w.globals.add("ac_ucw_outcome_isaf_victory")
                ident = "ac_up." + str(offset * 10 + index)
                self.assertTrue(w.trigger(get(w.events[ident][1], "trigger"), c))
                w.choose(ident, 0, tag); after = copy.deepcopy(c); w.choose(ident, 1, tag); self.assertEqual(after, c)
                self.assertIn(f"ac_up_event_{index}_answered", c.flags)

    def test_all_settlements_and_late_assessments_have_eligible_conclusions(self):
        for tag in COUNTRIES:
            for outcome in [*ucw.OUTCOMES, "ac_ucw_war_averted", "peace_without_war"]:
                w = World("2006.2.1"); c = w.countries[tag]
                if outcome != "peace_without_war":
                    w.globals.add(outcome)
                self.assertTrue(w.trigger([("ac_up_settlement_ready", "=", "yes")], c))
                last = COUNTRIES[tag]["rows"] - 1
                local = build.row_at(tag, "settlement", last, 0)
                self.assertTrue(w.trigger(get(w.focuses[local.id], "available"), c))
                c.subject = True; c.flags["ac_up_was_displaced"] = None
                external = build.row_at(tag, "settlement", last, 1)
                self.assertTrue(w.trigger(get(w.focuses[external.id], "available"), c))
                assessment = build.row_at(tag, "settlement", last, 2)
                w.run(assessment.id + "_reward", tag); w.run("ac_up_narrative_tick", tag)
                self.assertTrue(any(e[2] == "ac_up." + str(list(COUNTRIES).index(tag) * 10 + 6) for e in w.queue))

    def test_old_save_adoption_waits_for_generic_focus_and_preserves_completed_content(self):
        for tag in COUNTRIES:
            for previous in ("generic_focus","ac_regional_foundation"):
                w = World("2004.1.1"); c = w.countries[tag]; c.tree = previous
                c.focuses.update(("army_effort","ac_reg_register"))
                decision = tag + "_up_adopt_programme"
                c.generic_busy = True; self.assertFalse(w.available(decision, tag))
                c.generic_busy = False; before = (c.pp, c.cash, dict(c.variables)); w.take(decision, tag)
                self.assertEqual(c.tree, "ac_up_" + tag.lower() + "_tree")
                self.assertTrue({"army_effort","ac_reg_register"} <= c.focuses)
                self.assertEqual(before, (c.pp, c.cash, dict(c.variables)))

    def test_english_art_bindings_and_all_distinct_compositions(self):
        localization = (MOD / "localisation/english/ac_usean_partners_l_english.yml").read_text(encoding="utf-8-sig")
        keys = set(re.findall(r"^\s*([A-Za-z0-9_.]+):", localization, re.M))
        for row in FOCUSES:
            self.assertIn(row.id, keys); self.assertIn(row.id + "_desc", keys)
        for _, _, event in load("events/ac_usean_partners.txt"):
            if isinstance(event, list):
                for name in (get(event, "title"), get(event, "desc")):
                    self.assertIn(name, keys)
        from PIL import Image
        manifest = json.loads((HERE / "assets.json").read_text())
        focuses = json.loads((HERE / "focus_art.json").read_text())
        self.assertEqual(len(focuses), 228); self.assertEqual(len({a["sha256"] for a in focuses}), 228)
        self.assertEqual(len(manifest["assets"]), 311)
        graphics = "\n".join(p.read_text(encoding="utf-8-sig") for p in (MOD / "interface").glob("*.gfx"))
        for asset in manifest["assets"]:
            self.assertEqual(asset["frames"], 1); self.assertEqual(asset["frame_width"], asset["width"])
            self.assertEqual(len(re.findall(r'\bname\s*=\s*"' + re.escape(asset["sprite"]) + r'"', graphics)), 1, asset["sprite"])
            with Image.open(MOD / asset["file"]) as image:
                self.assertEqual(image.size, (asset["width"], asset["height"]))
                self.assertEqual(image.mode, "RGBA"); self.assertEqual(image.format, "DDS")
                self.assertEqual(image.getchannel("A").getextrema(), (asset["alpha_min"], asset["alpha_max"]))
                self.assertEqual(image.getpixel((0, 0))[3], 0, "Opaque corner: " + asset["file"])
                self.assertEqual(image.getpixel((image.width // 2, image.height // 2))[3], 255, "Missing central panel: " + asset["file"])
        result = subprocess.run([sys.executable, "-B", str(HERE / "build_art.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_content_never_takes_ownership_of_war_projects_leaders_or_borders(self):
        text = (MOD / "common/scripted_effects/ac_usean_partners.txt").read_text()
        for token in ("set_global_flag", "declare_war_on", "transfer_state", "add_core_of", "set_politics", "recruit_character", "create_country_leader", "add_building_construction", "add_equipment_to_stockpile"):
            self.assertNotIn(token, text)
        self.assertIn("ac_ucw_bound = yes", text)
        self.assertNotRegex(text, r"(?:set_variable|add_to_variable)\s*=\s*\{\s*ac_pol_capacity\s*=")
        # Paid service benefits are not an unpaid civil-war inheritance. All
        # static national policies, leases and operational scopes publish the
        # engine's existing no-copy guard; dynamic programmes also retain their
        # current/original-tag enable condition. Native inheritance is untested.
        ideas = [idea for relative in ('common/ideas/ac_usean_partners.txt',
                                      'common/ideas/ac_usean_partner_scopes.txt')
                 for _, _, outer in load(relative) for _, _, country in outer
                 for _, _, idea in country]
        self.assertEqual(71, len(ideas))
        for idea in ideas:
            self.assertEqual([('always', '=', 'no')], get(idea, 'allowed_civil_war'))
        captured = json.loads((HERE / "engine_contracts.json").read_text())
        hooks = get(load("common/on_actions/ac_usean_partners.txt"), "on_actions")
        self.assertTrue(set(captured["hooks"]) <= {key for key, _, _ in hooks})
        for row in captured["hooks"].values():
            self.assertTrue(row["source"].startswith("engine://")); self.assertTrue(row["root"]); self.assertTrue(row["from"])
        if args.engine:
            for source in captured["sources"]:
                self.assertEqual(source["sha256"], hashlib.sha256((args.engine / source["path"].removeprefix("engine://")).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + remainder, verbosity=2)
