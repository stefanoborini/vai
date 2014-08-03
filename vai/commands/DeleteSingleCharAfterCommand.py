from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta


class DeleteSingleCharAfterCommand(BufferCommand):
    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        if pos[1] == document.lineLength(pos[0]):
            return CommandResult(success=False, info=None)

        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMeta(pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars(pos, 1)
        return CommandResult(success=True, info=deleted)

