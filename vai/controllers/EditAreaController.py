import vaitk
import os
from vaitk import core
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

class CommandState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        # No commands. only movement and no-command operations

        if event.key() == vaitk.Key.Key_I:
            if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toCharFirstNonBlank()
            return InsertState

        if event.key() == vaitk.Key.Key_G:
            if event.modifiers() == 0:
                return GoState
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toLastLine()
                buffer.edit_area_model.document_pos_at_top = (max(1,
                                                                    buffer.cursor.pos[0]
                                                                  - edit_area.height()
                                                                  + 1),
                                                                 1
                                                             )
                return CommandState

            return UnknownState

        if event.key() == vaitk.Key.Key_D and event.modifiers() == 0:
            return DeleteState

        if event.key() == vaitk.Key.Key_Y and event.modifiers() == 0:
            return YankState

        if event.key() == vaitk.Key.Key_Z and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            return ZetaState

        if event.key() == vaitk.Key.Key_Dollar:
            buffer.cursor.toLineEnd()
            return CommandState

        if event.key() == vaitk.Key.Key_AsciiCircum:
            buffer.cursor.toLineBeginning()
            return CommandState

        if event.key() == vaitk.Key.Key_U:
            if len(buffer.command_history):
                command = buffer.command_history.pop()
                command.undo()
            return CommandState

        if event.key() == vaitk.Key.Key_A:
            if event.modifiers() == 0:
                buffer.cursor.toCharNext()
                return InsertState

            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                buffer.cursor.toLineEnd()
                return InsertState

            return UnknownState

        if event.key() == vaitk.Key.Key_N:
            if global_state.current_search is not None:
                text, direction = global_state.current_search
                if event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                    direction = {Search.SearchDirection.FORWARD: Search.SearchDirection.BACKWARD,
                                 Search.SearchDirection.BACKWARD: Search.SearchDirection.FORWARD}[direction]

                Search.find(buffer, text, direction)
            return CommandState

        if event.key() == vaitk.Key.Key_Asterisk:
            word_at, word_pos = buffer.document.wordAt(buffer.cursor.pos)
            if word_pos is not None:
                global_state.current_search = (word_at, Search.SearchDirection.FORWARD)

            Search.find(buffer, word_at, Search.SearchDirection.FORWARD)
            return CommandState

        if event.key() == vaitk.Key.Key_R:
            return ReplaceState

        # Command operations
        command = None
        new_state = CommandState

        if (event.key() == vaitk.Key.Key_X and event.modifiers() == 0) or \
                event.key() == vaitk.Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)

        elif event.key() == vaitk.Key.Key_O:
            if event.modifiers() == 0:
                new_state = InsertState
                command = commands.NewLineAfterCommand(buffer)
            elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                new_state = InsertState
                command = commands.NewLineCommand(buffer)

        elif event.key() == vaitk.Key.Key_J and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(buffer)

        elif event.key() == vaitk.Key.Key_D and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(buffer)

        elif event.key() == vaitk.Key.Key_P:
            if global_state.clipboard is not None:
                if event.modifiers() == 0:
                    command = commands.InsertLineAfterCommand(buffer, global_state.clipboard)
                elif event.modifiers() & vaitk.KeyModifier.ShiftModifier:
                    command = commands.InsertLineCommand(buffer, global_state.clipboard)

        if command is not None:
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)

            return new_state

        return UnknownState

class InsertState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        command = None
        document = buffer.document
        cursor = buffer.cursor

        if event.key() == vaitk.Key.Key_Escape:
            return CommandState
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

        return InsertState

class DeleteState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == vaitk.Key.Key_Escape:
            return CommandState

        if event.key() == vaitk.Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
                global_state.clipboard = result.info[2]
            return CommandState

        if event.key() == vaitk.Key.Key_W:
            command = commands.DeleteToEndOfWordCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)
            return CommandState

        # Reset if we don't recognize it.
        return CommandState

class YankState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == vaitk.Key.Key_Escape:
            return CommandState

        if event.key() == vaitk.Key.Key_Y:
            cursor_pos = buffer.cursor.pos
            global_state.clipboard = buffer.document.lineText(cursor_pos[0])
            return CommandState

        # Reset if we don't recognize it.
        return CommandState

class GoState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == vaitk.Key.Key_G:
            buffer.cursor.toFirstLine()

        return CommandState

class ReplaceState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if vaitk.isKeyCodePrintable(event.key()):
            command = commands.ReplaceSingleCharCommand(buffer, event.text())
            result = command.execute()
            if result.success:
                buffer.command_history.push(command)

        return CommandState

class ZetaState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        if event.key() == vaitk.Key.Key_Z and event.modifiers() & vaitk.KeyModifier.ShiftModifier:
            editor_controller.doSaveAndExit()

        return CommandState

class UnknownState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        raise Exception("Event delivered to UnknownState")

MODE_TO_STATE = {
    EditorMode.COMMAND: CommandState,
    EditorMode.INSERT: InsertState,
    EditorMode.DELETE: DeleteState,
    EditorMode.YANK: YankState,
    EditorMode.GO: GoState,
    EditorMode.REPLACE: ReplaceState,
    EditorMode.ZETA: ZetaState
}

STATE_TO_MODE = { v : k for k,v in MODE_TO_STATE.items() }

class EditAreaController(core.VObject):
    def __init__(self, edit_area, global_state, editor_controller):
        self._edit_area = edit_area
        self._buffer = None
        self._global_state = global_state
        self._editor_controller = editor_controller

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        if self._buffer is not None:
            self._buffer.cursor.positionChanged.disconnect(self._cursorPositionChanged)
            self._buffer.document.contentChanged.disconnect(self._documentContentChanged)

        self._buffer = buffer
        self._buffer.cursor.positionChanged.connect(self._cursorPositionChanged)
        self._buffer.document.contentChanged.connect(self._documentContentChanged)

    def handleKeyEvent(self, event):
        if self._buffer is None:
            event.accept()
            return

        if event.key() in DIRECTIONAL_KEYS:
            self._handleDirectionalKey(event)
            event.accept()
            return

        state = MODE_TO_STATE[self._global_state.editor_mode]
        new_state = state.handleEvent(event, self._buffer, self._global_state, self._edit_area, self._editor_controller)
        if new_state is UnknownState:
            self._global_state.editor_mode = STATE_TO_MODE[CommandState]
        else:
            self._global_state.editor_mode = STATE_TO_MODE[new_state]
            event.accept()

        self._edit_area.update()

    # Private

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
            doc_cursor.toLinePrev()
        elif direction == MoveDirection.DOWN:
            doc_cursor.toLineNext()
        elif direction == MoveDirection.LEFT:
            doc_cursor.toCharPrev()
        elif direction == MoveDirection.RIGHT:
            doc_cursor.toCharNext()
        elif direction == MoveDirection.END:
            doc_cursor.toLineEnd()
        elif direction == MoveDirection.HOME:
            doc_cursor.toLineBeginning()
        elif direction == MoveDirection.PAGE_UP:
            doc_cursor.toLine(max( buffer.edit_area_model.document_pos_at_top[0]-self._edit_area.height(),
                                    1)
                            )
        elif direction == MoveDirection.PAGE_DOWN:
            doc_cursor.toLine( min( buffer.edit_area_model.document_pos_at_top[0]+self._edit_area.height(),
                                    buffer.document.numLines()))
        else:
            raise Exception("Unknown direction flag %s", str(direction))

    def _cursorPositionChanged(self, *args):
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
        elif doc_cursor_pos[0] == top_pos[0] + self._edit_area.height():
            new_top_pos = (top_pos[0]+1, top_pos[1])
        elif doc_cursor_pos[0] < top_pos[0] - 1 \
            or doc_cursor_pos[0] > top_pos[0] + self._edit_area.height():
            # Cursor is far away. Put the line in the center
            new_top_pos = (doc_cursor_pos[0]-int(self._edit_area.height()/2), new_top_pos[1])

        # Now check horizontal positioning. This is easier because
        # We never scroll 1
        if doc_cursor_pos[1] < top_pos[1] or \
            doc_cursor_pos[1] > top_pos[1] + self._edit_area.width():
            new_top_pos = (new_top_pos[0], doc_cursor_pos[1] - int(self._edit_area.width()/2))

        #
        new_top_pos = ( max(1, new_top_pos[0]), new_top_pos[1])
        buffer.edit_area_model.document_pos_at_top = new_top_pos
        self._edit_area.visual_cursor_pos = ( doc_cursor_pos[1]-new_top_pos[1],
                                              doc_cursor_pos[0]-new_top_pos[0]
                                              )

        self._edit_area.update()


    def _documentContentChanged(self, *args):
        self._edit_area.update()



