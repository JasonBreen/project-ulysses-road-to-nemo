"""Twenty-four national choice events, distinct from the global squadron stories."""
from content import COUNTRIES
from usean_partner_builder import block, guard, loc, EVENTS

NARRATIVES = {
"SNS": [
    ("The Telephone That Everyone Calls",
     "A district operator has pinned three unofficial numbers beside the official switchboard. They reach the people who can find a water crew, open a shelter or explain why a receiving office is shut. None appears in the national register. Publishing the contact list would make a fragile local arrangement into a public service; keeping it within the rota would leave operators freer to improvise. The choice is who can demand an answer when a familiar voice is no longer there.",
     "Publish an accountable contact list and fund its upkeep.", "Keep a restricted operational rota."),
    ("The Key in the Wrong Office",
     "An inspection has found a sound shelter whose key is held by an office that closes before the evening protection rota begins. Everyone involved followed a written instruction. The protection service can fund a joint receiving desk and rebuild institutional capacity, or put dispatchers on an immediate priority footing so the next practical allocation need not wait. Neither course creates more staff; it changes how the existing service uses them.",
     "Fund the receiving desk and restore administrative capacity.", "Give the dispatch service room to authorise the next task."),
    ("A Forecast on Every Noticeboard",
     "The warning has produced notices that disagree in small but important ways. A protection officer asks for practical instruction cards explaining where uncertainty remains. Dispatch staff ask instead for time to revise the movement chain. The first choice strengthens preparation completed before the crisis boundary; the second improves a military and service capability that remains useful afterward. Neither can promise safety simply by printing a confident sentence.",
     "Pay for practical protection instructions before the crisis.", "Concentrate the work on the dispatch chain."),
    ("The Receiving Office Is Full",
     "A neighbouring service asks whether San Salvacion can accept another set of urgent requests. The local receiving desk is already carrying cases that were never assigned a destination. Officials can protect domestic continuity, or prepare a bounded offer to Central Usea with its receiving obligations written in advance. The recipient remains free to refuse. What cannot be offered is capacity that the country has only counted twice.",
     "Protect the domestic receiving programme.", "Prepare the paperwork for one bounded external offer."),
    ("A Desk Returns without Its Files",
     "Recovery has brought an official back to a desk whose surviving files do not match the cases being presented. Some records may be reconstructed; some cannot. An inspected restoration will rebuild local capacity and leave an honest gap in the evidence. A rapid operational restart will give dispatch work precedence and reopen the next review allocation. The service must choose what it can responsibly promise, rather than declare every missing record found.",
     "Fund an inspected restoration of the local record.", "Restart the dispatch work and reopen its next review."),
    ("The Network's Ordinary Year",
     "The national programme now has a record of what survived, what was refused and what had to be done under external conditions. Its conclusion does not decide the war or erase the settlement. The government can renew an ordinary civil service whose future funded completions support recovery, or retain a bounded readiness record at a continuing public cost. Either choice is an ongoing obligation, not a final gift from the calendar.",
     "Renew the ordinary service and its recovery work.", "Retain the readiness record and fund its standing burden."),
],
"AMB": [
    ("Two Owners of the Same Timetable",
     "A workshop's delivery book and a public receiving office both reserve the same morning movement. The workshop insists its slot has been promised for months; the office holds a more recent priority notice. Amber can publish a common record, accepting the public cost of explaining which bargain had to wait, or maintain a restricted operational schedule and concentrate on dispatch capability. The timetable is a development policy before it becomes a relief plan.",
     "Publish the common timetable and account for its costs.", "Keep an operational schedule for the dispatch offices."),
    ("A Guarantee Is Not an Empty Wagon",
     "A contractor has accepted a service guarantee but has no uncommitted crew to attach to it. Cancelling the whole bargain would destroy useful maintenance work; accepting its paper capacity would mislead the board. A funded inspection can restore administrative capacity and identify what remains deliverable. Alternatively the board can open the next practical allocation immediately and accept a narrower operational settlement.",
     "Fund the inspection and repair the service bargain.", "Open the next allocation around the capacity that remains."),
    ("The Reserve in the Fine Print",
     "The international warning has reached suppliers as a new clause in their standing contracts. Some can prepare a genuine civilian reserve if they receive clear instructions before the crisis. Others argue that the existing movement chain must be made more reliable first. The capacity board must choose between a preparation credit earned within the real window and transport coordination that remains useful in later years. It cannot backdate either decision.",
     "Pay for practical civilian reserve instructions.", "Prioritise the existing transport chain."),
    ("A Manifest with No Receiving Signature",
     "The proposed coalition service has a sending manifest and an impressive priority stamp. It still lacks a receiving official willing to accept the work. Amber can direct its development effort toward domestic services, or prepare a defined offer to Central Usea that carries a smaller administrative burden when it is sent. A funded service slot is still required, and a refused offer must return that slot rather than strand it abroad.",
     "Give the domestic development programme priority.", "Prepare one offer with its receiving obligations attached."),
    ("The Contract That Outlived the Emergency",
     "A supplier asks whether its temporary protection from ordinary competition is still in force. The receiving office wants the contract continued until every disputed delivery is settled. An inspected review restores administrative capacity and clarifies the development record. A faster operational settlement reopens the next review allocation and puts transport work first. Keeping both promises would simply reserve the same capacity again.",
     "Inspect the unfinished bargain before renewing it.", "Settle the operational schedule and reopen the review."),
    ("The Price of Standing Capacity",
     "Amber's service ledger now distinguishes spare capacity paid for, domestic movements authorised, offers refused and work actually received. The final review follows the settlement that exists, including any constraints on the country. Ministers can renew ordinary service work with continuing recovery value, or protect a readiness record at an ordinary public cost. Neither course creates another transport fleet or an unlimited claim on suppliers.",
     "Renew ordinary receiving services.", "Keep a funded readiness record."),
],
"UGE": [
    ("Two Keys and One Depot",
     "Two offices hold valid instructions to draw on the same small depot. One expects to support a local receiving service; the other has reserved the space for an emergency movement. Ugellas can publish the custody record and accept its continuing public burden, or keep the working list restricted and strengthen operational coordination. The finite slot limit remains in either case. A better form is not another warehouse.",
     "Publish the custody record and maintain it.", "Keep a restricted operational list."),
    ("The Unavailable Driver",
     "An exercise has found a driver named on three reserve lists. The driver is available, but not to all three offices at once. An inspected roster can rebuild institutional capacity and improve the mobility account. An immediate operational allocation can instead resolve the next practical task without waiting for a further rota. The reserve authority must record which commitment was left unmet.",
     "Fund a verified roster and rebuild capacity.", "Open the next practical allocation."),
    ("Space Reserved before the Warning",
     "The warning has made every unused corner of a depot look like a national reserve. Protection staff want practical instructions that turn some of that space into preparation before the deadline. Dispatchers want to concentrate on the receiving chain and the transport already available. Ugellas can improve one without pretending it has found unlimited storage, drivers or fuel. Work completed afterward will be response rather than earlier preparation.",
     "Fund practical reserve instructions within the window.", "Improve the receiving and movement chain."),
    ("One Slot Offered Twice",
     "A useful mobility service can be offered abroad only if the reserve authority remains able to account for the work left at home. Officials can protect domestic dispersal, or prepare a bounded offer to Central Usea. Preparing the offer reduces its later institutional burden, but it does not create another service slot or oblige the recipient to accept. Refusal must leave the mobility programme useful.",
     "Protect the domestic dispersal programme.", "Prepare a bounded mobility offer."),
    ("Receipts from Different Places",
     "Recovery has brought together receipts from offices that no longer share the same route. Some describe delivered work; others describe a load that never found a receiving service. Inspection can rebuild local capacity around the surviving evidence. A faster operational restart can instead prioritise movement and reopen the next review allocation. The missing receipt cannot honestly be replaced by a declaration that everything arrived.",
     "Inspect the surviving record and rebuild local capacity.", "Restart the movement service and reopen review."),
    ("A Reserve That Can Say No",
     "The reserve authority can now describe its actual limits under the settlement that remains. A useful national programme is one that can refuse a fifth commitment when only four slots exist. The country can renew ordinary service work whose funded completions aid recovery, or retain a readiness record with its continuing public burden. The choice preserves a limited capability rather than an endless emergency.",
     "Renew ordinary mobility and receiving services.", "Retain the funded readiness record."),
],
"DEL": [
    ("A Requisition without a Receipt",
     "A command office has a signed requisition that the receiving clerk says was never accepted. Both papers are genuine. Delarus can publish a common record and take responsibility for answering disputes, or retain a restricted operational account and improve the movement of instructions. The decision changes the administration's working practice. It neither replaces the existing leadership nor settles every later argument between inspectors and commanders.",
     "Publish an accountable common record.", "Retain a restricted operational account."),
    ("The Inspector and the Waiting Order",
     "An inspector has found that two lawful orders depend on the same public service. The command office needs an answer today; the records service wants to establish which obligation was accepted first. Funding a verified review restores institutional capacity. An immediate operational allocation instead opens the next task and strengthens coordination. Whichever course is chosen, one office will have to record a refusal.",
     "Fund the verified review and restore capacity.", "Open the next operational allocation."),
    ("An Emergency Stamp on the Forecast",
     "The international warning has acquired an emergency stamp before the receiving office has written a practical instruction. Civil inspectors propose guidance that can earn a real preparation credit before the crisis. Command staff ask for the same attention to be spent on the working record of instructions and obligations. The administration must distinguish preparing a service from merely acknowledging the forecast.",
     "Pay for verified practical preparation.", "Concentrate on command and receiving records."),
    ("Cooperation Is Not a Blank Cheque",
     "A request for cooperation has reached the obligation desk without a clear end to the receiving country's responsibility. Delarus can give domestic oversight precedence, or prepare a defined offer to Central Usea. The latter reduces the administrative burden of sending one offer, but leaves acceptance conditional on both participants remaining eligible. Existing leadership retains responsibility for either decision.",
     "Protect the domestic oversight programme.", "Prepare one offer with explicit obligations."),
    ("The Files That Came Back",
     "The records service has recovered a set of emergency dockets. Their signatures are legible, but some receiving offices cannot be reconstructed from the surviving evidence. A verified recovery builds institutional capacity and leaves the uncertainty recorded. A faster operational restart improves coordination and opens the next review allocation. Neither course can honestly turn every surviving instruction into a completed delivery.",
     "Inspect the recovered files and rebuild capacity.", "Restart operational work and reopen review."),
    ("The Record after the Warrant",
     "The final inspection distinguishes continuing obligations from emergency authority that has expired. It follows the actual settlement, including displacement or external constraints, rather than declaring a preferred result. Delarus can renew ordinary service work with continuing recovery value, or retain a funded readiness record. The country has acquired a practice of accountable government, not a new leader or an unlimited command mandate.",
     "Renew ordinary inspected services.", "Keep the funded readiness record."),
],
}


def option_effect(tag, index, choice):
    axes = COUNTRIES[tag]["axes"]
    variable = lambda axis, n: f"add_to_variable = {{ ac_up_{tag.lower()}_{axes[axis]} = {n} }}\n"
    if index == 1:
        return ("add_political_power = -15\nset_country_flag = ac_up_public_record\n" + variable(0, 3)) if choice == 0 else ("add_political_power = -10\n" + variable(2, 4))
    if index == 2:
        return ("add_political_power = -25\n" + variable(1, 2) + guard("ac_pol_active = yes", "set_temp_variable = { ac_pol_capacity_delta = 2 }\nac_pol_change_capacity = yes")) if choice == 0 else ("add_political_power = -15\nclr_country_flag = ac_up_allocation_lock\n" + variable(2, 4))
    if index == 3:
        return ("add_political_power = -20\nadd_to_variable = { ac_up_preparedness = 3 }\n" + variable(1, 2)) if choice == 0 else ("add_political_power = -15\n" + variable(2, 6))
    if index == 4:
        return ("add_political_power = -15\n" + variable(0, 5)) if choice == 0 else ("add_political_power = -15\nset_country_flag = ac_up_offer_priority\n" + variable(1, 2))
    if index == 5:
        return ("add_political_power = -20\n" + variable(0, 4) + guard("ac_pol_active = yes", "set_temp_variable = { ac_pol_capacity_delta = 1 }\nac_pol_change_capacity = yes")) if choice == 0 else ("add_political_power = -20\nclr_country_flag = ac_up_review_cooldown\n" + variable(2, 4))
    return ("add_political_power = -20\nset_country_flag = ac_up_ordinary_service\n" + variable(1, 2)) if choice == 0 else ("add_political_power = -20\nset_country_flag = ac_up_readiness_record\n" + variable(2, 2))


def option_preview(tag, index, choice):
    a, b, c = COUNTRIES[tag]["axis_titles"]
    return {
        (1, 0): f"15 political power. {a} +3; public record: +0.5% stability with a continuing +0.3% consumer-goods factor burden.",
        (1, 1): f"10 political power. {c} +4; no public-record commitment.",
        (2, 0): f"25 political power. {b} +2; restore 2 institutional capacity if that framework is active.",
        (2, 1): f"15 political power. {c} +4; reopen the next service allocation. An already occupied service remains occupied.",
        (3, 0): f"20 political power. {b} +2; record 3 verified preparation credits before 8 July 1999. Preparation is applied once after the existing Usean owner initializes.",
        (3, 1): f"15 political power. {c} +6; no additional preparation credit.",
        (4, 0): f"15 political power. {a} +5; concentrate on domestic service.",
        (4, 1): f"15 political power. {b} +2; the once-only FCU offer restores one institutional capacity after payment. The offer must still be earned and both partners remain eligible.",
        (5, 0): f"20 political power. {a} +4; restore 1 institutional capacity if that framework is active.",
        (5, 1): f"20 political power. {c} +4; reopen the national review allocation. Existing commitments and costs remain.",
        (6, 0): f"20 political power. {b} +2; future eligible funded service completions add one further recovery point through the existing Usean owner.",
        (6, 1): f"20 political power. {c} +2; +1% army organisation with a continuing +0.5% consumer-goods factor burden.",
    }[index, choice]


def build_narrative(effects, triggers):
    tick = guard("date > 1991.1.31", "set_country_flag = ac_up_event_1_past")
    tick += guard("date > 1999.7.7", "set_country_flag = ac_up_event_3_past")
    for offset, (tag, cfg) in enumerate(COUNTRIES.items()):
        actor_tick = ""
        for index, (title, desc, a, b) in enumerate(NARRATIVES[tag], 1):
            ident = "ac_up." + str(offset * 10 + index)
            condition = f"ac_up_active = yes tag = {tag} has_country_flag = ac_up_event_{index}_ready NOT = {{ has_country_flag = ac_up_event_{index}_answered }}"
            if index in (1, 3):
                condition += f" NOT = {{ has_country_flag = ac_up_event_{index}_past }}"
            if index == 1:
                condition += " date < 1991.2.1"
            if index == 3:
                condition += " date > 1996.4.19 date < 1999.7.8"
            if index == 4:
                condition += " date > 1999.7.7"
            if index in (5, 6):
                condition += " ac_up_settlement_ready = yes"
            actor_tick += guard(condition + f" NOT = {{ has_country_flag = ac_up_event_{index}_sent }}", f"set_country_flag = ac_up_event_{index}_sent\ncountry_event = {{ id = {ident} days = 1 }}")
            loc(ident + ".t", title); loc(ident + ".d", desc)
            event = f"id = {ident}\ntitle = {ident}.t\ndesc = {ident}.d\npicture = GFX_report_event_defense_white_paper\nis_triggered_only = yes\n" + block("trigger", condition)
            for choice, text in enumerate((a, b)):
                key = ident + (".a" if choice == 0 else ".b"); loc(key, text)
                effect = f"{tag}_up_event_{index}_{choice}_apply"
                loc(effect + "_tt", option_preview(tag, index, choice))
                option_condition = condition
                if index == 4 and choice == 1:
                    option_condition += " NOT = { has_country_flag = ac_up_offer_attempted }"
                effects[effect] = guard(option_condition, f"set_country_flag = ac_up_event_{index}_answered\n" + option_effect(tag, index, choice) + "ac_up_bound = yes\nac_up_recalculate = yes")
                body = f"name = {key}\nai_chance = {{ factor = {65 if choice == 0 else 35} }}\n"
                if index == 4 and choice == 1:
                    body += "trigger = { NOT = { has_country_flag = ac_up_offer_attempted } }\n"
                body += "custom_effect_tooltip = " + effect + "_tt\n" + block("hidden_effect", effect + " = yes")
                event += block("option", body)
            EVENTS.append(block("country_event", event))
        tick += guard("tag = " + tag, actor_tick)
    effects["ac_up_narrative_tick"] = tick
