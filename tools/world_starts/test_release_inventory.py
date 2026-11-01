"""Literal release inventory must retain scalar operations and short callers."""
import sys
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from release_inventory import report,walk,parse


class ReleaseInventoryTests(unittest.TestCase):
    def test_scalar_and_block_operations_are_both_visited(self):
        nodes=list(walk(parse('REC = { transfer_state = 345 load_oob = "REC_land" } country_event = recta.1 country_event = { id = recta.1 }')))
        self.assertIn(('transfer_state','345'),nodes)
        self.assertIn(('load_oob','"REC_land"'),nodes)
        self.assertIn(('country_event','recta.1'),nodes)
        self.assertIn(('id','recta.1'),nodes)

    def test_actual_inherited_entry_scalars_and_dispatches_are_recorded(self):
        rows={row['tag']:row for row in report()['countries']}
        aww={row['event']:row for row in rows['AWW']['entry_events']}
        self.assertEqual([272],aww['awwnb.1']['transferred_states'])
        self.assertEqual(['BLK'],aww['awwnb.1']['inherited_technology_from'])
        self.assertEqual(['AWW_land'],aww['awwnb.2']['direct_force_loads'])
        rec=rows['REC']['entry_events'][0]
        self.assertEqual([293,300,316,345],rec['transferred_states'])
        self.assertEqual(['REC_land'],rec['direct_force_loads'])
        self.assertIn('events/Belka.txt',rec['literal_callers'])
        self.assertTrue(rows['SBK']['other_observed_entry_scopes'])


if __name__=='__main__':unittest.main(verbosity=2)
