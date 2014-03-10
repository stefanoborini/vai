from videtoolkit import core, gui
from videtoolkit import editor
import time
import sys

try:
    app = gui.VApplication(sys.argv)

    model = editor.EditorModel("hello")
    widget = editor.Editor(model)

    #tabwidget = gui.VTabWidget()
    #label = gui.VLabel("Pretty Text", tabwidget)
    #tabwidget.addTab(label, "foo")
    #tabwidget.addTab(label, "bar")
    #tabwidget.addTab(label, "baz")
    #tabwidget.addTab(label, "baww")
    #label.setColor(1)
    #label.setGeometry(30,30,20,10)
    #tabwidget.show()

    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

