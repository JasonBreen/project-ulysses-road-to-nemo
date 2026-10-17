# Economy source and attribution

The economic core is a small, rewritten Millennium Dawn-inspired adaptation for Ulysses. It is not a copied MD installation or a license grant for the inherited Ulysses archive.

## Source examined

- Project: [Millennium Dawn](https://github.com/MillenniumDawn/Millennium-Dawn).
- Local source branch: `pr5306`, exact HEAD `2efae2f406d73346d85cb59f339a4f917c4b6869`.
- The source files below were clean against that HEAD when inspected. The source checkout was not edited, fetched, switched or committed.
- Upstream money-system header credits Angriest Bird, Hiddengearz and Killerrabbit; additional Millennium Dawn contributors retain their rights.
- License supplied by that source checkout: Creative Commons Attribution-ShareAlike 4.0 International. A verbatim copy is retained as [licenses/MD-CC-BY-SA-4.0.txt](licenses/MD-CC-BY-SA-4.0.txt).

| Source path at the pinned revision | Role in this adaptation |
| --- | --- |
| `common/scripted_effects/00_money_system.txt` | Budget quote vs settlement distinction; treasury, tax, spending and interest concepts |
| `common/scripted_effects/00_economic_system_utilities.txt` | Cash-shortfall borrowing, capped repayment and AI operating reserves |
| `common/on_actions/MD_on_actions.txt` | Weekly country-scope fiscal settlement and repayment order |
| `common/scripted_effects/!_market_effects.txt` | Examined procurement pricing dependencies; MD prices/equipment were not imported |
| `common/scripted_triggers/00_debt_ratio_triggers.txt` | Examined GDP-ratio gates; no ratio triggers were imported |
| `common/scripted_guis/00_MD_economyview_scripted_guis.txt` | Examined display/click dependencies; no MD GUI or sprites were imported |

SHA-256 of the principal inspected source bytes:

```text
LICENSE                                     23EE78C8BAE49CF08EA2F0C84945C66B987EBE4520881FB51B3DAD4FB43D07C2
00_money_system.txt                         4F33AA24881C34E567A42CA13883C5E5804F6D6192EC131944BE7389D7CAB068
00_economic_system_utilities.txt            892145C7CBAECEA6C5D1EA59F18FAB0C887DC2376E7CF949FD96D8EE5182C604
!_market_effects.txt                         F1FCB3EA0298B710D0F5361CA3009D6AA488B52F0CBA9094F36CE422076AF806
MD_on_actions.txt                           972D5436575E74CAC41A9E3DE804FD2C6E86FB640E0AC6EE0A6E9B68D77B568A
```

## What changed

The Ulysses implementation replaces MD's GDP and population seeds, productivity/employment model, custom buildings/resources, tax/spending laws, international investment returns, currencies, IMF/EU/UN hooks, array setup and large GUI graph with abstract factory-based capacity, a country-scope weekly ledger, bounded loans, unpaid bills, guarded decisions and one prepaid domestic contract. New identifiers are namespaced. No Earth-country history, Earth-country economic calibration, MD map, MD art, vanilla game assets or aircraft designs were copied.

MD's calendar and country assumptions are not suitable substitutes for Strangereal evidence. The factory coefficients, FU, rates, policy effects, credit limit, order price and production delay are new provisional gameplay calibration. They are not Project Aces lore, and no future canon through 2065 is inferred.

## Scoped license notice

For clarity, the following newly authored economy adaptation files and supporting economy documentation/tooling are offered under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- `mod/2985041246/common/{game_rules,scripted_triggers,scripted_effects,dynamic_modifiers,on_actions,decisions}/ac_economy*.txt`;
- `mod/2985041246/common/decisions/categories/ac_economy_categories.txt`;
- `mod/2985041246/localisation/english/ac_economy_l_english.yml`;
- `tools/economy_script.py`, `tools/test_economy.py`, `tools/Test-UlyssesEconomy.ps1`;
- `docs/ECONOMY.md`, `docs/ECONOMY_VALIDATION.md` and this provenance notice.

Retain source/creator credit, the license link/text, and the modification notice when sharing the adaptation. Share adapted material under the same or a compatible license and do not add restrictions that negate the licensed freedoms. These conditions follow the [Creative Commons deed](https://creativecommons.org/licenses/by-sa/4.0/) and accompanying legal code; private repository visibility does not change the license terms or grant rights to unrelated content. There is no MD or Project Aces endorsement.

This scoped notice does not relicense inherited Ulysses files, Project Aces names/art, third-party assets or Paradox material. Their provenance and rights remain separate. The preserved archive's distribution rights are not established by MD's license. This task authorizes private branch publication only; it does not authorize public distribution.

Engine-shape checks used the source checkout's `resources/documentation` references for country dynamic values, variable effects, game-rule checks, modifiers and stockpile effects. Those documentation files were read, not copied. Native 1.19 validation remains a separate acceptance gate.
