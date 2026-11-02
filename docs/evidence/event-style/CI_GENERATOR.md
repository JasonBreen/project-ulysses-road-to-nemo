# Original event producer and CI composition

The initial style publication exposed the original interface regression gate:
`build_events_ui.py --check` still generated the pre-style bindings. See failed
runs [41286416282](https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41286416282)
and [41286379471](https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41286379471),
with [the retained output](ci-failure.txt). No required check was removed.

The original producer now retains `build_base()` and composes its actual result
through `event_style.migration.generated_from()`. That entry point requires the
entire base text to equal the immutable original fit capture before applying
the same23 substitutions. It cannot ignore a changed upstream layout by reading
only a separate snapshot. Both full lexical and ordered-AST restoration remain
mandatory. The additional regression exercises the real producer and rejects
unregistered geometry, movement and sound changes. EventStyle now has15 cases;
its generation test also invokes the original producer CLI directly.

The authored style manifest was explicitly regenerated for the changed migration
source hash. Only that provenance field changed; DDS, SVG, GUI and font bytes
remain identical. The original fit capture and all protected sources remain
unchanged.

At `bef1305c1b7a472c82c80b1492eccd6e87e77d44`, six of seven selected groups
passed: style15, original interfaces8, fit15, review equality, effective base-only
ownership and strict authored assets. The final static group correctly rejected
the local PATH's different Pillow packaging output. That failed
[phase](ci-generator-composition/results.json) is retained. No images were
regenerated with the wrong library and no equality requirement was relaxed.

Using the selected Python3.12/Pillow11.3 environment and the parent's corrected,
read-only PowerShell launcher, all **three affected groups pass** at
`5f66ce07ad61301a342ea2c1ed72811be30ba739`: EventStyle15, original interface8,
and full installed-reference static validation. The
[before/after receipt](ci-generator-final/results.json) covers **8,773** raw
source inputs, unchanged fingerprint
`79ff859582c2ce354bf94f4e8e13655c63ca83758a4c77b7eca7ce7c3d8e39d2`.
The original full14-group and five-runner phases retain their own identities.

The style runner supports explicit repeated `--only <check>` arguments for
separate affected phases; it retains no earlier rows as current results. Its
full default profile now also includes the original interface gate.

Mod payload remains
`2858b8d653b80467124345fc04e4d790115277948408c16042f35107acc0999f`.
Event-window and decision ownership remain zero in the explicit base-only
profile; wider pools and native acceptance remain open. Native testing, desktop,
normal installation, display settings and saves were not changed.
