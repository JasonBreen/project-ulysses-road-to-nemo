"""Index of the official ACES Chronicle for Project Ulysses: what each official statement
says (paraphrased), which repository ledger cites it and how the mod treats it.

The committed record is ``tools/lore/chronicle.json``. It never stores the official text:
each row keeps a SHA-256 of the official sentence(s) it paraphrases, so a later read of
the site can be compared with the record without copying the pages into the repository.

Modes:

* ``python -B tools/lore/chronicle_index.py``            rewrite the Markdown index and the
  ``cited_in`` lists from the committed record and ``docs/*.md``;
* ``python -B tools/lore/chronicle_index.py --check``    verify the record is complete and the
  Markdown index is current (CI);
* ``python -B tools/lore/chronicle_index.py --refresh DIR``  parse freshly downloaded copies of
  the official pages in DIR (``home.html``, ``chronicle.html``, ``chronicle_details.html``,
  ``chronicle_weapons.html``, ``product.html``; download them with ``curl`` into an empty
  scratch directory), recompute every hash, report new, changed and removed entries, and
  merge the hashes into the record while keeping every authored field. A manual step; it
  is never run in CI.

Source layers: the four official pages are the only canon tier (docs/CANON_POLICY.md);
the paraphrases and dispositions are authored and reviewed in
docs/research/STRANGEREAL_LORE_1991_2020.md.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import html as html_module
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECORD = HERE / "chronicle.json"
INDEX = ROOT / "docs/research/CHRONICLE_INDEX.md"
PAGES = {
    "abstracts": ("https://acecombat.jp/en/chronicle/", "chronicle.html"),
    "details": ("https://acecombat.jp/en/chronicle/details/", "chronicle_details.html"),
    "weapons": ("https://acecombat.jp/en/chronicle/weapons/", "chronicle_weapons.html"),
    "products": ("https://acecombat.jp/en/product/", "product.html"),
}
TITLE = re.compile(r"^(?:ACE COMBAT|AIR COMBAT)")
YEAR = re.compile(r"^(19|20)\d\d$")
DAY = re.compile(r"^〜?(?:(?:\d\d|XX)\.(?:\d\d|XX)|SPRING|SUMMER|AUTUMN|FALL|WINTER)$", re.I)
RELEASE = re.compile(r"^\d{4}/\d\d/\d\d$")
# Each official statement holds one or more claims (one per distinct statement in the source sentence or
# narrative); every claim carries these authored fields.
AUTHORED = ("paraphrase", "people", "places", "organisations", "weapons_equipment", "units_ships_squadrons",
            "categories", "coverage", "disposition", "pending_wave", "conflicts", "unknowns")
DISPOSITIONS = ("implemented, official-sourced ledger row",
                "implemented by inherited mod content (mod provenance owner); official date is a reference anchor",
                "reference only (named in a ledger, not scripted)",
                "pending (planned wave or track)",
                "not covered anywhere in the repository",
                "out of scope (after 2020 or outside Strangereal)")


def lines(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    text = html_module.unescape(re.sub(r"<[^>]+>", "\n", text))
    text = re.sub(r"[ \t]+", " ", text)
    return [line.strip() for line in text.split("\n") if line.strip()]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract(folder):
    """Return {page: [statements]} from downloaded copies of the official pages."""
    folder = Path(folder)
    found = {}
    # DETAILS: a title line, then years, then "MM.DD" (or XX) with one or more sentences.
    rows, year, title, current = [], None, None, None
    for line in lines(folder / PAGES["details"][1]):
        if TITLE.match(line) and len(line) < 60:
            title = line
        elif YEAR.match(line):
            year = int(line)
        elif DAY.match(line) and year:
            day = line.lstrip("〜").upper()       # the page writes some unknown days as "xx"
            current = dict(key=f"{year} / {day}", year=year, date=day, title=title, text=[])
            rows.append(current)
        elif current is not None and not line.startswith("©"):
            current["text"].append(line)
    seen = {}
    for row in rows:
        row["text"] = " ".join(row["text"])
        # Several statements can share a date (XX months in 2020 and 2040): number the repeats.
        seen[row["key"]] = seen.get(row["key"], 0) + 1
        if seen[row["key"]] > 1:
            row["key"] += f" #{seen[row['key']]}"
    found["details"] = rows
    # SUPER WEAPONS: "<name>", "Game Title", "<title>", description.
    weapon_lines = lines(folder / PAGES["weapons"][1])
    rows = []
    for n, line in enumerate(weapon_lines):
        if line == "Game Title" and n > 0:
            body, m = [], n + 2
            while m < len(weapon_lines) and not (m + 1 < len(weapon_lines) and weapon_lines[m + 1] == "Game Title") \
                    and not weapon_lines[m].startswith("©"):
                body.append(weapon_lines[m])
                m += 1
            rows.append(dict(key=f"Super Weapons, {weapon_lines[n - 1]}", name=weapon_lines[n - 1], title=weapon_lines[n + 1], text=" ".join(body)))
    found["weapons"] = rows
    # ABSTRACTS: one narrative per title.
    abstract_lines = lines(folder / PAGES["abstracts"][1])
    titles = [n for n, line in enumerate(abstract_lines) if TITLE.match(line) and len(line) < 60]
    rows = []
    for k, n in enumerate(titles):
        end = titles[k + 1] if k + 1 < len(titles) else len(abstract_lines)
        body = [line for line in abstract_lines[n + 1:end] if not line.startswith("©")]
        rows.append(dict(key=f"Abstracts, {abstract_lines[n]}", title=abstract_lines[n], text=" ".join(body)))
    found["abstracts"] = rows
    # PRODUCT: the title appears twice, then the release date, then the blurb (repeated once).
    product_lines = lines(folder / PAGES["products"][1])
    rows = []
    for n, line in enumerate(product_lines):
        if RELEASE.match(line) and n >= 2 and product_lines[n - 1] == product_lines[n - 2]:
            body, m = [], n + 1
            while m < len(product_lines) and not YEAR.match(product_lines[m]) and not (
                    m + 2 < len(product_lines) and product_lines[m] == product_lines[m + 1] and RELEASE.match(product_lines[m + 2])):
                body.append(product_lines[m])
                m += 1
            rows.append(dict(key=f"Product, {product_lines[n - 1]}", title=product_lines[n - 1], release=line, text=" ".join(body)))
    found["products"] = rows
    return found


def page_hashes(folder):
    return {page: sha("\n".join(lines(Path(folder) / name))) for page, (_, name) in PAGES.items()}


def load():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def save(record):
    RECORD.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def citations(record):
    """Which docs cite each key: ``YYYY / MM.DD`` (also inside FATO-style day lists), a weapon name
    after "Super Weapons, ", or the page name for abstracts and product blurbs."""
    docs = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8", errors="replace") for p in sorted((ROOT / "docs").rglob("*.md"))}
    docs["README.md"] = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    for row in record["entries"]:
        patterns = []
        if row["page"] == "details":
            year, day = row["key"].split(" #")[0].split(" / ")
            if "." in day:
                month, dd = day.split(".")
                patterns.append(re.compile(rf"{year} ?/ ?(?:[0-9XX.,–\- ]*\b){re.escape(month)}\.{re.escape(dd)}\b"))
            else:
                patterns.append(re.compile(rf"{year} ?/ ?{day}\b", re.I))
        elif row["page"] == "weapons":
            patterns.append(re.compile(r"Super Weapons[, :]+[^|\n]*?" + re.escape(row["key"].split(", ", 1)[1])))
        else:
            patterns.append(re.compile(re.escape(row["key"])))
        row["cited_in"] = sorted(name for name, text in docs.items() if any(p.search(text) for p in patterns)
                                 and not name.startswith("docs/research/"))
    return record


def markdown(record):
    out = ["# Official ACES Chronicle index", "",
           "Generated by `tools/lore/chronicle_index.py` from `tools/lore/chronicle.json`; do not edit by hand.",
           f"Official pages read {record['read_date']}; the record stores paraphrases and hashes, never the official text.",
           "Paraphrases, dispositions and conflicts are reviewed in [STRANGEREAL_LORE_1991_2020.md](STRANGEREAL_LORE_1991_2020.md).",
           "", "| Page | URL | Text SHA-256 |", "| --- | --- | --- |"]
    for page, (url, _) in PAGES.items():
        out.append(f"| {page} | {url} | `{record['pages'][page]['text_sha256']}` |")
    counts = {}
    for row in record["entries"]:
        for claim in row["claims"]:
            counts[claim["disposition"]] = counts.get(claim["disposition"], 0) + 1
    out += ["", f"{len(record['entries'])} official statements, {sum(counts.values())} claims.", "",
            "| Disposition | Claims |", "| --- | ---: |"] + [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    cell = lambda value: value.replace("|", "\\|").replace("\n", " ")
    for page, heading in (("details", "Dated entries"), ("weapons", "Super Weapons"), ("abstracts", "Abstracts"), ("products", "Product blurbs")):
        out += ["", f"## {heading}", "", "| Key | Paraphrase | Disposition | Cited in | Affected IDs |", "| --- | --- | --- | --- | --- |"]
        for row in record["entries"]:
            if row["page"] != page:
                continue
            for n, claim in enumerate(row["claims"], 1):
                key = row["key"] + (f" ({n})" if len(row["claims"]) > 1 else "")
                ids = sorted({i for c in claim["coverage"] for i in c.get("ids", []) if re.fullmatch(r"[\w.]+", i)})
                out.append(f"| {cell(key)} | {cell(claim['paraphrase'])} | {cell(claim['disposition'])}"
                           f"{(' (' + claim['pending_wave'] + ')') if claim.get('pending_wave') else ''} | "
                           f"{', '.join(row['cited_in']) or 'none'} | {', '.join('`' + i + '`' for i in ids[:12]) or 'none'}"
                           f"{' …' if len(ids) > 12 else ''} |")
    return "\n".join(out) + "\n"


ERAS = ((1991, 1994, "1991–1994: before the Belkan War"), (1995, 1995, "1995: the Belkan War"),
        (1996, 1999, "1996–1999: Ulysses"), (2000, 2005, "2000–2005: the Usean Continental War"),
        (2006, 2013, "2006–2013: Free Erusea, Estovakia and the Circum-Pacific War"),
        (2014, 2016, "2014–2016: the Emmeria–Estovakia War"), (2017, 2020, "2019–2020: the Lighthouse War and Aurelia"))
ENTITY_GROUPS = (("organisations", "Countries and organisations"), ("people", "People and offices"),
                 ("weapons_equipment", "Weapons and equipment"), ("units_ships_squadrons", "Squadrons, ships and units (text only)"),
                 ("places", "Places (never mapped to states)"))
REPORT = ROOT / "docs/research/STRANGEREAL_LORE_1991_2020.md"
TEMPLATE = HERE / "report_template.md"


def report(record):
    cell = lambda value: " ".join(str(value).split()).replace("|", "\\|")
    short = lambda d: {"implemented, official-sourced ledger row": "implemented",
                       "implemented by inherited mod content (mod provenance owner); official date is a reference anchor": "inherited mod content",
                       "reference only (named in a ledger, not scripted)": "reference only",
                       "pending (planned wave or track)": "pending",
                       "not covered anywhere in the repository": "not covered",
                       "out of scope (after 2020 or outside Strangereal)": "out of scope"}[d]

    def label(claim):
        return short(claim["disposition"]) + (f" ({claim['pending_wave']})" if claim.get("pending_wave") else "")

    def section(title, rows, citation):
        out = [f"### {title}", "", "| Source | Claim | Disposition |", "| --- | --- | --- |"]
        for row, n, claim in rows:
            out.append(f"| {citation(row, n)} | {cell(claim['paraphrase'])} | {label(claim)} |")
        entities = {}
        for row, n, claim in rows:
            for field, _ in ENTITY_GROUPS:
                for name in claim.get(field, []):
                    entities.setdefault(field, {}).setdefault(name.strip(), []).append(citation(row, n).replace("*", ""))
        for field, heading in ENTITY_GROUPS:
            if entities.get(field):
                names = "; ".join(f"{cell(name)} ({', '.join(dict.fromkeys(keys))})" for name, keys in sorted(entities[field].items(), key=lambda kv: kv[0].lower()))
                out += ["", f"**{heading}:** {names}."]
        return out

    def claims(predicate):
        return [(row, n, claim) for row in record["entries"] if predicate(row) for n, claim in enumerate(row["claims"], 1)]

    dated = lambda row, n: f"*Chronicle, {row['key'].split(' #')[0]}*" + (f" ({n})" if len(row["claims"]) > 1 else "")
    other = lambda row, n: f"*{row['key']}*" + (f" ({n})" if len(row["claims"]) > 1 else "")
    eras = ["## The official record by era", ""]
    for low, high, title in ERAS:
        rows = claims(lambda row: row["page"] == "details" and low <= row["year"] <= high)
        eras += section(title, rows, dated) + [""]
    eras += ["## Super Weapons", ""] + section("Weapons named on the Super Weapons page", claims(lambda row: row["page"] == "weapons"), other)[1:] + [""]
    eras += ["## Title narratives", ""]
    for page, title in (("abstracts", "Abstracts"), ("products", "Product text")):
        eras += section(title, claims(lambda row, page=page: row["page"] == page), other) + [""]
    eras += ["## Outside the 1991–2020 horizon", "",
             "Background before the 1991 start and the 2028–2040 entries are recorded in the index for completeness; "
             "the background rows are reference only, and nothing after 2020 is authored content.", ""]
    eras += section("Background, 1981–1990", claims(lambda row: row["page"] == "details" and row["year"] < 1991), dated)
    later = claims(lambda row: row["page"] == "details" and row["year"] > 2020)
    eras += ["", f"### After 2020", "", f"{len(later)} claims from 2028 to 2040 (ACE COMBAT 3), all out of scope; see the index."]
    counts = {}
    for row in record["entries"]:
        for claim in row["claims"]:
            counts[short(claim["disposition"])] = counts.get(short(claim["disposition"]), 0) + 1
    total = sum(counts.values())
    summary = [f"{len(record['entries'])} official statements hold {total} claims.", "",
               "| Disposition | Claims | Meaning |", "| --- | ---: | --- |"]
    meaning = {"implemented": "a ledger row cites it and IDs implement it",
               "inherited mod content": "the inherited archive covers it without a sourced ledger row; mod provenance",
               "reference only": "a ledger names it; nothing is scripted",
               "pending": "a planned wave owns it (wave in brackets)",
               "not covered": "no ledger row and no script; candidates for later work",
               "out of scope": "after 2020, or a non-Strangereal title"}
    summary += [f"| {k} | {counts.get(k, 0)} | {v} |" for k, v in meaning.items()]
    conflicts = ["## Conflicts with mod content and between official pages", "",
                 "Where the official text and the inherited archive or another official page disagree, "
                 "the archive stays mod provenance and the disagreement is recorded here, not resolved.", "",
                 "| Source | Conflict |", "| --- | --- |"]
    unknowns = ["## What each claim leaves open", "",
                "These are the questions the source does not answer; content must not answer them as fact.", "",
                "| Source | Unknowns |", "| --- | --- |"]
    for row in record["entries"]:
        if row["page"] == "details" and not 1991 <= row["year"] <= 2020:
            continue
        for n, claim in enumerate(row["claims"], 1):
            source = (dated if row["page"] == "details" else other)(row, n)
            text = claim.get("conflicts", "").strip()
            if text and not text.lower().startswith(("none", "no conflict")):
                conflicts.append(f"| {source} | {cell(text)} |")
            if claim.get("unknowns", "").strip():
                unknowns.append(f"| {source} | {cell(claim['unknowns'])} |")
    pages = {page: sum(1 for row in record["entries"] if row["page"] == page) for page in PAGES}
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in (("details", pages["details"]), ("weapons", pages["weapons"]), ("abstracts", pages["abstracts"]),
                       ("products", pages["products"]), ("summary", "\n".join(summary)), ("eras", "\n".join(eras).rstrip()),
                       ("conflicts", "\n".join(conflicts)), ("unknowns", "\n".join(unknowns))):
        text = text.replace("{" + key + "}", str(value))
    return text


def refresh(folder):
    record = load() if RECORD.exists() else dict(schema=1, read_date="", pages={}, entries=[])
    fresh = extract(folder)
    hashes = page_hashes(folder)
    by_key = {(row["page"], row["key"]): row for row in record["entries"]}
    seen, report = set(), []
    for page, rows in fresh.items():
        for row in rows:
            key = (page, row["key"])
            seen.add(key)
            digest = sha(row["text"])
            if key not in by_key:
                entry = dict(page=page, key=row["key"], year=row.get("year"), date=row.get("date"), title=row.get("title"),
                             source_sha256=digest, claims=[], cited_in=[])
                record["entries"].append(entry)
                by_key[key] = entry
                report.append(f"new      {page}: {row['key']}")
            elif by_key[key]["source_sha256"] != digest:
                by_key[key]["source_sha256"] = digest
                by_key[key]["needs_review"] = True
                report.append(f"changed  {page}: {row['key']} (paraphrase needs review)")
    for key, row in by_key.items():
        if key not in seen:
            row["removed_from_source"] = True
            report.append(f"removed  {key[0]}: {key[1]}")
    record["pages"] = {page: dict(url=url, text_sha256=hashes[page]) for page, (url, _) in PAGES.items()}
    record["read_date"] = date.today().isoformat()
    order = {"details": 0, "weapons": 1, "abstracts": 2, "products": 3}
    record["entries"].sort(key=lambda r: (order[r["page"]], r.get("year") or 0, r.get("date") or "", r["key"]))
    save(citations(record))
    return report


def problems(record):
    found = []
    for row in record["entries"]:
        if "text" in row or "official_text" in row:
            found.append(f"{row['key']}: official text must not be stored")
        if not row.get("claims"):
            found.append(f"{row['key']}: no claims")
        for claim in row.get("claims", []):
            for field in AUTHORED:
                if field not in claim:
                    found.append(f"{row['key']}: missing {field}")
            if "official_text" in claim:
                found.append(f"{row['key']}: official text must not be stored")
            if not claim.get("paraphrase"):
                found.append(f"{row['key']}: no paraphrase")
            if claim.get("disposition") not in DISPOSITIONS:
                found.append(f"{row['key']}: unknown disposition")
        if not re.fullmatch(r"[0-9a-f]{64}", row.get("source_sha256", "")):
            found.append(f"{row['key']}: no source hash")
        if row.get("needs_review") or row.get("removed_from_source"):
            found.append(f"{row['key']}: flagged by --refresh and not yet reviewed")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--refresh", metavar="DIR", help="directory holding fresh downloads of the official pages")
    args = parser.parse_args()
    if args.refresh:
        for line in refresh(args.refresh):
            print(line)
        print(f"Chronicle record refreshed from {args.refresh}")
        return
    record = citations(load())
    text = markdown(record)
    failures = problems(record)
    stored = RECORD.read_text(encoding="utf-8").replace("\r\n", "\n")
    current = json.dumps(record, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        if stored != current:
            failures.append("tools/lore/chronicle.json cited_in lists are stale")
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8").replace("\r\n", "\n") != text:
            failures.append("docs/research/CHRONICLE_INDEX.md is stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8").replace("\r\n", "\n") != report(record):
            failures.append("docs/research/STRANGEREAL_LORE_1991_2020.md is stale")
        if failures:
            raise SystemExit("Chronicle index: " + "; ".join(failures))
    else:
        save(record)
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(text, encoding="utf-8", newline="\n")
        REPORT.write_text(report(record), encoding="utf-8", newline="\n")
        if failures:
            raise SystemExit("Chronicle index written with problems: " + "; ".join(failures))
    rows = len(record["entries"])
    print(f"Chronicle index: {rows} official statements, {sum(1 for r in record['entries'] if r['cited_in'])} cited in docs; "
          + ("consistent" if args.check else "written"))


if __name__ == "__main__":
    main()
