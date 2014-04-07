from videtoolkit import gui, core, utils
from . import flags
import logging

class CommandBar(gui.VWidget):
    def __init__(self, parent=None):
        super(CommandBar,self).__init__(parent=parent)
        self.returnPressed = core.VSignal(self)

        self._mode = flags.COMMAND_MODE
        self._state_label = gui.VLabel(parent=self)
        self._state_label.setGeometry((0,0,10,1))
        self._line_edit = gui.VLineEdit(parent=self)
        self._line_edit.returnPressed.connect(self.returnPressed)
        self._line_edit.setGeometry((11,0,50,1))
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
            self._state_label.setText("-- INSERT --")
        if self._mode == flags.COMMAND_INPUT_MODE:
            self._state_label.setText(":")
        elif self._mode == flags.REPLACE_MODE:
            self._state_label.setText("-- REPLACE --")
        elif self._mode == flags.VISUAL_BLOCK_MODE:
            self._state_label.setText("-- VISUAL BLOCK --")
        elif self._mode == flags.VISUAL_LINE_MODE:
            self._state_label.setText("-- VISUAL LINE --")
        elif self._mode == flags.VISUAL_MODE:
            self._state_label.setText("-- VISUAL --")
        else:
            self._state_label.setText("")
