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

def x(point):
    return point[0]
def y(point):
    return point[1]
def add(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])
def sub(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])
