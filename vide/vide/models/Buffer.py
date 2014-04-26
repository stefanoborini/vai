class Buffer:
    def __init__(self, document_model, view_model):
        self._document_model = document_model
        self._view_model = view_model

    def isEmpty(self):
        return self._document_model.isEmpty()

    def isModified(self):
        return self._document_model.isModified()

    def documentModel(self):
        return self._document_model

    def viewModel(self):
        return self._view_model

