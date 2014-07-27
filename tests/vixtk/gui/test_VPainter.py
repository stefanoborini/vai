import unittest
from vixtk import gui, test, core
import vixtk

class TestVPainter(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((40,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp = None
        del self.app

    def testDrawText(self):
        w = gui.VWidget()
        w.resize((40,40))
        painter = gui.VPainter(w)
        painter.drawText((10,10), "hello")
        self.assertEqual(self.screen.stringAt(10, 10, 5), "hello")

    def testDrawLineHorizontal(self):
        w = gui.VWidget()
        w.resize((40,40))
        painter = gui.VPainter(w)
        painter.drawLine((10,10), 5, vixtk.Orientation.Horizontal)
        self.assertEqual(self.screen.stringAt(10,10,5), "+---+")

    def testDrawLineVertical(self):
        w = gui.VWidget()
        w.resize((40,40))
        painter = gui.VPainter(w)
        painter.drawLine((10,10), 5, vixtk.Orientation.Vertical)
        self.assertEqual(self.screen.stringAt(10,10,1), "+")
        self.assertEqual(self.screen.stringAt(10,11,1), "|")
        self.assertEqual(self.screen.stringAt(10,12,1), "|")
        self.assertEqual(self.screen.stringAt(10,13,1), "|")
        self.assertEqual(self.screen.stringAt(10,14,1), "+")


    def testDrawRect(self):
        w = gui.VWidget()
        w.resize((40,40))
        painter = gui.VPainter(w)
        painter.drawRect((10,10,5,5))
        self.assertEqual(self.screen.stringAt(10,10,5), "+---+")
        self.assertEqual(self.screen.stringAt(10,11,5), "|   |")
        self.assertEqual(self.screen.stringAt(10,12,5), "|   |")
        self.assertEqual(self.screen.stringAt(10,13,5), "|   |")
        self.assertEqual(self.screen.stringAt(10,14,5), "+---+")

