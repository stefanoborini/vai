from videtoolkit import gui, core
import curses
import math


class EditorModel(core.VObject):
    def __init__(self, filename=None):
        if filename:
            self._contents = open(filename).readlines()
        else:
            self._contents = []
    def getLine(self, line):
        try:
            return self._contents[line]
        except:
            return ""

COMMAND_MODE = -1
INSERT_MODE = 1
DIRECTIONAL_KEYS = [ curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT ]

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super(StatusBar,self).__init__("", parent)
        index = gui.VApplication.vApp.screen().getColor(6,4)
        self.setColor(index)
        self._filename = ""
        self._position = ""

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, row, col):
        self._position = str(row)+","+str(col)
        self._updateText()

    def _updateText(self):
        self.setText(self._filename+" "+self._position)

class CommandBar(gui.VLabel):
    def __init__(self, parent):
        super(CommandBar,self).__init__("", parent)
        self._mode = None

    def _updateText(self):
        if self._mode == INSERT_MODE:
            self.setText("-- INSERT --")
        else:
            self.setText("")

    def setMode(self, mode):
        self._mode = mode
        self._updateText()

class Editor(gui.VWidget):
    def __init__(self, model, parent=None):
        super(Editor, self).__init__(parent)
        self._model = model
        self._top_line = 0
        self._cursor_pos = (0,0)
        self._state = COMMAND_MODE
        self._status_bar = StatusBar(self)
        self._command_bar = CommandBar(self)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)

        self._command_bar.move(0, self.size()[1]-1)
        self._command_bar.resize(self.size()[0], 1)

    def statusBar(self):
        return self._status_bar

    def render(self, painter):
        w, h = self.size()
        num_digits = math.log10(h)+1
        for i in xrange(0, h):
            painter.write(0, i, str(i+self._top_line).rjust(num_digits+1), 0)

        for i in xrange(0, h):
            painter.write(num_digits+1, i, "|", 0)

#        for i in xrange(0, h):
#            abs_pos = self.mapToGlobal(x+num_digits+2, y+i)
#            screen.write(abs_pos[0], abs_pos[1], self._model.getLine(self._top_line+i), 0)

        super(Editor, self).render(painter)

    def keyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            self._moveCursor(event)
        elif event.key() == 27 and self._state == INSERT_MODE:
            self._state = COMMAND_MODE
            self._command_bar.setMode(self._state)
        elif event.key() == ord('i') and self._state == COMMAND_MODE:
            self._state = INSERT_MODE
            self._command_bar.setMode(self._state)


        event.accept()

    def _moveCursor(self, event):
        if event.key() == curses.KEY_UP:
            self._cursor_pos = (self._cursor_pos[0], max(0, self._cursor_pos[1]-1))
        elif event.key() == curses.KEY_DOWN:
            self._cursor_pos = (self._cursor_pos[0], self._cursor_pos[1]+1)
        elif event.key() == curses.KEY_LEFT:
            self._cursor_pos = (max(self._cursor_pos[0]-1,0), self._cursor_pos[1])
        elif event.key() == curses.KEY_RIGHT:
            self._cursor_pos = (self._cursor_pos[0]+1, self._cursor_pos[1])

        self._status_bar.setPosition(*self._cursor_pos)
        gui.VCursor.move(self._cursor_pos[0]+self.pos()[0], self._cursor_pos[1]+self.pos()[1])
