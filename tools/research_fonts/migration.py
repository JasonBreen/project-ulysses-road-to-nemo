"""Pure reviewed font substitutions, with strict restoration for GUI fingerprints.

Call migrate on the immutable captured SOURCE before adding registered pages.
Remove only registered additions and their reviewed scrollbars before restore.
Neither function writes SOURCE or changes a non-font control/attribute.
"""
from __future__ import annotations

import copy
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/usea_expansion')]
from overhaul.text_structure import validate_structure
from script import parse
from research_fonts.policy import BINDINGS


def migrate(source: str) -> str:
    validate_structure(source)
    # Retain quote delimiters so assignment whitespace stops before its value.
    # Escaped quotes inside display strings are covered by the whole token.
    def hidden(match):
        token=match[0]
        if token.startswith('"'):
            return '"'+''.join('\n'if char=='\n'else' 'for char in token[1:-1])+'"'
        return ' '*len(token)
    mask=re.sub(r'"(?:\\.|[^"\\])*"|#[^\r\n]*',hidden,source)
    replacements = []
    for match in re.finditer(r'\b(?:font|buttonFont)\s*=\s*', mask, re.I):
        token = re.match(r'"(?:\\.|[^"\\])*"|[^\s{}#]+', source[match.end():])
        if token is None:
            raise ValueError('Research font assignment has no scalar value')
        old = token[0].strip('"')
        if old in BINDINGS:
            replacements.append((match.end(), match.end() + token.end(), '"' + BINDINGS[old].name + '"'))
    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]
    return source


def restore(tree, source: str):
    """Return a copy with only the reviewed migrated font fields restored.

    Reverting a font to its inherited alias is an error, not a normalization
    exemption. Unknown nodes/attributes must be removed by their actual owner
    or remain visible to the caller's unchanged whole-AST fingerprint check.
    """
    original = parse(source)
    result = copy.deepcopy(tree)

    def visit(old, current, path='gui'):
        if len(old) != len(current):
            raise ValueError('Unregistered research GUI structure at ' + path)
        for index, (before, after) in enumerate(zip(old, current)):
            key, op, value = before
            if (key, op) != tuple(after[:2]):
                raise ValueError('Research GUI attribute order changed at ' + path)
            address = path + '/' + key + '[' + str(index) + ']'
            if isinstance(value, list):
                if not isinstance(after[2], list):
                    raise ValueError('Research GUI block changed at ' + address)
                visit(value, after[2], address)
            elif key.lower() in ('font', 'buttonfont') and isinstance(value, str) and value.strip('"') in BINDINGS:
                expected = BINDINGS[value.strip('"')].name
                if not isinstance(after[2], str) or after[2].strip('"') != expected:
                    raise ValueError('Reviewed research font binding reverted or changed at ' + address)
                after[2] = value
    visit(original, result)
    return result
