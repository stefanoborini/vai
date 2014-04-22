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
    def __init__(self, document_model, view_model, view):
        self._document_model = document_model
        self._view_model = view_model
        self._view = view
        self._command_history = []

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._view.handleDirectionalKey(event)
            event.accept()
            return

        if self._view_model.editorMode() == flags.INSERT_MODE:
            if event.key() == videtoolkit.Key.Key_Escape:
                self._view_model.setEditorMode(flags.COMMAND_MODE)
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

        if self._view_model.editorMode() == flags.COMMAND_MODE:
            if event.key() == videtoolkit.Key.Key_I:
                if event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                    self._view.moveCursor(flags.HOME)
                self._view_model.setEditorMode(flags.INSERT_MODE)
            if event.key() == videtoolkit.Key.Key_X and event.modifiers() == 0:
                self._document_model.deleteAt(self._view.documentCursorPos(),1)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() == 0:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.documentCursorPos().row+1)
                self._command_history.append(command)
                command.execute()
                self._view.moveCursor(flags.DOWN)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.documentCursorPos().row)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_A and event.modifiers() == 0:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                self._view.moveCursor(flags.LEFT)
            elif event.key() == videtoolkit.Key.Key_A and event.modifiers() &  videtoolkit.KeyModifier.ShiftModifier:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                self._view.moveCursor(flags.END)
            elif event.key() == videtoolkit.Key.Key_U and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                if len(self._command_history):
                    command = self._command_history.pop()
                    command.undo()
            elif event.key() == videtoolkit.Key.Key_Colon and event.modifiers() == 0:
                pass


            event.accept()


