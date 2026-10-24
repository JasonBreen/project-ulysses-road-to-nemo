"""Execute the shipped aftermath subset offline; this is not the HOI4 engine.

Unknown syntax fails closed. Tests cover state transitions and references, not
native parsing, AI focus selection, rendered layout, or save serialization.
"""
import argparse
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import re
import subprocess
import sys
import unittest

from economy_script import parse, fields

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"
TAGS = ("BLK", "OSE", "UST", "SAP", "GEB", "FAT", "REC", "SBK", "AWW")


def load(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


def mapping(nodes):
    return {key: value for key, _, value in nodes}


def day(value):
    return date(*map(int, value.split("."))).toordinal()


@dataclass
class Country:
    tag: str
    exists: bool = True
    subject: bool = False
    war: bool = False
    capitulated: bool = False
    flags: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    ideas: dict = field(default_factory=dict)
    focuses: set = field(default_factory=set)
    opinions: set = field(default_factory=set)
    pp: float = 0
    stability: float = 0
    war_support: float = 0
    army_xp: float = 0
    air_xp: float = 0
    econ_requests: int = 0


class World:
    def __init__(self, when="1995.6.21", outcome="defeat", fiscal=False):
        self.today = day(when)
        self.globals = {"ac_postwar_contract_started", "ac_postwar_" + outcome}
        self.countries = {tag: Country(tag, exists=tag != "AWW") for tag in TAGS}
        self.countries["BLK"].flags["ac_postwar_ready"] = None
        self.countries["BLK"].focuses.add("ac_postwar_reconstruction")
        self.fiscal = fiscal
        self.effects = mapping(load("common/scripted_effects/ac_pwi.txt"))
        self.triggers = mapping(load("common/scripted_triggers/ac_pwi.txt"))
        self.events = {mapping(v)["id"]: v for k, _, v in load("events/ac_pwi.txt") if k == "country_event"}
        self.focuses = {mapping(v)["id"]: v for k, _, v in load("common/national_focus/ac_pwi.txt") if k == "shared_focus"}
        self.decisions = mapping(load("common/decisions/ac_pwi.txt")[0][2])
        self.queue = []
        self.weekly = mapping(load("common/on_actions/ac_pwi.txt")[0][2])

    def flag(self, country, key):
        return key in country.flags and (country.flags[key] is None or country.flags[key] > self.today)

    def number(self, value, country):
        try:
            return float(value)
        except ValueError:
            if value not in country.variables:
                raise AssertionError("Read of uninitialized variable: " + value)
            return country.variables[value]

    def trigger(self, nodes, country):
        answers = []
        for key, operator, value in nodes:
            if key in self.triggers:
                answer = self.trigger(self.triggers[key], country) == (value == "yes")
            elif key in ("OR", "AND", "NOT"):
                parts = [self.trigger([part], country) for part in value]
                answer = any(parts) if key == "OR" else (not all(parts) if key == "NOT" else all(parts))
            elif key == "always":
                answer = value == "yes"
            elif key == "original_tag":
                answer = country.tag == value
            elif key == "has_country_flag":
                answer = self.flag(country, value)
            elif key == "has_global_flag":
                answer = value in self.globals
            elif key == "has_variable":
                answer = value in country.variables
            elif key == "has_idea":
                answer = value in country.ideas
            elif key in ("has_war", "has_capitulated", "is_subject"):
                answer = getattr(country, {"has_war": "war", "has_capitulated": "capitulated", "is_subject": "subject"}[key]) == (value == "yes")
            elif key == "country_exists":
                answer = self.countries[value].exists
            elif key in TAGS:
                answer = self.countries[key].exists and self.trigger(value, self.countries[key])
            elif key in ("check_variable", "date"):
                if key == "date":
                    left, comparison, right = self.today, operator, day(value)
                else:
                    name, comparison, operand = value[0]
                    left, right = self.number(name, country), self.number(operand, country)
                answer = {"=": left == right, ">": left > right, "<": left < right, ">=": left >= right, "<=": left <= right}[comparison]
            elif key == "ac_econ_ready":
                answer = self.fiscal == (value == "yes")
            else:
                raise AssertionError("Unsupported trigger: " + key)
            answers.append(answer)
        return all(answers)

    def execute(self, nodes, country):
        branch = None
        for key, operator, value in nodes:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise AssertionError("Orphaned " + key)
                condition = key == "else" or self.trigger(mapping(value)["limit"], country)
                if not branch and condition:
                    self.execute([node for node in value if node[0] != "limit"], country)
                    branch = True
                continue
            branch = None
            if key in self.effects:
                self.execute(self.effects[key], country)
            elif key in TAGS:
                if self.countries[key].exists:
                    self.execute(value, self.countries[key])
            elif key == "set_country_flag":
                if isinstance(value, list):
                    data = fields(value)
                    country.flags[data["flag"]] = self.today + int(data["days"])
                else:
                    country.flags[value] = None
            elif key == "clr_country_flag":
                country.flags.pop(value, None)
            elif key == "set_global_flag":
                self.globals.add(value)
            elif key == "clr_global_flag":
                self.globals.discard(value)
            elif key in ("set_variable", "add_to_variable"):
                name, _, operand = value[0]
                amount = self.number(operand, country)
                country.variables[name] = amount if key == "set_variable" else country.variables.get(name, 0) + amount
            elif key == "clamp_variable":
                data = fields(value)
                assert data["var"] in country.variables
                country.variables[data["var"]] = min(float(data["max"]), max(float(data["min"]), country.variables[data["var"]]))
            elif key == "country_event":
                data = fields(value)
                assert data["id"] in self.events, data["id"]
                self.queue.append((self.today + int(data.get("days", 0)), country.tag, data["id"]))
            elif key in ("add_ideas", "remove_ideas"):
                if key == "add_ideas":
                    country.ideas[value] = None
                else:
                    country.ideas.pop(value, None)
            elif key == "add_timed_idea":
                data = fields(value)
                country.ideas[data["idea"]] = self.today + int(data["days"])
            elif key in ("add_opinion_modifier", "remove_opinion_modifier"):
                data = fields(value)
                pair = (data["target"], data["modifier"])
                country.opinions.add(pair) if key == "add_opinion_modifier" else country.opinions.discard(pair)
            elif key in ("add_political_power", "add_stability", "add_war_support", "army_experience", "air_experience"):
                attr = {"add_political_power": "pp", "add_stability": "stability", "add_war_support": "war_support", "army_experience": "army_xp", "air_experience": "air_xp"}[key]
                setattr(country, attr, getattr(country, attr) + float(value))
            elif key == "ac_econ_set_reconstruction":
                assert self.fiscal, "Unguarded economy dependency"
                country.econ_requests += 1
            else:
                raise AssertionError("Unsupported effect: " + key)

    def run(self, effect, tag="BLK"):
        self.execute(self.effects[effect], self.countries[tag])

    def tick(self, tag=None):
        for tag in ([tag] if tag else TAGS[:-1]):
            if self.countries[tag].exists:
                self.execute(mapping(self.weekly["on_weekly_" + tag])["effect"], self.countries[tag])

    def start(self):
        self.tick()
        return self

    def focus_available(self, ident, tag="BLK"):
        country = self.countries[tag]
        nodes = self.focuses[ident]
        for key, _, value in nodes:
            if key == "prerequisite" and not any(focus in country.focuses for _, _, focus in value):
                return False
            if key == "mutually_exclusive" and any(focus in country.focuses for _, _, focus in value):
                return False
        return self.trigger(mapping(nodes)["available"], country)

    def complete(self, ident, tag="BLK"):
        assert self.focus_available(ident, tag), "Unavailable focus: " + ident
        country = self.countries[tag]
        country.focuses.add(ident)
        self.execute(mapping(self.focuses[ident])["completion_reward"], country)

    def choose(self, event, option=0, tag="BLK", stale=False):
        data = self.events[event]
        country = self.countries[tag]
        if not stale:
            assert self.trigger(mapping(data)["trigger"], country)
        options = [v for k, _, v in data if k == "option"]
        chosen = options[option]
        if "trigger" in mapping(chosen) and not stale:
            assert self.trigger(mapping(chosen)["trigger"], country)
        self.execute([n for n in chosen if n[0] not in ("name", "trigger", "ai_chance")], country)


class AftermathTests(unittest.TestCase):
    def test_nine_outcome_policy_routes_and_duplicate_completion(self):
        endings = {"defeat": ("obligations", "repair", "reform", "neighbors"), "victory": ("administration", "costs", "expectations", "dividend"), "wacht_am_wal": ("terms", "frontier", "recognition", "restraint")}
        for outcome, suffixes in endings.items():
            for policy in ("negotiated", "authoritarian", "revanchist"):
                with self.subTest(outcome=outcome, policy=policy):
                    world = World(outcome=outcome).start()
                    c = world.countries["BLK"]
                    c.flags["inherited_monarchy"] = None
                    for step in ("missing", "soldiers", "services", "powers", "commission", "program"):
                        world.complete("ac_pwi_" + step)
                    world.choose("ac_pwi.2")
                    world.choose("ac_pwi.3")
                    prefix = "wacht" if outcome == "wacht_am_wal" else outcome
                    for suffix in suffixes:
                        world.complete("ac_pwi_" + prefix + "_" + suffix)
                    self.assertFalse(world.focus_available("ac_pwi_" + policy + "_1"))
                    world.today += 91
                    for index in range(1, 5):
                        ident = "ac_pwi_" + policy + "_" + str(index)
                        world.complete(ident)
                        before = (dict(c.variables), c.pp, set(c.ideas))
                        world.execute(mapping(world.focuses[ident])["completion_reward"], c)
                        self.assertEqual(before, (c.variables, c.pp, set(c.ideas)))
                    self.assertTrue(world.flag(c, "ac_pwi_national_settlement"))
                    self.assertTrue(world.flag(c, "inherited_monarchy"))
                    self.assertEqual(1, sum(world.flag(c, "ac_pwi_path_" + p) for p in ("negotiated", "authoritarian", "revanchist")))
                    for other in ("negotiated", "authoritarian", "revanchist"):
                        if other != policy:
                            self.assertFalse(world.focus_available("ac_pwi_" + other + "_1"))

    def test_neutral_fallback_excludes_authoritarian_and_revanchist(self):
        world = World(outcome="unclassified").start()
        c = world.countries["BLK"]
        c.focuses.add("ac_pwi_program")
        world.today += 91
        self.assertTrue(world.focus_available("ac_pwi_negotiated_1"))
        self.assertFalse(world.focus_available("ac_pwi_authoritarian_1"))
        self.assertFalse(world.focus_available("ac_pwi_revanchist_1"))

    def test_relative_initialization_is_idempotent_and_war_waits(self):
        world = World()
        c = world.countries["BLK"]
        c.war = True
        world.tick("BLK")
        self.assertNotIn("ac_pwi_started", c.flags)
        c.war = False
        world.tick("BLK")
        c.variables["ac_pwi_recovery"] = 77
        deadline = c.flags["ac_pwi_first_quarter"]
        world.today += 7
        world.tick("BLK")
        self.assertEqual(77, c.variables["ac_pwi_recovery"])
        self.assertEqual(deadline, c.flags["ac_pwi_first_quarter"])

    def test_partner_routes_and_constrained_guarantor(self):
        for outcome in ("defeat", "victory", "wacht_am_wal"):
            for subject in (False, True):
                world = World(outcome=outcome).start()
                for tag in ("OSE", "UST", "SAP", "GEB"):
                    c = world.countries[tag]
                    c.subject = subject if tag == "UST" else False
                    available = [ident for ident in world.focuses if ident.startswith(tag + "_pwi_")]
                    for _ in range(10):
                        for ident in available:
                            if ident not in c.focuses and world.focus_available(ident, tag):
                                world.complete(ident, tag)
                    if tag == "OSE":
                        self.assertEqual(outcome == "defeat", "OSE_pwi_guarantor" in c.focuses)
                        self.assertNotEqual("OSE_pwi_dialogue" in c.focuses, "OSE_pwi_containment" in c.focuses)
                    if tag == "UST":
                        self.assertEqual(subject, "UST_pwi_subject" in c.focuses)
                        self.assertEqual(not subject, "UST_pwi_sovereignty" in c.focuses)
                    self.assertTrue(any(ident.endswith(("legacy", "dialogue", "containment")) for ident in c.focuses))

    def test_all_six_accords_accept_refuse_withdraw_timeout_and_invalidate(self):
        from build_peace_we_inherit import PAIRS
        for index, (sender, target) in enumerate(PAIRS):
            key = "ac_pwi_" + sender.lower() + "_" + target.lower()
            for result in ("accepted", "refused", "withdrawn", "timeout", "invalid"):
                with self.subTest(pair=key, result=result):
                    world = World().start()
                    world.run(key + "_send", sender)
                    self.assertIn(key + "_pending", world.globals)
                    before = dict(world.countries[sender].variables)
                    if result == "accepted":
                        world.choose("ac_pwi.%s" % (100 + index * 4), tag=target)
                    elif result == "refused":
                        world.choose("ac_pwi.%s" % (100 + index * 4), option=1, tag=target)
                    elif result == "withdrawn":
                        world.run(key + "_withdrawn", sender)
                    elif result == "timeout":
                        world.today += 61
                        world.run(key + "_tick", sender)
                    else:
                        world.countries[target].exists = False
                        world.run(key + "_tick", sender)
                    self.assertIn(key + "_" + result, world.globals)
                    self.assertNotIn(key + "_pending", world.globals)
                    after = dict(world.countries[sender].variables)
                    world.choose("ac_pwi.%s" % (100 + index * 4), tag=target, stale=True)
                    self.assertEqual(after, world.countries[sender].variables)
                    if result != "accepted":
                        self.assertEqual(before, after)

    def test_subject_war_capitulation_and_annexation_block_offers(self):
        for attr in ("subject", "war", "capitulated", "exists"):
            world = World().start()
            setattr(world.countries["UST"], attr, attr != "exists")
            world.run("ac_pwi_ose_ust_send", "OSE")
            self.assertNotIn("ac_pwi_ose_ust_pending", world.globals)

    def test_partner_lost_after_acceptance_is_not_relief_bonus(self):
        world = World(when="1999.7.1").start()
        world.run("ac_pwi_blk_ose_send")
        world.run("ac_pwi_blk_ose_accept", "OSE")
        world.countries["OSE"].war = True
        c = world.countries["BLK"]
        c.variables["ac_pwi_preparedness"] = 45
        world.today = day("1999.7.8")
        world.tick("BLK")
        self.assertNotIn("ac_pwi_blk_ose_active", world.globals)
        self.assertEqual(45, c.variables["ac_pwi_relief_capacity"])
        self.assertNotIn(("OSE", "ac_pwi_reconstruction_accord"), c.opinions)

    def test_expired_acceptance_fails_before_the_next_weekly_cleanup(self):
        world = World().start()
        world.run("ac_pwi_blk_ose_send")
        world.today += 61
        world.choose("ac_pwi.100", tag="OSE", stale=True)
        self.assertNotIn("ac_pwi_blk_ose_accepted", world.globals)
        world.choose("ac_pwi.100", tag="OSE", option=1, stale=True)
        self.assertIn("ac_pwi_blk_ose_timeout", world.globals)

    def test_target_cleans_up_a_pending_offer_after_sender_annexation(self):
        world = World().start()
        world.run("ac_pwi_blk_ose_send")
        world.countries["BLK"].exists = False
        world.tick("OSE")
        self.assertIn("ac_pwi_blk_ose_invalid", world.globals)
        self.assertNotIn("ac_pwi_blk_ose_pending", world.globals)

    def test_the_wrong_country_cannot_send_or_accept_an_offer(self):
        world = World().start()
        world.run("ac_pwi_blk_ose_send", "UST")
        self.assertNotIn("ac_pwi_blk_ose_pending", world.globals)
        world.run("ac_pwi_blk_ose_send")
        world.run("ac_pwi_blk_ose_accept", "UST")
        self.assertNotIn("ac_pwi_blk_ose_accepted", world.globals)

    def test_calendar_does_not_wait_for_settlement_or_peace(self):
        world = World(when="1996.4.19")
        world.globals.clear()
        world.countries["BLK"].war = True
        world.tick("BLK")
        world.today = day("1996.4.20")
        world.tick("BLK")
        self.assertTrue(world.flag(world.countries["BLK"], "ac_pwi_warning_seen"))
        world.today = day("1999.7.8")
        world.tick("BLK")
        c = world.countries["BLK"]
        self.assertTrue(world.flag(c, "ac_pwi_crisis_resolved"))
        self.assertNotIn("ac_pwi_started", c.flags)
        before = len(world.queue)
        world.tick("BLK")
        self.assertEqual(before, len(world.queue))

    def test_late_calendar_does_not_replay_milestones_or_grant_relief(self):
        world = World(when="2000.1.1").start()
        c = world.countries["BLK"]
        self.assertTrue(world.flag(c, "ac_pwi_late_calendar"))
        self.assertEqual(0, c.variables["ac_pwi_relief_capacity"])
        self.assertFalse(any(item[2] in ("ac_pwi.70", "ac_pwi.71", "ac_pwi.72") for item in world.queue))
        self.assertTrue(world.flag(c, "ac_pwi_started"))

    def test_preparedness_and_recovery_and_partner_have_distinct_payoffs(self):
        for preparedness, recovery, partner, resilient in ((0, 20, False, False), (45, 20, False, False), (45, 70, True, True), (60, 20, False, True)):
            world = World(when="1999.7.1").start()
            c = world.countries["BLK"]
            c.variables.update(ac_pwi_preparedness=preparedness, ac_pwi_recovery=recovery)
            if partner:
                world.globals.add("ac_pwi_blk_ose_active")
            world.today = day("1999.7.8")
            world.tick("BLK")
            self.assertEqual(resilient, world.flag(c, "ac_pwi_relief_resilient"))
            before = dict(c.variables)
            world.run("ac_pwi_resolve_ulysses")
            self.assertEqual(before, c.variables)

    def test_capacity_lock_and_no_post_crisis_preparation(self):
        world = World(when="1996.4.20").start()
        c = world.countries["BLK"]
        civil = mapping(world.decisions["ac_pwi_civil_defense"])
        ready = mapping(world.decisions["ac_pwi_readiness"])
        self.assertTrue(world.trigger(civil["available"], c))
        world.execute(civil["complete_effect"], c)
        world.execute(civil["complete_effect"], c)
        self.assertEqual(25, c.variables["ac_pwi_preparedness"])
        self.assertFalse(world.trigger(ready["available"], c))
        world.today += 181
        self.assertTrue(world.trigger(ready["available"], c))
        world.today = day("1999.7.8")
        self.assertFalse(world.trigger(ready["available"], c))

    def test_economy_on_and_off_recovery_decision(self):
        for fiscal in (False, True):
            world = World(fiscal=fiscal).start()
            c = world.countries["BLK"]
            world.execute(mapping(world.decisions["ac_pwi_repair_program"])["complete_effect"], c)
            self.assertEqual(28, c.variables["ac_pwi_recovery"])
            self.assertEqual(int(fiscal), c.econ_requests)

    def test_clamps_and_no_periodic_drift(self):
        world = World().start()
        c = world.countries["BLK"]
        c.variables.update(ac_pwi_recovery=999, ac_pwi_confidence=-20, ac_pwi_tension=200)
        world.run("ac_pwi_bound_pressures")
        self.assertEqual((100, 0, 100), tuple(c.variables["ac_pwi_" + name] for name in ("recovery", "confidence", "tension")))
        before = dict(c.variables)
        world.today += 7
        world.tick("BLK")
        self.assertEqual(before, c.variables)
        c.variables.pop("ac_pwi_recovery")
        world.run("ac_pwi_bound_pressures")  # absent variables must not be clamped

    def test_aww_observed_only_and_no_second_spawn(self):
        world = World().start()
        world.countries["AWW"].exists = True
        world.tick("BLK")
        world.tick("BLK")
        self.assertEqual(1, sum(item[2] == "ac_pwi.74" for item in world.queue))
        self.assertFalse(any(item[2].startswith("awwnb.") for item in world.queue))

    def test_delayed_cabinet_choice_waits_for_peace_and_is_not_lost(self):
        world = World().start()
        c = world.countries["BLK"]
        c.war = True
        before = dict(c.variables)
        world.choose("ac_pwi.2")
        self.assertEqual(before, c.variables)
        world.choose("ac_pwi.2", option=1, stale=True)
        c.war = False
        world.tick("BLK")
        self.assertEqual(before["ac_pwi_recovery"] + 10, c.variables["ac_pwi_recovery"])
        after = dict(c.variables)
        world.tick("BLK")
        self.assertEqual(after, c.variables)

    def test_source_contract_and_all_new_localization(self):
        world = World()
        self.assertEqual(58, len(world.focuses))
        self.assertEqual(30, sum(ident.startswith("ac_pwi_") for ident in world.focuses))
        loc_path = MOD / "localisation/english/ac_pwi_l_english.yml"
        self.assertTrue(loc_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        keys = re.findall(r'^\s*([A-Za-z0-9_.]+):0\s+"', loc_path.read_text(encoding="utf-8-sig"), re.M)
        self.assertEqual(len(keys), len(set(keys)))
        for ident in world.focuses:
            self.assertIn(ident, keys)
            self.assertIn(ident + "_desc", keys)
        for ident in world.decisions:
            self.assertIn(ident, keys)
            self.assertIn(ident + "_desc", keys)
        for ident, nodes in world.events.items():
            data = mapping(nodes)
            self.assertIn(data["title"], keys)
            self.assertIn(data["desc"], keys)
            for kind, _, option in nodes:
                if kind == "option":
                    self.assertIn(mapping(option)["name"], keys)
        new_text = "\n".join(path.read_text(encoding="utf-8-sig") for path in MOD.rglob("ac_pwi.txt"))
        for forbidden in ("declare_war_on", "add_wargoal", "transfer_state", "annex_country", "set_politics", "load_focus_tree", "every_country", "every_state", "launch_nuke"):
            self.assertNotRegex(new_text, r"\b" + forbidden + r"\s*=")
        self.assertNotIn("awwnb.1", new_text)

    def test_imports_and_focus_coordinates(self):
        world = World()
        for filename, tag, expected in (("ac_belkan_campaign.txt", "BLK", 1), ("OSE.txt", "OSE", 2), ("UST.txt", "UST", 3), ("SAP.txt", "SAP", 1), ("GEB.txt", "GEB", 1)):
            trees = [v for k, _, v in load("common/national_focus/" + filename) if k == "focus_tree"]
            if tag == "BLK":
                trees = [v for v in trees if mapping(v)["id"] == "ac_belkan_postwar"]
            self.assertEqual(expected, len(trees))
            for tree in trees:
                imports = [v for k, _, v in tree if k == "shared_focus"]
                expected_ids = [ident for ident in world.focuses if ident.startswith("ac_pwi_" if tag == "BLK" else tag + "_pwi_")]
                self.assertTrue(set(expected_ids).issubset(imports))
        coords = {}
        for ident, nodes in world.focuses.items():
            data = mapping(nodes)
            tag = "BLK" if ident.startswith("ac_pwi_") else ident[:3]
            coordinate = (tag, int(data["x"]), int(data["y"]))
            self.assertNotIn(coordinate, coords, (ident, coords.get(coordinate)))
            coords[coordinate] = ident

    def test_generated_files_match_authoring_source(self):
        subprocess.run([sys.executable, str(ROOT / "tools/build_peace_we_inherit.py"), "--check"], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=MOD)
    args, remaining = parser.parse_known_args()
    MOD = args.mod_root.resolve()
    unittest.main(argv=[sys.argv[0]] + remaining)
