from videtoolkit import gui, core, utils
import curses
import math


class EditorModel(core.VObject):
    def __init__(self, filename=None):
        if filename:
            self._contents = open(filename).readlines()
            self._filename = filename
        else:
            self._contents = []
            self._filename = 'noname.txt'

    def getLine(self, line):
        try:
            return self._contents[line]
        except:
            return ""

    def filename(self):
        return self._filename

COMMAND_MODE = -1
INSERT_MODE = 1

class ViewModel(core.VObject):
    def __init__(self):
        super(ViewModel, self).__init__()
        self._state = COMMAND_MODE
        self._top_line = 0
        self.changed = core.VSignal(self)

    def state(self):
        return self._state

    def setState(self, state):
        self._state = state
        self.changed.emit()

    def topLine(self):
        return self._top_line

    def setTopLine(self, top_line):
        self._top_line = top_line
        self.changed.emit()

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
        self.setText(utils.strformat([(0, self._filename),
                                      (self.width()-len(self._position)-3, self._position)
                                     ], self.width()))

class CommandBar(gui.VLabel):
    def __init__(self, view_model, parent=None):
        super(CommandBar,self).__init__("", parent)
        self._view_model = view_model
        self._view_model.changed.connect(self.update)
        self._mode = None

    def _updateText(self):
        if self._mode == INSERT_MODE:
            self.setText("-- INSERT --")
        else:
            self.setText("")

    def setMode(self, mode):
        self._mode = mode
        self._updateText()

    def update(self):
        self.setMode(self._view_model.state())

class EditorController(core.VObject):
    def __init__(self, document_model, view_model, view):
        self._document_model = document_model
        self._view_model = view_model
        self._view = view

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            self._view.moveCursor(event)
        elif event.key() == 27 and self._view_model.state() == INSERT_MODE:
            self._view_model.setState(COMMAND_MODE)
        elif event.key() == ord('i') and self._view_model.state() == COMMAND_MODE:
            self._view_model.setState(INSERT_MODE)


        event.accept()

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super(Editor, self).__init__(parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._view_model.changed.connect(self.viewModelChanged)
        self._controller = EditorController(self._document_model, self._view_model, self)
        self._cursor_pos = (0,0)
        self._status_bar = StatusBar(self)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)
        self._status_bar.setFilename(self._document_model.filename())

        self._command_bar = CommandBar(self._view_model, self)
        self._command_bar.move(0, self.size()[1]-1)
        self._command_bar.resize(self.size()[0], 1)

    def statusBar(self):
        return self._status_bar

    def render(self, painter):
        w, h = self.size()
        num_digits = math.log10(h)+1
        for i in xrange(0, h):
            painter.write(0, i, str(i+self._view_model.topLine()).rjust(num_digits+1), 0)

        for i in xrange(0, h):
            painter.write(num_digits+1, i, " ", 0)

        for i in xrange(0, h):
            painter.write(num_digits+2, i, self._document_model.getLine(self._view_model.topLine()+i), 0)

        super(Editor, self).render(painter)

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)

    def moveCursor(self, event):
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

    def viewModelChanged(self):
        self.update()

    def update(self):
        pass
