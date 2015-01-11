from vaitk import gui, core

class InfoHoverBox(core.VObject):
    """
    View class that observes the buffer. If the cursor hovers a line where the
    Linting has information, shows a popup containing the associated message
    """

    def __init__(self):
        self._buffer = None
        self._current_shown_line = None

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buf):
        if buf is None:
            raise Exception("Buffer cannot be None")

        if self._buffer is not None:
            self._buffer.cursor.positionChanged.disconnect(self._cursorPositionChanged)

        self._buffer = buf
        self._buffer.cursor.positionChanged.connect(self._cursorPositionChanged)

    def _cursorPositionChanged(self, *args):
        if self._buffer is None:
            return

        cursor = self._buffer.cursor
        pos_at_top = self._buffer.edit_area_model.document_pos_at_top

        if self._current_shown_line == cursor.pos[0]:
            gui.VToolTip.hide()
            return

        lint = self._buffer.document.lineMetaInfo("LinterResult").data(cursor.pos[0])

        if lint is not None:
            self._current_shown_line = cursor.pos[0]
            gui.VToolTip.showText((0, cursor.pos[0]-pos_at_top[0]+1), lint.message)
        else:
            self._current_shown_line = None
            gui.VToolTip.hideText()
