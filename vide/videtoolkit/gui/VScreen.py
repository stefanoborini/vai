from . import VColor
import itertools
import curses
import select
import sys
import os
import logging
import threading

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
        self._curses_screen.nodelay(True)
        self._curses_screen.leaveok(True)
        self._curses_screen.notimeout(True)
        self._curses_lock = threading.Lock()
        self._color_lookup_cache = {}

        self._cursor_pos = (0,0)
        self._initColorPairs()

    def deinit(self):
        curses.nocbreak()
        self._curses_screen.keypad(0)
        curses.echo()
        curses.endwin()

    def refresh(self):
        with self._curses_lock:
            self._curses_screen.noutrefresh()
            curses.setsyx(self._cursor_pos[1], self._cursor_pos[0])
            curses.doupdate()

    def rect(self):
        return self.topLeft() + self.size()

    def size(self):
        with self._curses_lock:
            y, x = self._curses_screen.getmaxyx()
        return (x,y)

    def topLeft(self):
        return (0,0)

    def width(self):
        return self.size()[0]

    def height(self):
        return self.size()[1]

    def getKeyCode(self):
        # Prevent to hold the GIL
        select.select([sys.stdin], [], [])

        with self._curses_lock:
            c = self._curses_screen.getch()
            if c == 27:
                next_c = self._curses_screen.getch()
                if next_c == -1:
                    pass

        return c

    def write(self, pos, string, fg_color=None, bg_color=None):
        x,y = pos
        w,h = self.size()

        out_string = string

        if y < 0 or y >= h or x >= w:
            logging.info("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            return

        out_string = out_string[:w-x]

        if x < 0:
            logging.info("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = string[-x:]

        if len(out_string) == 0:
            return

        attr = self.getColorAttributes(fg_color, bg_color)
        if (x+len(out_string) > w):
            logging.info("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = out_string[:w-x]

        if (x+len(out_string) == w):
            with self._curses_lock:
                self._curses_screen.addstr(y, x, out_string[1:], attr)
                self._curses_screen.insstr(y, x, out_string[0], attr)
        else:
            with self._curses_lock:
                self._curses_screen.addstr(y, x, out_string, attr)

    def numColors(self):
        return min(curses.COLORS, 8)

    def getColorAttributes(self, fg=None, bg=None):
        fg_screen = None if fg is None else self._findClosestColor(fg)
        bg_screen = None if bg is None else self._findClosestColor(bg)

        fg_index = -1 if fg_screen is None else fg_screen.colorIdx()
        bg_index = -1 if bg_screen is None else bg_screen.colorIdx()

        try:
            pair_index = self._color_pairs.index( (fg_index, bg_index) )
        except:
            pair_index = self._color_pairs.index( (-1, -1) )

        with self._curses_lock:
            attr = curses.color_pair(pair_index)

        if fg_screen.attr():
            attr |= fg_screen.attr()

        return attr

    def setCursorPos(self, pos):
        if self.outOfBounds(pos):
            logging.info("out of bound in Screen.setCursorPos: %s" % str(pos))
            return

        self._cursor_pos = pos

    def cursorPos(self):
        return self._cursor_pos

    def _initColorPairs(self):
        # Init color pairs
        counter = 1
        self._color_pairs = [ (-1, -1) ]
        for bg in range(self.numColors()):
            for fg in range(self.numColors()):
                if fg == 0 and bg == 0:
                    continue
                self._color_pairs.append((fg, bg))
                try:
                    curses.init_pair(counter, fg, bg)
                except:
                    pass
                counter += 1

    def _findClosestColor(self, color):
        screen_color = self._color_lookup_cache.get(color.rgb())
        if screen_color is not None:
            return screen_color

        closest = sorted([(VColor.distance(color, screen_color),
                           screen_color)
                           for index, screen_color in enumerate(VGlobalScreenColor.allColors())
                         ],
                         key=lambda x: x[0]
                         )[0]
        self._color_lookup_cache[color.rgb()] = closest[1]
        return closest[1]

    def outOfBounds(self, pos):
        x, y = pos
        return (x >= self.size()[0] or y >= self.size()[1] or x < 0 or y < 0)

class VScreenColor(object):
    def __init__(self, color_idx, attr, equiv_rgb):
        self._color_idx = color_idx
        self._attr = attr
        self._equiv_rgb = equiv_rgb

    def attr(self):
        return self._attr

    def colorIdx(self):
        return self._color_idx

    def equivRgb(self):
        return self._equiv_rgb

    def r(self):
        return self._equiv_rgb[0]
    def g(self):
        return self._equiv_rgb[1]
    def b(self):
        return self._equiv_rgb[2]

class VGlobalScreenColor(object):
    black        = VScreenColor(curses.COLOR_BLACK, None, (0,0,0))
    darkred      = VScreenColor(curses.COLOR_RED, None, (170,0,0))
    darkgreen    = VScreenColor(curses.COLOR_GREEN, None, (0, 170, 0))
    brown        = VScreenColor(curses.COLOR_YELLOW, None, (170, 170, 0))
    darkblue     = VScreenColor(curses.COLOR_BLUE, None, (0, 0, 170))
    darkmagenta  = VScreenColor(curses.COLOR_MAGENTA, None, (170, 0, 170))
    darkcyan     = VScreenColor(curses.COLOR_CYAN, None, (0, 170, 170))
    lightgray    = VScreenColor(curses.COLOR_WHITE, None, (170, 170, 170))

    darkgray     = VScreenColor(curses.COLOR_BLACK, curses.A_BOLD, (100, 100, 100))
    lightred     = VScreenColor(curses.COLOR_RED, curses.A_BOLD, (255,0,0))
    lightgreen   = VScreenColor(curses.COLOR_GREEN, curses.A_BOLD, (0, 255, 0))
    yellow       = VScreenColor(curses.COLOR_YELLOW, curses.A_BOLD, (255, 255, 0))
    lightblue    = VScreenColor(curses.COLOR_BLUE, curses.A_BOLD, (0, 0, 255))
    lightmagenta = VScreenColor(curses.COLOR_MAGENTA, curses.A_BOLD, (255, 0, 255))
    lightcyan    = VScreenColor(curses.COLOR_CYAN, curses.A_BOLD, (0, 255, 255))
    white        = VScreenColor(curses.COLOR_WHITE, curses.A_BOLD, (255,255,255))

    red          = lightred
    green        = lightgreen
    blue         = lightblue
    magenta      = lightmagenta
    cyan         = lightcyan
    gray         = lightgray

    @classmethod
    def allColors(cls):
        return [c for c in list(cls.__dict__.values()) if isinstance(c, VScreenColor)]



class VScreenArea(object):
    def __init__(self, screen, rect):
        self._screen = screen
        self._rect = rect

    def write(self, pos, string, fg_color=None, bg_color=None):
        rel_x, rel_y = pos
        w, h = self.size()

        if rel_y < 0 or rel_y >= h or rel_x >= w:
            logging.info("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            return

        out_string = string
        if rel_x < 0:
            logging.info("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = string[-rel_x:]

        if len(out_string) == 0:
            return

        if (rel_x+len(out_string) > w):
            logging.info("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = out_string[:w-rel_x]

        self._screen.write( (rel_x+self.topLeft()[0], rel_y+self.topLeft()[1]),
                             string,
                             fg_color,
                             bg_color)

    def rect(self):
        return self._rect

    def size(self):
        return (self._rect[2], self._rect[3])

    def topLeft(self):
        return (self._rect[0], self._rect[1])

    def width(self):
        return self._rect[2]

    def height(self):
        return self._rect[3]

    def screen(self):
        return self._screen

    def clear(self):
        self._screen.erase()
        #for y in xrange(self.height()):
            #self.write( (0, y), ' '*self.width())

    def outOfBounds(self, pos):
        x, y = pos
        return (x >= self.size()[0] or y >= self.size()[1] or x < 0 or y < 0)

class DummyVScreen(object):
    def __init__(self, w, h):
        self._cursor_pos = (0,0)
        self._render_output = []
        self._size = (w, h)
        self._text = ""
        for h in range(self._size[1]):
            row = []
            self._render_output.append(row)
            for w in range(self._size[0]):
                row.append('.')

        self._log = []
        self._log.append("Inited screen")
    def deinit(self):
        self._log.append("Deinited screen")

    def refresh(self):
        self._log.append("Refresh")
        print(self)

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
        for pos in range(len(string)):
            try:
                self._render_output[y][x+pos] = string[pos]
            except:
                pass
    def dump(self):
        ret = []
        ret.append(" "+"".join(list(itertools.islice(itertools.cycle(list(map(str, list(range(10))))), self._size[0]+1))))
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


