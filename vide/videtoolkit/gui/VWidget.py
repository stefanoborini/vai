from .. import core
from .. import FocusPolicy
from ..core import events as coreevents
from .VApplication import VApplication
from .VPalette import VPalette
from .VPainter import VPainter
from .VScreen import VScreenArea


from .events import VPaintEvent, VFocusEvent
import logging


class VWidget(core.VObject):
    def __init__(self, parent=None):
        if parent is None:
            parent = VApplication.vApp.rootWidget()

        super().__init__(parent)

        if self.parent() is None:
            self._geometry = core.VRect(top_left = core.VPoint(0,0), size = VApplication.vApp.screen().size())
        else:
            self._geometry = self.parent().contentsRect()

        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True
        self._focus_policy = FocusPolicy.NoFocus

    def keyEvent(self, event):
        pass

    def setFocus(self):
        VApplication.vApp.setFocusWidget(self)

    def hasFocus(self):
        return (self is VApplication.vApp.focusWidget())

    def move(self, pos):
        if not isinstance(pos, core.VPoint):
            raise TypeError("Invalid pos argument")
        self.setGeometry(core.VRect(pos=pos, size=self.size()))

    def resize(self, size):
        if not isinstance(size, core.VSize):
            raise TypeError("Invalid size argument")

        self.setGeometry(core.VRect(pos=self.pos(), size=size))

    def pos(self):
        return self.geometry().topLeft()

    def size(self):
        return self.geometry().size()

    def rect(self):
        return core.VRect(top_left=core.VPoint(0,0), size=self.size())

    def absoluteRect(self):
        return core.VRect(self.mapToGlobal(core.VPoint(0,0)), self.size())

    def geometry(self):
        return self._geometry

    def width(self):
        return self.geometry().width()

    def height(self):
        return self.geometry().height()

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def setVisible(self, visible):
        logging.info("Setting explicit visibility for %s : %s" % (str(self), str(visible)))
        self._visible_explicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)
        self.update()

    def setVisibleImplicit(self, visible):
        logging.info("Setting implicit visibility for %s : %s" % (str(self), str(visible)))
        self._visible_implicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)
        self.update()

    def isVisible(self):
        return self._visible_explicit if self._visible_explicit is not None else self._visible_implicit

    def minimumSize(self):
        return core.VSize(0,0)

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, rect):
        self.logger.info("VWidget.setGeometry %s" % str(rect))

        min_size = self.minimumSize()
        self._geometry = core.VRect(pos=rect.topLeft(),
                                    size=core.VSize(max(min_size.width(), rect.width()),
                                          max(min_size.height(), rect.height()) )
                                )
        self.update()

    def mapToGlobal(self, pos):
        if self.parent() is None:
            return pos+self.pos()

        parent_corner = self.parent().mapToGlobal(core.VPoint(0,0))
        return parent_corner + self.pos() + pos

    def screenArea(self):
        abs_pos_topleft = self.mapToGlobal(core.VPoint(0,0))

        return VScreenArea( VApplication.vApp.screen(),
                            core.VRect(top_left = abs_pos_topleft,
                                       size = self.size()
                                       )
                             )

    def event(self, event):
        if isinstance(event, VPaintEvent):
            logging.info("Paint event. Receiver "+str(self))
            repaint_queue = [self]
            while len(repaint_queue) > 0:
                widget = repaint_queue.pop(0)
                if not widget.isVisible():
                    logging.info("Widget %s not visible. skipping." % str(widget))
                    continue

                logging.info("Widget %s visible. painting." % str(widget))
                widget.paintEvent(event)
                repaint_queue.extend(widget.children())

            return True
        elif isinstance(event, VFocusEvent):
            if event.eventType() == coreevents.VEvent.EventType.FocusIn:
                self.focusInEvent(event)
            elif event.eventType() == coreevents.VEvent.EventType.FocusOut:
                self.focusOutEvent(event)
            return True
        else:
            return super(VWidget, self).event(event)

        return False

    def paintEvent(self, event):
        painter = VPainter(self)
        #if self._layout is not None:
        #    self._layout.apply()

        size = self.size()
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled

        fg, bg = self.colors(color_group)

        for i in range(0, size.height()):
            painter.write( (0, i), ' '*size.width(), fg, bg)

    def focusInEvent(self, event):
        logging.info("FocusIn event")

    def focusOutEvent(self, event):
        logging.info("FocusOut event")

    def setFocusPolicy(self, policy):
        self._focus_policy = policy

    def focusPolicy(self):
        return self._focus_policy

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
        return core.VRect(top_left = core.VPoint(self.contentsMargins()[0],
                                                 self.contentsMargins()[1]
                                                ),
                          size = core.VSize( self.width()-self.contentsMargins()[0]-self.contentsMargins()[2],
                                             self.height()-self.contentsMargins()[1]-self.contentsMargins()[3]
                                            )
                        )

    def contentsMargins(self):
        return (0,0,0,0)
