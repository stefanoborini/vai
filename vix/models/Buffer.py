class Buffer:
    def __init__(self, document, view_model):
        self._document = document
        self._document_cursor = None
        self._view_model = view_model
        self._command_history = []

    def isEmpty(self):
        return self._document.isEmpty()

    def isModified(self):
        return self._document.isModified()

    def document(self):
        return self._document

    def documentCursor(self):
        return self._document_cursor

    def viewModel(self):
        return self._view_model

    def commandHistory(self):
        return self._command_history

    def addCommandHistory(self, command):
        self._command_history.append(command)

    def popCommandHistory(self):
        return self._command_history.pop()
