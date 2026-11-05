# Decision-category text

`measure.py` resolves every decision-category description (`<category>_desc`)
through its `[slots]` and measures it with the shipped ACBriefing16 bitmap font at
the width of the `full_text` control in `interface/countrydecisionview.gui`
(470 px). Offline measurement only; native rendering is untested (#8).

- Defined texts (`common/scripted_localisation`, `common/custom_localization`)
  resolve recursively, guarded against cycles. Variables (`[?var|0]`) print as
  `9999`; scope names (`[ROOT.GetName]`) as `Representative Country`; text icons
  (`£name`) count at their sprite frame width, or 24 px when the sprite is an
  engine one.
- Two variants: every slot at its widest alternative (`longest`) and at its
  narrowest (`shortest`). Slots are chosen independently, so `longest` can
  combine states that play cannot reach together; the allowlist reasons say so.
- Hard failures (a missing glyph, a word wider than the control, a cycle, a slot
  with no defined text, a missing key) fail `--check`.
- A category longer than `line_budget` in `contract.json` (14 lines) fails
  `--check` unless the contract allowlists it with a reason; an allowlist entry
  for a category within budget also fails, so the list cannot go stale.
- The `custom_icons` strip at y 75 is recorded; no category declares custom
  icons, which `tools/Test-DecisionText.py` checks.

Outputs: `docs/evidence/decision-text/measurements.json`, `index.html` and
`categories-longest.png` (the six longest categories, drawn unwrapped from the
measured lines). `python -B tools/decision_text/measure.py` writes them;
`--check` compares them (PNG by size and RGBA). `tools/content_waves/refresh_records.py`
regenerates them with the other shared records.

## The 5 November 2026 repair

Before: the two superpower registers measured 48 and 47 lines, seven content-wave
service categories 15–29 and two reconstruction categories 16. The service
categories printed every register (with "A standing policy has not yet been
selected" for each unchosen one) and repeated the cost paragraph.

After (user decision: show chosen policies only):

- Content waves (`tools/content_waves/framework.py`) and reconstruction
  (`tools/reconstruction/build.py`): one `<branch>_<P>_policy_line` defined text
  per register prints `Standing policy: <policy>` (with `(settled)` once settled)
  and nothing while unchosen. The category is status, one line per chosen policy,
  then the fee. The cost paragraph moves to `<P>_funded_cost_tooltip`, the
  engine's hover text for `custom_cost_text` (with `_blocked` for the
  unaffordable state).
- Superpower registers (`tools/superpowers/build.py`): the category keeps state
  (reserved units or allocation shares, completed periods, fee, last
  interruption) and one short line per non-idle scope; the standing rules move to
  `ac_snp_cost_ose_civil_tooltip`, `ac_snp_cost_ose_protected_tooltip` and
  `ac_snp_cost_yuk_tooltip`.

Result: 69 categories, 0 hard failures; five over budget, all allowlisted with
reasons (the inherited `OSE_congress_dec`, Erusea's two war-owner categories in
their all-settled worst case, and the two registers' all-scopes worst case).
