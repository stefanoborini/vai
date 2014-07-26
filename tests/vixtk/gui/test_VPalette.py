import unittest
from vixtk import gui, test

class TestVPalette(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testPalette(self):
        self.assertTrue(isinstance(self.app.palette(), gui.VPalette))

