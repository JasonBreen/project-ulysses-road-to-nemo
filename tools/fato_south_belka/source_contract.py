"""Protect inherited owners and retain read-only installed syntax provenance."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
PROTECTED=(
 'history/countries/FAT - FATO.txt','history/countries/SBK - South Belka.txt',
 'common/characters/FAT.txt','common/characters/ac_starting_governments.txt',
 'events/South_Belka.txt','events/Belka.txt','events/ac_continuation.txt',
 'common/on_actions/ac_on_actions.txt','common/on_actions/ac_release_foundations.txt',
 'common/scripted_effects/ac_release_foundations.txt','common/scripted_effects/ac_release_maintenance.txt',
 'common/scripted_effects/ac_pwi.txt','events/ac_pwi.txt',
 'common/decisions/BLK_decisions.txt','common/ideas/south_belka.txt',
)
PRIMARY=('documentation/effects_documentation.md','documentation/triggers_documentation.md',
 'common/on_actions/_documentation.md','common/decisions/AST.txt','events/AAT_Denmark.txt')
def digest(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()

# Keep engine_contract.json's original fifteen captures. Only this exact,
# separately reviewed release-owner revision is permitted in their composition.
# It retires automatic production-line purchases; no national caller edits it.
REVIEWED_RELEASE_UPDATE=dict(
    path='common/scripted_effects/ac_release_maintenance.txt',
    original_sha256='b73a36358dbcd17f41719c127302afac16c3fdb056668e043bcdc2c284e1dce0',
    reviewed_sha256='1bd93b4d785649d031620ac749b96c9f31d4aa96d5a56ed516dd5ade6b73d575',
    reviewed_commit='882c53e85d1c8f5eb4b004404b55677bb3c0b29f',
    tested_source='51622f4d72c6e1c497156ce1dd7fed881723e3f0',
    previous_reviewed_sha256='837d9946a1a72c93c67107f9243fe65ac1a6a2ea0ec1b133dbc7033fa867d67a',
    previous_reviewed_commit='45da6a51393edd6b909f5bb45930e09d0c1350e5',
)

# The 1991 history-data cleanup removes FAT Hugo Havel's literal ``xxx``
# portrait reference without changing the character, leader role or owning
# file. Keep the original owner capture above and admit only that exact
# reviewed byte transition; arbitrary FAT character edits must still fail.
REVIEWED_FAT_CHARACTER_UPDATE=dict(
    path='common/characters/FAT.txt',
    original_sha256='3e8d97162c988f77ba5ea6d6e1b385ec610d0993db33b59ab3d2a0c53022d030',
    reviewed_sha256='cf22e1cd9c62e4a6b6b2e38ae89195f136e0033e683fe99910c0f065b074e221',
    reviewed_commit='af0f15ebef470f9b5afe70dcf588977150ad2e82',
    tested_source='51622f4d72c6e1c497156ce1dd7fed881723e3f0',
)

# The same cleanup replaces Shilage's borrowed Delarus identity with a local
# generated office. The generated character owner remains protected; only the
# exact added SHI office block from the reviewed cleanup is admitted.
REVIEWED_STARTING_GOVERNMENT_UPDATE=dict(
    path='common/characters/ac_starting_governments.txt',
    original_sha256='d61bb67d26f902bf00383a83507ad132b63274b8d63db52e3b6b2fb0bb03bc5d',
    reviewed_sha256='cb96a00b5b1b060bf3031fe282d277437be5ff2b9d8d812be50b17683360c895',
    reviewed_commit='af0f15ebef470f9b5afe70dcf588977150ad2e82',
    tested_source='51622f4d72c6e1c497156ce1dd7fed881723e3f0',
)

# An earlier static repair moved the FATO grand-doctrine ids off their new_*
# spelling. Native playtest N003 (docs/evidence/native-belka-20261108/BUGS.md)
# showed the installed 1.19.4.2 definitions are new_mobile_warfare,
# new_base_strike and new_operational_integrity, so the history is back at its
# original capture and the unprefixed transition is no longer admitted.
RETIRED_FAT_DOCTRINE_UPDATE=dict(
    path='history/countries/FAT - FATO.txt',
    original_sha256='bf7b3af6547329c4d6c64e27279b24f4699eccc13f0f64cea5659c4006ad127f',
    retired_sha256='91cfdccce93f611c5d8a546977db03b7179dccaa0fd5d553ea4b937727b80a88',
    doctrine_ids=('new_mobile_warfare','new_base_strike','new_operational_integrity'),
)

# PR #71 changes only four Belkan outcome hooks. Retain the captured version,
# pin the reviewed file separately, and require the independent ordered-event
# restoration proof rather than approving arbitrary event-file recaptures.
REVIEWED_BELKAN_OUTCOME_UPDATE=dict(
    path='events/Belka.txt',
    original_sha256='b41096b5b6a7733d1b69d1fb92eea5d772033110795a43fabef9c1d4e2321ee5',
    reviewed_sha256='911f06d49e0e32ca6c116c5aaa7e3f43edff84e9d8bb381607cbbdc04d213cef',
    reviewed_commit='47328d73450a262b28e066b72b6ea167fbcfd4bf',
    tested_source='ad004bb3dc34a9a90392dae0582dd5a9d4c5620e',
)


# The 1991 focus-screen fix adds one mark_focus_tree_layout_dirty line to
# ac_pwi_start so the aftermath branch, now hidden by allow_branch until the
# aftermath begins, appears when it starts. Pin only that byte transition.
REVIEWED_PWI_LAYOUT_UPDATE=dict(
    path='common/scripted_effects/ac_pwi.txt',
    original_sha256='06449b2ad9a9a02924fab2066e9ea73bc808b73ab1e500ef91c1e705ce2a84e3',
    reviewed_sha256='e64c3c2004a6391ef88286552a7fba3073c67afdd196531684327430ee0566d4',
)

def validate_reviewed_belkan_outcomes(data):
    for directory in (ROOT/'tools',ROOT/'tools/usea_expansion'):
        if str(directory)not in sys.path:sys.path.append(str(directory))
    from release_foundations.event_contract import validate_file
    original=json.loads((ROOT/'tools/release_foundations/event_inputs.json').read_text())['files']['events/Belka.txt']
    validate_file(original,data.decode('utf-8-sig'),'events/Belka.txt')


def validate_protected(path,expected,data):
    actual=digest(data)
    if actual==expected:return 'original'
    update=REVIEWED_BELKAN_OUTCOME_UPDATE
    if path==update['path'] and expected==update['original_sha256'] and actual==update['reviewed_sha256']:
        validate_reviewed_belkan_outcomes(data)
        return 'reviewed-belkan-outcome-owner'
    for disposition,update in (
            ('reviewed-release-owner',REVIEWED_RELEASE_UPDATE),
            ('reviewed-fat-character-owner',REVIEWED_FAT_CHARACTER_UPDATE),
            ('reviewed-starting-government-owner',REVIEWED_STARTING_GOVERNMENT_UPDATE),
            ('reviewed-pwi-layout-refresh',REVIEWED_PWI_LAYOUT_UPDATE)):
        if (path==update['path'] and expected==update['original_sha256']
                and actual==update['reviewed_sha256']):return disposition
    raise ValueError('Inherited owner changed: '+path)

# PR #84 commit 5daf9cafdb17fb39b489ba6ec90153cbbbf46fe3 assigns only
# these two countries to their actual dedicated campaign trees. Preserve the
# frozen engine_contract profile hashes and admit only regional_tree=False;
# every other field must still reconstruct the original captured row exactly.
REVIEWED_SOTOAN_TREES = {'SOA': 'ac_wc_soa_tree', 'CSO': 'ac_wc_cso_tree'}


def validate_institution_profile(row, expected):
    tag = row['tag']
    original = row
    if tag in ('FAT', 'SBK') or tag in REVIEWED_SOTOAN_TREES:
        if row.get('regional_tree') is not False:
            raise ValueError('Dedicated institution tree disposition changed: ' + tag)
        original = dict(row, regional_tree=True)
    if digest(json.dumps(original, sort_keys=True).encode()) != expected:
        raise ValueError('Inherited institution profile changed: ' + tag)


def capture(reference):
    protected={}
    for relative in PROTECTED:
        path=MOD/relative
        if not path.exists():raise ValueError('Missing protected source '+relative)
        before=subprocess.run(['git','show','HEAD:mod/2985041246/'+relative],cwd=ROOT,capture_output=True,check=True).stdout
        if digest(before)!=digest(path.read_bytes()):raise ValueError('Protected source already differs '+relative)
        protected[relative]=digest(before)
    profiles=json.loads(subprocess.run(['git','show','172b0726e0170012cc60650994ea3d3fe9c07551:tools/institutions/profiles.json'],cwd=ROOT,capture_output=True,text=True,check=True).stdout)
    return dict(schema=1,parent='172b0726e0170012cc60650994ea3d3fe9c07551',
        institution_profile_rows_sha256={r['tag']:digest(json.dumps(r,sort_keys=True).encode()) for r in profiles},
        protected_sha256=protected,primary_sources_sha256={p:digest((reference/p).read_bytes()) for p in PRIMARY},
        native_engine_reference='Installed HOI4 1.19.4.1; read-only syntax/scope evidence',
        contracts={
          'on_annex':'ROOT winner, FROM annexed country. Actual south_belka.5 retains BLK annex_country target SBK transfer_troops yes; the callback cleans only this campaign.',
          'send_equipment':'Country effect: equipment archetype, positive amount, target country. Installed AST decisions transfer infantry_equipment and artillery_equipment. Rechecked native stock movement; model selection/transit remain native pending.',
          'stock_consumption':'Negative add_equipment_to_stockpile type infantry_equipment appears in installed AAT_Denmark. Matching archetype has_equipment guard precedes each own expenditure.',
          'focus_handoff':'Public ac_pol_previous_tree_idle includes generic, regional36 and continuous selected-zero-progress guards; unknown bespoke trees fail closed.',
          'money':'Actual ac_econ_pay_programme, ac_macro_change_commitment and ac_pol_change_capacity owners execute; no private public-account stock writer.',
        },native_acceptance=False)
def validate(reference=None):
    row=json.loads((HERE/'engine_contract.json').read_text())
    for path,expected in row['protected_sha256'].items():
        validate_protected(path,expected,(MOD/path).read_bytes())
    if reference:
        for path,expected in row['primary_sources_sha256'].items():
            if digest((reference/path).read_bytes())!=expected:raise ValueError('Installed primary source differs: '+path)
    return row
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',action='store_true');p.add_argument('--reference',type=Path);a=p.parse_args()
    if a.capture:
        if a.reference is None:raise SystemExit('--capture requires a read-only --reference')
        (HERE/'engine_contract.json').write_text(json.dumps(capture(a.reference),indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Protected owner signatures and primary syntax:',len(validate(a.reference)['protected_sha256']),'captured sources with exact reviewed owner versions; native pending')
