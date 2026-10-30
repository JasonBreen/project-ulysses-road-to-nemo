"""Lossless scalar tokens and ordered blocks for GUI/GFX compatibility metadata."""
import re


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\#[^\n]*|>=|<=|!=|[{}=<>]|[^\s{}=<>]+', text)
    tokens = [t for t in tokens if not t.startswith('#')]
    pos = 0
    def block(nested=False):
        nonlocal pos
        out = []
        while pos < len(tokens):
            key = tokens[pos]; pos += 1
            if key == '}':
                if not nested: raise ValueError('Unexpected }')
                return out
            if pos >= len(tokens) or tokens[pos] not in ('=', '<', '>', '<=', '>=', '!='):
                out.append([key, None, None]); continue
            op = tokens[pos]; pos += 1
            value = tokens[pos]; pos += 1
            if value == '{': value = block(True)
            out.append([key, op, value])
        if nested: raise ValueError('Unclosed block')
        return out
    return block()


def render(nodes, depth=0):
    lines=[]
    for k,op,v in nodes:
        prefix='\t'*depth+k
        if op is None: lines.append(prefix)
        elif isinstance(v,list): lines.extend([prefix+' '+op+' {',render(v,depth+1),'\t'*depth+'}'])
        else: lines.append(prefix+' '+op+' '+v)
    return '\n'.join(lines)


def get(nodes,key,default=None):
    return next((v for k,_,v in nodes if k.lower()==key.lower()),default)


def setv(nodes,key,value):
    for node in nodes:
        if node[0].lower()==key.lower(): node[2]=value;return
    nodes.append([key,'=',value])


def walk(nodes):
    for key,op,value in nodes:
        if isinstance(value,list):
            yield key,value
            yield from walk(value)


def xy(x,y):return [['x','=',str(x)],['y','=',str(y)]]
def size(w,h):return [['width','=',str(w)],['height','=',str(h)]]
