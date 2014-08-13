import unittest
from unittest.mock import Mock
from vaitk import gui, test, core
from vai.controllers import EditAreaController
from vai.EditArea import EditArea
from vai.models import GlobalState
from vai.models import Buffer
from vaitk.gui import events
import vaitk
from vai import flags

class TestEditAreaController(unittest.TestCase):
    def setUp(self):
        self.mock_edit_area = Mock(spec=EditArea)
        self.mock_buffer = Mock(spec=Buffer)
        self.mock_editor_model = Mock(spec=EditorModel)
        self.mock_editor_model.mode.return_value = flags.COMMAND_MODE

    @unittest.skip("Need to mock property")
    def testEditAreaController(self):
        controller = EditAreaController(self.mock_edit_area)
        controller.setModels(self.mock_buffer, self.mock_editor_model)
        event = events.VKeyEvent(vaitk.Key.Key_D)
        controller.handleKeyEvent(event)
        self.assertTrue(self.mock_editor_model.mode.__set__.called)
        self.assertEqual(self.mock_editor_model.mode.call_args[0][0], flags.DELETE_MODE)


        self.mock_editor_model.mode.reset_mock()
        self.mock_editor_model.mode.return_value = flags.DELETE_MODE
        event = events.VKeyEvent(vaitk.Key.Key_Q)
        controller.handleKeyEvent(event)
        self.assertTrue(self.mock_editor_model.mode.__set__.called)
        self.assertEqual(self.mock_editor_model.mode.call_args[0][0], flags.COMMAND_MODE)


if __name__ == '__main__':
    unittest.main()
