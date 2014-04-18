class VPoint(object):
    def __init__(self, x, y):
        self._pos = (x,y)

    def __iter__(self):
        return iter(self._pos)

    def x(self):
        return self._pos[0]

    def y(self):
        return self._pos[1]

    def __add__(self, other):
        return VPoint(self._pos[0]+other._pos[0], self._pos[1]+other._pos[1])

    def __sub__(self, other):
        return VPoint(self._pos[0]-other._pos[0], self._pos[1]-other._pos[1])

    def __str__(self):
        return "VPoint(x=%d, y=%d)" % self._pos
