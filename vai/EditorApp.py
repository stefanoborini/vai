from vaitk import gui
from . import Editor

class EditorApp(gui.VApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._editor_model = EditorModel()
        self._editor = Editor(self._editor_model)
        self._editor.show()

    def openFile(self, path):
        self._editor.controller.openFile(path)

