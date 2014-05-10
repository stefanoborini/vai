import vixtk
from vixtk import core
from . import flags
from . import commands
import logging

DIRECTIONAL_KEYS = [ vixtk.Key.Key_Up,
                     vixtk.Key.Key_Down,
                     vixtk.Key.Key_Left,
                     vixtk.Key.Key_Right ]

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

        if self._editor_model.mode() == flags.INSERT_MODE:
            self._handleEventInsertMode(event)

        elif self._editor_model.mode() == flags.COMMAND_MODE:
            self._handleEventCommandMode(event)

        elif self._editor_model.mode() == flags.DELETE_MODE:
            self._handleEventDeleteMode(event)

    def _handleEventInsertMode(self, event):
        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.setMode(flags.COMMAND_MODE)
        elif event.key() == vixtk.Key.Key_Backspace:
            self._buffer.documentCursor().deleteChar()
        elif event.key() == vixtk.Key.Key_Return:
            self._buffer.documentCursor().breakLine()
        else:
            text = event.text()
            if len(text) != 0:
                self._buffer.documentCursor().insert(event.text())

        event.accept()

    def _handleEventCommandMode(self, event):
        if event.key() == vixtk.Key.Key_I:
            if event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._buffer.documentCursor().toLineBeginning()
            self._editor_model.setMode(flags.INSERT_MODE)
            event.accept()

        elif event.key() == vixtk.Key.Key_X and event.modifiers() == 0:
            self._buffer.documentCursor().deleteAfter()
            event.accept()

        elif event.key() == vixtk.Key.Key_O:
            if event.modifiers() == 0:
                self._editor_model.setMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._buffer.document(), self._edit_area.documentCursorPos().row+1)
                self._buffer.commandHistory().append(command)
                command.execute()
                self._edit_area.moveCursor(flags.DOWN)
                event.accept()

            elif event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._editor_model.setMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._buffer.document(), self._edit_area.documentCursorPos().row)
                self._buffer.commandHistory().append(command)
                command.execute()
                event.accept()
            else:
                return

        elif event.key() == vixtk.Key.Key_A and event.modifiers() == 0:
            self._editor_model.setMode(flags.INSERT_MODE)
            self._edit_area.moveCursor(flags.LEFT)
            event.accept()

        elif event.key() == vixtk.Key.Key_A and event.modifiers() &  vixtk.KeyModifier.ShiftModifier:
            self._editor_model.setMode(flags.INSERT_MODE)
            self._edit_area.moveCursor(flags.END)
            event.accept()

        elif event.key() == vixtk.Key.Key_U:
            if len(self._buffer.commandHistory()):
                command = self._buffer.commandHistory().pop()
                command.undo()
            event.accept()

        elif event.key() == vixtk.Key.Key_D:
            self._editor_model.setMode(flags.DELETE_MODE)
            event.accept()

    def _handleEventDeleteMode(self, event):
        """
        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.setMode(flags.COMMAND_MODE)
            event.accept()
        elif event.key() == vixtk.Key.Key_D:
            self._editor_model.setMode(flags.DELETE_MODE)
            command = commands.DeleteLineCommand(self._buffer.document(), self._buffer.documentCursor().pos()[0])
            self._buffer.commandHistory().append(command)
            command.execute()
            self._editor_model.setMode(flags.COMMAND_MODE)
            event.accept()
        """
    def setModels(self, buffer, editor_model):
        self._buffer = buffer
        self._editor_model = editor_model

    def _hasModels(self):
        return self._buffer and self._editor_model
