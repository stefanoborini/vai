import unittest
from vaitk.test import VSignalSpy
from vai.models import GlobalState, EditorMode

class TestEditorModel(unittest.TestCase):
    def setUp(self):
        self._model = GlobalState()

    def testInit(self):
        self.assertEqual(self._model.editor_mode, EditorMode.COMMAND)

    def testModeSetting(self):
        spy = VSignalSpy(self._model.editorModeChanged)
        self._model.editor_mode = EditorMode.INSERT
        self.assertEqual(self._model.editor_mode, EditorMode.INSERT)
        self.assertEqual(spy.count(), 1)

if __name__ == '__main__':
    unittest.main()
