from .VApplication import VApplication
import logging

class VCursor(object):
    @staticmethod
    def setPos(pos):
        logging.info("Setting cursor pos to %s" % str(pos))
        VApplication.vApp.screen().setCursorPos(pos)

    @staticmethod
    def pos():
        return VApplication.vApp.screen().cursorPos()


