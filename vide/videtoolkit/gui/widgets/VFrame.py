from ..VWidget import VWidget
from ..VPalette import VPalette
from ..VPainter import VPainter

class VFrame(VWidget):
    def __init__(self, parent=None):
        super(VFrame, self).__init__(parent)
        self._title = None

    def paintEvent(self, event):
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)
        w, h = self.size()
        if self._title:

            #0123456789012
            #+-| hello |-+
            dash_length = (w -                  # total width of the dialog
                           2 -                  # space for the angles
                           len(self._title) -   # the space for the title itself
                           2 -                  # the two empty spaces on the sides of the title
                           2)                   # the vertical bars
            header = '+' + \
                     "-"*(dash_length/2) + \
                     "| " + \
                     self._title + \
                     " |" + \
                     "-"*(dash_length-(dash_length/2)) + \
                     "+"
        else:
            header = '+'+"-"*(w-2)+"+"

        painter = VPainter(self)
        painter.write(0, 0, header, fg, bg)

        for i in range(0, h-2):
            painter.write(0, i+1, '|'+' '*(len(header)-2)+"|", fg, bg)
        painter.write(0, h-1, '+'+"-"*(len(header)-2)+"+", fg, bg)

    def setTitle(self, title):
        self._title = title

    def minimumSize(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2,2)

    def contentsMargins(self):
        return (1,1,1,1)
