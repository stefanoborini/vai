from videtoolkit import gui, core, utils
from . import flags

class CommandBar(gui.VLabel):
    def __init__(self, parent=None):
        super(CommandBar,self).__init__(parent)
        self._mode = None
        self._updateText()

    def setMode(self, mode):
        self._mode = mode
        self._updateText()

    def _updateText(self):
        if self._mode == flags.INSERT_MODE:
            self.setText("-- INSERT --")
        elif self._mode == flags.REPLACE_MODE:
            self._setText("-- REPLACE --")
        elif self._mode == flags.VISUAL_BLOCK_MODE:
            self._setText("-- VISUAL BLOCK --")
        elif self._mode == flags.VISUAL_LINE_MODE:
            self._setText("-- VISUAL LINE --")
        elif self._mode == flags.VISUAL_MODE:
            self._setText("-- VISUAL --")
        else:
            self.setText("")

