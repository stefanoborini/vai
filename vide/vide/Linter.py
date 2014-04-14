import tempfile
import io
import logging
import subprocess
import os
from pylint.lint import Run
from pylint.reporters.text import ParseableTextReporter

class Linter(object):
    def __init__(self):
        pass

    def lint(self, document):
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        document.saveAs(tmpfile.name)
        env = os.environ
        env['LC_ALL']='en_US.UTF-8'
        env['LANG']='en_US.UTF-8'
        proc = subprocess.Popen(['/Users/sbo/.local/bin/pylint',
                           tmpfile.name,
                           "--msg-template='%s:{C}:{line}:{column}:{msg_id}:{obj}:{msg}'" % document.filename(),
                           '-r'
                           'n',
                           ],
                           stdout = subprocess.PIPE,
                           stderr = subprocess.STDOUT,
                           env=env
                           )
        proc.wait()
        lint_results = proc.stdout.read().splitlines()

        result = []
        for line in lint_results:
            if line.startswith(document.filename()):
                info = line.split(':')
                info = (info[0], info[1], int(info[2]), int(info[3]), info[4], info[5], info[6])
                result.append(info)
        return result
