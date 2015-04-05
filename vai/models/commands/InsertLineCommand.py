from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertLineCommand(BufferCommand):
    def __init__(self, buffer, text):
        super().__init__(buffer)
        if isinstance(text, list):
            self._text = text
        else:
            self._text = [ text ]

    def execute(self):
        document = self._document
        cursor = self._cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()

        for text in reversed(self._text):
            document.insertLine(pos[0], text)
            document.lineMetaInfo("Change").setData("added", pos[0])
            cursor.toCharFirstNonBlankForLine(pos[0])

        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self._saved_cursor_pos[0])
        self.restoreCursorPos()


