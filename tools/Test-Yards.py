"""Offline sea-trial decision regressions; these do not simulate HOI4 RNG."""

from pathlib import Path
import unittest

from economy_script import fields, read


MOD = Path(__file__).resolve().parents[1] / "mod/2985041246"


class SeaTrialTests(unittest.TestCase):
    def setUp(self):
        categories = fields(read(MOD / "common/decisions/ac_yards.txt"))
        self.trial = fields(fields(categories["ac_yards_cat"])["ac_yards_sea_trial"])

    def test_repeatable_trial_disables_the_fixed_seed_at_decision_scope(self):
        self.assertEqual("no", self.trial.get("fixed_random_seed"))

    def test_trial_remains_repeatable_and_rolls_after_completion(self):
        self.assertNotEqual("yes", self.trial.get("fire_only_once"))
        self.assertEqual("15", self.trial["cost"])
        self.assertEqual("21", self.trial["days_remove"])
        self.assertEqual(
            {"ac_yards_sea_trial_effect": "yes"},
            fields(self.trial["remove_effect"]),
        )

    def test_completion_retains_the_advertised_seventy_thirty_outcomes(self):
        effects = fields(read(MOD / "common/scripted_effects/ac_yards.txt"))
        trial = fields(effects["ac_yards_sea_trial_effect"])
        self.assertEqual(
            {"var": "ac_yards_trial_attempts", "value": "1"},
            fields(trial["add_to_variable"]),
        )
        outcomes = fields(trial["random_list"])
        self.assertEqual({"70", "30"}, set(outcomes))
        success = fields(outcomes["70"])
        self.assertEqual(
            {"var": "ac_yards_trials", "value": "1"},
            fields(success["add_to_variable"]),
        )
        self.assertEqual("ac_yards.10", success["country_event"])
        self.assertEqual(
            {"add_stability": "-0.01", "country_event": "ac_yards.11"},
            fields(outcomes["30"]),
        )


if __name__ == "__main__":
    unittest.main()
