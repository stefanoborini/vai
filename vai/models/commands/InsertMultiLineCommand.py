from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertMultiLineCommand(BufferCommand):
    AT_CURSOR = 0
    AFTER_CURSOR = 1
    def __init__(self, buffer, text, position):
        super().__init__(buffer)
        self._text = text
        self._position = position

    def execute(self):
        document = self._document
        cursor = self._cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()

        document.insertLines(pos[0]+self._position, self._text)
        document.lineMetaInfo("Change").setData(["added"]*len(self._text), pos[0]+self._position)
        cursor.toCharFirstNonBlankForLine(pos[0]+self._position)
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLines(self.savedCursorPos()[0]+self._position, len(self._text))
        self.restoreCursorPos()


