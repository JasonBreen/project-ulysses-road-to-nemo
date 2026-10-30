"""Execute the shipped Continental War subset offline; this is not the HOI4 engine.

Unknown syntax fails closed. Tests cover state transitions, routes and
references, not native parsing, AI behaviour, battles or save serialization.
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
TAGS = ("ERU", "FCU", "SNS", "AMB", "UGE", "DEL", "NPT")
CONTRACT_SET = ("ac_ucw_calendar_started", "ac_ucw_war_started", "ac_ucw_isaf_formed", "ac_ucw_stonehenge_seized",
                "ac_ucw_stonehenge_destroyed", "ac_ucw_megalith_active", "ac_ucw_megalith_destroyed",
                "ac_ucw_outcome_isaf_victory", "ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_stalemate", "ac_ucw_2005_assessed")
CONTRACT_READ = ("ac_sp_stonehenge_complete", "ac_npt_hosts_isaf")
OUTCOMES = ("ac_ucw_outcome_isaf_victory", "ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_stalemate")


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
    ai: bool = True
    capitulated: bool = False
    subject: bool = False
    bonuses: list = field(default_factory=list)
    opinions: list = field(default_factory=list)
    flags: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    ideas: dict = field(default_factory=dict)
    focuses: set = field(default_factory=set)
    tree: str = ""
    faction_name: str = ""
    misc: float = 0


class World:
    def __init__(self, when="1999.12.1", rule=False, fiscal=False):
        self.today = day(when)
        self.globals = set()
        self.countries = {tag: Country(tag) for tag in TAGS}
        self.faction = {"FCU": "FCU", "AMB": "FCU", "UGE": "FCU", "SNS": "FCU", "DEL": "FCU"}
        self.wars = set()
        self.controllers = {310: "SNS"}
        self.rule = rule
        self.fiscal = fiscal
        self.effects = mapping(load("common/scripted_effects/ac_ucw.txt"))
        self.triggers = mapping(load("common/scripted_triggers/ac_ucw.txt"))
        self.events = {mapping(v)["id"]: (k, v) for k, _, v in load("events/ac_ucw.txt") if k in ("country_event", "news_event")}
        self.focuses = {}
        for tag in ("ERU", "FCU"):
            tree = load("common/national_focus/%s.txt" % tag)[0][2]
            self.focuses.update({mapping(v)["id"]: v for k, _, v in tree if k == "focus"})
        self.decisions = {}
        for category, _, rows in load("common/decisions/ac_ucw.txt"):
            self.decisions.update({k: v for k, _, v in rows})
        self.queue = []
        self.news = []
        self.weekly = mapping(load("common/on_actions/ac_ucw.txt")[0][2])

    def at_war(self, a, b):
        return frozenset((a, b)) in self.wars

    def flag(self, country, key):
        return key in country.flags and (country.flags[key] is None or country.flags[key]>self.today)

    def number(self, value, country):
        try:
            return float(value)
        except ValueError:
            owner, name = (value.split(".", 1) if "." in value else (None, value))
            source = self.countries[owner] if owner else country
            if name not in source.variables:
                raise AssertionError("Read of uninitialized variable: " + value)
            return source.variables[name]

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
            elif key == "has_capitulated":
                answer = country.capitulated == (value == "yes")
            elif key == 'is_subject':
                answer = country.subject == (value == 'yes')
            elif key == 'has_war':
                answer = any(country.tag in war for war in self.wars) == (value == 'yes')
            elif key == "is_ai":
                answer = country.ai == (value == "yes")
            elif key == "has_war_with":
                answer = self.at_war(country.tag, value)
            elif key == "is_in_faction_with":
                answer = country.tag in self.faction and self.faction.get(country.tag) == self.faction.get(value)
            elif key == "is_faction_leader":
                answer = (self.faction.get(country.tag) == country.tag) == (value == "yes")
            elif key == "country_exists":
                answer = self.countries[value].exists
            elif key == "has_game_rule":
                data = fields(value)
                assert data == {"rule": "ac_playtest_shortcuts", "option": "enabled"}, data
                answer = self.rule
            elif key.isdigit():
                (inner, _, target), = value
                assert inner == "is_controlled_by", inner
                answer = self.controllers[int(key)] == (country.tag if target == "ROOT" else target)
            elif key in self.countries:
                answer = self.countries[key].exists and self.trigger(value, self.countries[key])
            elif key in ("check_variable", "date"):
                if key == "date":
                    left, comparison, right = self.today, operator, day(value)
                else:
                    name, comparison, operand = value[0]
                    left, right = self.number(name, country), self.number(operand, country)
                answer = {"=": left == right, ">": left > right, "<": left < right}[comparison]
            elif key == "ac_econ_ready":
                answer = self.fiscal == (value == "yes")
            else:
                raise AssertionError("Unsupported trigger: " + key)
            answers.append(answer)
        return all(answers)

    def declare(self, attacker, target):
        attackers = [t for t, leader in self.faction.items() if leader == self.faction.get(attacker)] or [attacker]
        defenders = [t for t, leader in self.faction.items() if leader == self.faction.get(target)] or [target]
        for a in attackers:
            for d in defenders:
                self.wars.add(frozenset((a, d)))

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
                if value == "yes":
                    self.execute(self.effects[key], country)
            elif key in self.countries:
                if self.countries[key].exists:
                    self.execute(value, self.countries[key])
            elif key == "set_country_flag":
                if isinstance(value,list):
                    data=fields(value);country.flags[data['flag']]=self.today+int(data['days'])
                else:country.flags[value] = None
            elif key == "set_global_flag":
                self.globals.add(value)
            elif key == "clr_country_flag":
                country.flags.pop(value,None)
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
            elif key in ("country_event", "news_event"):
                data = fields(value)
                assert data["id"] in self.events, data["id"]
                assert self.events[data["id"]][0] == key, (key, data["id"])
                (self.queue if key == "country_event" else self.news).append((self.today + int(data.get("days", 0)), country.tag, data["id"]))
            elif key in ("add_ideas", "remove_ideas"):
                if key == "add_ideas":
                    country.ideas[value] = None
                else:
                    country.ideas.pop(value, None)
            elif key == "add_timed_idea":
                country.ideas[fields(value)["idea"]] = None
            elif key == "add_opinion_modifier":
                assert fields(value)["modifier"] in ("ac_ucw_mediation", 'ac_exp_scientific_exchange')
                country.opinions.append(fields(value))
            elif key == 'add_tech_bonus':
                data=fields(value)
                assert data['category'] in ('industry','electronics')
                assert int(data['uses']) == 1 and 0 < float(data['bonus']) <= 1
                country.bonuses.append(data)
            elif key in ("add_political_power", "add_stability", "add_war_support", "army_experience", "air_experience", "navy_experience", 'add_manpower'):
                country.misc += float(value)
            elif key == "ac_econ_set_reconstruction":
                assert self.fiscal, "Unguarded economy dependency"
            elif key == "custom_effect_tooltip":
                assert isinstance(value, str) and value, "Empty explanatory tooltip"
            elif key == "load_focus_tree":
                country.tree = fields(value)["tree"]
            elif key == "declare_war_on":
                data = fields(value)
                assert data["type"] in ("annex_everything", "topple_government"), data
                self.declare(country.tag, data["target"])
            elif key == "white_peace":
                self.wars.discard(frozenset((country.tag, value)))
            elif key == "set_faction_name":
                country.faction_name = value
            elif key == "add_to_faction":
                self.faction[value] = self.faction.get(country.tag, country.tag)
            else:
                raise AssertionError("Unsupported effect: " + key)

    def run(self, effect, tag):
        self.execute(self.effects[effect], self.countries[tag])

    def tick(self, tags=TAGS):
        for tag in tags:
            if self.countries[tag].exists:
                self.execute(mapping(self.weekly["on_weekly_" + tag])["effect"], self.countries[tag])

    def weeks(self, count, tags=TAGS):
        for _ in range(count):
            self.today += 7
            self.tick(tags)
            self.drain()

    def drain(self):
        """Answer due country events with their AI-preferred option; later ones wait."""
        while True:
            due = [item for item in self.queue if item[0] <= self.today]
            if not due:
                return
            item = min(due, key=lambda entry: entry[0])
            self.queue.remove(item)
            _, tag, ident = item
            if self.countries[tag].exists:
                self.choose(ident, tag=tag, option=self.preferred(ident,tag))

    def preferred(self, ident, tag='ERU'):
        options = [v for k, _, v in self.events[ident][1] if k == "option"]
        weights = [float(fields(mapping(o)["ai_chance"])["factor"]) if self.trigger(mapping(o).get('trigger',[]),self.countries[tag]) else -1 for o in options]
        return weights.index(max(weights))

    def options(self, ident):
        return [v for k, _, v in self.events[ident][1] if k == "option"]

    def choose(self, ident, option=0, tag="ERU"):
        country = self.countries[tag]
        chosen = self.options(ident)[option]
        if "trigger" in mapping(chosen) and not self.trigger(mapping(chosen)["trigger"], country):
            return
        self.execute([n for n in chosen if n[0] not in ("name", "trigger", "ai_chance")], country)

    def available(self, ident, tag):
        data = mapping(self.decisions[ident])
        country = self.countries[tag]
        return all(self.trigger(data[part], country) for part in ("allowed", "visible", "available"))

    def take(self, ident, tag):
        assert self.available(ident, tag), "Unavailable decision: " + ident
        self.execute(mapping(self.decisions[ident])["complete_effect"], self.countries[tag])

    def focus_available(self, ident, tag):
        country = self.countries[tag]
        nodes = self.focuses[ident]
        for key, _, value in nodes:
            if key == "prerequisite" and not any(focus in country.focuses for _, _, focus in value):
                return False
            if key == "mutually_exclusive" and any(focus in country.focuses for _, _, focus in value):
                return False
        return self.trigger(mapping(nodes)["available"], country)

    def complete(self, ident, tag):
        assert self.focus_available(ident, tag), "Unavailable focus: " + ident
        self.countries[tag].focuses.add(ident)
        self.execute(mapping(self.focuses[ident])["completion_reward"], self.countries[tag])

    def outcome(self):
        return [flag for flag in OUTCOMES if flag in self.globals]

    def news_ids(self):
        return [item[2] for item in self.news]


def started(when="1999.12.8", **kwargs):
    world = World(when, **kwargs)
    world.tick()
    world.drain()
    return world


def at_war(when="2003.6.22", **kwargs):
    world = started("1999.12.8", **kwargs)
    world.today = day(when) - 7
    world.weeks(1)
    assert "ac_ucw_war_started" in world.globals
    return world


class ContinentalWarTests(unittest.TestCase):
    def test_calendar_starts_after_1999_assessment_and_loads_trees(self):
        world = World("1999.11.30")
        world.tick()
        self.assertNotIn("ac_ucw_calendar_started", world.globals)
        world = started()
        self.assertIn("ac_ucw_stonehenge_operational", world.globals)
        self.assertEqual("ac_ucw_eru_tree", world.countries["ERU"].tree)
        self.assertEqual("ac_ucw_fcu_tree", world.countries["FCU"].tree)
        self.assertEqual("", world.countries["SNS"].tree)
        self.assertEqual(45, world.countries["ERU"].variables["ac_ucw_grievance"])
        before = dict(world.countries["ERU"].variables)
        world.weeks(1)
        self.assertEqual(before, world.countries["ERU"].variables, "Indices must not drift weekly")

    def test_pwi_relief_outcome_seeds_pressure(self):
        world = World()
        world.countries["SNS"].flags["ac_pwi_relief_strained"] = None
        world.countries["AMB"].flags["ac_pwi_relief_resilient"] = None
        world.tick()
        self.assertEqual(55, world.countries["SNS"].variables["ac_ucw_pressure"])
        self.assertEqual(25, world.countries["AMB"].variables["ac_ucw_pressure"])

    def test_refugee_closure_canonical_and_alternative(self):
        for option, flag in ((0, "ac_ucw_border_closed"), (1, "ac_ucw_border_open")):
            world = started()
            world.today = day("2000.4.21")
            world.tick()
            self.assertEqual([(world.today + 1, "ERU")], [(d, tag) for d, tag, ident in world.queue if ident == "ac_ucw.10"])
            world.queue.clear()
            world.choose("ac_ucw.10", option)
            self.assertIn(flag, world.globals)
            self.assertEqual(option == 0, "ac_ucw.12" in world.news_ids())
        world = started()
        world.today = day("2000.4.21")
        world.tick()
        world.tick()
        self.assertEqual(1, sum(item[2] == "ac_ucw.10" for item in world.queue))

    def test_late_load_marks_milestones_and_never_replays_them(self):
        world = started("2005.3.1")
        self.assertIn("ac_ucw_late_calendar", world.globals)
        self.assertIn("ac_ucw_brief_shezna_done", world.globals)
        self.assertNotIn("ac_ucw_brief_whiskey_done", world.globals)
        self.assertNotIn("ac_ucw.10", [item[2] for item in world.queue])
        world.weeks(30)
        self.assertNotIn("ac_ucw_war_started", world.globals, "AI must not start the war on a late calendar")

    def test_ai_starts_war_in_summer_2003_window_and_faction_defends(self):
        world = started()
        world.today = day("2003.6.13")
        world.tick()
        self.assertNotIn("ac_ucw_war_started", world.globals)
        world = at_war()
        for tag in ("SNS", "FCU", "AMB", "UGE", "DEL"):
            self.assertTrue(world.at_war("ERU", tag), tag)
        self.assertIn("ac_ucw_eru_war_footing", world.countries["ERU"].ideas)
        self.assertIn("ac_ucw.20", world.news_ids())

    def test_low_grievance_keeps_the_ai_from_war(self):
        world = started()
        world.countries["ERU"].variables["ac_ucw_grievance"] = 20
        world.today = day("2003.7.1")
        world.tick()
        self.assertNotIn("ac_ucw_war_started", world.globals)

    def test_human_escalation_allows_an_early_invasion(self):
        world = started()
        eru = world.countries["ERU"]
        eru.ai = False
        world.today = day("2002.1.10")
        self.assertFalse(world.available("ac_ucw_eru_invade_san_salvacion", "ERU"))
        eru.variables["ac_ucw_grievance"] = 75
        eru.flags["ac_ucw_eru_mobilized"] = None
        world.take("ac_ucw_eru_war_plan", "ERU")
        world.take("ac_ucw_eru_invade_san_salvacion", "ERU")
        self.assertIn("ac_ucw_war_started", world.globals)
        self.assertFalse(world.available("ac_ucw_eru_invade_san_salvacion", "ERU"))

    def test_continental_accord_averts_the_war(self):
        world = started()
        eru = world.countries["ERU"]
        eru.ai = False
        world.today = day("2002.6.1")
        eru.variables["ac_ucw_grievance"] = 20
        world.take("ac_ucw_eru_continental_accord", "ERU")
        self.assertIn("ac_ucw_war_averted", world.globals)
        self.assertIn("ac_ucw.25", world.news_ids())
        eru.ai = True
        world.today = day("2003.7.1")
        world.weeks(4)
        self.assertNotIn("ac_ucw_war_started", world.globals)
        world.today = day("2005.1.1")
        world.weeks(1)
        self.assertIn("ac_ucw_2005_assessed", world.globals)
        self.assertEqual([], world.outcome())

    def test_mediation_is_answered_both_ways(self):
        for option, delta, reply in ((0, -10, "ac_ucw.14"), (1, 5, "ac_ucw.15")):
            world = started()
            world.take("ac_ucw_fcu_mediate", "FCU")
            world.queue.clear()
            world.choose("ac_ucw.13", option)
            self.assertEqual(45 + delta, world.countries["ERU"].variables["ac_ucw_grievance"])
            self.assertEqual(reply, world.queue[-1][2])

    def test_full_ai_war_reaches_each_stage_once_in_order(self):
        world = at_war()
        world.controllers[310] = "ERU"
        world.weeks(14)
        self.assertIn("ac_ucw_stonehenge_seized", world.globals)
        self.assertIn("ac_ucw_stonehenge_railguns", world.countries["ERU"].ideas)
        self.assertIn("ac_ucw_isaf_formed", world.globals)
        self.assertEqual("ac_ucw_isaf_faction", world.countries["FCU"].faction_name)
        self.assertIn("ac_ucw_stage_los_canas", world.globals)
        self.assertEqual("FCU", world.faction.get("NPT"), "NPT accepted the AI invitation")
        world.weeks(60)
        self.assertIn("ac_ucw_stage_north_point", world.globals)
        self.assertIn("ac_ucw_npt_isaf_rear_base", world.countries["NPT"].ideas)
        world.weeks(40)
        for stage in ("counteroffensive", "stonehenge"):
            self.assertIn("ac_ucw_stage_" + stage, world.globals)
        self.assertIn("ac_ucw_stonehenge_destroyed", world.globals)
        self.assertNotIn("ac_ucw_stonehenge_railguns", world.countries["ERU"].ideas)
        self.assertNotIn("ac_ucw_under_stonehenge", world.countries["FCU"].ideas)
        for news in ("ac_ucw.40", "ac_ucw.41", "ac_ucw.42", "ac_ucw.43", "ac_ucw.44"):
            self.assertEqual(1, world.news_ids().count(news), news)
        self.assertEqual({"ac_ucw_isaf_command", "ac_ucw_isaf_counteroffensive"}, {i for i in world.countries["FCU"].ideas if i.startswith("ac_ucw_isaf")})
        self.assertLessEqual(world.countries["FCU"].variables["ac_ucw_stage_weeks"], 520)

    def test_lost_stonehenge_removes_the_completed_project_battery(self):
        world = at_war()
        world.countries["FCU"].ideas["ac_sp_stonehenge_battery"] = None
        world.controllers[310] = "ERU"
        world.weeks(1)
        self.assertIn("ac_ucw_stonehenge_seized", world.globals)
        self.assertNotIn("ac_sp_stonehenge_battery", world.countries["FCU"].ideas, "seizure")
        world.countries["FCU"].ideas["ac_sp_stonehenge_battery"] = None
        world.controllers[310] = "SNS"
        world.weeks(1)
        self.assertIn("ac_ucw_stonehenge_destroyed", world.globals)
        self.assertNotIn("ac_sp_stonehenge_battery", world.countries["FCU"].ideas, "destruction")

    def test_stonehenge_custody_closes_once_the_battery_is_lost(self):
        world = started()
        world.complete("FCU_ucw_after_ulysses", "FCU")
        self.assertTrue(world.focus_available("FCU_ucw_stonehenge_custody", "FCU"))
        world.take("ac_ucw_fcu_garrison_stonehenge", "FCU")
        self.assertIn("ac_ucw_stonehenge_garrison", world.countries["SNS"].ideas)
        world = at_war()
        world.complete("FCU_ucw_after_ulysses", "FCU")
        world.countries["SNS"].ideas["ac_ucw_stonehenge_garrison"] = None
        world.controllers[310] = "ERU"
        world.weeks(1)
        self.assertNotIn("ac_ucw_stonehenge_garrison", world.countries["SNS"].ideas, "seizure ends the garrison")
        self.assertFalse(world.focus_available("FCU_ucw_stonehenge_custody", "FCU"), "seized")
        world.controllers[310] = "SNS"
        world.weeks(1)
        self.assertIn("ac_ucw_stonehenge_destroyed", world.globals)
        self.assertFalse(world.focus_available("FCU_ucw_stonehenge_custody", "FCU"), "destroyed")
        self.assertNotIn("ac_ucw_stonehenge_garrison", world.countries["SNS"].ideas)

    def test_stage_counter_is_clamped(self):
        world = at_war()
        world.weeks(14)
        world.countries["FCU"].ai = False
        world.countries["FCU"].variables["ac_ucw_stage_weeks"] = 519
        world.weeks(3)
        self.assertEqual(520, world.countries["FCU"].variables["ac_ucw_stage_weeks"])

    def test_human_isaf_takes_stage_decisions(self):
        world = at_war()
        world.countries["FCU"].ai = False
        world.weeks(12)
        self.assertNotIn("ac_ucw_stage_los_canas", world.globals)
        world.take("ac_ucw_order_los_canas", "FCU")
        self.assertFalse(world.available("ac_ucw_order_los_canas", "FCU"))
        self.assertFalse(world.available("ac_ucw_order_north_point", "FCU"))
        world.weeks(26)
        world.take("ac_ucw_order_north_point", "FCU")
        self.assertIn("ac_ucw_stage_north_point", world.globals)

    def test_ground_recapture_destroys_stonehenge(self):
        world = at_war()
        world.controllers[310] = "ERU"
        world.weeks(1)
        self.assertIn("ac_ucw_stonehenge_seized", world.globals)
        world.controllers[310] = "FCU"
        world.weeks(1)
        self.assertIn("ac_ucw_stonehenge_destroyed", world.globals)
        self.assertIn("ac_ucw_stage_stonehenge", world.globals, "Ground recapture completes the stage")
        self.assertEqual(1, world.news_ids().count("ac_ucw.44"))

    def test_north_point_without_host_flag_is_reinvited(self):
        world = at_war()
        world.weeks(14)
        world.faction.pop("NPT", None)
        world.countries["FCU"].ai = False
        world.countries["FCU"].variables["ac_ucw_stage_weeks"] = 30
        world.take("ac_ucw_order_north_point", "FCU")
        self.assertIn(("NPT", "ac_ucw.32"), [(item[1], item[2]) for item in world.queue])
        self.assertNotIn("ac_ucw_npt_isaf_rear_base", world.countries["NPT"].ideas)
        host = at_war()
        host.weeks(14)
        host.faction.pop("NPT", None)
        host.countries["NPT"].flags["ac_npt_hosts_isaf"] = None
        host.countries["FCU"].variables["ac_ucw_stage_weeks"] = 60
        host.weeks(1)
        self.assertIn("ac_ucw_npt_isaf_rear_base", host.countries["NPT"].ideas)

    def test_isaf_victory_megalith_and_assessment(self):
        world = at_war()
        world.weeks(5)
        world.countries["ERU"].ideas["ac_sp_megalith_fortress"] = None
        world.countries["ERU"].capitulated = True
        world.weeks(1)
        self.assertEqual(["ac_ucw_outcome_isaf_victory"], world.outcome())
        self.assertNotIn("ac_ucw_2005_assessed", world.globals)
        world.weeks(2)
        self.assertIn("ac_ucw_megalith_active", world.globals, "Megalith follows the surrender by a week")
        self.assertNotIn("ac_ucw_megalith_destroyed", world.globals)
        self.assertNotIn("ac_ucw_2005_assessed", world.globals, "No assessment while Megalith is held")
        world.weeks(2)
        self.assertIn("ac_ucw_megalith_destroyed", world.globals)
        self.assertNotIn("ac_ucw_megalith_active", world.globals)
        self.assertIn("ac_ucw_eru_provisional_government", world.countries["ERU"].ideas)
        self.assertNotIn("ac_sp_megalith_fortress", world.countries["ERU"].ideas, "completed project spirit ends with Megalith")
        world.weeks(1)
        self.assertIn("ac_ucw_2005_assessed", world.globals)
        self.assertEqual(["ac_ucw_outcome_isaf_victory"], world.outcome())

    def test_erusean_victory_and_annexed_erusea(self):
        world = at_war()
        world.weeks(5)
        world.countries["FCU"].capitulated = True
        world.weeks(1)
        self.assertEqual(["ac_ucw_outcome_erusean_victory"], world.outcome())
        world = at_war()
        world.weeks(5)
        world.countries["ERU"].exists = False
        world.weeks(1)
        self.assertEqual(["ac_ucw_outcome_isaf_victory"], world.outcome())

    def test_armistice_ends_every_front_as_stalemate(self):
        world = at_war()
        world.weeks(14)
        world.countries["ERU"].ai = False
        world.queue.clear()
        world.take("ac_ucw_fcu_offer_armistice", "FCU")
        world.queue.clear()
        world.choose("ac_ucw.46", 0, "ERU")
        self.assertEqual(["ac_ucw_outcome_stalemate"], world.outcome())
        self.assertFalse(any("ERU" in pair for pair in world.wars))
        self.assertIn("ac_ucw_stage_los_canas", world.globals)
        self.assertEqual([], [i for i in world.countries["FCU"].ideas if i.startswith(("ac_ucw_isaf", "ac_ucw_under"))])
        self.assertNotIn("ac_ucw_eru_war_footing", world.countries["ERU"].ideas)
        world.weeks(2)
        self.assertIn("ac_ucw_2005_assessed", world.globals)
        self.assertEqual(1, len(world.outcome()))

    def test_peace_made_elsewhere_is_recorded_as_stalemate_only_after_isaf(self):
        world = at_war()
        world.wars.discard(frozenset(("ERU", "FCU")))
        world.today = day("2003.6.28")
        world.tick(("ERU",))
        self.assertEqual([], world.outcome())
        world = at_war()
        world.weeks(14)
        world.wars.discard(frozenset(("ERU", "FCU")))
        world.weeks(1)
        self.assertEqual(["ac_ucw_outcome_stalemate"], world.outcome())

    def test_briefs_follow_the_war_state(self):
        world = at_war()
        world.controllers[310] = "ERU"
        world.today = day("2005.8.20")
        world.weeks(1)
        self.assertFalse(any(item.startswith("ac_ucw.7") for item in world.news_ids()), "Briefs need the war stage")
        world = at_war()
        world.controllers[310] = "ERU"
        world.weeks(110)
        world.today = max(world.today, day("2005.8.16"))
        world.weeks(1)
        ids = world.news_ids()
        for number in (70, 71, 72, 73, 74, 75, 77):
            self.assertEqual(1, ids.count("ac_ucw.%d" % number), number)
        self.assertEqual(0, ids.count("ac_ucw.76"), "San Salvacion is still Erusean-held")

    def test_playtest_shortcuts_are_gated_and_share_the_natural_route(self):
        self.assertFalse(World("1991.1.1").available("ac_playtest_ucw_open_calendar", "ERU"))
        world = World("1991.1.1", rule=True)
        world.countries["ERU"].ai = False
        world.countries["FCU"].ai = False
        world.take("ac_playtest_ucw_open_calendar", "ERU")
        self.assertIn("ac_ucw_calendar_started", world.globals)
        self.assertIn("ac_ucw_started", world.countries["FCU"].flags)
        self.assertEqual("ac_ucw_eru_tree", world.countries["ERU"].tree)
        world.take("ac_playtest_ucw_start_war", "ERU")
        self.assertTrue(world.at_war("ERU", "SNS"))
        world.take("ac_playtest_ucw_seize_stonehenge", "ERU")
        self.assertIn("ac_ucw_stonehenge_railguns", world.countries["ERU"].ideas)
        world.take("ac_playtest_ucw_form_isaf", "ERU")
        self.assertIn("ac_ucw_isaf_formed", world.globals)
        for stage in ("los_canas", "north_point", "counteroffensive", "stonehenge"):
            world.take("ac_playtest_ucw_next_stage", "ERU")
            self.assertIn("ac_ucw_stage_" + stage, world.globals)
        self.assertFalse(world.available("ac_playtest_ucw_next_stage", "ERU"))
        world.take("ac_playtest_ucw_report", "ERU")
        self.assertEqual("ac_ucw.99", world.queue[-1][2])
        world.take("ac_playtest_ucw_stalemate", "ERU")
        self.assertEqual(["ac_ucw_outcome_stalemate"], world.outcome())
        self.assertFalse(world.available("ac_playtest_ucw_isaf_victory", "ERU"))

    def test_shortcut_seizure_survives_weekly_ticks(self):
        world = World("1991.1.1", rule=True)
        for tag in ("ERU", "FCU"):
            world.countries[tag].ai = False
        for ident in ("ac_playtest_ucw_open_calendar", "ac_playtest_ucw_start_war", "ac_playtest_ucw_seize_stonehenge", "ac_playtest_ucw_form_isaf"):
            world.take(ident, "ERU")
        world.weeks(2)
        self.assertNotIn("ac_ucw_stonehenge_destroyed", world.globals, "A simulated seizure is not a ground recapture")
        for stage in ("los_canas", "north_point", "counteroffensive", "stonehenge"):
            world.take("ac_playtest_ucw_next_stage", "ERU")
            self.assertIn("ac_ucw_stage_" + stage, world.globals)
        real = at_war()
        real.controllers[310] = "ERU"
        real.weeks(1)
        real.controllers[310] = "SNS"
        real.weeks(1)
        self.assertIn("ac_ucw_stonehenge_destroyed", real.globals, "A real hold that is lost still destroys the battery")

    def test_accord_focus_closes_once_the_war_starts(self):
        world = started()
        for step in ("after_ulysses", "refugee_quotas", "continental_dialogue", "refugee_accord", "reconstruction_bonds", "arms_talks"):
            world.complete("ERU_ucw_" + step, "ERU")
        world.today = day("2003.7.1")
        world.run("ac_ucw_start_war", "ERU")
        self.assertIn("ac_ucw_war_started", world.globals)
        self.assertFalse(world.focus_available("ERU_ucw_continental_accord", "ERU"))
        world.execute(mapping(world.focuses["ERU_ucw_continental_accord"])["completion_reward"], world.countries["ERU"])
        self.assertNotIn("ac_ucw_continental_peace", world.countries["ERU"].ideas)

    def test_renewed_north_point_invitation_grants_the_rear_base(self):
        world = at_war()
        world.weeks(14)
        world.faction.pop("NPT", None)
        world.countries["NPT"].ideas.clear()
        world.countries["FCU"].ai = False
        world.countries["FCU"].variables["ac_ucw_stage_weeks"] = 30
        world.take("ac_ucw_order_north_point", "FCU")
        self.assertNotIn("ac_ucw_npt_isaf_rear_base", world.countries["NPT"].ideas)
        world.choose("ac_ucw.32", 0, "NPT")
        self.assertEqual("FCU", world.faction.get("NPT"))
        self.assertIn("ac_ucw_npt_isaf_rear_base", world.countries["NPT"].ideas)
    def test_eru_tree_routes(self):
        world = started()
        world.countries["ERU"].ai = False
        for step in ("after_ulysses", "close_the_border", "national_grievance", "army_modernization", "aegir_fleet", "mobilize", "san_salvacion_plan"):
            world.complete("ERU_ucw_" + step, "ERU")
        self.assertFalse(world.focus_available("ERU_ucw_continental_dialogue", "ERU"))
        self.assertFalse(world.focus_available("ERU_ucw_seize_stonehenge", "ERU"))
        world = started()
        eru = world.countries["ERU"]
        for step in ("after_ulysses", "refugee_quotas", "continental_dialogue", "refugee_accord", "reconstruction_bonds", "arms_talks"):
            world.complete("ERU_ucw_" + step, "ERU")
        self.assertLess(eru.variables["ac_ucw_grievance"], 25)
        world.today = day("2002.1.2")
        world.complete("ERU_ucw_continental_accord", "ERU")
        self.assertIn("ac_ucw_war_averted", world.globals)
        self.assertTrue(world.focus_available("ERU_ucw_armistice_line", "ERU"))
        self.assertFalse(world.focus_available("ERU_ucw_victors_order", "ERU"))

    def test_source_contract_localisation_and_banned_effects(self):
        world = World()
        self.assertEqual(72, len(world.focuses))
        loc_path = MOD / "localisation/english/ac_ucw_l_english.yml"
        self.assertTrue(loc_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        keys = re.findall(r'^\s*([A-Za-z0-9_.]+):0\s+"', loc_path.read_text(encoding="utf-8-sig"), re.M)
        self.assertEqual(len(keys), len(set(keys)))
        for ident in list(world.focuses) + list(world.decisions):
            self.assertIn(ident, keys)
            self.assertIn(ident + "_desc", keys)
        for ident, (_, nodes) in world.events.items():
            data = mapping(nodes)
            self.assertIn(data["title"], keys)
            self.assertIn(data["desc"], keys)
            for kind, _, option in nodes:
                if kind == "option":
                    self.assertIn(mapping(option)["name"], keys)
        text = "\n".join(path.read_text(encoding="utf-8-sig") for path in MOD.rglob("ac_ucw*.txt"))
        text += "\n".join((MOD / "common/national_focus" / name).read_text(encoding="utf-8") for name in ("ERU.txt", "FCU.txt"))
        for flag in set(re.findall(r"has_(?:country|global)_flag\s*=\s*(\w+)", text)):
            self.assertIn(flag, keys, "Raw flag ID in an engine-generated tooltip: " + flag)
        for flag in CONTRACT_SET:
            self.assertRegex(text, r"set_global_flag\s*=\s*" + flag + r"\b")
        for flag in CONTRACT_READ:
            self.assertRegex(text, r"has_(?:country|global)_flag\s*=\s*" + flag + r"\b")
        self.assertNotRegex(text, r"set_country_flag\s*=\s*ac_npt_hosts_isaf\b")
        decisions = (MOD / "common/decisions/ac_ucw.txt").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"set_global_flag = ac_sp_stonehenge_complete\b", text)), decisions.count("set_global_flag = ac_sp_stonehenge_complete"), "Only the playtest shortcut may stand in for the special project")
        for forbidden in ("transfer_state", "annex_country", "set_politics", "set_owner", "add_state_core", "every_country", "every_state", "launch_nuke", "set_state_controller"):
            self.assertNotRegex(text, r"\b" + forbidden + r"\s*=")
        state_ids = set(re.findall(r"\b(\d{2,3})\s*=\s*\{\s*is_controlled_by", text))
        self.assertEqual({"310"}, state_ids)
        triggers = (MOD / "common/scripted_triggers/ac_ucw.txt").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"\b310\b", text)), len(re.findall(r"\b310\b", triggers)), "Stonehenge state ID outside the scripted triggers")

    def test_focus_coordinates_prerequisites_and_art(self):
        world = World()
        coords = {}
        for ident, nodes in world.focuses.items():
            data = mapping(nodes)
            coordinate = (ident[:3], int(data["x"]), int(data["y"]))
            self.assertNotIn(coordinate, coords, (ident, coords.get(coordinate)))
            coords[coordinate] = ident
            for key, _, value in nodes:
                if key in ("prerequisite", "mutually_exclusive"):
                    for _, _, other in value:
                        self.assertIn(other, world.focuses, ident)
        sprites = {mapping(v)["name"].strip('"'): mapping(v) for k, _, v in load("interface/ac_expansion_focus.gfx")[0][2] if k == "spriteType"}
        shine = (MOD / "interface/ac_expansion_focus.gfx").read_text(encoding="utf-8-sig")
        for ident, nodes in world.focuses.items():
            icon = mapping(nodes)["icon"]
            self.assertIn(icon, sprites, ident)
            self.assertTrue((MOD / sprites[icon]["texturefile"].strip('"')).is_file(), ident)
            self.assertIn(icon + "_shine", shine, ident)
        gfx = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in (MOD / "interface").glob("*.gfx"))
        for ident, (_, nodes) in world.events.items():
            self.assertIn('"%s"' % mapping(nodes)["picture"], gfx, ident)
        for _, _, body in load("common/ideas/ac_ucw.txt")[0][2][0][2]:
            self.assertIn('"GFX_idea_%s"' % mapping(body)["picture"], gfx)

    def test_generated_files_match_authoring_source(self):
        subprocess.run([sys.executable, str(ROOT / "tools/build_continental_war.py"), "--check"], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=MOD)
    args, remaining = parser.parse_known_args()
    MOD = args.mod_root.resolve()
    unittest.main(argv=[sys.argv[0]] + remaining)
