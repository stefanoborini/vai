from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertLineAfterCommand(BufferCommand):
    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        document = self._buffer.document
        cursor = self._buffer.cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()
        cursor.toPos(pos)

        document.insertLine(pos[0]+1, self._text)
        document.lineMetaInfo("Change").setData("added", pos[0]+1)
        cursor.toLineNext()
        return CommandResult(True, None)

    def undo(self):
        self._buffer.document.deleteLine(self.savedCursorPos()[0]+1)
        self.restoreCursorPos()

