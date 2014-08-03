from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class InsertStringCommand(BufferCommand):
    """
    Insert a text string in the document
    at the current cursor position
    """
    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        self.saveCursorPos()
        self.saveLineMemento(pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        document.insertChars(self._pos, self._string)
        cursor.toPos( (self._pos[0], self._pos[1]+len(self._string)) )
        return CommandResult(success=True, info=None)

    def undo(self):
        self.restoreCursorPos()
        self.restoreLineMemento(BufferCommand.MEMENTO_REPLACE)

