# Research font repair: source acceptance record

The changed research screen now uses original briefing typography for all 301
inherited `font`/`buttonFont` assignments. The current LAND-composed screen has
316 assignments: twelve new `ACResearch*` roles plus its existing two authored
`ACBriefing*` fonts. No engine glyph pixels, complete engine font files, country
identities, research rules or inherited GUI geometry were imported or changed.

This isolated repair starts from verified remote main
`3810d1abeb9749a265b7b48e8d9eccddf08b1be2` and reviewed LAND parent
`c767c2da8222e0534ba4ed308d9dce1d0e2b14f4`. Runtime binding/migration commit
`5b4a25d243bfbf9012869d4a6da1874317c64fe4` supplies the complete payload change;
`0fd33670` adds the ink regressions, composable inventory test and measurements.
The installed-reference capture records its actual payload source head. Validation
logs pin their own source head and normalized source hashes separately.

The captured research SOURCE retains normalized SHA256
`d63f9f14304714a7359280fa2abb57addad229412a54ce05b3db80e0c0ad51f6`.
All 1,050 protected source fingerprints remain unchanged, including the already
recorded narrow UST delimiter repair. Strict normalization restores only the
twelve reviewed font substitutions after the actual owner removes its registered
page/tab and two description scrollbars. A reverted alias, another unreviewed
authored alias, geometry change or unregistered node cannot be hidden by it.

## Evidence and reproducibility

- [Validation results](validation/results.json) identify every affected command,
  exit status, source hash and log. The font suite has ten regressions; LAND has
  twenty-two; the interface repair suite has eight. The actual presentation
  parser checks 85 files, 561 counter bindings and two superevent category members.
  Strict explicit-texture checking inspects 6,968 sprite definitions and 1,264
  focus icons with zero missing asset references.
- [Effective reference capture](research-dependencies.json) rechecks the separate
  installed 1.19.4.1 primary font contract, which matches the immutable reviewed
  metadata. Its explicit base-only static profile resolves all 316 actual font
  assignments under fourteen authored aliases using exactly four hash-pinned
  FNT/DDS resource approvals. The research and decision screen ownership gates
  both have zero failures. Installed DLC is inventoried without being inferred
  enabled; the profile selects no DLC.
- [Bounds and alpha measurements](bounds.json) retain all 301 original control
  records, 292 declared text rectangles, 148 literal year measurements, all 361
  glyph alpha bounds for each of the two reused atlases, and ten illustrative
  label/name samples. The [offline font review](font-roles.png) uses the shipped
  authored atlas pixels and actual inherited rectangle sizes. It is not a game
  screenshot. Pinned Pillow 11.3.0 reproduces the PNG without using FreeType.

The original inline G/R/Y/H/T and applicable O/g state-color values remain exact.
Former dark stat labels use secondary light text on navy; amounts stay brighter,
and subordinate headings use muted cyan. Original close-button icons, controls,
tooltips, keyboard shortcuts and research actions remain bound to the same names.

## Measured limits and pending native coverage

The sixteen-point atlas's visible ink spans y=1..19; the twenty-point atlas spans
y=2..25 (exclusive bottom). These envelopes fit the minimum twenty- and
thirty-pixel rectangles assigned to those fonts. Baseline-shift adapters that
appeared to match old compact line/base metadata were rejected: shifts of minus
three/four pixels cut accented capitals off above y=0. The negative regression
measures actual alpha, so declaring a smaller line height cannot make it pass.

The authored atlas also has existing horizontal side bearings: certain letters
can extend one pixel left of the origin, and the fraction slash three. Dynamic
technology names, unit names, quantities and substituted text therefore retain
their original tooltips and maximum rectangles, but arbitrary string width or
left-edge clipping is not certified. Dense parent-row clipping, multiline
spacing, rasterization, color substitution and input remain native coverage
items. The source report's old font-line budget overruns are not presented as
proof of visible clipping.

Native testing remains paused. No game was launched, normal installation changed,
or user saves/settings touched. The requested 3440x1440 at 1.0, 1920x1080 at 1.0
and 2560x1440 at 1.25 checks remain untested for this payload. Language-specific
engine font fallbacks are outside this English repair. The completed global
presentation gate was not requested; its report explicitly remains unpassed.
The focused ownership/font approvals do not waive the wider conversion backlog.

The pure migration/restoration API and reproduction commands are documented in
`tools/research_fonts/README.md`. AIR and future registered pages can compose with
it without replacing SOURCE. After composition, regenerate the measurement
artifact before its `--check`; the original 301 migrated assignments remain fixed
while the new page's authored controls may increase the current assignment count.

## Integration and raw provenance hashes

The two existing text files below now have narrowly scoped `text eol=lf`
attributes. A pre-attribute Windows worktree can still contain an old CRLF copy.
Before profile recapture, verify each worktree file's LF-normalized contents equal
its committed Git blob; only then restore that exact blob's bytes. Use a binary
write of `git show HEAD:<repository-relative-path>` output, avoiding a shell text
redirect that may change encoding. Do not regenerate glyphs, rewrite differences
other than the verified line endings, or normalize DDS bytes.

The VFS provenance approvals remain **raw exact-file SHA256**, not normalized
text approvals:

| Repository-relative file | Canonical raw SHA256 |
| --- | --- |
| `mod/2985041246/gfx/fonts/ACBriefing16.fnt` | `b54c4e8a75752f56e889f8b9c8b04eda4f6ad8e49cdb2dcdf4a0cf31b2e3879b` |
| `mod/2985041246/gfx/fonts/ACBriefing20.fnt` | `dbc437adbc17ae885ef6ea96bf0deedb419796510a4a0a3dda6df58d273fde22` |
| `mod/2985041246/gfx/fonts/ACBriefing16.dds` | `af2f90a166ef497dc5e58a8fd2c65ff2ba06680a73dea164c1045da235561a7d` |
| `mod/2985041246/gfx/fonts/ACBriefing20.dds` | `e5893960b4ee64e7bb511fb7324b2188edc17a88d66b6d3b3b723411e2c8e625` |

The separate asset manifest explicitly labels its FNT/source text hashes as
LF-normalized and its DDS hashes as raw. That metadata convention does not change
the effective dependency auditor's raw provenance requirement. The successful
AIR-composed check follows the same per-file rule; other text files and all
binary resources receive no blanket normalization exception.
