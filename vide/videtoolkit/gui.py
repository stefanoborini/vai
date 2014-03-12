from . import core
import sys
import curses
import os

class VKeyEvent(object):
    def __init__(self, key):
        self._key = key
        self._accepted = False
    def key(self):
        return self._key
    def keyUnicode(self):
        return unichr(self._key)
    def accept(self):
        self._accepted = True
    def accepted(self):
        return self._accepted

class VPainter(object):
    def __init__(self, screen, widget):
        self._screen = screen
        self._widget = widget

    def write(self, x, y, string, color):
        abs_pos = self._widget.mapToGlobal(x, y)
        self._screen.write(abs_pos[0], abs_pos[1], string, color)

    def screen(self):
        return self._screen

class VScreen(object):
    def __init__(self):
        self._curses_screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()

        self._curses_screen.keypad(1)
        self._curses_screen.nodelay(True)
        self._curses_screen.leaveok(True)
        self._curses_screen.notimeout(True)
        counter = 1
        self._colormap = [ (-1, -1) ]
        for bg in range(0, self.numColors()):
            for fg in range(0, self.numColors()):
                if fg == 0 and bg == 0:
                    continue
                self._colormap.append((fg, bg))
                curses.init_pair(counter, fg, bg)
                counter += 1

    def deinit(self):
        curses.nocbreak()
        self._curses_screen.keypad(0)
        curses.echo()
        curses.endwin()

    def leaveok(self, flag):
        self._curses_screen.leaveok(flag)

    def refresh(self):
        self._curses_screen.refresh()

    def size(self):
        y, x = self._curses_screen.getmaxyx()
        return (x,y)

    def getch(self, *args):
        return self._curses_screen.getch(*args)

    def write(self, x, y, string, color):
        size = self.size()
        if x >= size[0] or y >= size[1]:
            return

        if (x+len(string) >= size[0]):
            string = string[:size[0]-x]
            self._curses_screen.addstr(y,x,string[1:], color)
            self._curses_screen.insstr(y, x, string[0], color)
        else:
            self._curses_screen.addstr(y,x,string, color)

    def numColors(self):
        return curses.COLORS

    def getColor(self, fg, bg):
        return self._colormap.index( (fg, bg) )

    def setCursorPos(self, x, y):
        curses.setsyx(y,x)
        self._curses_screen.move(y,x)
        self.refresh()

    def cursorPos(self):
        pos = self._curses_screen.getyx()
        return pos[1], pos[0]

class DummyVScreen(object):
    def __init__(self):
        self._cursor_pos = (0,0)
        self._render_output = []
        self._size = (60, 25)
        for h in xrange(self._size[1]):
            row = []
            self._render_output.append(row)
            for w in xrange(self._size[0]):
                row.append(' ')

        self._log = []
        self._log.append("Inited screen")
    def deinit(self):
        self._log.append("Deinited screen")

    def refresh(self):
        self._log.append("Refresh")

    def size(self):
        return self._size

    def cursorPos(self):
        return self._cursor_pos

    def setCursorPos(self, x, y):
        self._cursor_pos = (x,y)

    def leaveok(self, flag):
        pass

    def addstr(self, *args):
        pass

    def getch(self, *args):
        return -1

    def getColor(self, fg, bg):
        return 0

    def write(self, x, y, string, color):
        for pos in xrange(len(string)):
            try:
                self._render_output[y][x+pos] = string[pos]
            except:
                pass
    def dump(self):
        print "+"*(self._size[0]+2)
        for r in self._render_output:
            print "+"+''.join(r)+"+"
        print "+"*(self._size[0]+2)

    def charAt(self, x, y):
        return self._render_output[y][x]

    def stringAt(self, x, y, l):
        return ''.join(self._render_output[y][x:x+l])

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

class VApplication(core.VCoreApplication):
    def __init__(self, argv, screen=None):
        super(VApplication, self).__init__(argv)
        os.environ["ESCDELAY"] = "25"
        if screen:
            self._screen = screen
        else:
            self._screen = VScreen()

        self._top_level_widget = None
        self._focused_widget = None

    def exec_(self):
        self.renderWidgets()
        while 1:
            self.processEvents()

    def processEvents(self):
        c = self._screen.getch()
        if c < 0:
            for t in self._timers:
                t.heartbeat()
            self.renderWidgets()
            return
        elif c == 27:
            next_c = self._screen.getch()
            if next_c == -1:
                pass

        event = VKeyEvent(c)
        if self.focusedWidget():
            self.focusedWidget().keyEvent(event)
        self._screen.leaveok(False)
        #self._screen.addch(1,1,c)
        self.renderWidgets()
        # Check if screen was re-sized (True or False)
        x,y = self._screen.size()
        #resize = curses.is_term_resized(y, x)

        # Action in loop if resize is True:
        #if resize is True:
            #x, y = self._screen.size()
            #curses.resizeterm(y, x)
            #self.renderWidgets()

    def exit(self):
        super(VApplication, self).exit()
        self._screen.deinit()

    def setTopLevelWidget(self, widget):
        self._top_level_widget = widget

    def renderWidgets(self):
        curpos=self._screen.cursorPos()
        painter = VPainter(self._screen, self._top_level_widget)
        self._top_level_widget.render(painter)
        self._screen.setCursorPos(*curpos)
        self._screen.refresh()

    def screen(self):
        return self._screen

    def setFocusWidget(self, widget):
        self._focused_widget = widget

    def focusedWidget(self):
        return self._focused_widget

class VWidget(core.VObject):
    def __init__(self, parent=None):
        super(VWidget, self).__init__(parent)
        if parent is None:
            VApplication.vApp.setTopLevelWidget(self)
            self._size = VApplication.vApp.screen().size()
            self.setFocus()
        else:
            self._size = self.parent().size()

        self._pos = (0,0)
        self._layout = None
        self._color = 0

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

    def show(self):
        pass

    def setColor(self, color):
        self._color = color

    def color(self):
        return self._color

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, x, y, w, h):
        self._pos = (x,y)
        min_size = self.minimumSize()
        self._size = (max(min_size[0], w) , max(min_size[1], h))

    def mapToGlobal(self, x, y):
        if self.parent() is None:
            return (x,y)

        global_corner = self.parent().mapToGlobal(0,0)
        return (global_corner[0] + x, global_corner[1] + y)

    def render(self, painter):
        if self._layout is not None:
            self._layout.apply()

        for w in self.children():
            child_painter = VPainter(painter.screen(), w)
            w.render(child_painter)

class VFrame(VWidget):
    def __init__(self, parent=None):
        super(VFrame, self).__init__(parent)

    def render(self, painter):
        w, h = self.size()
        painter.write(0, 0, '+'+"-"*(w-2)+"+", self._color)
        for i in xrange(0, h-2):
            painter.write(0, i+1, '|'+' '*(w-2)+"|", self._color)
        painter.write(0, h-1, '+'+"-"*(w-2)+"+", self._color)

        super(VFrame, self).render(painter)

class VLabel(VWidget):
    def __init__(self, label, parent=None):
        super(VLabel, self).__init__(parent)
        self._label = label

    def render(self, painter):
        super(VLabel, self).render(painter)
        w, h = self.size()
        for i in xrange(0, h/2):
            painter.write(0, i, ' '*w, self._color)
        painter.write(0, h/2, self._label + ' '*(w-len(self._label)), self._color)
        for i in xrange(1+h/2, h):
            painter.write(0, i, ' '*w, self._color)

    def keyEvent(self, event):
        self._label = self._label + event.key()
        event.accept()

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        self._label = text

class VPushButton(VWidget):
    def __init__(self, label, parent=None):
        super(VPushButton, self).__init__(parent)
        self._label = label
        self.setColor(1)

    def render(self, painter):
        super(VPushButton, self).render(painter)
        for i in xrange(0, h/2):
            painter.write(0, i, ' '*w, self._color)
        painter.write(0, h/2, "[ "+self._label + " ]"+ ' '*(w-len(self._label)-4), curses.color_pair(self._color))
        for i in xrange(1+h/2, h):
            painter.write(0, i, ' '*w, curses.color_pair(self._color))

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
    def move(x,y):
        VApplication.vApp.screen().setCursorPos(x,y)

