from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class IndentCommand(BufferCommand):
    """
    Indent the line at the current cursor position.
    """
    def __init__(self, buffer):
        super().__init__(buffer)

    def execute(self):
        cursor = self._cursor
        document = self._document

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()
        self.saveModifiedState()

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        if changed is None:
            line_meta.setData("modified", pos[0])

        document.insertChars((pos[0], 1), " "*4)
        cursor.toPos((pos[0], pos[1]+4))
        document.documentMetaInfo("Modified").setData(True)

        return CommandResult(success=True, info=None)

