from videtoolkit import gui, core, utils
import math
import logging

class SideRuler(gui.VWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._start = 1
        self._end = None
        self._skip_intervals = []
        self._badges = {}

    def paintEvent(self, event):
        self.logger.info("Painting sideruler")
        w, h = self.size()
        painter = gui.VPainter(self)
        painter.erase()
        num_digits = self._lineNumberWidth()
        entries = _computeLineValues(self._start, h, self._skip_intervals)
        self.logger.info("Badges %s" % str(self._badges))
        for i, current in enumerate(entries):
            badge_mark = " "
            border = " "
            bg_color = gui.VGlobalColor.blue

            if self._end is not None and current > self._end:
                painter.drawText( (0, i), "~".ljust(num_digits)+" "+border,
                                fg_color=gui.VGlobalColor.blue,
                )
                continue

            badge = self._badges.get(current)
            if badge is not None:
                badge_mark = badge.mark()
                bg_color = badge.bgColor()

            painter.drawText( (0, i), str(current).rjust(num_digits) + badge_mark + border,
                            fg_color=gui.VGlobalColor.yellow, bg_color=bg_color)

        self.logger.info("Done painting sideruler")

#    def _computeExpectedValues(self):
#        if self._end_line is None:
#            values = range(self._start_line, self._start_line+self.height())
#        else:
#            values = range(self._start_line, min(self._end_line, self._start_line+self.height()))

    def setStart(self, start):
        self._start = start
        self.update()

    def minimumSize(self):
        return (self._lineNumberWidth(), 1)

    def _lineNumberWidth(self):

#        if self._document_model.numLines() == 0:
#            return 1
#
        num_digits = int(math.log10(max(_computeLineValues(self._start, self.height(), self._skip_intervals))))+1
        return num_digits


    def addBadge(self, line, badge):
        self.logger.info("Added badge %s %s" % (line, badge))
        self._badges[line] = badge
        self.update()

    def badge(self, line):
        return self._badges.get(line)

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

