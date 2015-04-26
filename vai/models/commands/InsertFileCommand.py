from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertFileCommand(BufferCommand):
    def __init__(self, buffer, filename):
        super().__init__(buffer)
        self._filename = filename
        self._how_many = None

    def execute(self):
        document = self._document
        cursor = self._cursor

        try:
            with open(self._filename,'r') as f:
                lines = f.readlines()
        except:
            return CommandResult(False, None)

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        self.saveModifiedState()
        pos = self.savedCursorPos()

        line_pos = pos[0]
        cursor.toPos((line_pos, 1))

        self._how_many = len(lines)
        document.insertLines(line_pos, lines)
        document.lineMetaInfo("Change").setData(["added"] * self._how_many, line_pos)
        document.documentMetaInfo("Modified").setData(True)

        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLines(self.savedCursorPos()[0], self._how_many)
        super().undo()


