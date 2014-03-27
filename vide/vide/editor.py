import videtoolkit
from videtoolkit import gui, core, utils
import logging
import curses
import math

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

DIRECTIONAL_KEYS = [ videtoolkit.Key.Key_Up, videtoolkit.Key.Key_Down, videtoolkit.Key.Key_Left, videtoolkit.Key.Key_Right ]

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super(StatusBar,self).__init__("", parent)
        self._filename = ""
        self._position = ""
        self.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)

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
        super(CommandBar,self).__init__(parent)
        self._view_model = view_model
        self._view_model.changed.connect(self.updateContent)
        self._mode = None
        self._updateText()

    def _updateText(self):
        if self._mode == INSERT_MODE:
            self.setText("-- INSERT --")
        else:
            self.setText("")

    def setMode(self, mode):
        self._mode = mode
        self._updateText()

    def updateContent(self):
        self.setMode(self._view_model.state())

class EditorController(core.VObject):
    def __init__(self, document_model, view_model, view):
        self._document_model = document_model
        self._view_model = view_model
        self._view = view
        self._command_history = []

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._view.moveCursor(event)
            event.accept()
            return

        if self._view_model.state() == INSERT_MODE:
            if event.key() == videtoolkit.Key.Key_Escape:
                self._view_model.setState(COMMAND_MODE)
                event.accept()
            return

        if self._view_model.state() == COMMAND_MODE:
            if event.key() == videtoolkit.Key.Key_I and event.modifiers() == 0:
                self._view_model.setState(INSERT_MODE)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() == 0:
                self._view_model.setState(INSERT_MODE)
                command = InsertLineAfterCommand(self._document_model, 2)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._view_model.setState(INSERT_MODE)
                command = InsertLineBeforeCommand(self._document_model, 2)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_U and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                if len(self._command_history):
                    command = self._command_history.pop()
                    command.undo()


            event.accept()

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super(Editor, self).__init__(parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._view_model.changed.connect(self.viewModelChanged)
        self._controller = EditorController(self._document_model, self._view_model, self)
        self._status_bar = StatusBar(self)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)
        self._status_bar.setFilename(self._document_model.filename())

        self._command_bar = CommandBar(self._view_model, self)
        self._command_bar.move(0, self.size()[1]-1)
        self._command_bar.resize(self.size()[0], 1)

        self._cursor_pos = (2,2)
        self.setFocus()


    def statusBar(self):
        return self._status_bar

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        num_digits = int(math.log10(self._document_model.numLines()))+1
        for i in xrange(0, h-2):
            painter.clear(0, i, w, 1)
            painter.write(0, i, str(i+self._view_model.topLine()).rjust(num_digits+1)+"  ")
            painter.write(num_digits+3, i, self._document_model.getLine(self._view_model.topLine()+i))

        gui.VCursor.setPos(self._cursor_pos[0], self._cursor_pos[1])

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)

    def moveCursor(self, event):
        if event.key() == videtoolkit.Key.Key_Up:
            self._cursor_pos = (self._cursor_pos[0], max(0, self._cursor_pos[1]-1))
        elif event.key() == videtoolkit.Key.Key_Down:
            self._cursor_pos = (self._cursor_pos[0], self._cursor_pos[1]+1)
        elif event.key() == videtoolkit.Key.Key_Left:
            self._cursor_pos = (max(self._cursor_pos[0]-1,0), self._cursor_pos[1])
        elif event.key() == videtoolkit.Key.Key_Right:
            self._cursor_pos = (self._cursor_pos[0]+1, self._cursor_pos[1])

        self._status_bar.setPosition(*self._cursor_pos)
        logging.info("moving cursor %s" % str(self._cursor_pos))
        gui.VCursor.setPos(self._cursor_pos[0]+self.pos()[0], self._cursor_pos[1]+self.pos()[1])

    def viewModelChanged(self):
        self.update()

    def update(self):
        pass
