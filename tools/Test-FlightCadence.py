"""Offline static-fire decision regressions; these do not simulate HOI4 RNG."""

from pathlib import Path
import unittest

from economy_script import fields, read


MOD = Path(__file__).resolve().parents[1] / "mod/2985041246"


class StaticFireTests(unittest.TestCase):
    def setUp(self):
        categories = fields(read(MOD / "common/decisions/ac_flight_cadence.txt"))
        self.trial = fields(fields(categories["ac_flight_cadence_cat"])["ac_flight_static_fire"])

    def test_repeatable_static_fire_disables_the_fixed_seed_at_decision_scope(self):
        self.assertEqual("no", self.trial.get("fixed_random_seed"))

    def test_static_fire_remains_repeatable_and_rolls_after_completion(self):
        self.assertNotEqual("yes", self.trial.get("fire_only_once"))
        self.assertEqual("20", self.trial["cost"])
        self.assertEqual("14", self.trial["days_remove"])
        self.assertEqual(
            {"ac_flight_static_fire_effect": "yes"},
            fields(self.trial["remove_effect"]),
        )

    def test_completion_retains_the_seventy_thirty_outcomes(self):
        effects = fields(read(MOD / "common/scripted_effects/ac_flight_cadence.txt"))
        outcomes = fields(fields(effects["ac_flight_static_fire_effect"])["random_list"])
        self.assertEqual({"70", "30"}, set(outcomes))
        success = fields(outcomes["70"])
        self.assertEqual(
            {"var": "ac_flight_success", "value": "1"},
            fields(success["add_to_variable"]),
        )
        self.assertEqual("ac_flight_cadence.1", success["country_event"])
        failure = fields(outcomes["30"])
        self.assertEqual({"if", "add_stability", "country_event"}, set(failure))
        self.assertEqual("-0.02", failure["add_stability"])
        self.assertEqual("ac_flight_cadence.2", failure["country_event"])
        guarded_loss = fields(failure["if"])
        self.assertEqual(
            [("ac_flight_success", ">", "0")],
            fields(guarded_loss["limit"])["check_variable"],
        )
        self.assertEqual(
            {"var": "ac_flight_success", "value": "-1"},
            fields(guarded_loss["add_to_variable"]),
        )


if __name__ == "__main__":
    unittest.main()
