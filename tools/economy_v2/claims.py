"""First-controller monthly allocation; forecasts never claim state output.

The authorized settlement freezes a state receipt for its first controller's
existing numeric country ID and boundary date. Later same-boundary controllers
cannot collect that same state's output/tax base again. This is a whole-period
allocation rule, not proration or an attempt to reverse an already paid bill.
Native country-ID/save stability and scheduling/performance remain test gates.
Primary country-ID syntax: engine://common/decisions/CZE.txt,
CZE_skoda_select_country complete_effect/FROM stores THIS.id in a variable.
"""


def allocate():
    return '''# Private settlement allocation. UI/quote paths never execute this.
set_variable = { ac_macro_settled_real_gdp = 0 }
set_variable = { ac_macro_settled_tax_base = 0 }
every_controlled_state = {
 if = { limit = { has_variable = ac_macro_real_output }
  if = { limit = { OR = { NOT = { has_variable = ac_macro_claim_date } check_variable = { ac_macro_claim_date < date } } }
   set_variable = { ac_macro_claim_date = date }
   set_variable = { ac_macro_claim_receiver = PREV.id }
   set_variable = { ac_macro_claim_output = ac_macro_real_output }
   set_temp_variable = { ac_macro_claim_factor = 1 }
   subtract_from_temp_variable = { ac_macro_claim_factor = ac_macro_disruption }
   multiply_variable = { ac_macro_claim_output = ac_macro_claim_factor }
   set_variable = { ac_macro_claim_tax_base = ac_macro_claim_output }
   if = { limit = { NOT = { is_owned_by = PREV } } multiply_variable = { ac_macro_claim_tax_base = 0.35 } }
  }
  if = { limit = { check_variable = { ac_macro_claim_date = date } check_variable = { var = ac_macro_claim_receiver value = PREV.id compare = equals } }
   add_to_variable = { PREV.ac_macro_settled_real_gdp = ac_macro_claim_output }
   add_to_variable = { PREV.ac_macro_settled_tax_base = ac_macro_claim_tax_base }
  }
 }
}
# Temporarily quote this period's allocated bases; the final public quote below
# restores current physical-controller forecasts after the payment is complete.
set_variable = { ac_macro_real_gdp = ac_macro_settled_real_gdp }
set_variable = { ac_macro_nominal_gdp = ac_macro_settled_real_gdp }
multiply_variable = { ac_macro_nominal_gdp = ac_macro_price_multiplier }
set_variable = { ac_macro_tax_base = ac_macro_settled_tax_base }
multiply_variable = { ac_macro_tax_base = ac_macro_price_multiplier }
'''
