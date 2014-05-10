import tempfile
import contextlib
import io
import logging
import subprocess
import os
import pyflakes.api

class LinterResult:
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

class PyFlakesLinter:
    def lint(self, document):
        reporter = Reporter()
        pyflakes.api.check(document.text(), document.filename(), reporter=reporter)
        return reporter.errors()

class PyLintLinter:
    def lint(self, document):
        env = os.environ
        env['LC_ALL']='en_US.UTF-8'
        env['LANG']='en_US.UTF-8'
        stdout = tempfile.NamedTemporaryFile(delete=False)
        stderr = tempfile.NamedTemporaryFile(delete=False)
        proc = subprocess.Popen(['pylint',
                           document.filename(),
                           "--msg-template='%s:{C}:{line}:{column}:{msg_id}:{obj}:{msg}'" % document.filename(),
                           '-r'
                           'n',
                           ],
                           stdout = stdout,
                           stderr = stderr,
                           env=env,
                           universal_newlines=True
                           )
        proc.wait()
        stdout.close()
        stderr.close()
        with contextlib.closing(open(stdout.name)) as f:
            lint_results = f.readlines()

        #with contextlib.closing(open(stderr.name)) as f:
        #    lint_results = f.readlines()

        result = []
        for line in lint_results:
            if line.startswith(document.filename()):
                info = line.split(':')
                info = LinterResult(filename=info[0],
                                    level=info[1],
                                    line=int(info[2]),
                                    column=int(info[3]),
                                    message=info[6]
                                   )
                result.append(info)
        return result

