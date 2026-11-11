# Playtest: wiring repairs, merged Usea Depth content and the national-depth trees

**Status: planned and not run.** You approve and run this playtest by hand.
- Nothing here launches the game or touches your installed game, settings or
  saves (`AGENTS.md`).
- Every case in `docs/native_evidence/wiring_depth/cases.csv` is `NOT_RUN`
  until a native run you approve fills it in.
- Static checks, including the wiring audit, are never native results.

**What it extends:**
- #70, the 1991 → Belkan War → postwar playtest;
- #8, the native and long-run tests;
- the existing specifications it reuses:
  - [BELKAN_WAR_PLAYTEST_PLAN.md](BELKAN_WAR_PLAYTEST_PLAN.md) for the Belkan
    routes, console steps and save checkpoints;
  - [NATIVE_PLAYTEST_CHECKLIST.md](NATIVE_PLAYTEST_CHECKLIST.md);
  - [PLAYTEST_CONTINENTAL_WAR.md](PLAYTEST_CONTINENTAL_WAR.md) for the 2003
    war;
  - [NATIVE_LAUNCH_ISOLATION_20261018.md](NATIVE_LAUNCH_ISOLATION_20261018.md)
    for the fail-closed isolated launch.

It adds only what this branch changes:
- the repairs found by the wiring audit ([WIRING_AUDIT.md](WIRING_AUDIT.md));
- main's Usea Depth packages, merged here;
- the lobby restyle combined with main's responsive geometry;
- the national-depth trees ([NATIONAL_DEPTH.md](NATIONAL_DEPTH.md)).

## The case list

`tools/wiring/playtest_cases.py` writes the case list. The case IDs give the
groups:

| Group | Cases |
| --- | --- |
| Preflight | candidate, isolation and control log |
| Launch | 1991 start; the lobby's restyle and responsive geometry |
| Usea Depth | one case per adopt-decision package (minors A and B); one per import block (Erusea, Central Usea, North Point, partners) |
| Focus screens | main's era-opening gates reveal campaign lanes after their date |
| National depth | per tree: screen, a 1991–1996 natural play, every event once, decisions |
| Wiring repairs | the AWW and SER networks, Sapin, Excalibur and Hoffnung, the dead idea references, live event text, the Belkan defeat flag |
| Long run | AI observer 1991–2004; save and reload at checkpoints |

`python -B tools/wiring/playtest_cases.py --check` runs in CI. It fails when the
list is stale, or when a case names an ID that no longer exists in the mod, so
the packet keeps in step as content waves land.

## Preflight

1. **Freeze the candidate.**
   - Record its full SHA, the payload manifest hash and the descriptor checksum.
   - Run the static suite (`tools/Test-UlyssesStatic.ps1`) and keep its output.
     List the known Linux-only image-byte failures separately; on Windows CI
     they pass.
2. **Isolate.** `tools/Test-NativeLaunchConfig.ps1` passes for a disposable
   profile:
   - the profile is outside your normal HOI4 user data;
   - exactly one enabled mod, whose descriptor `path=` resolves to the payload.

   Record SHA-256 hashes of your normal saves and launcher configuration before
   and after the run.
3. **Control log.** Launch the same copied engine with no mod to the main menu,
   and keep its `error.log` to attribute errors.
4. Record the HOI4 build, DLC list, game rules, difficulty, resolution and UI
   scale.

## Routes and rules

- **Natural route first.** A case counts as a reachability pass only on a
  natural route.
- **Forced routes** (console `event`, `tag`, `focus.autocomplete`) run only in
  separate saves labelled as diagnostic. They are recorded as
  `native-pass (forced)` and prove only that the downstream content works.
- **Belkan cases** follow the routes and console steps in
  `BELKAN_WAR_PLAYTEST_PLAN.md`. For `belkan-defeat-flag`, reuse its O3
  natural defeat route.

**Wiring-repair specifics:**

| Case | Route | What to check |
| --- | --- | --- |
| `wire-release-network-hidden` | Release AWW and SER through their existing release paths. Diagnostic saves may use the release decisions directly. | The repair decision never appears, and no political power is spent. |
| `wire-sapin-demobilise` | Needs a defensive war for Sapin. | Mobilise one state's national guard. After peace, demobilisation appears and removes the `sap_draft_infantry_id` units. |
| `wire-sapin-chain-ends` | `event sapin_civil_war.1` in a diagnostic save. | `list_flags` shows `sap_political_crisis_over`, and no parliament event (`sapin_politics.4`–`.13`) follows. |
| `wire-hoffnung-achievement` | Diagnostic save during Wacht am Wal with Excalibur land strikes unlocked. | A strike on Hoffnung (state 602) sets `used_excalibur_on_hoffnung_achievement`. Achievements stay off in a modified run, so read the flag rather than the achievement popup. |

**National-depth trees (Perbla now; each later wave adds its own):**
1. Open the tree at 1920×1080 and at your UI scale, and screenshot it beside its
   review image in `docs/evidence/national-depth/`.
2. Play 1991–1996 on the natural route. Take one regime path, whose AI weight
   is 0, and one exclusive economic path.

## Save checkpoints

Save, then reload:
- at the start of 1991, and in 1992, 1996, 2000 and 2004;
- before and after each forced diagnostic.

Raw saves stay outside Git. For Belkan checkpoints, use
`tools/belkan_balance/native_checkpoint.py` as the Belkan plan describes.

## Recording results

- **Status.** Fill in `Status` and `Evidence` for each row: `native-pass`,
  `native-pass (forced)`, `native-fail` or `not exercised`.
- **Separate columns.** Natural, forced and static results stay apart. Never
  copy a static result into `Status`.
- **Failures.** Grade each one blocker, major, minor or cosmetic. Record its
  ID, the `error.log` excerpt (attributed against the control log) and the
  steps to reproduce.
- **Report.** Store the dated report and the preservation audit in
  `docs/native_evidence/wiring_depth/<date>/`.
- **Follow-ups.** Each blocker becomes an issue linked to #70 and #8.

## Suggested timing

Run this together with the #70 Belkan run, after:
- this branch's merge, wiring repairs and compiler alignment (done 11 November
  2026);
- the first national-campaign wave (era 1 for the 29 countries with nothing
  yet), which waits on your Perbla review.

One isolated session then covers the wiring repairs, Usea Depth, Perbla and the
new trees.
