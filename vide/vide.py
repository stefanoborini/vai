import sys
import curses

import atexit

class KeyEvent(object):
    def __init__(self, key):
        self._key = key
    def key(self):
        return self._key

class VApplication(object):
    def __init__(self, argv):
        self._screen = curses.initscr()
        self._centralWidget = None
        atexit.register(self.exit)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.noecho()
        curses.cbreak()
        self._screen.keypad(1)

    def exec_(self):
        self.renderWidgets()
        while 1:
            c = self._screen.getch()
            event = KeyEvent(chr(c))
            self._central_widget.keyEvent(event)
            #self._screen.addch(1,1,c)
            self.renderWidgets()
            self._screen.refresh()
            # Check if screen was re-sized (True or False)
            y, x = self._screen.getmaxyx()
            resize = curses.is_term_resized(y, x)

            # Action in loop if resize is True:
            if resize is True:
                y, x = screen.getmaxyx()
                curses.resizeterm(y, x)
                self.renderWidgets()


    def exit(self):
        print "Exiting"
        curses.nocbreak()
        self._screen.keypad(0)
        curses.echo()
        curses.endwin()

    def setCentralWidget(self, widget):
        self._central_widget = widget

    def renderWidgets(self):
        self._central_widget.render(self._screen)
        self._screen.refresh()

    def screen(self):
        return self._screen

class VWidget(object):
    def __init__(self, parent=None):
        self._parent = parent
        parent.addChild(self)
        self._children = []

    def keyEvent(self, event):
        for child in self._children:
            child.keyEvent(event)
        return event

    def addChild(self, child):
        self._children.append(child)

class VLabel(VWidget):
    def __init__(self, label, parent=None):
        self._label = label
        self._color = None
        self._pos = (0,0)
        self._size = (10,10)

    def render(self, screen):
        w, h = self.size()
        x, y = self.pos()
        if self._color:
            for i in xrange(-h/2, 0):
                screen.addstr(y+i, x, ' '*w, curses.color_pair(self._color))
            screen.addstr(y, x, self._label + ' '*(w-len(self._label)), curses.color_pair(self._color))
            for i in xrange(1, h/2):
                screen.addstr(y+i, x, ' '*w, curses.color_pair(self._color))

    def pos(self):
        return self._pos
    def size(self):
        return self._size
    def setGeometry(self, x, y, w, h):
        self._pos = (x,y)
        min_size = self.minimumSize()
        self._size = (max(min_size[0], w) , max(min_size[1], h))

    def show(self):
        pass

    def setColor(self, color):
        self._color = color

    def keyEvent(self, event):
        self._label = self._label + event.key()

    def minimumSize(self):
        return (len(self._label), 1)

#class VTextArea


try:
    app = VApplication(sys.argv)

    label = VLabel("Pretty Text")
    label.setColor(1)
    app.setCentralWidget(label)
    label.setGeometry(30,30,20,10)
    label.show()

    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

