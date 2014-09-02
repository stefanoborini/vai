import unittest
from unittest.mock import Mock, PropertyMock
from vaitk import gui, test, core
from vai.EditArea import EditArea
from vai import models
from vaitk.gui import events
import vaitk
from vai import flags
from tests import fixtures

from vai import controllers


class TestEditAreaController(unittest.TestCase):
    def setUp(self):
        self.mock_edit_area = Mock(spec=EditArea)
        self.mock_edit_area.height.return_value = 20
        self.mock_edit_area.width.return_value = 20
        self.mock_buffer = Mock(spec=models.Buffer)
        self.mock_global_state = Mock(spec=models.GlobalState)
        type(self.mock_global_state).editor_mode = PropertyMock(return_value=models.EditorMode.COMMAND)
        self.mock_editor_controller = Mock(spec=controllers.EditorController)

    def testBug121(self):
        buffer = fixtures.buffer("basic_python.py")
        controller = controllers.EditAreaController(self.mock_edit_area,
                                                    self.mock_global_state,
                                                    self.mock_editor_controller)
        controller.buffer = buffer
        buffer.cursor.toPos((1,3))

        line_before = buffer.document.lineText(1)
        event = events.VKeyEvent(vaitk.Key.Key_Backspace)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.cursor.pos, (1,2))
        self.assertEqual(line_before, buffer.document.lineText(1))


if __name__ == '__main__':
    unittest.main()
