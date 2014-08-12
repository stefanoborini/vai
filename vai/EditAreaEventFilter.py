import vaitk
from vaitk import core, gui

from . import flags
import logging

class EditAreaEventFilter(core.VObject):
    """
    Event filter to detect the use of commandbar initiation
    keys, such as :, / and ?
    """
    def __init__(self, command_bar, global_state):
        super().__init__()
        self._global_state = global_state
        self._command_bar = command_bar

    def eventFilter(self, event):
        if not isinstance(event, gui.VKeyEvent):
            return False

        if self._global_state.mode != flags.COMMAND_MODE:
            return False

        if event.key() == vaitk.Key.Key_Colon:
            self._global_state.mode = flags.COMMAND_INPUT_MODE
            self._command_bar.setFocus()
            return True

        if event.key() == vaitk.Key.Key_Slash:
            self._global_state.mode = flags.SEARCH_FORWARD_MODE
            self._command_bar.setFocus()
            return True

        if event.key() == vaitk.Key.Key_Question:
            self._global_state.mode = flags.SEARCH_BACKWARD_MODE
            self._command_bar.setMode(flags.SEARCH_BACKWARD_MODE)
            self._command_bar.setFocus()
            return True

        if event.key() == vaitk.Key.Key_N and event.modifiers() & vaitk.KeyModifier.ControlModifier:
            self._buffer_list.selectNext()
            return True

        if event.key() == vaitk.Key.Key_P and event.modifiers() & vaitk.KeyModifier.ControlModifier:
            self._buffer_list.selectPrev()
            return True

        return False

    def setModel(self, global_state):
        self._global_state = global_state

