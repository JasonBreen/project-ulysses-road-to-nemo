"""Extract a small, non-personal campaign record from a native text save.

Raw saves remain outside the repository: they contain player names and unrelated
campaign state. This records only the five expansion actors and owning flags.
It reports observations, not assertions that a branch was naturally played.
"""
import argparse, hashlib, json, re
from pathlib import Path

TAGS = ('ERU', 'FCU', 'NPT', 'REC', 'YUK')


def section(text, name, indent):
    prefix = '\t' * indent
    match = re.search(r'^' + prefix + re.escape(name) + r'=\{', text, re.M)
    if not match:
        return ''
    depth = 1
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]', text[match.end():]):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return text[match.end():match.end()+token.start()]
    raise ValueError('Unclosed native block: '+name)


def scalar(text, name):
    match = re.search(r'^\s*' + re.escape(name) + r'=("[^"]*"|[^\s{}]+)', text, re.M)
    return match[1].strip('"') if match else None


def capture(path, coverage):
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    if not text.startswith('HOI4txt'):
        raise ValueError('Use a native uncompressed text save.')
    countries = section(text, 'countries', 0)
    result = dict(save=path.name, sha256=hashlib.sha256(raw).hexdigest(),
                  date=scalar(text, 'date'), version=scalar(text, 'version'),
                  player=scalar(text, 'player'), coverage=coverage, countries={})
    for tag in TAGS:
        body = section(countries, tag, 1)
        if not body:
            raise ValueError('Country missing: ' + tag)
        flags = section(body, 'flags', 2)
        variables = section(body, 'variables', 2)
        result['countries'][tag] = dict(
            tree=scalar(body, 'focus_tree'),
            completed=re.findall(r'^\s*completed="((?:'+'|'.join(TAGS)+r')[^"]*)"', body, re.M),
            flags=sorted(set(re.findall(r'^\s*((?:ac_(?:exp|ucw|yuk|npt|rec)|(?:'+'|'.join(TAGS)+r')_exp)[\w]*)=\{', flags, re.M))),
            variables={k:v for k,v in re.findall(r'^\s*(ac_(?:ucw|pwi)_\w+)=([^\s{}]+)', variables, re.M)})
    result['global_flags'] = sorted(set(re.findall(r'^\s*(ac_(?:ucw|sp)_\w+)=\{', section(text, 'flags', 0), re.M)))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('save', type=Path)
    parser.add_argument('--coverage', required=True, help='Describe natural, shortcut or fixture provenance honestly.')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(capture(args.save, args.coverage), indent=2)+'\n', encoding='utf-8')
    print('Recorded campaign checkpoint:', args.output)
