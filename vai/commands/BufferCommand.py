class BufferCommand(object):
    MEMENTO_INSERT, MEMENTO_REPLACE = list(range(2))
    def __init__(self, buffer):
        self._buffer = buffer
        self._document = buffer.document
        self._cursor = buffer.cursor

        self._line_memento_data = []
        self._sub_command = None
        self._saved_cursor_pos = None

    def saveCursorPos(self):
        self._saved_cursor_pos = self._cursor.pos

    def restoreCursorPos(self):
        self._cursor.toPos(self._saved_cursor_pos)
        self._saved_cursor_pos = None

    def savedCursorPos(self):
        return self._saved_cursor_pos

    def saveLineMemento(self, line_number, restore_strategy):
        self._line_memento_data.append( (line_number, restore_strategy, self._document.lineMemento(line_number)) )

    def restoreLineMemento(self):
        line_number, restore_strategy, memento = self._line_memento_data.pop()

        if restore_strategy == BufferCommand.MEMENTO_INSERT:
            self._document.insertFromMemento(line_number, memento)
        elif restore_strategy == BufferCommand.MEMENTO_REPLACE:
            self._document.replaceFromMemento(line_number, memento)
        else:
            raise Exception("Unknown restore mode for memento")

    def lastSavedMemento(self):
        return self._line_memento_data[-1]

    def undo(self):
        if self._sub_command is not None:
            self._sub_command.undo()
            return

        for i in range(len(self._line_memento_data)):
            self.restoreLineMemento()

        if self._saved_cursor_pos is not None:
            self.restoreCursorPos()
