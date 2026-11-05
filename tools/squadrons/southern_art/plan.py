"""Art plan for the southern stories and the Anean continuations.

Thirty-two original masters: for Aurelia and Leasath, four cast portraits,
eight scenes (core slots 1-5, ending slots 6/7/8) and one loading screen
each; for the Emmerian and Estovakian epilogues, three scenes each (their
portraits are the original masters). Subjects come from the story metadata;
prompts use the exact Pacific templates (tools/squadrons/pacific_art/plan.json).

Every master starts ``awaiting generation``. This session has no image
generator; masters are generated in a session that has one (or supplied by
the user), recorded with their raw SHA-256 and reviewed through the Pacific
intake and review steps, and only then can a story be admitted. No placeholder
is ever packaged. ``--check`` keeps plan.json equal to the metadata and
refuses an admitted story whose masters are not all reviewed and present.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
STORY = HERE.parent
sys.path[:0] = [str(STORY / 'southern'), str(STORY / 'anean_epilogue')]
import story_contract  # noqa: E402
import epilogue_contract  # noqa: E402

NATIONALITY = {'AUR': 'Aurelian', 'LEA': 'Leasathian', 'EMM': 'Emmerian', 'EVA': 'Estovakian'}
AWAITING = 'awaiting generation'
REVIEWED = 'original master visually reviewed'
PORTRAIT = ('Use case: illustration-story. Create ONE original painted-realistic editorial character portrait for Project Ulysses, a fictional '
            'Strangereal story. This is original supporting cast, never an existing Ace Combat character or a national government leader. '
            'Character: {name}, {nation} {role}. Appearance and mood: {appearance} Head and shoulders, gently three-quarter toward the viewer, '
            'entire hair and head comfortably inside the frame with generous headroom and shoulder margin for later portrait-card crops. '
            'Portrait aspect 4:5. Realistic natural skin, individual facial features and believable eyes, subtle painted texture and practical '
            'cloth grain. Soft natural cool daylight and restrained navy/cyan surroundings; simple blurred service-room background without a '
            'recognizable location. Plain practical 1990s clothing, no rank or name patches. No hands, weapon, permanent injury, text, lettering, '
            'numbers, logo, flag, insignia, emblem, signature, watermark, yellow paint or overlay, UI border, collage, glowing cyberpunk lights '
            'or WWII costume. Fill the full image with the portrait and background; one person only.')
OPENING = ('Use case: illustration-story. Create ONE original wide 16:9 painted-realistic aviation editorial illustration for an authored '
           'Strangereal supporting-cast story. Subtle visible painted texture, realistic practical interiors and natural skin/light, restrained '
           'navy/cyan cloth and architecture. Grounded everyday service work in an anonymous place, conventional 1991-2020 machinery, no '
           'recognizable aircraft type or Earth landmark. ')
SCENE_FIT = ('Make the important narrative subjects readable in the central 60 percent width and central 75 percent height for a later 200x160 '
             'event-card crop. Compose distinct depth and light, not a collage or game screenshot. Fill the whole frame; no borders, '
             'letterboxing or UI. Scene: ')
LOADING_FIT = ('Make the important narrative subjects readable in the central 50 percent width and middle 55 percent height for a conservative '
               '3440:1440 center-cover loading crop. Compose distinct depth and light, not a collage or game screenshot. Fill the whole frame; '
               'no borders, letterboxing or UI. This is a separately composed full-bleed cinematic loading-screen master, never a widened event '
               'crop. Keep whole important aircraft, vehicle and worker silhouettes inside the crop-safe middle height. Calm low-detail '
               'foreground/sky may carry later loading text, but paint no text now. ')
CLOSING = (' No readable text, lettering, numerals, pseudo-writing, insignia, badge, seal, logo, flag, watermark, signature, yellow stripe, yellow '
           'overlay, strategic weapon, airborne aircraft, battle, explosion, blood, grave, corpse, named national leader or established Ace Combat '
           'cameo. All papers, labels, boards, screens and clothing are unmarked. Do not assert a national victory, peace, defeat, surrender, '
           'occupation or compulsory historical outcome. Natural soft warm lamps are allowed; no artificial yellow graphic artifacts.')
ENDINGS = {'6': 'trusted', '7': 'compromised', '8': 'fractured'}


def sentence(text):
    text = text.strip()
    return text if text.endswith('.') else text + '.'


def asset(ident, tag, kind, file, prompt, **extra):
    return dict(id=ident, tag=tag, kind=kind, file=file, **extra, prompt=prompt, transparent_background=False,
                generation_references=[], status=AWAITING, sha256=None)


def plan():
    assets = []
    for row in story_contract.stories():
        tag, low = row['tag'], row['tag'].lower()
        for person in row['cast']:
            assets.append(asset(person['id'], tag, 'original story-cast portrait', 'portraits/' + person['id'] + '.png',
                                PORTRAIT.format(name=person['name'], nation=NATIONALITY[tag], role=person['role'].lower(),
                                                appearance=sentence(person['portrait']))))
        for slot in sorted(row['scene_subjects'], key=int):
            scene = row['scene_subjects'][slot]
            title = tag + ' ' + slot + ' -- ' + sentence(scene['title'])
            assets.append(asset(low + '_scene_' + slot, tag, 'original story narrative scene', 'scenes/' + low + '_scene_' + slot + '.png',
                                OPENING + SCENE_FIT + title + ' ' + sentence(scene['subject']) + CLOSING,
                                title=title, subject=scene['subject'], chapters=row['chapters_by_slot'].get(slot, []),
                                ending=ENDINGS.get(slot)))
        title = tag + ' loading -- ' + sentence(row['title'])
        assets.append(asset(low + '_loading', tag, 'original independent loading screen', 'loading/' + low + '_loading.png',
                            OPENING + LOADING_FIT + title + ' ' + sentence(row['loading_subject']) + CLOSING,
                            title=title, subject=row['loading_subject']))
    for row in epilogue_contract.epilogues():
        tag, low = row['tag'], row['tag'].lower()
        for slot in sorted(row['scene_subjects'], key=int):
            scene = row['scene_subjects'][slot]
            title = tag + ' epilogue ' + slot + ' -- ' + sentence(scene['title'])
            assets.append(asset(low + '_epilogue_scene_' + slot, tag, 'original epilogue narrative scene',
                                'epilogue/' + low + '_epilogue_scene_' + slot + '.png',
                                OPENING + SCENE_FIT + title + ' ' + sentence(scene['subject']) + CLOSING,
                                title=title, subject=scene['subject'], chapters=row['chapters_by_slot'][slot], ending=None))
    return dict(schema=1, source_layer='Original supporting fiction for the southern stories and Anean continuations; not national leaders or official biography',
                prompt_templates='tools/squadrons/pacific_art/plan.json (exact Pacific portrait, scene and loading templates)',
                portrait_crop='Original 4:5 master; 156x210 full-height contain, as the Pacific portraits.',
                scenes_crop='Wide 16:9 masters; subjects in the central 60 percent width for the 200x160 event crop.',
                loading_crop='Independent 16:9 masters; subjects in the middle 55 percent height for a 3440:1440 center cover.',
                generator_available_in_authoring_session=False, assets=assets)


def preserve_review(old, new):
    """Recorded hashes and review states survive regeneration while the prompt is unchanged."""
    previous = {a['id']: a for a in old.get('assets', [])}
    for item in new['assets']:
        before = previous.get(item['id'])
        if before and before['prompt'] == item['prompt']:
            item['status'], item['sha256'] = before['status'], before['sha256']
            item['generation_references'] = before['generation_references']
    return new


def admitted_problems(data):
    problems = []
    admitted = set(story_contract.ADMITTED) | set(epilogue_contract.ADMITTED)
    for item in data['assets']:
        path = HERE / item['file']
        if item['status'] == REVIEWED:
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                problems.append('Reviewed master missing or changed: ' + item['file'])
        elif item['tag'] in admitted:
            problems.append('Admitted story has an unreviewed master: ' + item['id'])
        elif path.exists():
            problems.append('Unreviewed master file present without a record: ' + item['file'])
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = HERE / 'plan.json'
    old = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    data = preserve_review(old, plan())
    text = json.dumps(data, indent=2) + '\n'
    if args.check:
        if not path.exists() or path.read_text(encoding='utf-8').replace('\r\n', '\n') != text:
            raise SystemExit('Stale southern art plan')
        problems = admitted_problems(data)
        if problems:
            raise SystemExit('\n'.join(problems))
    else:
        path.write_text(text, encoding='utf-8', newline='\n')
    counts = {}
    for item in data['assets']:
        counts[item['status']] = counts.get(item['status'], 0) + 1
    print(str(len(data['assets'])) + ' planned masters: ' + ', '.join(f'{v} {k}' for k, v in sorted(counts.items())))


if __name__ == '__main__':
    main()
