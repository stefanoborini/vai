import unittest
from vaitk import gui, test, core

class TestVWidget(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp = None
        del self.app

    def testInit(self):
        w = gui.VWidget()

