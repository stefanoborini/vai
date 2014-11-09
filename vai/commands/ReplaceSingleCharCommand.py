from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class ReplaceSingleCharCommand(BufferCommand):
    def __init__(self, buffer, char):
        super().__init__(buffer)
        self._char = char

    def execute(self):
        document = self._buffer.document
        cursor = self._buffer.cursor
        pos = cursor.pos
        meta_info = document.lineMetaInfo("Change")

        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        meta_info.setData('modified', pos[0])
        deleted = document.replaceChars(pos, 1, self._char)
        return CommandResult(True, deleted)

