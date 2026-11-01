# CI Python selection and read-only validation

The original publication failed its final PowerShell static step on Windows:
the wrapper preferred `py` over the workflow's selected `python`. The launcher
chose Python3.15.1 without Pillow even though setup-python's Python3.12.10 had
the pinned dependencies. Both runs remain identifiable:
[41286097930](https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41286097930)
and [41286057913](https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41286057913).
The failed output is retained in [ci-failure.txt](ci-failure.txt).

`Test-UlyssesStatic.ps1` now resolves the first application named `python` from
the active PATH, falling back to the Windows launcher only when no Python
application is available. It logs the actual executable. This honors an activated
virtual environment and GitHub's setup-python environment without installing or
changing any system software.

The first local probe exposed multiple PATH applications returning an array of
paths; that failure is retained in [the initial probe](ci-python-selection/results.json).
After selecting one application, the static checks passed, but the exact-source
fence correctly rejected a rewritten tracked `.pyc` file. That attempted run
has only its [static log](ci-python-selection-fixed/static.txt), not a passing
final receipt. Only that generated cache was restored. The wrapper now disables
bytecode writes for its Python subprocesses and restores the prior process
environment setting in `finally`; no original cache was deleted or recaptured.

The final end-to-end probe **passes** at
`7089727bd3630453f052cd6d0784c69f307ba089`. An ignored scratch directory places
a deliberately failing `py.cmd` in PATH while the selected Python3.12/Pillow11.3
environment is active. Full installed-reference/immutable-baseline static
validation passes, the wrong-launcher marker is absent, and all **8,733** raw
source inputs remain unchanged before/after. Fingerprint:
`14a12547d8354089856d79bc70f32390a01cd25db9454340cc6c503a950df169`.
See [the final results](ci-python-selection-final/results.json) and
[exact-source receipt](ci-python-selection-final/source-receipt.json).

These changes affect validation tooling only. The original fourteen bounded
event-fit checks retain their source identities, and the mod payload remains
`82e2745942177cfe35f3732fcce47d5bc6a0285bba2bfead5d967a1af669acae`.
Native testing remains paused; no game, profile, display, installation or save
was changed. Final-head remote CI is reported separately on PR54.
