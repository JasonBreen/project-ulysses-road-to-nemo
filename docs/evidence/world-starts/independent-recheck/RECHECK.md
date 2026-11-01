# Independent correction recheck

Exact detached checkpoint: **c87312f5bb6cb2bfeebcaadedb5753c87463a221**.
This is a narrow source-only recheck of the earlier three findings, fourteen
railway overlaps and Ustio's explicit inherited liability. The earlier review
directory remains unchanged. No authored export, active country worktree,
installation or native application was changed.

The prior three source-accounting defects are addressed at this checkpoint:

1. **Personnel:** CSO preserves three formations with four infantry battalions
   each. The actual force requires 13,380 personnel against a 15,000 nominal core
   pool, with a 1,338 replacement reserve and **282 remaining**. MST now requires
   46,480 with 8,872 remaining after reserve; SLA requires 8,840 with 5,276
   remaining. These are source budgets, not observed native mobilization.
2. **Non-core capacity:** YUK adds no industry or resources in states 515/555,
   preserving their KLG cores. All 45 requested military factories have core
   backing. DOR preserves the three inherited military factories and FRU core
   in state 487 without adding industry/resources there. Its raw military total
   is now 13; the conservative core total and production plan are both 10.
   Non-core output is excluded rather than assuming compliance or rounding.
3. **Ferustia:** The worksheet now reads its actual Free Trade, Low Economic
   Mobilisation, Limited Conscription and retained spirits, including the
   negative resource modifier. It exposes industrial aluminium 4 / steel 6
   import deficits. Rounded separately at the captured trade terms, those
   require two civilian factories, matching the conservative two-factory
   allowance after consumer goods. The industrial import-CIV margin is zero.
   The source expressly leaves eligibility, supplier availability and delivery
   unguaranteed. Full-tempo fuel is an additional constraint; this is not a
   claim that every force can operate continuously at full tempo.

The original railway prefix hash remains exact. None of the earlier fourteen
level-3/4 edges is redeclared in the appended rows; the new source therefore no
longer relies on uncertain duplicate-edge precedence for those cases.

**UST remains an open source liability.** It retains 48,600 deployed personnel
against a conservative 17,617 pool, with a 4,860 replacement reserve and a
35,843 shortfall. `personnel.json` calls this `inherited_reinforcement_debt`,
keeps `universal_sustainable_start_acceptance = false`, and lists UST as a known
source liability. The registry exposes the
`inherited_personnel_reinforcement_debt` gap and uses
`authored_foundation_with_inherited_policy_debt_native_pending`, rather than
silently reporting a clean global start. Existing conditional reform routes are
documented; their natural pacing and reachability remain unaccepted. No force,
population, manpower or law grant was introduced to hide that inherited debt.

The installed-primary WorldStarts suite passes **24/24**, including primary
recapture, source-hash variation checks, negative OOB/law mutations, core-only
capacity, actual policies, preserved armies and railway-level regressions.
Independent read-only assertions checked the concrete values above against the
actual manifests/worksheets and the earlier fourteen recorded railway edges.
`results.json` retains the exact input hashes and outcomes.

No new blocker was found within this bounded recheck. This does not grant
universal sustainable-start or native acceptance: the documented inherited UST
liability, later legacy-owner integration, trade delivery and native parsing,
mobilization, fuel, supply, AI pacing and save/reload checks remain separate.
