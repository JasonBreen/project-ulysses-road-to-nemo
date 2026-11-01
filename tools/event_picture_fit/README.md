# Bounded event-picture packaging API

The implementation and provenance ledger is
[docs/EVENT_PICTURE_FIT.md](../../docs/EVENT_PICTURE_FIT.md).
Use Python3.12/Pillow11.3.0, matching CI. No engine or desktop is launched.

```python
from event_picture_fit.fit import contain
country_texture = contain(original_master, 'country_event')  #210×176
news_texture = contain(original_master, 'news_event')        #397×153
```

`original_master` may be a path or a Pillow image. The helper preserves the full
composition using Lanczos containment on opaque navy. Existing smaller assets
that already fit do not need conversion. Frame dimensions and effective GUI
scale are checked against the actual required picture/options/title controls,
not solely an asset manifest.

The read-only consumer audit takes an explicit list of event files:

```python
from event_picture_fit.audit import audit, DEFAULT_EVENTS
report = audit(DEFAULT_EVENTS + ['events/new_country_owner.txt'])
```

The CLI `--events` option may be repeated and replaces the default seven-file
scope. Unsupported dynamic picture syntax fails closed instead of being silently
certified. Explicit pictures must resolve to unambiguous actual sprite and DDS
definitions. Picture-implicit events are recorded separately; they do not count
as certified visible consumers. The current32 implicit entries are hidden.

```powershell
python -B tools/Test-EventPictures.py
python -B tools/event_picture_fit/audit.py
python -B tools/event_picture_fit/review.py
python -B tools/event_picture_fit/review.py --check
python -B tools/reconstruction/build_art.py --check
python -B tools/superpowers/build_art.py --check
python -B tools/fato_south_belka/build_art.py --check
python -B tools/anea/build_art.py --check
python -B tools/anea/build_system.py --check
python -B tools/build_continental_war.py --check
# After committing a clean candidate, retain exact-source broad evidence:
python -B tools/event_picture_fit/run_checks.py --engine <read-only-installed-HOI4>
```

`contract.json` is the original review capture, not an automatically refreshable
baseline. `proof.py` admits only the24 explicitly reviewed news picture changes;
country texture and original-master preservation remains independent. The
existing authoritative generators and committed output change together. The
Continental War generator also packages the six original news sources/bindings.
Do not run `capture.py` over an existing contract to bless another change.

The14 focused regressions include real temporary event→sprite→DDS→GUI fixtures
for oversized textures, news/country misuse, missing controls/bindings, actual
scale/sibling-bound mutations and invalid frame dimensions. Review PNG compression
variation is accepted only with exact dimensions/RGBA; changed pixels fail.
No shared GUI, force history, strategic owner or source capture is replaced.
