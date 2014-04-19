from videtoolkit import gui, core, utils
import videtoolkit
from . import flags
import logging

class CommandBar(gui.VWidget):
    def __init__(self, parent=None):
        super(CommandBar,self).__init__(parent=parent)
        self.returnPressed = core.VSignal(self)
        self.escapePressed = core.VSignal(self)

        self._mode = flags.COMMAND_MODE

        self._state_label = gui.VLabel(parent=self)
        self._state_label.setGeometry(core.VRect( core.VPoint(0,0), core.VSize(1,1)))

        self._line_edit = gui.VLineEdit(parent=self)
        self._line_edit.returnPressed.connect(self.returnPressed)
        self._line_edit.setGeometry(core.VRect( core.VPoint(1,0),core.VSize(self.width()-1,1)))
        self._line_edit.installEventFilter(self)
        self._updateText()

    def setMode(self, mode):
        logging.info("CommandBar: setting mode "+str(mode))
        self._mode = mode
        self._updateText()

    def commandText(self):
        return self._line_edit.text()

    def clear(self):
        self._mode = flags.COMMAND_MODE
        self._line_edit.clear()
        self._updateText()

    def setFocus(self):
        self._line_edit.setFocus()

    def _updateText(self):
        if self._mode == flags.INSERT_MODE:
            text = "-- INSERT --"
        elif self._mode == flags.COMMAND_INPUT_MODE:
            text = ":"
        elif self._mode == flags.REPLACE_MODE:
            text = "-- REPLACE --"
        elif self._mode == flags.VISUAL_BLOCK_MODE:
            text = "-- VISUAL BLOCK --"
        elif self._mode == flags.VISUAL_LINE_MODE:
            text = "-- VISUAL LINE --"
        elif self._mode == flags.VISUAL_MODE:
            text = "-- VISUAL --"
        else:
            text = ""

        self._state_label.resize( core.VSize(len(text), 1) )
        self._state_label.setText(text)
        self._line_edit.setGeometry(core.VRect( core.VPoint(len(text),0), core.VSize(self.width()-len(text),1)))

    def eventFilter(self, event):
        if isinstance(event, gui.VKeyEvent):
            if event.key() == videtoolkit.Key.Key_Escape:
                self.escapePressed.emit()
                return True
            elif event.key() == videtoolkit.Key.Key_Backspace and len(self.commandText()) == 0:
                self.escapePressed.emit()
                return True
        return False
