import vaitk
import os
from vaitk import core
import logging
from . import flags
from . import Search
from . import commands
from .SymbolLookupDb import SymbolLookupDb

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
    def __init__(self, edit_area, editor_model):
        self._edit_area = edit_area
        self._editor_model = editor_model

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
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

    # Private
    def _handleEventInsertMode(self, event):
        buffer = self._editor_model.buffer_list.current
        command = None
        document = buffer.document
        cursor = buffer.cursor

        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
        elif event.key() == vaitk.Key.Key_Backspace:
            command = commands.DeleteSingleCharCommand(buffer)
        elif event.key() == vaitk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)
        elif event.key() == vaitk.Key.Key_Return:
            command = commands.BreakLineCommand(buffer)
        else:
            if event.key() == vaitk.Key.Key_Tab:
                if cursor.pos[1] == 1:
                    text = " "*4
                else:
                    prefix = document.wordAt( (cursor.pos[0], cursor.pos[1]-1))
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
                command = commands.InsertStringCommand(buffer, text)

        if command is not None:
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            self._edit_area.ensureCursorVisible()

        event.accept()

    def _handleEventCommandMode(self, event):
        # FIXME This code sucks. We need better handling of the state machine
        # No commands. only movement and no-command operations
        buffer = self._editor_model.buffer_list.current
        if event.key() == vaitk.Key.Key_I:
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toCharFirstNonBlank()
            self._editor_model.mode = flags.INSERT_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.GO_MODE
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toLastLine()
                buffer.edit_area_model.document_pos_at_top = (max(1,
                                                                    buffer.cursor.pos[0]
                                                                  - self._edit_area.height()
                                                                  + 1),
                                                                 1
                                                             )
                self._editor_model.mode = flags.COMMAND_MODE

            event.accept()
            return

        if event.key() == vaitk.Key.Key_D and event.modifiers() == 0:
            self._editor_model.mode = flags.DELETE_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Y and event.modifiers() == 0:
            self._editor_model.mode = flags.YANK_MODE
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
            if len(self._buffer.command_history):
                command = buffer.command_history.pop()
                command.undo()
                self._edit_area.ensureCursorVisible()
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
            if self._editor_model.current_search is None:
                event.accept()
                return

            text, direction = self._editor_model.current_search
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                direction = {flags.FORWARD:flags.BACKWARD,
                             flags.BACKWARD: flags.FORWARD}[direction]

            Search.find(buffer, text, direction)
            self._edit_area.ensureCursorVisible()
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Asterisk:
            word_at, word_pos = buffer.document.wordAt(buffer.cursor.pos)
            if word_pos is not None:
                self._editor_model.current_search = (word_at, flags.FORWARD)

            Search.find(buffer, word_at, flags.FORWARD)
            self._edit_area.ensureCursorVisible()
            event.accept()
            return

        if event.key() == vaitk.Key.Key_R:
            self._editor_model.mode = flags.REPLACE_MODE
            event.accept()
            return

        # Command operations
        command = None

        if (event.key() == vaitk.Key.Key_X and event.modifiers() == 0) or \
            event.key() == vaitk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)
        elif event.key() == vaitk.Key.Key_O:
            if event.modifiers() == 0:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineAfterCommand(buffer)
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._editor_model.mode = flags.INSERT_MODE
                command = commands.NewLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_J and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_D and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_P:
            if self._editor_model.clipboard is not None:
                if event.modifiers() == 0:
                    command = commands.InsertLineAfterCommand(buffer, self._editor_model.clipboard)
                elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                    command = commands.InsertLineCommand(buffer, self._editor_model.clipboard)
        if command is not None:
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            self._edit_area.ensureCursorVisible()
            event.accept()

    def _handleEventDeleteMode(self, event):
        buffer = self._editor_model.buffer_list.current
        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
                self._editor_model.clipboard = result.info[2]
            self._edit_area.ensureCursorVisible()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_W:
            command = commands.DeleteToEndOfWordCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            self._edit_area.ensureCursorVisible()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        # Reset if we don't recognize it.
        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()
        return

    def _handleEventYankMode(self, event):
        buffer = self._editor_model.buffer_list.current
        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Y:
            cursor_pos = self._buffer.cursor.pos
            self._editor_model.clipboard = buffer.document.lineText(cursor_pos[0])
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        # Reset if we don't recognize it.
        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()
        return

    def _handleEventGoMode(self, event):
        buffer = self._editor_model.buffer_list.current
        if event.key() == vaitk.Key.Key_Escape:
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            buffer.edit_area_model.document_pos_at_top = (1,1)
            buffer.cursor.toFirstLine()
            self._editor_model.mode = flags.COMMAND_MODE
            event.accept()
            return

    def _handleEventReplaceMode(self, event):
        buffer = self._editor_model.buffer_list.current
        if vaitk.isKeyCodePrintable(event.key()):
            command = commands.ReplaceSingleCharCommand(buffer, event.text())
            result = command.execute()
            if result.success:
                self._buffer.command_history.push(command)
            self._edit_area.ensureCursorVisible()

        self._editor_model.mode = flags.COMMAND_MODE
        event.accept()

