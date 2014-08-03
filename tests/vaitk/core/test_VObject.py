import unittest
from vixtk import core

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

        self.assertEqual(p.depthFirstFullTree(), [p, c1, c3, c2])
        self.assertEqual(c2.depthFirstFullTree(), [p, c1, c3, c2])
        self.assertEqual(c2.depthFirstSubTree(), [c2])
        self.assertEqual(c1.depthFirstSubTree(), [c1, c3])

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

        self.assertEqual(c3_1.depthFirstRightTree(), [c3_2, c2_3, c1_2, c2_4, c3_3, c2_5, c1_3])
        self.assertEqual(c3_3.depthFirstRightTree(), [c2_5, c1_3])

