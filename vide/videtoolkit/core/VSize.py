class VSize(object):
    def __init__(self, width, height):
        self._size = (width, height)

    def __iter__(self):
        return iter(self._size)

    def width(self):
        return self._size[0]

    def height(self):
        return self._size[1]

    def __str__(self):
        return "VSize(width=%d, height=%d)" % self._size
