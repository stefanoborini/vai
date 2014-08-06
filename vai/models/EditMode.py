from vaitk import core

class EditMode(core.VObject):
    """
    Separate model class to hold the current editor mode
    """
    COMMAND = 0
    COMMAND_INPUT = 1
    INSERT = 2
    REPLACE = 3
    VISUAL_BLOCK = 4
    VISUAL_LINE = 5
    VISUAL = 6
    DELETE = 7
    SEARCH_FORWARD = 8
    SEARCH_BACKWARD = 9
    GO = 10
    YANK = 11

    def __init__(self, mode):
        super().__init__()

        self._mode = mode
        self.changed = core.VSignal(self)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if self._mode != mode:
            self._mode = mode
            self.changed.emit(mode)



