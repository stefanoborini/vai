import unittest
from vixtk import test, gui, core
from vix import widgets

class StatusBarTest(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,10))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp=None
        del self.app

    def testBasicRepresentation(self):
        bar = widgets.StatusBar(parent=None)
        bar.setGeometry((0,0,40,1))
        bar.show()
        bar.setPosition( (1,1))
        bar.setFilename("foo")
        bar.setFileChangedFlag(True)
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0,0,40),  "foo [+]                           1,1   ")

        bar.setPosition( (3,3))
        bar.setFilename("bar")
        bar.setFileChangedFlag(False)
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0,0,40),  "bar                               3,3   ")


if __name__ == '__main__':
    unittest.main()
