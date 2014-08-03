import unittest
from vixtk.test import VSignalSpy
from vix.models.EditorModel import EditorModel
from vix import flags

class TestEditorModel(unittest.TestCase):
    def setUp(self):
        self._model = EditorModel()

    def testInit(self):
        self.assertEqual(self._model.mode(), flags.COMMAND_MODE)

    def testModeSetting(self):
        spy = VSignalSpy(self._model.modeChanged)
        self._model.setMode(flags.INSERT_MODE)
        self.assertEqual(self._model.mode(), flags.INSERT_MODE)
        self.assertEqual(spy.count(), 1)

if __name__ == '__main__':
    unittest.main()
