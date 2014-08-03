from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class DeleteToEndOfLineCommand(BufferCommand):
    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()
        pos = cursor.pos

        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMeta(pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars(self._pos, document.lineLength(pos[0])-pos[1])
        cursor.toCharPrev()
        return CommandResult(success=True, info=deleted)

