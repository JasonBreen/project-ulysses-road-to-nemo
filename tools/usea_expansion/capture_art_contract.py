"""Capture texture dimensions and engine sprite contracts, never installed pixels."""
import argparse,json,re,sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'port_1_19'))
from pdx import top_items

HERE=Path(__file__).resolve().parent;MOD=HERE.parents[1]/'mod/2985041246'


def field(raw,key,default=None):
    m=re.search(r'\b'+key+r'\s*=\s*(?:"([^"]*)"|([^\s{}]+))',raw,re.I)
    return (m[1] if m[1] is not None else m[2]) if m else default


def main():
    p=argparse.ArgumentParser();p.add_argument('game',type=Path);a=p.parse_args()
    game={};local={};specs=[]
    for folder,dest in [(a.game/'interface',game),(MOD/'interface',local)]:
        for f in sorted(folder.rglob('*.gfx')):
            for kind,name,raw in top_items(f.read_text(encoding='utf-8-sig',errors='replace'),'spriteTypes'):
                if name:dest[name]=(kind,raw,f)
    wanted={}
    for name,(kind,raw,f) in local.items():
        tex=field(raw,'texturefile')
        if tex:tex=tex.lstrip('/')
        if tex and not (MOD/tex).exists():wanted[(str(f.relative_to(MOD)),name)]=(kind,raw,tex,'repair')
    gui='\n'.join((MOD/'interface'/name).read_text() for name in ('nationalfocusview.gui','frontendmainview.gui','countrytechtreeview.gui','eventwindow.gui'))
    for ref in sorted(set(re.findall(r'"(GFX_ac_ui_[^"]+)"',gui))):
        suffix=ref.removeprefix('GFX_ac_ui_')
        original=suffix if suffix.startswith('gfx_') else 'GFX_'+suffix
        if original not in game and original not in local:raise ValueError('Unknown sprite '+original)
        kind,raw,_=local.get(original,game.get(original));tex=field(raw,'texturefile')
        if tex:tex=tex.lstrip('/')
        wanted[('interface/ac_expansion_ui.gfx',ref)]=(kind,raw,tex,'focus_ui')
    # These sprite names are selected inside the engine, not just by GUI text.
    focus_names=[name for _,name,_ in top_items((a.game/'interface/nationalfocusview.gfx').read_text(encoding='utf-8-sig'),'spriteTypes')]
    focus_names += [n for n in game if n.startswith(('GFX_technology_','GFX_focus_link','GFX_focus_exclusive','GFX_cont_focus','GFX_ongoing_focus','GFX_highlight_focus'))]
    for name in focus_names:
        if not name or name in local:continue
        kind,raw,_=game[name];tex=field(raw,'texturefile')
        if tex:wanted[('interface/ac_expansion_ui.gfx',name)]=(kind,raw,tex,'engine_focus')
    for (file,name),(kind,raw,tex,role) in sorted(wanted.items()):
        if not tex:continue
        src=MOD/tex if (MOD/tex).exists() else a.game/tex
        if not src.exists() and tex.startswith('../'):src=a.game/tex.lstrip('./')
        if not src.exists() and src.with_suffix('.dds').exists():src=src.with_suffix('.dds')
        if not src.exists() and src.name.startswith('subtech_air_techs_'):
            src=src.with_name(src.name.replace('subtech_air_techs_','subtechnology_'))
        if not src.exists():
            matches=list((a.game/'gfx').rglob(src.name))
            if len(matches)==1:src=matches[0]
        if not src.exists() and src.name=='researching_anim_strip.dds':
            src=a.game/'gfx/interface/techtree/tech_doctrine_researching_anim_strip.dds'
        frames=int(field(raw,'noOfFrames','1'))
        if src.exists():
            with Image.open(src) as im:w,h=im.size
        else:
            # Some engine filter definitions point at absent/DLC assets. The
            # focus filter slot is 37x36; an original 32px glyph fits inside it.
            if 'filter' not in tex:raise ValueError('No format reference '+str(src))
            w,h=32*frames,32
            print('Authored 32px filter replacement for absent reference:',name)
        spec=dict(file=file,name=name,kind=kind,width=w,height=h,frames=frames,source_texture=tex,role=role)
        for key in ('borderSize','size'):
            m=re.search(r'\b'+key+r'\s*=\s*\{([^{}]+)\}',raw,re.I)
            if m:spec[key]=m[1].strip()
        effect=field(raw,'effectFile')
        if effect:spec['effectFile']=effect
        specs.append(spec)
    # Preserve the original format/provenance of references already repaired.
    previous=json.loads((HERE/'ui_assets.json').read_text()) if (HERE/'ui_assets.json').exists() else []
    merged={s['name']:s for s in previous}
    for spec in specs:merged.setdefault(spec['name'],spec)
    specs=list(merged.values())
    (HERE/'ui_assets.json').write_text(json.dumps(specs,indent=2)+'\n')
    print('Recorded',len(specs),'sprite format contracts; no installed pixels copied.')


if __name__=='__main__':main()
