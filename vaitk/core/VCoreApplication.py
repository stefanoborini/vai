from .VObject import VObject
from .VSignal import VSignal

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
        self.aboutToQuit = VSignal(self):

    def addTimer(self, timer):
        """
        Add a timer to the application.
        This routine should not be called manually.
        """
        self._timers.append(timer)

    def exit(self, retcode=0):
        """
        Exits the application.
        """
        VCoreApplication.vApp = None

    def sendEvent(self, receiver, event):
        """
        Directly send an event to a receiver.
        """
        receiver.event(event)

    def applicationName(self):
        raise NotImplementedError()

    def applicationVersion(self):
        raise NotImplementedError()

    def instance(self):
        raise NotImplementedError()

    def exec_(self):
        raise NotImplementedError()

    def processEvents(self, flags)
        raise NotImplementedError()

    def postEvent(self, receiver, event):
        raise NotImplementedError()

    def sendPostedEvents(self, receiver, event_type):
        raise NotImplementedError()

    def removePostedEvents(self, receiver, event_type):
        raise NotImplementedError()

    def hasPendingEvents(self):
        raise NotImplementedError()

    def notify(self, receiver, event):
        raise NotImplementedError()

    def applicationDirPath(self):
        raise NotImplementedError()

    def applicationFilePath(self):
        raise NotImplementedError()

    def startingUp(self):
        raise NotImplementedError()

    def closingDown(self):
        raise NotImplementedError()

    def setEventFilter(self, event_filter):
        raise NotImplementedError()



