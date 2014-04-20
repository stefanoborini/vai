import videtoolkit
from videtoolkit import gui, core
from .EditorController import EditorController
from .positions import CursorPos, DocumentPos
from . import flags

class EditArea(gui.VWidget):
    def __init__(self, document_model, view_model, parent):
        super(EditArea, self).__init__(parent)

        self._controller = EditorController(document_model, view_model, self)

        self._document_model = document_model
        self._view_model = view_model
        self._cursor_pos = CursorPos(0,0)
        self.setFocusPolicy(videtoolkit.FocusPolicy.StrongFocus)

        self.scrollDown = core.VSignal(self)
        self.scrollDown.connect(self.scrollDownSlot)
        self.scrollUp = core.VSignal(self)
        self.scrollUp.connect(self.scrollUpSlot)

        self.cursorPositionChanged = core.VSignal(self)

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        painter.erase()
        for i in range(0, h):
            document_line = self._view_model.documentPosAtTop().row + i
            if document_line < self._document_model.numLines():
                painter.drawText( (0, i), self._document_model.getLine(document_line).replace('\n', ' '))

        gui.VCursor.setPos( self.mapToGlobal((self._cursor_pos[0], self._cursor_pos[1])))

    def scrollDownSlot(self):
        top_pos = self._view_model.documentPosAtTop()
        new_pos = DocumentPos(top_pos.row+1, top_pos.column)
        self._view_model.setDocumentPosAtTop(new_pos)
        self.update()

    def scrollUpSlot(self):
        top_pos = self._view_model.documentPosAtTop()
        new_pos = DocumentPos(top_pos.row-1, top_pos.column)
        self._view_model.setDocumentPosAtTop(new_pos)
        self.update()

    def cursorPos(self):
        return self._cursor_pos

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)
        self.update()

    def focusInEvent(self, event):
        gui.VCursor.setPos(self.mapToGlobal((self._cursor_pos[0], self._cursor_pos[1])))

    def documentPos(self):
        top_pos = self._view_model.documentPosAtTop()
        doc_pos = DocumentPos(top_pos.row+self.cursorPos().y, top_pos.column+self.cursorPos().x)
        if doc_pos.row > self._document_model.numLines():
            return None

        line_length = self._document_model.lineLength(doc_pos.row)
        if doc_pos.column > line_length+1:
            return None

        return doc_pos

    def handleDirectionalKey(self, event):
        if self._document_model.isEmpty():
            return

        key = event.key()

        direction = { videtoolkit.Key.Key_Up: flags.UP,
                      videtoolkit.Key.Key_Down: flags.DOWN,
                      videtoolkit.Key.Key_Left: flags.LEFT,
                      videtoolkit.Key.Key_Right: flags.RIGHT
                    }[key]

        self.moveCursor(direction)

    def moveCursor(self, direction):
        cursor_pos = self.cursorPos()
        current_doc_pos = self.documentPos()
        current_surrounding_lines_length = {}
        for offset in [-1, 0, 1]:
            line_num=current_doc_pos.row+offset
            if self._document_model.hasLine(line_num):
                current_surrounding_lines_length[offset] = self._document_model.lineLength(line_num)
            else:
                current_surrounding_lines_length[offset] = None

        mode_offset = 0 if self._view_model.editorMode() == flags.INSERT_MODE else -1

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

        self._cursor_pos = new_pos
        #new_doc_pos = self.cursorToDocumentPos(new_pos)
        #self._status_bar.setPosition(new_doc_pos)
        gui.VCursor.setPos( self.mapToGlobal((new_pos[0], new_pos[1])))
        self.cursorPositionChanged.emit(self.documentPos())

