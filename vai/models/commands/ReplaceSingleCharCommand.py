from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class ReplaceSingleCharCommand(BufferCommand):
    def __init__(self, buffer, char):
        super().__init__(buffer)
        self._char = char

    def execute(self):
        document = self._buffer.document
        cursor = self._buffer.cursor
        
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        
        pos = self.savedCursorPos()
        cursor.toPos(pos)
         
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        document.lineMetaInfo("Change").setData('modified', pos[0])
        deleted = document.replaceChars(pos, 1, self._char)
        return CommandResult(True, deleted)

