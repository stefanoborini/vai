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
        cursor.toPos( (self._pos[0], 1) )
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

        if cursor.pos()[0] == document.numLines():
            # Last line. Move the cursor up
            if not cursor.toLinePrev():
                # It's also the first line. Go at the beginning
                cursor.toLineBeginning()

        self._line_memento = document.lineMemento(self._pos[0])
        document.deleteLine(self._pos[0])

        # Deleted line, now we check the length of what comes up from below.
        # and set the cursor at the end of the line, if needed
        if document.lineLength(cursor.pos()[0]) < cursor.pos()[1]:
            cursor.toPos( (cursor.pos()[0], document.lineLength(cursor.pos()[0])))

        return CommandResult(success=True, info=self._line_memento)

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
        self._sub_command = None

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()

        pos = cursor.pos()
        if pos == (1,1):
            return CommandResult(success=False, info=None)

        if pos[1] == 1:
            cursor.toPos( (pos[0]-1, document.lineLength(pos[0]-1)) )
            command = JoinWithNextLineCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
                return CommandResult(True, '\n')
            else:
                return CommandResult(False, None)

        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars( (self._pos[0], self._pos[1]-1), 1)
        cursor.toCharPrev()
        return CommandResult(success=True, info=deleted)

    def undo(self):
        if self._sub_command is not None:
            self._sub_command.undo()
            return

        cursor = self._buffer.documentCursor()
        document = self._buffer.document()
        cursor.toPos(self._pos)
        document.replaceFromMemento(self._pos[0], self._line_memento)

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
        document = self._buffer.document()
        cursor.toPos(self._pos)
        document.replaceFromMemento(self._pos[0], self._line_memento)

class BreakLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None
        self._sub_command = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()

        self._pos = cursor.pos()
        if self._pos[1] == document.lineLength(self._pos[0]):
            command = NewLineAfterCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
            return result

        if self._pos[1] == 1:
            command = NewLineCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
            cursor.toPos((self._pos[0]+1, 1))
            return result

        self._line_memento = document.lineMemento(self._pos[0])

        document.breakLine(self._pos)
        cursor.toPos((self._pos[0]+1, 1))
        line_meta = document.lineMeta(self._pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        document.updateLineMeta(self._pos[0]+1, {LineMeta.Change: "added"})
        return CommandResult(success=True, info=None)

    def undo(self):
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)

        if self._sub_command is not None:
            self._sub_command.undo()
            return

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
        document = self._buffer.document()
        pos = cursor.pos()
        if pos[0] == document.numLines():
            return CommandResult(success=False, info=None)

        self._pos = pos
        document = self._buffer.document()
        line_meta = document.lineMeta(self._pos[0])

        self._line_1_memento = document.lineMemento(self._pos[0])
        self._line_2_memento = document.lineMemento(self._pos[0]+1)

        document.joinWithNextLine(self._pos[0])
        if line_meta.get(LineMeta.Change) == None:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        return CommandResult(success=True, info=None)

    def undo(self):
        document = self._buffer.document()
        document.insertFromMemento(self._pos[0]+1, self._line_2_memento)
        document.replaceFromMemento(self._pos[0], self._line_1_memento)
        cursor = self._buffer.documentCursor()
        cursor.toPos(self._pos)

class InsertStringCommand(object):
    def __init__(self, buffer, string):
        self._buffer = buffer
        self._string = string
        self._pos = None
        self._line_memento = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()
        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            self._buffer.documentCursor().updateLineMeta({LineMeta.Change: "modified"})

        document.insertChars(self._pos, self._string)
        cursor.toPos( (self._pos[0], self._pos[1]+len(self._string)) )
        return CommandResult(success=False, info=None)

    def undo(self):
        self._buffer.documentCursor().toPos(self._pos)
        self._buffer.document().replaceFromMemento(self._pos[0], self._line_memento)

class DeleteToEndOfLineCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._pos = None
        self._line_memento = None

    def execute(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()

        self._pos = cursor.pos()
        self._line_memento = document.lineMemento(self._pos[0])

        line_meta = document.lineMeta(self._pos[0])
        if not LineMeta.Change in line_meta:
            document.updateLineMeta(self._pos[0], {LineMeta.Change: "modified"})

        deleted = document.deleteChars(self._pos, document.lineLength(self._pos[0])-self._pos[1])
        cursor.toCharPrev()
        return CommandResult(success=True, info=deleted)

    def undo(self):
        cursor = self._buffer.documentCursor()
        document = self._buffer.document()
        cursor.toPos(self._pos)
        document.replaceFromMemento(self._pos[0], self._line_memento)
