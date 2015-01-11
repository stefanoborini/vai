from vaitk import gui, core

class InfoHoverBox(core.VObject):
    """
    View class that observes the buffer. If the cursor hovers a line where the
    Linting has information, shows a popup containing the associated message
    """

    def __init__(self):
        self._buffer = None

        # The line for which the popup is visible 
        self._current_shown_line = None
        self._hide_timer = core.VTimer()
        self._hide_timer.setInterval(2000)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._toolTipTimeOut)

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buf):
        if buf is None:
            raise Exception("Buffer cannot be None")

        if self._hide_timer.isRunning():
            self._hide_timer.stop()

        if self._buffer is not None:
            self._buffer.cursor.positionChanged.disconnect(self._cursorPositionChanged)

        self._buffer = buf
        self._buffer.cursor.positionChanged.connect(self._cursorPositionChanged)

    def _cursorPositionChanged(self, *args):
        if self._buffer is None:
            return

        cursor = self._buffer.cursor

        # If the cursor changed but remained on the same line, let things be
        if self._current_shown_line == cursor.pos[0]:
            return

        # Line changed. Stop the timer and hide the tooltip.
        self._hide_timer.stop()
        gui.VToolTip.hideText()

        # If there's information, show the new one
        lint = self._buffer.document.lineMetaInfo("LinterResult").data(cursor.pos[0])

        if lint is not None:
            pos_at_top = self._buffer.edit_area_model.document_pos_at_top
            self._current_shown_line = cursor.pos[0]
            gui.VToolTip.showText((0, cursor.pos[0]-pos_at_top[0]+1), lint.message)
            self._hide_timer.start()
        else:
            self._current_shown_line = None
        
    def _toolTipTimeOut(self):
        """Callback to hide the tooltip after a few seconds"""
        gui.VToolTip.hideText()



