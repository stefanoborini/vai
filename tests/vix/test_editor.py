import unittest
from videtoolkit import gui
from vide import editor

class TestEditor(unittest.TestCase):

    def setUp(self):
        self.screen = gui.DummyVScreen()
        self.app = gui.VApplication([], screen=self.screen)

    def tearDown(self):
        del self.screen
        self.app.exit()
        del self.app

    def testEditor(self):

        ed = editor.Editor(editor.EditorModel(), None)
        self.app.processEvents()
        self.screen.dump()



if __name__ == '__main__':
    unittest.main()
