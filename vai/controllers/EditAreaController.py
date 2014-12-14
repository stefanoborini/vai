import vaitk
import os
from vaitk import core, Key, KeyModifier
from ..models import EditorMode
from .. import Search
from ..models import commands
from ..SymbolLookupDb import SymbolLookupDb

DIRECTIONAL_KEYS = [ Key.Key_Up,
                     Key.Key_Down,
                     Key.Key_Left,
                     Key.Key_Right,
                     Key.Key_PageUp,
                     Key.Key_PageDown,
                     Key.Key_Home,
                     Key.Key_End,
                     ]

class CommandState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        # No commands. only movement and no-command operations
        key = event.key()
        modifiers = event.modifiers()

        if key == Key.Key_H:
            buffer.cursor.toCharPrev()
            return CommandState

        if key == Key.Key_J:
            buffer.cursor.toLineNext()
            return CommandState

        if key == Key.Key_K:
            buffer.cursor.toLinePrev()
            return CommandState

        if key == Key.Key_L:
            buffer.cursor.toCharNext()
            return CommandState

        if key == Key.Key_I:
            if modifiers & KeyModifier.ShiftModifier:
                buffer.cursor.toCharFirstNonBlank()
            return InsertState

        if key == Key.Key_Backspace:
            buffer.cursor.toCharPrev()
            return CommandState

        if key == Key.Key_G:
            if modifiers == 0:
                return GoState
            elif modifiers & KeyModifier.ShiftModifier:
                buffer.cursor.toLastLine()
                buffer.edit_area_model.document_pos_at_top = (max(1,
                                                                    buffer.cursor.pos[0]
                                                                  - edit_area.height()
                                                                  + 1),
                                                                 1
                                                             )
                return CommandState

            return UnknownState

        if key == Key.Key_Apostrophe and modifiers == 0:
            return GoToBookmarkState

        if key == Key.Key_D and modifiers == 0:
            return DeleteState

        if key == Key.Key_Y and modifiers == 0:
            return YankState

        if key == Key.Key_Z and modifiers & KeyModifier.ShiftModifier:
            return ZetaState

        if key == Key.Key_M and modifiers == 0:
            return BookmarkState

        if key == Key.Key_Dollar:
            buffer.cursor.toLineEnd()
            return CommandState

        if key == Key.Key_AsciiCircum:
            buffer.cursor.toLineBeginning()
            return CommandState

        if key == Key.Key_U:
            try:
                command = buffer.command_history.prev()
            except IndexError:
                return CommandState

            command.undo()
            return CommandState

        if key == Key.Key_R and modifiers & KeyModifier.ControlModifier:
            try:
                command = buffer.command_history.next()
            except IndexError:
                return CommandState

            command.execute()
            return CommandState

        if key == Key.Key_A:
            if modifiers == 0:
                buffer.cursor.toCharNext()
                return InsertState

            elif modifiers & KeyModifier.ShiftModifier:
                buffer.cursor.toLineEnd()
                return InsertState

            return UnknownState

        if key == Key.Key_N:
            if global_state.current_search is not None:
                text, direction = global_state.current_search
                if modifiers & KeyModifier.ShiftModifier:
                    direction = {Search.SearchDirection.FORWARD: Search.SearchDirection.BACKWARD,
                                 Search.SearchDirection.BACKWARD: Search.SearchDirection.FORWARD}[direction]

                Search.find(buffer, text, direction)
            return CommandState

        if key == Key.Key_Asterisk:
            word_at, word_pos = buffer.document.wordAt(buffer.cursor.pos)
            if word_pos is not None:
                global_state.current_search = (word_at, Search.SearchDirection.FORWARD)

            Search.find(buffer, word_at, Search.SearchDirection.FORWARD)
            return CommandState

        if key == Key.Key_R:
            return ReplaceState

        # Command operations
        command = None
        new_state = CommandState

        if (key == Key.Key_X and modifiers == 0) or \
                key == Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)

        elif key == Key.Key_O:
            if modifiers == 0:
                new_state = InsertState
                command = commands.NewLineAfterCommand(buffer)
            elif modifiers & KeyModifier.ShiftModifier:
                new_state = InsertState
                command = commands.NewLineCommand(buffer)

        elif key == Key.Key_J and event.modifiers() & KeyModifier.ShiftModifier:
            command = commands.JoinWithNextLineCommand(buffer)

        elif key == Key.Key_D and event.modifiers() & KeyModifier.ShiftModifier:
            command = commands.DeleteToEndOfLineCommand(buffer)

        elif key == Key.Key_P:
            if global_state.clipboard is not None:
                if modifiers == 0:
                    command = commands.InsertLineAfterCommand(buffer, global_state.clipboard)
                elif modifiers & KeyModifier.ShiftModifier:
                    command = commands.InsertLineCommand(buffer, global_state.clipboard)

        if command is not None:
            result = command.execute()
            if result.success:
                buffer.command_history.add(command)

            return new_state

        return UnknownState

class InsertState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        command = None
        document = buffer.document
        cursor = buffer.cursor

        if event.key() == Key.Key_Escape:
            return CommandState
        elif event.key() == Key.Key_Backspace:
            command = commands.DeleteSingleCharCommand(buffer)
        elif event.key() == Key.Key_Delete:
            command = commands.DeleteSingleCharAfterCommand(buffer)
        elif event.key() == Key.Key_Return:
            command = commands.BreakLineCommand(buffer)
        else:
            if event.key() == Key.Key_Tab:
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
                buffer.command_history.add(command)

        return InsertState

class DeleteState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == Key.Key_D:
            command = commands.DeleteLineAtCursorCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.add(command)
                global_state.clipboard = result.info[0][1]

        if event.key() == Key.Key_W:
            command = commands.DeleteToEndOfWordCommand(buffer)
            result = command.execute()
            if result.success:
                buffer.command_history.add(command)
                global_state.clipboard = result.info[0][1]

        # Reset if we don't recognize it.
        return CommandState

class YankState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == Key.Key_Escape:
            return CommandState

        if event.key() == Key.Key_Y:
            cursor_pos = buffer.cursor.pos
            global_state.clipboard = buffer.document.lineText(cursor_pos[0])
            return CommandState

        # Reset if we don't recognize it.
        return CommandState

class GoState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if event.key() == Key.Key_G:
            buffer.cursor.toFirstLine()

        return CommandState

class BookmarkState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if Key.Key_A <= event.key() <= Key.Key_Z:
            marker = vaitk.vaiKeyCodeToText(event.key())
            buffer.document.lineMetaInfo("Bookmark").setDataForLines({buffer.cursor.line : marker})

        return CommandState

class GoToBookmarkState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):

        if Key.Key_A <= event.key() <= Key.Key_Z:
            marker = vaitk.vaiKeyCodeToText(event.key())
            found = buffer.document.lineMetaInfo("Bookmark").findWhere(lambda x: x == marker)
            if len(found) != 0:
                buffer.cursor.toLine(list(found.keys())[0])

        return CommandState

class ReplaceState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        if vaitk.isKeyCodePrintable(event.key()):
            command = commands.ReplaceSingleCharCommand(buffer, event.text())
            result = command.execute()
            if result.success:
                buffer.command_history.add(command)

        return CommandState

class ZetaState:
    @classmethod
    def handleEvent(cls, event, buffer, global_state, edit_area, editor_controller):
        if event.key() == Key.Key_Z and event.modifiers() & KeyModifier.ShiftModifier:
            editor_controller.doSaveAndExit()

        return CommandState

class UnknownState:
    """
    Represents a transition that is not valid.
    If a state handler returns UnknownState,
    it means that the event should not be accepted,
    and the state should revert to Command
    """
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
    EditorMode.ZETA: ZetaState,
    EditorMode.BOOKMARK: BookmarkState,
    EditorMode.GOTOBOOKMARK: GoToBookmarkState,
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

        state = MODE_TO_STATE.get(self._global_state.editor_mode)
        if not state:
            return

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
        buffer = self._buffer
        doc_cursor = buffer.cursor

        if key == Key.Key_Up:
            doc_cursor.toLinePrev()
        elif key == Key.Key_Down:
            doc_cursor.toLineNext()
        elif key == Key.Key_Left:
            doc_cursor.toCharPrev()
        elif key == Key.Key_Right:
            doc_cursor.toCharNext()
        elif key == Key.Key_End:
            doc_cursor.toLineEnd()
        elif key == Key.Key_Home:
            doc_cursor.toLineBeginning()
        elif key == Key.Key_PageUp:
            doc_cursor.toLine(max( buffer.edit_area_model.document_pos_at_top[0]-self._edit_area.height(),
                                    1)
                            )
        elif key == Key.Key_PageDown:
            new_pos = min( buffer.edit_area_model.document_pos_at_top[0]+self._edit_area.height()-1,
                           buffer.document.numLines())
            doc_cursor.toLine(new_pos)
            buffer.edit_area_model.document_pos_at_top = (new_pos, 1)
        else:
            raise Exception("Unknown direction flag %s", str(key))

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
        new_top_pos = ( max(1, new_top_pos[0]), max(1,new_top_pos[1]))
        buffer.edit_area_model.document_pos_at_top = new_top_pos
        self._edit_area.visual_cursor_pos = ( doc_cursor_pos[1]-new_top_pos[1],
                                              doc_cursor_pos[0]-new_top_pos[0]
                                              )

        self._edit_area.update()

    def _documentContentChanged(self, *args):
        self._edit_area.update()
