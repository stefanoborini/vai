from ..models import Configuration
from vaitk import gui

class StatusBarController(object):
    def __init__(self, status_bar):
        self._status_bar = status_bar
        self._status_bar.setColors(gui.VGlobalColor.nameToColor(Configuration.get("colors.status_bar.fg")),
                                   gui.VGlobalColor.nameToColor(Configuration.get("colors.status_bar.bg"))
                                  )
        self._buffer = None

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        if self._buffer is not None:
            self._buffer.document.modifiedChanged.disconnect(self._status_bar.setFileChangedFlag)
            self._buffer.document.filenameChanged.disconnect(self._status_bar.setFilename)
            self._buffer.cursor.positionChanged.disconnect(self._status_bar.setPosition)

        self._buffer = buffer

        # Connect the signals
        self._buffer.document.modifiedChanged.connect(self._status_bar.setFileChangedFlag)
        self._buffer.document.filenameChanged.connect(self._status_bar.setFilename)
        self._buffer.cursor.positionChanged.connect(self._status_bar.setPosition)

        # Update the widget
        self._status_bar.setFilename(self._buffer.document.filename())
        self._status_bar.setFileChangedFlag(self._buffer.document.isModified())
        self._status_bar.setPosition(self._buffer.cursor.pos)
