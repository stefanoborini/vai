__version__ = "1.0"
#!/usr/bin/env python3
from vixtk import core, gui
from . import editor
import sys
import pdb

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="The filename to open")
    args = parser.parse_args()

    try:
        app = gui.VApplication(sys.argv)

        e = editor.Editor()
        if args.filename:
            e.openFile(args.filename)

        e.show()
        app.exec_()
    except Exception as e:
        import traceback
        open("crashreport.out", "w").write(traceback.format_exc())
        pdb.post_mortem()

    return 0

