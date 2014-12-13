from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteSingleCharAfterCommand(BufferCommand):
    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        if pos[1] == document.lineLength(pos[0]):
            return CommandResult(success=False, info=None)

        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])

        if changed is None:
            line_meta.setData("modified", pos[0])

        deleted = document.deleteChars(pos, 1)
        return CommandResult(success=True, info=deleted)

