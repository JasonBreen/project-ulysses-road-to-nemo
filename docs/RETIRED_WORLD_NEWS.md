# Inherited Earth news compatibility retirement

The inherited `events/NewsEvents.txt` retained automatic WWII and Earth-specific
world news inside the Strangereal campaign. This package replaces that file with
294 hidden, triggered-only, effect-free compatibility handlers. It does not add a
new historical event, change a war outcome or substitute a generic news observer
for the existing authored Strangereal campaigns.

The set is the union of 286 IDs in the inherited mod file and 294 IDs in the
installed 1.19.4.1 reference, including eight reference IDs absent from the old
override. Existing IDs remain valid for previously queued calls; the handlers
have no automatic trigger, mean time to happen, displayed options, illustration
or reward. No `replace_path = events` or entire event-family deletion is used.

The established `tools/usea_expansion/build_retired_mechanics.py` remains the
owner. Its explicit contract now distinguishes `news_event` from the default
`country_event`. Existing bounded crisis cleanup is preserved. Generated output
and its contract ship together; UTF-8/LF packaging is explicit and reproducible.

`retired_news_sources.json` records the intake commit, original/reference hashes,
ID sets and two actual installed hidden-news examples by ID and hash. It contains
metadata, not copied installed source or media. The same file records normalized
hashes of every other authored event file as a preservation receipt for this
package. Future changes to those files belong to their own owners; these
receipts are not an instruction to freeze later campaign development.

The seven focused regressions check the independent ID union, every actual
handler's AST, literal event callers, quoted/commented text, generator ownership
and reproducibility. With a supplied read-only reference, they also recapture the
installed ID set and verify the hidden-news examples. The caller scan covers
literal block and short-form calls in the mod's common/events/history text. It
does not claim that engine, DLC or dynamically assembled calls are absent.
Adjacent inline comments are tokenized separately even when no space precedes
`#`; quoted text remains atomic. Without an installed reference, the one
primary-metadata test is explicitly skipped; six source regressions run in CI.

Reproduce the bounded source checks from the repository root:

```powershell
python -B tools/usea_expansion/build_retired_mechanics.py --check
python -B tools/Test-RetiredWorldNews.py --reference '<read-only HOI4 root>'
python -B tools/Test-InterfaceRepairs.py
python -B tools/audit_visual_dependencies.py --strict-all
pwsh -NoProfile -File tools/Test-UlyssesStatic.ps1 -ModRoot mod/2985041246 -ReferenceGameRoot '<read-only HOI4 root>' -BaselineRoot '<immutable inherited baseline>'
```

The evidence index is `docs/evidence/retired-world-news/validation.json`.
Source/static parsing and compatibility-shape checks do not establish native
event suppression, saves or rendering. Native testing remains paused, and the
normal installation, desktop, settings and saves were not changed. Wider
WWII/Earth event families, generic modern unscripted-war news, DLC fallbacks,
models, portrait pools and audio remain in the full conversion backlog. This
small retirement does not pass the complete anti-vanilla gate.
