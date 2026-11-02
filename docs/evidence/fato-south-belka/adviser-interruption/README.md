# South Belkan adviser interruption review

[Review finding](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/50#discussion_r4434617612).

Osean capitulation and annexation callbacks previously marked South Belka's adviser route as refused even when no request or visit existed. That could replace its earned accountable or interim assessment with the domestic-after-refusal outcome.

The generator and committed effect now require South Belka to have an open request or an active visit before recording an interruption. Osea's stale notification is still cleared. Existing arrangements retain their cleanup, paid costs and actual acceptance history; repeated callbacks are inert.

Two added actual-source tests cover 12 no-arrangement scenarios (two callbacks, three histories and two case outcomes), plus four pending/accepted arrangements with repeated callbacks. Complete instance dictionaries are compared for unaffected South Belka. Before the fix, all 12 no-arrangement scenarios failed; the four existing-arrangement scenarios passed. After the fix all scenarios pass, including the resulting accountable/interim assessment.

Final tested source: `7036c4548dcc6f63049c219fb29c0f0d86d80910`. All **six selected source groups pass**, including **30 actual-owner tests**, source/art 10, both generators, the installed-primary contract and authored assets `--strict-all`. The 8,148 raw source inputs retain SHA-256 `00a7b5562755055e5ab592247ae918b6f169f993d47cc79cbcff6f269071bbf1` before and after. Payload SHA-256: `3abffbf71232952437b7592dc4d3fc3fea8f2641c740d4e1bffa97091372f102`.

[Final checks](final-checks/checks.json) and [payload metadata](payload.json) bind these results to that source. The initial source `b1ea5f80` retained its three passing groups and one failed source/art group in [the first receipt](checks/checks.json): the artwork manifest still named the old generator dependency hash. Refreshing that one hash changed no texture or artwork master. The complete six-group final run then passed.

Native testing remains paused. This is source execution and primary-reference validation, not engine callback, save/reload, AI or visual acceptance. No normal installation, profile or save was changed.
