import vixtk
from vixtk import core, gui

from . import flags
import logging

class EditAreaEventFilter(core.VObject):
    """
    Event filter to detect the use of commandbar initiation
    keys, such as :, / and ?
    """
    def __init__(self, command_bar):
        super().__init__()
        self._editor_model = None
        self._command_bar = command_bar

    def eventFilter(self, event):
        if not self._hasModel():
            return False

        if not isinstance(event, gui.VKeyEvent):
            return False

        if self._editor_model.mode() != flags.COMMAND_MODE:
            return False

        if event.key() == vixtk.Key.Key_Colon:
            self._editor_model.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setFocus()
            return True

        if event.key() == vixtk.Key.Key_Slash:
            self._editor_model.setMode(flags.SEARCH_FORWARD_MODE)
            self._command_bar.setMode(flags.SEARCH_FORWARD_MODE)
            self._command_bar.setFocus()
            return True

        if event.key() == vixtk.Key.Key_Question:
            self._editor_model.setMode(flags.SEARCH_BACKWARD_MODE)
            self._command_bar.setMode(flags.SEARCH_BACKWARD_MODE)
            self._command_bar.setFocus()
            return True

        return False

    def setModel(self, editor_model):
        self._editor_model = editor_model

    # Private

    def _hasModel(self):
        return self._editor_model is not None


