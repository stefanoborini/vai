import unittest
from vaitk import test, gui, core
from vai.widgets import CommandBar
from vai.models import EditorMode

class CommandBarTest(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((100,40))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp=None
        del self.app

    def testBasicCommandBar(self):
        bar = CommandBar(parent=None)
        bar.setGeometry((0,0,100,1))
        bar.show()
        bar.editor_mode = EditorMode.INSERT
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0,0,12),  "-- INSERT --")
        bar.editor_mode = EditorMode.COMMAND
        self.app.processEvents()
        self.assertEqual(self.screen.stringAt(0,0,12),  "            ")


if __name__ == '__main__':
    unittest.main()
