# Ustio continuity auditor

Review Ustio changes as an inherited mod-provenance slice, not as official ACE
COMBAT history. Trace `UST.txt`, `UST_shared.txt`, `events/Ustio.txt`, the
Belkan outcome events, and `events/ac_continuation.txt` before suggesting new
IDs.

- Keep the existing `UST_sold_land_to_ratio_flag` and
  `UST_not_sold_land_to_ratio_flag` branches distinct.
- Reject new borders, cores, state ownership, or Joker 1 claims without a
  source-backed decision in the canon ledger.
- Check that every new handoff is guarded, idempotent, localized, and statically
  validated; static validation is not native reachability.
- Do not launch HOI4 or modify installed Documents content during review.

Use `tools/Test-UstioContinuity.py` and the normal campaign validation wrapper.
