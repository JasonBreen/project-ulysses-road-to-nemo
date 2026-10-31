# World capital ownership — Package 1 foundation slice

Fourteen active country histories inherited a capital assigned to a foreign
state. This package replaces those assignments using the geographic fallback
approved for the overhaul. All 62 landowning histories now point to owned states.
The other 48 owned-capital assignments, seven dormant histories and the unresolved
PLH/state171 placeholder are preserved.

These are **provisional gameplay capital districts**, not newly sourced canonical
cities. The exact selection and every candidate distance are committed in
`tools/world_capitals/placements.json`. Existing state names are retained here;
the regional-label owner may give unresolved localities their separately
documented provisional labels. No inferred city identity is introduced.

| Tag | Country | Previous foreign capital state | New owned capital district | Representative owned province |
| --- | --- | ---: | ---: | ---: |
| AEM | Aemurraq | 1 | 451 | 5764 |
| AZB | Azbekerania | 1 | 452 | 814 |
| CRS | Corscae | 1 | 62 | 1718 |
| ECH | Echinata | 1 | 574 | 9467 |
| ESN | Silvonia | 1 | 227 | 3218 |
| GLA | Glaceland | 1 | 50 | 3811 |
| KLG | Kaluga | 1 | 23 | 5047 |
| MAY | Malynea | 224 | 341 | 4010 |
| RMN | Romny | 1 | 85 | 1467 |
| SET | Seterano | 1 | 362 | 1966 |
| SFA | Sfaenland | 1 | 497 | 5342 |
| SOA | Sotoa | 1 | 511 | 9194 |
| VER | Verusa | 481 | 61 | 2666 |
| WEL | Wellow | 1 | 247 | 3960 |

The representative province documents the selection; this package does not
change a victory point or pretend the engine has accepted a new map-object
placement. Country history changes only its root `capital` value. Parties,
characters, ideas, technologies, starting OOBs, dated history and foreign-owned
generator sections are preserved. There are no startup effects, old-save grants,
ownership/core/manpower edits, new tags, raster changes or strategic-region edits.

The verified implementation base is `3810d1abeb9749a265b7b48e8d9eccddf08b1be2`.
Inputs come from the inherited mod country/state histories, definition table,
province raster and impassable adjacency records. No official source maps these
fourteen capital locations; the approved fallback is their explicit source layer.
Connectivity uses actual shared pixel edges with impassable connections removed.
Landmass size uses pixel area rather than province count; state centroids use
only the state's land on the selected component. Lowest state ID resolves an
equal-distance tie. Selection uses exact rational arithmetic over integer raster
coordinate moments; diagnostic centroids/distances are recorded to six decimals.
This avoids platform-dependent last-bit floating differences without changing
the raster or treating a near tie as an exact one.

Reproduce with Python3.12, Pillow11.3.0 and numpy2.2.6:

```powershell
python -B tools/world_capitals/build.py
python -B tools/world_capitals/build.py --check
python -B tools/Test-WorldCapitals.py
```

The nine focused regressions check all69 dispositions, ownership for all62
landowning histories, raster-derived reproducibility, area versus province-count
selection, state-centre tie rules, foreign section preservation and the narrowly
bounded generated output. Existing foundation/economy packages can add their
history sections without changing the capital repair. The new workflow repeats
the mapping and ownership checks in CI.

This is an owned-capital repair, not a certificate of world playability. Starting
industry, logistics, rosters and AI still require the other foundation slices.
Native capital placement, supply behavior and old-save behavior remain pending
the separately authorized native acceptance round. Native testing is paused;
no game, normal installation, profile, save or display setting was changed.
