import vaitk
from vaitk import gui, core
from ..models import EditorMode

EditorModeView = {
        EditorMode.COMMAND_INPUT : "Command: ",
        EditorMode.DELETE : "Delete ...",
        EditorMode.SEARCH_FORWARD : "Search: ",
        EditorMode.SEARCH_BACKWARD : "Search backward: ",
        EditorMode.GO : "Go to ...",
        EditorMode.BOOKMARK : "Set bookmark ...",
        EditorMode.GOTOBOOKMARK : "Go to bookmark ...",
        EditorMode.INSERT : "-- INSERT --",
        EditorMode.VISUAL_BLOCK : "-- VISUAL BLOCK --",
        EditorMode.VISUAL_LINE : "-- VISUAL LINE--",
        EditorMode.VISUAL : "-- VISUAL --",
        EditorMode.REPLACE : "-- REPLACE --",
        }

class CommandBar(gui.VWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.returnPressed = core.VSignal(self)
        self.escapePressed = core.VSignal(self)
        self.tabPressed = core.VSignal(self)

        self._editor_mode = EditorMode.COMMAND

        self._state_label = gui.VLabel(parent=self)
        self._state_label.setGeometry((0,0,1,1))

        self._line_edit = gui.VLineEdit(parent=self)
        self._line_edit.returnPressed.connect(self.returnPressed)
        self._line_edit.setGeometry((1,0,self.width()-1,1))
        self._line_edit.installEventFilter(self)
        self._updateText()

    @property
    def editor_mode(self):
        return self._editor_mode

    @editor_mode.setter
    def editor_mode(self, editor_mode):
        self._editor_mode = editor_mode
        self._updateText()

    def setEditorMode(self, editor_mode):
        self.editor_mode = editor_mode

    @property
    def command_text(self):
        return self._line_edit.text().strip()

    @command_text.setter
    def command_text(self, text):
        self._line_edit.setText(text)
        self._line_edit.end()

    def clear(self):
        self._editor_mode = EditorMode.COMMAND
        self._line_edit.clear()
        self._updateText()

    def setFocus(self):
        self._line_edit.setFocus()

    def eventFilter(self, event):
        if isinstance(event, gui.VKeyEvent):
            if event.key() == vaitk.Key.Key_Escape:
                self.escapePressed.emit()
                return True
            elif event.key() == vaitk.Key.Key_Backspace and len(self.command_text) == 0:
                self.escapePressed.emit()
                return True
            if event.key() == vaitk.Key.Key_Tab:
                self.tabPressed.emit()
                return True
        return False

    def setErrorString(self, error_string):
        self._line_edit.clear()
        self._state_label.resize( (len(error_string), 1) )
        self._state_label.setText(error_string)
        self._line_edit.setGeometry( (len(error_string), 0, self.width()-len(error_string), 1) )

    # Private

    def _updateText(self):
        text = EditorModeView.get(self._editor_mode, "")
        self._state_label.resize( (len(text), 1) )
        self._state_label.setText(text)
        self._line_edit.setGeometry( (len(text), 0, self.width()-len(text), 1) )

