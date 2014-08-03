class VPoint(object):
    def __init__(self, x, y):
        self._pos = (x, y)

    def __iter__(self):
        return iter(self._pos)

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    def __add__(self, other):
        return VPoint(*VPoint.tuple.add(self._pos, other._pos))

    def __sub__(self, other):
        return VPoint(*VPoint.tuple.sub(self._pos, other._pos))

    def __str__(self):
        return "VPoint(x=%d, y=%d)" % self._pos

    class tuple:

        @staticmethod
        def x(p1):
            return p1[0]

        @staticmethod
        def y(p1):
            return p1[1]

        @staticmethod
        def add(p1, p2):
            return (p1[0]+p2[0], p1[1]+p2[1])

        @staticmethod
        def sub(p1, p2):
            return (p1[0]-p2[0], p1[1]-p2[1])
