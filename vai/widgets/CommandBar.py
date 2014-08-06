import vaitk
from vaitk import gui, core
from ..models import EditMode

class CommandBar(gui.VWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.returnPressed = core.VSignal(self)
        self.escapePressed = core.VSignal(self)

        self._mode = EditMode.COMMAND

        self._state_label = gui.VLabel(parent=self)
        self._state_label.setGeometry((0,0,1,1))

        self._line_edit = gui.VLineEdit(parent=self)
        self._line_edit.returnPressed.connect(self.returnPressed)
        self._line_edit.setGeometry((1,0,self.width()-1,1))
        self._line_edit.installEventFilter(self)
        self._updateText()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        self._updateText()

    def setMode(self, mode):
        self.mode = mode

    @property
    def command_text(self):
        return self._line_edit.text()

    def clear(self):
        self._mode = EditMode.COMMAND
        self._line_edit.clear()
        self._updateText()

    def setFocus(self):
        self._line_edit.setFocus()

    def eventFilter(self, event):
        if isinstance(event, gui.VKeyEvent):
            if event.key() == vaitk.Key.Key_Escape:
                self.escapePressed.emit()
                return True
            elif event.key() == vaitk.Key.Key_Backspace and len(self.commandText()) == 0:
                self.escapePressed.emit()
                return True
        return False

    # Private

    def _updateText(self):
        if self._mode == EditMode.INSERT:
            text = "-- INSERT --"
        elif self._mode == EditMode.COMMAND_INPUT:
            text = ":"
        elif self._mode == EditMode.REPLACE:
            text = "-- REPLACE --"
        elif self._mode == EditMode.VISUAL_BLOCK:
            text = "-- VISUAL BLOCK --"
        elif self._mode == EditMode.VISUAL_LINE:
            text = "-- VISUAL LINE --"
        elif self._mode == EditMode.VISUAL:
            text = "-- VISUAL --"
        elif self._mode == EditMode.SEARCH_FORWARD:
            text = "/"
        elif self._mode == EditMode.SEARCH_BACKWARD:
            text = "?"
        else:
            text = ""

        self._state_label.resize( (len(text), 1) )
        self._state_label.setText(text)
        self._line_edit.setGeometry( (len(text), 0, self.width()-len(text), 1) )

