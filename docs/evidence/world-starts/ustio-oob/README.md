# Existing Ustio event-roster delimiter repair

`ustio_na.3` already loads `UST_band_of_broders_units`. The inherited OOB ended
inside its `units` block. This repair adds the missing closing brace and retains
the compatibility filename, seven-infantry template and single veteran formation
at province 2930, with both equipment and experience factors equal to one.

`before-after.json` demonstrates the failure in the actual recorded Git source,
the successful repaired parse and exact normalized-prefix preservation. The
existing native-compatibility source gate now checks the real event/OOB binding
and retained payload, alongside its 1,120 selected startup cases. Its successful
log is `compatibility.txt`. These are source checks, not native loading or unit
delivery observations.

A separate inherited reference, `UST_moblise_militia_focus_oob`, still has no
authored file in the working source or preserved archive. Its civil-war parent
is explicitly unavailable. Shared descendants can import through their parent,
so absence of a direct import is not treated as proof that the reference is
unreachable. This later branch needs its own reviewed, costed content contract;
no roster or free units are invented to silence that gap. It is outside the 1991
starting-roster acceptance and remains visible for Ustio branch-cohesion work.
