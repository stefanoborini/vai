class VSignal(object):
    def __init__(self, sender):
        self._sender = sender
        self._slots = []
        self._enabled = True

    def connect(self, target):
        if isinstance(target, VSignal):
            slot = target.emit
        else:
            slot = target
        self._slots.append(slot)

    def disconnect(self, target):
        self._slots.remove(target)

    def emit(self, *args, **kwargs):
        if not self._enabled:
            return

        for slot in self._slots:
            slot(*args, **kwargs)

    def setEnabled(self, enabled):
        self._enabled = enabled
