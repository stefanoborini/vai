#!/usr/bin/env python3
__version__ = "1.5"

def _workaroundNCurses():
    """
    This routine works around the ncurses library.
    It must be called before everything else, so that ncurses is not
    loaded.
    The problem is that python installs and links by default to
    ncurses, instead of ncursesw (wide characters). The result is that unicode
    stuff gets corrupted. We work around the problem as explained in the
    comments. The two libraries appear to be compatible, so if I just "mimic"
    the library name, it behaves correctly.

    Unfortunately, we _must_ rely on a shell script to export LD_LIBRARY_PATH
    for us. I found out that dlopen does not honor LD_LIBRARY_PATH if changed
    after startup.

    The end result is that I always copy the ncurses wide character when not
    in a local lib source.
    """

    import platform
    import os
    import sys

    if platform.system() != "Linux":
        return

    local_lib_path = os.path.expanduser("~/.local/lib/vai/")

    # We already deployed the workaround
    if os.path.exists(os.path.join(local_lib_path, "libncurses.so")):
        return

    if platform.processor() == "x86_64":
        ncurses_path = "/lib/x86_64-linux-gnu/libncursesw.so.5.9"
    else:
        ncurses_path = "/lib/i386-linux-gnu/libncursesw.so.5.9"

    # If the library does not exist on the system, we give up and start rendering in ascii
    if not os.path.exists(ncurses_path):
        from . import models
        models.Configuration.flags["has_wide_ncurses"] = False
        return

    # If present, copy the libraries to the local lib path, with a different name, to trick
    # python in using them
    import shutil
    os.makedirs(local_lib_path, exist_ok=True)

    # Just three copies, I'm a lazy bum.
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so.5.9"))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so.5"))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so"))

    # Signals the shell script that the thing has been deployed and need to restart vai
    sys.exit(42)

_workaroundNCurses()

from vaitk import core, gui
from . import EditorApp
from . import models
from . import BugReport
import os
import sys
import io
import argparse
import locale
import logging
logging.basicConfig(filename="foo", level=logging.DEBUG)

def main():
    # Sets the locale to the default (user specified) locale, as suggested by ncurses docs
    locale.setlocale(locale.LC_ALL, "")

    parser = argparse.ArgumentParser(description="A Vim-like editor, with big dreams.")
    parser.add_argument("filename", nargs="?", help="The filename to open")
    parser.add_argument("--dump-default-config",
                        help="Dump the default configuration to the config file. Useful to reset a broken configuration.",
                        action="store_true")
    parser.add_argument("--profile", help="Enable profiling at the end of the run.", action="store_true")
    parser.add_argument("--pdb", help="Enable debugging with pdb in case of crash.", action="store_true")
    parser.add_argument("--noreport", help="Skip request for bug reporting.", action="store_true")
    parser.add_argument("--version", '-v', help="Print the version number.", action="version",
                                           version='vai {0}'.format(__version__))
    args = parser.parse_args()

    app = None
    try:

        if args.dump_default_config:
            filename = models.Configuration.filename()
            if os.path.exists(filename):
                print("Refusing to overwrite existing config file %s. Delete the file manually and try again." % filename)
                sys.exit(1)

            models.Configuration.save()
            print("Dumped default configuration in %s" % filename)
            sys.exit(0)
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

        saved_files = []
        if app is not None:
            saved_files = app.dumpBuffers()

            app.resetScreen()

        with contextlib.closing(open("vai_crashreport.out", "w")) as f:
            f.write(traceback.format_exc())

        if args.pdb:
            import pdb
            pdb.post_mortem()

        if not args.noreport:
            BugReport.report(saved_files)

    return 0

