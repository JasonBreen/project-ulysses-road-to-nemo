# PR55 review fixes before the separate padding repair

Source `ec6238458a88256fdc8ff32236e71c5e6c216cce` is pinned over 8774 tracked inputs with identical before/after raw hash `8b1c74cef7e2336fc280b030b22e85bd2f250b375dc13a01ab8bef78b9c29060`. The report contains **9 passing and 3 failing groups out of 12**. Counts are derived directly from `source-checks/results.json`.

The EventStyle gate retains two failures out of 19 tests: actual text fit and the review CLI both reject the 16 newly exposed horizontal-ink findings. All four new review regressions pass, including real narrow-word/top/left negatives, repeated conditional fields, native font registration and same-sized opaque frame rebinding. The effective auditor's 42 tests pass.

The first static-reference attempt used WindowsApps Python and failed the known UCW packaging-version check. That environmental failure remains in its original receipt. The isolated rerun with the pinned interpreter directory on subprocess PATH passed at the same source `ec6238458a88256fdc8ff32236e71c5e6c216cce`; see `static-pinned-host/results.json`. No source was changed between those two attempts.

`raw-metrics-before-padding.json` preserves all 1,892 field records, 16 horizontal failures, 256 scroll-accessible bottom overflows, 130 dynamic fields and 90 inherited localization exclusions before any padding change. `original-art-preservation.json` proves all 12 DDS textures and 12 editable SVG masters are byte-identical to published base 2cf68b83. The original GUI/captures and 23-value registration remain unchanged in this phase.

`padding-primary.json` records native nonzero borderSize examples. These prove property existence, not a verified maxWidth/interior formula. Root separately authorized an explicit provisional two-inset source repair with both width interpretations modeled and native semantics unaccepted. That repair is a later source commit; no tolerance or failure exemption is applied here.

The subsequent separately committed provisional-padding phase passes all12 affected groups. See [padding-source-checks/README.md](padding-source-checks/README.md) for the exact source receipt and both modeled interpretations; native inset semantics remain unaccepted. The pre-padding failures above are retained as historical evidence.
