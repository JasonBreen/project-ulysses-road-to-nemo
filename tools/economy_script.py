"""Strict offline harness for the authored economy subset, not a HOI4 engine.

Reads the shipped scripts, preserves repeated keys, and rejects unknown commands.
Decimal arithmetic verifies accounting; HOI4 precision/scheduling needs runtime QA.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
import re


TOKEN = re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|>=|<=|!=|[={}<>]|[\w.:@/-]+')
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"


def parse(text):
    tokens = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            raise ValueError("Unrecognized script character at " + repr(text[position:position + 30]))
        token = match.group()
        if not token.isspace() and not token.startswith("#"):
            tokens.append(token.strip('"'))
        position = match.end()
    position = 0

    def block(nested=False):
        nonlocal position
        result = []
        while position < len(tokens):
            key = tokens[position]
            position += 1
            if key == "}":
                if not nested:
                    raise ValueError("Unexpected closing brace")
                return result
            if key in ("{", "=", "<", ">", ">=", "<=", "!="):
                raise ValueError("Expected key, got " + key)
            if position == len(tokens) or tokens[position] not in ("=", "<", ">", ">=", "<=", "!="):
                result.append((key, None, None))
                continue
            operator = tokens[position]
            position += 1
            if position == len(tokens):
                raise ValueError("Missing value for " + key)
            value = tokens[position]
            position += 1
            if value == "{":
                value = block(True)
            elif value == "}":
                raise ValueError("Missing value for " + key)
            result.append((key, operator, value))
        if nested:
            raise ValueError("Unclosed brace")
        return result

    return block()


def fields(block):
    result = {}
    for key, operator, value in block:
        if key in result:
            raise ValueError("Duplicate field: " + key)
        if operator != "=":
            raise ValueError("Expected assignment: " + key)
        result[key] = value
    return result


def read(path):
    return parse(path.read_text(encoding="utf-8-sig"))


def definitions(folder):
    result = {}
    for path in sorted((MOD / folder).glob("ac_economy*.txt")):
        for key, operator, value in read(path):
            if key in result or operator != "=" or not isinstance(value, list):
                raise ValueError("Invalid or duplicate definition: " + key)
            result[key] = value
    return result


@dataclass
class Country:
    variables: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)
    modifiers: set = field(default_factory=set)
    equipment: dict = field(default_factory=dict)
    factories: int = 0
    military_factories: int = 1
    owns_state: bool = True
    war: bool = False
    ai: bool = False
    capitulated: bool = False
    tech: bool = True
    day: int = 0

    def value(self, key):
        return self.variables.get(key, Decimal(0))


class Harness:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.effects = definitions("common/scripted_effects")
        self.triggers = definitions("common/scripted_triggers")
        self.actions = read(MOD / "common/on_actions/ac_economy_on_actions.txt")[0][2]
        self.decisions = definitions("common/decisions")["ac_economy_budget"]

    def number(self, value, country, temporary):
        try:
            return Decimal(value)
        except Exception:
            if value == "num_of_controlled_factories":
                return Decimal(country.factories)
            if value.startswith("ac_econ_"):
                return temporary.get(value, country.value(value))
            raise ValueError("Unknown numeric input: " + value)

    def trigger(self, block, country, temporary):
        answers = []
        for key, operator, value in block:
            if operator != "=" and key != "num_of_military_factories":
                raise ValueError("Unexpected trigger comparison: " + key)
            if key in self.triggers:
                answers.append(self.trigger(self.triggers[key], country, temporary) == (value == "yes"))
            elif key == "NOT":
                answers.append(not self.trigger(value, country, temporary))
            elif key == "OR":
                answers.append(any(self.trigger([child], country, temporary) for child in value))
            elif key == "always":
                answers.append(value == "yes")
            elif key == "has_game_rule":
                assert fields(value) == {"rule": "ac_economy", "option": "experimental"}
                answers.append(self.enabled)
            elif key == "any_owned_state":
                answers.append(country.owns_state and self.trigger(value, country, temporary))
            elif key == "has_country_flag":
                answers.append(value in country.flags and (country.flags[value] is None or country.flags[value] > country.day))
            elif key == "has_dynamic_modifier":
                answers.append(fields(value)["modifier"] in country.modifiers)
            elif key == "check_variable":
                if len(value) == 1 and value[0][0] not in {"var", "value", "compare"}:
                    variable, comparison, operand = value[0]
                else:
                    comparison_fields = fields(value)
                    if set(comparison_fields) != {"var", "value", "compare"}:
                        raise ValueError("Expected shorthand comparison or var/value/compare form")
                    variable = comparison_fields["var"]
                    operand = comparison_fields["value"]
                    comparison = {
                        "equals": "=",
                        "greater_than": ">",
                        "less_than": "<",
                        "greater_than_or_equals": ">=",
                        "less_than_or_equals": "<=",
                    }.get(comparison_fields["compare"])
                    if comparison is None:
                        raise ValueError("Unsupported variable comparison: " + comparison_fields["compare"])
                left = self.number(variable, country, temporary)
                right = self.number(operand, country, temporary)
                answers.append({"=": left == right, ">": left > right, "<": left < right,
                                ">=": left >= right, "<=": left <= right, "!=": left != right}[comparison])
            elif key in ("has_war", "is_ai", "has_capitulated"):
                attribute = {"has_war": "war", "is_ai": "ai", "has_capitulated": "capitulated"}[key]
                answers.append(getattr(country, attribute) == (value == "yes"))
            elif key == "has_tech":
                assert value == "infantry_weapons"
                answers.append(country.tech)
            elif key == "num_of_military_factories":
                assert operator == ">" and value == "0"
                answers.append(country.military_factories > 0)
            else:
                raise ValueError("Unsupported trigger: " + key)
        return all(answers)

    def execute(self, block, country, temporary=None, countries=None):
        if temporary is None:
            temporary = {}
        branch = None
        for key, operator, value in block:
            if operator != "=":
                raise ValueError("Unexpected effect operator: " + key)
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise ValueError("Orphaned " + key)
                condition = key == "else" or self.trigger(next(v for k, _, v in value if k == "limit"), country, temporary)
                if not branch and condition:
                    self.execute([entry for entry in value if entry[0] != "limit"], country, temporary, countries)
                    branch = True
                continue
            branch = None
            if key in self.effects:
                assert value == "yes"
                self.execute(self.effects[key], country, temporary, countries)
            elif key in ("set_variable", "add_to_variable", "subtract_from_variable", "multiply_variable",
                         "set_temp_variable", "add_to_temp_variable", "multiply_temp_variable"):
                if len(value) != 1 or value[0][1] != "=":
                    raise ValueError("Expected shorthand arithmetic")
                variable, _, operand = value[0]
                if not variable.startswith("ac_econ_"):
                    raise ValueError("Variable outside economy namespace")
                destination = temporary if "temp_variable" in key else country.variables
                amount = self.number(operand, country, temporary)
                previous = destination.get(variable, Decimal(0))
                destination[variable] = amount if key.startswith("set_") else (
                    previous + amount if key.startswith("add_") else previous - amount if key.startswith("subtract_") else previous * amount)
            elif key == "set_country_flag":
                if isinstance(value, list):
                    options = fields(value)
                    country.flags[options["flag"]] = country.day + int(options["days"])
                else:
                    country.flags[value] = None
            elif key == "add_dynamic_modifier":
                country.modifiers.add(fields(value)["modifier"])
            elif key == "add_equipment_to_stockpile":
                options = fields(value)
                assert options == {"type": "infantry_equipment_0", "amount": "100", "producer": "ROOT"}
                country.equipment[options["type"]] = country.equipment.get(options["type"], 0) + int(options["amount"])
            elif key == "every_country":
                for target in countries or []:
                    limit = next(v for k, _, v in value if k == "limit")
                    if self.trigger(limit, target, {}):
                        self.execute([entry for entry in value if entry[0] != "limit"], target, {}, countries)
            else:
                raise ValueError("Unsupported effect: " + key)

    def call(self, name, country):
        self.execute(self.effects[name], country)

    def action(self, name, countries):
        action = fields(fields(self.actions)[name])["effect"]
        if name == "on_startup":
            self.execute(action, None, countries=countries)
        else:
            for country in countries:
                country.day += 7
                self.execute(action, country)

    def click(self, name, country):
        decision = fields(fields(self.decisions)[name])
        if self.trigger(decision["available"], country, {}):
            self.execute(decision["complete_effect"], country)
            return True
        return False


def validate_content(harness):
    """Check all branches, integration references, localization and workspace shape."""
    effect_native = {"if", "else_if", "else", "set_variable", "add_to_variable", "subtract_from_variable",
                     "multiply_variable", "set_temp_variable", "add_to_temp_variable", "multiply_temp_variable",
                     "set_country_flag", "add_dynamic_modifier", "add_equipment_to_stockpile", "every_country"}
    trigger_native = {"NOT", "OR", "always", "has_game_rule", "any_owned_state", "has_country_flag",
                      "has_dynamic_modifier", "check_variable", "has_war", "is_ai", "has_capitulated", "has_tech",
                      "num_of_military_factories"}

    assigned = set()
    used = set()
    modifiers = definitions("common/dynamic_modifiers")

    def check(block, is_trigger=False):
        for key, operator, value in block:
            library = harness.triggers if is_trigger else harness.effects
            native = trigger_native if is_trigger else effect_native
            if key not in library and key not in native:
                raise ValueError("Unresolved script symbol: " + key)
            if key in library:
                if value != "yes" or operator != "=":
                    raise ValueError("Invalid scripted call: " + key)
            elif key in ("if", "else_if", "else", "every_country"):
                for child in value:
                    check(child[2] if child[0] == "limit" else [child], child[0] == "limit")
            elif key in ("NOT", "OR", "any_owned_state"):
                check(value, True)
            elif key == "check_variable":
                if len(value) == 1 and value[0][0] not in {"var", "value", "compare"}:
                    variable, _, operand = value[0]
                else:
                    comparison_fields = fields(value)
                    if set(comparison_fields) != {"var", "value", "compare"}:
                        raise ValueError("Invalid variable comparison")
                    variable = comparison_fields["var"]
                    operand = comparison_fields["value"]
                if not variable.startswith("ac_econ_"):
                    raise ValueError("Invalid economy variable")
                used.add(variable)
                if operand.startswith("ac_econ_"):
                    used.add(operand)
                if not (re.fullmatch(r"-?\d+(?:\.\d+)?", operand) or operand.startswith("ac_econ_") or operand == "num_of_controlled_factories"):
                    raise ValueError("Unknown numeric symbol: " + operand)
            elif "variable" in key:
                if len(value) != 1 or not value[0][0].startswith("ac_econ_"):
                    raise ValueError("Invalid economy variable")
                operand = value[0][2]
                (used if is_trigger else assigned).add(value[0][0])
                if operand.startswith("ac_econ_"):
                    used.add(operand)
                if not (re.fullmatch(r"-?\d+(?:\.\d+)?", operand) or operand.startswith("ac_econ_") or operand == "num_of_controlled_factories"):
                    raise ValueError("Unknown numeric symbol: " + operand)
            elif key in ("has_dynamic_modifier", "add_dynamic_modifier"):
                if fields(value)["modifier"] not in modifiers:
                    raise ValueError("Undefined economy modifier")

    for block in harness.effects.values():
        check(block)
    for block in harness.triggers.values():
        check(block, True)
    for block in modifiers.values():
        data = fields(block)
        check(data["enable"], True)
        for key, variable in data.items():
            if key != "enable":
                if key not in ("stability_factor", "production_speed_buildings_factor"):
                    raise ValueError("Unsupported economy modifier: " + key)
                used.add(variable)
    for _, _, action in harness.actions:
        check(fields(action)["effect"])
    keys = set()
    path = MOD / "localisation/english/ac_economy_l_english.yml"
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("English localization needs UTF-8 BOM")
    for key in re.findall(r'^\s+(ac_\w+):\d*\s+"', raw.decode("utf-8-sig"), re.M):
        if key in keys:
            raise ValueError("Duplicate localization: " + key)
        keys.add(key)
    needed = {"ac_economy_budget", "ac_economy_budget_desc", "ac_econ_budget_modifier", "ac_economy_rule",
              "ac_economy_rule_group", "ac_economy_disabled", "ac_economy_disabled_desc",
              "ac_economy_experimental", "ac_economy_experimental_desc"}
    for name, _, decision in harness.decisions:
        needed.update((name, name + "_desc"))
        data = fields(decision)
        if data["cost"] != "0" or fields(data["ai_will_do"])["base"] != "0":
            raise ValueError("Decision would charge PP or enable uncalibrated AI policy")
        check(data["available"], True)
        check(data["complete_effect"])
    if needed - keys:
        raise ValueError("Missing English keys: " + str(sorted(needed - keys)))
    used.update(re.findall(r'\[\?(ac_econ_\w+)', raw.decode("utf-8-sig")))
    if used - assigned:
        raise ValueError("Unassigned economy variables: " + str(sorted(used - assigned)))
    rules = fields(definitions("common/game_rules")["ac_economy"])
    if fields(rules["default"])["name"] != "disabled":
        raise ValueError("Economy must be default-off")
    equipment_path = MOD / "common/units/equipment/infantry.txt"
    if equipment_path.exists():
        equipment = fields(read(equipment_path))["equipments"]
        if "infantry_equipment_0" not in fields(equipment):
            raise ValueError("Procurement equipment is not defined")
    # The 1.19 continuation deliberately uses the installed game's current
    # equipment schema. The inherited 1.14 unit file is preserved outside the
    # active payload, so only validate it when a mod explicitly supplies one.
    technology_path = MOD / "common/technologies/infantry.txt"
    if technology_path.exists():
        technologies = fields(read(technology_path))["technologies"]
        technology = fields(fields(technologies)["infantry_weapons"])
        if "infantry_equipment_0" not in {key for key, _, _ in technology["enable_equipments"]}:
            raise ValueError("Procurement technology does not unlock the equipment")


if __name__ == "__main__":
    validate_content(Harness())
    print("Economy script references and English localization passed (offline subset only).")
