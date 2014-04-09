import videtoolkit
from videtoolkit import core, gui

from . import flags
import logging

class EditAreaEventFilter(core.VObject):
    def __init__(self, view_model, command_bar):
        self._view_model = view_model
        self._command_bar = command_bar

    def eventFilter(self, event):
        logging.info("Event filter!")
        if isinstance(event, gui.VKeyEvent) and event.key() == videtoolkit.Key.Key_Colon:
            self._view_model.setEditorMode(flags.COMMAND_INPUT_MODE)
            self._command_bar.setFocus()
            return True

        return False



