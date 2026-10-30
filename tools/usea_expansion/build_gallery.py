"""Build a portable review gallery from the exact packaged textures."""
import base64,html,io,json
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'
OUT=ROOT/'docs/evidence/usea-expansion/artwork-gallery.html'

def picture(path,width):
    with Image.open(path) as source:
        im=source.convert('RGBA');im.thumbnail((width,width))
        buffer=io.BytesIO();im.save(buffer,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()

def card(path,title,detail,category,width=700):
    return '<article data-kind="'+category+'"><img loading="lazy" src="'+picture(path,width)+'" alt="'+html.escape(title)+'"><h3>'+html.escape(title)+'</h3><p>'+html.escape(detail)+'</p></article>'

def main():
    cards=[]
    for row in json.loads((HERE/'media_assets.json').read_text()):
        file=row['file']
        if '_small.dds' in file:continue
        if '/event_pictures/' in file:
            category='events';path=HERE/row['source'];detail='Original illustration master. In-game country-event texture: 200 × 160, with navy letterboxing.'
        else:
            category='portraits' if '/leaders/' in file else 'loading'
            path=MOD/file;detail=f"Official AC8 promotional artwork · {row['width']} × {row['height']} DDS · Bandai Namco Entertainment"
        cards.append(card(path,Path(file).stem.replace('ac_exp_','').replace('_',' ').title(),detail,category))
    for row in json.loads((HERE/'leader_assets.json').read_text()):
        cards.append(card(MOD/row['file'],Path(row['file']).stem+' government office',row['role'],'portraits',210))
    for row in json.loads((HERE/'focus_art.json').read_text()):
        cards.append(card(MOD/row['asset'],row['title'],row['id']+' · '+', '.join(row['motifs']),'focus',192))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Project Ulysses — artwork review</title>
<style>:root{color-scheme:dark}body{margin:0;background:#081621;color:#daedf2;font:16px system-ui}header{padding:32px;max-width:1100px}h1{font-size:30px;margin:0 0 12px}p{line-height:1.5}nav{display:flex;gap:10px;flex-wrap:wrap}button,input{background:#102b3b;color:inherit;border:1px solid #5dd0df;padding:10px;font:inherit}button[aria-pressed=true]{background:#285466}main{padding:24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}article{background:#0d202e;border:1px solid #2d5568;padding:16px;overflow:hidden}article img{width:100%;height:250px;object-fit:contain;background:#081621}article[data-kind=portraits] img{image-rendering:auto}article[data-kind=focus] img{height:144px;image-rendering:auto}article h3{font-size:18px;margin:12px 0 4px}article p{font-size:13px;color:#b9cdd4;overflow-wrap:anywhere}article[hidden]{display:none}</style>
<header><h1>Project Ulysses · Artwork review</h1><p>Four official AC8 loading screens, eight named portrait assets, ten original event illustrations, and 192 focus icons. The North Point runway scene uses the corrected master with the yellow mark removed. Portraits are a presentation collection; they are not assigned to 1991–2005 governments.</p><p>Source and credit records: <a href="../../../tools/usea_expansion/official_art.json">official art</a> · <a href="../../../tools/usea_expansion/original_art.json">original art</a> · <a href="../../../tools/usea_expansion/media_assets.json">packaging manifest</a>. This gallery is an asset review, not native acceptance.</p><nav><button data-filter="all" aria-pressed="true">All</button><button data-filter="loading">Loading screens</button><button data-filter="portraits">Portraits</button><button data-filter="events">Event scenes</button><button data-filter="focus">Focus icons</button><input id="search" aria-label="Search artwork" placeholder="Search artwork"></nav></header><main>'''+''.join(cards)+'''</main><script>let filter='all';const search=document.querySelector('#search');function update(){document.querySelectorAll('article').forEach(a=>a.hidden=(filter!=='all'&&a.dataset.kind!==filter)||!a.textContent.toLowerCase().includes(search.value.toLowerCase()));document.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.filter===filter))}document.querySelectorAll('button').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;update()});search.oninput=update;</script></html>''',encoding='utf-8')
    print(OUT)

if __name__=='__main__':main()
