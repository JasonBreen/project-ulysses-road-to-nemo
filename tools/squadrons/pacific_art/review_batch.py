"""Record individual source review notes without changing original image bytes."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / 'plan.json').read_text())
rows = {row['id']: row for row in plan['assets']}
reviews = json.loads(Path(sys.argv[1]).read_text())
for key, review in reviews.items():
    p = HERE.parent / 'sources' / rows[key]['file']
    info = json.loads(p.with_suffix('.json').read_text())
    info.update(visual_reviewed=True, review=review)
    p.with_suffix('.json').write_bytes((json.dumps(info, indent=2) + '\n').encode())
    rows[key]['status'] = 'original master visually reviewed'
(HERE / 'plan.json').write_bytes((json.dumps(plan, indent=2) + '\n').encode())
