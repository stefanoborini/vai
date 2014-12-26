from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteSingleCharAfterCommand(BufferCommand):
    def execute(self):
        document = self._document

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()
        
        self._cursor.toPos(pos)
 
        if pos[1] == document.lineLength(pos[0]):
            return CommandResult(success=False, info=None)

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])

        if changed is None:
            line_meta.setData("modified", pos[0])

        deleted = document.deleteChars(pos, 1)
        return CommandResult(success=True, info=deleted)

