# National economy v2 — source implementation and acceptance contract

The full economy is the default for new 1991 campaigns. It adds real and nominal
output, prices, three tax lanes, five category budgets, public credit and arrears,
force operating obligations, sustained readiness and recoverable fiscal crises.
Native factories, construction queues, equipment, fuel, supply and units remain
the physical simulation. GDP never creates offsite factories or duplicate goods.

**Status: implemented source and offline checks; native acceptance pending.**
No game, profile, user save, normal installation or display setting was changed.
The existing native-testing pause remains in force. No rendered GUI, native
arithmetic, real-save serialization, native AI pace or balance acceptance is
claimed for this package.

## Units, sources and starting data

Amounts are billions of abstract fiscal units. They are not dollars or a newly
invented canonical currency. Real annual output uses constant 1991 prices; the
price index begins at 100. Nominal annual GDP is real GDP times that index / 100.
Monthly operating flows use annual bases / 12. Growth and inflation are
annualized simple rates applied monthly / 1200, not exact annual compounding.

`tools/economy_v2/profiles.json` contains all 69 country profiles and allocations
to the inherited 612 states. The numbers are fictional gameplay calibration
within the approved design, not official national accounts or a territorial claim.
Selected major/actor GDPs use explicit profiles; the remaining seed estimates
use inherited population and industry as proxies. Population/industry-weighted
state allocations preserve each profile's starting total, subject to recorded
six-decimal rounding. No owner, core, border, population or map file is changed;
state 171 and placeholder regional geography remain unresolved.

The installed TNO/TFR files were examined as capability references only. No code,
country calibration, art, institutions or production-unit system was copied.
The existing experimental economy is an MD-inspired adaptation; its scoped
credit and CC-BY-SA notice in `ECONOMY_PROVENANCE.md` remain applicable to that
retained code and its compatibility modifications. The original v2 owner and
procedural artwork are separately identified by their source files.

## Policy and simulation

| Item | Authored rule |
| --- | --- |
| Income / business / consumption tax | Household 55%, business-surplus 25%, consumption 65% of nominal taxable output, respectively; these bases deliberately overlap in different tax incidence. Collection efficiency applies once. |
| Initial tax rates | 20% / 20% / 5%; lane controls move by two percentage points; caps 40% / 35% / 15%. |
| Tax presets | Low 16/16/4%; standard 20/20/5%; high 26/24/8%. |
| Budget categories | Administration 1.5%, services 5%, education/research 3%, development 2%, defense 3% of annual nominal output at standard targets. |
| Category levels | Low / standard / expanded: 75% / 100% / 125% of the category's standard envelope. Each category is independently adjustable. |
| Budget presets | Balanced, development, emergency relief, mobilization, and stabilization. Each changes the actual five targets, rather than merely its label. |
| Policy timing | A shared 30-day cooldown; forecasts change immediately, settlement and investment benefits do not. |
| Administration | Delivered funding and target level affect collection; efficiency is bounded 10–98%. |
| Services | Delivered funding affects stability. |
| Education | Delivered funding affects research and contributes to delayed productivity. |
| Development | Delivered funding affects construction, lagged growth and economic-disruption recovery. Native queues still build actual capacity. |
| Defense | Actual deployed-force obligations are a floor beneath the chosen envelope; the target affects readiness recovery. Existing forces cannot be made free by lowering a slider. |
| Borrowing | A tranche is 0.5% of GDP, minimum 0.001 billion. Aggregate domestic principal is retained; outstanding debt is never erased when the credit ceiling falls. |
| Credit | Ceiling of one year's current nominal GDP; no additional voluntary debt or policy spending with arrears. Automatic settlement financing is limited to available credit. |
| Interest | Annual variable sovereign rate starts at 4%, with pressure premiums above debt/GDP thresholds and during arrears. The monetary stance can move between 2% and 8%. No bond-lot or exchange-rate simulation is asserted. |
| Crisis | Two consecutive monthly funding ratios below 90% begin a three-settlement correction warning. Further underfunding after that window activates a fiscal crisis. Three funded settlements with arrears declining or already zero end it; remaining financial obligations are preserved. Government, ideology and territory are never changed by this generic owner. |

Real growth responds to investment with a lag, high-tax drag, underfunding, war,
crisis and changes in actual factory capacity. The capacity contribution is
bounded and lasts for the relevant monthly change; economic growth does not
grant another factory. Growth is bounded −20% to +10% annually. Inflation
gradually returns toward its baseline, with supply-disruption/war pressure and
monetary stance effects, bounded −5% to +25%. Borrowing does not directly mint
output or automatically create inflation. These are gameplay rules to calibrate
in native tests, not claims of a real-world macroeconomic model.

All domestic-interest, mobilization-law and national-spirit identities remain.
Their existing physical production effects coexist with v2's delivered-service
modifiers. Native balance must examine that stacking; this package does not
claim the entire total conversion or every inherited law has been redesigned.

## Monthly owner and conservation

The new owner settles on `on_monthly`. Its callback authorizes the private
settlement effect; a persisted last-settlement date rejects a repeated callback
on the same date, including a reloaded state. Startup initializes/quotes only.
Legacy weekly callbacks dispatch only to the saved experimental model. No UI,
focus, story event or refresh invokes settlement.

`ac_macro_warning_months_left` is the settled correction deadline, counting
3→2→1→0 after the warning begins. `ac_macro_warning_months` records elapsed
correction settlements. Repeated callbacks and quotes cannot advance either
clock. A funded month with unchanged outstanding arrears does not advance the
three-month recovery record; improvement must be sustained. Ending the active
crisis does not forgive remaining debt or arrears.

The first scheduled accounting boundary is February 1991. Newly released or
identity-reset accounts settle at the next monthly callback, including the
callback that first discovers the account. Opening such an account during
startup/reload creates no settlement and cannot postpone that first boundary.
There is no historical catch-up or first-month proration.

The monthly sequence snapshots physical conditions, quotes obligations, receives
revenue, finances a shortfall within credit, funds available obligations, records
arrears, pays old arrears from surplus, and updates real conditions/readiness,
crisis state, replacement programmes and AI priorities. Forecasts are recomputed
afterwards; last-settled values remain distinct.

Without external transactions or consumed replacement escrow:

`Δ(cash + escrow − debt − arrears) = settled revenue − billed obligations`.

Borrow/repay conserve this position. Unpaid obligations become arrears instead
of disappearing. Paying those arrears reduces cash and arrears equally. Escrow
reservation/refund conserves the position; programme completion consumes it once.

Prices, state output and variables remain conservatively scaled. The actual
engine range, rounding and minimum meaningful payment are **open native gates**.
Decimal offline conservation is not proof of HOI4 arithmetic. An approved native
probe must cover the largest 2020 economy, smallest country's payment, long-run
prices, negative growth and rounding/remainder behavior before release acceptance.

## Physical economy, occupation and releases

Persistent real productive value belongs to a state. Its controller aggregates
realized output; a foreign controller collects only 35% of the occupied state's
normal tax base. The previous owner receives no tax from territory it does not
control. State output is counted once. Ownership/control changes do not transfer
cash, erase debt, grant stockpiles or clone factories. Disruption is bounded
0–75% and recovers only through delivered development funding.

Real deployed personnel, aircraft and hull counts determine force operating
burdens. Carrier/submarine premiums supplement a base hull cost, avoiding
overlapping capital/screen/carrier classifications. War multiplies operating
costs. These costs fund personnel/maintenance/support; native supply, fuel,
attrition and equipment replacement retain their own physical behavior.

Replacement funding reserves 0.005 billion and observes 100 additional infantry
equipment produced by the native queue. Until that production exists it cannot
complete. It reserves no individual production line, and grants no equipment.
The programme consumes escrow once and supports readiness. Cancellation refunds
remaining escrow once. Existing experimental four-pulse prepaid contracts retain
their original delivery and refund behavior, without a balance conversion.

Only fresh history-marked accounts at the original 1991 opening receive starting
treasury and debt. A country with no owned land is not initialized or seeded.
Later releases initialize from currently inherited state output without historical
cash/debt grants. Civil-war clones cannot copy an original country's account:
identity-bound readiness detects the new engine country ID and discards copied
financial identity before initializing an unseeded account. The exact native
inheritance paths remain a required test.

## Public integration API

| API | Contract |
| --- | --- |
| `ac_macro_ready` | Full mode, initialized identity, and owned land. |
| `ac_econ_ready` | Compatibility readiness: full or saved experimental mode. Disabled mode stays inactive. |
| `ac_macro_quote` / `ac_econ_refresh_budget` | Recompute forecasts and display aliases; never settle money, advance production, or replay starting grants. |
| `ac_macro_try_spend` | Positive temp `ac_macro_transaction_amount`, in billions; rechecks cash/arrears/readiness. Clears then sets `ac_macro_transaction_succeeded` on successful payment. Consumer gates its reward and once-only flag on success. |
| `ac_macro_receive` | Receives a positive temp amount. The originating deal/event owns its once-only and partner checks; this effect is not a bilateral-money-creation system. |
| `ac_macro_change_commitment` | Adds signed temp `ac_macro_commitment_delta` to annual commitments. Consumer records the exact applied amount and owns once-only addition/removal. |
| `ac_macro_apply_disruption` | Bounded positive temp `ac_macro_disruption_delta`, applied to currently controlled state economies; caller owns historical/once-only eligibility. |
| `ac_econ_can_pay_programme` / `ac_econ_pay_programme` | Existing faction programme uses a new prospective 0.002-billion price in full mode, retains exactly 2 FU in experimental mode, and touches no cash when disabled. This is not a conversion rate for legacy balances. |

All established public `ac_econ_` names remain as dispatchers. Experimental
internals use `ac_econ_legacy_` names with unchanged original variables and flags.
Existing disabled/experimental rule values remain valid. The `full` default is
new-campaign policy; an old save without the new history marker is not reseeded
or silently converted. There is no automatic catch-up for expired history.

Existing Anea/Usean preparation and recovery indices remain with their campaign
owners. Their PP and temporary industrial costs are not automatically added as
new fiscal commitments. Additional country/political costs must be explicit,
guarded and once-only; scale them to output rather than imposing a flat billion
on every country. No new border, tag, leader or historical outcome is authored.

## UI, verification and release gates

The current full-mode HUD opens five direct-control pages: Economy, Budget, Finance,
Industry and Forces. Direct visibility rules prevent the prior nested-page
overlap defect. The 860×640 window uses original navy/cyan RGBA DDS geometry and
the existing authored ACBriefing fonts. It retains Escape/close and dragging.
The saved experimental mode retains its three-page directorate and its actual
transaction owners. Full-mode source bounds and frame hashes are checked
offline; actual rendering/input remains untested.

This page arrangement is an implementation gap against the accepted Overview,
Budget, Industry and readiness, Debt and contracts, and Ledger structure. A
rolling settled-history ledger and its graphs are not implemented in this
integration candidate; their follow-up remains required before claiming the
approved economy interface complete.

Reproduce and check from repository root:

```powershell
python -B tools/economy_v2/build.py
python -B tools/economy_v2/build.py --check
python -B tools/usea_expansion/build_dashboard.py --check
python -B tools/Test-EconomyV2.py
python -B -m unittest discover -s tools -p test_economy.py
python -B tools/Test-UlyssesFactions.py
```

The macro suite executes shipped scripts and covers conservation, monthly
authorization, reload copies, disabled/legacy accounts, clone/release identity,
tax/category controls, presets, crises, output transfer, observed production and
all-country AI budgets through 2020. The legacy harness deliberately reports
full-mode branches as foreign/inactive; the independent macro interpreter covers
them against the actual new owners. Neither harness is Paradox's engine.
The long-run inputs are synthetic force/war observations; they do not load the
native OOBs or establish that a naturally played war is affordable or balanced.
`tools/economy_v2/run_checks.py` retains commands, exit status and logs under
`docs/evidence/economy-v2`. Add `--core --engine <installed-reference>` for the
full static wrapper; after Package 0 integration the same engine option also
runs its loose-file dependency gate for the macro screen.

Native release acceptance still requires fresh games at all three requested
display configurations, every page/action, saved legacy accounts, pending
contracts, real save/reload around settlement, releases/civil wars/occupation,
numeric precision, AI war budgets, disaster recovery and natural campaign pace.
International lending, exchange rates, bond markets, per-airframe maintenance,
sector input-output matrices and a custom global resource market are deferred.
