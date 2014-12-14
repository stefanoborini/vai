from vaitk import core
from .EditorMode import EditorMode

class GlobalState(core.VObject):
    """
    Represents global state of the editor that is not dependent on
    the currently selected buffer.
    """
    def __init__(self):
        super().__init__()
        self._editor_mode = EditorMode.COMMAND
        self._current_search = None
        self._clipboard = None

        self.editorModeChanged = core.VSignal(self)

    @property
    def editor_mode(self):
        return self._editor_mode

    @editor_mode.setter
    def editor_mode(self, mode):
        if self._editor_mode != mode:
            self._editor_mode = mode
            self.editorModeChanged.emit(mode)

    @property
    def current_search(self):
        return self._current_search

    @current_search.setter
    def current_search(self, search):
        assert(len(search) == 2)
        self._current_search = search

    @property
    def clipboard(self):
        return self._clipboard

    @clipboard.setter
    def clipboard(self, text):
        self._clipboard = text

