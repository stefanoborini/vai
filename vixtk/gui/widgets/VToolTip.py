from .VLabel import VLabel
from ..VPainter import VPainter
from ..VPalette import VPalette

class VToolTip(VLabel):
    _instance = None
    @classmethod
    def showText(cls, pos, text):
        if cls._instance is None:
            tip = VToolTip(text, parent=None)
            tip.resize(tip.minimumSize())
            tip.move(pos)
            tip.show()
            cls._instance = tip
        return
    @classmethod
    def hide(cls):
        if cls._instance is not None:
            VLabel.hide(cls._instance)
            cls._instance = None

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.ToolTipText)
        painter.bg_color = self.palette().color(VPalette.ColorGroup.Active,
                                        VPalette.ColorRole.ToolTipBase)
        painter.drawText( (0, 0), self._label)
