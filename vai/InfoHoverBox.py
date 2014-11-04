from vaitk import gui, core

class InfoHoverBox(core.VObject):
    def __init__(self, buffer):
        self._buffer = None

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

        meta = self._buffer.document.lineMetaInfo("LinterResult").data(1, self._buffer.document.numLines())
        lint = meta[cursor.pos[0]-1]

        if lint is not None:
            gui.VToolTip.showText((0, cursor.pos[0]-pos_at_top[0]+1), lint.message)
        else:
            gui.VToolTip.hide()
