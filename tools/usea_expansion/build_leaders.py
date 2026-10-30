"""Implement missing 1991 government roles without inventing people.

Sinclair's earlier term was explicitly approved by the user on 2026-10-30.
Other missing identities use a localized office and their existing national flag.
Only new-campaign histories are wired; no startup effect replaces saved leaders.
"""
import argparse,hashlib,json,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
from script import parse,get,walk
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
SUBTYPES={'democratic':'centrism','communism':'socialism','fascism':'fascism_ideology','neutrality':'centrism_na','monarchism':'constitutional_monarchy'}
MARKER='# BEGIN EXPANSION START LEADER'

def capture():
    leaders={}
    groups=get(parse((MOD/'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig')),'ideologies')
    subtype_group={sub:group for group,_,body in groups for sub,_,_ in get(body,'types',[])}
    for p in (MOD/'common/characters').glob('*.txt'):
        if p.name=='ac_starting_governments.txt':continue
        for ident,_,node in get(parse(p.read_text(encoding='utf-8-sig',errors='replace')),'characters',[]):
            roles=[v for k,_,v in node if k=='country_leader']
            leaders[ident]=[subtype_group.get(get(r,'ideology','').strip('"')) for r in roles if get(r,'expire','"2066.1.1"').strip('"')>'1991.1.1']
    rows=[]
    for p in sorted((MOD/'history/countries').glob('*.txt')):
        text=p.read_text(encoding='utf-8-sig').split(MARKER)[0];t=parse(text)
        party=get(get(t,'set_politics',[]),'ruling_party','neutrality')
        recruited=[v for k,_,v in t if k=='recruit_character']
        active=[c for c in recruited if party in leaders.get(c,[])]
        legacy=any(k=='create_country_leader' for k,_,v in t)
        rows.append(dict(tag=p.name[:3],history=p.relative_to(MOD).as_posix(),party=party,existing_active=active,legacy=legacy,missing=not active and not legacy))
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    manifest=HERE/'leaders.json'
    if not manifest.exists():manifest.write_text(json.dumps(capture(),indent=2)+'\n')
    rows=json.loads(manifest.read_text());chars=[];loc=[];gfx=[];assets=[];outputs={}
    for row in rows:
        if not row['missing']:continue
        tag=row['tag'];named=tag=='FCU';ident='FCU_robert_sinclair' if named else tag+'_ac_government_office'
        name='Robert Sinclair' if named else 'Office of the Crown' if row['party']=='monarchism' else 'National Administration'
        desc=('Robert Sinclair leads Central Usea in this campaign. His presence at the 1991 start is provisional mod chronology; the official chronology identifies him as FCU president when ISAF is founded in 2003.' if named else 'This office represents the starting government. The identity of its 1991 officeholder has not been established for this mod; the national emblem is used in place of an invented individual.')
        loc.extend([f' {ident}:0 "{name}"',f' {ident}_desc:0 "{desc}"'])
        source=MOD/'gfx/flags'/f'{tag}.tga'
        if not source.exists():source=MOD/'gfx/flags'/f'{tag}_{row["party"]}.tga'
        path=f'gfx/leaders/AC_start_governments/{tag}.dds';sprite='GFX_ac_exp_government_'+tag
        # Technical packaging of existing flag identity inside an original frame.
        canvas=Image.new('RGBA',(156,210),(8,22,33,255));d=ImageDraw.Draw(canvas)
        d.rectangle((7,7,148,202),outline=(45,85,104,255),width=2)
        d.line((16,27,140,27),fill=(93,208,223,255),width=2)
        d.line((16,183,140,183),fill=(93,208,223,255),width=2)
        if source.exists():
            with Image.open(source) as original:flag=ImageOps.contain(original.convert('RGBA'),(126,100),Image.Resampling.LANCZOS)
            canvas.alpha_composite(flag,((156-flag.width)//2,(210-flag.height)//2))
        else:
            # SET has no flag in the payload. A labeled office card is not a new
            # national flag, coat of arms, or a fabricated person's portrait.
            font=ImageFont.truetype(str(ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'),28)
            d.text((78,105),tag,font=font,anchor='mm',fill=(218,237,242,255))
        import io
        stream=io.BytesIO();canvas.save(stream,format='DDS');outputs[path]=stream.getvalue()
        assets.append(dict(file=path,width=156,height=210,frames=1,source=source.relative_to(MOD).as_posix() if source.exists() else None,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None,sha256=hashlib.sha256(outputs[path]).hexdigest(),role='existing national flag in original office frame' if source.exists() else 'original office identification card; established flag absent'))
        gfx.append(f'spriteType = {{ name = "{sprite}" texturefile = "{path}" }}')
        chars.append(f'''{ident} = {{
 name = {ident}
 portraits = {{ civilian = {{ large = "{sprite}" }} }}
 country_leader = {{ ideology = {SUBTYPES[row['party']]} traits = {{ }} expire = "2066.1.1.1" desc = {ident}_desc }}
}}''')
        target=MOD/row['history'];old=target.read_text(encoding='utf-8-sig').split(MARKER)[0].rstrip()
        outputs[row['history']]=(old+'\n\n'+MARKER+'\n# New campaigns only; provenance: tools/usea_expansion/leaders.json.\nrecruit_character = '+ident+'\n# END EXPANSION START LEADER\n').encode()
    outputs['common/characters/ac_starting_governments.txt']=('characters = {\n'+'\n'.join(chars)+'\n}\n').encode()
    outputs['localisation/english/ac_starting_governments_l_english.yml']=('l_english:\n'+'\n'.join(loc)+'\n').encode('utf-8-sig')
    outputs['interface/ac_starting_governments.gfx']=('spriteTypes = {\n'+'\n'.join(gfx)+'\n}\n').encode()
    for file,data in outputs.items():
        target=MOD/file
        if a.check:
            actual=target.read_bytes() if target.exists() else b''
            if file.endswith(('.txt','.yml','.gfx')):actual=actual.replace(b'\r\n',b'\n');data=data.replace(b'\r\n',b'\n')
            if actual!=data:raise SystemExit('Starting leader output differs: '+file)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    if not a.check:(HERE/'leader_assets.json').write_text(json.dumps(assets,indent=2)+'\n')
    print('Starting government audit:',len(rows),'histories;',len(chars),'missing roles implemented (Sinclair plus office representations).')

if __name__=='__main__':main()
