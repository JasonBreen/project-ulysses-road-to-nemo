"""Static namespace contract for shared 1991 AI strategy definitions."""

from pathlib import Path
import unittest

from economy_script import fields, read


MOD = Path(__file__).resolve().parents[1] / "mod/2985041246"
EXPECTED_IDS = {
    "ac_default_production",
    "ac_naval_roles",
    "ac_air_1991",
    "ac_convoy_escort",
    "ac_template_design",
    "ac_pp_spend",
    "ac_stockpile",
    "ac_garrison_priority",
    "ac_intelligence_agency",
    "ac_market_peace",
    "ac_market_war",
}


class SharedAIStrategyTests(unittest.TestCase):
    def test_shared_strategies_keep_unique_stable_ac_ids(self):
        # fields rejects duplicate top-level IDs; parse ignores comments and
        # distinguishes strategy names from their nested engine role IDs.
        strategies = fields(read(MOD / "common/ai_strategy/default.txt"))
        self.assertEqual(EXPECTED_IDS, set(strategies))


if __name__ == "__main__":
    unittest.main()
