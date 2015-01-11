"""
Module to handle fixtures in the test system.
It makes access to fixtures easy, convenient and practical.
"""
import inspect
import os
from vai.models import Buffer

# The place where global fixtures are looked up if local fixtures are not found
GLOBAL_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "global_fixtures")

def get(name, dirname="fixtures"):
    """
    Method to get a specific fixture path given its filename
    When invoked in a module, dir or method, the fixtures are searched
    in the current module directory, under the "fixtures" subdir.
    If that file does not exist, it will check the global fixtures.
    """
    fixture_local_dir = localDir(dirname)
    path = os.path.join(fixture_local_dir, name)
    if os.path.exists(path):
        return path
    
    return os.path.join(GLOBAL_FIXTURES_DIR, name)

def localDir(dirname="fixtures"):
    """
    Produces the local dir for the fixtures
    """
    frames = inspect.getouterframes(inspect.currentframe())
    for frame_info in frames:
        # Skips all routines inside this file, until you reach one that isn't
        if frame_info[0].f_globals['__file__'] != __file__:
            current_path = os.path.dirname(frame_info[1])
            return os.path.join(current_path, dirname)

    raise Exception("Should not reach")


def buffer(name):
    """
    Creates and returns a fully initialized buffer from a given fixture name
    """
    buf = Buffer()
    buf.document.open(get(name))
    return buf

def tempFile(name):
    """
    Returns a temporary file in a proper subdirectory
    Useful if the test needs a file that must be used and deleted afterwards
    """
    
    path = os.path.join(localDir("_test_"), name)

    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    return path

