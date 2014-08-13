import unittest
from vaitk import gui, test, core
from vai import Editor
from vai.models import BufferList, GlobalState

class TestEditor(unittest.TestCase):
    def setUp(self):
        self.screen = test.VTextScreen((30,30))
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        core.VCoreApplication.vApp=None
        del self.app

    def testEditor(self):
        ed = Editor.Editor(GlobalState(), BufferList())
        self.app.processEvents()
        self.screen.dump()



if __name__ == '__main__':
    unittest.main()
