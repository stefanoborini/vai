import atexit
import time
import threading
from .gui import events

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

class _TimerThread(threading.Thread):
    def __init__(self, timeout, single_shot, callback):
        super(_TimerThread, self).__init__()
        self.daemon = True
        self._timeout = timeout
        self._single_shot = single_shot
        self._callback = callback
        self.stop = threading.Event()
    def run(self):
        while True:
            time.sleep(self._timeout/1000.0)
            self._callback()
            if self._single_shot or self.stop.is_set():
                break


class VTimer(VObject):
    def __init__(self):
        self._interval = None
        self._single_shot = False
        self.timeout = VSignal(self)
        self._thread = None

    def start(self, timeout):
        if self._thread is not None:
            return

        self._thread = _TimerThread(timeout, self._single_shot, self._timeout)
        self._thread.start()

    def _timeout(self):
        VCoreApplication.vApp.postEvent(self, events.VTimerEvent())

    def setSingleShot(self, single_shot):
        self._single_shot = single_shot

    def stop(self):
        if self._thread:
            self._thread.stop.set()
        self._thread = None

    def timerEvent(self, event):
        if isinstance(event, events.VTimerEvent):
            self.timeout.emit()

