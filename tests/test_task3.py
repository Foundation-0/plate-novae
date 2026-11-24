import unittest,runpy,pathlib,tempfile,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
m=runpy.run_path(str(ROOT/'tools/null_rates.py'))
class OfflineTests(unittest.TestCase):
    def test_behaviour(self):

        self.assertIsNone(m['summarize']([])['groups_per_thousand_plates'])
        r=m['summarize']([dict(star_id='a',plates=100,passing_groups=1),dict(star_id='b',plates=100,passing_groups=0)])
        self.assertEqual(r['flagged_star_fraction'],.5);self.assertEqual(r['groups_per_thousand_plates'],5)
        with self.assertRaises(ValueError):m['summarize']([dict(star_id='a',plates=0,passing_groups=1)])

if __name__=="__main__":unittest.main()
