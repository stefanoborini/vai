class VColor:
    def __init__(self, rgb):
        self._rgb = rgb

    @property
    def rgb(self):
        return self._rgb

    def hexString(self):
        return "%0.2X%0.2X%0.2X" % self.rgb

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    @staticmethod
    def distance(color1, color2):
        return (color1.r - color2.r)**2 + (color1.g - color2.g)**2 + (color1.b - color2.b)**2

    class tuple:
        @staticmethod
        def distance(color1, color2):
            return (color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2


class VGlobalColor:
    black = VColor(rgb=(0,0,0))

    darkred = VColor(rgb=(170,0,0))
    lightred = VColor(rgb=(255,0,0))
    red = darkred

    darkgreen = VColor(rgb=(0,170,0))
    lightgreen = VColor(rgb=(0,255,0))
    green = darkgreen

    darkblue = VColor(rgb=(0,0,170))
    lightblue = VColor(rgb=(0,0,255))
    blue = darkblue

    darkcyan = VColor(rgb=(0,170,170))
    lightcyan = VColor(rgb=(0,255,255))
    cyan = darkcyan

    darkmagenta = VColor(rgb=(170,0,170))
    lightmagenta = VColor(rgb=(255,0,255))
    magenta = darkmagenta

    yellow = VColor(rgb=(255,255,0))
    brown = VColor(rgb=(170,170,0))
    grey = VColor(rgb=(170,170,170))
    white = VColor(rgb=(255,255,255))


    def nameToColor(name):
        return VGlobalColor.__dict__.get(name)

