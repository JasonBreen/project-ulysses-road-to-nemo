"""The bespoke and anti-filler gate for national-depth specs.

These rules fail a build; they are what makes "bespoke" checkable. Thresholds
come from the approved plan (6 November 2026).
"""
from collections import Counter
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import spec as S  # noqa: E402

MIN_OWN = 120
MIN_BRANCHES = 10
MIN_EXCLUSIVE_SHARE = 0.20
MAX_SIGNATURE_REPEATS = 3
MAX_CURRENCY_SHARE = 0.10
MIN_DEFINED_SHARE = 0.60
MIN_DESC_WORDS = 45
MAX_SIMILARITY = 0.30
LATEST_FIRST_ERA = 2002          # a minor must still have open non-exclusive work after this year
CAMPAIGN_SHAPE = ('register', 'policy_a', 'policy_b', 'operations', 'review', 'settlement')


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def shingles(text, masks=()):
    tokens = [w for w in words(text) if w not in masks]
    return {tuple(tokens[i:i + 5]) for i in range(max(0, len(tokens) - 4))}


def similarity(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def signature(focus):
    return tuple(sorted(type(r).__name__ + ':' + repr(sorted(vars(r).items())) for r in focus.reward))


def branch_shape(branch):
    """The prerequisite structure and cost pattern, independent of names."""
    order = {f.key: i for i, f in enumerate(branch.focuses)}
    return tuple((tuple(sorted(order[p] for p in f.after if p in order)), tuple(sorted(order[p] for p in f.after_any if p in order)),
                  f.cost, bool(f.exclusive)) for f in branch.focuses)


def lint(module, others=(), strict=True):
    """Return a list of problems. `others` are (name, description) pairs from every other spec and the mod."""
    m, c = module, module.COUNTRY
    problems = []

    def check(condition, message):
        if not condition:
            problems.append('%s: %s' % (c.tag, message))
    focuses = [f for b in m.BRANCHES for f in b.focuses]
    keys = {f.key for f in focuses}
    if strict:
        check(len(focuses) >= MIN_OWN, '%d own focuses; at least %d required' % (len(focuses), MIN_OWN))
        check(len(m.BRANCHES) >= MIN_BRANCHES, '%d branches; at least %d required' % (len(m.BRANCHES), MIN_BRANCHES))
    exclusive = {f.key for f in focuses if f.exclusive} | {k for f in focuses for k in f.exclusive}
    check(len(exclusive) >= MIN_EXCLUSIVE_SHARE * len(focuses), 'only %d focuses in mutually exclusive groups' % len(exclusive))
    shapes = Counter(branch_shape(b) for b in m.BRANCHES)
    check(max(shapes.values()) <= 2, 'a branch shape repeats more than twice')
    for b in m.BRANCHES:
        check(tuple(f.key.rsplit('_', 1)[-1] for f in b.focuses[-6:]) != CAMPAIGN_SHAPE, b.key + ': the 6-node campaign shape')
    signatures = Counter(signature(f) for f in focuses if f.reward)
    worst = signatures.most_common(1)
    check(not worst or worst[0][1] <= MAX_SIGNATURE_REPEATS, 'one reward signature appears %d times' % (worst[0][1] if worst else 0))
    with_reward = [f for f in focuses if f.reward]
    currency = [f for f in with_reward if all(isinstance(r, S.CURRENCY) for r in f.reward)]
    defined = [f for f in focuses if any(isinstance(r, S.DEFINED) for r in f.reward)]
    check(len(currency) <= MAX_CURRENCY_SHARE * len(focuses), '%d focuses grant only bare currency' % len(currency))
    check(len(defined) >= MIN_DEFINED_SHARE * len(focuses), 'only %d focuses touch a defined idea, flag, event, decision or state' % len(defined))
    check(all(f.reward for f in focuses), 'a focus has no reward: ' + ', '.join(f.key for f in focuses if not f.reward)[:200])
    set_flags = {r.name for f in focuses for r in f.reward if isinstance(r, S.Flag)} | \
                {r.name for e in m.EVENTS for o in e.options for r in o.effects if isinstance(r, S.Flag)}
    read_flags = {r.name for f in focuses for r in f.requires if isinstance(r, (S.HasFlag, S.NotFlag))}
    check(set_flags <= read_flags, 'flags set but never read: ' + ', '.join(sorted(set_flags - read_flags)))
    check(read_flags <= set_flags, 'flags read but never set: ' + ', '.join(sorted(read_flags - set_flags)))
    titles = Counter(f.title.lower() for f in focuses)
    check(max(titles.values()) == 1, 'duplicate titles within the tree')
    other_titles = {t.lower() for t, _ in others}
    check(not any(f.title.lower() in other_titles for f in focuses), 'titles already used elsewhere: ' +
          ', '.join(f.title for f in focuses if f.title.lower() in other_titles)[:200])
    short = [f.key for f in focuses if len(words(f.desc)) < MIN_DESC_WORDS]
    check(not short, '%d descriptions under %d words: %s' % (len(short), MIN_DESC_WORDS, ', '.join(short[:6])))
    masks = set(words(c.name)) | {c.tag.lower()}
    mine = [(f.key, shingles(f.desc, masks)) for f in focuses]
    theirs = [shingles(d, masks) for _, d in others]
    for i, (key, sh) in enumerate(mine):
        for other_key, osh in mine[i + 1:]:
            if similarity(sh, osh) >= MAX_SIMILARITY:
                problems.append('%s: descriptions of %s and %s are too similar' % (c.tag, key, other_key))
        if any(similarity(sh, osh) >= MAX_SIMILARITY for osh in theirs):
            problems.append('%s: description of %s repeats text from another tree' % (c.tag, key))
    if strict:
        late = [f for b in m.BRANCHES if b.era >= LATEST_FIRST_ERA for f in b.focuses if not f.exclusive]
        check(late, 'no non-exclusive focus opens in %d or later' % LATEST_FIRST_ERA)
    del keys
    return problems
