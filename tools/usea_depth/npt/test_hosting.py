"""Execute the generated hosting/lane subset offline, never the native engine."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
import test_npt as npt
from usea_expansion.script import get, parse

spec = importlib.util.spec_from_file_location("ucw_hosting", ROOT / "tools/Test-ContinentalWar.py")
ucw = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ucw
spec.loader.exec_module(ucw)


class HostingWorld(ucw.World):
    """Extend the strict UCW evaluator with the existing North Point focus syntax."""
    def __init__(self):
        super().__init__("2005.1.2")
        self.effects.update(npt.mapping(parse(npt.text("effects"))))
        self.focuses.update(npt.shared_focuses())
        self.focuses.update({get(v, "id"): v for k, _, v in
                             ucw.load("common/national_focus/NPT_pre_continental_war.txt") if k == "shared_focus"})
        self.events.update({get(v, "id"): (k, v) for k, _, v in parse(npt.text("events")) if k == "country_event"})
        self.globals.add("ac_ucw_isaf_formed")
        self.countries["NPT"].focuses.update({"NPT_ud_continent_at_the_edge", "NPT_open_the_airfields"})

    def trigger(self, nodes, country):
        answers = []
        for key, op, value in nodes:
            if key == "has_completed_focus":
                answers.append(value in country.focuses)
            elif key == "custom_trigger_tooltip":
                answers.append(self.trigger([node for node in value if node[0] != "tooltip"], country))
            else:
                answers.append(super().trigger([(key, op, value)], country))
        return all(answers)

    def execute(self, nodes, country):
        remaining = []
        for key, op, value in nodes:
            if key == "add_opinion_modifier" and get(value, "modifier") == "considers_friend":
                country.opinions.append(ucw.fields(value))
            else:
                remaining.append((key, op, value))
        super().execute(remaining, country)

    def focus_available(self, ident, tag="NPT"):
        country = self.countries[tag]
        node = self.focuses[ident]
        if ident in country.focuses:
            return False
        for key, _, value in node:
            if key == "prerequisite" and not any(ref in country.focuses for _, _, ref in value):
                return False
            if key == "mutually_exclusive" and any(ref in country.focuses for _, _, ref in value):
                return False
        return self.trigger(get(node, "available", []), country)


class Hosting(unittest.TestCase):
    neutral = "NPT_ud_neutral_waters"
    allied = "NPT_ud_allied_rear"
    neutral_idea = "NPT_ud_neutral_waters_spirit"

    def host(self, world, route):
        if route == "focus":
            world.complete("NPT_host_isaf", "NPT")
        elif route in ("invitation_early", "invitation_at_hq"):
            if route == "invitation_at_hq":
                world.globals.update({"ac_ucw_war_started", "ac_ucw_stage_north_point"})
                world.wars.add(frozenset(("ERU", "FCU")))
            world.choose("ac_ucw.32", 0, "NPT")
            self.assertEqual("FCU", world.faction["NPT"])
        else:
            world.globals.update({"ac_ucw_war_started", "ac_ucw_stage_los_canas"})
            world.wars.add(frozenset(("ERU", "FCU")))
            world.faction["NPT"] = "FCU"
            world.execute(world.effects["ac_ucw_stage_north_point"], world.countries["FCU"])
            self.assertIn("ac_ucw_npt_isaf_rear_base", world.countries["NPT"].ideas)

    def assert_hosted(self, world):
        country = world.countries["NPT"]
        self.assertNotIn(self.neutral_idea, country.ideas)
        self.assertNotIn("NPT_ud_lane_neutral", country.flags)
        self.assertIn("NPT_ud_lane_allied", country.flags)
        self.assertTrue(world.focus_available(self.allied))
        # Satisfy prerequisite chains to prove each unfinished neutral focus is gated.
        for slug in npt.c.NEUTRAL_FOCUSES:
            ident = npt.c.ident(slug)
            for group in npt.focus_refs(world.focuses[ident], "prerequisite"):
                country.focuses.update(group)
            country.focuses.discard(ident)
            self.assertFalse(world.focus_available(ident), ident)
            self.assertEqual("yes", get(world.focuses[ident], "cancel_if_invalid"))
            self.assertEqual("no", get(world.focuses[ident], "continue_if_invalid"))
        world.complete(self.allied, "NPT")
        self.assertIn("NPT_ud_allied_rear_services_spirit", country.ideas)
        self.assertTrue(world.focus_available("NPT_ud_schools_returned"))
        self.assertTrue(world.focus_available("NPT_ud_joint_air_control"))

    def test_all_hosting_routes_before_and_after_neutral_choice(self):
        for route in ("focus", "invitation_early", "invitation_at_hq", "allied_hq_stage"):
            for neutral_first in (False, True):
                with self.subTest(route=route, neutral_first=neutral_first):
                    world = HostingWorld()
                    if neutral_first:
                        world.complete(self.neutral, "NPT")
                        self.assertIn(self.neutral_idea, world.countries["NPT"].ideas)
                    self.host(world, route)
                    self.assert_hosted(world)

    def test_neutral_route_remains_complete_when_hosting_is_declined(self):
        world = HostingWorld()
        world.complete(self.neutral, "NPT")
        world.choose("ac_ucw.32", 1, "NPT")
        for slug in ("internment_convention", "neutral_hospital_berths", "neutral_ground", "armed_watch", "neutral_to_the_end"):
            world.complete(npt.c.ident(slug), "NPT")
        country = world.countries["NPT"]
        self.assertIn(self.neutral_idea, country.ideas)
        self.assertIn("NPT_ud_lane_neutral", country.flags)
        self.assertNotIn("NPT_ud_lane_allied", country.flags)
        self.assertFalse(world.focus_available(self.allied))

    def test_reconciliation_is_idempotent_and_survives_rear_base_idea_removal(self):
        world = HostingWorld()
        world.complete(self.neutral, "NPT")
        self.host(world, "invitation_at_hq")
        country = world.countries["NPT"]
        before = copy.deepcopy(country)
        world.execute(world.effects["ac_ud_npt_accept_hosting"], country)
        self.assertEqual(before, country)
        country.ideas.pop("ac_ucw_npt_isaf_rear_base")
        self.assertTrue(world.focus_available(self.allied))
        self.assertFalse(world.trigger(parse(npt.c.NOT_HOSTING), country))

    def test_in_flight_neutral_rewards_cannot_restore_neutrality(self):
        for route in ("focus", "invitation_early", "invitation_at_hq", "allied_hq_stage"):
            world = HostingWorld()
            self.host(world, route)
            country = world.countries["NPT"]
            before = copy.deepcopy(country)
            queued = list(world.queue)
            for slug in npt.c.NEUTRAL_FOCUSES:
                # Directly execute the stale completion payload, bypassing UI cancellation.
                world.execute(get(world.focuses[npt.c.ident(slug)], "completion_reward"), country)
            self.assertEqual(before, country, route)
            self.assertEqual(queued, world.queue, route)
        # Prove the original unconditional reward would restore the neutral spirit.
        world.execute(parse("set_country_flag = NPT_ud_lane_neutral add_ideas = " + self.neutral_idea), country)
        self.assertIn(self.neutral_idea, country.ideas)

    def test_neutral_idea_cancels_for_existing_hosting_saves(self):
        ideas = get(get(parse(npt.text("ideas")), "ideas"), "country")
        cancel = get(get(ideas, self.neutral_idea), "cancel")
        self.assertIsNotNone(cancel)
        world = HostingWorld()
        country = world.countries["NPT"]
        self.assertFalse(world.trigger(cancel, country))
        country.focuses.add("NPT_host_isaf")
        self.assertTrue(world.trigger(cancel, country))
        country.focuses.remove("NPT_host_isaf")
        country.ideas["ac_ucw_npt_isaf_rear_base"] = None
        self.assertTrue(world.trigger(cancel, country))

    def test_original_missing_hook_and_mutual_exclusion_are_detected(self):
        for route in ("focus", "invitation_early"):
            world = HostingWorld()
            world.complete(self.neutral, "NPT")
            world.effects["ac_ud_npt_accept_hosting"] = []
            self.host(world, route)
            with self.assertRaises(AssertionError):
                self.assert_hosted(world)
        world = HostingWorld()
        world.complete(self.neutral, "NPT")
        self.host(world, "focus")
        world.focuses[self.allied].append(["mutually_exclusive", "=", [["focus", "=", self.neutral]]])
        self.assertFalse(world.focus_available(self.allied))


if __name__ == "__main__":
    unittest.main(verbosity=2)
