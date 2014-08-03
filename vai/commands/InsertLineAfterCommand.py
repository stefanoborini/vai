from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertLineAfterCommand(BufferCommand):
    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        self.saveCursorPos()

        document.insertLine(cursor.pos[0]+1, self._text)
        cursor.toLineNext()
        return CommandResult(True, None)

    def undo(self):
        document.deleteLine(self._saved_cursor_pos[0]+1)
        self.restoreCursorPos()

