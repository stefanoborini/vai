from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteLineAtCursorCommand(BufferCommand):
    def execute(self):
        document = self._document
        if document.isEmpty():
            return CommandResult(success=False, info=None)

        cursor = self._cursor
        pos = cursor.pos
        self.saveCursorPos()

        if pos[0] == document.numLines():
            # Last line. Move the cursor up
            if not cursor.toLinePrev():
                # It's also the first line. Go at the beginning
                cursor.toLineBeginning()

        self.saveLineMemento(pos, BufferCommand.MEMENTO_INSERT)
        document.deleteLine(pos)

        # Deleted line, now we check the length of what comes up from below.
        # and set the cursor at the end of the line, if needed
        if document.lineLength(pos[0]) < pos[1]:
            cursor.toPos( (pos[0], document.lineLength(pos[0])))

        return CommandResult(success=True, info=self._line_memento)


