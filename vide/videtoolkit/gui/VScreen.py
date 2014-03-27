from . import VColor
import itertools
import curses
import select
import sys
import os

class VScreen(object):
    def __init__(self):
        os.environ["ESCDELAY"] = "25"
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

        self._cursor_pos = (0,0)
        self._initColors()
        self._initColorPairs()

    def deinit(self):
        curses.nocbreak()
        self._curses_screen.keypad(0)
        curses.echo()
        curses.endwin()

    def refresh(self):
        self._curses_screen.noutrefresh()
        curses.setsyx(self._cursor_pos[1], self._cursor_pos[0])
        curses.doupdate()


    def size(self):
        y, x = self._curses_screen.getmaxyx()
        return (x,y)

    def getch(self, *args):
        # Prevent to hold the GIL
        select.select([sys.stdin], [], [])
        return self._curses_screen.getch(*args)

    def write(self, x, y, string, fg_color=None, bg_color=None):
        size = self.size()
        if self.outOfBounds(x,y):
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
        try:
            return self._color_pairs.index( (fg_index, bg_index) )
        except:
            return self._color_pairs.index( (-1, -1) )

    def setCursorPos(self, x, y):
        if self.outOfBounds(x,y):
            return

        self._cursor_pos = (x,y)

    def cursorPos(self):
        return self._cursor_pos
        #pos = self._curses_screen.getyx()
        #return pos[1], pos[0]

    def _initColors(self):
        self._colors = []
        for c in xrange(self.numColors()):
             self._colors.append(VColor.VColor(VColor.cursesRgbToRgb(curses.color_content(c))))

    def _initColorPairs(self):
        # Init color pairs
        counter = 1
        self._color_pairs = [ (-1, -1) ]
        for bg in range(0, self.numColors(), 2):
            for fg in range(0, self.numColors(), 2):
                if fg == 0 and bg == 0:
                    continue
                self._color_pairs.append((fg, bg))
                try:
                    curses.init_pair(counter, fg, bg)
                except:
                    raise Exception(str(counter))
                    pass
                counter += 1

    def _findClosestColorIndex(self, color):
        closest = sorted([(VColor.distance(color, screen_color),
                           index)
                           for index, screen_color in enumerate(self._colors)
                         ],
                         key=lambda x: x[0]
                         )[0]

        return closest[1]

    def outOfBounds(self, x, y):
        return (x >= self.size()[0] or y >= self.size()[1] or x < 0 or y < 0)

class VScreenArea(object):
    def __init__(self, screen, abs_x, abs_y, w, h):
        self._screen = screen
        self._topleft_coords = (abs_x, abs_y)
        self._size = (w, h)

    def write(self, rel_x, rel_y, string, fg_color=None, bg_color=None):
        size = self.size()
        if rel_x >= size[0] or rel_y >= size[1]:
            return

        if rel_x < 0 or rel_y < 0:
            return

        if (rel_x+len(string) >= size[0]):
            string = string[:size[0]-rel_x]

        self._screen.write(rel_x+self._topleft_coords[0],
                           rel_y+self._topleft_coords[1],
                           string,
                           fg_color,
                           bg_color)

    def size(self):
        return self._size

    def screen(self):
        return self._screen

    def clear(self):
        for y in xrange(self._size[1]):
            self.write(0, y, ' '*self._size[0])

class DummyVScreen(object):
    def __init__(self, w, h):
        self._cursor_pos = (0,0)
        self._render_output = []
        self._size = (w, h)
        self._text = ""
        for h in xrange(self._size[1]):
            row = []
            self._render_output.append(row)
            for w in xrange(self._size[0]):
                row.append('.')

        self._log = []
        self._log.append("Inited screen")
    def deinit(self):
        self._log.append("Deinited screen")

    def refresh(self):
        self._log.append("Refresh")
        print self

    def size(self):
        return self._size

    def cursorPos(self):
        return self._cursor_pos

    def setCursorPos(self, x, y):
        self._cursor_pos = (x,y)

    def addstr(self, *args):
        pass

    def getch(self, *args):
        if len(self._text) == 0:
            return -1
        char_ret, self._text = self._text[0], self._text[1:]

        return char_ret

    def typeText(self, text):
        self._text = text

    def getColor(self, fg, bg):
        return 0

    def write(self, x, y, string, fg_color=None, bg_color=None):
        for pos in xrange(len(string)):
            try:
                self._render_output[y][x+pos] = string[pos]
            except:
                pass
    def dump(self):
        ret = []
        ret.append(" "+"".join(list(itertools.islice(itertools.cycle(map(str, range(10))), self._size[0]+1))))
        #print "+"*(self._size[0]+2)
        for i, r in enumerate(self._render_output):
            ret.append(str(i%10)+''.join(r)+"+")
        ret.append( "+"*(self._size[0]+2))
        return ret

    def __str__(self):
        return "\n".join(self.dump())

    def charAt(self, x, y):
        return self._render_output[y][x]

    def stringAt(self, x, y, l):
        return ''.join(self._render_output[y][x:x+l])


