from videtoolkit import gui
import time
import sys

try:
    app = gui.VApplication(sys.argv)
    screen = app.screen()
    for r in xrange(0, 26):
        for g in xrange(0, 26):
            for b in xrange(0, 26):
                screen.write(g,b,' ', gui.VColor((0,0,0)), gui.VColor((r*10,g*10,b*10)))
                screen.refresh()

        screen.write(26,26,"red = %d" % (r*10),gui.VColor((255,255,255)), gui.VColor((0,0,0)))
        screen.refresh()
        time.sleep(1)
    #app.exec_()
except Exception as e:
    import traceback
    open("crashreport.out", "w").write(traceback.format_exc())

