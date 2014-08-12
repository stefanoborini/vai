import vaitk
import os
from vaitk import core
import logging
from ..models import EditorMode
from .. import Search
from .. import commands
from ..flags import MoveDirection
from ..SymbolLookupDb import SymbolLookupDb

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
    def __init__(self, edit_area, global_state):
        self._edit_area = edit_area
        self._buffer = None
        self._global_state = global_state

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        self._buffer = buffer
        self._buffer.cursor.positionChanged.connect(self._cursorPositionChanged)

    def handleKeyEvent(self, event):
        if self._buffer is None:
            event.accept()
            return

        if event.key() in DIRECTIONAL_KEYS:
            self._handleDirectionalKey(event)
            event.accept()
            return


    def _handleDirectionalKey(self, event):
        buffer = self._buffer

        if buffer is None or buffer.document.isEmpty():
            return

        key = event.key()

        direction = { vaitk.Key.Key_Up:       MoveDirection.UP,
                      vaitk.Key.Key_Down:     MoveDirection.DOWN,
                      vaitk.Key.Key_Left:     MoveDirection.LEFT,
                      vaitk.Key.Key_Right:    MoveDirection.RIGHT,
                      vaitk.Key.Key_PageUp:   MoveDirection.PAGE_UP,
                      vaitk.Key.Key_PageDown: MoveDirection.PAGE_DOWN,
                      vaitk.Key.Key_Home:     MoveDirection.HOME,
                      vaitk.Key.Key_End:      MoveDirection.END,
                    }[key]

        buffer = self._buffer

        doc_cursor = buffer.cursor

        if direction == MoveDirection.UP:
#            if self._visual_cursor_pos[1] == 0:
#                self.scrollUp()
            doc_cursor.toLinePrev()
        elif direction == MoveDirection.DOWN:
#            if self._visual_cursor_pos[1] == self.height()-1:
#                self.scrollDown()
            doc_cursor.toLineNext()
        elif direction == MoveDirection.LEFT:
#            if self._visual_cursor_pos[0] == 0:
#                self.scrollPageLeft()
            doc_cursor.toCharPrev()
        elif direction == MoveDirection.RIGHT:
#            if self._visual_cursor_pos[0] == self.width()-1:
#                self.scrollPageRight()
            doc_cursor.toCharNext()
        elif direction == MoveDirection.END:
            doc_cursor.toLineEnd()
        elif direction == MoveDirection.HOME:
            doc_cursor.toLineBeginning()
        elif direction == MoveDirection.PAGE_UP:
#            self.scrollPageUp()
            doc_cursor.toLine(buffer.edit_area_model.document_pos_at_top[0])
        elif direction == MoveDirection.PAGE_DOWN:
#            self.scrollPageDown()
            doc_cursor.toLine(buffer.edit_area_model.document_pos_at_top[0])
        else:
            raise Exception("Unknown direction flag %s", str(direction))

    def _cursorPositionChanged(self, *args):
        print( "cursor position changed")







"""
        if self._global_state.mode == EditorMode.INSERT:
            self._handleEventInsertMode(event)

        elif self._global_state.mode == EditorMode.COMMAND:
            self._handleEventCommandMode(event)

        elif self._global_state.mode == EditorMode.REPLACE:
            self._handleEventReplaceMode(event)

        elif self._global_state.mode == EditorMode.DELETE:
            self._handleEventDeleteMode(event)

        elif self._global_state.mode == EditorMode.GO:
            self._handleEventGoMode(event)

        elif self._global_state.mode == EditorMode.YANK:
            self._handleEventYankMode(event)

        self._edit_area.update()
"""
"""
    def scrollDown(self):
        buffer = self._buffer

        if buffer is None:
            return

        top_pos = buffer.edit_area_model.document_pos_at_top

        if top_pos[0] + self.height() > buffer.document.numLines():
            return

        new_pos = (top_pos[0]+1, top_pos[1])
        buffer.edit_area_model.document_pos_at_top = new_pos

        self.update()

"""
"""
    def scrollUp(self):
        buffer = self._buffer

        if buffer is None:
            return

        top_pos = buffer.edit_area_model.document_pos_at_top
        if top_pos[0] == 1:
            return

        new_pos = (top_pos[0]-1, top_pos[1])
        buffer.edit_area_model.document_pos_at_top = new_pos
        self.update()

"""
"""
    def scrollPageUp(self):
        buffer = self._buffer

        if buffer is None:
            return

        top_pos = buffer.edit_area_model.document_pos_at_top
        new_pos = (top_pos[0]-self.height()+2, top_pos[1])
        if new_pos[0] < 1:
           new_pos = (1, top_pos[1])

        buffer.edit_area_model.document_pos_at_top = new_pos
        self.update()

"""
"""
    def scrollPageDown(self):
        buffer = self._buffer

        if buffer is None:
            return

        top_pos = buffer.edit_area_model.document_pos_at_top
        new_pos = (top_pos[0]+self.height()-2, top_pos[1])
        if new_pos[0] > buffer.document.numLines():
            new_pos = (buffer.document.numLines(),  top_pos[1])

        buffer.edit_area_model.document_pos_at_top = new_pos
        self.update()

"""
"""
    def scrollPageLeft(self):
        buffer = self._global_state.buffer_list.current

        if buffer is None:
            return

        top_pos = buffer.edit_area_model.document_pos_at_top
        new_pos = (top_pos[0], top_pos[1]-int(self.width()/2))
        if new_pos[1] < 1:
           new_pos = (top_pos[0], 1)

        buffer.edit_area_model.document_pos_at_top = new_pos
        self.update()

"""
"""
    def scrollPageRight(self):
        buffer = self._global_state.buffer_list.current

        if buffer is None:
            return

        top_pos = self._buffer.edit_area_model.document_pos_at_top
        new_pos = (top_pos[0], top_pos[1]+int(self.width()/2))

        buffer.edit_area_model.document_pos_at_top = new_pos
        self.update()

"""
"""
    def ensureCursorVisible(self):
        # There are multiple zones where the cursor can be, and the behavior is
        # different depending where the cursor is relative to the viewport area.
        # if the cursor is within 1 position above or below the visible area,
        # then it should scroll one line.
        # In all other cases (horizontal, and vertical distant) it should jump.
        buffer = self._buffer

        if buffer is None:
            return

        doc_cursor_pos = buffer.cursor.pos
        top_pos = buffer.edit_area_model.document_pos_at_top

        new_top_pos = top_pos
        # Check and adjust the vertical positioning

        if doc_cursor_pos[0] == top_pos[0] - 1:
            # Cursor is just outside the top border, scroll one
            new_top_pos = (top_pos[0]-1, top_pos[1])
        elif doc_cursor_pos[0] == top_pos[0] + self.height():
            new_top_pos = (top_pos[0]+1, top_pos[1])
        elif doc_cursor_pos[0] < top_pos[0] - 1 \
            or doc_cursor_pos[0] > top_pos[0] + self.height():
            # Cursor is far away. Put the line in the center
            new_top_pos = (doc_cursor_pos[0]-int(self.height()/2), new_top_pos[1])

        # Now check horizontal positioning. This is easier because
        # We never scroll 1
        if doc_cursor_pos[1] < top_pos[1] or \
            doc_cursor_pos[1] > top_pos[1] + self.width():
            new_top_pos = (new_top_pos[0], doc_cursor_pos[1] - int(self.width()/2))

        #
        new_top_pos = ( max(1, new_top_pos[0]), new_top_pos[1])
        buffer.edit_area_model.document_pos_at_top = new_top_pos
        self.update()

"""
"""
    # Private

    def _handleEventInsertMode(self, event):
        buffer = self._buffer

        command = None
        document = buffer.document
        cursor = buffer.cursor

        if event.key() == vaitk.Key.Key_Escape:
            self._global_state.mode = EditorMode.COMMAND
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

"""
"""
    def _handleEventCommandMode(self, event):
        # FIXME This code sucks. We need better handling of the state machine
        # No commands. only movement and no-command operations
        buffer = self._buffer

        if event.key() == vaitk.Key.Key_I:
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toCharFirstNonBlank()
            self._global_state.mode = EditorMode.INSERT
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            if event.modifiers() == 0:
                self._global_state.mode = EditorMode.GO
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toLastLine()
                buffer.edit_area_model.document_pos_at_top = (max(1,
                                                                    buffer.cursor.pos[0]
                                                                  - self._edit_area.height()
                                                                  + 1),
                                                                 1
                                                             )
                self._global_state.mode = EditorMode.COMMAND

            event.accept()
            return

        if event.key() == vaitk.Key.Key_D and event.modifiers() == 0:
            self._global_state.mode = EditorMode.DELETE
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Y and event.modifiers() == 0:
            self._global_state.mode = EditorMode.YANK
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Dollar:
            self._edit_area.moveCursor(EditorMode.END)
            event.accept()
            return

        if event.key() == vaitk.Key.Key_AsciiCircum:
            self._edit_area.moveCursor(EditorMode.HOME)
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
                self._global_state.mode = EditorMode.INSERT
                self._edit_area.moveCursor(MoveDirection.LEFT)

            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._global_state.mode = EditorMode.INSERT
                self._edit_area.moveCursor(MoveDirection.END)
            else:
                return
            event.accept()
            return

        if event.key() == vaitk.Key.Key_N:
            if self._global_state.current_search is None:
                event.accept()
                return

            text, direction = self._global_state.current_search
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                direction = {SearchDirection.FORWARD: SearchDirection.BACKWARD,
                             SearchDirection.BACKWARD: SearchDirection.FORWARD}[direction]

            Search.find(buffer, text, direction)
            self._ensureCursorVisible()
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Asterisk:
            word_at, word_pos = buffer.document.wordAt(buffer.cursor.pos)
            if word_pos is not None:
                self._global_state.current_search = (word_at, SearchDirection.FORWARD)

            Search.find(buffer, word_at, SearchDirection.FORWARD)
            self._ensureCursorVisible()
            event.accept()
            return

        if event.key() == vaitk.Key.Key_R:
            self._global_state.mode = MoveDirection.REPLACE
            event.accept()
            return

        # Command operations
        command = None

        if (event.key() == vaitk.Key.Key_X and event.modifiers() == 0) or \
            event.key() == vaitk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)
        elif event.key() == vaitk.Key.Key_O:
            if event.modifiers() == 0:
                self._global_state.mode = EditorMode.INSERT
                command = commands.NewLineAfterCommand(buffer)
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                self._global_state.mode = EditorMode.INSERT
                command = commands.NewLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_J and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_D and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(buffer)
        elif event.key() == vaitk.Key.Key_P:
            if self._global_state.clipboard is not None:
                if event.modifiers() == 0:
                    command = commands.InsertLineAfterCommand(buffer, self._global_state.clipboard)
                elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                    command = commands.InsertLineCommand(buffer, self._global_state.clipboard)
        if command is not None:
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            self._ensureCursorVisible()
            event.accept()

"""
"""
    def _handleEventDeleteMode(self, event):
        buffer = self._buffer

        if event.key() == vaitk.Key.Key_Escape:
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        if event.key() == vaitk.Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
                self._global_state.clipboard = result.info[2]
            self._ensureCursorVisible()
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        if event.key() == vaitk.Key.Key_W:
            command = commands.DeleteToEndOfWordCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            self._ensureCursorVisible()
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        # Reset if we don't recognize it.
        self._global_state.mode = EditorMode.COMMAND
        event.accept()
        return

"""
"""
    def _handleEventYankMode(self, event):
        buffer = self._buffer

        if event.key() == vaitk.Key.Key_Escape:
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        if event.key() == vaitk.Key.Key_Y:
            cursor_pos = self._buffer.cursor.pos
            self._global_state.clipboard = buffer.document.lineText(cursor_pos[0])
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        # Reset if we don't recognize it.
        self._global_state.mode = EditorMode.COMMAND
        event.accept()
        return

"""
"""
    def _handleEventGoMode(self, event):
        buffer = self._buffer

        if event.key() == vaitk.Key.Key_Escape:
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return

        if event.key() == vaitk.Key.Key_G:
            buffer.edit_area_model.document_pos_at_top = (1,1)
            buffer.cursor.toFirstLine()
            self._global_state.mode = EditorMode.COMMAND
            event.accept()
            return
"""
"""
    def _handleEventReplaceMode(self, event):
        buffer = self._buffer

        if vaitk.isKeyCodePrintable(event.key()):
            command = commands.ReplaceSingleCharCommand(buffer, event.text())
            result = command.execute()
            if result.success:
                self._buffer.command_history.push(command)
            self._ensureCursorVisible()

        self._global_state.mode = EditorMode.COMMAND
        event.accept()
"""
