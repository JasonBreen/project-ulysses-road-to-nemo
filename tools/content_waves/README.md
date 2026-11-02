# Content waves A and D

Generator for Wave A (Free Erusea and the oversight years, Erusea 36 and Central
Usea 24 focuses) and Wave D (Nordennavic's northern reserve, 42 focuses). The
source ledger and runtime contract are in
[docs/CONTENT_WAVES_A_D.md](../../docs/CONTENT_WAVES_A_D.md).

| File | Role |
| --- | --- |
| `framework.py` | Six-node branch compiler: focuses, policies, funded services, narrative, defined texts, weekly and interruption hooks |
| `free_erusea.py` | Wave A branches and the tagless Free Erusea owner (`ac_fe`) |
| `nordennavic.py` | Wave D branches, tree adoption and the read-only Anean callback |
| `build.py` | Writes script, localization, the NEC tree and the ERU/FCU import blocks; writes `manifest.json` |
| `build_art.py` | Writes DDS textures, `interface/ac_content_waves.gfx`, `assets.json`, event masters and galleries |
| `test_waves.py` | Source checks and actual-script offline runtime tests |

```text
python -B tools/content_waves/build.py           # regenerate script and localization
python -B tools/content_waves/build_art.py       # regenerate artwork (Pillow 11.3.0)
python -B tools/content_waves/build.py --check   # read-only
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/test_waves.py
```

Edit the content modules, then regenerate both outputs and commit them together.
`tools/build_continental_war.py` preserves the `# BEGIN OVERSIGHT YEARS IMPORTS`
block in `ERU.txt` and `FCU.txt`; this generator owns that block's contents.
All values are provisional gameplay; only the dates noted in the ledger are
official anchors.
