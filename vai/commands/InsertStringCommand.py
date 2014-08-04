from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class InsertStringCommand(BufferCommand):
    """
    Insert a text string in the document at the current cursor position.
    """
    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMeta(pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        document.insertChars(pos, self._text)
        cursor.toPos( (pos[0], pos[1]+len(self._text)) )
        return CommandResult(success=True, info=None)

