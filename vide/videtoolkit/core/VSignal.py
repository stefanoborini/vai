class VSignal(object):
    def __init__(self, sender):
        self._sender = sender
        self._slots = []

    def connect(self, target):
        if isinstance(target, VSignal):
            slot = target.emit
        else:
            slot = target
        self._slots.append(slot)

    def disconnect(self, target):
        self._slots.remove(target)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)

