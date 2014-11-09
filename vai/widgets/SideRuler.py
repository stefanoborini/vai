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
        current_fg, current_bg = self.currentColors()
        painter = gui.VPainter(self)
        painter.erase()
        num_digits = self._lineNumberWidth()
        entries = self.visibleRowNumbers()
        for i, current in enumerate(entries):
            badge_mark = " "
            border = " "
            painter.bg_color = current_bg

            if current > self._num_rows:
                painter.fg_color = current_fg
                painter.drawText( (0, i), "~".ljust(num_digits)+" "+border)
                continue

            badge = self._badges.get(current)
            if badge is not None:
                badge_mark = badge.marker
                painter.bg_color = badge.bg_color
            painter.fg_color = current_fg
            painter.drawText( (0, i),
                              str(current).rjust(num_digits) + badge_mark + border,
                              )

    def setNumRows(self, num_rows):
        """Sets the total number of document rows"""
        self._num_rows = num_rows
        self.update()

    def setTopRow(self, top_row):
        """Sets the top row value, that is the value at the very top of the ruler"""
        self._top_row = top_row
        self.update()

    def minimumSize(self):
        return (self._lineNumberWidth(), 1)

    def addBadges(self, badges):
        """
        Add the badges to the internal badge set.
        badges is a dictionary { linenumber: badge }
        """

        self._badges.update(badges)
        self.update()

    def setBadges(self, badges):
        self._badges.clear()
        self._badges.update(badges)
        self.update()

    def removeBadges(self, line_num_list):
        for line in line_num_list:
            del self._badges[line]

        self.update()

    def clearBadges(self):
        self._badges.clear()

        self.update()

    def visibleRowNumbers(self):
        """Returns a list of all row numbers visible on the ruler"""
        w, h = self.size()
        return _computeLineValues(self._top_row, self._num_rows, self._skip_intervals)

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

