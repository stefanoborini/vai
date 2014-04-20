#!/usr/bin/env python3
from videtoolkit import core, gui
from vide import editor
from vide.TextDocument import TextDocument
import time
import sys

def usage():
    print("Usage: %s filename" % sys.argv[0])

try:
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    app = gui.VApplication(sys.argv)

    model = TextDocument(sys.argv[1])
    widget = editor.Editor(model)
    widget.show()
    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

