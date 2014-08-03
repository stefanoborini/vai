from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class DeleteToEndOfWordCommand(BufferCommand):
    SPACERS = " {}[]().!@#$%^&*()=,"

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()

        pos = cursor.pos
        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMeta(pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        text = document.lineText(pos[0])
        if text[pos[1]-1] in DeleteToEndOfWordCommand.SPACERS:
            remove_count = len(text[pos[1]-1:]) - len(text[pos[1]-1:].lstrip(DeleteToEndOfWordCommand.SPACERS))
        else:
            # Get the next spacer from the current position.
            # It's the first of this list comprehension, if available
            spacer_indexes = [ pos for pos, c in enumerate(text) if (pos > pos[1]-1 and c in DeleteToEndOfWordCommand.SPACERS)]
            if len(spacer_indexes) == 0:
                remove_count = document.lineLength(pos[0])-pos[1]
            else:
                remove_count = (spacer_indexes[0]+1) - pos[1]

        deleted = document.deleteChars(self._pos, remove_count)
        return CommandResult(success=True, info=deleted)


