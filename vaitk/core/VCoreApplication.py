from .VObject import VObject

class VCoreApplication(VObject):
    """
    Core application class. Only one instance is allowed to exist.
    """
    vApp = None

    def __init__(self, argv):
        super().__init__()
        self._timers = []

        if VCoreApplication.vApp is not None:
            raise Exception("Only one application is allowed")

        VCoreApplication.vApp = self

    def addTimer(self, timer):
        """
        Add a timer to the application.
        This routine should not be called manually.
        """
        self._timers.append(timer)

    def exit(self):
        """
        Exits the application.
        """
        VCoreApplication.vApp = None
