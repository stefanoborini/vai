import inspect
import os

def get(name):
    frame_info = inspect.getouterframes(inspect.currentframe())[1]
    return os.path.join(os.path.dirname(frame_info[1]), "fixtures", name)

