from .. import core
from ..consts import Index

class VPainter:
    def __init__(self, widget):
        self._widget = widget

    def drawText(self, pos, string, fg_color=None, bg_color=None):
        widget_colors = self._widget.currentColors()
        if fg_color is None:
            fg_color = widget_colors[Index.FG_COLOR]

        if bg_color is None:
            bg_color = widget_colors[Index.BG_COLOR]

        self._widget.screenArea().write(pos, string, fg_color, bg_color)

    def eraseRect(self, rect):
        widget_colors = self._widget.currentColors()
        screen_area = self._widget.screenArea()
        top_left = (rect[Index.RECT_X], rect[Index.RECT_Y])
        string = ' '*rect[Index.RECT_WIDTH]
        for h_idx in range(rect[Index.RECT_HEIGHT]):
            screen_area.write( (top_left[Index.X], top_left[Index.Y] + h_idx),
                               string,
                               widget_colors[Index.FG_COLOR], widget_colors[Index.BG_COLOR])

    def erase(self):
        self.eraseRect(self._widget.rect())

    def setColors(self, pos, colors):
        self._widget.screenArea().setColors(pos, colors)
