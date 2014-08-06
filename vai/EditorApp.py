from vaitk import gui
from .Editor import Editor
from . import models

class EditorApp(gui.VApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._editor_model = models.EditorModel()
        self._editor = Editor(self._editor_model)
        self._editor.show()

    def openFile(self, path):
        self._editor.controller.openFile(path)

