#!/usr/bin/env python3
__version__ = "1.2a"

from vaitk import core, gui
from . import EditorApp
from . import BugReport
import sys
import io
import argparse

def main():
    parser = argparse.ArgumentParser(description="A Vim-like editor, with big dreams.")
    parser.add_argument("filename", nargs="?", help="The filename to open")
    parser.add_argument("--profile", help="Enable profiling at the end of the run.", action="store_true")
    parser.add_argument("--pdb", help="Enable debugging with pdb in case of crash.", action="store_true")
    parser.add_argument("--noreport", help="Skip request for bug reporting.", action="store_true")
    parser.add_argument("--version", '-v', help="Print the version number.", action="version",
                                           version='vai {0}'.format(__version__))
    args = parser.parse_args()

    try:

        app = EditorApp.EditorApp(sys.argv)
        if args.filename:
            app.openFile(args.filename)

        if args.profile:
            import cProfile
            pr = cProfile.Profile()
            pr.enable()

        app.exec_()

        if args.profile:
            pr.disable()
            s = io.StringIO()
            sortby = 'tottime'
            import pstats
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print(s.getvalue())

        app.resetScreen()

    except Exception as e:
        import traceback
        import contextlib

        app.resetScreen()

        with contextlib.closing(open("vai_crashreport.out", "w")) as f:
            f.write(traceback.format_exc())

        if args.pdb:
            import pdb
            pdb.post_mortem()

        if not args.noreport:
            BugReport.report()

    return 0

