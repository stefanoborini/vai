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
        return CommandResult(True, None)

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
        return CommandResult(True, None)

    def undo(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()
        document.deleteLine(self._pos[0]+1)
        cursor.toPos(self._pos)

class DeleteLineAtCursorCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None

    def execute(self):
        document = self._buffer.document()
        if document.isEmpty():
            return CommandResult(success=False, info=None)

        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()

        if cursor.pos()[0] == self._buffer.document().numLines():
            # Last line. Move the cursor up
            if not cursor.toLinePrev():
                cursor.toLineBeginning()

        self._line_memento = document.lineMemento(self._pos[0])
        document.deleteLine(self._pos[0])
        return CommandResult(success=True, info=None)

    def undo(self):
        document = self._buffer.document()
        document.insertFromMemento(self._pos[0], self._line_memento)
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)

class DeleteSingleCharCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        if cursor.pos()[1] == 1:
            return CommandResult(success=False, info=None)

        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars( (self._pos[0], self._pos[1]-1), 1)
        cursor.toCharPrev()
        return CommandResult(success=True, info=deleted)

    def undo(self):
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        cursor.replaceFromMemento(self._line_memento)

class DeleteSingleCharAfterCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()

        if cursor.pos()[1] == document.lineLength(cursor.pos()[0]):
            return CommandResult(success=False, info=None)

        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars(self._pos, 1)
        return CommandResult(success=True, info=deleted)

    def undo(self):
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        cursor.replaceFromMemento(self._line_memento)

class BreakLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None
        self._sub_command = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()
        pos = cursor.pos()

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
            return result


        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        document.breakLine(self._pos)
        cursor.toPos((self._pos[0]+1, 1))
        line_meta = document.lineMeta(self._pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        document.updateLineMeta(self._pos[0]+1, {LineMeta.Change: "added"})
        return CommandResult(success=True, info=None)

    def undo(self):
        if self._sub_command is not None:
            self._sub_command.undo()
            return

        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        document = self._buffer.document()
        document.replaceFromMemento(self._pos[0], self._line_memento)
        document.deleteLine(self._pos[0]+1)

class JoinWithNextLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_1_memento = None
        self._line_2_memento = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()
        document = self._buffer.document()
        line_meta = document.lineMeta(self._pos[0])

        document.joinWithNextLine(self._pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        return CommandResult(success=True, info=None)

    def undo(self):
        raise NotImplementedError()

class InsertStringCommand(object):
    def __init__(self, buffer, string):
        self._buffer = buffer
        self._string = string
        self._pos = None
        self._meta_modified = False

    def execute(self):
        raise NotImplementedError()
        cursor = self._buffer.documentCursor()
        self._pos = cursor.pos()
        line_meta = cursor.lineMeta()
        if not LineMeta.Change in line_meta:
            self._buffer.documentCursor().updateLineMeta({LineMeta.Change: "modified"})
            self._meta_modified = True

        for c in self._string:
            self._buffer.documentCursor().insertSingleChar(c)

    def undo(self):
        raise NotImplementedError()
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)
        self._buffer.document().deleteChars(self._pos, len(self._string))
        if self._meta_modified:
            self._buffer.document().deleteLineMeta(self._pos[0], LineMeta.Change)
