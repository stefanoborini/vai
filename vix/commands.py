import collections
from .models.TextDocument import LineMeta

CommandResult = collections.namedtuple('CommandResult', ['success', 'info'])

class NewLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        self._pos = cursor.pos()
        document.newLine(self._pos[0])
        document.updateLineMeta(self._pos[0], {LineMeta.Change: "added"})

    def undo(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()
        document.deleteLine(self._pos[0])
        cursor.toPos(self._pos)

class NewLineAfterCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        self._pos = cursor.pos()
        document.newLineAfter(self._pos[0])
        document.updateLineMeta(self._pos[0]+1, {LineMeta.Change: "added"})
        cursor.toLineNext()

    def undo(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()
        document.deleteLine(self._pos[0]+1)
        cursor.toPos(self._pos)

class DeleteLineAtCursorCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_text = None
        self._line_meta = None
        self._char_meta = None

    def execute(self):
        document = self._buffer.document()
        if document.isEmpty():
            return CommandResult(success=False, info=None)

        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()

        self._line_text = document.lineText(self._pos[0])
        self._line_meta = document.lineMeta(self._pos[0])
        self._char_meta = document.charMeta( (self._pos[0], 1))
        document.deleteLine(self._pos[0])
        return CommandResult(success=True, info=None)

    def undo(self):
        if self._pos is None:
            return

        document = self._buffer.document()
        document.insertLine(self._pos[0], self._line_text)
        document.updateLineMeta(self._pos[0], self._line_meta)
        document.updateCharMeta( (self._pos[0], 1), self._char_meta)

        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        self._pos = None

class DeleteSingleCharCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._deleted = None
        self._meta_modified = False

    def execute(self):
        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()
        line_meta = cursor.lineMeta()
        if not LineMeta.Change in line_meta:
            self._buffer.documentCursor().updateLineMeta({LineMeta.Change: "modified"})
            self._meta_modified = True

        self._deleted = cursor.deleteSingleChar()

    def undo(self):
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        cursor.insertSingleChar(self._deleted[0])

class BreakLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()
        cursor.breakLine()
        document = self._buffer.document()
        if document.lineMeta(cursor.pos()[0]-1).get(LineMeta.Change) == None:
            document.updateLineMeta(cursor.pos()[0]-1, {LineMeta.Change: "modified"})
        document.updateLineMeta(cursor.pos()[0], {LineMeta.Change: "added"})

    def undo(self):
        pass

class InsertStringCommand(object):
    def __init__(self, buffer, string):
        self._buffer = buffer
        self._string = string
        self._pos = None
        self._meta_modified = False

    def execute(self):
        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()
        line_meta = cursor.lineMeta()
        if not LineMeta.Change in line_meta:
            self._buffer.documentCursor().updateLineMeta({LineMeta.Change: "modified"})
            self._meta_modified = True

        for c in self._string:
            self._buffer.documentCursor().insertSingleChar(c)

    def undo(self):
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        self._buffer.document().deleteChars(self._pos, len(self._string))
        if self._meta_modified:
            self._buffer.document().deleteLineMeta(self._pos[0], LineMeta.Change)
