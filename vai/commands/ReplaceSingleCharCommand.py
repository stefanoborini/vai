from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class ReplaceSingleCharCommand(BufferCommand):
    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()
        pos = cursor.pos
        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        deleted = document.replaceChars(pos, 1, self._char)
        return CommandResult(True, deleted)

