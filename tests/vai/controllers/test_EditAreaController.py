import unittest
from unittest.mock import Mock, PropertyMock
from vai.EditArea import EditArea
from vai import models
from vaitk.gui import events
import vaitk
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

    def testBug119(self):
        buffer = fixtures.buffer("basic_python.py")
        controller = controllers.EditAreaController(self.mock_edit_area,
                                                    self.mock_global_state,
                                                    self.mock_editor_controller)
        controller.buffer = buffer
        buffer.cursor.toLastLine()
        last_line_number = buffer.cursor.line
        second_to_last_line = buffer.document.lineText(last_line_number-1)

        type(self.mock_global_state).editor_mode = PropertyMock(return_value=models.EditorMode.DELETE)

        event = events.VKeyEvent(vaitk.Key.Key_D)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.cursor.line, last_line_number-1)
        self.assertEqual(buffer.document.lineText(buffer.cursor.line), second_to_last_line)

    def testShiftJ(self):
        buffer = fixtures.buffer("basic_python.py")
        controller = controllers.EditAreaController(self.mock_edit_area,
                                                    self.mock_global_state,
                                                    self.mock_editor_controller)
        controller.buffer = buffer
        buffer.cursor.toFirstLine()
        type(self.mock_global_state).editor_mode = PropertyMock(return_value=models.EditorMode.COMMAND)

        self.assertEqual(buffer.document.numLines(), 4)

        event = events.VKeyEvent(vaitk.Key.Key_J | vaitk.KeyModifier.ShiftModifier)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.document.numLines(), 3)

    def testdw(self):
        buffer = fixtures.buffer("basic_python.py")
        controller = controllers.EditAreaController(self.mock_edit_area,
                                                    self.mock_global_state,
                                                    self.mock_editor_controller)
        controller.buffer = buffer
        buffer.cursor.toFirstLine()
        type(self.mock_global_state).editor_mode = PropertyMock(return_value=models.EditorMode.DELETE)

        event = events.VKeyEvent(vaitk.Key.Key_W)
        controller.handleKeyEvent(event)

        self.assertEqual(buffer.document.lineText(1), "!python\n")            
        self.assertEqual(self.mock_global_state.clipboard, '#')

        event = events.VKeyEvent(vaitk.Key.Key_W)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.document.lineText(1), "python\n")            
        self.assertEqual(self.mock_global_state.clipboard, '!')

        event = events.VKeyEvent(vaitk.Key.Key_W)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.document.lineText(1), "\n")            
        self.assertEqual(self.mock_global_state.clipboard, 'python')

        event = events.VKeyEvent(vaitk.Key.Key_W)
        controller.handleKeyEvent(event)
        self.assertEqual(buffer.document.lineText(1), "\n")            
        self.assertEqual(self.mock_global_state.clipboard, '')

    def testdd(self):
        global_state = models.GlobalState()
        buffer = fixtures.buffer("basic_python.py")
        controller = controllers.EditAreaController(self.mock_edit_area,
                                                    global_state,
                                                    self.mock_editor_controller)
        controller.buffer = buffer
        buffer.cursor.toFirstLine()

        event = events.VKeyEvent(vaitk.Key.Key_D)
        controller.handleKeyEvent(event)

        event = events.VKeyEvent(vaitk.Key.Key_D)
        controller.handleKeyEvent(event)

        self.assertEqual(global_state.clipboard, '#!python\n')
    
if __name__ == '__main__':
    unittest.main()
