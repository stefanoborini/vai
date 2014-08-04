from .TextDocumentCursor import TextDocumentCursor

class Buffer:
    def __init__(self, document, edit_area_model):
        self._document = document
        self._document_cursor = TextDocumentCursor(self._document)
        self._edit_area_model = edit_area_model
        self._command_history = []

    def isEmpty(self):
        return self._document.isEmpty()

    def isModified(self):
        return self._document.isModified()

    def document(self):
        return self._document

    @property
    def cursor(self):
        return self._document_cursor

    def documentCursor(self):
        return self._document_cursor

    def editAreaModel(self):
        return self._edit_area_model

    def commandHistory(self):
        return self._command_history

    def addCommandHistory(self, command):
        self._command_history.append(command)

    def popCommandHistory(self):
        return self._command_history.pop()
