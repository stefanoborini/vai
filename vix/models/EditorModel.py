from vixtk import core
from .. import flags

class EditorModel(core.VObject):
    def __init__(self):
        super().__init__()
        self._mode = flags.COMMAND_MODE
        self.modeChanged = core.VSignal(self)

    def mode(self):
        return self._mode

    def setMode(self, mode):
        if self._mode != mode:
            self._mode = mode
            self.modeChanged.emit(self._mode)

