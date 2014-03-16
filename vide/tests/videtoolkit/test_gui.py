import unittest
from videtoolkit import gui

class TestGui(unittest.TestCase):

    def setUp(self):
        self.screen = gui.DummyVScreen()
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testVLabel(self):
        label = gui.VLabel("hello")
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, self.screen.size()[1]/2, 5), "hello")

    def testVFrame(self):
        label = gui.VFrame()
        self.app.processEvents()
        self.screen.dump()
        #self.assertEqual(self.screen.stringAt(0, self.screen.size()[1]/2, 5), "hello")

class TestGui2(unittest.TestCase):

    def testColors(self):
        app = gui.VApplication([])
        print app.numColors()
        app.supportedColors()

if __name__ == '__main__':
    unittest.main()
