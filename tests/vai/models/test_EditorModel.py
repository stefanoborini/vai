import unittest
from vaitk.test import VSignalSpy
from vai.models.EditorModel import EditorModel
from vai.models.EditMode import EditMode
from vai import flags

class TestEditorModel(unittest.TestCase):
    def setUp(self):
        self._model = EditorModel()

    def testInit(self):
        self.assertEqual(self._model.edit_mode.mode, EditMode.COMMAND)

    def testModeSetting(self):
        spy = VSignalSpy(self._model.edit_mode.changed)
        self._model.edit_mode.setMode(EditMode.INSERT)
        self.assertEqual(self._model.edit_mode.mode, EditMode.INSERT)
        self.assertEqual(spy.count(), 1)

if __name__ == '__main__':
    unittest.main()
