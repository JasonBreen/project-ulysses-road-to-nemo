"""Explicit original-fit versus composed-style screen acceptance; no broad gate."""
import unittest
from event_picture_fit.run_checks import screen_matches,require_screen_source,ORIGINAL_FAILURES
class EventRunner(unittest.TestCase):
    def fixture(self,failures=None,profile=True):
        return {'gate_covered_screens':{'eventwindow.gui':{'failures':failures or []},'countrydecisionview.gui':{'failures':[]}},
            'dlc_archive_coverage':{'status':'explicit_profile_inspected' if profile else 'activation_unspecified_inventory_only','selected_descriptors':[]},
            'summary':{'engine_fallback':690,'missing_definition':137},'parse_failures':[{}]*12}
    def test_current_source_requires_exact_registered_style_owner(self):
        require_screen_source('event-style')
        with self.assertRaisesRegex(ValueError,'original unstyled GUI'):require_screen_source('original-fit')
        with self.assertRaisesRegex(ValueError,'Unknown'):require_screen_source('auto-accept')
    def test_current_style_zero_profile_scoped_screen_contract(self):
        self.assertTrue(screen_matches(self.fixture(),0,'event-style'))
        self.assertFalse(screen_matches(self.fixture(profile=False),0,'event-style'))
        report=self.fixture();report['dlc_archive_coverage']['selected_descriptors']=['dlc/unreviewed.dlc']
        self.assertFalse(screen_matches(report,0,'event-style'))
    def test_any_screen_failure_missing_screen_or_wrong_exit_rejects(self):
        for name in ('eventwindow.gui','countrydecisionview.gui'):
            report=self.fixture();report['gate_covered_screens'][name]['failures']=['sprite:unexpected:engine_fallback']
            self.assertFalse(screen_matches(report,0,'event-style'))
            del report['gate_covered_screens'][name];self.assertFalse(screen_matches(report,0,'event-style'))
        self.assertFalse(screen_matches(self.fixture(),1,'event-style'))
    def test_historical15_contract_is_exact_and_never_mistaken_for_style(self):
        report=self.fixture(list(ORIGINAL_FAILURES),profile=False)
        self.assertTrue(screen_matches(report,1,'original-fit'));self.assertFalse(screen_matches(report,1,'event-style'))
        self.assertFalse(screen_matches(report,0,'original-fit'))
        for failures in (ORIGINAL_FAILURES[:-1],ORIGINAL_FAILURES+['sprite:unreviewed:engine_fallback'],ORIGINAL_FAILURES+[ORIGINAL_FAILURES[0]]):
            self.assertFalse(screen_matches(self.fixture(failures),1,'original-fit'))
    def test_unknown_mode_rejected_and_global_failures_remain_outside_bounded_pass(self):
        self.assertTrue(screen_matches(self.fixture(),0,'event-style'))
        with self.assertRaises(ValueError):screen_matches(self.fixture(),0,'implicit-global-closure')
if __name__=='__main__':unittest.main(verbosity=2)
