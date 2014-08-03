from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class JoinWithNextLineCommand(BufferCommand):
    def execute(self):
        cursor = self._cursor
        document = self._document
        pos = cursor.pos

        if pos[0] == document.numLines():
            return CommandResult(success=False, info=None)

        self.saveCursorPos()
        line_meta = document.lineMeta(self._pos[0])

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        self.saveLineMemento(pos[0]+1, BufferCommand.MEMENTO_INSERT)

        document.joinWithNextLine(pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(pos[0], {LineMeta.Change: "modified"})

        return CommandResult(success=True, info=None)

