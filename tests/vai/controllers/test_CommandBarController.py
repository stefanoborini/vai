import unittest
from unittest.mock import Mock, PropertyMock
from vaitk.core import VSignal
from vai import widgets
from vai import models
from vai import controllers
from vai.EditArea import EditArea


class TestCommandBarController(unittest.TestCase):
    def setUp(self):
        self.command_bar = Mock(spec=widgets.CommandBar)
        self.command_bar.returnPressed = Mock(spec=VSignal)
        self.command_bar.tabPressed = Mock(spec=VSignal)
        self.command_bar.escapePressed = Mock(spec=VSignal)

        self.edit_area = Mock(spec=EditArea)
        self.edit_area.height.return_value = 20
        self.edit_area.width.return_value = 20
        self.global_state = Mock(spec=models.GlobalState)
        self.global_state.editorModeChanged = Mock(spec=VSignal)
        self.editor_controller = Mock(spec=controllers.EditorController)


    def testParseCommandBar(self):
        self.global_state.editor_mode = models.EditorMode.COMMAND_INPUT
        self.command_bar.command_text = ""

        controller = controllers.CommandBarController(self.command_bar, self.edit_area,
                                                      self.editor_controller, self.global_state)

        controller.parseCommandBar()

    def testAutocompleteCommandBar(self):

        self.global_state.editor_mode = models.EditorMode.COMMAND_INPUT
        self.command_bar.command_text = ""

        controller = controllers.CommandBarController(self.command_bar, self.edit_area,
                                                      self.editor_controller, self.global_state)

        controller.autocompleteCommandBar()

if __name__ == '__main__':
    unittest.main()
