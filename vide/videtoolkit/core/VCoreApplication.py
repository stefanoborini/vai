import atexit
from .VObject import VObject
import logging

class VCoreApplication(VObject):
    vApp = None
    debug = logging.DEBUG
    def __init__(self, argv):
        self.logger.debug("__init__")
        super(VCoreApplication, self).__init__()
        self._timers = []

        if VCoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VCoreApplication.vApp = self
        atexit.register(self.exit)

    def addTimer(self, timer):
        self.logger.debug("addTimer")
        self._timers.append(timer)

    def exit(self):
        self.logger.debug("exit")
        VCoreApplication.vApp = None

