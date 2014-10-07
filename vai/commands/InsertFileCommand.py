from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class InsertFileCommand(BufferCommand):
    def __init__(self, buffer, filename):
        super().__init__(buffer)
        self._filename = filename
        self._how_many = None

    def execute(self):
        document = self._document
        cursor = self._cursor
        line_pos = cursor.line

        try:
            with open(self._filename,'r') as f:
                lines = f.readlines()
        except:
            return CommandResult(False, None)

        self.saveCursorPos()
        self._how_many = len(lines)
        document.insertLines(line_pos, lines)
        document.updateLinesMeta(line_pos, self._how_many, {LineMeta.Change: "added"})

        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLines(self.savedCursorPos()[0], self._how_many)
        super().undo()


