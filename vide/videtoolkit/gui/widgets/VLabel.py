from ..VWidget import VWidget
from ..VPainter import VPainter
from ..VPalette import VPalette

class VLabel(VWidget):
    def __init__(self, label="", parent=None):
        super(VLabel, self).__init__(parent)
        self._label = label

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.WindowText)
        bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.Window)
        for i in range(0, h/2):
            painter.write( (0, i), ' '*w, fg_color, bg_color)
        painter.write( (0, h/2), self._label + ' '*(w-len(self._label)), fg_color, bg_color)
        for i in range(1+h/2, h):
            painter.write( (0, i), ' '*w, fg_color, bg_color)

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        if text != self._label:
            self._label = text
            self.update()
