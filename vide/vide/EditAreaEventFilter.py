import videtoolkit
from videtoolkit import core, gui

from . import flags
import logging

class EditAreaEventFilter(core.VObject):
    def __init__(self, command_bar):
        super().__init__()
        self._editor_model = None
        self._command_bar = command_bar

    def eventFilter(self, event):
        if not self._hasModel():
            return False

        self.logger.info("Event filter!")
        if isinstance(event, gui.VKeyEvent) and event.key() == videtoolkit.Key.Key_Colon:
            self._editor_model.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setFocus()
            return True

        return False

    def _hasModel(self):
        return self._editor_model is not None

    def setModel(self, editor_model):
        self._editor_model = editor_model


