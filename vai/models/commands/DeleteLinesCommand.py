from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
import copy

class DeleteLinesCommand(BufferCommand):
    """
    Deletes a bunch of lines.
    """
    def __init__(self, buffer, from_line, num_lines):
        super().__init__(buffer)
        self._from_line = from_line
        self._num_lines = num_lines
        self._fragment = None
        self._old_line_meta_info = {}

    def execute(self):
        document = self._document
        cursor = self._cursor
        if document.isEmpty():
            return CommandResult(success=False, info=None)

        if self.savedCursorPos() is None:
            self.saveCursorPos()

        pos = self.savedCursorPos()

        self._fragment = document.extractFragment(self._from_line, self._num_lines)

        if pos[0] == document.numLines():
            cursor.toLinePrev()
            cursor.toLineBeginning()

        if document.lineMetaInfo("Change").data(pos[0]) != "added":
            # Add markers above and below
            if document.hasLine(pos[0]-1):
                self._old_line_meta_info[-1] = document.lineMetaInfo("Change").data(pos[0]-1)
                document.lineMetaInfo("Change").setData("deletion_before", pos[0]-1)

            if document.hasLine(self._from_line+self._num_lines+1):
                self._old_line_meta_info[1] = document.lineMetaInfo("Change").data(pos[0]+1)
                document.lineMetaInfo("Change").setData("deletion_after", pos[0]+1)

        document.deleteLines(self._from_line, self._num_lines)

        # Deleted line, now we check the length of what comes up from below.
        # and set the cursor at the end of the line, if needed
        if document.lineLength(cursor.line) < cursor.column:
            cursor.toPos((cursor.line, document.lineLength(cursor.line)))
        else:
            cursor.toPos(pos)

        return CommandResult(success=True, info=self._fragment)

    def undo(self):
        return
#        document = self._document
#        cursor = self._cursor
#        pos = cursor.pos
#
#        if -1 in self._old_line_meta_info:
#            document.lineMetaInfo("Change").setData(self._old_line_meta_info[-1], pos[0]-1)
#
#        if 1 in self._old_line_meta_info:
#            document.lineMetaInfo("Change").setData(self._old_line_meta_info[1], pos[0]+1)

