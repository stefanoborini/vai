import unittest
from vixtk import core

class testVPoint(unittest.TestCase):
    def testVPoint(self):
        v = core.VPoint(x=4, y=5)
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 5)
        self.assertEqual(tuple(v), (4,5))

    def testSum(self):
        v1 = core.VPoint(x=4, y=5)
        v2 = core.VPoint(x=2, y=3)
        vres = v1+v2
        self.assertEqual(vres.x, 6)
        self.assertEqual(vres.y, 8)

    def testDifference(self):
        v1 = core.VPoint(x=4, y=5)
        v2 = core.VPoint(x=2, y=2)
        vres = v1-v2
        self.assertEqual(vres.x, 2)
        self.assertEqual(vres.y, 3)

    def testVPointTuple(self):
        self.assertEqual(core.VPoint.tuple.x((3,2)), 3)
        self.assertEqual(core.VPoint.tuple.y((3,2)), 2)
        self.assertEqual(core.VPoint.tuple.add((4,5), (2,3)), (6,8))
        self.assertEqual(core.VPoint.tuple.sub((4,5), (2,2)), (2,3))
