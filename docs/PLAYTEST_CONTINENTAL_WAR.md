# Playtesting the Usean Continental War

This guide covers the `ac_ucw` arc: the Ulysses fallout (2000–2003), the Usean Continental War (2003–2005), and the Erusea and Central Usea/ISAF focus trees. Sources and provenance are listed in [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md). Native results are recorded separately under issue #8. Nothing below has been confirmed in a native run yet.

## Setup

1. Pull merged `main` into the play install. The C: clone is `Documents/Paradox Interactive/Hearts of Iron IV/mod/project-ulysses-road-to-nemo`.
2. On the game-rules screen, set **Project Ulysses experiments → Playtest shortcuts** to **Enabled**. It is off by default, and with it off no shortcut decisions are shown.
3. Start the 1991 campaign as Erusea (ERU) or Central Usea (FCU). Launch with `-debug` if you want console access.

## Shortcut routes

The **Playtest shortcuts** decision category runs the same scripted effects as the natural route, so flags and ideas match a normal playthrough. Every shortcut is free and repeatable while its condition holds.

| Route | Shortcut decisions, in order | What to check |
| --- | --- | --- |
| Fallout | Open the Usean calendar | Erusea and FCU switch to their new trees; the opening brief `ac_ucw.1` fires; the "After Ulysses: Usea" category appears |
| Early war | Open the calendar → Push Erusea to the brink → Start the Continental War | Erusea is at war with SNS and every FCU treaty member; news `ac_ucw.20` fires; the war category replaces the fallout category |
| Stonehenge | … → Erusea seizes Stonehenge | Erusea gets Stonehenge Railguns and FCU gets Under Stonehenge's Guns; news `ac_ucw.40` fires |
| ISAF | … → Form ISAF | The faction is renamed Independent State Allied Forces; FCU declares on Erusea if it was not already at war; North Point gets the invitation `ac_ucw.32` |
| Stages | … → Advance the war one stage, four times | Los Canas, North Point HQ, landing, then Stonehenge destroyed; each news event fires exactly once and FCU's ideas swap at each stage |
| ISAF victory | … → Force ISAF victory | Farbanti news; Megalith `ac_ucw.60` reaches FCU after 7 days and `ac_ucw.61` 14 days later; Erusea gets Provisional Autonomous Government; the 2005 assessment follows |
| Erusean victory | … → Force Erusean victory | News `ac_ucw.51`; assessment; Erusea's Victor's Order focus becomes available |
| Armistice | … → Force an armistice | Erusea makes white peace with every allied participant; news `ac_ucw.52`; assessment |
| State | Report the war state, at any time | `ac_ucw.99` shows the stage, outcome, Erusean grievance and FCU stage weeks |

## Natural routes (shortcuts off)

| Route | How | Expected |
| --- | --- | --- |
| Canonical AI war | Observe from 1999 with both sides AI | The calendar starts after 30 Nov 1999; the border closure lands on 21 Apr 2000; the AI war starts from 21 Jun 2003 if grievance is above 24; ISAF forms after 21 Aug 2003; AI stage fallbacks follow 3, 52, 18 and 10 weeks after each previous stage |
| Escalation | Play Erusea: Close the Border → The Nation's Grievance → … → Plan for San Salvacion, then take Invade San Salvacion | Invasion available from 2002 with the plan and grievance at 70 or more |
| De-escalation | Play Erusea: quotas or dialogue → Refugee Accord → Reconstruction Bonds → Usean Arms Talks → A Continental Accord | The war is averted (`ac_ucw_war_averted`); the AI never starts it; the assessment arrives after 2004 |
| Human ISAF | Play FCU through the war | Stage decisions open at 1, 26, 9 and 4 weeks; armistice offers open after Los Canas |
| Ground recapture | Retake state 310 after Erusea seizes it | Stonehenge is destroyed without the strike decision |

## Console cheat sheet

| Command | Use here |
| --- | --- |
| `tag ERU` / `tag FCU` / `tag NPT` | Switch country |
| `observe` | AI-only run |
| `event ac_ucw.30 FCU` | Fire the ISAF founding directly |
| `focus.autocomplete` | Complete focuses instantly |
| `pp 500` | Afford decisions |
| `list_flags` | Check `ac_ucw_*` flags (global and country) |
| `get_var ac_ucw_grievance` / `list_vars` | Read the indices while playing Erusea; `ac_ucw_stage_weeks` while playing FCU |
| `set_var ac_ucw_grievance 80` | Push the escalation threshold |

## Native checklist (not yet run)

- [ ] The game rule appears and defaults to Disabled
- [ ] The Erusea and FCU trees load without errors and render with mod art only
- [ ] All 38 events open with their long-form text, pictures and options
- [ ] The AI war starts and FCU's faction joins in defence
- [ ] The ISAF rename shows in the diplomacy view
- [ ] Each stage and news event fires once; no duplicates after save/load
- [ ] Every outcome reaches the 2005 assessment
- [ ] `error.log` has no new `ac_ucw` errors
