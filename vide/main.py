from videtoolkit import core, gui
from vide import editor
from vide.EditorModel import EditorModel
import time
import sys

try:
    app = gui.VApplication(sys.argv)

    model = EditorModel("setup.cfg")
    widget = editor.Editor(model)
    widget.show()
    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

