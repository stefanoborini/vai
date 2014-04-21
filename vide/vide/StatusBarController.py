class StatusBarController(object):
    def __init__(self, status_bar, document_model, view_model):
        self._status_bar = status_bar
        self._view_model = view_model
        self._document_model = document_model

        self._document_model.modifiedChanged.connect(self._status_bar.setFileChangedFlag)
