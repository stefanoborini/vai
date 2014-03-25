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

if __name__ == '__main__':
    unittest.main()
