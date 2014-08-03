from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from ..models.TextDocument import LineMeta

class BreakLineCommand(BufferCommand):
    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        self.saveCursorPos()

        if pos[1] == document.lineLength(pos[0]):
            command = NewLineAfterCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
            return result

        if pos[1] == 1:
            command = NewLineCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
            cursor.toPos((pos[0]+1, 1))
            return result

        self.saveDocumentMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        current_text = document.lineText(pos[0])
        current_indent = len(current_text) - len(current_text.lstrip(' '))

        document.breakLine(self._pos)
        document.insertChars( (pos[0]+1, 1), ' '*current_indent )
        cursor.toPos((pos[0]+1, current_indent+1))

        line_meta = document.lineMeta(pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        document.updateLineMeta(pos[0]+1, {LineMeta.Change: "added"})
        return CommandResult(success=True, info=None)

    def undo(self):
        self.restoreCursorPos()

        if self._sub_command is not None:
            self._sub_command.undo()
            return

        self.restoreDocumentMemento()
        self._document.deleteLine(cursor.pos[0]+1)

