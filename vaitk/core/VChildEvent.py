from .VEvent import VEvent

class VChildEvent(VEvent):
    def __init__(self, event_type, child):
        super().__init__(event_type)
        self._child = child

