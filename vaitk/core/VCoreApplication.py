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

    @staticmethod
    def instance():
        return VCoreApplication.vApp

    def addTimer(self, timer):
        """
        Add a timer to the application.
        This routine should not be called manually.
        """
        self._timers.append(timer)

    @staticmethod
    def exit():
        """
        Exits the application.
        """
        VCoreApplication.vApp = None

    @staticmethod
    def sendEvent(receiver, event):
        """
        Directly send an event to a receiver.
        """
        event.setSpontaneous(False)
        return receiver.event(event)

    @staticmethod
    def sendSpontaneousEvent(receiver, event):
        event.setSpontaneous(True)
        return receiver.event(event)

    @staticmethod
    def postEvent(receiver, event, priority = None):
        pass


    @staticmethod
    def processEvents():
        pass

    def event(self, event):
        pass

    def compressEvent(event, receiver, post_event_list):
        pass

