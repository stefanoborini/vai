from .VLabel import VLabel
from ..VPainter import VPainter
from ..VPalette import VPalette
from ... import core

class VToolTip(VLabel):
    @staticmethod
    def showText(pos, text):
        tip = VToolTip(text, parent=None)
        tip.resize(tip.minimumSize())
        tip.move(pos)
        tip.show()

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.ToolTipText)
        bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.ToolTipBase)
        for i in range(0, int(h/2)):
            painter.drawText( core.VPoint(0, i), ' '*w, fg_color, bg_color)
        painter.drawText( core.VPoint(0, int(h/2)), self._label + ' '*(w-len(self._label)), fg_color, bg_color)
        for i in range(1+int(h/2), h):
            painter.drawText( core.VPoint(0, i), ' '*w, fg_color, bg_color)


