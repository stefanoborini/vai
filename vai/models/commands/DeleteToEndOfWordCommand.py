from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteToEndOfWordCommand(BufferCommand):
    SPACERS = " {}[]().!@#$%^&*=,"

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
        if changed is None:
            line_meta.setData("modified", pos[0])

        text = document.lineText(pos[0])

        # Zero based, for text.
        cur_index = pos[1]-1

        char_under_cursor = text[cur_index]
        if text[cur_index] in DeleteToEndOfWordCommand.SPACERS:
            # cursor is on a spacer. Delete everything up to the first non spacer
            # or the first spacer that is not the one we are currently on.
            remove_count = len(text[cur_index:]) - len(text[cur_index:].lstrip(char_under_cursor))
            remove_count += len(text[cur_index+remove_count:]) - len(text[cur_index+remove_count:].lstrip(' '))
        else:
            # Get the next spacer from the current position.
            # It's the first of this list comprehension, if available
            spacer_indexes = [ p for p, c in enumerate(text) if (p > cur_index and c in DeleteToEndOfWordCommand.SPACERS)]
            if len(spacer_indexes) == 0:
                # None, just remove to end of line
                remove_count = document.lineLength(pos[0]) - cur_index + 1
            else:
                # Remove the non-spacer, plus all the ' ' up to the next spacer
                remove_count = spacer_indexes[0] - cur_index
                remove_count += len(text[cur_index+remove_count:]) - len(text[cur_index+remove_count:].lstrip(' '))

        deleted = document.deleteChars(pos, remove_count)
        document.documentMetaInfo("Modified").setData(True)
        return CommandResult(success=True, info=deleted)


