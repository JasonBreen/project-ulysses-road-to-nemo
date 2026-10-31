"""Read-only consistency gate for the approved roadmap; not gameplay validation."""

import argparse
import json
from pathlib import Path


DEFAULT_PLAN = Path(__file__).with_name("release_plan.json")


def check(plan):
    problems = []

    def require(condition, message):
        if not condition:
            problems.append(message)

    require(plan["schema_version"] == 1, "Unknown release-plan schema")
    countries = plan["countries"]
    require(len(countries) == 19, "Expected 19 individually budgeted countries")
    require(len({row["tag"] for row in countries}) == len(countries), "Duplicate country budget")
    packages = {row["id"] for row in plan["packages"]}
    require(packages == set(range(6)), "Expected Packages 0 through 5")
    for row in countries:
        require(row["target_definitions"] - row["baseline_definitions"] == row["new_definitions"],
                f"{row['tag']}: baseline/target/addition mismatch")
        require(row["new_definitions"] >= 0, f"{row['tag']}: negative addition budget")
        require(set(row["delivery_packages"]) <= packages, f"{row['tag']}: unknown package")
    counts = plan["count_contract"]
    for field, key in [("new_definitions", "country_additions"),
                       ("baseline_definitions", "country_baseline_definitions"),
                       ("target_definitions", "country_target_definitions")]:
        require(sum(row[field] for row in countries) == counts[key], f"Country {key} sum mismatch")
    require(counts["country_additions"] == 1028, "Approved country addition budget is 1,028")
    delivered = sum(row.get("delivered_since_approval", 0) for row in countries)
    remaining = sum(row.get("remaining_definitions", row["new_definitions"]) for row in countries)
    require(delivered == counts.get("delivered_since_approval", 0), "Delivered focus accounting mismatch")
    require(remaining == counts.get("remaining_country_additions", 1028), "Remaining focus accounting mismatch")
    require(delivered + remaining == 1028, "Delivered and remaining focuses must reconcile to approval budget")
    for row in countries:
        require(row.get("remaining_definitions", row["new_definitions"]) + row.get("delivered_since_approval", 0)
                == row["new_definitions"], f"{row['tag']}: delivered/remaining mismatch")
    require(counts["regional_shared_definitions"] == plan["regional_framework"]["shared_focus_definitions"] == 36,
            "Regional framework budget must remain 36")
    require(not counts["regional_counted_in_country_additions"], "Regional framework double-counted")
    usean = [row for row in countries if row["tag"] in {"SNS", "AMB", "UGE", "DEL"}]
    require(len(usean) == 4 and sum(row["new_definitions"] for row in usean) == 228,
            "First Usean wave must contain four countries and 228 additions")
    stories = plan["stories"]
    require({row["host_tag"] for row in stories} == {"BLK", "UST", "ERU", "SNS", "EMM", "EVA"}
            and len(stories) == 6, "Initial story portfolio must contain the six approved hosts")
    require(len({row["theater"] for row in stories}) >= 3, "Global story portfolio needs three theaters")
    for row in stories:
        require(row["core_chapters"] == 20 and row["choice_chapters_minimum"] >= 12
                and row["endings_minimum"] >= 3 and row["core_original_cast"] == 4,
                f"{row['host_tag']}: story budget differs from approved minimums")
    require(sum(row["core_chapters"] for row in stories) == 120, "Initial story core chapter sum must be 120")
    art = plan["story_art"]
    require(sum(row["core_original_cast"] for row in stories) == art["core_portraits"] == 24,
            "Initial core cast/portrait count must be 24")
    require(art["illustrations"] == 48 and art["loading_screens"] == 6, "Initial story art budget mismatch")
    later = plan["later_story_hosts"]
    require(len(later) == 4 and {row["host_tag"] for row in later} == {"OSE", "YUK", "AUR", "LEA"}
            and all(row["core_chapters"] == 20 for row in later), "Later story portfolio mismatch")
    economy = plan["economy"]
    require(len(economy["tax_bases"]) == 3 and len(economy["spending_envelopes"]) == 5
            and len(economy["pages"]) == 5, "Economic tax/envelope/page contract mismatch")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
        problems = check(plan)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"Invalid release plan: {exc}") from exc
    if problems:
        raise SystemExit("Release-plan problems:\n- " + "\n- ".join(problems))
    print("PASS: 19 country budgets, 1,028 country additions + 36 regional focuses; "
          "six initial stories / 120 chapters / 24 core portraits. Roadmap only; gameplay acceptance is separate.")


if __name__ == "__main__":
    main()
