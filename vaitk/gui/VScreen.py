from . import VColor
from ..consts import Index
import curses, _curses
import select
import sys
import os
import logging
import threading

class VException(Exception): pass

class VScreen(object):
    def __init__(self):
        # Timeout so that ncurses sends out the pure esc key instead of considering it
        # the start of a escape command. We need this to exit insert mode in vai, and
        # it makes sense overall
        os.environ["ESCDELAY"] = "25"
        try:
            self._curses_screen = curses.initscr()
        except:
            raise VException("Cannot initialize screen") 
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        self._curses_screen.keypad(1)
        self._curses_screen.nodelay(True)
        self._curses_screen.leaveok(True)
        self._curses_screen.notimeout(True)

        # ncurses is not thread safe, we need a lock to prevent writing collide with reading
        self._curses_lock = threading.Lock()

        # Resolves the rgb color to the screen color
        self._color_lookup_cache = {}

        # Resolves fg, bg native index to the associated color pair index
        self._attr_lookup_cache = {}

        # The first color pair is always defined with index 0 and contains the default fg and bg colors
        self._color_pairs = [ (-1, -1) ]

        self._cursor_pos = (0,0)
        self.logger = logging.getLogger(self.__class__.__name__)
        if hasattr(self, "debug"):
            self.logger.setLevel(self.debug)
        else:
            self.logger.setLevel(logging.CRITICAL+1)
        VGlobalScreenColor.init(self.numColors())

    def reset(self):
        curses.nocbreak()
        self._curses_screen.keypad(0)
        curses.echo()
        curses.endwin()

    def refresh(self):
        with self._curses_lock:
            self._curses_screen.noutrefresh()
            curses.setsyx(self._cursor_pos[Index.Y], self._cursor_pos[Index.X])
            curses.doupdate()

    def rect(self):
        return self.topLeft() + self.size()

    def size(self):
        with self._curses_lock:
            h, w = self._curses_screen.getmaxyx()
        return (w,h)

    def topLeft(self):
        return (0,0)

    def width(self):
        return self.size()[Index.SIZE_WIDTH]

    def height(self):
        return self.size()[Index.SIZE_HEIGHT]

    def getKeyCode(self):
        # Prevent to hold the GIL
        select.select([sys.stdin], [], [])

        with self._curses_lock:
            c = self._curses_screen.getch()
            # 27 = Escape character, but it's also used to create multikeys.
            # So we detect a pure escape by getting again. If it returns
            # -1, it means there's no additional keys and it's a pure escape
            if c == 27:
                next_c = self._curses_screen.getch()
                if next_c == -1:
                    pass
                # FIXME later: handle multikeys

        return c

    def write(self, pos, string, fg_color=None, bg_color=None):
        x,y = pos
        w,h = self.size()

        out_string = string

        if y < 0 or y >= h or x >= w:
            self.logger.error("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            return

        out_string = out_string[:w-x]

        if x < 0:
            self.logger.error("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = string[-x:]

        if len(out_string) == 0:
            return

        attr = self.getColorAttributeCode(fg_color, bg_color)
        if (x+len(out_string) > w):
            self.logger.error("Out of bound in VScreen.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = out_string[:w-x]

        if (x+len(out_string) == w):
            with self._curses_lock:
                # Old ncurses trick. We can't write the very last character, so
                # we add everything but the first, and then push everything forward
                self._curses_screen.addstr(y, x, out_string[1:], attr)
                self._curses_screen.insstr(y, x, out_string[0], attr)
                self._curses_screen.noutrefresh()
        else:
            with self._curses_lock:
                self._curses_screen.addstr(y, x, out_string, attr)
                self._curses_screen.noutrefresh()

    def setColors(self, pos, colors):
        """
        Sets the color attributes for a specific line, starting at pos and forward until the colors
        array runs out
        """

        x,y = pos
        w,h = self.size()

        out_colors = colors

        if y < 0 or y >= h or x >= w:
            self.logger.error("Out of bound in VScreen.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            return

        out_colors = out_colors[:w-x]

        if x < 0:
            self.logger.error("Out of bound in VScreen.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            out_colors = colors[-x:]

        if len(out_colors) == 0:
            return

        if (x+len(out_colors) > w):
            self.logger.error("Out of bound in VScreen.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            out_colors = out_colors[:w-x]

        for num, colors in enumerate(out_colors):
            fg_color, bg_color = colors
            attr = self.getColorAttributeCode(fg_color, bg_color)
            with self._curses_lock:
                self._curses_screen.chgat(y, x+num, 1, attr)

    def numColors(self):
        return curses.COLORS

    def getColorAttributeCode(self, fg=None, bg=None):
        """Given fg and bg colors, find and return the correct attribute code to apply with chgat"""
        fg_screen = None if fg is None else self._findClosestColor(fg)
        bg_screen = None if bg is None else self._findClosestColor(bg)

        if (fg_screen, bg_screen) in self._attr_lookup_cache:
            return self._attr_lookup_cache[(fg_screen, bg_screen)]

        fg_index = -1 if fg_screen is None else fg_screen.colorIdx()
        bg_index = -1 if bg_screen is None else bg_screen.colorIdx()

        attr = self._getPairAttrFromColors(fg_index, bg_index)

        if fg_screen and fg_screen.attr():
            attr |= fg_screen.attr()

        self._attr_lookup_cache[(fg_screen, bg_screen)] = attr
        return attr

    def _getPairAttrFromColors(self, fg_index, bg_index):
        t = (fg_index, bg_index)

        if t in self._color_pairs:
            pair_index = self._color_pairs.index( (fg_index, bg_index) )
        else:
            pair_index = len(self._color_pairs)
            with self._curses_lock:
                curses.init_pair(pair_index, fg_index, bg_index)
            self._color_pairs.append((fg_index, bg_index))

        with self._curses_lock:
            attr = curses.color_pair(pair_index)

        return attr
        # Init color pairs

    def setCursorPos(self, pos):
        if self.outOfBounds(pos):
            self.logger.error("out of bound in Screen.setCursorPos: %s" % str(pos))
            return

        self._cursor_pos = pos

    def cursorPos(self):
        return self._cursor_pos

    def _findClosestColor(self, color):
        screen_color = self._color_lookup_cache.get(color.rgb)
        if screen_color is not None:
            return screen_color

        closest = sorted([(VColor.VColor.distance(color, screen_color),
                           screen_color)
                           for index, screen_color in enumerate(VGlobalScreenColor.allColors())
                         ],
                         key=lambda x: x[0]
                         )[0]
        self._color_lookup_cache[color.rgb] = closest[1]
        return closest[1]

    def outOfBounds(self, pos):
        x, y = pos
        return (x >= self.width() or y >= self.height() or x < 0 or y < 0)

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

    @property
    def r(self):
        return self._equiv_rgb[0]
    @property
    def g(self):
        return self._equiv_rgb[1]
    @property
    def b(self):
        return self._equiv_rgb[2]

class VGlobalScreenColor(object):
    @classmethod
    def init(cls, num_colors):
        if num_colors == 8 or num_colors == 256:
            cls.term_0        = VScreenColor(0  , None, (0x00,0x00,0x00))
            cls.term_1        = VScreenColor(1  , None, (0x80,0x00,0x00))
            cls.term_2        = VScreenColor(2  , None, (0x00,0x80,0x00))
            cls.term_3        = VScreenColor(3  , None, (0x80,0x80,0x00))
            cls.term_4        = VScreenColor(4  , None, (0x00,0x00,0x80))
            cls.term_5        = VScreenColor(5  , None, (0x80,0x00,0x80))
            cls.term_6        = VScreenColor(6  , None, (0x00,0x80,0x80))
            cls.term_6        = VScreenColor(7  , None, (0xc0,0xc0,0xc0))
            cls.term_8        = VScreenColor(8  , None, (0x80,0x80,0x80))

            cls.black        = VScreenColor(curses.COLOR_BLACK, None, (0,0,0))
            cls.darkred      = VScreenColor(curses.COLOR_RED, None, (170,0,0))
            cls.darkgreen    = VScreenColor(curses.COLOR_GREEN, None, (0, 170, 0))
            cls.brown        = VScreenColor(curses.COLOR_YELLOW, None, (170, 170, 0))
            cls.darkblue     = VScreenColor(curses.COLOR_BLUE, None, (0, 0, 170))
            cls.darkmagenta  = VScreenColor(curses.COLOR_MAGENTA, None, (170, 0, 170))
            cls.darkcyan     = VScreenColor(curses.COLOR_CYAN, None, (0, 170, 170))
            cls.lightgray    = VScreenColor(curses.COLOR_WHITE, None, (170, 170, 170))

            cls.darkgray     = VScreenColor(curses.COLOR_BLACK, curses.A_BOLD, (100, 100, 100))
            cls.lightred     = VScreenColor(curses.COLOR_RED, curses.A_BOLD, (255,0,0))
            cls.lightgreen   = VScreenColor(curses.COLOR_GREEN, curses.A_BOLD, (0, 255, 0))
            cls.yellow       = VScreenColor(curses.COLOR_YELLOW, curses.A_BOLD, (255, 255, 0))
            cls.lightblue    = VScreenColor(curses.COLOR_BLUE, curses.A_BOLD, (0, 0, 255))
            cls.lightmagenta = VScreenColor(curses.COLOR_MAGENTA, curses.A_BOLD, (255, 0, 255))
            cls.lightcyan    = VScreenColor(curses.COLOR_CYAN, curses.A_BOLD, (0, 255, 255))
            cls.white        = VScreenColor(curses.COLOR_WHITE, curses.A_BOLD, (255,255,255))

            cls.red          = cls.lightred
            cls.green        = cls.lightgreen
            cls.blue         = cls.lightblue
            cls.magenta      = cls.lightmagenta
            cls.cyan         = cls.lightcyan
            cls.gray         = cls.lightgray

        if num_colors == 256:
            cls.term_9        = VScreenColor(9  , None, (0xff,0x00,0x00))
            cls.term_10       = VScreenColor(10 , None, (0x00,0xff,0x00))
            cls.term_11       = VScreenColor(11 , None, (0xff,0xff,0x00))
            cls.term_12       = VScreenColor(12 , None, (0x00,0x00,0xff))
            cls.term_13       = VScreenColor(13 , None, (0xff,0x00,0xff))
            cls.term_14       = VScreenColor(14 , None, (0x00,0xff,0xff))
            cls.term_15       = VScreenColor(15 , None, (0xff,0xff,0xff))
            cls.term_16       = VScreenColor(16 , None, (0x00,0x00,0x00))
            cls.term_17       = VScreenColor(17 , None, (0x00,0x00,0x5f))
            cls.term_18       = VScreenColor(18 , None, (0x00,0x00,0x87))
            cls.term_19       = VScreenColor(19 , None, (0x00,0x00,0xaf))
            cls.term_20       = VScreenColor(20 , None, (0x00,0x00,0xd7))
            cls.term_21       = VScreenColor(21 , None, (0x00,0x00,0xff))
            cls.term_22       = VScreenColor(22 , None, (0x00,0x5f,0x00))
            cls.term_23       = VScreenColor(23 , None, (0x00,0x5f,0x5f))
            cls.term_24       = VScreenColor(24 , None, (0x00,0x5f,0x87))
            cls.term_25       = VScreenColor(25 , None, (0x00,0x5f,0xaf))
            cls.term_26       = VScreenColor(26 , None, (0x00,0x5f,0xd7))
            cls.term_27       = VScreenColor(27 , None, (0x00,0x5f,0xff))
            cls.term_28       = VScreenColor(28 , None, (0x00,0x87,0x00))
            cls.term_29       = VScreenColor(29 , None, (0x00,0x87,0x5f))
            cls.term_30       = VScreenColor(30 , None, (0x00,0x87,0x87))
            cls.term_31       = VScreenColor(31 , None, (0x00,0x87,0xaf))
            cls.term_32       = VScreenColor(32 , None, (0x00,0x87,0xd7))
            cls.term_33       = VScreenColor(33 , None, (0x00,0x87,0xff))
            cls.term_34       = VScreenColor(34 , None, (0x00,0xaf,0x00))
            cls.term_35       = VScreenColor(35 , None, (0x00,0xaf,0x5f))
            cls.term_36       = VScreenColor(36 , None, (0x00,0xaf,0x87))
            cls.term_37       = VScreenColor(37 , None, (0x00,0xaf,0xaf))
            cls.term_38       = VScreenColor(38 , None, (0x00,0xaf,0xd7))
            cls.term_39       = VScreenColor(39 , None, (0x00,0xaf,0xff))
            cls.term_40       = VScreenColor(40 , None, (0x00,0xd7,0x00))
            cls.term_41       = VScreenColor(41 , None, (0x00,0xd7,0x5f))
            cls.term_42       = VScreenColor(42 , None, (0x00,0xd7,0x87))
            cls.term_43       = VScreenColor(43 , None, (0x00,0xd7,0xaf))
            cls.term_44       = VScreenColor(44 , None, (0x00,0xd7,0xd7))
            cls.term_45       = VScreenColor(45 , None, (0x00,0xd7,0xff))
            cls.term_46       = VScreenColor(46 , None, (0x00,0xff,0x00))
            cls.term_47       = VScreenColor(47 , None, (0x00,0xff,0x5f))
            cls.term_48       = VScreenColor(48 , None, (0x00,0xff,0x87))
            cls.term_49       = VScreenColor(49 , None, (0x00,0xff,0xaf))
            cls.term_50       = VScreenColor(50 , None, (0x00,0xff,0xd7))
            cls.term_51       = VScreenColor(51 , None, (0x00,0xff,0xff))
            cls.term_52       = VScreenColor(52 , None, (0x5f,0x00,0x00))
            cls.term_53       = VScreenColor(53 , None, (0x5f,0x00,0x5f))
            cls.term_54       = VScreenColor(54 , None, (0x5f,0x00,0x87))
            cls.term_55       = VScreenColor(55 , None, (0x5f,0x00,0xaf))
            cls.term_56       = VScreenColor(56 , None, (0x5f,0x00,0xd7))
            cls.term_57       = VScreenColor(57 , None, (0x5f,0x00,0xff))
            cls.term_58       = VScreenColor(58 , None, (0x5f,0x5f,0x00))
            cls.term_59       = VScreenColor(59 , None, (0x5f,0x5f,0x5f))
            cls.term_60       = VScreenColor(60 , None, (0x5f,0x5f,0x87))
            cls.term_61       = VScreenColor(61 , None, (0x5f,0x5f,0xaf))
            cls.term_62       = VScreenColor(62 , None, (0x5f,0x5f,0xd7))
            cls.term_63       = VScreenColor(63 , None, (0x5f,0x5f,0xff))
            cls.term_64       = VScreenColor(64 , None, (0x5f,0x87,0x00))
            cls.term_65       = VScreenColor(65 , None, (0x5f,0x87,0x5f))
            cls.term_66       = VScreenColor(66 , None, (0x5f,0x87,0x87))
            cls.term_67       = VScreenColor(67 , None, (0x5f,0x87,0xaf))
            cls.term_68       = VScreenColor(68 , None, (0x5f,0x87,0xd7))
            cls.term_69       = VScreenColor(69 , None, (0x5f,0x87,0xff))
            cls.term_70       = VScreenColor(70 , None, (0x5f,0xaf,0x00))
            cls.term_71       = VScreenColor(71 , None, (0x5f,0xaf,0x5f))
            cls.term_72       = VScreenColor(72 , None, (0x5f,0xaf,0x87))
            cls.term_73       = VScreenColor(73 , None, (0x5f,0xaf,0xaf))
            cls.term_74       = VScreenColor(74 , None, (0x5f,0xaf,0xd7))
            cls.term_75       = VScreenColor(75 , None, (0x5f,0xaf,0xff))
            cls.term_76       = VScreenColor(76 , None, (0x5f,0xd7,0x00))
            cls.term_77       = VScreenColor(77 , None, (0x5f,0xd7,0x5f))
            cls.term_78       = VScreenColor(78 , None, (0x5f,0xd7,0x87))
            cls.term_79       = VScreenColor(79 , None, (0x5f,0xd7,0xaf))
            cls.term_80       = VScreenColor(80 , None, (0x5f,0xd7,0xd7))
            cls.term_81       = VScreenColor(81 , None, (0x5f,0xd7,0xff))
            cls.term_82       = VScreenColor(82 , None, (0x5f,0xff,0x00))
            cls.term_83       = VScreenColor(83 , None, (0x5f,0xff,0x5f))
            cls.term_84       = VScreenColor(84 , None, (0x5f,0xff,0x87))
            cls.term_85       = VScreenColor(85 , None, (0x5f,0xff,0xaf))
            cls.term_86       = VScreenColor(86 , None, (0x5f,0xff,0xd7))
            cls.term_87       = VScreenColor(87 , None, (0x5f,0xff,0xff))
            cls.term_88       = VScreenColor(88 , None, (0x87,0x00,0x00))
            cls.term_89       = VScreenColor(89 , None, (0x87,0x00,0x5f))
            cls.term_90       = VScreenColor(90 , None, (0x87,0x00,0x87))
            cls.term_91       = VScreenColor(91 , None, (0x87,0x00,0xaf))
            cls.term_92       = VScreenColor(92 , None, (0x87,0x00,0xd7))
            cls.term_93       = VScreenColor(93 , None, (0x87,0x00,0xff))
            cls.term_94       = VScreenColor(94 , None, (0x87,0x5f,0x00))
            cls.term_95       = VScreenColor(95 , None, (0x87,0x5f,0x5f))
            cls.term_96       = VScreenColor(96 , None, (0x87,0x5f,0x87))
            cls.term_97       = VScreenColor(97 , None, (0x87,0x5f,0xaf))
            cls.term_98       = VScreenColor(98 , None, (0x87,0x5f,0xd7))
            cls.term_99       = VScreenColor(99 , None, (0x87,0x5f,0xff))
            cls.term_100      = VScreenColor(100, None, (0x87,0x87,0x00))
            cls.term_101      = VScreenColor(101, None, (0x87,0x87,0x5f))
            cls.term_102      = VScreenColor(102, None, (0x87,0x87,0x87))
            cls.term_103      = VScreenColor(103, None, (0x87,0x87,0xaf))
            cls.term_104      = VScreenColor(104, None, (0x87,0x87,0xd7))
            cls.term_105      = VScreenColor(105, None, (0x87,0x87,0xff))
            cls.term_106      = VScreenColor(106, None, (0x87,0xaf,0x00))
            cls.term_107      = VScreenColor(107, None, (0x87,0xaf,0x5f))
            cls.term_108      = VScreenColor(108, None, (0x87,0xaf,0x87))
            cls.term_109      = VScreenColor(109, None, (0x87,0xaf,0xaf))
            cls.term_110      = VScreenColor(110, None, (0x87,0xaf,0xd7))
            cls.term_111      = VScreenColor(111, None, (0x87,0xaf,0xff))
            cls.term_112      = VScreenColor(112, None, (0x87,0xd7,0x00))
            cls.term_113      = VScreenColor(113, None, (0x87,0xd7,0x5f))
            cls.term_114      = VScreenColor(114, None, (0x87,0xd7,0x87))
            cls.term_115      = VScreenColor(115, None, (0x87,0xd7,0xaf))
            cls.term_116      = VScreenColor(116, None, (0x87,0xd7,0xd7))
            cls.term_117      = VScreenColor(117, None, (0x87,0xd7,0xff))
            cls.term_118      = VScreenColor(118, None, (0x87,0xff,0x00))
            cls.term_119      = VScreenColor(119, None, (0x87,0xff,0x5f))
            cls.term_120      = VScreenColor(120, None, (0x87,0xff,0x87))
            cls.term_121      = VScreenColor(121, None, (0x87,0xff,0xaf))
            cls.term_122      = VScreenColor(122, None, (0x87,0xff,0xd7))
            cls.term_123      = VScreenColor(123, None, (0x87,0xff,0xff))
            cls.term_124      = VScreenColor(124, None, (0xaf,0x00,0x00))
            cls.term_125      = VScreenColor(125, None, (0xaf,0x00,0x5f))
            cls.term_126      = VScreenColor(126, None, (0xaf,0x00,0x87))
            cls.term_127      = VScreenColor(127, None, (0xaf,0x00,0xaf))
            cls.term_128      = VScreenColor(128, None, (0xaf,0x00,0xd7))
            cls.term_129      = VScreenColor(129, None, (0xaf,0x00,0xff))
            cls.term_130      = VScreenColor(130, None, (0xaf,0x5f,0x00))
            cls.term_131      = VScreenColor(131, None, (0xaf,0x5f,0x5f))
            cls.term_132      = VScreenColor(132, None, (0xaf,0x5f,0x87))
            cls.term_133      = VScreenColor(133, None, (0xaf,0x5f,0xaf))
            cls.term_134      = VScreenColor(134, None, (0xaf,0x5f,0xd7))
            cls.term_135      = VScreenColor(135, None, (0xaf,0x5f,0xff))
            cls.term_136      = VScreenColor(136, None, (0xaf,0x87,0x00))
            cls.term_137      = VScreenColor(137, None, (0xaf,0x87,0x5f))
            cls.term_138      = VScreenColor(138, None, (0xaf,0x87,0x87))
            cls.term_139      = VScreenColor(139, None, (0xaf,0x87,0xaf))
            cls.term_140      = VScreenColor(140, None, (0xaf,0x87,0xd7))
            cls.term_141      = VScreenColor(141, None, (0xaf,0x87,0xff))
            cls.term_142      = VScreenColor(142, None, (0xaf,0xaf,0x00))
            cls.term_143      = VScreenColor(143, None, (0xaf,0xaf,0x5f))
            cls.term_144      = VScreenColor(144, None, (0xaf,0xaf,0x87))
            cls.term_145      = VScreenColor(145, None, (0xaf,0xaf,0xaf))
            cls.term_146      = VScreenColor(146, None, (0xaf,0xaf,0xd7))
            cls.term_147      = VScreenColor(147, None, (0xaf,0xaf,0xff))
            cls.term_148      = VScreenColor(148, None, (0xaf,0xd7,0x00))
            cls.term_149      = VScreenColor(149, None, (0xaf,0xd7,0x5f))
            cls.term_150      = VScreenColor(150, None, (0xaf,0xd7,0x87))
            cls.term_151      = VScreenColor(151, None, (0xaf,0xd7,0xaf))
            cls.term_152      = VScreenColor(152, None, (0xaf,0xd7,0xd7))
            cls.term_153      = VScreenColor(153, None, (0xaf,0xd7,0xff))
            cls.term_154      = VScreenColor(154, None, (0xaf,0xff,0x00))
            cls.term_155      = VScreenColor(155, None, (0xaf,0xff,0x5f))
            cls.term_156      = VScreenColor(156, None, (0xaf,0xff,0x87))
            cls.term_157      = VScreenColor(157, None, (0xaf,0xff,0xaf))
            cls.term_158      = VScreenColor(158, None, (0xaf,0xff,0xd7))
            cls.term_159      = VScreenColor(159, None, (0xaf,0xff,0xff))
            cls.term_160      = VScreenColor(160, None, (0xd7,0x00,0x00))
            cls.term_161      = VScreenColor(161, None, (0xd7,0x00,0x5f))
            cls.term_162      = VScreenColor(162, None, (0xd7,0x00,0x87))
            cls.term_163      = VScreenColor(163, None, (0xd7,0x00,0xaf))
            cls.term_164      = VScreenColor(164, None, (0xd7,0x00,0xd7))
            cls.term_165      = VScreenColor(165, None, (0xd7,0x00,0xff))
            cls.term_166      = VScreenColor(166, None, (0xd7,0x5f,0x00))
            cls.term_167      = VScreenColor(167, None, (0xd7,0x5f,0x5f))
            cls.term_168      = VScreenColor(168, None, (0xd7,0x5f,0x87))
            cls.term_169      = VScreenColor(169, None, (0xd7,0x5f,0xaf))
            cls.term_170      = VScreenColor(170, None, (0xd7,0x5f,0xd7))
            cls.term_171      = VScreenColor(171, None, (0xd7,0x5f,0xff))
            cls.term_172      = VScreenColor(172, None, (0xd7,0x87,0x00))
            cls.term_173      = VScreenColor(173, None, (0xd7,0x87,0x5f))
            cls.term_174      = VScreenColor(174, None, (0xd7,0x87,0x87))
            cls.term_175      = VScreenColor(175, None, (0xd7,0x87,0xaf))
            cls.term_176      = VScreenColor(176, None, (0xd7,0x87,0xd7))
            cls.term_177      = VScreenColor(177, None, (0xd7,0x87,0xff))
            cls.term_178      = VScreenColor(178, None, (0xd7,0xaf,0x00))
            cls.term_179      = VScreenColor(179, None, (0xd7,0xaf,0x5f))
            cls.term_180      = VScreenColor(180, None, (0xd7,0xaf,0x87))
            cls.term_181      = VScreenColor(181, None, (0xd7,0xaf,0xaf))
            cls.term_182      = VScreenColor(182, None, (0xd7,0xaf,0xd7))
            cls.term_183      = VScreenColor(183, None, (0xd7,0xaf,0xff))
            cls.term_184      = VScreenColor(184, None, (0xd7,0xd7,0x00))
            cls.term_185      = VScreenColor(185, None, (0xd7,0xd7,0x5f))
            cls.term_186      = VScreenColor(186, None, (0xd7,0xd7,0x87))
            cls.term_187      = VScreenColor(187, None, (0xd7,0xd7,0xaf))
            cls.term_188      = VScreenColor(188, None, (0xd7,0xd7,0xd7))
            cls.term_189      = VScreenColor(189, None, (0xd7,0xd7,0xff))
            cls.term_190      = VScreenColor(190, None, (0xd7,0xff,0x00))
            cls.term_191      = VScreenColor(191, None, (0xd7,0xff,0x5f))
            cls.term_192      = VScreenColor(192, None, (0xd7,0xff,0x87))
            cls.term_193      = VScreenColor(193, None, (0xd7,0xff,0xaf))
            cls.term_194      = VScreenColor(194, None, (0xd7,0xff,0xd7))
            cls.term_195      = VScreenColor(195, None, (0xd7,0xff,0xff))
            cls.term_196      = VScreenColor(196, None, (0xff,0x00,0x00))
            cls.term_197      = VScreenColor(197, None, (0xff,0x00,0x5f))
            cls.term_198      = VScreenColor(198, None, (0xff,0x00,0x87))
            cls.term_199      = VScreenColor(199, None, (0xff,0x00,0xaf))
            cls.term_200      = VScreenColor(200, None, (0xff,0x00,0xd7))
            cls.term_201      = VScreenColor(201, None, (0xff,0x00,0xff))
            cls.term_202      = VScreenColor(202, None, (0xff,0x5f,0x00))
            cls.term_203      = VScreenColor(203, None, (0xff,0x5f,0x5f))
            cls.term_204      = VScreenColor(204, None, (0xff,0x5f,0x87))
            cls.term_205      = VScreenColor(205, None, (0xff,0x5f,0xaf))
            cls.term_206      = VScreenColor(206, None, (0xff,0x5f,0xd7))
            cls.term_207      = VScreenColor(207, None, (0xff,0x5f,0xff))
            cls.term_208      = VScreenColor(208, None, (0xff,0x87,0x00))
            cls.term_209      = VScreenColor(209, None, (0xff,0x87,0x5f))
            cls.term_210      = VScreenColor(210, None, (0xff,0x87,0x87))
            cls.term_211      = VScreenColor(211, None, (0xff,0x87,0xaf))
            cls.term_212      = VScreenColor(212, None, (0xff,0x87,0xd7))
            cls.term_213      = VScreenColor(213, None, (0xff,0x87,0xff))
            cls.term_214      = VScreenColor(214, None, (0xff,0xaf,0x00))
            cls.term_215      = VScreenColor(215, None, (0xff,0xaf,0x5f))
            cls.term_216      = VScreenColor(216, None, (0xff,0xaf,0x87))
            cls.term_217      = VScreenColor(217, None, (0xff,0xaf,0xaf))
            cls.term_218      = VScreenColor(218, None, (0xff,0xaf,0xd7))
            cls.term_219      = VScreenColor(219, None, (0xff,0xaf,0xff))
            cls.term_220      = VScreenColor(220, None, (0xff,0xd7,0x00))
            cls.term_221      = VScreenColor(221, None, (0xff,0xd7,0x5f))
            cls.term_222      = VScreenColor(222, None, (0xff,0xd7,0x87))
            cls.term_223      = VScreenColor(223, None, (0xff,0xd7,0xaf))
            cls.term_224      = VScreenColor(224, None, (0xff,0xd7,0xd7))
            cls.term_225      = VScreenColor(225, None, (0xff,0xd7,0xff))
            cls.term_226      = VScreenColor(226, None, (0xff,0xff,0x00))
            cls.term_227      = VScreenColor(227, None, (0xff,0xff,0x5f))
            cls.term_228      = VScreenColor(228, None, (0xff,0xff,0x87))
            cls.term_229      = VScreenColor(229, None, (0xff,0xff,0xaf))
            cls.term_230      = VScreenColor(230, None, (0xff,0xff,0xd7))
            cls.term_231      = VScreenColor(231, None, (0xff,0xff,0xff))
            cls.term_232      = VScreenColor(232, None, (0x08,0x08,0x08))
            cls.term_233      = VScreenColor(233, None, (0x12,0x12,0x12))
            cls.term_234      = VScreenColor(234, None, (0x1c,0x1c,0x1c))
            cls.term_235      = VScreenColor(235, None, (0x26,0x26,0x26))
            cls.term_236      = VScreenColor(236, None, (0x30,0x30,0x30))
            cls.term_237      = VScreenColor(237, None, (0x3a,0x3a,0x3a))
            cls.term_238      = VScreenColor(238, None, (0x44,0x44,0x44))
            cls.term_239      = VScreenColor(239, None, (0x4e,0x4e,0x4e))
            cls.term_240      = VScreenColor(240, None, (0x58,0x58,0x58))
            cls.term_241      = VScreenColor(241, None, (0x60,0x60,0x60))
            cls.term_242      = VScreenColor(242, None, (0x66,0x66,0x66))
            cls.term_243      = VScreenColor(243, None, (0x76,0x76,0x76))
            cls.term_244      = VScreenColor(244, None, (0x80,0x80,0x80))
            cls.term_245      = VScreenColor(245, None, (0x8a,0x8a,0x8a))
            cls.term_246      = VScreenColor(246, None, (0x94,0x94,0x94))
            cls.term_247      = VScreenColor(247, None, (0x9e,0x9e,0x9e))
            cls.term_248      = VScreenColor(248, None, (0xa8,0xa8,0xa8))
            cls.term_249      = VScreenColor(249, None, (0xb2,0xb2,0xb2))
            cls.term_250      = VScreenColor(250, None, (0xbc,0xbc,0xbc))
            cls.term_251      = VScreenColor(251, None, (0xc6,0xc6,0xc6))
            cls.term_252      = VScreenColor(252, None, (0xd0,0xd0,0xd0))
            cls.term_253      = VScreenColor(253, None, (0xda,0xda,0xda))
            cls.term_254      = VScreenColor(254, None, (0xe4,0xe4,0xe4))
            cls.term_255      = VScreenColor(255, None, (0xee,0xee,0xee))

    @classmethod
    def allColors(cls):
        return [c for c in list(cls.__dict__.values()) if isinstance(c, VScreenColor)]

class VScreenArea(object):
    def __init__(self, screen, rect):
        self._screen = screen
        self._rect = rect
        self.logger = logging.getLogger(self.__class__.__name__)
        if hasattr(self, "debug"):
            self.logger.setLevel(self.debug)
        else:
            self.logger.setLevel(logging.CRITICAL+1)

    def write(self, pos, string, fg_color=None, bg_color=None):
        rel_x, rel_y = pos
        w, h = self.size()

        if rel_y < 0 or rel_y >= h or rel_x >= w:
            self.logger.error("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            return

        out_string = string
        if rel_x < 0:
            self.logger.error("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = string[-rel_x:]
            rel_x = 0

        if len(out_string) == 0:
            return

        if (rel_x+len(out_string) > w):
            self.logger.error("Out of bound in VScreenArea.write: pos=%s size=%s len=%d '%s'" % (str(pos), str(self.size()), len(string), string))
            out_string = out_string[:w-rel_x]

        top_left_x, top_left_y = self.topLeft()
        self._screen.write( (rel_x+top_left_x, rel_y+top_left_y),
                             out_string,
                             fg_color,
                             bg_color)

    def setColors(self, pos, colors):
        rel_x, rel_y = pos
        w, h = self.size()

        if rel_y < 0 or rel_y >= h or rel_x >= w:
            self.logger.error("Out of bound in VScreenArea.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            return

        out_colors = colors
        if rel_x < 0:
            self.logger.error("Out of bound in VScreenArea.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            out_colors = colors[-rel_x:]
            rel_x = 0

        if len(out_colors) == 0:
            return

        if (rel_x+len(out_colors) > w):
            self.logger.error("Out of bound in VScreenArea.setColors: pos=%s size=%s len=%d" % (str(pos), str(self.size()), len(colors)))
            out_colors = out_colors[:w-rel_x]

        top_left_x, top_left_y = self.topLeft()
        self._screen.setColors( (rel_x+top_left_x, rel_y+top_left_y), out_colors)

    def rect(self):
        return self._rect

    def size(self):
        return (self._rect[Index.RECT_WIDTH], self._rect[Index.RECT_HEIGHT])

    def topLeft(self):
        return (self._rect[Index.RECT_X], self._rect[Index.RECT_Y])

    def width(self):
        return self._rect[Index.RECT_WIDTH]

    def height(self):
        return self._rect[Index.RECT_HEIGHT]

    def screen(self):
        return self._screen

    def erase(self):
        for y in range(self.height()):
            self.write( (0, y), ' '*self.width())

    def outOfBounds(self, pos):
        x, y = pos
        return (x >= self.size()[Index.SIZE_WIDTH] or y >= self.size()[Index.SIZE_HEIGHT] or x < 0 or y < 0)

