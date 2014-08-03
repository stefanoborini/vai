import unittest
from vixtk import gui, test, core

class TestVPalette(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp = None
        del self.app

    def testPalette(self):
        self.assertTrue(isinstance(self.app.palette(), gui.VPalette))

