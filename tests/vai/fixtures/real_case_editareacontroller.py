import vaitk
from vaitk import core
from . import flags
from . import Search
from . import commands
import logging

DIRECTIONAL_KEYS = [ vaitk.Key.Key_Up,
                     vaitk.Key.Key_Down,
                     vaitk.Key.Key_Left,
                     vaitk.Key.Key_Right,
                     vaitk.Key.Key_PageUp,
                     vaitk.Key.Key_PageDown,
                     vaitk.Key.Key_Home,
                     vaitk.Key.Key_End,
                     ]

class EditAreaController(core.VObject):
    def __init__(self, edit_area):
        self._buffer = None
        self._editor_model = None
        self._edit_area = edit_area

    def handleKeyEvent(self, event):
        if not self._hasModels():
            return

        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._edit_area.handleDirectionalKey(event)
            event.accept()
            return

        if self._editor_model.mode == flags.INSERT_MODE:
            self._handleEventInsertMode(event)

        elif self._editor_model.mode == flags.COMMAND_MODE:
            self._handleEventCommandMode(event)

        elif self._editor_model.mode == flags.DELETE_MODE:
            self._handleEventDeleteMode(event)

        elif self._editor_model.mode == flags.GO_MODE:
            self._handleEventGoMode(event)

    def setModels(self, buffer, editor_model):
        self._buffer = buffer
        self._editor_model = editor_model

    # Private

    def _handleEventInsertMode(self, event):
        command = None

        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
        elif event.key() == vaitk.Key.Key_Backspace:
            command = commands.DeleteSingleCharCommand(self._buffer)
        elif event.key() == vaitk.Key.Key_Return:
            command = commands.BreakLineCommand(self._buffer)
        else:
            if event.key() == vaitk.Key.Key_Tab:
                text = " "*4
            else:
                text = event.text()

            if len(text) != 0:
                command = commands.InsertStringCommand(self._buffer, text)

        if command is not None:
            self._buffer.commandHistory().append(command)
            command.execute()

        event.accept()

    def _handleEventCommandMode(self, event):
        # FIXME This code sucks. We need better handling of the state machine
        # No commands. only movement and no-command operations
        if event.key() == vaitk.Key.Key_I:
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._buffer.documentCursor().toLineBeginning()
            self._editor_model.mode = flags.INSERT_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.GO_MODE
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._buffer.documentCursor().toLastLine()
                self._buffer.editAreaModel().setDocumentPosAtTop((self._buffer.documentCursor().pos()[0]-self._edit_area.height()+1,1))
                self._editor_model.mode = flags.COMMAND_MODE

            event.accept()
            return

        if event.key() == vaitk.Key.Key_D and event.modifiers() == 0:
            self._editor_model.mode = flags.DELETE_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Dollar:
            self._edit_area.moveCursor(flags.END)
            event.accept()
            return

        if event.key() == vaitk.Key.Key_AsciiCircum:
            self._edit_area.moveCursor(flags.HOME)
            event.accept()
            return

        if event.key() == vaitk.Key.Key_U:
            if len(self._buffer.commandHistory()):
                command = self._buffer.commandHistory().pop()
                command.undo()
            event.accept()
            return

        if event.key() == vaitk.Key.Key_A:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.INSERT_MODE
                self._edit_area.moveCursor(flags.LEFT)

            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._editor_model.mode = flags.INSERT_MODE
                self._edit_area.moveCursor(flags.END)
            else:
                return
            event.accept()
            return

        if event.key() == vaitk.Key.Key_N:
            if event.modifiers() == 0:
                if self._editor_model.current_search is not None:
                    Search.find(self._buffer, self._editor_model.current_search)
                event.accept()
                return
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                if self._editor_model.current_search is not None:
                    Search.find(self._buffer, self._editor_model.current_search, backwards=True)
                event.accept()
                return

        # Command operations
        command = None

        if event.key() == vaitk.Key.Key_X and event.modifiers() == 0:
            command = commands.DeleteSingleCharAfterCommand(self._buffer)

        elif event.key() == vaitk.Key.Key_O:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineAfterCommand(self._buffer)
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineCommand(self._buffer)
        elif event.key() == vaitk.Key.Key_J and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(self._buffer)
        elif event.key() == vaitk.Key.Key_D and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(self._buffer)

        if command is not None:
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            event.accept()

    def _handleEventDeleteMode(self, event):
        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return
        else:
            # Reset if we don't recognize it.
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

    def _handleEventGoMode(self, event):
        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            self._buffer.editAreaModel().setDocumentPosAtTop((1,1))
            self._buffer.documentCursor().toFirstLine()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

    # Private

    def _hasModels(self):
        return self._buffer and self._editor_model
