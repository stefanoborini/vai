from .VCoreApplication import VCoreApplication
from .VObject import VObject
from .VSignal import VSignal
from . import VTimerEvent
import time
import threading

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
            if self.stop.is_set():
                break
            self._callback()
            if self._single_shot:
                break

class VTimer(VObject):
    def __init__(self):
        super().__init__()
        self._interval = None
        self._single_shot = False
        self.timeout = VSignal(self)
        self._thread = None
        VCoreApplication.vApp.addTimer(self)

    def start(self):
        if self._thread is not None:
            return
        if self._interval is None:
            return
        self._thread = _TimerThread(self._interval, self._single_shot, self._timeout)
        self._thread.start()

    def _timeout(self):
        VCoreApplication.vApp.postEvent(self, VTimerEvent.VTimerEvent())

    def setSingleShot(self, single_shot):
        self._single_shot = single_shot

    def setInterval(self, interval):
        self._interval = interval

    def stop(self):
        if self._thread:
            self._thread.stop.set()
        self._thread = None

    def isRunning(self):
        return self._thread is not None

    def timerEvent(self, event):
        if isinstance(event, VTimerEvent.VTimerEvent):
            self.timeout.emit()

    @staticmethod
    def singleShot(timeout, callback):
        timer = VTimer()
        timer.setInterval(timeout)
        timer.setSingleShot(True)
        timer.timeout.connect(callback)
        timer.start()


