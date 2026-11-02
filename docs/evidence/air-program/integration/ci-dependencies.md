# Standalone aviation CI dependency

The first standalone Linux aviation job passed all 32 aviation cases, LAND,
fonts, binary-filter checks and the primary capability audit, then failed
before executing the 61-start coverage gate: `foundation_map` imports NumPy but
this new workflow installed only Pillow. The main Windows workflow already
installs both dependencies, matching the local CI-parity environment.

The standalone workflow now installs the same pinned `numpy==2.2.6` alongside
`Pillow==11.3.0`. The coverage gate remains present. No production script, map,
asset, test assertion or local environment was changed to hide the failure.
The original failed run remains available:
<https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41274527288>.

The existing local exact-source phases used both pinned dependencies and passed
coverage. Exact-head remote CI must still be verified after pushing this fix.
