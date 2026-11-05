"""Preserve the reviewed additive focus imports when a legacy owner regenerates."""
import re

MARKER = 'AC CAMPAIGNS'
PATTERN = re.compile(r'(?m)^\t# BEGIN AC CAMPAIGNS IMPORTS\n(?:\tshared_focus = \w+\n)+\t# END AC CAMPAIGNS IMPORTS\n')


def attach(text, identifiers):
    text = text.replace('\r\n', '\n')
    if text.count('# BEGIN AC CAMPAIGNS IMPORTS') != len(PATTERN.findall(text)):
        raise ValueError('Malformed campaign import block')
    text = PATTERN.sub('', text)
    # Several inherited country files contain a tree for each historical branch.
    # Preserve bytes outside the additive blocks and import into every such tree.
    masked = re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*', lambda m:' '*len(m[0]), text)
    closes=[]
    for match in re.finditer(r'\bfocus_tree\s*=\s*\{',masked):
        depth=1;cursor=match.end()
        while depth and cursor<len(masked):
            if masked[cursor]=='{':depth+=1
            elif masked[cursor]=='}':depth-=1
            cursor+=1
        if depth:raise ValueError('Unbalanced inherited focus tree')
        closes.append(cursor-1)
    if not closes:
        raise ValueError('Missing focus tree closing brace')
    block = '\t# BEGIN AC CAMPAIGNS IMPORTS\n' + ''.join('\tshared_focus = '+i+'\n' for i in identifiers) + '\t# END AC CAMPAIGNS IMPORTS\n'
    for closing in reversed(closes):text=text[:closing]+block+text[closing:]
    return text


def preserve(path, text):
    if path.exists():
        source = path.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        matches = PATTERN.findall(source)
        if matches and not PATTERN.search(text):
            return attach(text, re.findall(r'shared_focus = (\w+)', ''.join(matches)))
    return text
