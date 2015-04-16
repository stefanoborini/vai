from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DedentCommand(BufferCommand):
    """
    Dedent the line at the current cursor position.
    """
    def __init__(self, buffer):
        super().__init__(buffer)

    def execute(self):
        cursor = self._cursor
        document = self._document

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()

        text = document.lineText(pos[0])
        if text[0:4] != '    ':
            return CommandResult(success=False, info=None)

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])

        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        # Naive implementation. Needs improvement.
        document.deleteChars((pos[0], 1), 4)
        if changed is None:
            line_meta.setData("modified", pos[0])

        document.documentMetaInfo("Modified").setData(True)

        cursor.toPos((pos[0], pos[1]-4))

        return CommandResult(success=True, info=None)

