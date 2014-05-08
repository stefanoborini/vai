#!/usr/bin/env python3
__version__ = "1.0"

from vixtk import core, gui
from . import Editor
import sys
import pdb
import io
import pstats
import argparse
import cProfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="The filename to open")
    args = parser.parse_args()

    try:
        app = gui.VApplication(sys.argv)

        e = Editor.Editor()
        if args.filename:
            e.openFile(args.filename)

        e.show()
        pr = cProfile.Profile()
        pr.enable()
        app.exec_()
        pr.disable()
        s = io.StringIO()
        sortby = 'tottime'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
    except Exception as e:
        import traceback
        open("crashreport.out", "w").write(traceback.format_exc())
        pdb.post_mortem()

    return 0

