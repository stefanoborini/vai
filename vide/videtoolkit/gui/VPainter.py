class VPainter(object):
    def __init__(self, widget):
        self._widget = widget

    def write(self, x, y, string, fg_color=None, bg_color=None):
        widget_colors = self._widget.currentColors()
        if fg_color is None:
            fg_color = widget_colors[0]

        if bg_color is None:
            bg_color = widget_colors[1]

        self._widget.screenArea().write(x, y, string, fg_color, bg_color)

    def clear(self, x, y, w, h):
        widget_colors = self._widget.currentColors()
        for h_idx in xrange(h):
            self._widget.screenArea().write(x, y+h_idx, ' '*w, widget_colors[0], widget_colors[1])


