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


class PyLintLinter:
    def __init__(self):
        pass

    def lint(self, filename=None, original_filename=None, code=None):
        env = os.environ
        env['LC_ALL']='en_US.UTF-8'
        env['LANG']='en_US.UTF-8'
        stdout = tempfile.NamedTemporaryFile(delete=False)
        stderr = tempfile.NamedTemporaryFile(delete=False)
        raise Exception(filename)
        proc = subprocess.Popen(['pylint',
                           filename,
                           "--msg-template='%s:{C}:{line}:{column}:{msg_id}:{obj}:{msg}'" % original_filename,
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

        f=open("xxx", "w")
        f.write(str(lint_results))
        f.close()
        with contextlib.closing(open(stderr.name)) as f:
            lint_results = f.readlines()

        f=open("yyy", "w")
        f.write(str(lint_results))
        f.close()

        result = []
        for line in lint_results:
            if line.startswith(original_filename):
                info = line.split(':')
                info = LinterResult(info[0], info[1], int(info[2]), int(info[3]), info[4], info[5], info[6])
                result.append(info)
        return result


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
    def lint(self, filename=None, original_filename=None, code=None):
        reporter = Reporter()
        pyflakes.api.check(code, original_filename, reporter=reporter)
        return reporter.errors()
