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

`UST_moblise_militia_focus_oob` was absent from the working source and the
preserved archive when this delimiter repair was recorded. Its civil-war parent
is explicitly unavailable (`available = { always = no }` on `UST_civil_war`);
the civil-war event force-completes that parent. Shared descendants can import
through their parent, so absence of a direct import is not proof that the
reference is unreachable. The later branch now has its own provisional roster,
labelled in [CANON_LEDGER.md](../../../CANON_LEDGER.md). That roster is outside
the 1991 starting-roster acceptance: country history still does not load it, and
this delimiter repair did not invent those units.
