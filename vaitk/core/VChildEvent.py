from .VEvent import VEvent

class VChildEvent(VEvent):
    def __init__(self, event_type, child):
        if event_type not in [VEvent.EventType.ChildAdded,
                              VEvent.EventType.ChildPolished,
                              VEvent.EventType.ChildRemoved]:
            raise Exception("Invalid child event %s" % str(event_type))
        super().__init__(event_type)
        self._child = child

    def child(self):
        return self._child
