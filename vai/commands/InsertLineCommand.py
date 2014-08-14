from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class InsertLineCommand(BufferCommand):
    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        document = self._document
        cursor = self._cursor
        pos = cursor.pos

        self.saveCursorPos()

        document.insertLine(pos[0], self._text)
        document.updateLineMeta(pos[0], {LineMeta.Change: "added"})
        cursor.toPos((pos[0], 1))
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self._saved_cursor_pos[0])
        self.restoreCursorPos()


