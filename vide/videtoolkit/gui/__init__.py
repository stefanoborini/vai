from .. import core
from .. import Key, KeyModifier, nativeToVideKeyCode, videKeyCodeToText
import logging
import sys
import os
import copy
import select
from .VApplication import VApplication
from .VColor import VColor
from .VPalette import VPalette
from .VScreen import VScreen

logging.basicConfig(filename='example.log',level=logging.DEBUG)



class VKeyEvent(object):
    def __init__(self, key_code):
        self._key_code = key_code
        self._accepted = False

    def keyCode(self):
        return self._key_code

    def key(self):
        return self._key_code & Key.Mask

    def modifiers(self):
        return self._key_code & KeyModifier.Mask

    def text(self):
        return videKeyCodeToText(self._key_code)

    def accept(self):
        self._accepted = True

    def accepted(self):
        return self._accepted

    @staticmethod
    def fromNativeKeyCode(native_key_code):
        key_code = nativeToVideKeyCode(native_key_code)
        return VKeyEvent(key_code)

class VPaintEvent(object):
    pass

class VPainter(object):
    def __init__(self, screen, widget):
        self._screen = screen
        self._widget = widget

    def write(self, x, y, string, fg_color=None, bg_color=None):
        widget_colors = self._widget.currentColors()
        if fg_color is None:
            fg_color = widget_colors[0]

        if bg_color is None:
            bg_color = widget_colors[1]

        abs_pos = self._widget.mapToGlobal(x, y)
        self._widget.palette()
        self._screen.write(abs_pos[0], abs_pos[1], string, fg_color, bg_color)

    def screen(self):
        return self._screen

    def clear(self, x, y, w, h):
        widget_colors = self._widget.currentColors()
        abs_pos = self._widget.mapToGlobal(x, y)
        for h_idx in xrange(h):
            self._screen.write(abs_pos[0], abs_pos[1]+h_idx, ' '*w, widget_colors[0], widget_colors[1])

class VHLayout(object):
    def __init__(self):
        self._widgets = []
        self._parent = None

    def addWidget(self, widget):
        self._widgets.append(widget)

    def apply(self):
        size = self.parent().size()
        available_size = size[0]/len(self._widgets)
        for i,w in enumerate(self._widgets):
            w.move(available_size*i,0)
            w.resize(available_size, size[1])

    def setParent(self, parent):
        self._parent = parent

    def parent(self):
        return self._parent

class VVLayout(object):
    def __init__(self):
        self._widgets = []
        self._parent = None

    def addWidget(self, widget):
        self._widgets.append(widget)

    def apply(self):
        size = self.parent().size()
        available_size = size[1]/len(self._widgets)
        remainder = size[1] % len(self._widgets)
        plot_pos = 0
        for i,w in enumerate(self._widgets):
            w.move(0, plot_pos)
            if remainder > 0:
                w.resize(size[0], available_size+1)
                remainder -= 1
                plot_pos += available_size + 1
            else:
                w.resize(size[0], available_size)
                plot_pos += available_size

    def setParent(self, parent):
        self._parent = parent

    def parent(self):
        return self._parent





class VWidget(core.VObject):
    def __init__(self, parent=None):
        super(VWidget, self).__init__(parent)
        if parent is None:
            VApplication.vApp.addTopLevelWidget(self)
            self._size = VApplication.vApp.screen().size()
            self.setFocus()
        else:
            self._size = self.parent().size()

        self._pos = (0,0)
        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True

    def keyEvent(self, event):
        if not event.accepted():
            self._parent.keyEvent(event)

    def setFocus(self):
        VApplication.vApp.setFocusWidget(self)

    def move(self, x, y):
        self._pos = (x,y)

    def resize(self, w, h):
        self._size = (w,h)

    def pos(self):
        return self._pos

    def size(self):
        return self._size

    def width(self):
        return self._size[0]

    def height(self):
        return self._size[1]

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def setVisible(self, visible):
        self._visible_explicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)

    def setVisibleImplicit(self, visible):
        self._visible_implicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)

    def isVisible(self):
        return self._visible_explicit if self._visible_explicit is not None else self._visible_implicit

    def minimumSize(self):
        return (1,1)

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, x, y, w, h):
        self._pos = (x,y)
        min_size = self.minimumSize()
        self._size = (max(min_size[0], w) , max(min_size[1], h))

    def mapToGlobal(self, x, y):
        if self.parent() is None:
            return (x+self._pos[0],y+self._pos[1])

        global_corner = self.parent().mapToGlobal(0,0)
        return (global_corner[0] + self.pos()[0] + x, global_corner[1] + self.pos()[1] + y)

    def render(self, painter):
        if not self.isVisible():
            return

        if self._layout is not None:
            self._layout.apply()

        w, h = self.size()
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)

        for i in xrange(0, h):
            painter.write(0, i, ' '*w, fg, bg)

        for w in self.children():
            child_painter = VPainter(painter.screen(), w)
            w.render(child_painter)

    def isEnabled(self):
        return self._enabled

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def setEnabled(self, enabled):
        self._enabled = enabled

    def palette(self):
        if self._palette is None:
            self._palette = VApplication.vApp.palette().copy()

        return self._palette

    def setColors(self, fg=None, bg=None):
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText, fg)
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.Window, bg)

    def colors(self, color_group = VPalette.ColorGroup.Active):

        fg = self.palette().color(color_group, VPalette.ColorRole.WindowText)
        bg = self.palette().color(color_group, VPalette.ColorRole.Window)

        return (fg, bg)

    def currentColors(self):
        if self.isActive():
            color_group = VPalette.ColorGroup.Active
        else:
            if isEnabled(self):
                color_group = VPalette.ColorGroup.Inactive
            else:
                color_group = VPalette.ColorGroup.Disabled
        return self.colors(color_group)

    def update(self):
        VApplication.vApp.postEvent(VPaintEvent())

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
    def __init__(self, label, parent=None):
        super(VLabel, self).__init__(parent)
        self._label = label

    def render(self, painter):
        super(VLabel, self).render(painter)
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

class VCursor(object):
    @staticmethod
    def setPos(x,y):
        VApplication.vApp.screen().setCursorPos(x,y)

    def pos(x,y):
        return VApplication.vApp.screen().cursorPos(x,y)





