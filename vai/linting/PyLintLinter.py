'''
import tempfile
import contextlib
import io
import logging
import subprocess
import os
from ..AsyncDocumentProcessor import AsyncDocumentProcessor

class PyLintLinter(AsyncDocumentProcessor):
    """
    Slow, but very accurate  Linter. We need async processing for this one to happen.
    For now it is unused.
    """

    def __init__(self, document, editor):
        super().__init__(document)
        self._editor = editor

    def run(self):
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
                                    message=info[6].strip()
                                   )
                result.append(info)
        return result

'''
