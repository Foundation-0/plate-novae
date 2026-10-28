import unittest,runpy,pathlib,tempfile,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
m=runpy.run_path(str(ROOT/'tools/recovery.py'))
class OfflineTests(unittest.TestCase):
    def test_behaviour(self):

        ps=[dict(jd=100+i,magnitude=10,series='a' if i<2 else 'b',plate_id=str(i)) for i in range(3)]
        self.assertEqual(m['classify'](ps+[ps[0]],100,13)['outcome'],'recovered')
        self.assertEqual(m['classify']([dict(p,series='a') for p in ps],100,13)['outcome'],'insufficient corroboration')
        self.assertEqual(m['classify']([],100,13)['coverage'],'no good detections')

if __name__=="__main__":unittest.main()
