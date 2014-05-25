from vixtk import gui, core

class InfoHoverBox(gui.VLabel):
    def paintEvent(self, event):
        painter = gui.VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(gui.VPalette.ColorGroup.Active,
                                        gui.VPalette.ColorRole.ToolTipText)
        bg_color = self.palette().color(gui.VPalette.ColorGroup.Active,
                                        gui.VPalette.ColorRole.ToolTipBase)

        painter.drawText( (0, 0), self._label, fg_color, bg_color)

