# Usean partner authoring

`content.py` is the editorial source for 228 focuses, their four-act positions,
policy alternatives and focus-specific art subject pairs. `build.py` compiles
country programmes and national programme modifiers. `programmes.py` owns the distinct
national service rules and reciprocal FCU offers. `narrative.py` owns 24 national
choice events. All generated scripts and English localization are committed.

`scopes.py` curates 29 paid operational scopes and the 117 specific focus
capabilities they require. `scope_rules.py` compiles their finite-resource,
payment, expiry and interruption contracts. `purposes.json` records actual
consumers for all 228 focuses, including the baseline and remaining sole-axis
counts. The individual-capability regression executes every linked action.

Reproduce with Python 3.12 and `Pillow==11.3.0 numpy==2.2.6`:

```powershell
python -B tools/usean_partners/build.py
python -B tools/usean_partners/build_art.py
python -B tools/usean_partners/build.py --check --require-dependencies
python -B tools/usean_partners/test_content.py --require-dependencies
```

The dependency gate requires the real Package 1 `ac_pol_*` capacity owner and
fiscal programme compatibility API. Never add local substitute definitions to
make this gate pass. `test_content.py` explicitly adapts their published
contracts for isolated national-script execution; their complete arithmetic and
GUI behavior belong to the owners' own suites and native acceptance.

`build_art.py` packages original editable glyph geometry into RGBA DDS. It
checks its renderer version, all 228 unique focus render hashes, and byte-for-byte
texture/binding/source-manifest/review-gallery consistency. The manifests record
one-frame dimensions and alpha extrema. `--check` never writes. The contact
sheet and gallery are review artifacts, not native screenshots.

See `docs/USEAN_PARTNER_CAMPAIGNS.md` for the source ledger, mechanics, save
contracts and evidence boundaries. Native testing is paused; no launcher,
installation, user save or settings modification is part of this workflow.
