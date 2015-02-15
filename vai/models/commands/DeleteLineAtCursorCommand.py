from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
import copy

class DeleteLineAtCursorCommand(BufferCommand):
    def execute(self):
        document = self._document
        if document.isEmpty():
            return CommandResult(success=False, info=None)

        cursor = self._cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()
        cursor.toPos(pos)

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_INSERT)
        old_line = copy.deepcopy(self.lastSavedMemento()[2])
        self._old_line_meta_info = {}

        if pos[0] == document.numLines():
            cursor.toLinePrev()
            cursor.toLineBeginning()

        if document.lineMetaInfo("Change").data(pos[0]) != "added":
            # Add markers above and below
            if document.hasLine(pos[0]-1):
                self._old_line_meta_info[-1] = document.lineMetaInfo("Change").data(pos[0]-1)
                document.lineMetaInfo("Change").setData("deletion_before", pos[0]-1)

            if document.hasLine(pos[0]+1):
                self._old_line_meta_info[1] = document.lineMetaInfo("Change").data(pos[0]+1)
                document.lineMetaInfo("Change").setData("deletion_after", pos[0]+1)

        # Delete the line
        document.deleteLine(pos[0])

        # Deleted line, now we check the length of what comes up from below.
        # and set the cursor at the end of the line, if needed
        if document.lineLength(cursor.line) < cursor.column:
            cursor.toPos((cursor.line, document.lineLength(cursor.line)))

        return CommandResult(success=True, info=old_line)

    def undo(self):
        super().undo()
        document = self._document
        cursor = self._cursor
        pos = cursor.pos

        if -1 in self._old_line_meta_info:
            document.lineMetaInfo("Change").setData(self._old_line_meta_info[-1], pos[0]-1)

        if 1 in self._old_line_meta_info:
            document.lineMetaInfo("Change").setData(self._old_line_meta_info[1], pos[0]+1)

