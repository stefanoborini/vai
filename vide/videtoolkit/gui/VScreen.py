from . import VColor

import curses
import select
import sys

class VScreen(object):
    def __init__(self):
        self._curses_screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        self._curses_screen.keypad(1)
        self._curses_screen.nodelay(False)
        self._curses_screen.leaveok(True)
        self._curses_screen.notimeout(True)

        self._initColors()
        self._initColorPairs()

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
        # Prevent to hold the GIL
        select.select([sys.stdin], [], [])
        return self._curses_screen.getch(*args)

    def write(self, x, y, string, fg_color=None, bg_color=None):
        size = self.size()
        if x >= size[0] or y >= size[1]:
            return

        color_pair = self.getColorPair(fg_color, bg_color)
        if (x+len(string) >= size[0]):
            string = string[:size[0]-x]
            self._curses_screen.addstr(y, x, string[1:], curses.color_pair(color_pair))
            self._curses_screen.insstr(y, x, string[0], curses.color_pair(color_pair))
        else:
            self._curses_screen.addstr(y, x, string, curses.color_pair(color_pair))

    def numColors(self):
        return curses.COLORS

    def supportedColors(self):
        return self._colors

    def getColorPair(self, fg=None, bg=None):
        fg_index = -1 if fg is None else self._findClosestColorIndex(fg)
        bg_index = -1 if bg is None else self._findClosestColorIndex(bg)

        if fg_index == 0 and bg_index == 0:
            return self._color_pairs.index( (-1, -1) )
        return self._color_pairs.index( (fg_index, bg_index) )

    def setCursorPos(self, x, y):
        curses.setsyx(y,x)
        self._curses_screen.move(y,x)
        self.refresh()

    def cursorPos(self):
        pos = self._curses_screen.getyx()
        return pos[1], pos[0]

    def _initColors(self):
        self._colors = []
        for c in xrange(self.numColors()):
             self._colors.append(VColor.VColor(VColor.cursesRgbToRgb(curses.color_content(c))))

    def _initColorPairs(self):
        # Init color pairs
        counter = 1
        self._color_pairs = [ (-1, -1) ]
        for bg in range(0, self.numColors()):
            for fg in range(0, self.numColors()):
                if fg == 0 and bg == 0:
                    continue
                self._color_pairs.append((fg, bg))
                curses.init_pair(counter, fg, bg)
                counter += 1

    def _findClosestColorIndex(self, color):
        closest = sorted([(VColor.distance(color, screen_color),
                           index)
                           for index, screen_color in enumerate(self._colors)
                         ],
                         key=lambda x: x[0]
                         )[0]

        return closest[1]

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


