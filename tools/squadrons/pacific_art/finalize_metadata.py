"""Record crop/alpha contracts without modifying any retained PNG bytes."""
import json
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'plan.json').read_text())
for asset in plan['assets']:
    path=HERE.parent/'sources'/asset['file'];record=path.with_suffix('.json');info=json.loads(record.read_text())
    with Image.open(path) as image:
        info.update(mode=image.mode,frames=1,alpha_extrema=list(image.convert('RGBA').getchannel('A').getextrema()))
    if asset['file'].startswith('portraits/'):
        info['packaging_contract']='Full-height contain at156x210; preserve complete head/hair. Never attach these original fictional story portraits to national government leaders.'
        if asset['id']=='rhea_calder':info['packaging_contract']+=' Rhea has a tight upper hair margin; never trim additional source height.'
    elif asset['file'].startswith('scenes/'):
        info['packaging_contract']='Full-source contain at200x160 retains the complete narrative action. Center-cover previews are conservative review alternatives, not universal approved replacements.'
        if asset['id'] in ('ose_scene_6','yuk_scene_8'):
            info['packaging_contract']+=' Required full fit: center-cover can discard an outer cast member or a separate departure and change the meaning.'
    else:
        info['packaging_contract']='Independent1932x814 full-bleed panoramic original. Use the reviewed center-cover treatment for1920x1080 and3440:1440; do not use a generic contain path with large navy bars. Native loading scaling remains untested.'
        info['requested_aspect']='16:9 with a conservative wider-screen safe area'
        info['returned_aspect_disposition']='Service returned a wider panorama; original retained byte-for-byte, both requested presentation ratios reviewed as separate center-cover derivatives.'
    info['evidence_tier']='Original-master and offline fit/crop review only; DDS bindings, native rendering and game integration remain separate owner gates.'
    if asset['id']=='yuk_scene_8':
        info['review']=info['review'].replace('Central event crop retains the empty board and separation; peripheral room detail is contextual.',
            'Full-source fit retains both separate departures and the empty board. Center-cover loses peripheral narrative detail and must not replace the full-fit card.')
    record.write_bytes((json.dumps(info,indent=2)+'\n').encode())
    asset['status']='original master visually reviewed'
(HERE/'plan.json').write_bytes((json.dumps(plan,indent=2)+'\n').encode())
print('Recorded26 crop/alpha/provenance contracts; selected image bytes unchanged.')
