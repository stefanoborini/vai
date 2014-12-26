from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from .NewLineCommand import NewLineCommand
from .NewLineAfterCommand import NewLineAfterCommand

class BreakLineCommand(BufferCommand):
    def execute(self):
        cursor = self._cursor
        document = self._document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        
        pos = self.savedCursorPos()

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

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        current_text = document.lineText(pos[0])
        current_indent = len(current_text) - len(current_text.lstrip(' '))

        document.breakLine(pos)
        text_broken_line = document.lineText(pos[0]+1)
        document.deleteChars((pos[0]+1, 1), len(text_broken_line)-len(text_broken_line.lstrip(' ')))
        document.insertChars( (pos[0]+1, 1), ' '*current_indent )
        cursor.toPos((pos[0]+1, current_indent+1))

        line_meta = document.lineMetaInfo("Change")

        if line_meta.data(pos[0]) == None:
            line_meta.setData([ "modified", "added" ], pos[0])
        else:
            line_meta.setData([ "added" ], pos[0]+1)

        return CommandResult(success=True, info=None)

    def undo(self):
        self.restoreCursorPos()

        if self._sub_command is not None:
            self._sub_command.undo()
            self._sub_command = None
            return

        self.restoreLineMemento()
        self._document.deleteLine(self._cursor.pos[0]+1)

