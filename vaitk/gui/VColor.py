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
    black = VColor(rgb=(255,0,0))
    red = VColor(rgb=(255,0,0))
    green = VColor(rgb=(0,255,0))
    blue = VColor(rgb=(0,0,255))
    cyan = VColor(rgb=(0,255,255))
    magenta = VColor(rgb=(255,0,255))
    yellow = VColor(rgb=(255,255,0))
    white = VColor(rgb=(255,255,255))
    brown = VColor(rgb=(170,170,0))


