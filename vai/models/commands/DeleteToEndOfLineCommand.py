from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteToEndOfLineCommand(BufferCommand):
    def execute(self):
        cursor = self._buffer.cursor
        document = self._buffer.document

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()
        cursor.toPos(pos)

        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])
        if changed:
            line_meta.setData("modified", pos[0])

        deleted = document.deleteChars(pos, document.lineLength(pos[0])-pos[1])
        cursor.toCharPrev()
        document.documentMetaInfo("Modified").setData(True)
        return CommandResult(success=True, info=deleted)

