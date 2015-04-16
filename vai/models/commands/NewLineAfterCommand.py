from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class NewLineAfterCommand(BufferCommand):
    def execute(self):
        document = self._document
        cursor = self._cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()

        current_text = document.lineText(pos[0])
        current_indent = len(current_text) - len(current_text.lstrip(' '))

        document.newLineAfter(pos[0])
        document.insertChars( (pos[0]+1, 1), ' '*current_indent )
        document.lineMetaInfo("Change").setData("added", pos[0]+1)
        cursor.toPos((pos[0]+1, 1))
        cursor.toLineEnd()
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self.savedCursorPos()[0]+1)
        self.restoreCursorPos()

