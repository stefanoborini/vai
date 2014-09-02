from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class DeleteToEndOfWordCommand(BufferCommand):
    SPACERS = " {}[]().!@#$%^&*()=,"

    def execute(self):
        cursor = self._buffer.cursor
        document = self._buffer.document

        pos = cursor.pos
        self.saveCursorPos()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMeta(pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        text = document.lineText(pos[0])

        # Zero based, for text.
        cur_index = pos[1]-1

        if text[cur_index] in DeleteToEndOfWordCommand.SPACERS:
            # cursor is on a spacer. Delete everything up to the first non spacer
            remove_count = len(text[cur_index:]) - len(text[cur_index:].lstrip(DeleteToEndOfWordCommand.SPACERS))
        else:
            # Get the next spacer from the current position.
            # It's the first of this list comprehension, if available
            spacer_indexes = [ p for p, c in enumerate(text) if (p > cur_index and c in DeleteToEndOfWordCommand.SPACERS)]
            if len(spacer_indexes) == 0:
                remove_count = document.lineLength(pos[0]) - cur_index + 1
            else:
                # Remove the non-spacer, plus all the spacers up to the next non-spacer
                remove_count = spacer_indexes[0] - cur_index
                remove_count += len(text[cur_index+remove_count:]) - len(text[cur_index+remove_count:].lstrip(DeleteToEndOfWordCommand.SPACERS))

        deleted = document.deleteChars(pos, remove_count)
        return CommandResult(success=True, info=deleted)


