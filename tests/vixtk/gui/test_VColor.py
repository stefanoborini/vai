import unittest
from vixtk import gui, test

class TestVColor(unittest.TestCase):
    def testVColor(self):
        color = gui.VColor((255,25,127))
        self.assertEqual(color.rgb(), (255, 25, 127))
        self.assertEqual(color.hexString(), "FF197F")



