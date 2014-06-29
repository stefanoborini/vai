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
        return (self.left() <= other.right()
                and self.right() >= other.left()
                and self.top() <= other.bottom()
                and self.bottom() >= other.top())

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

    def __str__(self):
        return "VRect(x=%d, y=%d, width=%d, height=%d)" % (self.x(), self.y(), self.width(), self.height())

def x(rect):
    return rect[0]
def y(rect):
    return rect[1]
def left(rect):
    return rect[0]
def right(rect):
    return rect[0] + rect[2] - 1
def top(rect):
    return rect[1]
def bottom(rect):
    return rect[1] + rect[3] - 1
def topLeft(rect):
    return (rect[0], rect[1])
def topRight(rect):
    return (rect[0] + rect[2] - 1, rect[1])
def bottomLeft(rect):
    return (rect[0], rect[1] + rect[3] - 1)
def bottomRight(rect):
    return (rect[0] + rect[2] - 1, rect[1] + rect[3] - 1)
def size(rect):
    return (rect[2], rect[3])
def height(rect):
    return rect[3]
def width(rect):
    return rect[2]
def isNull(rect):
    return (rect[2] == 0 and rect[3] == 0)
def moveTo(rect, top_left):
    return (top_left[0], top_left[1], rect[2], rect[3])
def intersects(rect, other):
    return (left(rect) <= right(other)
                and right(rect) >= left(other)
                and top(rect) <= bottom(other)
                and bottom(rect) >= top(other))

