class CreateLineCommand(object):
    def __init__(self, model, line_number):
        self._model = model
        self._line_number = line_number

    def execute(self):
        self._model.createLine(self._line_number)

    def undo(self):
        self._model.deleteLine(self._line_number)


class DeleteLineCommand(object):
    def __init__(self, model, line_number):
        self._model = model
        self._line_number = line_number
        self._line_contents = None

    def execute(self):
        self._line_contents = self._model.getLine(self._line_number)
        self._model.deleteLine(self._line_number)

    def undo(self):
        if self._line_contents:
            self._model.insertLine(self._line_number, self._line_contents)
        self._line_contents = None
