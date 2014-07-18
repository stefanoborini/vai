from vixtk import core
from .. import flags

class EditorModel(core.VObject):
    def __init__(self):
        super().__init__()
        self._mode = flags.COMMAND_MODE
        self._current_search = None
        self.modeChanged = core.VSignal(self)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if self._mode != mode:
            self._mode = mode
            self.modeChanged.emit(self._mode)

    @property
    def current_search(self):
        return self._current_search

    @current_search.setter
    def current_search(self, search):
        self._current_search = search
