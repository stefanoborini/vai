from .VApplication import VApplication
import logging

class VCursor:
    @staticmethod
    def setPos(pos):
        VApplication.vApp.screen().setCursorPos(pos)

    @staticmethod
    def pos():
        return VApplication.vApp.screen().cursorPos()


