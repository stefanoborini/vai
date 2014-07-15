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

        if isinstance(event, gui.VKeyEvent) \
               and event.key() == vixtk.Key.Key_Colon\
               and self._editor_model.mode() == flags.COMMAND_MODE:
            self._editor_model.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setFocus()
            return True

        return False

    def setModel(self, editor_model):
        self._editor_model = editor_model

    # Private

    def _hasModel(self):
        return self._editor_model is not None


