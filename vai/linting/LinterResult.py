class LinterResult:
    """
    "Namedtuple" class to hold information about the linter results
    """
    class Level:
        INFO = 0
        WARNING = 1
        ERROR = 2

    def __init__(self, filename, level, line, column, message):
        self.filename = filename
        self.level = level
        self.line = line
        self.column = column
        self.message = message


