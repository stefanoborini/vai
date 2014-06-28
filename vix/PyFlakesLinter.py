from .LinterResult import LinterResult
import pyflakes.api

class PyFlakesLinter:
    def __init__(self, document):
        self._document = document

    def runOnce(self):
        reporter = Reporter()
        pyflakes.api.check(self._document.text(),
                           self._document.filename(),
                           reporter=reporter)
        return reporter.errors()

class Reporter:
    def __init__(self):
        self._errors = []

    def unexpectedError(self, *args):
        pass

    def syntaxError(self, filename, msg, lineno, offset, text):
        self._errors.append( LinterResult(filename = filename,
                                          level = LinterResult.Level.ERROR,
                                          line = lineno,
                                          column = offset,
                                          message = msg)
                            )

    def flake(self, msg):
        self._errors.append( LinterResult(filename = msg.filename,
                                          level = LinterResult.Level.WARNING,
                                          line = msg.lineno,
                                          column = msg.col,
                                          message = str(msg))
                            )

    def errors(self):
        return self._errors

