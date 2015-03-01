from .TextDocument import TextDocument
from .TextDocumentCursor import TextDocumentCursor
from .EditAreaModel import EditAreaModel
from .CommandHistory import CommandHistory

class Buffer:
    """
    Represents an editable buffer, and contains the document, the cursor
    position, the command history, and all the state that is local to a
    specific buffer.
    """
    def __init__(self):
        self._document = TextDocument()
        self._document_cursor = TextDocumentCursor(self._document)
        self._edit_area_model = EditAreaModel()
        self._command_history = CommandHistory()
        self._selection_start_pos = None
        self._document.createLineMetaInfo("LinterResult")
        self._document.createLineMetaInfo("Change")
        self._document.createLineMetaInfo("Bookmark")

    def isEmpty(self):
        """
        Returns True if the document is empty
        """
        return self._document.isEmpty()

    def isModified(self):
        """
        Returns True if the document is modified
        """
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

    @property
    def selection_start_pos(self):
        return self._selection_start_pos
    
    @selection_start_pos.setter
    def selection_start_pos(self, pos):
        self._selection_start_pos = pos
        
