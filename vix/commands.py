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
        self._line_contents = cursor.currentLine()
        self._cursor_pos = cursor.pos()
        cursor.deleteLine()

    def undo(self):
        if self._line_contents is None or self._cursor_pos is None:
            return

        document = self._buffer.document()
        document.insertLine(self._cursor_pos[0], self._line_contents)

        cursor = self._buffer.documentCursor()
        cursor.moveTo(self._cursor_pos)
        self._line_contents = None
        self._cursor_pos = None

