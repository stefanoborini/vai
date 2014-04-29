class StatusBarController(object):
    def __init__(self, status_bar):
        self._status_bar = status_bar
        self._document_model = None
        self._view_model = None

    def setModels(self, document_model, view_model):
        if self._document_model:
            self._document_model.modifiedChanged.disconnect(self._status_bar.setFileChangedFlag)
            self._document_model.filenameChanged.disconnect(self._status_bar.setFilename)

        self._document_model = document_model
        self._document_model.modifiedChanged.connect(self._status_bar.setFileChangedFlag)
        self._document_model.filenameChanged.connect(self._status_bar.setFilename)

        self._status_bar.setFilename(self._document_model.filename())
        self._status_bar.setFileChangedFlag(self._document_model.isModified())
