import unittest
from videtoolkit import gui

class TestVApplication(unittest.TestCase):

    def testInit(self):
        screen = gui.DummyVScreen()
        app = gui.VApplication([], screen=screen)

        self.assertTrue(gui.VApplication.vApp is app)
        self.assertRaises(Exception, lambda : gui.VApplication([], screen=screen))
        app.exit()
        self.assertEqual(gui.VApplication.vApp, None)

class TestVApplicationInterface(unittest.TestCase):

    def setUp(self):
        self.screen = gui.DummyVScreen()
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testPalette(self):
        self.assertTrue(isinstance(self.app.palette(), gui.VPalette))


class TestGui2(unittest.TestCase):
    def testVColor(self):
        color = gui.VColor((255,25,127))
        self.assertEqual(color.rgb(), (255, 25, 127))
        self.assertEqual(color.hexString(), "FF197F")


"""
    def testVLabel(self):
        label = gui.VLabel("hello")
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, self.screen.size()[1]/2, 5), "hello")

    def testVFrame(self):
        label = gui.VFrame()
        self.app.processEvents()
        self.screen.dump()
        #self.assertEqual(self.screen.stringAt(0, self.screen.size()[1]/2, 5), "hello")

"""
if __name__ == '__main__':
    unittest.main()
