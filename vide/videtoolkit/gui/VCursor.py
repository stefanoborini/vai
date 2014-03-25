from .VApplication import VApplication

class VCursor(object):
    @staticmethod
    def setPos(x,y):
        VApplication.vApp.screen().setCursorPos(x,y)

    def pos(x,y):
        return VApplication.vApp.screen().cursorPos(x,y)


