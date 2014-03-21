class VPainter(object):
    def __init__(self, widget):
        self._widget = widget

    def write(self, x, y, string, fg_color=None, bg_color=None):
        widget_colors = self._widget.currentColors()
        if fg_color is None:
            fg_color = widget_colors[0]

        if bg_color is None:
            bg_color = widget_colors[1]

        abs_pos = self._widget.mapToGlobal(x, y)
        self._widget.palette()
        self._screen.write(abs_pos[0], abs_pos[1], string, fg_color, bg_color)

    def clear(self, x, y, w, h):
        widget_colors = self._widget.currentColors()
        abs_pos = self._widget.mapToGlobal(x, y)
        for h_idx in xrange(h):
            self._screen.write(abs_pos[0], abs_pos[1]+h_idx, ' '*w, widget_colors[0], widget_colors[1])


