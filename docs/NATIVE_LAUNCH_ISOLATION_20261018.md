# Native launch isolation design — 2026-10-18

Native launches are currently held. This document records the static correction
to the prior wrapper; it is not runtime evidence.

## What the installed build exposes

Static ASCII inspection of the installed `hoi4.exe` (`Operation Postern
v1.19.3.0.c01a`) found the executable option strings `userdir=` and `mod=`.
The same binary contains the launcher configuration keys `launcher-settings.json`,
`gameDataPath`, and `userdir.txt`. The wrapper therefore uses explicit
`-userdir=<profile>` and `-mod=<descriptor>` arguments, with a profile-local
`dlc_load.json` selecting exactly one descriptor.

## Why the prior run was invalid

The prior final17 descriptor was under the G: profile, but its exact `path=`
entry pointed to `C:\Users\New\Documents\Paradox Interactive\Hearts of Iron IV\mod\ProjectUlysses_Continuation_native_20261018`.
The G: profile did not contain that payload. The wrapper also did not provide an
explicit `-userdir=`/`-mod=` pair or fail closed on the mismatch. Its native
observations are revoked.

## Fail-closed contract

`tools/Test-NativeLaunchConfig.ps1` requires:

- an isolated profile outside the normal HOI4 user-data tree;
- a descriptor and payload both inside that profile's `mod/` directory;
- an exact descriptor `path=` resolving to that payload;
- exactly one `dlc_load.json` enabled mod matching the descriptor;
- required payload directories and no unexpected top-level mod entries;
- no Millennium Dawn, MD/OEM, or vanilla markers;
- unchanged launcher settings when a preserved baseline is supplied.

The validator reports `RuntimeIsolationProven=False` even when the static
contract passes. It never launches HOI4.

The companion local wrapper is `C:\Users\New\Documents\Codex\2026-10-16\task\run_native_reviewfix.ps1`.
It now defaults to the validator's read-only plan, can prepare a fresh profile
only under `G:\Project-Ulysses-Continuation-native-test-20261018`, never edits
installed launcher settings, and refuses the `-Launch` switch while native
testing is paused.
