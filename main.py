#!/usr/bin/env python3
from vixtk import core, gui
from vix import editor
import sys
import pdb

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", help="The filename to open")
args = parser.parse_args()

try:
    app = gui.VApplication(sys.argv)

    editor = editor.Editor()
    if args.filename:
        editor.openFile(args.filename)

    editor.show()
    app.exec_()
except Exception as e:
    #import traceback
    #open("crashreport.out", "w").write(traceback.format_exc())
    pdb.post_mortem()

