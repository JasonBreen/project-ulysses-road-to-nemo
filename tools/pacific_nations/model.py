"""Original national continuations; no war, project or physical-economy owner."""
from dataclasses import dataclass
import importlib
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
SUFFIXES={8:('brief','civil','protected','protocol','review','public_return','staff_return','settlement'),
          6:('brief','civil','protected','protocol','review','settlement'),
          4:('brief','civil','protected','settlement')}


@dataclass(frozen=True)
class Branch:
    tag:str
    key:str
    parent:str
    opens:str
    motifs:tuple
    steps:tuple
    policies:tuple
    hearing:str
    assessment:str

    @property
    def id(self):return self.tag+'_snc_'+self.key
    @property
    def suffixes(self):return SUFFIXES[len(self.steps)]
    def focus(self,index):return self.id+'_'+self.suffixes[index]


def countries():
    result=[]
    for tag in('OSE','YUK'):
        name='pacific_nations.'+tag.lower()
        if importlib.util.find_spec(name):
            module=importlib.import_module(name)
            expected=44 if tag=='OSE'else 42
            if sum(len(b.steps)for b in module.BRANCHES)!=expected:raise ValueError('Incorrect continuation budget '+tag)
            if len(module.BRANCHES)!=6:raise ValueError('Six individual national lanes required')
            for b in module.BRANCHES:
                if b.tag!=tag or len(b.steps)not in SUFFIXES:raise ValueError('Invalid national branch '+b.key)
                if any(len(text.split())<80 for title,text in b.steps):raise ValueError('Focus needs substantive prose: '+b.id)
                if min(len(b.hearing.split()),len(b.assessment.split()))<80:raise ValueError('National scene too short '+b.id)
            result.append(module)
    return result


def branches():return tuple(b for module in countries()for b in module.BRANCHES)


def refs(branch,index):
    suffix=branch.suffixes[index]
    if suffix=='brief':return ['%s_snp_%s_settlement'%(branch.tag,branch.parent)]
    if suffix in('civil','protected'):return [branch.focus(0)]
    if suffix=='protocol':return [branch.id+'_civil',branch.id+'_protected']
    if suffix in('public_return','staff_return'):return [branch.id+'_review']
    if suffix=='settlement'and len(branch.steps)==8:return [branch.id+'_public_return',branch.id+'_staff_return']
    if suffix=='settlement'and len(branch.steps)==4:return [branch.id+'_civil',branch.id+'_protected']
    return [branch.focus(index-1)]


def positions():
    result={}
    for module in countries():
        for number,b in enumerate(module.BRANCHES):
            x=([20,38,56]if b.tag=='OSE'else[3,18,33])[number%3]
            y=(36 if b.tag=='OSE'else 28)+(number//3)*9
            for index,suffix in enumerate(b.suffixes):
                if suffix in('civil','public_return'):offset=-2
                elif suffix in('protected','staff_return'):offset=2
                else:offset=0
                row=0 if suffix=='brief'else 1 if suffix in('civil','protected')else 2 if suffix=='protocol'or len(b.steps)==4 else 3 if suffix=='review'else 4 if suffix in('public_return','staff_return')or len(b.steps)==6 else 5
                result[b.focus(index)]=(x+offset,y+row)
    return result
