from vixtk import gui, core

class InfoHoverBox(gui.VLabel):
    def paintEvent(self, event):
        painter = gui.VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(gui.VPalette.ColorGroup.Active,
                                        gui.VPalette.ColorRole.ToolTipText)
        bg_color = self.palette().color(gui.VPalette.ColorGroup.Active,
                                        gui.VPalette.ColorRole.ToolTipBase)
        for i in range(0, int(h/2)):
            painter.drawText( (0, i), ' '*w, fg_color, bg_color)
        painter.drawText( (0, int(h/2)), self._label + ' '*(w-len(self._label)), fg_color, bg_color)
        for i in range(1+int(h/2), h):
            painter.drawText( (0, i), ' '*w, fg_color, bg_color)


