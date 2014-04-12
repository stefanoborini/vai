import tempfile
import StringIO
import logging
import subprocess
import os

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
                           "--msg-template='%s:{line}:{column}:{msg_id}:{obj}:{msg}" % document.filename(),
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
                info = (info[0], int(info[1]), int(info[2]), info[3], info[4], info[5])
                result.append(info)

        return result
