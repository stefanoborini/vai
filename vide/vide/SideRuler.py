from videtoolkit import gui, core, utils
import math

class SideRuler(gui.VWidget):
    def __init__(self, parent):
        super(SideRuler, self).__init__(parent)
        self._start_line = 1
        self._end_line = None
        self._skip_intervals = []

    def paintEvent(self, event):
        pass
#        w, h = self.size()
#        painter = gui.VPainter(self)
#        painter.clear( (0, 0, w, h) )
#        num_digits = self._lineNumberWidth()
#        for i in xrange(0, h):
#            badge_mark = " "
#            border = " "
#            if self._document_model.isEmpty() and i == 0:
#                painter.write( (0, i), "1".rjust(num_digits) + badge_mark + border, fg_color=gui.VGlobalColor.cyan, bg_color=gui.VGlobalColor.blue)
#                continue
#
#            document_line = self._view_model.documentPosAtTop()[0] + i
#            if document_line > self._document_model.numLines():
#                painter.write( (0, i), "~".rjust(num_digits)+" "+border, fg_color=gui.VGlobalColor.blue)
#                continue
#
#            badge = self._view_model.badge(document_line)
#            if badge is not None:
#                badge_mark = badge.mark()
#            painter.write( (0, i), str(document_line).rjust(self._lineNumberWidth()) + badge_mark + border,
#                            fg_color=gui.VGlobalColor.cyan, bg_color=gui.VGlobalColor.blue)

    def _computeExpectedValues(self):
        if self._end_line is None:
            values = range(self._start_line, self._start_line+self.height())
        else:
            values = range(self._start_line, min(self._end_line, self._start_line+self.height()))



    def minimumSize(self):
        return (self._lineNumberWidth()+1+1, 0)

    def _lineNumberWidth(self):
        if self._document_model.numLines() == 0:
            return 1

        num_digits = int(math.log10(self._document_model.numLines()))+1
        return num_digits

