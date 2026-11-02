# LAND integration with reviewed parent repairs

The original LAND component and its fourteen successful check groups remain
recorded at `d0c45f0704dda6f4bf97de32fd4d2c9b7d61ce9b`, based on `224c9ccb`.
The integration parent additionally contains the reviewed world-start and
presentation fixes, the retired world-news compatibility handlers, and the
existing Ustio event-roster delimiter repair `9e4016c5`.

The original 1,050 protected source hashes are retained unchanged. Exactly one
reviewed repair is recorded alongside them: the Ustio OOB receives a newline and
its missing final closing brace. The strengthened preservation test requires
the exact new hash, removes those exact three appended bytes, requires the
original hash, demonstrates the old unclosed-block failure and checks the
parent's independent before/after receipt. No other protected file is exempted
and no broad recapture was performed.

All 22 focused LAND tests pass again with the read-only installed reference.
`focused.txt` records that result. `attempts/` retains an initial invocation with
the wrong CLI option and the first preservation assertion's incorrect assumption
that the original file ended with a newline. The corrected assertion uses the
actual preserved EOF bytes; the country/unit payload was not changed to fit it.

These are source/primary-metadata results. Native designers, AI field selection,
production delivery, operating costs, rendering and save/reload remain untested
while native testing is paused.
