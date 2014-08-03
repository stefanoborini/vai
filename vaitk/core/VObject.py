from . import VTimerEvent
import logging


class VObject:
    """
    Base class for all objects in VixTk.
    Provides methods for the object hierarchy traversal.

    A derived class can set the class variable debug to True to enable
    debugging at the DEBUG level for that specific class.

    Example:
    class Foo(VObject):
        debug = True

    The class can also specify the specific logging level
    class Foo(VObject):
        debug = True
        debug_level = logging.INFO

    An instance of VObject will always have a logger in self.logger
    """

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.logger = logging.getLogger(cls.__name__)
        if hasattr(cls, "debug"):
            if hasattr(cls, "debug_level"):
                level = cls.debug_level
            else:
                level = logging.DEBUG
            instance.logger.setLevel(level)
            instance.logger.log(level, "Debugging enabled for "+str(cls.__name__))
        else:
            instance.logger.setLevel(logging.CRITICAL+1)

        return instance

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

    def removeChild(self, child):
        self._children.remove(child)

    def depthFirstFullTree(self):
        return self.root().depthFirstSubTree()

    def depthFirstSubTree(self):
        result = [self]
        for c in self.children():
            result.extend(c.depthFirstSubTree())
        return result

    def root(self):
        return self.traverseToRoot()[-1]

    def traverseToRoot(self):
        result = [self]
        if self.parent() is None:
            return result
        result.extend(self.parent().traverseToRoot())
        return result

    def depthFirstRightTree(self):
        depth_first_tree = self.depthFirstFullTree()
        return depth_first_tree[depth_first_tree.index(self)+1:]

    def depthFirstLeftTree(self):
        depth_first_tree = self.depthFirstFullTree()
        return depth_first_tree[:depth_first_tree.index(self)]

    def installEventFilter(self, event_filter):
        self._event_filters.append(event_filter)

    def eventFilter(self, watched, event):
        return False

    def installedEventFilters(self):
        return self._event_filters

    def event(self, event):
        if isinstance(event, VTimerEvent.VTimerEvent):
            self.timerEvent(event)
            return True
        return False

    def timerEvent(self, event):
        return True

    def __str__(self):
        return self.__class__.__name__
