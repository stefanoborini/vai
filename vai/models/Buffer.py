from .TextDocument import TextDocument
from .TextDocumentCursor import TextDocumentCursor
from .EditAreaModel import EditAreaModel

class Buffer:
    def __init__(self):
        self._document = TextDocument()
        self._document_cursor = TextDocumentCursor(self._document)
        self._edit_area_model = EditAreaModel()
        self._command_history = CommandHistory()

    def isEmpty(self):
        return self._document.isEmpty()

    def isModified(self):
        return self._document.isModified()

    @property
    def document(self):
        return self._document

    @property
    def cursor(self):
        return self._document_cursor

    @property
    def edit_area_model(self):
        return self._edit_area_model

    @property
    def command_history(self):
        return self._command_history

class CommandHistory:
    def __init__(self):
        self._history = []

    def __len__(self):
        return len(self._history)

    def push(self, command):
        self._history.append(command)

    def pop(self):
        return self._history.pop()
