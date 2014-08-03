from ..VWidget import VWidget

class VPushButton(VWidget):
    def __init__(self, label, parent=None):
        super(VPushButton, self).__init__(parent)
        self._label = label

    def render(self, painter):
        super(VPushButton, self).render(painter)
        for i in range(0, h/2):
            painter.write(0, i, ' '*w)
        painter.write(0, h/2, "[ "+self._label + " ]"+ ' '*(w-len(self._label)-4))
        for i in range(1+h/2, h):
            painter.write(0, i, ' '*w)
