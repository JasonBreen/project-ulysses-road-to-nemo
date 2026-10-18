# Native compatibility auditor

Audit inherited HOI4 content against the installed native version before changing gameplay.

- Start from the immutable archive/baseline and the active `mod/2985041246` copy.
- Treat every legacy identifier as a contract to classify: preserve, map to a verified native identifier, or quarantine with a reason.
- Use whole-token replacements only. Never run a mechanical port twice without checking that it is idempotent.
- Inspect `common/units`, `common/technologies`, `history/countries`, `history/units`, equipment groups, AI templates and descriptors together.
- Run the repository static checks and an isolated native startup only when explicitly authorized; restore launcher settings and never modify another playset.
- Report source paths, exact identifiers, native version, profile path, log filters, and known base-game diagnostics separately.

Acceptance is evidence-backed: no claim of runtime reachability, save/reload stability, AI behavior, or long-run play unless that exact behavior was exercised and recorded.
