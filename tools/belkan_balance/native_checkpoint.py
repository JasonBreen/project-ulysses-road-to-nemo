"""Create a sanitized Belkan War checkpoint from an uncompressed HOI4 save.

The raw save stays outside the repository. It contains player/profile data and
the state of every country. This extractor retains only bounded campaign,
economy, force-readiness, and state-control observations for the seven actors in
the Belkan balance matrix. Observations do not establish that a route was
reached naturally; callers must label provenance explicitly.

The isolated native root must contain ``native-provenance.json`` and the payload
manifest named by that file. The sidecar binds a checkpoint to an exact source
commit, payload manifest, and copied engine without adding local paths to the
retained JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
TAGS = ("BLK", "OSE", "UST", "SAP", "GEB", "FAT", "REC")
PROVENANCE_VALUES = ("natural", "disabled-control", "forced")
RUN_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z")
HEX_40_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
HEX_64_RE = re.compile(r"[0-9a-fA-F]{64}\Z")

CAMPAIGN_FLAG_PREFIXES = (
    "ac_campaign_",
    "ac_postwar_",
    "ac_continuation_",
    "ac_macro_",
    "ac_econ_",
    "belka_",
    "belkan_",
)
GLOBAL_FLAG_PREFIXES = (
    "ac_campaign_",
    "ac_postwar_",
    "ac_continuation_",
    "belka_",
    "belkan_",
)
VARIABLE_PREFIXES = ("ac_campaign_", "ac_macro_", "ac_econ_", "BLK_")

MACRO_FIELDS = {
    "mode": "ac_macro_mode",
    "cash": "ac_macro_cash",
    "debt": "ac_macro_debt",
    "debt_ratio": "ac_macro_debt_ratio",
    "arrears": "ac_macro_arrears",
    "funding": "ac_macro_funding",
    "readiness": "ac_macro_readiness",
    "readiness_modifier": "ac_macro_readiness_modifier",
    "nominal_gdp": "ac_macro_nominal_gdp",
    "real_gdp": "ac_macro_real_gdp",
    "potential_gdp": "ac_macro_potential_gdp",
    "growth": "ac_macro_growth",
    "inflation": "ac_macro_inflation",
    "crisis": "ac_macro_crisis",
    "warning": "ac_macro_warning",
    "stress_months": "ac_macro_stress_months",
    "recovery_months": "ac_macro_recovery_months",
    "upkeep": "ac_macro_upkeep",
    "supply_pressure": "ac_macro_supply_pressure",
    "budget_defense": "ac_macro_budget_defense",
    "budget_services": "ac_macro_budget_services",
    "budget_education": "ac_macro_budget_education",
    "budget_development": "ac_macro_budget_development",
    "budget_administration": "ac_macro_budget_administration",
}
LEGACY_ECONOMY_FIELDS = {
    "treasury": "ac_econ_treasury",
    "debt": "ac_econ_debt",
    "arrears": "ac_econ_arrears",
    "balance": "ac_econ_balance",
    "revenue": "ac_econ_revenue",
    "spending": "ac_econ_spending",
    "military_spending": "ac_econ_military_spending",
    "civilian_spending": "ac_econ_civilian_spending",
    "tax_rate": "ac_econ_tax_rate",
    "capacity": "ac_econ_capacity",
}

CONTROL_GROUPS = {
    "BLK_belkan_war_controls_heart_lands": {
        "states": (228, 584, 8, 302, 364, 369, 330, 331, 270, 590, 272, 600, 259, 242, 602, 265, 596, 235, 224),
        "requirements": (),
    },
    "BLK_belkan_war_controls_ustio": {
        "states": (309, 339, 335, 378, 358, 340),
        "requirements": ("UST_capitulated",),
    },
    "BLK_belkan_war_controls_north": {
        "states": (316, 293, 256, 220),
        "requirements": ("FAT_subject_of_BLK", "GEB_subject_of_BLK", "REC_subject_of_BLK"),
    },
    "BLK_belkan_war_controls_south": {
        "states": (604, 211, 357, 324, 269, 296),
        "requirements": (),
    },
    "BLK_wacht_am_wall_state_control": {
        "states": (228, 584, 8, 302, 364, 369, 330, 331, 270, 590, 272, 600, 259, 242, 602, 265, 596, 235, 224, 316, 293, 256, 220),
        "requirements": (),
    },
}


class CheckpointError(ValueError):
    """Raised when required save or provenance evidence is unavailable."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _quoted_or_token(pattern_name: str) -> str:
    return re.escape(pattern_name) + r'=("(?:\\.|[^"\\])*"|[^\s{}]+)'


def scalar_at(text: str, name: str, indent: int) -> str | None:
    prefix = "\t" * indent
    match = re.search(r"^" + re.escape(prefix) + _quoted_or_token(name), text, re.M)
    if match is None:
        return None
    value = match.group(1)
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def _block_end(text: str, content_start: int, name: str) -> int:
    depth = 1
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]', text[content_start:]):
        if token.group(0) == "{":
            depth += 1
        elif token.group(0) == "}":
            depth -= 1
            if depth == 0:
                return content_start + token.start()
    raise CheckpointError(f"Unclosed native block: {name}")


def block_at(text: str, name: str, indent: int) -> str | None:
    prefix = "\t" * indent
    match = re.search(r"^" + re.escape(prefix + name) + r"=\{", text, re.M)
    if match is None:
        return None
    end = _block_end(text, match.end(), name)
    return text[match.end():end]


def named_blocks(text: str, indent: int, names: Iterable[str] | None = None) -> dict[str, str]:
    prefix = "\t" * indent
    wanted = set(names) if names is not None else None
    result: dict[str, str] = {}
    pattern = re.compile(r"^" + re.escape(prefix) + r"([A-Za-z0-9_.@:-]+)=\{", re.M)
    for match in pattern.finditer(text):
        name = match.group(1)
        if wanted is not None and name not in wanted:
            continue
        end = _block_end(text, match.end(), name)
        result[name] = text[match.end():end]
    return result


def parsed_value(value: str | None) -> Any:
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "yes":
        return True
    if lowered == "no":
        return False
    if lowered in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
        return value
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\.\d+)(?:[eE][-+]?\d+)?", value):
        number = float(value)
        return number if math.isfinite(number) else value
    return value


def variables_at(text: str, indent: int) -> dict[str, Any]:
    prefix = "\t" * indent
    pattern = re.compile(
        r"^" + re.escape(prefix) + r"([A-Za-z0-9_.@:-]+)=(\"(?:\\.|[^\"\\])*\"|[^\s{}]+)",
        re.M,
    )
    return {name: parsed_value(value.strip('"')) for name, value in pattern.findall(text)}


def flags_at(text: str, indent: int) -> set[str]:
    return set(named_blocks(text, indent))


def warning(code: str, scope: str, field: str, message: str) -> dict[str, str]:
    return {"code": code, "scope": scope, "field": field, "message": message}


def relevant_focus(focus_id: str, tag: str) -> bool:
    return focus_id.startswith((tag + "_", "BLK_", "ac_belkan_", "ac_postwar_", "ac_pwi_"))


def relevant_flag(flag: str, tag: str) -> bool:
    return flag.startswith(CAMPAIGN_FLAG_PREFIXES + (tag + "_", "BLK_"))


def provenance_sidecar(save: Path) -> tuple[Path, dict[str, Any]]:
    candidates = []
    current = save.parent.resolve()
    for _ in range(6):
        candidates.append(current / "native-provenance.json")
        if current.parent == current:
            break
        current = current.parent
    sidecar = next((candidate for candidate in candidates if candidate.is_file()), None)
    if sidecar is None:
        raise CheckpointError("Missing native-provenance.json in the save directory or isolated native-root ancestors.")
    try:
        data = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CheckpointError(f"Invalid native provenance sidecar: {error}") from error
    if data.get("schema_version") != 1:
        raise CheckpointError("native-provenance.json must use schema_version 1.")
    source_commit = str(data.get("source_commit", ""))
    if not HEX_40_RE.fullmatch(source_commit):
        raise CheckpointError("native-provenance.json requires a full 40-character source_commit.")
    payload = data.get("payload_manifest")
    if not isinstance(payload, dict):
        raise CheckpointError("native-provenance.json requires a payload_manifest object.")
    manifest_name = payload.get("file")
    expected_hash = str(payload.get("sha256", ""))
    if not isinstance(manifest_name, str) or not manifest_name or Path(manifest_name).is_absolute():
        raise CheckpointError("payload_manifest.file must be a non-empty relative path.")
    if not HEX_64_RE.fullmatch(expected_hash):
        raise CheckpointError("payload_manifest.sha256 must be a 64-character SHA-256 value.")
    manifest = (sidecar.parent / manifest_name).resolve()
    try:
        manifest.relative_to(sidecar.parent.resolve())
    except ValueError as error:
        raise CheckpointError("payload_manifest.file must stay inside the isolated native root.") from error
    if not manifest.is_file():
        raise CheckpointError("The payload manifest named by native-provenance.json is missing.")
    actual_hash = sha256(manifest)
    if actual_hash.lower() != expected_hash.lower():
        raise CheckpointError("The payload manifest hash does not match native-provenance.json.")
    engine = data.get("engine")
    if not isinstance(engine, dict) or not all(str(engine.get(key, "")).strip() for key in ("version", "build_id", "checksum")):
        raise CheckpointError("native-provenance.json requires engine version, build_id, and checksum.")
    return sidecar, data


def _optional_scalar(
    text: str,
    name: str,
    indent: int,
    warnings: list[dict[str, str]],
    scope: str,
    field: str | None = None,
) -> Any:
    value = scalar_at(text, name, indent)
    if value is None:
        warnings.append(warning("missing_optional_field", scope, field or name, f"{name} is absent from this save context."))
        return None
    parsed = parsed_value(value)
    if isinstance(parsed, str) and parsed.lower() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}:
        warnings.append(warning("nonfinite_numeric_field", scope, field or name, f"{name} contains a non-finite value."))
    return parsed


def country_snapshot(tag: str, body: str | None, warnings: list[dict[str, str]]) -> dict[str, Any]:
    scope = f"countries.{tag}"
    if body is None:
        warnings.append(warning("missing_country", scope, "present", f"{tag} is absent from the save's country table."))
        return {
            "present": False,
            "focus_tree": None,
            "selected_focus": None,
            "completed_focuses": [],
            "flags": [],
            "variables": {},
            "stability": None,
            "war_support": None,
            "surrender_progress": None,
            "manpower": None,
            "fuel": {"current": None, "maximum": None, "gain": None, "cost": None},
            "political_power": None,
            "command_power": None,
            "economy": None,
        }

    country_flags_body = block_at(body, "flags", 2)
    country_variables_body = block_at(body, "variables", 2)
    country_flags = flags_at(country_flags_body or "", 3)
    country_variables = variables_at(country_variables_body or "", 3)
    selected_variables = {
        key: value for key, value in country_variables.items() if key.startswith(VARIABLE_PREFIXES)
    }
    completed = sorted(
        {
            focus_id
            for focus_id in re.findall(r'^\t\tcompleted="([^"]+)"', body, re.M)
            if relevant_focus(focus_id, tag)
        }
    )
    focus = block_at(body, "focus", 2)
    manpower = block_at(body, "manpower", 2)
    fuel = block_at(body, "fuel_status", 2)
    politics = block_at(body, "politics", 2)
    economy = {
        "macro": {name: country_variables.get(variable) for name, variable in MACRO_FIELDS.items()},
        "legacy": {name: country_variables.get(variable) for name, variable in LEGACY_ECONOMY_FIELDS.items()},
    }
    macro_ready = "ac_macro_ready" in country_flags or "ac_macro_initialized" in country_flags
    if macro_ready:
        for required in ("cash", "debt", "arrears", "funding", "readiness", "nominal_gdp", "growth", "inflation", "crisis"):
            if economy["macro"][required] is None:
                warnings.append(warning("missing_economy_field", scope, required, f"Economy v2 is marked ready but {required} is absent."))

    return {
        "present": True,
        "focus_tree": scalar_at(body, "focus_tree", 2),
        "selected_focus": scalar_at(focus or "", "id", 3),
        "completed_focuses": completed,
        "flags": sorted(flag for flag in country_flags if relevant_flag(flag, tag)),
        "variables": selected_variables,
        "stability": _optional_scalar(body, "stability", 2, warnings, scope),
        "war_support": _optional_scalar(body, "war_support", 2, warnings, scope),
        "surrender_progress": _optional_scalar(body, "surrender_progress", 2, warnings, scope),
        "manpower": _optional_scalar(manpower or "", "ratio", 3, warnings, scope, "manpower"),
        "fuel": {
            "current": _optional_scalar(fuel or "", "fuel", 3, warnings, scope, "fuel.current"),
            "maximum": _optional_scalar(fuel or "", "max_fuel", 3, warnings, scope, "fuel.maximum"),
            "gain": _optional_scalar(fuel or "", "fuel_gain", 3, warnings, scope, "fuel.gain"),
            "cost": _optional_scalar(fuel or "", "fuel_cost", 3, warnings, scope, "fuel.cost"),
        },
        "political_power": _optional_scalar(politics or "", "political_power", 3, warnings, scope),
        "command_power": _optional_scalar(body, "command_power", 2, warnings, scope),
        "economy": economy,
    }


def state_controllers(states: str) -> dict[int, str | None]:
    result: dict[int, str | None] = {}
    wanted = {str(state) for row in CONTROL_GROUPS.values() for state in row["states"]}
    for state_id, body in named_blocks(states, 1, wanted).items():
        controller = scalar_at(body, "controller", 2) or scalar_at(body, "owner", 2)
        result[int(state_id)] = controller
    return result


def control_groups(states: str, countries: dict[str, str], warnings: list[dict[str, str]]) -> dict[str, Any]:
    controllers = state_controllers(states)
    requirements: dict[str, bool | None] = {
        "UST_capitulated": parsed_value(scalar_at(countries.get("UST", ""), "capitulated", 2)),
        "FAT_subject_of_BLK": scalar_at(countries.get("FAT", ""), "overlord", 2) == "BLK" if scalar_at(countries.get("FAT", ""), "overlord", 2) is not None else None,
        "GEB_subject_of_BLK": scalar_at(countries.get("GEB", ""), "overlord", 2) == "BLK" if scalar_at(countries.get("GEB", ""), "overlord", 2) is not None else None,
        "REC_subject_of_BLK": scalar_at(countries.get("REC", ""), "overlord", 2) == "BLK" if scalar_at(countries.get("REC", ""), "overlord", 2) is not None else None,
    }
    result: dict[str, Any] = {}
    for trigger, contract in CONTROL_GROUPS.items():
        required_states = list(contract["states"])
        controlled = [state for state in required_states if controllers.get(state) == "BLK"]
        missing = [state for state in required_states if controllers.get(state) != "BLK"]
        additional = {name: requirements[name] for name in contract["requirements"]}
        unknown_requirements = [name for name, value in additional.items() if value is None]
        if unknown_requirements:
            warnings.append(
                warning(
                    "unevaluated_trigger_requirement",
                    f"control_groups.{trigger}",
                    "additional_requirements",
                    "Save serialization did not expose: " + ", ".join(unknown_requirements),
                )
            )
        passed = not missing and all(value is True for value in additional.values()) if not unknown_requirements else None
        result[trigger] = {
            "required_states": required_states,
            "controlled_by_BLK": controlled,
            "missing_or_other_controller": missing,
            "state_control_passed": not missing,
            "additional_requirements": additional,
            "passed": passed,
        }
    return result


def lifecycle(global_flags: set[str], blk: dict[str, Any]) -> dict[str, Any]:
    country_flags = set(blk.get("flags") or [])
    outcome_flags = {
        "belkan_victory": "belka_won_belkan_war",
        "wacht_am_wal": "belka_won_belkan_war_wacht_am_wal",
        "defeat": "belka_lost_belkan_war",
        "unclassified": "ac_postwar_unclassified",
    }
    outcomes = [name for name, flag in outcome_flags.items() if flag in global_flags]
    return {
        "committed": "ac_campaign_war_committed" in country_flags,
        "arc_started": "ac_campaign_arc_started" in global_flags,
        "war_active": "belkan_war_is_happening" in global_flags,
        "war_weeks": (blk.get("variables") or {}).get("ac_campaign_war_weeks"),
        "stages": {
            "one": "ac_campaign_stage_one" in country_flags,
            "two": "ac_campaign_stage_two" in country_flags,
            "three": "ac_campaign_stage_three" in country_flags,
        },
        "outcomes": outcomes,
        "postwar_ready": "ac_postwar_ready" in country_flags,
        "postwar_flags": sorted(flag for flag in global_flags if flag.startswith("ac_postwar_")),
    }


def capture(save: Path, run_id: str, provenance: str) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        raise CheckpointError("run-id must be 1-80 characters using letters, digits, dot, underscore, or hyphen.")
    if provenance not in PROVENANCE_VALUES:
        raise CheckpointError("provenance must be natural, disabled-control, or forced.")
    if not save.is_file():
        raise CheckpointError(f"Save does not exist: {save}")

    _sidecar, native = provenance_sidecar(save)
    raw = save.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise CheckpointError("The save is not valid UTF-8 text; use save_as_binary=no.") from error
    if not (text.startswith("HOI4txt\n") or text.startswith("HOI4txt\r\n")):
        raise CheckpointError("Use an uncompressed native text save beginning with HOI4txt.")

    date = scalar_at(text, "date", 0)
    save_version = scalar_at(text, "version", 0)
    save_checksum = scalar_at(text, "checksum", 0)
    player = scalar_at(text, "player", 0)
    countries_body = block_at(text, "countries", 0)
    states_body = block_at(text, "states", 0)
    global_flags_body = block_at(text, "flags", 0)
    global_variables_body = block_at(text, "variables", 0)
    missing_required = [
        name
        for name, value in (
            ("date", date),
            ("version", save_version),
            ("checksum", save_checksum),
            ("player", player),
            ("countries", countries_body),
            ("states", states_body),
            ("flags", global_flags_body),
        )
        if value is None
    ]
    if missing_required:
        raise CheckpointError("Save is missing required checkpoint fields: " + ", ".join(missing_required))
    if not re.fullmatch(r"\d{1,4}\.\d{1,2}\.\d{1,2}\.\d{1,2}", date or ""):
        raise CheckpointError("Save date does not use the expected HOI4 timestamp form.")

    country_blocks = named_blocks(countries_body or "", 1, TAGS)
    if "BLK" not in country_blocks:
        raise CheckpointError("Belka is missing from the save's country table; campaign lifecycle cannot be established.")
    warnings: list[dict[str, str]] = []
    countries = {tag: country_snapshot(tag, country_blocks.get(tag), warnings) for tag in TAGS}
    global_flags = flags_at(global_flags_body or "", 1)
    selected_global_flags = {flag for flag in global_flags if flag.startswith(GLOBAL_FLAG_PREFIXES)}
    global_variables = variables_at(global_variables_body or "", 1)
    selected_global_variables = {
        key: value for key, value in global_variables.items() if key.startswith(("ac_campaign_", "ac_postwar_", "BLK_"))
    }
    if global_variables_body is None:
        warnings.append(warning("missing_optional_block", "global", "variables", "The save has no top-level variables block."))
    if player not in TAGS and player not in {"---", "observer", "spectator"}:
        warnings.append(warning("out_of_scope_player_tag", "run", "player_tag", "The active player tag is outside the Belkan checkpoint matrix."))

    engine = native["engine"]
    if str(engine["version"]) not in (save_version or "") and (save_version or "") not in str(engine["version"]):
        warnings.append(warning("engine_version_mismatch", "provenance", "engine.version", "The sidecar engine version and save version are not identical."))

    result = {
        "schema_version": SCHEMA_VERSION,
        "evidence_class": "native_observation",
        "run": {
            "id": run_id,
            "provenance": provenance,
            "date": date,
            "player_tag": player,
            "observer": player in {"---", "observer", "spectator"},
        },
        "source": {
            "commit": native["source_commit"].lower(),
            "payload_manifest_sha256": native["payload_manifest"]["sha256"].lower(),
        },
        "engine": {
            "version": str(engine["version"]),
            "build_id": str(engine["build_id"]),
            "checksum": str(engine["checksum"]),
            "save_version": save_version,
            "save_checksum": save_checksum,
        },
        "save": {
            "filename": save.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "lifecycle": None,
        "global_flags": sorted(selected_global_flags),
        "global_variables": selected_global_variables,
        "countries": countries,
        "control_groups": control_groups(states_body or "", country_blocks, warnings),
        "warnings": warnings,
    }
    result["lifecycle"] = lifecycle(selected_global_flags, countries["BLK"])
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--provenance", choices=PROVENANCE_VALUES, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.save.resolve() == args.output.resolve():
            raise CheckpointError("Output must not overwrite the raw save.")
        result = capture(args.save, args.run_id, args.provenance)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (CheckpointError, OSError) as error:
        print(f"native checkpoint error: {error}", file=sys.stderr)
        return 2
    print(f"Recorded sanitized Belkan checkpoint: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
