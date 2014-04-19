from ... import FocusPolicy
from ... import core
from ... import Key
from ..VWidget import VWidget
from ..VPainter import VPainter
from ..VCursor import VCursor

class VLineEdit(VWidget):
    def __init__(self, contents="", parent=None):
        super(VLineEdit, self).__init__(parent)
        self._text = contents
        self._cursor_position = len(self._text)
        self._selection = None
        self._max_length = 32767
        self.setFocusPolicy(FocusPolicy.StrongFocus)

        self.returnPressed = core.VSignal(self)
        self.cursorPositionChanged = core.VSignal(self)
        self.textChanged = core.VSignal(self)
        self.selectionChanged = core.VSignal(self)
        self.editingFinished = core.VSignal(self)

    def maxLength(self):
        return self._max_length

    def setMaxLength(self, max_length):
        self._max_length = max_length
        self._text = self._text[:self._max_length]
        self.deselect()

    def cursorPosition(self):
        return self._cursor_position

    def setCursorPosition(self, position):
        old_pos = self._cursor_position
        self._cursor_position = position
        self.cursorPositionChanged.emit(old_pos, position)

    def setSelection(self, start, length):
        if len(self._text) == 0:
            return
        self._selection = (0, len(self._text))
        self.selectionChanged.emit()

    def selectAll(self):
        if len(self._text) == 0:
            return
        self._selection = (0, len(self._text))
        self.selectionChanged.emit()

    def selectionStart(self):
        pass

    def selectionEnd(self):
        pass

    def sizeHint(self):
        pass

    def deselect(self):
        self._selection = None
        self.selectionChanged.emit()

    def home(self):
        self._cursor_position = 0
        self.cursorPositionChanged.emit(old_pos, position)

    def end(self):
        self._cursor_position = len(self._text)
        self.cursorPositionChanged.emit(old_pos, position)

    def text(self):
        return self._text

    def setText(self, text):
        self.deselect()
        if text != self._text:
            self._text = text
            self.textChanged.emit(self._text)
            self.update()

    def backspace(self):
        if self._selection:
            pass
        else:
            pass

    def clear(self):
        self.setText("")
        self._cursor_position = 0

    def cursorForward(self, mark):
        pass

    def cursorBackward(self, mark):
        pass

    def cursorWordForward(self, mark):
        pass

    def cursorWordBackward(self, mark):
        pass

    def minimumSizeHint(self):
        return core.VSize(len(self._text), 1)

    def paintEvent(self, event):
        w, h = self.size()
        painter = VPainter(self)
        painter.drawText( core.VPoint(0, 0), self._text + ' '*(w-len(self._text)))
        if self.hasFocus():
            VCursor.setPos(self.mapToGlobal(core.VPoint(0,0)) + core.VPoint(self._cursor_position,0))

    def focusInEvent(self, event):
        VCursor.setPos(self.mapToGlobal(core.VPoint(0,0)) + core.VPoint(self._cursor_position,0))

    def keyEvent(self, event):
        if event.key() == Key.Key_Return:
            self.returnPressed.emit()
        elif event.key() == Key.Key_Left:
            self._cursor_position = max(0, self._cursor_position-1)
        elif event.key() == Key.Key_Right:
            self._cursor_position = min(len(self._text), self._cursor_position+1)
        elif event.key() == Key.Key_Backspace:
            if self._cursor_position == 0:
                event.accept()
                return
            self._cursor_position -= 1
            self._text = self._text[:self._cursor_position] + self._text[self._cursor_position+1:]
        else:
            self._text = self._text[:self._cursor_position] + event.text() +  self._text[self._cursor_position:]
            self._cursor_position += len(event.text())
        event.accept()
        self.update()

    def minimumSize(self):
        return core.VSize(len(self._text), 1)

    def selectedText(self):
        pass
