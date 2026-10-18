"""Regression checks for native-schema migration semantics reviewed on PR #14."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod" / "2985041246"


def read(relative: str) -> str:
    return (MOD / relative).read_text(encoding="utf-8-sig")


def main() -> int:
    mapper = (ROOT / "tools" / "Port-NativeEquipmentReferences.py").read_text(
        encoding="utf-8"
    )
    assert '"antiair_1": "interwar_antiair"' in mapper
    for technology in (
        "basic_medium_battery",
        "improved_airplane_launcher",
        "air_tank_buster_1",
    ):
        assert f'"{technology}":' not in mapper, technology

    for path in (MOD / "history" / "countries").glob("*.txt"):
        assert "antiair_1" not in path.read_text(encoding="utf-8-sig"), path

    for relative, technology in (
        ("history/countries/BLK - Belka.txt", "basic_medium_battery"),
        ("history/countries/OSE - Osea.txt", "basic_medium_battery"),
        ("history/countries/OSE - Osea.txt", "improved_airplane_launcher"),
        ("history/countries/OSE - Osea.txt", "air_tank_buster_1"),
        ("history/countries/SAP - Sapin.txt", "basic_medium_battery"),
    ):
        assert technology in read(relative), (relative, technology)

    compatibility = read("common/technologies/ac_native_compatibility.txt")
    assert "start_year = 1991" in compatibility
    assert not re.search(r"position\s*=\s*\{[^}]*y\s*=\s*1991", compatibility)

    sapin = read("common/ideas/sapin.txt")
    idea = sapin[sapin.index("sap_concentrated_ifv_production") : sapin.index("# sap_overwhelming_advance_idea")]
    assert idea.count("mechanized_equipment = {") == 1
    assert idea.count("armored_car_equipment = {") == 1

    ustio = read("common/national_focus/UST_shared.txt")
    manpats = ustio[ustio.index("id = UST_import_MANPATS") : ustio.index("id = UST_ask_ratio_for_help")]
    arm_the_man = ustio[ustio.index("id = UST_to_arm_the_man") : ustio.index("id = UST_last_second_mobilization")]
    assert "type = anti_tank_equipment_1" in manpats
    assert "type = anti_tank_equipment_1" in arm_the_man

    continuation = (MOD / "events" / "ac_ustio_continuation.txt").read_text(encoding="utf-8-sig")
    option = continuation[continuation.index("option = {") :]
    assert "has_country_flag = UST_sold_land_to_ratio_flag }\n\t\t\tset_country_flag = ac_ustio_continuation_started" in option
    assert "has_country_flag = UST_not_sold_land_to_ratio_flag }\n\t\t\tset_country_flag = ac_ustio_continuation_started" in option

    decisions = read("common/decisions/SAP_decisions.txt")
    moderate = decisions[decisions.index("SAP_court_moderate_support") : decisions.index("SAP_attempt_to_mediate_differences")]
    assert "value = -0.025\n\t\t\t\t}\n\t\t\t}\n\t\t\telse =" in moderate

    regents = read("common/national_focus/SAP_pre_belkan_war.txt")
    for character, other in (
        ("SAP_domingo_escalona", ("SAP_ramira_arguijo", "SAP_raul_de_haro", "SAP_alphonso_espinal")),
        ("SAP_alphonso_espinal", ("SAP_domingo_escalona", "SAP_ramira_arguijo", "SAP_raul_de_haro")),
    ):
        start = regents.index(f"character = {character}")
        block = regents[start : regents.index("traits =", start)]
        assert "available =" in block
        for rival in other:
            assert rival in block

    localization = (MOD / "localisation" / "english" / "ac_native_compatibility_l_english.yml").read_text(encoding="utf-8-sig")
    for key in ("ifv1", "imv1", "infantry_manpats"):
        assert f"{key}:0" in localization

    ose_names = MOD / "common" / "units" / "names_divisions" / "OSE_names_divisions.txt"
    assert "OSE_MOT_01" in ose_names.read_text(encoding="utf-8-sig")
    assert "OSE_MOT_01" in read("history/units/OSE_land.txt")
    assert "OSE_MOT_01" in read("history/units/OSE_land_ai.txt")

    for name in ("Deutschland Class", "Guinevere Mark I", "Guinevere Mark II"):
        assert name in read("history/countries/BLK - Belka.txt"), name

    print("native semantic mapping regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
