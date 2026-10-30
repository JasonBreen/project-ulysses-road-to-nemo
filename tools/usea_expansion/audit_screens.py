"""Resolve repaired-screen dependencies through the effective engine/mod GUI graph.

Unlike the authored-GFX gate, this reads installed engine definitions and follows
scrollbar templates. It distinguishes texture ownership from shader/flag bindings.
"""
import argparse,json,re,sys
from pathlib import Path
from script import parse,get,walk
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/port_1_19'))
from pdx import top_items
TEX=re.compile(r'\btexturefile[12]?\s*=\s*(?:"([^"]+)"|([^\s{}]+))',re.I)
def effective(engine,suffix):
    files={p.relative_to(engine/'interface').as_posix():p for p in (engine/'interface').rglob('*'+suffix)}
    files.update({p.relative_to(MOD/'interface').as_posix():p for p in (MOD/'interface').rglob('*'+suffix)})
    return [files[k] for k in sorted(files)]
def audit(engine):
    sprites={};templates={};conflicts={}
    for p in effective(engine,'.gfx'):
        for _,name,raw in top_items(p.read_text(encoding='utf-8-sig',errors='replace'),'spriteTypes'):
            if name:
                sprites.setdefault(name,[]).append((p,raw))
    for p in effective(engine,'.gui'):
        try:tree=parse(p.read_text(encoding='utf-8-sig',errors='replace'))
        except (ValueError,IndexError):continue
        for kind,node in walk(tree):
            if kind.lower() in ('scrollbartype','extendedscrollbartype'):
                templates[get(node,'name','').strip('"')]=(p,node)
    report={};failures=[]
    for filename in ('nationalfocusview.gui','countrytechtreeview.gui','ac_economy_gui.gui','eventwindow.gui'):
        tree=parse((MOD/'interface'/filename).read_text())
        if filename=='eventwindow.gui':
            # Operative/leader event windows are preserved compatibility layouts,
            # outside the country/news visual repair being certified here.
            tree=[row for row in tree[0][2] if isinstance(row[2],list) and get(row[2],'name','').strip('"') in ('EventWindow','EventWindow_News','event_option_entry')]
        refs=set();queue=[tree];seen=set();bars=[]
        while queue:
            for _,node in walk(queue.pop()):
                for key,_,v in node:
                    if isinstance(v,list):continue
                    if key.lower() in ('spritetype','quadtexturesprite') and v:refs.add(v.strip('"'))
                    if key.lower() in ('scrollbartype','verticalscrollbar','horizontalscrollbar') and v:
                        name=v.strip('"')
                        if name in seen:continue
                        seen.add(name)
                        if name not in templates:failures.append('Missing scrollbar '+name);continue
                        p,body=templates[name];bars.append(dict(name=name,source=str(p)));queue.append([['template','=',body]])
        if filename=='nationalfocusview.gui':
            # Runtime-selected state and line sprites do not appear in the GUI.
            for _,name,_ in top_items((engine/'interface/nationalfocusview.gfx').read_text(encoding='utf-8-sig'),'spriteTypes'):
                if name:refs.add(name)
            for p in (MOD/'common/continuous_focus').glob('*.txt'):
                refs.update(re.findall(r'\bicon\s*=\s*(GFX_\w+)',p.read_text()))
        rows=[]
        for name in sorted(refs):
            if name in ('GFX_flag_small2','GFX_frontend_bg','GFX_report_event_001','GFX_news_event_001'):
                rows.append(dict(sprite=name,ownership='runtime-selected flag/background/event picture; owning content audit required'));continue
            defs=sprites.get(name,[])
            if not defs:failures.append('Unresolved sprite '+name);rows.append(dict(sprite=name,ownership='missing'));continue
            if len(defs)>1:
                textures={tuple((m[1] or m[2]) for m in TEX.finditer(raw)) for _,raw in defs}
                if len(textures)>1:conflicts[name]=[str(p) for p,_ in defs]
            p,raw=defs[-1];assets=[(m[1] or m[2]).replace('\\','/').lstrip('/') for m in TEX.finditer(raw)]
            owned=bool(assets) and all((MOD/a).exists() for a in assets)
            if not owned:failures.append('Engine imagery or missing texture: '+name)
            rows.append(dict(sprite=name,ownership='mod' if owned else 'engine or missing',definition=str(p),textures=assets,shaders=re.findall(r'effectFile\s*=\s*"([^"]+)"',raw,re.I)))
        report[filename]=dict(sprites=rows,scrollbars=bars)
    report.update(conflicting_effective_sprite_definitions=conflicts,failures=sorted(set(failures)))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('engine',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();report=audit(a.engine)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(failures=report['failures'],conflicts=report['conflicting_effective_sprite_definitions']),indent=2))
    if report['failures'] or report['conflicting_effective_sprite_definitions']:raise SystemExit(1)
