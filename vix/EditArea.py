import vixtk
from vixtk import gui, core
from .EditAreaController import EditAreaController
from .positions import CursorPos, DocumentPos
from . import flags
import logging

from pygments.formatter import Formatter
from pygments import token

TOKEN_TO_COLORS = {
    token.Keyword: (gui.VGlobalColor.yellow, None),
    token.Keyword.Namespace: (gui.VGlobalColor.magenta, None),
    token.Comment: (gui.VGlobalColor.cyan, None),
    token.Name.Function: (gui.VGlobalColor.cyan, None),
    token.Name.Class: (gui.VGlobalColor.cyan, None),
}

class EditArea(gui.VWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._controller = EditAreaController(self)

        self._buffer = None
        self._editor_model = None
        self._visual_cursor_pos = CursorPos(0,0)
        self.setFocusPolicy(vixtk.FocusPolicy.StrongFocus)

        self.scrollDown = core.VSignal(self)
        self.scrollDown.connect(self.scrollDownSlot)
        self.scrollUp = core.VSignal(self)
        self.scrollUp.connect(self.scrollUpSlot)

        self.cursorPositionChanged = core.VSignal(self)

    def setModels(self, buffer, editor_model):
        self._buffer = buffer
        self._editor_model = editor_model
        self._controller.setModels(buffer, editor_model)
        self.update()

    def _hasModels(self):
        return self._buffer and self._editor_model

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        painter.erase()
        if self._hasModels():
            for i in range(0, h):
                document_line = self._buffer.viewModel().documentPosAtTop().row + i
                if document_line < self._buffer.document().numLines():
                    line = self._buffer.document().getLine(document_line)
                    painter.drawText( (0, i), line.replace('\n', ' '))
                    char_meta = self._buffer.document().charMeta(document_line)
                    colors = [TOKEN_TO_COLORS.get(tok, (None, None)) for tok in char_meta.get("lextoken", [])]
                    painter.setColors( (0,i), colors)

        gui.VCursor.setPos( self.mapToGlobal((self._visual_cursor_pos[0], self._visual_cursor_pos[1])))

    def scrollDownSlot(self):
        if not self._hasModels():
            return
        top_pos = self._buffer.viewModel().documentPosAtTop()
        new_pos = DocumentPos(top_pos.row+1, top_pos.column)
        self._buffer.viewModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollUpSlot(self):
        if not self._hasModels():
            return
        top_pos = self._buffer.viewModel().documentPosAtTop()
        new_pos = DocumentPos(top_pos.row-1, top_pos.column)
        self._buffer.viewModel().setDocumentPosAtTop(new_pos)
        self.update()

    def keyEvent(self, event):
        if not self._hasModels():
            return
        self._controller.handleKeyEvent(event)
        self.update()

    def focusInEvent(self, event):
        if not self._hasModels():
            return
        gui.VCursor.setPos(self.mapToGlobal((self._visual_cursor_pos[0], self._visual_cursor_pos[1])))

    def documentCursorPos(self):
        if not self._hasModels():
            return None

        top_pos = self._buffer.viewModel().documentPosAtTop()
        doc_pos = DocumentPos(top_pos.row+self._visual_cursor_pos.y, top_pos.column+self._visual_cursor_pos.x)
        if doc_pos.row > self._buffer.document().numLines():
            return None

        line_length = self._buffer.document().lineLength(doc_pos.row)
        if doc_pos.column > line_length+1:
            return None

        return doc_pos

    def handleDirectionalKey(self, event):
        if not self._hasModels():
            return

        if self._buffer.document().isEmpty():
            return

        key = event.key()

        direction = { vixtk.Key.Key_Up: flags.UP,
                      vixtk.Key.Key_Down: flags.DOWN,
                      vixtk.Key.Key_Left: flags.LEFT,
                      vixtk.Key.Key_Right: flags.RIGHT
                    }[key]

        self.moveCursor(direction)

    def moveCursor(self, direction):
        if not self._hasModels():
            return
        cursor_pos = self._visual_cursor_pos
        current_doc_pos = self.documentCursorPos()
        current_surrounding_lines_length = {}
        for offset in [-1, 0, 1]:
            line_num=current_doc_pos.row+offset
            if self._buffer.document().hasLine(line_num):
                current_surrounding_lines_length[offset] = self._buffer.document().lineLength(line_num)
            else:
                current_surrounding_lines_length[offset] = None

        mode_offset = 0 #if self._view_model.editorMode() == flags.INSERT_MODE else -1

        if direction == flags.UP:
            if current_surrounding_lines_length[-1] is None:
                return
            new_pos = CursorPos( min(cursor_pos.x, current_surrounding_lines_length[-1]+mode_offset),
                                 max(cursor_pos.y-1, 0)
                      )
            if cursor_pos.y-1 < 0:
                self.scrollUp.emit()

        elif direction == flags.DOWN:
            if current_surrounding_lines_length[1] is None:
                return
            new_pos = CursorPos(min(cursor_pos.x, current_surrounding_lines_length[1]+mode_offset),
                                min(cursor_pos.y+1, self.height()-1)
                      )
            if cursor_pos.y+1 >= self.height():
                self.scrollDown.emit()

        elif direction == flags.LEFT:
            new_pos = CursorPos(max(cursor_pos.x-1,0), cursor_pos.y)
        elif direction == flags.RIGHT:
            new_pos = CursorPos(min(cursor_pos.x+1,
                           current_surrounding_lines_length[0]+mode_offset,
                           self.width()-1),
                       cursor_pos.y
                       )
        elif direction == flags.HOME:
            new_pos = CursorPos(0, cursor_pos.y)
        elif direction == flags.END:
            new_pos = CursorPos(min(current_surrounding_lines_length[0], self.width()-1), cursor_pos.y)

        self._visual_cursor_pos = new_pos
        gui.VCursor.setPos( self.mapToGlobal((new_pos[0], new_pos[1])))
        self.cursorPositionChanged.emit(self.documentCursorPos())

