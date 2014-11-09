from vaitk import gui, core, utils
import math
from collections import namedtuple

LineBadge = namedtuple('LineBadge', ["marker", "fg_color", "bg_color"])

class SideRuler(gui.VWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._num_lines = 1
        self._top_line = 1
        self._skip_intervals = []
        self._badges = {}

    def paintEvent(self, event):
        w, h = self.size()
        current_fg, current_bg = self.currentColors()
        painter = gui.VPainter(self)
        painter.erase()
        num_digits = self._lineNumberWidth()
        entries = _computeLineValues(self._top_line, h, self._skip_intervals)
        for i, current in enumerate(entries):
            badge_mark = " "
            painter.bg_color = current_bg

            if current > self._num_lines:
                painter.fg_color = current_fg
                painter.drawText( (0, i), "~".ljust(num_digits).ljust(w))
                continue

            badge = self._badges.get(current)
            if badge is not None:
                badge_mark = badge.marker
                painter.fg_color = badge.fg_color
                painter.bg_color = badge.bg_color
            else:
                painter.fg_color = current_fg
                painter.bg_color = current_bg
            painter.drawText( (0, i),
                              (str(current).rjust(num_digits) + badge_mark).ljust(w),
                              )

    def setNumLines(self, num_lines):
        """Sets the total number of lines the document has"""
        self._num_lines = num_lines
        self.update()

    def setTopLine(self, top_line):
        """Sets the current top line that is displayed"""
        self._top_line = top_line
        self.update()

    def minimumSize(self):
        return (self._lineNumberWidth(), 1)

    def setBadges(self, badges_dict):
        """Set badges at specified lines, overriding the current ones."""
        self._badges.update(badges_dict)
        self.update()

    def removeBadges(self, lines):
        """Clear specific badge lines"""
        if line in self._badges:
            del self._badges[line]
            self.update()

    def badges(self, lines):
        return [self._badges.get(line) for line in lines]

    def visibleLineNumbers(self):
        w, h = self.size()
        line_values = _computeLineValues(self._top_line, h, self._skip_intervals)
        return [l for l in line_values if l <= self._num_lines]

    # Private

    def _lineNumberWidth(self):
        return int(math.log10(self._num_lines))+1



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

