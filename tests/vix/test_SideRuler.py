import unittest
from vixtk import test, gui, core
from vix import SideRuler

class SideRulerTest(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((30,30))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp=None
        del self.app

    def testWhetever(self):
        ruler = SideRuler.SideRuler(parent=None)
        ruler.setGeometry((0,0,10,10))
        self.app.processEvents()
        print(str(self.screen))



if __name__ == '__main__':
    unittest.main()
