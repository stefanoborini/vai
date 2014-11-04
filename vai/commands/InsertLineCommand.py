from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

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
        line_meta = document.lineMetaInfo("Change")
        line_meta.setData(pos[0], "added")
        cursor.toPos((pos[0], 1))
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self._saved_cursor_pos[0])
        self.restoreCursorPos()


