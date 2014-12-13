from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class NewLineCommand(BufferCommand):
    def execute(self):
        document = self._document
        cursor = self._cursor
        pos = cursor.pos
        self.saveCursorPos()

        current_text = document.lineText(pos[0])
        current_indent = len(current_text) - len(current_text.lstrip(' '))

        document.newLine(pos[0])
        document.insertChars( (pos[0], 1), ' '*current_indent )
        line_meta = document.lineMetaInfo("Change")
        line_meta.setData("added", pos[0])
        cursor.toPos( (pos[0], document.lineLength(pos[0])))
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self._saved_cursor_pos[0])
        self.restoreCursorPos()

