class CommandHistory:
    def __init__(self):
        self._past = []
        self._future = []

    def add(self, command):
        self._past.append(command)
        self._future = []

    def prev(self):
        command = self._past.pop(-1)
        self._future.insert(0, command)
        return command

    def next(self):
        command = self._future.pop(0)
        self._past.append(command)
        return command

    def numUndoableCommands(self):
        return len(self._past)

    def numRedoableCommands(self):
        return len(self._future)
