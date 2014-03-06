import atexit
import time

class VSignal(object):
    def __init__(self, sender):
        self._sender = sender
        self._slots = []

    def connect(self, slot):
        self._slots.append(slot)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)

class VObject(object):
    def __init__(self, parent = None):
        self._parent = parent
        self._children = []
        if self._parent is not None:
            parent.addChild(self)

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def addChild(self, child):
        self._children.append(child)

    @staticmethod
    def connect(signal, slot):
        signal.connect(slot)

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
        pass

class VTimer(VObject):
    def __init__(self, timeout):
        self._start_time = None
        self._timeout = timeout
        self.timeout = VSignal(self)
        VCoreApplication.vApp.addTimer(self)

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._start_time = None

    def heartbeat(self):
        if self._start_time is None:
            return

        if time.time() - self._start_time > self._timeout:
            self._start_time = time.time()
            self.timeout.emit()

