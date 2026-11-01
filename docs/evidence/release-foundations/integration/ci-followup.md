# Publication follow-up

PR #47's first changed-file scan exposed 23 inherited missing English keys in
the four event files wrapped by this packet. The scan was not suppressed.
`ac_release_legacy_events_l_english.yml` supplies neutral captions and short
descriptions for those exact existing references: the AWW deployment callback;
Excalibur operational reports; Belkan mobilisation/retrenchment notices; the
hidden standing-order callback; and South Belkan separation/reintegration.
They describe inherited scripted actions, introduce no named person/date or
canonical claim, and do not alter any trigger, effect, state or outcome.

Source layer: inherited mod event contracts, with newly authored English
presentation. References: `events/AWWNB.txt` (`awwnb.2`), `events/Belka.txt`
(`belka_dlp_war.4/.5/.6/.105/.106`, `belka_l_monarchy.1`,
`belka_wacht_am_wal.3`) and `events/South_Belka.txt` (`south_belka.4/.5`).
There is no assertion that these notices establish official ACES chronology.

The Linux capital job also caught a platform-dependent release inventory:
event/template text written on Windows had CRLF while committed checkouts use
LF. The inventory now labels and checks SHA-256 after CRLF-to-LF normalization,
matching the project's existing authored-text convention. It does not normalize
spaces, comments, tokens or binary data. A negative regression changes internal
spacing and proves its digest still changes. Native payload/texture hashes and
the immutable original captures remain separate and untouched.

The second Linux check isolated an additional ordering dependency: WindowsPath
sorts case-insensitively, whereas PosixPath preserves case. All scanned source,
roster and input-hash paths now use the same explicit POSIX-string key. A fourth
inventory regression compares mixed-case Windows and POSIX fixture paths and
requires identical ordering. Text/JSON equality remains a strict gate.

The economy-review input receipt was regenerated from the combined canonical
macro owner after merging PR #46's receipt correction. Its five rendered pages,
twelve settled monthly results and zero source-bound findings remain unchanged.
An outdated source hash is corrected without weakening report equality.

Initial runs retained for audit:

- Missing English keys: <https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41271807660>.
- Linux inventory equality: <https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41271807676>.

The earlier `3b8a3d26...` payload receipts continue to identify their original
mechanical-test phases. The English addition produces a new final payload;
it must not be described as byte-identical to those earlier receipts.
