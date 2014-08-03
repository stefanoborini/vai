import unittest
from vaitk import gui, test

class TestVLabel(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    @unittest.skip
    def testVLabel(self):
        label = gui.VLabel("hello")
        label.show()
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "hello")

    @unittest.skip
    def testVLabelChangeString(self):
        label = gui.VLabel("hello")
        label.show()
        self.app.processEvents()
        label.setText("world")
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "hello")
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0, int(self.screen.size()[1]/2), 5), "world")


