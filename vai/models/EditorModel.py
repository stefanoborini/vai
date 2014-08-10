from vaitk import core
from .. import flags
from .BufferList import BufferList
from .EditMode import EditMode

class EditorModel(core.VObject):
    def __init__(self):
        super().__init__()
        self._edit_mode = EditMode(EditMode.COMMAND)
        self._buffer_list = BufferList()
        self._current_search = None
        self._clipboard = None

    @property
    def edit_mode(self):
        return self._edit_mode

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

    @property
    def buffer_list(self):
        return self._buffer_list
