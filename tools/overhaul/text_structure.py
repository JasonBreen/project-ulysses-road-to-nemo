"""Validate braces and quoted tokens before the supported Paradox AST reader.

This is lexical validation, not a claim to implement every engine grammar or
validate native rendering. Braces in comments and escaped strings are data.
"""


def validate_structure(text):
    opened = []
    quoted = False
    escaped = False
    comment = False
    quote_line = None
    line = 1
    for character in text:
        if comment:
            if character == "\n":
                comment = False
                line += 1
            continue
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            if character == "\n":
                line += 1
            continue
        if character == "#":
            comment = True
        elif character == '"':
            quoted = True
            quote_line = line
        elif character == "{":
            opened.append(line)
        elif character == "}":
            if not opened:
                raise ValueError("Unexpected } at line " + str(line))
            opened.pop()
        elif character == "\n":
            line += 1
    if quoted:
        raise ValueError("Unterminated quoted token starting at line " + str(quote_line))
    if opened:
        raise ValueError("Unclosed block starting at line " + str(opened[-1]))
