# Review findings: source identity and escaped display text

Both actionable findings on PR #46 are addressed in source:

- <https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/46#discussion_r4434333731>:
  HEAD equality alone did not establish that the tested inputs matched the
  commit. The integration runner now rejects staged, unstaged and untracked
  source changes before and after execution. It also fingerprints every
  tracked non-evidence input using its raw working-tree bytes and verifies the
  same fingerprint after the checks. Generated `docs/evidence` is the explicit
  exception. The report retains this input fingerprint alongside the separate
  delivered-mod payload hash. This is a boundary check, not an immutable sandbox
  or proof that a transient change reverted between observations never happened.
- <https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/46#discussion_r4434333748>:
  the inherited token mask mishandled escaped quotes in GUI display strings.
  Font migration now validates structural balance and masks whole escape-aware
  string tokens/comments while retaining real assignment delimiters. The
  existing display-string regression now includes quoted font-like text,
  escaped backslashes, comment characters and `buttonFont`-like text. It checks
  exact preservation of all bytes except the actual reviewed font assignment,
  valid structure and restoration to the original parsed control tree.

Four temporary-Git regressions cover clean input/evidence output, dirty source,
a different clean commit, and a raw CRLF change that Git text normalization
considers clean. The last case still fails the raw input-fingerprint comparison.
They run on both CI platforms. The ten font tests and current 23 LAND tests
retain all original geometry, protected-source, glyph-alpha and physical-cost
checks. The production GUI and delivered textures are unchanged by these fixes.

Earlier phase receipts remain valid records of the commands that ran. Their
HEAD-only runner did not enforce this stronger clean-input boundary; do not
retroactively describe those receipts as having the new guard. The separately
recorded review-fix phase exercises the strengthened runner itself.

No review-thread reply/resolution, native launch, desktop action, installation
change, merge or release publication is performed by this repair.
