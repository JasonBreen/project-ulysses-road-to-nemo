# PR54 control and fresh-evidence review corrections

All four review findings are addressed without changing a texture, narrative,
GUI control or original capture:

- [Required paths](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/54#discussion_r4434819757): country/news pictures require the exact reviewed full control paths and positions, not inferred event types based on coordinates alone. Renamed or relocated roots fail.
- [Anchors](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/54#discussion_r4434819772): pictures and their actual sibling obstacles require the supported upper-left orientation. Unknown, conflicting or changed anchors fail before bounds are certified.
- [Fresh audit output](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/54#discussion_r4434819797): the prior graph report is removed before the subprocess. A crash, missing file or invalid fresh JSON cannot reuse an old15-fallback report.
- [Failed current receipts](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/54#discussion_r4434819808): starting a new invocation invalidates the current passing receipt and archives its report/logs. Unexpected ownership results write a failed current receipt before exit, retaining actual decision failures rather than an unconditional empty list. Source verification failure also prevents a pass.

At clean source `0c4603433c4dc264ecb18053494a6e5756c63c43`, all **15 configured
required groups pass**, including **EventPictures17** and **EventEvidence8**.
The [complete result](results.json) retains a sixteenth, separately classified
broader-screen audit with its exact original15-fallback failure. The known
backlog is accepted only as that historical bounded contract, not whole-window,
global or native closure. All actual decision failures are recorded.

Before/after source fences cover **8,735 tracked raw non-evidence inputs**,
unchanged fingerprint
`8cd674fcf6ed93cce81101e4b9df60924038ca06489184c2cd55ea279a45c657`.
The code includes PR53's complete dynamic-state assertion review correction.
Mod payload remains
`82e2745942177cfe35f3732fcce47d5bc6a0285bba2bfead5d967a1af669acae`.

The eight evidence regressions execute real subprocesses for crashed/no-report,
invalid-report and actual decision-failure cases. They also check prior-receipt
invalidation/archive retention, unknown screens, changed source, empty runs and
the explicit historical backlog. The new cases run in CI. The control tests
mutate actual required GUI paths and both picture/sibling anchors. An initial
fixture changed the unrelated country title instead of the required news-title
sibling; its path-specific correction now exercises every intended control.

Earlier14-group, CI-interpreter and artwork phases retain their original source
identities. Final-head remote CI is reported separately. No review thread has
been replied to or resolved. Native testing, normal installation, display and
user saves remain untouched.
