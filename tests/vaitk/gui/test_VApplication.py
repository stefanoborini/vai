import unittest
from vaitk import gui, test, core

class TestVApplication(unittest.TestCase):
    def testInit(self):
        screen = test.VTextScreen((40,40))
        self.assertTrue(gui.VApplication.vApp is None)

        app = gui.VApplication([], screen=screen)
        self.assertTrue(gui.VApplication.vApp is app)
        self.assertRaises(Exception, lambda : gui.VApplication([], screen=screen))
        app.exit()
        core.VCoreApplication.vApp = None

