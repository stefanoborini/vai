import unittest
from videtoolkit import gui

class TestVApplication(unittest.TestCase):
    def testInit(self):
        screen = gui.DummyVScreen((40,40))
        app = gui.VApplication([], screen=screen)

        self.assertTrue(gui.VApplication.vApp is app)
        self.assertRaises(Exception, lambda : gui.VApplication([], screen=screen))
        app.exit()
        self.assertEqual(gui.VApplication.vApp, None)

class TestVWidget(unittest.TestCase):
    def setUp(self):
        self.screen = gui.DummyVScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testInit(self):
        w = gui.VWidget()

class TestVPalette(unittest.TestCase):
    def setUp(self):
        self.screen = gui.DummyVScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testPalette(self):
        self.assertTrue(isinstance(self.app.palette(), gui.VPalette))

class TestVLabel(unittest.TestCase):
    def setUp(self):
        self.screen = gui.DummyVScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app
    def testVLabel(self):
        label = gui.VLabel("hello")
        label.show()
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "hello")

    def testVLabelChangeString(self):
        label = gui.VLabel("hello")
        label.show()
        self.app.processEvents()
        label.setText("world")
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "hello")
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "world")

class TestVColor(unittest.TestCase):
    def testVColor(self):
        color = gui.VColor((255,25,127))
        self.assertEqual(color.rgb(), (255, 25, 127))
        self.assertEqual(color.hexString(), "FF197F")



"""

    def testVFrame(self):
        label = gui.VFrame()
        self.app.processEvents()
        self.screen.dump()
        #self.assertEqual(self.screen.stringAt(0, self.screen.size()[1]/2, 5), "hello")

"""
if __name__ == '__main__':
    unittest.main()
