from ... import core
from ... import Key, KeyModifier, nativeToVideKeyCode, videKeyCodeToText
import logging
import sys
import os
import copy
import select
from ..VApplication import VApplication
from ..VColor import VColor
from ..VPalette import VPalette
from ..VScreen import VScreen
from ..VPainter import VPainter
from ..VWidget import VWidget

class VFrame(VWidget):
    def __init__(self, parent=None):
        super(VFrame, self).__init__(parent)

    def render(self, painter):
        w, h = self.size()
        painter.write(0, 0, '+'+"-"*(w-2)+"+")
        for i in xrange(0, h-2):
            painter.write(0, i+1, '|'+' '*(w-2)+"|")
        painter.write(0, h-1, '+'+"-"*(w-2)+"+")

        super(VFrame, self).render(painter)

class VDialog(VWidget):
    def __init__(self, parent=None):
        super(VDialog, self).__init__(parent)
        self._title = None

    def render(self, painter):
        if not self.isVisible():
            return

        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)
        w, h = self.size()
        if self._title:

            #0123456789012
            #+-| hello |-+
            dash_length = (w -                  # total width of the dialog
                           2 -                  # space for the angles
                           len(self._title) -   # the space for the title itself
                           2 -                  # the two empty spaces on the sides of the title
                           2)                   # the vertical bars
            header = '+' + \
                     "-"*(dash_length/2) + \
                     "| " + \
                     self._title + \
                     " |" + \
                     "-"*(dash_length-(dash_length/2)) + \
                     "+"
        else:
            header = '+'+"-"*(w-2)+"+"

        painter.write(0, 0, header, fg, bg)

        for i in xrange(0, h-2):
            painter.write(0, i+1, '|'+' '*(len(header)-2)+"|", fg, bg)
        painter.write(0, h-1, '+'+"-"*(len(header)-2)+"+", fg, bg)

    def setTitle(self, title):
        self._title = title

    def minimumSize(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2,2)

class VLabel(VWidget):
    def __init__(self, label="", parent=None):
        super(VLabel, self).__init__(parent)
        self._label = label

    def paintEvent(self, event):
        #super(VLabel, self).render(painter)
        painter = VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.WindowText)
        bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.Window)
        for i in xrange(0, h/2):
            painter.write(0, i, ' '*w, fg_color, bg_color)
        painter.write(0, h/2, self._label + ' '*(w-len(self._label)), fg_color, bg_color)
        for i in xrange(1+h/2, h):
            painter.write(0, i, ' '*w, fg_color, bg_color)

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        if text != self._label:
            self._label = text
            self.update()

class VLineEdit(VWidget):
    def __init__(self, contents="", parent=None):
        super(VLineEdit, self).__init__(parent)
        self._text = contents
        self._cursor_position = len(self._text)
        self._selection = None
        self._max_length = 32767

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

    def backspace(self):
        if self._selection:
            pass
        else:
            pass

    def clear(self):
        self.setText("")

    def cursorForward(self, mark):
        pass

    def cursorBackward(self, mark):
        pass

    def cursorWordForward(self, mark):
        pass

    def cursorWordBackward(self, mark):
        pass

    def minimumSizeHint(self):
        return (1, 1)

    def render(self, painter):
        super(VLineEdit, self).render(painter)
        w, h = self.size()
        painter.write(0, 0, self._text + ' '*(w-len(self._text)))

        VCursor.setPos(self.mapToGlobal(0,0)[0]+self._cursor_position,self.mapToGlobal(0,0)[1])

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
        return (1, 1)

    def selectedText(self):
        pass

class VPushButton(VWidget):
    def __init__(self, label, parent=None):
        super(VPushButton, self).__init__(parent)
        self._label = label

    def render(self, painter):
        super(VPushButton, self).render(painter)
        for i in xrange(0, h/2):
            painter.write(0, i, ' '*w)
        painter.write(0, h/2, "[ "+self._label + " ]"+ ' '*(w-len(self._label)-4))
        for i in xrange(1+h/2, h):
            painter.write(0, i, ' '*w)

class VTabWidget(VWidget):
    def __init__(self, parent=None):
        super(VTabWidget, self).__init__(parent)
        self._tabs = []
        self._selected_tab_idx = -1

    def addTab(self, widget, label):
        self._tabs.append((widget, label))
        self._selected_tab_idx = 2

    def render(self, screen):
        screen = VApplication.vApp.screen()
        w, h = screen.size()
        if len(self._tabs):
            tab_size = w/len(self._tabs)
            header = ""
            for index, (_, label) in enumerate(self._tabs):
                header = label+" "*(tab_size-len(label))
                screen.write(tab_size * index, 0, header, curses.color_pair(1 if index == self._selected_tab_idx else 0))
            widget = self._tabs[self._selected_tab_idx][0]
            widget.render(screen)

