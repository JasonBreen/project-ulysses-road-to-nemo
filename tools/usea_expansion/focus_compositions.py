"""Subject-led art direction; no baked captions used to manufacture uniqueness."""
import re

# Ordered, specific subjects precede broad institutional language. Each focus
# receives a primary subject, a supporting subject, and a distinct arrangement.
RULES=[
 ('headquarters|host isaf','command'),('tango line','gate'),('arm.s length','peace'),
 ('ulysses','meteor'),('stonehenge','radar'),('megalith','missile'),
 ('border|frontier|customs|inspections','gate'),('refugee|resettlement|repatriation|voluntary returns','refugees'),
 ('hospital|medical','medical'),('shelter|camps|humanitarian','shelter'),
 ('rail|freight','rail'),('machine.tool|workshop|maintenance|repair','tools'),
 ('observator','telescope'),('arkbird|orbital|space','satellite'),('tracking|warning|watch|air picture','radar'),
 ('register|inventory|archives|protocols|charter|standards','document'),
 ('audit|accounts|burden|credit|bonds|grievance','scales'),
 ('armistice|peace|neutral|accord','peace'),('fishing','fishing'),
 ('harbour|harbor|coastal|fleet|naval|escort','navy'),('airfield|runway|aircrew','runway'),
 ('air |aircraft|wings|sorties','air'),('amphibious|beachhead|landing|return to the continent','carrier'),
 ('depot|stores|stockpile|logistic|transport|supply','logistics'),
 ('bridge|corridors|road','bridge'),('rebuild|reconstruction|recovery','rebuild'),
 ('election|mandate|reformist','ballot'),('veteran|volunteer','medal'),
 ('security|guard|hardline|hold |garrison','security'),
 ('training|college|exercises|drills','training'),
 ('scientific|science|data','science'),('industry|industrial|production','industry'),
 ('economic|economy|dividend|fund','economy'),('talks|dialogue|mediate|consultations|contacts|liaison|outreach|cooper|partnership|ties','diplomacy'),
 ('command|staff|readiness|defence|defense|army|arms|reserve|mobilize|responsibility|initiative|intervention','command'),
 ('civil|service|resilience|endure','civil'),
 ('government|administrati|cabinet|secretariat|council|republic|office|compact|course|order|communism|desk|commitment','assembly'),
 ('assess|review|programme|commission|settlement|plan|lessons','document'),
]
SUPPORT={
 'meteor':'civil','missile':'command','gate':'document','refugees':'civil',
 'medical':'logistics','shelter':'medical','rail':'logistics','tools':'industry',
 'telescope':'science','satellite':'science','radar':'communications',
 'document':'assembly','scales':'economy','peace':'diplomacy','fishing':'economy',
 'navy':'logistics','runway':'air','air':'command','carrier':'navy',
 'logistics':'document','bridge':'rebuild','rebuild':'tools','ballot':'assembly',
 'medal':'civil','security':'command','training':'command','science':'document',
 'industry':'tools','economy':'scales','diplomacy':'document','command':'communications',
 'civil':'medical','assembly':'document',
}
LAYOUTS=[
 ('inset', (30,32,112,108), (124,108,42,42)),
 ('paired', (25,35,83,100), (108,58,56,66)),
 ('stacked', (48,30,96,86), (70,120,52,40)),
 ('diagonal', (30,30,95,87), (107,96,61,61)),
 ('triptych', (63,32,95,102), (28,113,45,45)),
 ('horizon', (39,25,114,93), (66,120,60,43)),
 ('left_inset', (52,32,112,108), (25,108,42,42)),
 ('lower_subject', (48,74,99,83), (72,22,48,45)),
]

def direction(title,tag,used):
    subjects=[]
    for pattern,subject in RULES:
        if subject not in subjects and re.search(pattern,title.lower()):subjects.append(subject)
    if not subjects:raise ValueError('Art direction missing for '+title)
    primary=subjects[0];secondary=subjects[1] if len(subjects)>1 else SUPPORT[primary]
    pair=(tag,primary,secondary);index=used.get(pair,0);used[pair]=index+1
    if index>=len(LAYOUTS):raise ValueError('More hand-authored arrangements needed for '+str(pair))
    return [primary,secondary],LAYOUTS[index]
