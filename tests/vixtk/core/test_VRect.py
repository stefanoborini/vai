import unittest
from vixtk import core

class TestVRect(unittest.TestCase):
    def testVRect(self):
        r = core.VRect((2,3), (4,5))
        self.assertIsInstance(r.size(), core.VSize)
        self.assertIsInstance(r.topLeft(), core.VPoint)

    def testVRectIsNull(self):
        r = core.VRect((2,3), (4,5))
        self.assertFalse(r.isNull())

        r = core.VRect((2,3), (0,0))
        self.assertTrue(r.isNull())

    def testVRectIntersects(self):
        #self.assertTrue(core.VRect((2,3), (4,5)).intersects(core.VRect((2,3), (4,5))))
        #self.assertFalse(core.VRect((2,3), (4,5)).intersects(core.VRect((2,3), (0,0))))
        #self.assertFalse(core.VRect((2,3), (4,5)).intersects(core.VRect((0,0), (2,3))))
        #self.assertTrue(core.VRect((2,3), (4,5)).intersects(core.VRect((3,4), (1,1))))
        #self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((1,2), (1,1))))
        #self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((3,4), (1,1))))
        #self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((3,3), (1,1))))
        #self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((4,4), (1,1))))

        self.assertTrue(core.VRect((0,0), (18,1)).intersects(core.VRect((4,0), (142,40))))
    def testVRectDimensionality(self):
        r = core.VRect((2,3), (4,5))

        self.assertEqual(r.x(), 2)
        self.assertEqual(r.y(), 3)
        self.assertEqual(r.width(), 4)
        self.assertEqual(r.height(), 5)
        self.assertEqual(r.size().width(), 4)
        self.assertEqual(r.size().height(), 5)
        self.assertEqual(r.topLeft().x, 2)
        self.assertEqual(r.topLeft().y, 3)
        self.assertEqual(r.topRight().x, 5)
        self.assertEqual(r.topRight().y, 3)
        self.assertEqual(r.bottomLeft().x, 2)
        self.assertEqual(r.bottomLeft().y, 7)
        self.assertEqual(r.bottomRight().x, 5)
        self.assertEqual(r.bottomRight().y, 7)
        self.assertEqual(r.left(), 2)
        self.assertEqual(r.right(), 5)
        self.assertEqual(r.top(), 3)
        self.assertEqual(r.bottom(), 7)


