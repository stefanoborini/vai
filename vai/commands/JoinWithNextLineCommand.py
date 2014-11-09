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
        line_meta = document.lineMetaInfo("Change")

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        self.saveLineMemento(pos[0]+1, BufferCommand.MEMENTO_INSERT)

        document.joinWithNextLine(pos[0])
        if line_meta.data(pos[0]) == None:
            line_meta.setData("modified", pos[0])

        return CommandResult(success=True, info=None)

