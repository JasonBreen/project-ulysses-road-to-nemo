# PR53 complete country-state assertions

This source-only correction addresses
[the review finding](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/53#discussion_r4434795354)
at the remotely verified published head
`65666017797753012327b1183d537b5edab11b41`. Code commit
`6ad2de3e0a04c7d0896489eee5795b5f5dfd2efd` changes only the three new
enabled-but-unready test snapshots: `copy.deepcopy(vars(country))` is compared
with the complete current `vars(country)`. This includes declared dataclass
fields and dynamically attached attributes, including political power, ideas
and timed ideas. Deep copying also protects nested sets and dictionaries from
aliasing. No production guard, price, payment, reservation, fiscal writer,
interpreter, generator, delivered mod file or original source capture changes.

The [fresh four-group results](results.json) all pass under the existing clean
source-fence runner:

| Check | Result |
| --- | --- |
| Actual partner-owner integration |5 tests PASS |
| Actual reconstruction-owner execution |18 tests PASS |
| Actual superpower-owner execution |15 tests PASS |
| Full static check with read-only installed reference and immutable baseline |PASS |

The strengthened unready matrices execute four authoritative account faults for
all81 scopes:29 partner,20 reconstruction and32 superpower, giving324 rejected
starts. They retain actual `ac_econ_enabled = yes` and `ac_econ_ready = no`
assertions. Existing successful and interrupted programme coverage remains in
the same three suites. Their readiness, payment and capacity owners are actual
generated scripts; no readiness or financial substitute is introduced.

The [nine mutation probes](mutation-probes.json) separately verify assertion
sensitivity. Each owner's actual unready test is run with an in-memory change
to political power, the idea set or timed-idea state after an actual rejected
start. Dataclass equality ignores all9 injected changes; the corrected full-state
assertions catch all9. The partner timed-idea probe additionally verifies that a
newly attached attribute is detected; reconstruction/superpower probes mutate
their existing nested dictionaries. These are intentional test mutations, not
production behavior or newly discovered charges.

Both suite execution and sensitivity probes retain matching before/after raw
source fences:8705 tracked inputs at the clean code commit, with SHA256
`b10893e3eb20a8c9ee99d71322cced4ad3bf91b64ae93158fd5dd9785a7de222`.
The source fence excludes review evidence itself. The only source difference
from the published parent is the three specified test files. All earlier
captures and completed story checkpoints remain untouched. Machine-local paths
in the new logs/commands are replaced with explicit placeholders; test statuses,
source fingerprints and payload hashes are retained unchanged.

Reproduce from the clean correction branch with Python3.12, Pillow11.3.0 and the
existing repository dependencies:

```text
python -B tools/programme_funding/run_checks.py --output docs/evidence/programme-funding/dynamic-state-review --reference <read-only-installed-reference> --baseline <immutable-baseline-payload> --only partner-runtime --only reconstruction-runtime --only superpower-runtime --only full-static
python -B docs/evidence/programme-funding/dynamic-state-review/mutation_probe.py
```

The helper performs only in-memory mutations and retains its own source fence.
This is offline script/assertion and static evidence. It does not establish
native game behavior, serialization, fixed-point precision or AI pacing. No
native execution, installation synchronization, push, review reply or thread
resolution was performed.
