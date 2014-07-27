from .. import Orientation, LineCapStyle, LineStyle, CornerCapStyle
from ..consts import Index


class VPainter:
    def __init__(self, widget):
        self._widget = widget
        colors = self._widget.currentColors()
        self._fg_color = colors[Index.FG_COLOR]
        self._bg_color = colors[Index.BG_COLOR]
        self._corner_cap_style = CornerCapStyle.Plus
        self._line_cap_style = LineCapStyle.Plus
        self._line_style = LineStyle.Full

    @property
    def fg_color(self):
        return self._fg_color
    @fg_color.setter
    def fg_color(self, color):
        self._fg_color = color
    @property
    def bg_color(self):
        return self._bg_color
    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color

    def drawText(self, pos, string):
        self._widget.screenArea().write(pos, string, self.fg_color, self.bg_color)

    def drawRect(self, rect):
        screen_area = self._widget.screenArea()

        x, y = rect[Index.RECT_X], rect[Index.RECT_Y]
        w, h = rect[Index.RECT_WIDTH], rect[Index.RECT_HEIGHT]
        fg, bg = self.fg_color, self.bg_color
        cap, line, vline = _getRectComponents(self._corner_cap_style, self._line_style)

        if w >= 2 and h >= 2:
            screen_area.write( (x,y), cap + line * (w-2) + cap, fg, bg)
            for i in range(0, h-2):
                screen_area.write( (x,y+i+1), vline+' '*(w-2)+vline, fg, bg)
            screen_area.write( (x, y+h-1), cap+line*(w-2)+cap, fg, bg)

    def drawLine(self, pos, length, direction):
        screen_area = self._widget.screenArea()
        x,y = pos
        fg, bg = self.fg_color, self.bg_color
        cap, line, vline = _getLineComponents(self._line_cap_style, self._line_style)

        if direction == Orientation.Horizontal:
            screen_area.write( (x,y), cap + line * (length-2) + cap, fg, bg)
        elif direction == Orientation.Vertical:
            screen_area.write( (x,y), cap, fg, bg)
            for i in range(0, length-2):
                screen_area.write( (x,y+i+1), vline, fg, bg)
            screen_area.write( (x,y+length-1), cap, fg, bg)

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

    def recolor(self, pos, colors):
        self._widget.screenArea().setColors(pos, colors)


def _getLineComponents(line_cap_style, line_style):
    if line_style == LineStyle.NoLine:
        return (' ', ' ', ' ')

    line, vline = {
                    LineStyle.Full: ('-', '|')
                  }.get(line_style, (' ', ' '))

    cap = { LineCapStyle.Plus: '+'
          }.get(line_cap_style, ' ')

    return (cap, line, vline)

def _getRectComponents(corner_cap_style, line_style):
    if line_style == LineStyle.NoLine:
        return (' ', ' ', ' ')

    line, vline = {
                    LineStyle.Full: ('-', '|')
                  }.get(line_style, (' ', ' '))

    cap = { LineCapStyle.Plus: '+'
          }.get(corner_cap_style, ' ')

    return (cap, line, vline)
