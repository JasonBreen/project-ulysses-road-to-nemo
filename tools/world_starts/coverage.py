"""Combined active-world source coverage, with owner and release gaps preserved.

This reads selected country-history/OOB branches. It is not an engine, logistics
throughput simulation, or a universal sustainable-start acceptance certificate.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from inventory import inspect
from legacy_foundation import binding_gaps


def report(require_integrated=False):
    def load(relative):return json.loads((ROOT/relative).read_text())
    sources={
        'world_starts':set(load('tools/world_starts/profiles.json')['countries']),
        'world_foundation':set(load('tools/world_foundation/profiles.json')['countries']),
        'anea':set(load('tools/anea/foundation.json')['countries']),
        'world_legacy':set(load('tools/world_starts/legacy_profiles.json')['countries']),
    }
    counts=Counter(tag for tags in sources.values() for tag in tags)
    baseline=load('tools/world_starts/baseline_inventory.json')
    active={row['tag'] for row in baseline['countries'] if row['classification']=='active'}
    if set(counts)!=active or any(count!=1 for count in counts.values()):
        raise ValueError('Physical owner partition is missing, overlapping or extends into an emergent/placeholder start')
    registry={row['tag']:row for row in load('tools/world_foundation/country_registry.json')['countries']}
    inventory=inspect();rows=[];gaps=binding_gaps()
    if require_integrated and gaps:raise ValueError('; '.join(gaps))
    for row in inventory['countries']:
        if row['classification']!='active':continue
        selected=[]
        for case in row['cases']:
            rosters=case['rosters'];names=[r['file'] for r in rosters]
            if case['errors'] or len(names)!=len(set(names)) or not case['divisions']:
                raise ValueError('Missing, repeated or invalid selected starting roster: '+row['tag'])
            placements=[r for r in rosters if r.get('invalid_placements')]
            if placements:raise ValueError('Selected force deployment outside owned territory: '+row['tag'])
            selected.append(dict(bba=case['bba'],mtg=case['mtg'],rosters=names,
                divisions=case['divisions'],planes=case['planes'],ships=case['ships'],
                requested_production=dict(sum((Counter(r['production']) for r in rosters),Counter()))))
        for case in row['other_start_contexts']:
            names=[r['file'] for r in case['rosters']]
            if not case['divisions'] or len(names)!=len(set(names)) or any(r.get('error') or r.get('invalid_placements') for r in case['rosters']):
                raise ValueError('Invalid selected FATO human/AI context')
        registered=registry[row['tag']]
        rows.append(dict(tag=row['tag'],owner=next(owner for owner,tags in sources.items() if row['tag'] in tags),
            base_BBA_MTG_cases=selected,additional_FATO_contexts=row['other_start_contexts'],
            source_gaps=registered['source_gaps'],status=registered['support_status'],
            native_acceptance=registered['native_acceptance']))
    if {row['tag'] for row in rows}!=active or len(rows)!=len(active):
        raise ValueError('Candidate registry no longer represents the exact 61 active starting countries')
    return dict(schema=1,active_countries=len(active),owner_counts={owner:len(tags) for owner,tags in sources.items()},
        base_BBA_MTG_selected_cases=sum(len(row['base_BBA_MTG_cases']) for row in rows),
        external_owner_binding_gaps=gaps,universal_sustainable_start_acceptance=False,
        preserved_source_liabilities=['UST inherited personnel/reinforcement debt',
            'BLK state 309 seven-province sealed inherited component has no mandatory starting target; universal geographic connectivity is not claimed'],
        extra_DLC_status='NSB/La Resistance cases and release gates belong to each force owner; the four base projections alone do not establish them.',
        exclusions=[dict(tag=row['tag'],classification=row['classification']) for row in baseline['countries'] if row['classification']!='active'],
        evidence='Actual selected source histories and rosters; native parsing, mission availability, supply/fuel delivery, AI growth and save/reload remain untested.',
        countries=rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--require-integrated-owner',action='store_true');args=parser.parse_args()
    data=report(args.require_integrated_owner);text=json.dumps(data,indent=2)+'\n';path=HERE/'coverage.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Combined active-world coverage report differs')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('Active physical owners:',data['owner_counts'],'; actual base source cases:',data['base_BBA_MTG_selected_cases'])
    print('External force binding:',data['external_owner_binding_gaps'] or 'exact local receipts match')
    print('Universal sustainable-start acceptance remains false; explicit source/DLC/native gates are retained.')
