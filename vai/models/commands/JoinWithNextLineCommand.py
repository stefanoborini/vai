from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class JoinWithNextLineCommand(BufferCommand):
    def execute(self):
        document = self._document
       
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        
        pos = self.savedCursorPos() 
        
        if pos[0] == document.numLines():
            return CommandResult(success=False, info=None)

        self._cursor.toPos(pos)

        line_meta = document.lineMetaInfo("Change")

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        self.saveLineMemento(pos[0]+1, BufferCommand.MEMENTO_INSERT)

        document.joinWithNextLine(pos[0])
        if line_meta.data(pos[0]) == None:
            line_meta.setData("modified", pos[0])

        return CommandResult(success=True, info=None)

