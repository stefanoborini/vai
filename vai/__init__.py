#!/usr/bin/env python3
__version__ = "1.4"

def _workaroundNCurses():
    """
    This routine works around the ncurses library.
    It must be called before everything else, so that ncurses is not
    loaded.
    The problem is that python installs and links by default to 
    ncurses, instead of ncursesw. The result is that unicode stuff
    gets corrupted. We work around the problem as explained in the comments
    """

    # First we check, without loading it, if the current _curses module is linked to 
    # ncursesw or ncurses.
    # If the first, we are done.

    import imp
    import subprocess
    import platform
    import os

    if platform.system() != "Linux":
        return

    local_lib_path = os.path.expanduser("~/.local/lib/vai/")
    # We already deployed the workaround, or the ncursesw is already present and
    # we skip the check.
    if os.path.exists(os.path.join(local_lib_path, "libncurses.so")) \
       or os.path.exists(os.path.join(local_lib_path, "ncursesw_ok")):
        return

    # We get the module without importing it and run ldd on it, getting the 
    # relevant library
    module_file = imp.find_module("_curses")[1]
    
    out = subprocess.getoutput("ldd %s" % module_file)

    lines = out.splitlines()
    library_name = ""
    for line in lines:
        if "ncurses" not in line:
            continue
        library_name = [x.strip() for x in line.split("=>")][0]
    
    # The _curses module is linked against ncursesw. This will work for us.
    # so we mark it ok and be done with it
    if "ncursesw" in library_name:
        os.makedirs(local_lib_path, exist_ok=True)
        f=open(os.path.join(local_lib_path, "ncursesw_ok"), 'w')
        f.close()
        return

    # Otherwise, we need to see if the system has ncursesw somewhere.
    # Apparently, we can trick python in loading ncursesw as ncurses and it will
    # work.
    
    if platform.processor() == "x86_64":
        ncurses_path = "/lib/x86_64-linux-gnu/libncursesw.so.5.9"
    else:
        ncurses_path = "/lib/i386-linux-gnu/libncursesw.so.5.9"
    
    # If the library does not exist on the system, we give up and start rendering in ascii
    if not os.path.exists(ncurses_path):
        from . import models
        models.Configuration.flags["has_wide_ncurses"] = False
        return

    # If present, copy the libraries to the local lib path,
    # export LD_LIBRARY_PATH to the .local/lib/vai and make it go
    import shutil
    os.makedirs(local_lib_path, exist_ok=True)
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so.5.9"))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so.5"))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, "libncurses.so"))

    if "LD_LIBRARY_PATH" in os.environ:
        ld_lib_path = local_lib_path+":"+os.environ["LD_LIBRARY_PATH"]
    else:
        ld_lib_path = local_lib_path
    
    os.environ["LD_LIBRARY_PATH"] = ld_lib_path
    
    # Finally, trigger the import of curses, so that the ncurses library gets loaded
    import _curses 





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

