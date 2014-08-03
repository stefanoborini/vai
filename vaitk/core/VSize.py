class VSize(object):
    def __init__(self, width, height):
        self._size = (width, height)

    def __iter__(self):
        return iter(self._size)

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def __str__(self):
        return "VSize(width=%d, height=%d)" % self._size

    class tuple:
        @staticmethod
        def width(size):
            return size[0]
        
        @staticmethod
        def height(size):
            return size[1]
