"""Reproducible original ACES chrome, semantic focus compositions and DDS packaging.

Uses only authored geometry, the bundled OFL font and recorded format metadata.
No installed-game pixels or fonts are read. Official art is packaged separately.
"""
import argparse,hashlib,json,math,re,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'port_1_19'))
from pdx import top_items

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
NAVY=(8,22,33,255);PANEL=(13,32,46,255);EDGE=(45,85,104,255)
CYAN=(93,208,223,255);WHITE=(218,237,242,255);GOLD=(230,181,95,255)
FONT=ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'
COUNTRIES=('ERU','FCU','NPT','REC','YUK')
ASSETS=[]


def save(relative,im,frames=1,role='authored'):
    p=MOD/relative;p.parent.mkdir(parents=True,exist_ok=True)
    im.convert('RGBA').save(p)
    ASSETS.append(dict(file=relative,width=im.width,height=im.height,frames=frames,role=role,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))


def glyph(im,kind,rect,color=CYAN):
    x,y,w,h=rect;d=ImageDraw.Draw(im)
    def pts(p):return [(round(x+a*w/100),round(y+b*h/100)) for a,b in p]
    def line(p):d.line(pts(p),fill=color,width=max(1,round(w/22)),joint='curve')
    def poly(p):d.polygon(pts(p),fill=color)
    def ellipse(a,b,c,e):d.ellipse((x+a*w/100,y+b*h/100,x+c*w/100,y+e*h/100),outline=color,width=max(1,round(w/24)))
    if kind=='industry':
        line([(8,88),(8,45),(33,57),(33,39),(61,54),(61,17),(79,17),(79,88),(8,88)])
        for a in (23,44,66):line([(a,69),(a,79)])
    elif kind=='logistics':
        line([(5,70),(95,70),(95,34),(5,34),(5,70)]);line([(65,34),(65,70)])
        ellipse(16,68,35,88);ellipse(68,68,87,88);line([(12,21),(48,21)])
    elif kind=='air':
        poly([(50,4),(57,40),(94,68),(94,77),(57,64),(57,85),(71,94),(29,94),(43,85),(43,64),(6,77),(6,68),(43,40)])
    elif kind in ('navy','carrier','submarine'):
        poly([(5,64),(95,64),(78,86),(22,86)])
        line([(18,92),(38,96),(58,92),(80,96),(96,92)])
        if kind=='carrier':line([(8,53),(90,53),(90,64)]);line([(70,53),(70,24),(82,24),(82,53)])
        elif kind=='submarine':ellipse(11,45,88,75);line([(44,45),(44,27),(57,27),(57,35)])
        else:line([(25,62),(31,42),(59,42),(70,62)]);line([(49,42),(49,12),(67,26),(49,26)])
    elif kind=='assembly':
        poly([(5,27),(50,6),(95,27)]);line([(9,90),(91,90)])
        for a in (23,50,77):line([(a,37),(a,79)])
    elif kind=='ballot':
        line([(12,49),(12,89),(88,89),(88,49),(12,49)]);line([(34,60),(66,60)])
        line([(26,25),(58,7),(78,38),(46,55),(26,25)])
    elif kind=='science':
        ellipse(13,13,87,87);ellipse(35,5,65,95);line([(7,50),(93,50)]);poly([(46,45),(54,45),(57,50),(50,56),(44,50)])
    elif kind=='radar':
        ellipse(8,8,92,92);ellipse(29,29,71,71);line([(50,50),(80,19)]);line([(50,6),(50,94)]);line([(6,50),(94,50)])
    elif kind=='diplomacy':
        line([(8,42),(33,24),(53,35),(68,27),(94,43),(73,72),(57,85),(39,73),(8,42)])
        line([(33,24),(25,44),(40,53),(53,35)]);line([(39,57),(59,75)])
    elif kind=='economy':
        for a,b in [(12,45),(39,30),(66,12)]:
            line([(a,88),(a,b),(a+18,b),(a+18,88)])
        line([(7,93),(93,93)])
    elif kind=='civil':
        line([(12,88),(12,44),(50,10),(88,44),(88,88),(12,88)])
        line([(50,45),(50,77)]);line([(34,61),(66,61)])
    elif kind=='rebuild':
        line([(18,94),(18,12),(86,12),(18,40)]);line([(70,12),(70,57),(80,57),(80,68)])
        line([(38,93),(38,70),(64,70),(64,93)]);line([(9,94),(29,94)])
    elif kind=='communications':
        line([(32,93),(50,32),(68,93)]);line([(39,71),(61,71)])
        ellipse(42,10,58,26);line([(29,9),(20,18),(29,27)]);line([(71,9),(80,18),(71,27)])
    elif kind=='training':
        poly([(5,32),(50,12),(95,32),(50,53)]);line([(24,46),(24,68),(50,79),(76,68),(76,46)])
        line([(90,34),(90,70)])
    elif kind=='command':
        line([(8,18),(92,18),(92,86),(8,86),(8,18)]);line([(25,70),(45,43),(70,62),(84,31)])
        ellipse(36,34,54,52);line([(21,8),(21,28)])
    elif kind=='meteor':
        poly([(10,66),(22,49),(44,45),(59,65),(48,88),(26,94)])
        for a in (0,18,36):line([(49+a,9),(30+a,42)])
    elif kind=='missile':
        poly([(50,4),(61,25),(61,71),(76,91),(57,83),(43,83),(24,91),(39,71),(39,25)])
        line([(46,92),(46,99)]);line([(54,92),(54,99)])
    elif kind=='gate':
        line([(8,90),(8,42),(18,42),(18,90)]);line([(82,90),(82,42),(92,42),(92,90)])
        line([(18,49),(82,49)]);line([(18,65),(82,65)])
        for a in (29,48,67):line([(a,49),(a+10,65)])
        line([(46,38),(46,8),(63,8),(63,30),(46,30)])
    elif kind=='refugees':
        ellipse(14,8,30,24);ellipse(43,12,59,28);ellipse(72,8,88,24)
        for a in (22,51,80):
            line([(a,32),(a,67),(a-9,92)]);line([(a,67),(a+9,92)]);line([(a-12,51),(a,35),(a+12,51)])
        line([(61,63),(74,63),(74,81),(61,81),(61,63)])
    elif kind=='medical':
        line([(8,30),(92,30),(92,88),(8,88),(8,30)]);line([(34,30),(34,14),(66,14),(66,30)])
        line([(50,42),(50,76)]);line([(33,59),(67,59)])
    elif kind=='shelter':
        line([(4,88),(50,14),(96,88),(4,88)]);line([(50,14),(50,88)])
        line([(37,88),(50,57),(63,88)])
    elif kind=='rail':
        line([(25,97),(38,76)]);line([(75,97),(62,76)])
        for a in (82,91):line([(20,a),(80,a)])
        line([(20,72),(20,16),(33,6),(67,6),(80,16),(80,72),(20,72)])
        line([(31,24),(69,24),(69,43),(31,43),(31,24)])
        ellipse(29,54,41,66);ellipse(59,54,71,66)
    elif kind=='tools':
        line([(18,86),(68,36)]);line([(25,93),(76,42)])
        line([(68,36),(60,20),(67,6),(73,25),(88,29),(92,12),(98,25),(90,41),(76,42)])
        line([(12,17),(86,91)]);line([(7,23),(18,12),(40,34),(29,45),(7,23)])
    elif kind=='telescope':
        line([(13,36),(67,8),(80,32),(26,60),(13,36)])
        line([(50,47),(50,63),(22,94)]);line([(50,63),(77,94)]);line([(50,63),(50,95)])
    elif kind=='satellite':
        line([(36,36),(64,36),(64,64),(36,64),(36,36)])
        for a in (4,72):
            line([(a,31),(a+24,31),(a+24,70),(a,70),(a,31)])
            line([(a+12,31),(a+12,70)]);line([(a,51),(a+24,51)])
        line([(28,51),(36,51)]);line([(64,51),(72,51)])
        line([(50,36),(50,15),(63,4)]);line([(44,76),(37,91)]);line([(58,78),(55,97)])
    elif kind=='document':
        line([(17,6),(65,6),(83,24),(83,94),(17,94),(17,6)])
        line([(65,6),(65,24),(83,24)])
        for a in (38,51,64):line([(29,a),(70,a)])
        line([(30,79),(41,87),(58,73)])
    elif kind=='scales':
        line([(50,8),(50,87),(25,87),(75,87)]);line([(12,26),(88,26)])
        for a in (23,77):
            line([(a,26),(a-16,59),(a+16,59),(a,26)])
            line([(a-16,59),(a-8,68),(a+8,68),(a+16,59)])
    elif kind=='peace':
        line([(50,92),(50,20)])
        for a,b in ((22,40),(42,60),(62,80)):
            poly([(50,b),(22,a),(19,a-14),(37,a-5)])
            poly([(50,b),(78,a),(81,a-14),(63,a-5)])
    elif kind=='fishing':
        line([(8,51),(24,32),(55,25),(78,38),(96,22),(96,78),(78,62),(55,75),(24,68),(8,51)])
        ellipse(24,45,30,51);line([(49,26),(61,11),(70,31)])
    elif kind=='runway':
        line([(15,94),(39,6),(61,6),(85,94),(15,94)])
        for a,b in ((16,26),(38,51),(66,83)):line([(50,a),(50,b)])
        for a in (23,36,64,77):line([(a,87),(a,94)])
    elif kind=='bridge':
        line([(4,70),(96,70)]);line([(22,90),(22,16)]);line([(78,90),(78,16)])
        line([(5,57),(22,27),(50,55),(78,27),(95,57)])
        for a,b in ((12,45),(35,40),(50,55),(65,40),(88,45)):line([(a,b),(a,70)])
    elif kind=='medal':
        line([(18,4),(41,4),(60,43),(40,57),(18,4)])
        line([(60,4),(82,4),(61,53),(43,43),(60,4)])
        ellipse(27,45,73,93);poly([(50,53),(55,66),(69,67),(58,76),(61,88),(50,81),(39,88),(42,76),(31,67),(45,66)])
    else:
        line([(50,5),(87,23),(81,66),(50,94),(19,66),(13,23),(50,5)])
        line([(31,48),(45,63),(70,34)])


def themes(title):
    words=title.lower()
    rules=[('carrier|amphib|lift','carrier'),('submarine','submarine'),('naval|navy|fleet|harbor|harbour|maritime|port|sea lane','navy'),('air|wing|fighter|flight|pilot','air'),('radar|warning|tracking','radar'),('arkbird|orbital|science|research|scientific','science'),('rail|supply|logistic|transport|stockpile|depot','logistics'),('rebuild|recovery|reconstruction|repair','rebuild'),('refugee|relief|shelter|medical|civil|rescue','civil'),('industrial|industry|production|factory|manufactur|workshop','industry'),('econom|bond|trade|export|treasury|accounts|budget|audit','economy'),('elect|ballot|mandate','ballot'),('diploma|treaty|accord|talks|partner|cooper|dialogue|neutral|ties|compact|outreach','diplomacy'),('school|college|exercise|training|instructor|veteran','training'),('communication|radio|network|signal','communications'),('command|staff|doctrine|planning|review|plan|lessons','command'),('assembly|government|administr|council|reform|republic|oversight','assembly')]
    rules.extend([('machine.tool','industry'),('freight|reserve allocation','logistics'),('cabinet|secretariat|desk','assembly'),('service board','civil')])
    selected=[theme for pattern,theme in rules if re.search(pattern,words)]
    return (selected+['security','command'])[:2]


def skin(spec):
    w,h,n=spec['width'],spec['height'],spec['frames'];fw=w//n
    im=Image.new('RGBA',(w,h),(0,0,0,0));name=spec['name'].lower()
    for i in range(n):
        tile=Image.new('RGBA',(fw,h),(0,0,0,0));d=ImageDraw.Draw(tile)
        accent=GOLD if ('researched' in name or 'completed' in name) else EDGE if 'unavailable' in name else CYAN
        if n>1:accent=[accent,WHITE,GOLD,EDGE,CYAN][i%5]
        if 'transparen' in name or name.endswith(('event_pic_clip','event_news_pic_overlay')):pass
        elif 'close' in name or 'clear' in name:
            d.rectangle((0,0,fw-1,h-1),fill=NAVY,outline=EDGE)
            d.line((fw*.3,h*.3,fw*.7,h*.7),fill=accent,width=max(1,fw//12))
            d.line((fw*.7,h*.3,fw*.3,h*.7),fill=accent,width=max(1,fw//12))
        elif re.search(r'focus_(unavailable|can_start|current|completed)',name):
            d.rectangle((0,0,fw-1,h-1),fill=NAVY,outline=accent)
            d.line((1,h-3,fw-2,h-3),fill=accent,width=2)
        elif 'scroll' in name:
            if 'up' in name:d.polygon([(fw/2,2),(2,h-2),(fw-2,h-2)],fill=accent)
            elif 'down' in name:d.polygon([(2,2),(fw-2,2),(fw/2,h-2)],fill=accent)
            elif 'left' in name:d.polygon([(2,h/2),(fw-2,2),(fw-2,h-2)],fill=accent)
            elif 'right' in name:d.polygon([(2,2),(fw-2,h/2),(2,h-2)],fill=accent)
            else:d.rectangle((0,0,fw-1,h-1),fill=EDGE if 'track' in name else accent)
        elif 'link' in name or 'exclusive_line' in name:
            cx,cy=fw//2,h//2
            if 'exclusive' in name:
                d.line((0,cy,fw,cy),fill=accent,width=max(1,h//8))
                if 'link_exclusive' in name:glyph(tile,'security',(1,1,max(1,fw-2),max(1,h-2)),accent)
            else:
                # Directional tiles repeat along the graph. Drawing a full
                # cross in every left/right tile produces a rail-like fence.
                directions=name.split('focus_link')[-1].strip('_').split('_')
                ends={'up':(cx,0),'down':(cx,h),'left':(0,cy),'right':(fw,cy)}
                if directions==['']:directions=['up','down']
                for direction in directions:
                    if direction in ends:d.line(((cx,cy),ends[direction]),fill=accent,width=2)
        elif ('progress' in name or 'bar3' in name) and h<50:
            d.rectangle((0,0,fw-1,h-1),fill=PANEL,outline=accent)
            if 'frame' not in name:d.rectangle((2,2,max(2,fw-3),max(2,h-3)),fill=accent)
        elif any(k in name for k in ('bg','background','frame','button','item','tab','border','header','win','tile','find','stripes','event_option_entry')):
            d.rectangle((0,0,fw-1,h-1),fill=NAVY,outline=EDGE)
            if fw>5 and h>5:
                d.line((2,2,min(fw-3,fw//3),2),fill=accent,width=2)
                d.line((fw-fw//3,h-3,fw-3,h-3),fill=accent,width=2)
            if ('frame' in name or 'border' in name) and not any(k in name for k in ('window','dialog','paper')):
                if fw>10 and h>10:d.rectangle((4,4,fw-5,h-5),fill=(0,0,0,0))
            if 'tab' in name and h>25:glyph(tile,themes(name)[0],(fw*.35,h*.15,fw*.3,h*.7),accent)
        elif 'close' in name or 'clear' in name:
            d.line((fw*.25,h*.25,fw*.75,h*.75),fill=accent,width=max(1,fw//12))
            d.line((fw*.75,h*.25,fw*.25,h*.75),fill=accent,width=max(1,fw//12))
        elif 'glow' in name or 'ongoing' in name or 'highlight' in name:
            d.ellipse((1,1,fw-2,h-2),outline=(*accent[:3],130),width=max(1,min(fw,h)//22))
        elif 'niche' in name:
            glyph(tile,['air','navy','radar','security','logistics','communications','science','command'][i%8],(1,1,fw-2,h-2),accent)
        else:
            motif=themes(name)[0]
            if 'ships' in spec['source_texture'] or 'navalcombat' in spec['source_texture']:motif='submarine' if 'submarine' in name else 'carrier' if 'carrier' in name else 'navy'
            glyph(tile,motif,(1,1,max(1,fw-2),max(1,h-2)),accent)
        im.alpha_composite(tile,(i*fw,0))
    return im


def build_ui():
    specs=json.loads((HERE/'ui_assets.json').read_text());new=[];engine=[];files={}
    for spec in specs:
        asset='gfx/interface/ac_expansion/ui/'+spec['name']+'.dds'
        save(asset,skin(spec),spec['frames'],'original UI artwork')
        if spec['role']=='repair':files.setdefault(spec['file'],{})[spec['name']]=asset
        else:
            body='name = "%s"\ntexturefile = "%s"\nnoOfFrames = %d\n'%(spec['name'],asset,spec['frames'])
            for key in ('borderSize','size'):
                if key in spec:body+=key+' = { '+spec[key]+' }\n'
            if spec['kind'].lower()=='frameanimatedspritetype':body+='animation_rate_fps = 15\nlooping = yes\nplay_on_show = yes\n'
            if 'effectFile' in spec:body+='effectFile = "'+spec['effectFile']+'"\n'
            (engine if spec['role']=='engine_focus' else new).append(spec['kind']+' = {\n'+body+'}\n')
    for file,mapping in files.items():
        p=MOD/file;text=p.read_text(encoding='utf-8-sig')
        for kind,name,raw in top_items(text,'spriteTypes'):
            if name in mapping:
                replacement=re.sub(r'\btexturefile\s*=\s*(?:"[^"]*"|[^\s{}]+)','texturefile = "'+mapping[name]+'"',raw,count=1,flags=re.I)
                text=text.replace(raw,replacement)
        p.write_text('\n'.join(line.rstrip() for line in text.splitlines())+'\n',encoding='utf-8')
    for suffix,color in [('',CYAN),('_bg',PANEL)]:
        save('gfx/interface/ac_expansion/ui/focus_progress'+suffix+'.dds',Image.new('RGBA',(166,21),color),role='original progress texture')
    new.append('progressbartype = { name = "GFX_ac_ui_prod_progress_bar3" color = { 0.36 0.82 0.87 } colortwo = { 0.05 0.12 0.18 } textureFile1 = "gfx/interface/ac_expansion/ui/focus_progress.dds" textureFile2 = "gfx/interface/ac_expansion/ui/focus_progress_bg.dds" size = { x = 166 y = 21 } effectFile = "gfx/FX/progress_startend.lua" }\n')
    research=MOD/'interface/countrytechtreeview.gfx'
    text=re.sub(r'"gfx[\\/]+interface[\\/]+prod_progress_bar2(_bg)?\.dds"',lambda m:'"gfx/interface/ac_expansion/ui/research_progress'+(m[1] or '')+'.dds"',research.read_text())
    research.write_text(text)
    for suffix,color in [('',CYAN),('_bg',PANEL)]:save('gfx/interface/ac_expansion/ui/research_progress'+suffix+'.dds',Image.new('RGBA',(218,21),color),role='original research progress texture')
    (MOD/'interface/ac_expansion_ui.gfx').write_text('spriteTypes = {\n'+''.join(new)+'}\n')
    # Same filename suppresses the engine's later definitions. An early-sorted
    # additive GFX file alone is insufficient for hard-coded focus-state names.
    (MOD/'interface/nationalfocusview.gfx').write_text('spriteTypes = {\n'+''.join(engine)+'}\n')


def focus_records():
    loc={}
    for p in (MOD/'localisation/english').glob('*.yml'):
        for m in re.finditer(r'^\s*([\w.]+):\d*\s+"(.*)"',p.read_text(encoding='utf-8-sig'),re.M):loc[m[1]]=m[2]
    records=[]
    for p in (MOD/'common/national_focus').glob('*.txt'):
        if not p.name.startswith(COUNTRIES):continue
        for m in re.finditer(r'\bid\s*=\s*(\w+)\s+icon\s*=\s*(\w+)',p.read_text(encoding='utf-8-sig')):
            ident=m[1]
            overrides={'ERU_ucw_garrison_the_continent':['logistics','security'],'FCU_ucw_exp_peace_commission':['assembly','diplomacy'],'REC_exp_council_audit':['economy','command']}
            records.append(dict(id=ident,file=p.relative_to(MOD).as_posix(),tag=ident[:3],title=loc.get(ident,ident),motifs=overrides.get(ident,themes(loc.get(ident,ident)))))
    return records


def build_focuses():
    from focus_compositions import direction
    sprites=[];records=focus_records();font=ImageFont.truetype(str(FONT),14);used={}
    for record in records:
        ident,title,tag=record['id'],record['title'],record['tag']
        im=Image.new('RGBA',(192,192));d=ImageDraw.Draw(im)
        index=COUNTRIES.index(tag);accent=[(219,164,91,255),CYAN,(148,210,186,255),(202,137,128,255),(151,183,225,255)][index]
        silhouettes=[[(18,34),(96,10),(174,34),(161,147),(96,177),(31,147)],[(20,20),(172,20),(172,155),(96,179),(20,155)],[(96,7),(181,88),(151,163),(41,163),(11,88)],[(28,15),(164,15),(180,150),(96,179),(12,150)],[(96,7),(171,39),(171,153),(21,153),(21,39)]]
        d.polygon(silhouettes[index],fill=NAVY);d.line(silhouettes[index]+[silhouettes[index][0]],fill=accent,width=3)
        # Explicit subjects and arrangements differ even without title text.
        record['motifs'],layout=direction(title,tag,used)
        record['composition']=layout[0]
        glyph(im,record['motifs'][0],layout[1],WHITE)
        glyph(im,record['motifs'][1],layout[2],accent)
        d.text((96,17),tag,font=font,fill=accent,anchor='mt')
        im=im.resize((96,96),Image.Resampling.LANCZOS)
        asset='gfx/interface/ac_expansion/focus/'+ident+'.dds';save(asset,im,role='original focus artwork')
        name='GFX_ac_exp_'+ident
        for suffix in ('','_shine'):
            sprites.append('spriteType = { name = "%s%s" texturefile = "%s" }'%(name,suffix,asset))
        record.update(sprite=name,asset=asset)
        p=MOD/record['file'];text=p.read_text(encoding='utf-8-sig')
        text=re.sub(r'(\bid\s*=\s*'+ident+r'\s+icon\s*=\s*)\w+',lambda m:m[1]+name,text)
        p.write_text(text,encoding='utf-8')
    (MOD/'interface/ac_expansion_focus.gfx').write_text('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n')
    (HERE/'focus_art.json').write_text(json.dumps(records,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--ui-only',action='store_true');a=p.parse_args()
    build_ui()
    if not a.ui_only:
        build_focuses()
        build_policy_art()
        build_continuous()
    (HERE/'assets.json').write_text(json.dumps(ASSETS,indent=2)+'\n')
    print('Original artwork packaged:',len(ASSETS),'textures.')


def build_policy_art():
    from fcu_content import POLICIES
    sprites=[]
    for tag in COUNTRIES:
        subjects=[('civil','assembly'),('directive','security'),('service','rebuild')]
        if tag=='FCU':subjects=[(key,value[3]) for key,value in POLICIES.items()]
        for kind,motif in subjects+[('programmes','civil'),('maintain_services','training')]:
            size=(75,75) if kind not in ('programmes','maintain_services') else (100,100) if kind=='programmes' else (32,32)
            im=Image.new('RGBA',(150,150));d=ImageDraw.Draw(im)
            d.polygon([(12,20),(138,20),(138,118),(75,145),(12,118)],fill=NAVY,outline=CYAN)
            glyph(im,motif,(28,32,94,85),WHITE)
            d.text((75,4),tag,font=ImageFont.truetype(str(FONT),16),fill=CYAN,anchor='mt')
            im=im.resize(size,Image.Resampling.LANCZOS)
            path='gfx/interface/ac_expansion/policies/'+tag.lower()+'_'+kind+'.dds';save(path,im,role='original national policy artwork')
            name=('GFX_decision_category_ac_exp_'+tag.lower()+'_programmes' if kind=='programmes' else 'GFX_decision_'+tag+'_exp_maintain_services' if kind=='maintain_services' else 'GFX_idea_ac_exp_'+tag.lower()+'_'+kind)
            sprites.append('spriteType = { name = "'+name+'" texturefile = "'+path+'" }')
    (MOD/'interface/ac_expansion_policies.gfx').write_text('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n')

def build_continuous():
    from script import render,walk,get,setv
    contract=json.loads((HERE/'continuous_contract.json').read_text());sprites=[]
    # Swiss militia/readiness mechanics have no Strangereal country or owner.
    # Keep ordinary production, training and construction continuous focuses.
    for _,node in walk(contract):
        node[:]=[row for row in node if not (row[0]=='focus' and isinstance(row[2],list) and (get(row[2],'id','').startswith('SWI_')))]
    for _,node in walk(contract):
        icon=get(node,'icon')
        if not icon:continue
        name='GFX_ac_exp_continuous_'+get(node,'id')
        setv(node,'icon',name)
        im=Image.new('RGBA',(96,96));d=ImageDraw.Draw(im)
        d.polygon([(48,4),(89,24),(85,75),(48,92),(11,75),(7,24)],fill=NAVY,outline=CYAN)
        glyph(im,themes(icon)[0],(22,22,52,52),WHITE)
        asset='gfx/interface/ac_expansion/continuous/'+get(node,'id')+'.dds';save(asset,im,role='original continuous focus artwork')
        sprites.append('spriteType = { name = "'+name+'" texturefile = "'+asset+'" }')
    path=MOD/'common/continuous_focus/generic.txt';path.parent.mkdir(exist_ok=True);path.write_text(render(contract)+'\n')
    (MOD/'interface/ac_expansion_continuous.gfx').write_text('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n')

if __name__=='__main__':main()
