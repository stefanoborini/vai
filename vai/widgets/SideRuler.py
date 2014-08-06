from vaitk import gui, core, utils
import math
from collections import namedtuple

LineBadge = namedtuple('LineBadge', ["marker", "description", "fg_color", "bg_color"])

class SideRuler(gui.VWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._num_rows = 1
        self._top_row = 1
        self._skip_intervals = []
        self._badges = {}

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        painter.erase()
        num_digits = self._lineNumberWidth()
        entries = _computeLineValues(self._top_row, h, self._skip_intervals)
        for i, current in enumerate(entries):
            badge_mark = " "
            border = " "
            painter.bg_color = gui.VGlobalColor.blue

            if current > self._num_rows:
                painter.fg_color = gui.VGlobalColor.blue
                painter.drawText( (0, i), "~".ljust(num_digits)+" "+border)
                continue

            badge = self._badges.get(current)
            if badge is not None:
                badge_mark = badge.marker
                painter.bg_color = badge.bg_color
            painter.fg_color = gui.VGlobalColor.yellow
            painter.drawText( (0, i),
                              str(current).rjust(num_digits) + badge_mark + border,
                              )


    def setNumRows(self, num_rows):
        self._num_rows = num_rows
        self.update()

    def setTopRow(self, top_row):
        self._top_row = top_row
        self.update()

    def minimumSize(self):
        return (self._lineNumberWidth(), 1)

    def addBadge(self, line, badge):
        self._badges[line] = badge
        self.update()

    def removeBadge(self, line):
        if line in self._badges:
            del self._badges[line]
            self.update()

    def badge(self, line):
        return self._badges.get(line)

    # Private

    def _lineNumberWidth(self):
        return int(math.log10(self._num_rows))+1


def _computeLineValues(start, how_many, skip):
    result = []
    current = start
    for i in range(how_many):
        for interval in skip:
            begin, end = interval
            if begin < current < end:
                current = end
        result.append(current)
        current += 1
    return result

