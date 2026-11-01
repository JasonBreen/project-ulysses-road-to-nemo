"""Original national programme calibration, not canonical institutions or GDP."""
from dataclasses import dataclass
from superpowers.content import BRANCHES

COUNTRIES={'OSE':'Osea','YUK':'Yuktobania'}
LATER_PARENT={
 'guarantor_review':'appropriations','civil_space':'air_watch',
 'procurement_scrutiny':'productive_capacity','crisis_authority':'continental_transport',
 'distribution_review':'allocation','maritime_support':'logistics',
 'technical_cooperation':'industrial_orders','orders_review':'training'}
LAYOUT={'OSE':([20,38,56,74],20,28,6500),'YUK':([2,15,28,41],12,20,3168)}

@dataclass(frozen=True)
class Service:
    branch:object
    index:int
    number:int

    @property
    def id(self):return f'{self.branch.tag}_snp_{self.branch.key}_service_{self.index+1}'
    @property
    def prefix(self):return f'ac_snp_{self.branch.tag.lower()}_{self.branch.key}_{self.index+1}'
    @property
    def lane(self):return 'civil'if self.index==0 else 'protected'
    @property
    def weight(self):return self.index+1 if self.branch.tag=='OSE' else 25
    @property
    def title(self):return self.branch.services[self.index][0]
    @property
    def objective(self):return self.branch.services[self.index][1]
    @property
    def modifiers(self):return self.branch.services[self.index][2]
    @property
    def event(self):return 'ac_snp.'+str(1000+self.number)

SERVICES=tuple(Service(b,n,i*2+n)for i,b in enumerate(BRANCHES)for n in range(2))

# Deliberate original subjects. Each branch has two recognisable motifs; six
# compositions pair them with a distinct stage subject and arrangement.
SUBJECTS={
 'appropriations':('assembly','document'),'productive_capacity':('industry','training'),
 'continental_transport':('logistics','rail'),'air_watch':('radar','air'),
 'guarantor_review':('diplomacy','scales'),'civil_space':('satellite','science'),
 'procurement_scrutiny':('tools','economy'),'crisis_authority':('security','ballot'),
 'allocation':('economy','assembly'),'industrial_orders':('industry','tools'),
 'logistics':('rail','logistics'),'training':('training','air'),
 'distribution_review':('document','civil'),'maritime_support':('navy','tools'),
 'technical_cooperation':('science','satellite'),'orders_review':('security','scales')}
