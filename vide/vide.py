import time
import sys
import curses

import atexit

class VSignal(object):
    def __init__(self, sender):
        self._sender = sender
        self._slots = []

    def connect(self, slot):
        self._slots.append(slot)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)


class VKeyEvent(object):
    def __init__(self, key):
        self._key = key
        self._accepted = False
    def key(self):
        return self._key
    def accept(self):
        self._accepted = True
    def accepted(self):
        return self._accepted

class VScreen(object):
    def __init__(self):
        self._curses_screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.noecho()
        curses.cbreak()
        self._curses_screen.keypad(1)
        self._curses_screen.nodelay(True)

    def deinit(self):
        curses.nocbreak()
        self._curses_screen.keypad(0)
        curses.echo()
        curses.endwin()

    def refresh(self):
        self._curses_screen.refresh()

    def size(self):
        y, x = self._curses_screen.getmaxyx()
        return (x,y)

    def addstr(self, *args):
        self._curses_screen.addstr(*args)

    def getch(self, *args):
        return self._curses_screen.getch(*args)

class VObject(object):
    def __init__(self, parent = None):
        self._parent = parent
        self._children = []
        if self._parent is not None:
            parent.addChild(self)

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def addChild(self, child):
        self._children.append(child)

    @staticmethod
    def connect(signal, slot):
        signal.connect(slot)

class VApplication(VObject):
    vApp = None

    def __init__(self, argv):
        super(VApplication, self).__init__()
        self._screen = VScreen()
        self._top_level_widget = None
        self._focused_widget = None
        self._timers = []

        if VApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VApplication.vApp = self
        atexit.register(self.exit)

    def exec_(self):
        self.renderWidgets()
        while 1:
            c = self._screen.getch()
            if c < 0:
                for t in self._timers:
                    t.heartbeat()
                self.renderWidgets()
                continue
            event = VKeyEvent(unichr(c))
            if self.focusedWidget():
                self.focusedWidget().keyEvent(event)
            #self._screen.addch(1,1,c)
            self.renderWidgets()
            # Check if screen was re-sized (True or False)
            x,y = self._screen.size()
            resize = curses.is_term_resized(y, x)

            # Action in loop if resize is True:
            if resize is True:
                x, y = self._screen.size()
                curses.resizeterm(y, x)
                self.renderWidgets()

    def exit(self):
        print "Exiting"
        self._screen.deinit()

    def setTopLevelWidget(self, widget):
        self._top_level_widget = widget

    def renderWidgets(self):
        self._top_level_widget.render()
        self._screen.refresh()

    def screen(self):
        return self._screen

    def setFocusWidget(self, widget):
        self._focused_widget = widget

    def focusedWidget(self):
        return self._focused_widget

    def addTimer(self, timer):
        self._timers.append(timer)

class VWidget(VObject):
    def __init__(self, parent=None):
        super(VWidget, self).__init__(parent)
        if parent is None:
            VApplication.vApp.setTopLevelWidget(self)

    def keyEvent(self, event):
        if not event.accepted():
            self._parent.keyEvent(event)

    def setFocus(self):
        VApplication.setFocusWidget(self)

    def move(self, x, y):
        self._pos = (x,y)

    def pos(self):
        return self._pos

    def size(self):
        return self._size

    def show(self):
        pass

    def setGeometry(self, x, y, w, h):
        self._pos = (x,y)
        min_size = self.minimumSize()
        self._size = (max(min_size[0], w) , max(min_size[1], h))

class VLabel(VWidget):
    def __init__(self, label, parent=None):
        super(VLabel, self).__init__(parent)
        self._label = label
        self._color = None
        self._pos = (0,0)
        self._size = (10,10)

    def render(self):
        screen = VApplication.vApp.screen()
        w, h = self.size()
        x, y = self.pos()
        if self._color:
            for i in xrange(-h/2, 0):
                screen.addstr(y+i, x, ' '*w, curses.color_pair(self._color))
            screen.addstr(y, x, self._label + ' '*(w-len(self._label)), curses.color_pair(self._color))
            for i in xrange(1, h/2):
                screen.addstr(y+i, x, ' '*w, curses.color_pair(self._color))

    def setColor(self, color):
        self._color = color

    def keyEvent(self, event):
        self._label = self._label + event.key()
        event.accept()

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        self._label = text

class VTabWidget(VWidget):
    def __init__(self, parent=None):
        super(VTabWidget, self).__init__(parent)
        self._tabs = []
        self._selected_tab_idx = -1

    def addTab(self, widget, label):
        self._tabs.append((widget, label))
        self._selected_tab_idx = 2

    def render(self):
        screen = VApplication.vApp.screen()
        w, h = screen.size()
        if len(self._tabs):
            tab_size = w/len(self._tabs)
            header = ""
            for index, (_, label) in enumerate(self._tabs):
                header = label+" "*(tab_size-len(label))
                screen.addstr(0, tab_size * index, header, curses.color_pair(1 if index == self._selected_tab_idx else 0))
            widget = self._tabs[self._selected_tab_idx][0]
            widget.render()

class VTimer(VObject):
    def __init__(self, timeout):
        self._start_time = None
        self._timeout = timeout
        self.timeout = VSignal(self)
        VApplication.vApp.addTimer(self)

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._start_time = None

    def heartbeat(self):
        if self._start_time is None:
            return

        if time.time() - self._start_time > self._timeout:
            self._start_time = time.time()
            self.timeout.emit()


#class VTextArea


try:
    app = VApplication(sys.argv)

    tabwidget = VTabWidget()
    label = VLabel("Pretty Text", tabwidget)
    tabwidget.addTab(label, "foo")
    tabwidget.addTab(label, "bar")
    tabwidget.addTab(label, "baz")
    tabwidget.addTab(label, "baww")
    label.setColor(1)
    label.setGeometry(30,30,20,10)
    tabwidget.show()

    timer = VTimer(1)
    timer.timeout.connect(lambda: label.setText(str(time.time())))
    timer.start()
    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

