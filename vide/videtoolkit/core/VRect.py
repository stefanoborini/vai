from .VPoint import VPoint
from .VSize import VSize
#  012345678901234567890
# 0
# 1
# 2  AAAAA
# 3  AAAAA
# 4  AAAAA
# 5       BBB
# 6       BBB
# 7       BBB
# 8
# A = (2,2),(5,3) topleft 2,2 bottomright 6,4

class VRect(object):
    def __init__(self, top_left, size):
        if isinstance(top_left, VPoint):
            self._top_left = top_left
        else:
            self._top_left = VPoint(x=top_left[0], y=top_left[1])

        if isinstance(size, VSize):
            self._size = size
        else:
            self._size = VSize(width=size[0], height=size[1])

    def size(self):
        return self._size
    def height(self):
        return self._size.height()
    def width(self):
        return self._size.width()
    def isNull(self):
        return (self.width() == 0 and self.height() == 0)
    def moveTo(self, top_left):
        self._top_left = top_left
    def intersects(self, other):
        return (self.left() < other.right()
                and self.right() > other.left()
                and self.top() < other.bottom()
                and self.bottom() > other.top())

    def x(self):
        return self.topLeft().x()
    def y(self):
        return self.topLeft().y()
    def left(self):
        return self.x()
    def right(self):
        return self.left() + self.width() - 1
    def top(self):
        return self.y()
    def bottom(self):
        return self.top() + self.height() - 1
    def topLeft(self):
        return self._top_left
    def topRight(self):
        return VPoint(self.right(), self.top())
    def bottomLeft(self):
        return VPoint(self.left(), self.bottom())
    def bottomRight(self):
        return VPoint(self.right(), self.bottom())

