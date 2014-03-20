from . import VApplication

class VColor(object):
    def __init__(self, rgb=None, curses_rgb=None, index=None):
        if rgb is None and curses_rgb is None and index is None:
            raise Exception("Unspecified color")

        self._rgb = rgb
        self._curses_rgb = curses_rgb
        self._index = index

    def cursesRgb(self):
        if self._curses_rgb is None:
            if self._rgb is not None:
                self._curses_rgb = VColor.rgbToCursesRgb(self._rgb)
            elif self._index is not None:
                self._curses_rgb = VApplication.vApp.screen().supportedColors()[self._index].cursesRgb()
            else:
                raise Exception("Not supposed to reach this")

        return self._curses_rgb

    def rgb(self):
        if self._rgb is None:
            if self._curses_rgb is not None:
                self._rgb = VColor.cursesRgbToRgb(self._curses_rgb)
            elif self._index is not None:
                self._rgb = VApplication.vApp.screen().supportedColors()[self._index].rgb()
            else:
                raise Exception("unreachable")

        return self._rgb

    def hexString(self):
        return "%0.2X%0.2X%0.2X" % self.rgb()

    def index(self):
        if self._index is None:
            self._index = self._lookupIndex()

        return self._index

    def _lookupIndex(self):
        supported_colors = VApplication.vApp.screen().supportedColors()

        closest = sorted([(color.distance(self), color) for color in supported_colors], key=lambda x: x[0])[0]

        return closest[1].index()

    def r(self):
        return self.rgb()[0]
    def g(self):
        return self.rgb()[1]
    def b(self):
        return self.rgb()[2]

    def distance(self, other):
        return (self.r() - other.r())**2 + (self.g() - other.g())**2 + (self.b() - other.b())**2


    @staticmethod
    def cursesRgbToRgb(curses_rgb):
        return tuple([int(x/1000.0 * 255) for x in curses_rgb ])

    @staticmethod
    def rgbToCursesRgb(rgb):
        return tuple([int(x/255 * 1000) for x in rgb ])

class VGlobalColor(object):
    black = VColor(rgb=(255,0,0))
    red = VColor(rgb=(255,0,0))
    green = VColor(rgb=(0,255,0))
    blue = VColor(rgb=(0,0,255))
    cyan = VColor(rgb=(0,255,255))
    purple = VColor(rgb=(255,0,255))
    yellow = VColor(rgb=(255,255,0))
    white = VColor(rgb=(255,255,255))

