import unittest
from videtoolkit import core

class TestVObject(unittest.TestCase):
    def testInstantiation(self):
        o = core.VObject()
        self.assertEqual(o.parent(), None)
        self.assertEqual(len(o.children()), 0)

    def testParent(self):
        p = core.VObject()
        c1 = core.VObject(p)
        c2 = core.VObject(p)
        self.assertEqual(p.parent(), None)
        self.assertEqual(len(p.children()), 2)
        self.assertEqual(p.children()[0], c1)
        self.assertEqual(p.children()[1], c2)
        self.assertEqual(c1.parent(), p)
        self.assertEqual(c2.parent(), p)
        self.assertEqual(len(c1.children()), 0)
        self.assertEqual(len(c2.children()), 0)

    def testTree(self):
        p = core.VObject()
        c1 = core.VObject(p)
        c2 = core.VObject(p)
        c3 = core.VObject(c1)

        self.assertEqual(p.tree(), [p, c1, c3, c2])

    def testTraverseToRoot(self):
        p = core.VObject()
        c1 = core.VObject(p)
        c2 = core.VObject(p)
        c3 = core.VObject(c1)

        self.assertEqual(p.traverseToRoot(), [p])
        self.assertEqual(c3.traverseToRoot(), [c3, c1, p])

    def testRoot(self):
        p = core.VObject()
        c1 = core.VObject(p)
        c2 = core.VObject(p)
        c3 = core.VObject(c1)

        self.assertEqual(p.root(), p)
        self.assertEqual(c1.root(), p)
        self.assertEqual(c2.root(), p)
        self.assertEqual(c3.root(), p)

    def testRightTree(self):
        p = core.VObject()
        c1_1 = core.VObject(p)
        c2_1 =   core.VObject(c1_1)
        c2_2 =   core.VObject(c1_1)
        c3_1 =     core.VObject(c2_2)
        c3_2 =     core.VObject(c2_2)
        c2_3 =   core.VObject(c1_1)
        c1_2 = core.VObject(p)
        c2_4 =   core.VObject(c1_2)
        c3_3 =     core.VObject(c2_4)
        c2_5 =   core.VObject(c1_2)
        c1_3 = core.VObject(p)

        self.assertEqual(c3_1.rightTree(), [c3_2, c2_3, c1_2, c2_4, c3_3, c2_5, c1_3])
        self.assertEqual(c3_3.rightTree(), [c2_5, c1_3])

class TestCore(unittest.TestCase):
    def testVSignal(self):
        arg = []
        sender = core.VObject()
        signal = core.VSignal(sender)
        def slot(x):
            arg.append(x)
        signal.connect(slot)

        signal.emit(3)

        self.assertEqual(len(arg), 1)
        self.assertEqual(arg[0], 3)

    def testVPoint(self):
        p = core.VPoint(3,2)

        self.assertEqual(p.x(), 3)
        self.assertEqual(p.y(), 2)

        self.assertEqual(list(p), [3,2])


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
        self.assertTrue(core.VRect((2,3), (4,5)).intersects(core.VRect((2,3), (4,5))))
        self.assertFalse(core.VRect((2,3), (4,5)).intersects(core.VRect((2,3), (0,0))))
        self.assertFalse(core.VRect((2,3), (4,5)).intersects(core.VRect((0,0), (2,3))))
        self.assertTrue(core.VRect((2,3), (4,5)).intersects(core.VRect((3,4), (1,1))))
        self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((1,2), (1,1))))
        self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((3,4), (1,1))))
        self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((3,3), (1,1))))
        self.assertFalse(core.VRect((2,3), (1,1)).intersects(core.VRect((4,4), (1,1))))

    def testVRectDimensionality(self):
        r = core.VRect((2,3), (4,5))

        self.assertEqual(r.x(), 2)
        self.assertEqual(r.y(), 3)
        self.assertEqual(r.width(), 4)
        self.assertEqual(r.height(), 5)
        self.assertEqual(r.size().width(), 4)
        self.assertEqual(r.size().height(), 5)
        self.assertEqual(r.topLeft().x(), 2)
        self.assertEqual(r.topLeft().y(), 3)
        self.assertEqual(r.topRight().x(), 5)
        self.assertEqual(r.topRight().y(), 3)
        self.assertEqual(r.bottomLeft().x(), 2)
        self.assertEqual(r.bottomLeft().y(), 7)
        self.assertEqual(r.bottomRight().x(), 5)
        self.assertEqual(r.bottomRight().y(), 7)
        self.assertEqual(r.left(), 2)
        self.assertEqual(r.right(), 5)
        self.assertEqual(r.top(), 3)
        self.assertEqual(r.bottom(), 7)

class testVSize(unittest.TestCase):
    def testVSize(self):
        v = core.VSize(width=4, height=5)
        self.assertEqual(v.height(), 5)
        self.assertEqual(v.width(), 4)
        self.assertEqual(tuple(v), (4,5))

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

if __name__ == '__main__':
    unittest.main()
