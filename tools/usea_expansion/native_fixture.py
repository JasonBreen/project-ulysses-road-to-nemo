"""Copy an isolated text save for visual country inspection; no campaign rewards."""
import argparse,hashlib,json,re
from pathlib import Path

ROOT=Path('G:/Project-Ulysses-Native-20261030-Expansion')
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('tag',choices=('ERU','FCU','NPT','REC','YUK'))
    args=parser.parse_args()
    source=args.source.resolve();folder=(ROOT/'profile/save games').resolve()
    if source.parent!=folder:raise SystemExit('Only disposable-profile saves are accepted.')
    raw=source.read_bytes();text=raw.decode('utf-8-sig')
    if not text.startswith('HOI4txt'):raise SystemExit('A text save is required.')
    old=re.search(r'^player="([A-Z]{3})"(?=\r?$)',text,re.M).group(1)
    text,count=re.subn(r'^player="'+old+'"(?=\r?$)', 'player="'+args.tag+'"',text,count=1,flags=re.M)
    assert count==1
    text,count=re.subn(r'(player_countries=\{\s*)'+old+r'(=\{)',r'\g<1>'+args.tag+r'\2',text,count=1)
    assert count==1
    target=folder/('visual_'+args.tag+'_1991.hoi4')
    if target.exists():raise SystemExit('Refusing to replace an existing fixture.')
    target.write_bytes(text.encode('utf-8'))
    record=dict(source=source.name,source_sha256=hashlib.sha256(raw).hexdigest(),
        fixture=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        changes=['player tag','player_countries key'],coverage='Visual inspection only; no natural progression claim')
    (ROOT/'evidence'/('fixture_'+args.tag+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(target)
if __name__=='__main__':main()
