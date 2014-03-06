from videtoolkit import core, gui
import time
import sys

try:
    app = gui.VApplication(sys.argv)

    tabwidget = gui.VTabWidget()
    label = gui.VLabel("Pretty Text", tabwidget)
    tabwidget.addTab(label, "foo")
    tabwidget.addTab(label, "bar")
    tabwidget.addTab(label, "baz")
    tabwidget.addTab(label, "baww")
    label.setColor(1)
    label.setGeometry(30,30,20,10)
    tabwidget.show()

    timer = core.VTimer(1)
    timer.timeout.connect(lambda: label.setText(str(time.time())))
    timer.start()
    app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

