from .. import core
from .VApplication import VApplication
from .VPalette import VPalette
from .VPainter import VPainter
from .VScreen import VScreenArea

from .events import VPaintEvent

class VWidget(core.VObject):
    def __init__(self, parent=None):
        super(VWidget, self).__init__(parent)
        if parent is None:
            VApplication.vApp.addTopLevelWidget(self)
            self._size = VApplication.vApp.screen().size()
            self._pos = (0,0)
            self.setFocus()
        else:
            contents_rect = self.parent().contentsRect()
            self._pos = contents_rect[0], contents_rect[1]
            self._size = contents_rect[2], contents_rect[3]

        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True

    def keyEvent(self, event):
        pass

    def setFocus(self):
        VApplication.vApp.setFocusWidget(self)

    def move(self, x, y):
        self._pos = (x,y)
        self.update()

    def resize(self, w, h):
        self._size = (w,h)
        self.update()

    def pos(self):
        return self._pos

    def size(self):
        return self._size

    def rect(self):
        return (0,0, self.width(), self.height())

    def width(self):
        return self._size[0]

    def height(self):
        return self._size[1]

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def setVisible(self, visible):
        self._visible_explicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)
        self.update()

    def setVisibleImplicit(self, visible):
        self._visible_implicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)
        self.update()

    def isVisible(self):
        return self._visible_explicit if self._visible_explicit is not None else self._visible_implicit

    def minimumSize(self):
        return (1,1)

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, x, y, w, h):
        self._pos = (x,y)
        min_size = self.minimumSize()
        self._size = (max(min_size[0], w) , max(min_size[1], h))
        self.update()

    def mapToGlobal(self, x, y):
        if self.parent() is None:
            return (x+self._pos[0],y+self._pos[1])

        global_corner = self.parent().mapToGlobal(0,0)
        return (global_corner[0] + self.pos()[0] + x, global_corner[1] + self.pos()[1] + y)

    def screenArea(self):
        abs_pos_topleft = self.mapToGlobal(0,0)

        return VScreenArea( VApplication.vApp.screen(),
                            abs_pos_topleft[0],
                            abs_pos_topleft[1],
                            self.width(),
                            self.height())

    def paintEvent(self, event):
        painter = VPainter(self)
        #if self._layout is not None:
        #    self._layout.apply()

        w, h = self.size()
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)

        for i in xrange(0, h):
            painter.write(0, i, ' '*w, fg, bg)

    def isEnabled(self):
        return self._enabled

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def setEnabled(self, enabled):
        self._enabled = enabled

    def palette(self):
        if self._palette is None:
            self._palette = VApplication.vApp.palette().copy()

        return self._palette

    def setColors(self, fg=None, bg=None):
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText, fg)
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.Window, bg)

    def colors(self, color_group = VPalette.ColorGroup.Active):

        fg = self.palette().color(color_group, VPalette.ColorRole.WindowText)
        bg = self.palette().color(color_group, VPalette.ColorRole.Window)

        return (fg, bg)

    def currentColors(self):
        if self.isActive():
            color_group = VPalette.ColorGroup.Active
        else:
            if isEnabled(self):
                color_group = VPalette.ColorGroup.Inactive
            else:
                color_group = VPalette.ColorGroup.Disabled
        return self.colors(color_group)

    def update(self):
        VApplication.vApp.postEvent(self,VPaintEvent())

    def contentsRect(self):
        return (self.contentsMargins()[0],
                self.contentsMargins()[1],
                self.width()-self.contentsMargins()[0]-self.contentsMargins()[2],
                self.height()-self.contentsMargins()[1]-self.contentsMargins()[3]
                )

    def contentsMargins(self):
        return (0,0,0,0)
