import unittest
from vixtk import core

class testVPoint(unittest.TestCase):
    def testVPoint(self):
        v = core.VPoint(x=4, y=5)
        self.assertEqual(v.x(), 4)
        self.assertEqual(v.y(), 5)
        self.assertEqual(tuple(v), (4,5))

    def testSum(self):
        v1 = core.VPoint(x=4, y=5)
        v2 = core.VPoint(x=2, y=3)
        vres = v1+v2
        self.assertEqual(vres.x(), 6)
        self.assertEqual(vres.y(), 8)
    def testDifference(self):
        v1 = core.VPoint(x=4, y=5)
        v2 = core.VPoint(x=2, y=2)
        vres = v1-v2
        self.assertEqual(vres.x(), 2)
        self.assertEqual(vres.y(), 3)

    def testVPoint(self):
        p = core.VPoint(3,2)

        self.assertEqual(p.x(), 3)
        self.assertEqual(p.y(), 2)

        self.assertEqual(list(p), [3,2])
