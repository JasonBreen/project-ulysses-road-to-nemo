"""Original national office scenes; no canonical people, battles or outcomes."""
from superpowers.content import BRANCHES,focus_id
from superpowers.mechanics import COUNTRIES

# Each response is an original incident, distinct from the focus-description
# context. Speakers are unnamed working roles, never invented officeholders.
SCENES={
 'appropriations':(
  'The Third Copy',
  "The receiving clerk lays three copies of the same staff reservation across the committee table. Each bears a different departmental seal. The chair asks which copy should become the public record; the clerk answers that choosing a copy will not release a single worker. A civil-service representative proposes a hearing at which the receiving offices can challenge the reservation. The defence representative asks for a protected session first, so junior staff can explain how the duplicate promises were made without answering for their superiors in public. Both want a usable register. They disagree about which protection must come first, and the clerk waits with all three copies still open.",
  ('Let the receiving offices challenge the public schedule.','Protect the first staff testimony and publish the limits.'),
  'A Reservation with an Answer',
  "The clerk returns with the same three copies, now attached to a completed receiving period. The committee can trace the service actually performed and the work displaced by it. One of the original departments has asked that its superseded reservation be removed. The chair leaves it in the file. A later reader needs to understand why the office declined a promise as well as why it accepted another. The standing appropriation preserves the selected priority and its continuing burden. It gives the next government a responsible receiving office, rather than permission to count the same staff three times."),
 'productive_capacity':(
  'The Apprentice at the Back of the Room',
  "An apprentice has attended the whole workshop meeting without speaking. When the superintendent begins to close the docket, she asks whether the training release listed beside her name is still real. A repair deadline has already used the reserved hours. The production representative offers an internal arrangement: a senior worker will cover the lessons after the shift. The training secretary asks that the release itself be restored and the delayed productive work recorded openly. Neither proposal gives the workshop an extra person. The apprentice wants the qualification and knows that the worker offering to teach her is already staying late. The board must decide whose promise it will protect.",
  ('Protect the scheduled training release and record the delay.','Accept supervised instruction within a protected workshop rota.'),
  'The Qualification and the Waiting Work',
  "The apprentice brings a corrected training return to the review. It records the instruction actually received rather than the hours initially reserved. Beside it lies the maintenance queue, including work deliberately left waiting. The superintendent no longer describes both as an unused reserve. The board's chosen policy has become a practical obligation with a cost that somebody can identify. Its improved settlement will support the next period, but it will not erase the delay or create a second shift of trained workers. The apprentice asks that the receiving clerk keep both documents together so her qualification cannot later be used to conceal the work that paid for it."),
 'continental_transport':(
  'A Timetable Written in Two Inks',
  "The dispatch exercise uses two inks for movements whose receiving windows overlap. A civil coordinator has marked the ordinary repair traffic; the military liaison has marked a support reservation. Both lines end at the same receiving desk. When a trainee tries to solve the exercise by moving one line into an unmarked hour, the dispatcher asks who will staff it. The room falls quiet. The civil coordinator proposes published notice periods, so affected services can challenge an exception before preparing their work around it. The liaison proposes a protected urgent channel with an identified officer answerable for every displaced reservation. The exercise needs a rule that somebody can actually follow.",
  ('Publish the notice period and the receiving office’s right to object.','Keep an urgent channel with a named receiving responsibility.'),
  'The Movement That Was Deliberately Delayed',
  "The review includes the movement that the exercise deliberately delayed. Its receiving office has written a short account of the staff and maintenance time released by that decision. The military liaison asks that the report distinguish a refusal from a lost message. The civil coordinator agrees and asks that an accepted exception remain visible for the same reason. The completed service period gives the timetable a tested procedure; it cannot make every requested window available. Under the standing settlement, later dispatchers inherit the chosen priority and its burden, together with a record explaining why one unfulfilled reservation was the responsible result."),
 'air_watch':(
  'Three Seconds on a Training Tape',
  "A controller stops a recorded handover exercise at a three-second silence. No aircraft is waiting on this channel; the staff are working through a desk rehearsal. The training officer says that the silence allowed a confirmation to arrive. The civil liaison says the receiving office could not tell a deliberate pause from a broken connection. A junior controller asks whether that uncertainty belongs in the open lesson or in a protected instructor's return. Publishing it would let outside receiving offices test the procedure. Protecting the first debrief could make staff more willing to admit how uncertain they were. The tape remains stopped while the committee decides how the lesson will be received.",
  ('Open the handover lesson to civil receiving offices.','Protect the instructor’s first debrief and require a bounded return.'),
  'A Pause with a Receiving Rule',
  "The controller plays the silent interval again. This time the completed exercise return identifies which office should acknowledge the pause and what happens when its answer does not arrive. Nobody has removed the uncertain three seconds. The watch policy has gained a tested receiving rule while retaining its political or civilian reservation cost. The instructor cautions that a desk exercise proves no aircraft serviceability or operational success. The committee accepts that limit and keeps the unfinished questions beside the final lesson. A later watch can use the procedure without inheriting a claim that quiet on a training tape meant certainty."),
 'guarantor_review':(
  'The Letter without a Receiving Date',
  "The external-commitments folder contains a letter thanking the government for assistance. The review staff cannot find a corresponding receiving date. One official wants the letter included as evidence of confidence; another asks whether anybody can now explain what was promised. The committee has no authority to manufacture a foreign answer. It can publish a limited renewal schedule around the domestic staff actually available, or first protect a narrower receiving mandate while those staff inspect the old undertaking. The civil-service officer asks that a refusal remain an acceptable return. The military representative agrees, provided the next government can distinguish a refused promise from an obligation quietly abandoned.",
  ('Publish a limited renewal schedule and retain useful refusals.','Protect a narrower inspection mandate before renewing the promise.'),
  'A Useful Answer Can Be a Limit',
  "The completed review returns the unanswered letter with its missing receiving date still marked. The national service has established what the domestic offices can sustain and who must explain a proposed renewal. It has not invented foreign consent. The committee keeps that distinction in the standing guarantee. The earlier priority remains different under public hearings and a protected mandate, and its continuing burden remains payable at home. A later government may accept, renegotiate or refuse another undertaking from this record. It will first have to name the receiving office and the work that its promise would displace."),
 'civil_space':(
  'The Notebook outside the Sealed Folder',
  "A technical archivist brings two objects to the review: a sealed programme folder and an ordinary notebook of methods that the researchers used to check their observations. The security officer asks which belongs to the cooperation record. The archivist answers that the notebook can be useful even when the programme's present status permits no new exchange. A civil researcher wants the transferable methods opened to independent scrutiny. The test representative asks for a protected technical return before uncertain results are treated as established knowledge. Two measurements remain unanswered in the notebook's margin, and neither researcher will mark them complete merely to empty the agenda. The committee must decide how to keep useful knowledge without promising a result that the responsible programme has not delivered.",
  ('Open the reusable methods and mark uncertain results clearly.','Protect the technical return until the uncertainty is examined.'),
  'What the Archive Can Honestly Keep',
  "The archivist returns a receiving list from the completed period. It separates usable methods from material whose status remains restricted or unresolved. A researcher asks whether the final hearing will describe that distinction as a disappointing result. The chair instead calls it the limit of the national archive's authority. The standing policy improves the chosen disclosure or protected-testing route while retaining its cost. It leaves the strategic programme and cooperation state with their responsible offices. The notebook can now be found by a later technical team without requiring that team to believe an announcement whose underlying result was never received."),
 'procurement_scrutiny':(
  'The Inspector’s Unused Stamp',
  "The acceptance inspector has brought an unused stamp to the committee. During a receiving exercise, an invoice and a workshop return carried matching totals but different explanations of what had passed inspection. The procurement officer asks whether the discrepancy could have been corrected inside the office. The inspector says it could, and asks who would then know why the stamp was withheld. An open receiving test would let the affected workshops challenge the record. A protected replacement-priority return would let technical staff reconcile it before a disputed entry was treated as a failed delivery. Both routes can preserve the objection. They reserve different authority and impose different costs on the next receiving period.",
  ('Keep the withheld acceptance open to receiving-office challenge.','Reconcile the technical return under a protected replacement priority.'),
  'An Acceptance Record with the Objection Intact',
  "The inspector places the stamp beside the completed return without using it on the superseded form. The exercise has established a procedure for identifying what was inspected, what was accepted and what remains disputed. The committee keeps the original objection in the final record. Its standing settlement can improve inspection or replacement administration, but factories, orders and actual equipment remain necessary for a delivery. The procurement officer asks that the next receiving team inherit that limit as plainly as it inherits the selected priority. A readable invoice must never become a substitute for the thing that was supposed to arrive."),
 'crisis_authority':(
  'The Instruction during the Rehearsal',
  "The emergency-authority exercise stops when the receiving clerk asks for an approval that the instruction cites but does not contain. The officer conducting the drill says the delay would matter during a real crisis. The clerk agrees and leaves the line open. A civil representative proposes a verification return that every affected office can read. The command liaison proposes a narrower delegated mandate with an explicit expiry and a protected channel for the missing answer. Neither wants obedience to depend on an unanswered telephone. The committee must choose which route will receive exceptional instructions, and who will be responsible when the promised confirmation does not come.",
  ('Require a civil verification return before exceptional authority expands.','Use a limited delegated mandate with a protected confirmation channel.'),
  'Authority That Can Receive a Question',
  "The clerk brings the original instruction to the final exercise review. Its missing approval has not been quietly added to the old copy. The completed period records how the receiving office asked its question and which authority was required to answer. That procedure gives the standing mandate a practical limit, whether the government chose public verification or protected delegation. It predicts no future conflict and grants no permanent emergency powers. The liaison asks that the next exercise retain the same right to stop at an unanswered line. The committee agrees that the record would be less useful if its final page contained only success."),
 'allocation':(
  'The Messenger Returns with the Docket',
  "A district messenger returns an allocation docket because the receiving office cannot release the staff listed on it. The command representative recognizes the reservation but has a second claim against the same hours. The civil administrator asks which office should explain the delay to the people waiting for ordinary services. A public receiving route would reserve more discretion for those civil offices. A protected command route would concentrate responsibility for the support commitment and require the delay to be recorded there. Neither creates additional staff. The messenger waits while the secretariat decides who will receive the next unanswered request, and which share of the finite allocation that answer must use.",
  ('Give civil receiving offices the larger share of discretion.','Reserve the command share and identify who answers for displaced work.'),
  'A Hundred Points with Responsible Offices',
  "The messenger brings back the first docket together with the completed receiving period. Its original reservation can now be traced to an office, a release decision and the work that actually followed. The allocation still totals one hundred. The improvement is that neither side can claim the same unreserved share without showing what it would displace. The standing settlement preserves the selected civil or command priority and its continuing cost. The secretariat retains the returned docket because it records a limit that the clean final table cannot show by itself: allocating responsibility is useful only when an office remains available to receive the complaint."),
 'industrial_orders':(
  'The Repair Window on the Order Sheet',
  "A workshop planner has crossed out a productive shift and written maintenance in the margin. The order representative asks why a trained crew should stand aside while an important return is waiting. The planner replies that the crew is not idle; it is trying to keep the next reservation credible. A civil commission member proposes protecting the workshop's ordinary receiving and training windows. The command representative proposes a narrower defence-order reserve, with one office responsible for recording every displaced job. Neither option gives the workshop another machine or a second skilled crew. The disagreement concerns who may promise the hours already available, and who must answer when those hours are used elsewhere.",
  ('Protect ordinary workshop continuity and its receiving windows.','Reserve the defence-order share and keep the displaced work visible.'),
  'The Work Left on the Schedule',
  "The planner returns with a completed inspection period and the jobs that remained on the schedule. The final record does not describe those jobs as free capacity. It explains which reservation took priority and what the workshop received in return. The standing compact improves the selected receiving or order policy while retaining its continuing burden. The command representative asks that a later allocation not erase the maintenance line simply because the period has closed. The civil member agrees. Neither side will inherit a factory, a productive shift or a skilled worker that the national programme did not physically possess."),
 'logistics':(
  'Two Receiving Windows in the Depot Exercise',
  "The depot exercise gives a trainee two dispatch requests and one receiving window. He places both requests on the board and waits for the instructor to identify the more important seal. The instructor asks instead which office has reserved the staff. A civil dispatcher proposes protecting district delivery windows until an exception is accepted by their receiving desk. The command liaison proposes a protected support allocation with a recorded duty to explain displaced civilian work. Both rules can produce a refusal. The trainee asks whether that would count as failing the exercise. The committee must decide whether its receiving record is allowed to show a responsible limit before it records another promise.",
  ('Protect district windows until their receiving office accepts an exception.','Reserve command dispatch and record every displaced civil reservation.'),
  'The Refusal in the Dispatch Return',
  "The completed exercise return includes one refused dispatch. Its receiving office has explained which reservation made the refusal necessary and what would have to change before the request could be accepted. The instructor keeps that explanation beside the successful receiving entry. The national timetable has gained a usable procedure, rather than an assertion that all traffic can move at once. Its standing settlement retains the chosen priority and the opportunity cost shown in the allocation. The trainee can now distinguish a message that was lost from a request that reached a responsible office and received an unwelcome but useful answer."),
 'training':(
  'The Unsigned Instructor’s Note',
  "A junior instructor has left a note about an exercise return without signing it. The commission secretary asks whether it should be included in the professional review. The staff representative says that an unsigned objection cannot alter a command assessment; another instructor asks why the author did not believe a signed objection would be received. An open debrief could let the training offices test the criticism together. A protected staff return could give the instructor a responsible channel before the dispute becomes public. Neither route proves that the note is correct. The commission must choose how uncertainty can reach somebody able to answer it without treating silence as professional agreement.",
  ('Open the lesson to a professional debrief across receiving offices.','Protect the first staff return and require an accountable answer.'),
  'A Professional Lesson with Its Doubt Preserved',
  "The note has a receiving entry in the completed period. The record distinguishes the criticism, the staff answer and the parts that remain uncertain. The commission has not rewritten the inherited command-reform choice to obtain that result. Its standing settlement improves the selected professional or staff-directed route while preserving the continuing cost. A senior instructor asks that the uncertainty remain in the final lesson, so a later class will not mistake an accepted procedure for proof that every judgment was correct. The secretary files the original note beside its answer instead of replacing both with a cleaner assessment."),
 'distribution_review':(
  'The Receipt That Does Not Close the Case',
  "A receiving clerk has marked a case complete because the docket contains a receipt. The civil inspector points to a later correction showing that the receiving office had asked for different work. The command liaison says that the original reservation was fulfilled as authorized. Nobody disputes the signatures. They disagree about which question the receipt answers. A standing civil inspection route would give the receiving office more authority to reopen the case. A protected command-priority route would keep responsibility concentrated while requiring the correction to remain attached to the original allocation. The committee must choose how a valid record can still be challenged when it does not explain the service people expected to receive.",
  ('Let civil receiving offices reopen the discrepancy.','Keep command responsibility and attach the unresolved correction.'),
  'The Correction beside the Receipt',
  "The final distribution return contains the receipt and the later correction. A completed service period has established which office must receive the discrepancy and who can authorize the next response. The committee leaves the two documents together. Its standing policy retains the chosen civil inspection or protected command priority, along with the continuing cost that made that priority possible. The clerk asks whether the case should now be described as successful. The inspector answers that the useful result is more precise: the government can explain what was received, what remains disputed and where the next question must go."),
 'maritime_support':(
  'The Shore Office’s Old Maintenance Book',
  "A former watch officer brings an old maintenance book to the shore commission. Several entries refer to reservations whose present receiving authority is unclear. The harbour representative asks that ordinary civil services receive a protected window before another exceptional support promise is made. The naval liaison asks for a bounded fleet-maintenance share with one shore office answerable for the resulting delays. Neither asks the book to prove that a hull is currently serviceable, or even that an old entry still describes an active vessel. The commission must decide how present support work will be received, and how the dockside record will explain the civilian work reserved or displaced by that choice.",
  ('Protect civil port windows and let the shore office challenge exceptions.','Reserve bounded fleet maintenance and identify its dockside responsibility.'),
  'The Quayside Limit in the Final Return',
  "The old book returns with the completed shore-support inspection. Its useful entries have responsible receiving offices; uncertain entries remain marked as uncertain. The standing policy improves the selected civil or fleet-maintenance priority while retaining the cost of reserved staff. The naval liaison asks that the final return distinguish support administration from a claim about operating tempo. The harbour representative agrees and keeps the waiting repair work in the record. The same vessels and repair queues still wait beyond the committee room, and she insists that their needs remain on the following week's agenda. The shore establishment has acquired a better way to explain what it can sustain and what it must decline."),
 'technical_cooperation':(
  'The Researcher’s Second Copy',
  "A researcher has kept a second copy of a technical method because the first was filed with a cooperation programme whose present status she cannot confirm. The security representative asks whether the copy belongs in a civil archive or a protected technical docket. The receiving secretary points out that neither filing decision can establish an accord that the responsible authorities have not accepted. An open civil return could preserve useful methods and their uncertainties. A protected allocation could first examine which observations can be released without turning an incomplete result into public assurance. The researcher wants somebody to receive the copy in either case, so interrupted or absent cooperation does not make domestic knowledge disappear with the unanswered folder.",
  ('Open the reusable civil methods with their uncertainty intact.','Protect the technical examination before releasing an incomplete result.'),
  'A Domestic Use for the Second Copy',
  "The researcher receives an archive entry from the completed period. It identifies what the domestic office can use, what remains protected and which result has not been established. The standing scientific policy improves the chosen disclosure or protected-allocation route while retaining its cost. The file offers no answer to the wider cooperation question, only a signed promise that another domestic team will receive her methods. The secretary files the second copy where a later team can find it without first assuming that a cooperation announcement remained valid. The useful national conclusion is the receiving route itself: knowledge has an accountable home even when another office cannot promise a new exchange."),
 'orders_review':(
  'The Seal and the Missing Approval',
  "The verification exercise ends with an envelope left open on the ministerial desk. Its seal is correct, but the instruction refers to an approval that the receiving staff cannot locate. The command liaison asks for a response that can survive a real deadline. The clerk asks for a channel that can survive an unwelcome question. A ministerial verification duty would reserve more civil authority for receiving the challenge. A limited command mandate would protect a narrower response chain with an explicit duty to return the missing answer. Neither route changes the inherited intervention or command-reform record. The review must choose how responsibility moves when a valid-looking order reaches the office that is expected to obey it.",
  ('Reserve ministerial authority to receive and verify the challenge.','Protect a limited command return with an explicit answering duty.'),
  'A Question That Reached Its Authority',
  "The final orders return records the challenge and the office that received it. The completed exercise has not proved that every future instruction will arrive on time or that every answer will be wise. It has established a funded route through which a missing approval can be questioned without making silence the final authority. The standing settlement improves the selected ministerial or command procedure while retaining its continuing burden. The clerk leaves the envelope open in the review copy. A later government can inherit the record and use the route without being told that an exercise decided the outcome of a conflict that had not yet occurred."),
}

OPENINGS={
 'OSE':('The Register Has Three Spaces',
  "The federal receiving clerk has drawn three spaces across the new schedule. A committee member asks why the form is so small when the country has many services. The clerk answers that a limited register must be capable of refusing a promise. A civil administrator wants the first hearing to let ordinary receiving offices challenge the reservations made in their names. The defence representative asks that staff first have a protected channel for explaining uncertain estimates. Neither proposal supplies another trained team. Both can make the register more credible, while giving a different audience the first claim on its attention. The clerk places the blank schedule between them and waits for an instruction that can be entered without writing the same space twice.",
  ('Begin with a civil receiving-office hearing.','Begin with a protected readiness return.')),
 'YUK':('The Two Columns Must Still Add Up',
  "The allocation secretary draws a line beneath the civil and command columns. Their total is one hundred, although each receiving office has brought requests that would use more. A district administrator asks for greater discretion to release ordinary services. The command representative wants a protected support share so a national undertaking has a responsible office behind it. Neither can satisfy every request by changing the label on the columns. The first hearing will establish who may question an allocation before it becomes a promise to another service. The secretary asks both representatives to leave the unaccepted requests on the table. A useful docket must record what was displaced as well as what the government chose to receive.",
  ('Give the first discretion to civil receiving offices.','Protect the first command-support reservation.'))}

FINALS={
 'OSE':('A Federal Schedule That Can Be Renewed',
  "The receiving clerk brings the first three-space register to the final hearing. It is covered in corrections, but every completed period now has an office that received it and a record of the work deliberately left waiting. The committee has chosen different priorities across the civilian, readiness and external books. Their costs have not vanished because the assessment is complete. A later government will inherit those priorities together with a finite schedule on which to renew or refuse another promise. The civil administrator asks for a protected period of public maintenance review. The defence representative asks for a narrower readiness return. Both accept that the next undertaking must name its receiving authority before it occupies another space. The clerk opens a fresh page without increasing the number of spaces.",
  ('Support the public maintenance return.','Reserve an accountable readiness return.')),
 'YUK':('A Docket with Somewhere to Send the Next Question',
  "The original allocation sheet has been returned so often that its folds are beginning to tear. The secretary places it beneath the completed national returns. The civil and command shares still total one hundred; what has changed is the government's ability to identify who reserved each period and who must answer for the work it displaced. The inherited intervention, command-reform and scientific-cooperation records remain their own obligations. These national procedures do not erase them. A district representative asks for a further period of civil inspection. The command liaison asks for a bounded support return with the displaced civilian claims kept beside it. The next government can choose either, and must keep a receiving office available when the unanswered requests arrive again.",
  ('Support the civil inspection return.','Reserve the bounded command-support return.'))}


def narrative(effects,triggers,loc,idea):
    from superpowers.build import block,guard,active,bid,host
    events=[];custom=[];dispatch=[];interrupt=[]
    def choice_delta(tag,index):
        if tag=='OSE':return 'add_to_variable = { ac_snp_ose_public = '+('4'if index==0 else'-2')+' }\nadd_to_variable = { ac_snp_ose_security = '+('-2'if index==0 else'4')+' }\n'
        return 'add_to_variable = { ac_snp_yuk_civil = '+('5'if index==0 else'-5')+' }\n'
    def event(number,tag,title,prose,condition,options,picture):
        ident='ac_snp.'+str(number);token='ac_snp_message_'+str(number)
        triggers[token+'_answerable']=active(tag)+' has_country_flag = '+token+'_pending has_country_flag = '+token+'_window NOT = { has_country_flag = '+token+'_answered }'
        dispatch.append(guard(active(tag)+' '+condition+' NOT = { has_country_flag = '+token+'_sent }','set_country_flag = '+token+'_sent\nset_country_flag = '+token+'_pending\nset_country_flag = { flag = '+token+'_window days = 60 }\ncountry_event = { id = '+ident+' days = 1 }'))
        interrupt.extend(['clr_country_flag = '+token+'_pending','clr_country_flag = '+token+'_window'])
        loc(ident+'.t',title);loc(ident+'.d',prose)
        body='id = '+ident+'\ntitle = '+ident+'.t\ndesc = '+ident+'.d\npicture = '+picture+'\nis_triggered_only = yes\nfire_only_once = yes\ntrigger = { '+token+'_answerable = yes }\n'
        for i,(label,action)in enumerate(options):
            key=ident+'.'+chr(97+i);loc(key,label)
            apply=token+'_reply_'+str(i)
            effects[apply]=guard(token+'_answerable = yes','set_country_flag = '+token+'_answered\nclr_country_flag = '+token+'_pending\nclr_country_flag = '+token+'_window\n'+action+'\nac_snp_reconcile = yes')
            if 40<=number<70:summary='Retain the completed national service record and its prior choices. This acknowledgement authorizes no additional funded period.'
            elif tag=='OSE':summary=('Civil support +4, readiness support -2.'if i==0 else'Readiness support +4, civil support -2.')+' Both observations remain within zero to one hundred.'
            else:summary='Move up to five existing allocation points toward '+('civil receiving offices'if i==0 else'command support')+', protecting active reservations. The two shares still total one hundred.'
            loc(key+'_effect_tt',summary)
            shown='custom_effect_tooltip = '+key+'_effect_tt\n'
            if number>=70:shown+='show_ideas_tooltip = '+tag+'_snp_final_'+('civil'if i==0 else'protected')+'_spirit\n'
            body+=block('option','name = '+key+'\nai_chance = { factor = '+('55'if i==0 else'45')+' }\n'+shown+block('hidden_effect',apply+' = yes'))
        events.append(block('country_event',body))
    for i,tag in enumerate(COUNTRIES):
        title,prose,labels=OPENINGS[tag]
        options=[(label,'set_country_flag = '+tag+'_snp_opening_'+('civil'if n==0 else'protected')+'\n'+choice_delta(tag,n))for n,label in enumerate(labels)]
        ready='OR = { '+' '.join('has_country_flag = '+focus_id(b,0)+'_done'for b in BRANCHES if b.tag==tag)+' }'
        event(1+i,tag,title,prose,ready,options,'GFX_ac_snp_event_'+tag.lower()+'_national')
    for i,b in enumerate(BRANCHES):
        title,prose,labels,final_title,final_prose=SCENES[b.key];branch=bid(b)
        policy=branch+'_policy_context';entries=''
        for p in(1,2):
            key=policy+'_'+str(p);loc(key,'The standing policy is '+b.policies[p-1][0].lower()+'. Its continuing opportunity cost remains in the national schedule.')
            entries+=block('text','trigger = { has_country_flag = '+focus_id(b,p)+'_done }\nlocalization_key = '+key)
        custom.append(block('defined_text','name = '+policy+'\n'+entries))
        options=[(label,'set_country_flag = '+branch+'_reply_'+('civil'if n==0 else'protected')+'\n'+choice_delta(b.tag,n))for n,label in enumerate(labels)]
        context=('\n[ac_snp_yuk_intervention_context]\n[ac_snp_yuk_command_context]'if b.tag=='YUK'and b.key in('allocation','training','distribution_review','orders_review')else'')
        if b.key in('civil_space','technical_cooperation'):context+='\n[ac_snp_arkbird_context]'
        event(10+i,b.tag,title,prose+'\n\n['+policy+']'+context,'OR = { has_country_flag = '+focus_id(b,1)+'_done has_country_flag = '+focus_id(b,2)+'_done }',options,'GFX_ac_snp_event_'+branch)
        callback=branch+'_response_context';entries=''
        for kind,text in(('civil','The earlier reply gave the civil receiving offices the first route for a challenge. The assessment retains that decision and the responsibilities it reserved.'),
                         ('protected','The earlier reply protected the first professional or command return. The assessment preserves the uncertainty and identifies the office responsible for answering it.'),
                         ('unanswered','No first reply was ratified. The chair reads that absence into the final record before turning to the service period and its receiving office.')):
            key=callback+'_'+kind;loc(key,text)
            entries+=block('text',('trigger = { has_country_flag = '+branch+'_reply_'+kind+' }\n'if kind!='unanswered'else'')+'localization_key = '+key)
        custom.append(block('defined_text','name = '+callback+'\n'+entries))
        period=branch+'_period_context';loc(period+'_domestic','The latest qualifying period was funded as reduced domestic continuity during war. Records, training liaison and maintenance administration continued while other staff answered urgent national needs.')
        loc(period+'_ordinary','The latest qualifying period completed its ordinary national receiving work. The assessment retains its costs and identifies the office expected to answer when another funded period is requested.')
        custom.append(block('defined_text','name = '+period+'\n'+block('text','trigger = { has_country_flag = '+branch+'_last_domestic }\nlocalization_key = '+period+'_domestic')+block('text','localization_key = '+period+'_ordinary')))
        event(40+i,b.tag,final_title,final_prose+'\n\n['+callback+']\n['+period+']\n['+policy+']'+context,'has_country_flag = '+focus_id(b,5)+'_done',
              [('File the assessment with its unresolved questions.','set_country_flag = '+branch+'_assessment_recorded')],'GFX_ac_snp_event_'+branch)
    for i,tag in enumerate(COUNTRIES):
        title,prose,labels=FINALS[tag];options=[]
        for n,label in enumerate(labels):
            ident=tag+'_snp_final_'+('civil'if n==0 else'protected')
            values=({'repair_speed_factor':.025,'political_power_gain':-.05}if n==0 else{'army_org_factor':.02,'consumer_goods_factor':.005})if tag=='OSE'else({'repair_speed_factor':.025,'army_org_factor':-.005}if n==0 else{'supply_consumption_factor':-.02,'consumer_goods_factor':.005})
            idea(ident+'_spirit',COUNTRIES[tag]+(': Public Receiving Assessment'if n==0 else': Accountable Support Return'),
                 'The completed national review supports this ninety-day receiving period. Its continuing political, civilian or readiness cost remains; existing national obligations are retained.',values)
            options.append((label,'set_country_flag = '+ident+'\nadd_timed_idea = { idea = '+ident+'_spirit days = 90 }\n'+choice_delta(tag,n)))
        ready=' '.join('has_country_flag = '+focus_id(b,5)+'_done'for b in BRANCHES if b.tag==tag)
        callback=tag+'_snp_opening_context';entries=''
        for kind,text in(('civil','The first hearing gave civil receiving offices the first claim on the register’s attention. The final account returns to that promise without declaring every dispute settled.'),
                         ('protected','The first hearing began with a protected professional return. The final account records the chosen responsibility without erasing the work that remained outside it.'),
                         ('unanswered','The opening invitation was never ratified. The final account says so plainly and proceeds from the national periods that were actually completed.')):
            key=callback+'_'+kind;loc(key,text);entries+=block('text',('trigger = { has_country_flag = '+tag+'_snp_opening_'+kind+' }\n'if kind!='unanswered'else'')+'localization_key = '+key)
        custom.append(block('defined_text','name = '+callback+'\n'+entries))
        event(70+i,tag,title,prose+'\n\n['+callback+']',ready,options,'GFX_ac_snp_event_'+tag.lower()+'_national')
    # Context is an observation of established owners, never an outcome writer.
    for name,options in {
      'ac_snp_yuk_intervention_context':[
        ('has_country_flag = YUK_fp_intervened','The intervention return still lies beside the allocation sheet. Its obligations are among the claims the receiving office must answer.'),
        ('has_country_flag = YUK_fp_stood_aside','The earlier decision to stand aside remains in the ministerial return. The committee must explain what that restraint reserved for domestic services.'),
        ('','No intervention instruction appears in the material before the committee. The review begins with the receiving responsibilities already assigned.')],
      'ac_snp_yuk_command_context':[
        ('has_idea = yuk_reformed_field_command','Field-command reform governs the officers attending this review. Their task is to make receiving responsibilities clear within that structure.'),
        ('has_idea = yuk_expeditionary_command','Expeditionary-command priorities govern the officers attending this review. The receiving secretary asks them to identify the domestic work reserved beside those commitments.'),
        ('has_idea = yuk_top_heavy_command_structure','The command return still passes through the top-heavy approval structure. The secretary leaves that chain visible while identifying where a receiving office can send its challenge.'),
        ('','The secretary places the government’s present command return beside the allocation sheet, so each new reservation has somewhere to send its next question.')],
      'ac_snp_arkbird_context':[
        ('has_global_flag = ac_sp_arkbird_complete','The debris-clearing programme’s completed return has reached the office. Research staff can examine the received methods within their accepted scientific mandate.'),
        ('YUK = { has_country_flag = ac_yuk_arkbird_partner }','The Yuktobanian partnership appears in the cooperation record. The receiving secretary asks which methods can be examined and which questions still await a joint answer.'),
        ('','The docket contains no joint completion return. Research staff work with domestic methods saved in the archive and mark where a new exchange would be useful.')]
    }.items():
        entries=''
        for n,(condition,text)in enumerate(options):
            key=name+'_'+str(n);loc(key,text);entries+=block('text',('trigger = { '+condition+' }\n'if condition else'')+'localization_key = '+key)
        custom.append(block('defined_text','name = '+name+'\n'+entries))
    effects['ac_snp_narrative_tick']='\n'.join(dispatch)
    effects['ac_snp_interrupt_messages']=guard('ac_snp_participant = yes','\n'.join(interrupt))
    return '\n'.join(events),'\n'.join(custom)
