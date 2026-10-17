"""Behavioral regression tests against the shipped economy scripts, using stdlib only."""

import copy
from datetime import date
from decimal import Decimal as D
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from economy_script import Country, Harness, MOD, ROOT, fields, parse, validate_content


class EconomyTests(unittest.TestCase):
    def setUp(self):
        self.h = Harness()
        self.c = Country(factories=20)
        self.h.action("on_startup", [self.c])

    def set_values(self, **values):
        for key, value in values.items():
            self.c.variables["ac_econ_" + key] = D(str(value))

    def value(self, key):
        return self.c.value("ac_econ_" + key)

    def worth(self):
        return self.value("treasury") + self.value("procurement_escrow") - self.value("debt") - self.value("arrears")

    def test_static_contract(self):
        validate_content(self.h)

    def test_disabled_has_no_writes_even_from_direct_effects(self):
        h = Harness(enabled=False)
        country = Country()
        original = copy.deepcopy(country)
        h.action("on_startup", [country])
        for name in h.effects:
            h.call(name, country)
        self.assertEqual(country, original)
        h.action("on_weekly", [country])
        self.assertFalse(country.variables)
        self.assertFalse(country.flags)
        self.assertFalse(country.modifiers)
        self.assertFalse(country.equipment)

    def test_state_less_country_is_excluded(self):
        c = Country(owns_state=False)
        self.h.action("on_startup", [c])
        self.h.action("on_weekly", [c])
        self.assertEqual(c.variables, {})

    def test_initialization_is_idempotent_on_reload(self):
        self.set_values(treasury=11, debt=3, arrears=2, procurement_weeks=2, procurement_escrow=5)
        self.c.flags["ac_econ_tax_cooldown"] = 30
        before = copy.deepcopy(self.c)
        reloaded = copy.deepcopy(self.c)
        self.h.action("on_startup", [reloaded])
        self.assertEqual(reloaded, before)

    def test_quote_refresh_cannot_mint_or_settle(self):
        self.set_values(debt=3, arrears=2, procurement_weeks=2, procurement_escrow=5)
        before = self.worth()
        for _ in range(25):
            self.h.call("ac_econ_refresh_budget", self.c)
        self.assertEqual(self.worth(), before)
        self.assertEqual(self.value("procurement_weeks"), 2)
        self.assertEqual(self.value("last_revenue"), 0)

    def test_peace_budget_and_country_pulse_scope(self):
        other = Country(factories=0)
        self.h.action("on_startup", [other])
        self.h.action("on_weekly", [self.c, other])
        self.assertEqual(self.value("last_revenue"), 5)
        self.assertEqual(self.value("last_spending"), 4)
        self.assertEqual(self.value("treasury"), 51)
        self.assertEqual(other.value("ac_econ_treasury"), D("10.2"))

    def test_newly_released_country_initializes_on_its_first_week(self):
        new = Country(factories=0)
        self.h.action("on_weekly", [new])
        self.assertIn("ac_econ_initialized", new.flags)
        self.assertEqual(new.value("ac_econ_treasury"), D("10.2"))

    def test_war_burden_and_interest_settle_once(self):
        self.c.war = True
        self.set_values(treasury=1, debt=10)
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("last_spending"), D("5.5"))
        self.assertEqual(self.value("last_interest"), D("0.01"))
        self.assertEqual(self.value("treasury"), D("0.49"))
        self.assertEqual(self.value("debt"), 10)

    def test_partial_credit_becomes_arrears_without_deleting_liability(self):
        self.c.war = True
        self.set_values(treasury=0, debt="129.8")
        before = self.worth()
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("debt"), 130)
        self.assertEqual(self.value("treasury"), 0)
        self.assertEqual(self.value("last_borrowed"), D("0.2"))
        self.assertEqual(self.value("arrears"), D("0.4298"))
        self.assertEqual(self.worth() - before, self.value("last_balance"))
        self.assertEqual(self.value("stability"), D("-0.05"))
        self.assertFalse(self.h.click("ac_econ_borrow_decision", self.c))
        self.assertFalse(self.h.click("ac_econ_order_infantry_decision", self.c))

    def test_above_ceiling_debt_survives_lower_revenue(self):
        self.set_values(debt=200, treasury=0, tax_level=0)
        self.c.war = True
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("debt"), 200)
        self.assertEqual(self.value("credit_room"), 0)
        self.assertGreater(self.value("arrears"), 0)

    def test_existing_bills_are_paid_before_voluntary_repayment(self):
        self.set_values(treasury=10, debt=3, arrears=2)
        self.h.call("ac_econ_repay", self.c)
        self.assertEqual(self.value("debt"), 3)
        before = self.worth()
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("arrears"), 0)
        self.assertEqual(self.value("last_arrears_paid"), 2)
        self.assertEqual(self.worth() - before, self.value("last_balance"))

    def test_borrowing_rechecks_stale_quote_and_never_exceeds_ceiling(self):
        self.set_values(debt=127)
        # Cached credit room from initialization is stale; the effect must recheck.
        self.h.call("ac_econ_borrow", self.c)
        self.assertEqual(self.value("debt"), 127)
        self.set_values(debt=125)
        before = self.worth()
        self.h.call("ac_econ_borrow", self.c)
        self.h.call("ac_econ_borrow", self.c)
        self.assertEqual(self.value("debt"), 130)
        self.assertEqual(self.worth(), before)

    def test_partial_and_final_repayments_conserve_cash(self):
        self.set_values(treasury=2, debt=3)
        before = self.worth()
        self.h.call("ac_econ_repay", self.c)
        self.assertEqual(self.value("treasury"), 0)
        self.assertEqual(self.value("debt"), 1)
        self.assertEqual(self.worth(), before)
        self.set_values(treasury=20)
        before = self.worth()
        self.h.call("ac_econ_repay", self.c)
        self.h.call("ac_econ_repay", self.c)
        self.assertEqual(self.value("treasury"), 19)
        self.assertEqual(self.value("debt"), 0)
        self.assertEqual(self.value("interest"), 0)
        self.assertEqual(self.worth(), before)

    def test_ai_repays_from_surplus_with_operating_reserve(self):
        self.c.ai = True
        self.set_values(treasury=20, debt=3)
        before = self.worth()
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("debt"), 0)
        self.assertGreaterEqual(self.value("treasury"), 2 * self.value("spending"))
        self.assertEqual(self.worth() - before, self.value("last_balance"))

    def test_procurement_rejects_each_missing_prerequisite(self):
        for attribute, value in [("tech", False), ("military_factories", 0), ("capitulated", True)]:
            with self.subTest(attribute=attribute):
                original = getattr(self.c, attribute)
                setattr(self.c, attribute, value)
                cash = self.value("treasury")
                self.h.call("ac_econ_order_infantry", self.c)
                self.assertEqual(self.value("treasury"), cash)
                self.assertEqual(self.value("procurement_weeks"), 0)
                setattr(self.c, attribute, original)
        for values in [dict(treasury="4.99"), dict(treasury=20, arrears=1)]:
            self.set_values(**values)
            cash = self.value("treasury")
            self.h.call("ac_econ_order_infantry", self.c)
            self.assertEqual(self.value("treasury"), cash)
            self.assertEqual(self.value("procurement_weeks"), 0)

    def test_duplicate_orders_cancellation_and_repeated_refunds(self):
        before = self.worth()
        self.h.call("ac_econ_order_infantry", self.c)
        self.h.call("ac_econ_order_infantry", self.c)
        self.assertEqual(self.value("treasury"), 45)
        self.assertEqual(self.value("procurement_escrow"), 5)
        self.assertEqual(self.worth(), before)
        self.h.call("ac_econ_cancel_procurement", self.c)
        self.h.call("ac_econ_cancel_procurement", self.c)
        self.assertEqual(self.value("treasury"), 50)
        self.assertEqual(self.worth(), before)
        self.assertEqual(self.c.equipment, {})

    def test_contract_delivers_once_after_four_productive_pulses(self):
        self.h.click("ac_econ_order_infantry_decision", self.c)
        for _ in range(3):
            self.h.action("on_weekly", [self.c])
            self.assertEqual(self.c.equipment, {})
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.c.equipment, {"infantry_equipment_0": 100})
        self.assertEqual(self.value("procurement_escrow"), 0)
        self.h.call("ac_econ_cancel_procurement", self.c)
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.c.equipment, {"infantry_equipment_0": 100})
        self.assertEqual(self.value("treasury"), 50)

    def test_contract_pauses_after_factory_loss_and_survives_reload(self):
        self.h.call("ac_econ_order_infantry", self.c)
        self.c.military_factories = 0
        self.h.action("on_weekly", [self.c])
        self.assertEqual(self.value("procurement_weeks"), 4)
        reloaded = copy.deepcopy(self.c)
        self.h.action("on_startup", [reloaded])
        self.assertEqual(reloaded, self.c)
        self.c.military_factories = 1
        for _ in range(4):
            self.h.action("on_weekly", [self.c])
        self.assertEqual(self.c.equipment, {"infantry_equipment_0": 100})

    def test_tax_policy_has_shared_cooldown_and_real_modifier(self):
        self.assertTrue(self.h.click("ac_econ_high_tax_decision", self.c))
        self.assertEqual(self.value("revenue"), D("6.25"))
        self.assertEqual(self.value("stability"), D("-0.03"))
        self.assertFalse(self.h.click("ac_econ_low_tax_decision", self.c))
        self.h.call("ac_econ_set_low_tax", self.c)
        self.assertEqual(self.value("tax_level"), 2)
        self.c.day = 30
        self.assertTrue(self.h.click("ac_econ_low_tax_decision", self.c))
        self.assertEqual(self.value("stability"), D("0.02"))
        self.assertEqual(self.value("revenue"), D("3.75"))
        self.assertIn("ac_econ_budget_modifier", self.c.modifiers)

    def test_reconstruction_spends_more_and_shares_service_cooldown(self):
        cash = self.value("treasury")
        self.h.click("ac_econ_reconstruction_decision", self.c)
        self.assertEqual(self.value("civilian_spending"), 4)
        self.assertEqual(self.value("construction"), D("0.05"))
        self.assertEqual(self.value("treasury"), cash)
        self.assertFalse(self.h.click("ac_econ_basic_services_decision", self.c))
        self.set_values(arrears=1)
        self.h.call("ac_econ_refresh_budget", self.c)
        self.assertEqual(self.value("construction"), 0)

    def test_long_run_reconciles_through_war_and_industry_loss(self):
        self.c.war = True
        for week in range(600):
            if week == 60:
                self.c.factories = 0
            if week == 300:
                self.c.war = False
                self.h.call("ac_econ_set_high_tax", self.c)
            before = self.worth()
            self.h.action("on_weekly", [self.c])
            self.assertAlmostEqual(self.worth() - before, self.value("last_balance"), places=18)
            for key in ("treasury", "debt", "arrears", "credit_room"):
                self.assertGreaterEqual(self.value(key), 0)

    def test_1991_through_2065_stress_bounds(self):
        weeks = ((date(2066, 1, 1) - date(1991, 1, 1)).days + 6) // 7
        self.assertEqual(weeks, 3914)
        for war, reconstruction, low_tax, industry_loss in [
            (False, False, False, False),
            (True, True, True, False),
            (True, True, True, True),
        ]:
            with self.subTest(war=war, industry_loss=industry_loss):
                self.c = Country(factories=99995, war=war)
                self.h.action("on_startup", [self.c])
                self.assertEqual(self.value("capacity"), 1000)
                self.set_values(tax_level=0 if low_tax else 2,
                                civilian_level=1 if reconstruction else 0)
                for week in range(weeks):
                    if week == 100 and industry_loss:
                        self.c.factories = 0
                    before = self.worth()
                    self.h.action("on_weekly", [self.c])
                    self.assertAlmostEqual(self.worth() - before, self.value("last_balance"), places=18)
                    for key in ("treasury", "debt", "arrears", "credit_room"):
                        self.assertGreaterEqual(self.value(key), 0)
                        self.assertLess(self.value(key), 1000000)
                    self.assertLessEqual(self.value("debt"), 6500)


    def test_parser_and_validator_fail_closed_on_deliberate_errors(self):
        for text in ["bad = {", "bad = }", "bad = { value = 1 }}", "bad = 1 ;"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse(text)
        self.h.effects["ac_econ_borrow"].append(("misspelled_effect", "=", "yes"))
        with self.assertRaisesRegex(ValueError, "Unresolved script symbol"):
            validate_content(self.h)
        with self.assertRaisesRegex(ValueError, "Unsupported effect"):
            self.h.call("ac_econ_borrow", self.c)

    def test_unknown_numeric_input_and_namespace_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown numeric input"):
            self.h.execute(parse("set_variable = { ac_econ_treasury = earth_gdp }"), self.c)
        with self.assertRaisesRegex(ValueError, "outside economy namespace"):
            self.h.execute(parse("set_variable = { treasury = 5 }"), self.c)

    def test_validator_detects_undefined_variable_in_an_unreached_branch(self):
        self.h.effects["ac_econ_borrow"].append(
            ("set_variable", "=", [("ac_econ_test", "=", "ac_econ_typo")]))
        with self.assertRaisesRegex(ValueError, "Unassigned economy variables"):
            validate_content(self.h)

    def test_validator_detects_missing_localization_and_broken_tech_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            paths = ["localisation/english/ac_economy_l_english.yml", "common/game_rules/ac_economy_rules.txt",
                     "common/units/equipment/infantry.txt", "common/technologies/infantry.txt",
                     "common/dynamic_modifiers/ac_economy_modifiers.txt"]
            for relative in paths:
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(MOD / relative, destination)
            localization = target / paths[0]
            original = localization.read_bytes()
            localization.write_bytes(original.replace(b"ac_econ_repay_decision:", b"ac_econ_typo:"))
            with patch("economy_script.MOD", target), self.assertRaisesRegex(ValueError, "Missing English keys"):
                validate_content(self.h)
            localization.write_bytes(original)
            technology = target / "common/technologies/infantry.txt"
            technology.write_text(technology.read_text().replace("infantry_equipment_0", "missing_equipment"))
            with patch("economy_script.MOD", target), self.assertRaisesRegex(ValueError, "does not unlock"):
                validate_content(self.h)

    def test_workspace_is_relative_and_tasks_are_manual(self):
        workspace = json.loads((ROOT / "Project-Ulysses.code-workspace").read_text(encoding="utf-8"))
        self.assertEqual(workspace["folders"], [{"name": "Project Ulysses", "path": "."}])
        self.assertNotIn("settings", workspace)
        self.assertNotIn("extensions", workspace)
        tasks = {task["label"]: task for task in workspace["tasks"]["tasks"]}
        self.assertEqual(len(tasks), 3)
        for task in tasks.values():
            self.assertNotIn("runOptions", task)
            self.assertNotIn("isBackground", task)
        for task in tasks.values():
            for argument in task.get("args", []):
                if argument.startswith("${workspaceFolder}/"):
                    self.assertTrue((ROOT / argument.split("/", 1)[1]).exists())


if __name__ == "__main__":
    unittest.main()
