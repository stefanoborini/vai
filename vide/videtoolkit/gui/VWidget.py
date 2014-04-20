from .. import core
from ..consts import Index
from .. import FocusPolicy
from ..core import events as coreevents
from .VApplication import VApplication
from .VPalette import VPalette
from .VPainter import VPainter
from .VScreen import VScreenArea


from . import events
import logging


class VWidget(core.VObject):
    def __init__(self, parent=None):
        if parent is None:
            parent = VApplication.vApp.rootWidget()

        super().__init__(parent)

        if self.parent() is None:
            self._geometry = (0,0) + VApplication.vApp.screen().size()
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
        if not isinstance(pos, tuple):
            raise TypeError("Invalid pos argument")
        self.setGeometry(pos+self.size())

    def resize(self, size):
        if not isinstance(size, tuple):
            raise TypeError("Invalid size argument")

        self.setGeometry(self.pos()+size)

    def pos(self):
        geometry = self.geometry()
        return ( geometry[Index.RECT_X],
                 geometry[Index.RECT_Y]
                 )


    def size(self):
        return ( self.geometry()[Index.RECT_WIDTH],
                 self.geometry()[Index.RECT_HEIGHT]
                 )

    def rect(self):
        return (0,0)+self.size()

    def absoluteRect(self):
        return self.mapToGlobal((0,0))+self.size()

    def geometry(self):
        return self._geometry

    def width(self):
        return self.geometry()[Index.RECT_WIDTH]

    def height(self):
        return self.geometry()[Index.RECT_HEIGHT]

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def setVisible(self, visible):
        self.logger.info("Setting explicit visibility for %s : %s" % (str(self), str(visible)))
        self._visible_explicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)

        if visible:
            VApplication.vApp.postEvent(self,events.VShowEvent())
        else:
            VApplication.vApp.postEvent(self,events.VHideEvent())

    def setVisibleImplicit(self, visible):
        self.logger.info("Setting implicit visibility for %s : %s" % (str(self), str(visible)))
        self._visible_implicit = visible
        for w in self.children():
            w.setVisibleImplicit(visible)

        if visible:
            VApplication.vApp.postEvent(self,events.VShowEvent())
        else:
            VApplication.vApp.postEvent(self,events.VHideEvent())

    def isVisible(self):
        return self._visible_explicit if self._visible_explicit is not None else self._visible_implicit

    def minimumSize(self):
        return (0,0)

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, rect):
        self.logger.info("VWidget.setGeometry %s" % str(rect))

        old_geometry = self._geometry

        min_size = self.minimumSize()
        self._geometry = (rect[Index.RECT_X],
                          rect[Index.RECT_Y],
                          max(min_size[Index.SIZE_WIDTH], rect[Index.RECT_WIDTH]),
                          max(min_size[Index.SIZE_HEIGHT], rect[Index.RECT_HEIGHT])
                         )

        if not self.isVisible():
            return

        if  (old_geometry[Index.RECT_X], old_geometry[Index.RECT_Y])  \
            != (self._geometry[Index.RECT_X], self._geometry[Index.RECT_Y]):

            VApplication.vApp.postEvent(self, events.VMoveEvent())

        if (old_geometry[Index.RECT_WIDTH], old_geometry[Index.RECT_WIDTH]) \
            != (self._geometry[Index.RECT_HEIGHT], self._geometry[Index.RECT_HEIGHT]):

            VApplication.vApp.postEvent(self, events.VResizeEvent())

    def mapToGlobal(self, pos):
        top_left = self.pos()
        if self.parent() is None:
            return (pos[Index.X]+top_left[Index.X], pos[Index.Y]+top_left[Index.Y])

        parent_corner = self.parent().mapToGlobal((0,0))
        return ( parent_corner[Index.X] + top_left[Index.X] + pos[Index.X],
                 parent_corner[Index.Y] + top_left[Index.Y] + pos[Index.Y]
                 )

    def screenArea(self):
        abs_pos_topleft = self.mapToGlobal((0,0))

        return VScreenArea( VApplication.vApp.screen(),
                            abs_pos_topleft + self.size()
                          )

    def event(self, event):
        self.logger.info("Event %s. Receiver %s" % (str(event), str(self)))

        if isinstance(event, events.VPaintEvent):
            if not self.isVisible():
                return True

            repaint_queue = [self]
            while len(repaint_queue) > 0:
                widget = repaint_queue.pop(0)
                if widget.isVisible():
                    self.logger.info("Widget %s visible. painting." % str(widget))
                    widget.paintEvent(event)

                for w in widget.depthFirstRightTree():
                    self.logger.info("Widget %s in rightTree" % str(w))
                    self.logger.info("%s, %s", w.absoluteRect(), widget.absoluteRect())
                    if core.intersects(w.absoluteRect(),widget.absoluteRect()):
                        self.logger.info("Intersected")
                        repaint_queue.append(w)
                self.logger.info("repaint queue: %s" % str(repaint_queue))


        elif isinstance(event, events.VFocusEvent):
            if self.isVisible():
                if event.eventType() == coreevents.VEvent.EventType.FocusIn:
                    self.focusInEvent(event)
            else:
                if event.eventType() == coreevents.VEvent.EventType.FocusOut:
                    self.focusOutEvent(event)

        elif isinstance(event, events.VHideEvent):
            if not self.isVisible():
                return True

            self.hideEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                #self.logger.info("%s, %s", w.absoluteRect(), self.absoluteRect())
                #if w.absoluteRect().intersects(self.absoluteRect()):
                    #self.logger.info("Intersected")
                w.paintEvent(events.VPaintEvent())
        elif isinstance(event, events.VShowEvent):
            if self.isVisible():
                return True

            self.showEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.paintEvent(events.VPaintEvent())
        elif isinstance(event, events.VMoveEvent):
            if not self.isVisible():
                return True

            self.moveEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.paintEvent(events.VPaintEvent())
        elif isinstance(event, events.VResizeEvent):
            if not self.isVisible():
                return True

            self.resizeEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.paintEvent(events.VPaintEvent())
        else:
            return super().event(event)

        return True

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

        string = ' '*size[Index.SIZE_WIDTH]
        for i in range(0, size[Index.SIZE_HEIGHT]):
            painter.drawText( (0, i), string, fg, bg)

    def focusInEvent(self, event):
        self.logger.info("FocusIn event")

    def focusOutEvent(self, event):
        self.logger.info("FocusOut event")

    def hideEvent(self, event):
        self.logger.info("Hide event")

    def moveEvent(self, event):
        self.logger.info("Move event")

    def showEvent(self, event):
        self.logger.info("Show event")

    def resizeEvent(self, event):
        self.logger.info("Resize event")

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
        VApplication.vApp.postEvent(self,events.VPaintEvent())

    def contentsRect(self):
        margins = self.contentsMargins()
        return (margins[Index.MARGIN_LEFT],
                margins[Index.MARGIN_TOP],
                self.width()-margins[Index.MARGIN_LEFT]-margins[Index.MARGIN_RIGHT],
                self.height()-margins[Index.MARGIN_TOP]-margins[Index.MARGIN_BOTTOM]
                )

    def contentsMargins(self):
        return (0,0,0,0)
