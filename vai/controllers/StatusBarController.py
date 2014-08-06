class StatusBarController(object):
    def __init__(self, status_bar):
        self._status_bar = status_bar
        self._document = None
        self._document_cursor = None

    def setModels(self, document, document_cursor):
        if self._document:
            self._document.modifiedChanged.disconnect(self._status_bar.setFileChangedFlag)
            self._document.filenameChanged.disconnect(self._status_bar.setFilename)

        if self._document_cursor:
            self._document_cursor.positionChanged.disconnect(self._status_bar.setPosition)

        self._document = document
        self._document.modifiedChanged.connect(self._status_bar.setFileChangedFlag)
        self._document.filenameChanged.connect(self._status_bar.setFilename)

        self._document_cursor = document_cursor
        self._document_cursor.positionChanged.connect(self._status_bar.setPosition)

        self._status_bar.setFilename(self._document.filename())
        self._status_bar.setFileChangedFlag(self._document.isModified())
        self._status_bar.setPosition(self._document_cursor.pos)
