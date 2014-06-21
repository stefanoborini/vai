import unittest
from vixtk import core

class testVSize(unittest.TestCase):
    def testVSize(self):
        v = core.VSize(width=4, height=5)
        self.assertEqual(v.height(), 5)
        self.assertEqual(v.width(), 4)
        self.assertEqual(tuple(v), (4,5))

