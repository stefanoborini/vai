from .VLayout import VLayout

class VBoxLayout(VLayout):
    class Direction:
        LeftToRight = 0
        RightToLeft = 1
        TopToBottom = 2
        BottomToTop = 3

    def __init__(self, direction, parent):
        super().__init(parent)
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    def insertLayout(self):
        pass

    def insertWidget(self, index, widget):
        
        self._widgets.append(widget)

    def apply(self):
        size = self.parent().size()
        available_size = size[0]/len(self._widgets)
        for i,w in enumerate(self._widgets):
            w.move(available_size*i,0)
            w.resize(available_size, size[1])

    def setParent(self, parent):
        self._parent = parent

    def parent(self):
        return self._parent

    def invalidate(self):
        self._dirty = True
        super().invalidate()

