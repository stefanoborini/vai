from .. import core

class VPainter:
    def __init__(self, widget):
        self._widget = widget

    def drawText(self, pos, string, fg_color=None, bg_color=None):
        widget_colors = self._widget.currentColors()
        if fg_color is None:
            fg_color = widget_colors[0]

        if bg_color is None:
            bg_color = widget_colors[1]

        self._widget.screenArea().write(pos, string, fg_color, bg_color)

    def eraseRect(self, rect):
        widget_colors = self._widget.currentColors()
        for h_idx in range(rect.height()):
            self._widget.screenArea().write( rect.topLeft() + core.VPoint(0, h_idx),
                                             ' '*rect.width(),
                                             widget_colors[0], widget_colors[1])

    def erase(self):
        self.eraseRect(self._widget.rect())
