import vixtk
import os
from vixtk import core
import logging
from . import flags
from . import Search
from . import commands
from .SymbolLookupDb import SymbolLookupDb

DIRECTIONAL_KEYS = [ vixtk.Key.Key_Up,
                     vixtk.Key.Key_Down,
                     vixtk.Key.Key_Left,
                     vixtk.Key.Key_Right,
                     vixtk.Key.Key_PageUp,
                     vixtk.Key.Key_PageDown,
                     vixtk.Key.Key_Home,
                     vixtk.Key.Key_End,
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

        elif self._editor_model.mode == flags.REPLACE_MODE:
            self._handleEventReplaceMode(event)

        elif self._editor_model.mode == flags.DELETE_MODE:
            self._handleEventDeleteMode(event)

        elif self._editor_model.mode == flags.GO_MODE:
            self._handleEventGoMode(event)

        elif self._editor_model.mode == flags.YANK_MODE:
            self._handleEventYankMode(event)

    def setModels(self, buffer, editor_model):
        self._buffer = buffer
        self._editor_model = editor_model

    # Private
    def _handleEventInsertMode(self, event):
        command = None
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
        elif event.key() == vixtk.Key.Key_Backspace:
            command = commands.DeleteSingleCharCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_Return:
            command = commands.BreakLineCommand(self._buffer)
        else:
            if event.key() == vixtk.Key.Key_Tab:
                if cursor.pos()[1] == 1:
                    text = " "*4
                else:
                    prefix = document.wordAt( (cursor.pos()[0], cursor.pos()[1]-1))
                    if prefix[1] is None:
                        text = " "*4
                    else:
                        lookup = [x for x in SymbolLookupDb.lookup(prefix[0]) if x != '']
                        if len(lookup) >= 1:
                            text = os.path.commonprefix(lookup)
                        else:
                            text = ''
            else:
                text = event.text()

            if len(text) != 0:
                command = commands.InsertStringCommand(self._buffer, text)

        if command is not None:
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            self._edit_area.ensureCursorVisible()

        event.accept()

    def _handleEventCommandMode(self, event):
        # FIXME This code sucks. We need better handling of the state machine
        # No commands. only movement and no-command operations
        if event.key() == vixtk.Key.Key_I:
            if event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._buffer.documentCursor().toCharFirstNonBlank()
            self._editor_model.mode = flags.INSERT_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_G:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.GO_MODE
            elif event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._buffer.documentCursor().toLastLine()
                self._buffer.editAreaModel().setDocumentPosAtTop((self._buffer.documentCursor().pos()[0]-self._edit_area.height()+1,1))
                self._editor_model.mode = flags.COMMAND_MODE

            event.accept()
            return

        if event.key() == vixtk.Key.Key_D and event.modifiers() == 0:
            self._editor_model.mode = flags.DELETE_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_Y and event.modifiers() == 0:
            self._editor_model.mode = flags.YANK_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_Dollar:
            self._edit_area.moveCursor(flags.END)
            event.accept()
            return

        if event.key() == vixtk.Key.Key_AsciiCircum:
            self._edit_area.moveCursor(flags.HOME)
            event.accept()
            return

        if event.key() == vixtk.Key.Key_U:
            if len(self._buffer.commandHistory()):
                command = self._buffer.commandHistory().pop()
                command.undo()
                self._edit_area.ensureCursorVisible()
            event.accept()
            return

        if event.key() == vixtk.Key.Key_A:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.INSERT_MODE
                self._edit_area.moveCursor(flags.LEFT)

            elif event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._editor_model.mode = flags.INSERT_MODE
                self._edit_area.moveCursor(flags.END)
            else:
                return
            event.accept()
            return

        if event.key() == vixtk.Key.Key_N:
            if self._editor_model.current_search is None:
                event.accept()
                return

            text, direction = self._editor_model.current_search
            if event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                direction = {flags.FORWARD:flags.BACKWARD,
                             flags.BACKWARD: flags.FORWARD}[direction]

            Search.find(self._buffer, text, direction)
            self._edit_area.ensureCursorVisible()
            event.accept()
            return

        if event.key() == vixtk.Key.Key_Asterisk:
            word_at, word_pos = self._buffer.document().wordAt(self._buffer.documentCursor().pos())
            if word_pos is not None:
                self._editor_model.current_search = (word_at, flags.FORWARD)

            Search.find(self._buffer, word_at, flags.FORWARD)
            self._edit_area.ensureCursorVisible()
            event.accept()
            return

        if event.key() == vixtk.Key.Key_R:
            self._editor_model.mode = flags.REPLACE_MODE
            event.accept()
            return

        # Command operations
        command = None

        if (event.key() == vixtk.Key.Key_X and event.modifiers() == 0) or \
            event.key() == vixtk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_O:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineAfterCommand(self._buffer)
            elif event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_J and event.modifiers() & vixtk.KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_D and event.modifiers() & vixtk.KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(self._buffer)
        elif event.key() == vixtk.Key.Key_P:
            if self._editor_model.clipboard is not None:
                if event.modifiers() == 0:
                    command = commands.InsertLineAfterCommand(self._buffer, self._editor_model.clipboard)
                elif event.modifiers() & vixtk.KeyModifier.ShiftModifier:
                    command = commands.InsertLineCommand(self._buffer, self._editor_model.clipboard)
        if command is not None:
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            self._edit_area.ensureCursorVisible()
            event.accept()

    def _handleEventDeleteMode(self, event):
        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
                self._editor_model.clipboard = result.info[2]
            self._edit_area.ensureCursorVisible()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_W:
            command = commands.DeleteToEndOfWordCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            self._edit_area.ensureCursorVisible()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        # Reset if we don't recognize it.
        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()
        return

    def _handleEventYankMode(self, event):
        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_Y:
            cursor_pos = self._buffer.documentCursor().pos()
            self._editor_model.clipboard = self._buffer.document().lineText(cursor_pos[0])
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        # Reset if we don't recognize it.
        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()
        return

    def _handleEventGoMode(self, event):
        if event.key() == vixtk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vixtk.Key.Key_G:
            self._buffer.editAreaModel().setDocumentPosAtTop((1,1))
            self._buffer.documentCursor().toFirstLine()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

    def _handleEventReplaceMode(self, event):
        if vixtk.isKeyCodePrintable(event.key()):
            command = commands.ReplaceSingleCharCommand(self._buffer, event.text())
            result = command.execute()
            if result.success:
                self._buffer.commandHistory().append(command)
            self._edit_area.ensureCursorVisible()

        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()

    # Private

    def _hasModels(self):
        return self._buffer and self._editor_model
