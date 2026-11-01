"""New-regime office fallback executes real recruit/role/promote syntax."""
import copy,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from release_harness import World,parse,get
STATES={'AWW':272,'REC':316,'SHI':426}
CONTRACT=json.loads((HERE/'leader_contract.json').read_text())
NAMED={tag:next((government,ident) for ident,governments in row['identities'].items() for government in governments)
       for tag,row in CONTRACT['countries'].items()}
def office(tag,ident):return ident if ident.endswith('_ac_government_office') else CONTRACT['countries'][tag]['fallback']
def release(w,tag):
    w.release_action('on_startup');state=STATES[tag];w.states[state].owner=w.states[state].controller=tag;w.release_action('on_release_as_free',tag,'BLK')
    return w.countries[tag]
def promotions(w):return [n for n in w.native_log if n[0] in ('add_country_leader_role','promote_character')]
class Leaders(unittest.TestCase):
    def test_primary_routes_retain_all_three_named_identities_and_authored_roles(self):
        for tag,(government,ident) in NAMED.items():
            w=World();w.countries[tag].government=government;before=copy.deepcopy(w.character_roles[ident]);release(w,tag)
            self.assertEqual(ident,w.ruling_leader[tag]);self.assertEqual(before,w.character_roles[ident]);self.assertNotIn(tag+'_ac_release_government_office',w.character_ids[tag])
    def test_new_primary_regime_promotes_its_authored_role_over_an_unimplemented_default(self):
        for tag,(government,ident) in NAMED.items():
            w=World();w.countries[tag].government=government;w.ruling_leader[tag]='unimplemented_engine_default';release(w,tag)
            self.assertEqual(ident,w.ruling_leader[tag]);self.assertNotIn(tag+'_ac_release_government_office',w.character_ids[tag])
    def test_all_current_governments_get_existing_identity_or_a_readable_new_office_once(self):
        taxonomy=CONTRACT['subtypes']
        for tag,(original,ident) in NAMED.items():
            for government in taxonomy:
                w=World();w.countries[tag].government=government;before=copy.deepcopy(w.character_roles[ident]);release(w,tag)
                self.assertEqual(ident if government==original else office(tag,ident),w.ruling_leader[tag])
                if office(tag,ident)==ident:
                    self.assertTrue(before<=w.character_roles[ident]);self.assertIn(government,w.character_roles[ident])
                else:self.assertEqual(before,w.character_roles[ident])
                first=copy.deepcopy(promotions(w));w.run('ac_release_'+tag+'_ensure_ruling_office',tag);w.run('ac_release_'+tag+'_physical_registration',tag);w.release_action('on_monthly',tag)
                self.assertEqual(first,promotions(w))
    def test_adoption_and_rerelease_never_replace_saved_leader_or_duplicate_roles(self):
        w=World(new=False);w.states[316].owner=w.states[316].controller='REC';w.ruling_leader['REC']='saved_officeholder';w.release_action('on_startup');w.run('ac_release_REC_ensure_ruling_office','REC')
        self.assertEqual('saved_officeholder',w.ruling_leader['REC']);self.assertEqual([],promotions(w))
        w=World();w.countries['REC'].government='fascism';release(w,'REC');before=copy.deepcopy(promotions(w));leader=w.ruling_leader['REC'];w.release_action('on_annex','BLK','REC')
        w.states[316].owner=w.states[316].controller='BLK';w.states[316].owner=w.states[316].controller='REC';w.release_action('on_release_as_free','REC','BLK');w.run('ac_release_REC_ensure_ruling_office','REC')
        self.assertEqual(leader,w.ruling_leader['REC']);self.assertEqual(before,promotions(w))
    def test_another_existing_authored_ruler_is_not_displaced(self):
        w=World();w.countries['REC'].government='democratic';w.character_ids['REC'].add('FCU_robert_sinclair');w.ruling_leader['REC']='FCU_robert_sinclair';release(w,'REC')
        self.assertEqual('FCU_robert_sinclair',w.ruling_leader['REC']);self.assertNotIn('REC_ac_release_government_office',w.character_ids['REC'])
    def test_shared_clarkson_identity_is_not_stolen_or_duplicated(self):
        w=World();w.character_ids['DEL'].add('DEL_artur_clarkson');w.ruling_leader['DEL']='DEL_artur_clarkson';release(w,'SHI')
        self.assertIn('DEL_artur_clarkson',w.character_ids['DEL']);self.assertNotIn('DEL_artur_clarkson',w.character_ids['SHI']);self.assertEqual('SHI_ac_government_office',w.ruling_leader['SHI'])
        self.assertEqual('DEL_artur_clarkson',w.ruling_leader['DEL'])
    def test_office_roles_use_current_taxonomy_and_local_emblem_art_without_biographies(self):
        data=json.loads((HERE/'leader_contract.json').read_text());self.assertEqual(3,len(data['countries']));source=(HERE/'leader_contract.json').read_text()
        for tag,row in data['countries'].items():
            self.assertEqual(tag+'_ac_release_government_office',row['fallback']);self.assertTrue(row['identities'])
        primary=json.loads((HERE/'engine_hooks.json').read_text());self.assertIn('documentation/effects_documentation.md',primary['primary_sources_sha256'])
        effects=(HERE/'leaders.py').read_text();self.assertNotIn('set_country_leader_ideology',effects);self.assertNotIn('set_popularities',effects)
if __name__=='__main__':unittest.main(verbosity=2)
