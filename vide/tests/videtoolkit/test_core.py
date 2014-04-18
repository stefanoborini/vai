import unittest
from videtoolkit import core

class TestCore(unittest.TestCase):
    def testVObject(self):
        o = core.VObject()
        self.assertEqual(o.parent(), None)
        self.assertEqual(len(o.children()), 0)

    def testVObjectParent(self):
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

    def testVObjectTree(self):
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

    def testVSize(self):
        v = core.VSize(width=4, height=5)
        self.assertEqual(v.height(), 5)
        self.assertEqual(v.width(), 4)
        self.assertEqual(tuple(v), (4,5))

if __name__ == '__main__':
    unittest.main()
