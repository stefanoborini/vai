import atexit
from .VObject import VObject

class VCoreApplication(VObject):
    vApp = None

    def __init__(self, argv):
        super(VCoreApplication, self).__init__()
        self._timers = []

        if VCoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VCoreApplication.vApp = self
        atexit.register(self.exit)

    def addTimer(self, timer):
        self._timers.append(timer)

    def exit(self):
        VCoreApplication.vApp = None

