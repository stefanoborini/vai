from vaitk import gui
from .Editor import Editor
from . import models
import os


class EditorApp(gui.VApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config_file = os.path.expanduser("~/.vairc")
        if os.path.exists(config_file):
            try:
                models.Configuration.initFromFile(config_file)
            except:
                pass
        # We keep them at the App level because the app will be responsible
        # for coordinating the async system in the future.
        self._global_model = models.GlobalState()
        self._buffer_list = models.BufferList()

        self._editor = Editor(self._global_model, self._buffer_list)

        self._editor.show()

    def openFile(self, path):
        self._editor.controller.openFile(path)

