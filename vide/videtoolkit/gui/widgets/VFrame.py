from ..VWidget import VWidget
class VFrame(VWidget):
    def __init__(self, parent=None):
        super(VFrame, self).__init__(parent)

    def paintEvent(self, event):
        w, h = self.size()
        painter = VPainter(self)
        painter.write(0, 0, '+'+"-"*(w-2)+"+")
        for i in xrange(0, h-2):
            painter.write(0, i+1, '|'+' '*(w-2)+"|")
        painter.write(0, h-1, '+'+"-"*(w-2)+"+")
