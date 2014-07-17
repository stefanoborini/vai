import unittest
from unittest.mock import Mock
from vixtk import gui, test, core
from vix.EditAreaController import EditAreaController
from vix.EditArea import EditArea
from vix.models.EditorModel import EditorModel
from vix.models.Buffer import Buffer
from vixtk.gui import events
import vixtk
from vix import flags

class TestEditAreaController(unittest.TestCase):
    def setUp(self):
        self.mock_edit_area = Mock(spec=EditArea)
        self.mock_buffer = Mock(spec=Buffer)
        self.mock_editor_model = Mock(spec=EditorModel)
        self.mock_editor_model.mode.return_value = flags.COMMAND_MODE

    def testEditAreaController(self):
        controller = EditAreaController(self.mock_edit_area)
        controller.setModels(self.mock_buffer, self.mock_editor_model)
        event = events.VKeyEvent(vixtk.Key.Key_D)
        controller.handleKeyEvent(event)
        self.assertTrue(self.mock_editor_model.setMode.called)
        self.assertEqual(self.mock_editor_model.setMode.call_args[0][0], flags.DELETE_MODE)


        self.mock_editor_model.setMode.reset_mock()
        self.mock_editor_model.mode.return_value = flags.DELETE_MODE
        event = events.VKeyEvent(vixtk.Key.Key_Q)
        controller.handleKeyEvent(event)
        self.assertTrue(self.mock_editor_model.setMode.called)
        self.assertEqual(self.mock_editor_model.setMode.call_args[0][0], flags.COMMAND_MODE)


if __name__ == '__main__':
    unittest.main()
