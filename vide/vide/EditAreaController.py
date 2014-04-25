import videtoolkit
from videtoolkit import core
from . import flags
from . import commands
import logging

DIRECTIONAL_KEYS = [ videtoolkit.Key.Key_Up,
                     videtoolkit.Key.Key_Down,
                     videtoolkit.Key.Key_Left,
                     videtoolkit.Key.Key_Right ]

class EditAreaController(core.VObject):
    def __init__(self, view):
        self._document_model = None
        self._view_model = None
        self._editor_model = None
        self._view = view
        self._command_history = []

    def handleKeyEvent(self, event):
        if not self._hasModels():
            return

        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._view.handleDirectionalKey(event)
            event.accept()
            return

        if self._editor_model.mode() == flags.INSERT_MODE:
            self._handleEventInsertMode(event)

        elif self._editor_model.mode() == flags.COMMAND_MODE:
            self._handleEventCommandMode(event)

        elif self._editor_model.mode() == flags.DELETE_MODE:
            self._handleEventDeleteMode(event)


    def _handleEventInsertMode(self, event):
        if event.key() == videtoolkit.Key.Key_Escape:
            self._editor_model.setMode(flags.COMMAND_MODE)

        elif event.key() == videtoolkit.Key.Key_Backspace:
            self._view.moveCursor(flags.LEFT)
            self._document_model.deleteAt(self._view.documentCursorPos(),1)

        elif event.key() == videtoolkit.Key.Key_Return:
            self._document_model.breakAt(self._view.documentCursorPos())
            self._view.moveCursor(flags.DOWN)
            self._view.moveCursor(flags.HOME)

        else:
            text = event.text()
            if len(text) != 0:
                self._document_model.insertAt(self._view.documentCursorPos(), event.text())
                self._view.moveCursor(flags.RIGHT)

        event.accept()

    def _handleEventCommandMode(self, event):
        if event.key() == videtoolkit.Key.Key_I:
            if event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._view.moveCursor(flags.HOME)
            self._editor_model.setMode(flags.INSERT_MODE)
            event.accept()

        elif event.key() == videtoolkit.Key.Key_X and event.modifiers() == 0:
            self._document_model.deleteAt(self._view.documentCursorPos(),1)
            event.accept()

        elif event.key() == videtoolkit.Key.Key_O:
            if event.modifiers() == 0:
                self._editor_model.setMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.documentCursorPos().row+1)
                self._command_history.append(command)
                command.execute()
                self._view.moveCursor(flags.DOWN)
                event.accept()

            elif event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._editor_model.setMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.documentCursorPos().row)
                self._command_history.append(command)
                command.execute()
                event.accept()
            else:
                return

        elif event.key() == videtoolkit.Key.Key_A and event.modifiers() == 0:
            self._editor_model.setMode(flags.INSERT_MODE)
            self._view.moveCursor(flags.LEFT)
            event.accept()

        elif event.key() == videtoolkit.Key.Key_A and event.modifiers() &  videtoolkit.KeyModifier.ShiftModifier:
            self._editor_model.setMode(flags.INSERT_MODE)
            self._view.moveCursor(flags.END)
            event.accept()

        elif event.key() == videtoolkit.Key.Key_U:
            if len(self._command_history):
                command = self._command_history.pop()
                command.undo()
            event.accept()

        elif event.key() == videtoolkit.Key.Key_D:
            self._editor_model.setMode(flags.DELETE_MODE)

            event.accept()

    def _handleEventDeleteMode(self, event):
        if event.key() == videtoolkit.Key.Key_Escape:
            self._editor_model.setMode(flags.COMMAND_MODE)
            event.accept()
        elif event.key() == videtoolkit.Key.Key_D:
            self._editor_model.setMode(flags.DELETE_MODE)
            command = commands.DeleteLineCommand(self._document_model, self._view.documentCursorPos().row)
            self._command_history.append(command)
            command.execute()
            self._editor_model.setMode(flags.COMMAND_MODE)
            event.accept()

    def setModels(self, document_model, view_model, editor_model):
        self._document_model = document_model
        self._view_model = view_model
        self._editor_model = editor_model

    def _hasModels(self):
        return self._document_model and self._view_model and self._editor_model
