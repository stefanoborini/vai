from . import gui, core
import curses
import math


class EditorModel(core.VObject):
    def __init__(self, filename):
        self._contents = open(filename).readlines()

    def getLine(self, line):
        try:
            return self._contents[line]
        except:
            return ""

COMMAND_MODE = -1
INSERT_MODE = 1

class Editor(gui.VWidget):
    def __init__(self, model, parent=None):
        super(Editor, self).__init__(parent)
        #self._model = model
        #self._top_line = 0
        #self._cursor_pos = (0,0)
        #self._state = COMMAND_MODE
        self._status_bar = gui.VLabel("HELLO", parent=self)
        self._command_bar = gui.VLabel("HELLO", parent=self)
        index = gui.VApplication.vApp.screen().getColor(6,4)
        self._status_bar.setColor(index)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)

        self._command_bar.move(0, self.size()[1]-1)
        self._command_bar.resize(self.size()[0], 1)

    def statusBar(self):
        return self_status_bar

    def render(self):
#        screen = gui.VApplication.vApp.screen()
#        w, h = self.size()
#        x, y = self.pos()
#
#        num_digits = math.log10(h)+1
#        for i in xrange(0, h):
#            abs_pos = self.mapToGlobal(x, y+i)
#            screen.write(abs_pos[0], abs_pos[1], str(i+self._top_line).rjust(num_digits+1), 0)
#
#        for i in xrange(0, h):
#            abs_pos = self.mapToGlobal(x+num_digits+1, y+i)
#            screen.write(abs_pos[0], abs_pos[1], "|", 0)
#
#        for i in xrange(0, h):
#            abs_pos = self.mapToGlobal(x+num_digits+2, y+i)
#            screen.write(abs_pos[0], abs_pos[1], self._model.getLine(self._top_line+i), 0)

        super(Editor, self).render()

    def keyEvent(self, event):
        if event.key() == curses.KEY_UP:
            self._cursor_pos = (self._cursor_pos[0], max(0, self._cursor_pos[1]-1))
        elif event.key() == curses.KEY_DOWN:
            self._cursor_pos = (self._cursor_pos[0], self._cursor_pos[1]+1)
        elif event.key() == curses.KEY_LEFT:
            self._cursor_pos = (max(self._cursor_pos[0]-1,0), self._cursor_pos[1])
        elif event.key() == curses.KEY_RIGHT:
            self._cursor_pos = (self._cursor_pos[0]+1, self._cursor_pos[1])

        gui.VCursor.move(self._cursor_pos[0]+self.pos()[0], self._cursor_pos[1]+self.pos()[1])
        event.accept()
