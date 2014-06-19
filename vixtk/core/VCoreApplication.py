import atexit
from .VObject import VObject
import logging

class VCoreApplication(VObject):
    """
    Core application class. Only one instance is allowed to exist.
    """

    vApp = None

    def __init__(self, argv):
        self.logger.debug("__init__")
        super(VCoreApplication, self).__init__()
        self._timers = []

        if VCoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VCoreApplication.vApp = self

    def addTimer(self, timer):
        """
        Add a timer to the application.
        This routine should not be called manually.
        """
        self.logger.debug("addTimer")
        self._timers.append(timer)

    def exit(self):
        """
        Exits the application.
        """
        self.logger.debug("exit")
        VCoreApplication.vApp = None

