from .events import VTimerEvent

class VObject(object):
    def __init__(self, parent = None):
        self._parent = parent
        self._children = []
        self._event_filters = []
        if self._parent is not None:
            parent.addChild(self)

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def addChild(self, child):
        self._children.append(child)

    def tree(self):
        result = [self ]
        for c in self.children():
            result.extend(c.tree())
        return result

    def traverseToRoot(self):
        result = [self]
        if self.parent() is None:
            return result
        result.extend(self.parent().traverseToRoot())
        return result

    def installEventFilter(self, event_filter):
        self._event_filters.append(event_filter)

    def eventFilter(self, watched, event):
        return False

    def installedEventFilters(self):
        return self._event_filters

    def event(self, event):
        if isinstance(event, VTimerEvent):
            self.timerEvent(event)
            return True
        return False

    def timerEvent(self, event):
        return True

    def __str__(self):
        return self.__class__.__name__
