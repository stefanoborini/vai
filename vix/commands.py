class CreateLineCommand(object):
    def __init__(self, model, line_number):
        self._model = model
        self._line_number = line_number

    def execute(self):
        self._model.newLine(self._line_number)
        self._model.updateLineMeta(self._line_number, {"change": "added"})

    def undo(self):
        self._model.deleteLine(self._line_number)
        self._model.updateLineMeta(self._line_number, {"change": None})

class DeleteLineAtCursorCommand(object):
    def __init__(self, buffer):
        self._buffer = buffer
        self._cursor_pos = None
        self._line_contents = None

    def execute(self):
        document = self._buffer.document()
        cursor = self._buffer.documentCursor()
        self._line_contents = cursor.lineText()
        self._cursor_pos = cursor.pos()
        cursor.deleteLine()

    def undo(self):
        if self._line_contents is None or self._cursor_pos is None:
            return

        document = self._buffer.document()
        document.insertLine(self._cursor_pos[0], self._line_contents)

        cursor = self._buffer.documentCursor()
        cursor.toPos(self._cursor_pos)
        self._line_contents = None
        self._cursor_pos = None

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
        if not "change" in line_meta:
            self._buffer.documentCursor().updateLineMeta({"change": "modified"})
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
        if document.lineMeta(cursor.pos()[0]-1).get("change") == None:
            document.updateLineMeta(cursor.pos()[0]-1, {"change": "modified"})
        document.updateLineMeta(cursor.pos()[0], {"change": "added"})

    def undo(self):
        pass
