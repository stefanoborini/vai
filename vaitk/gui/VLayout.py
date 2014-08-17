from .. import core

class VWidgetItem:
    def __init__(self, layout, widget):
        self._layout = layout
        self._widget = widget

class VSpacerItem:
    def __init__(self):
        pass

class VLayout(core.VObject):
    def __init__(self, parent):
        super().__init__(parent)

        if parent is None:
            return

        parent.setLayout(self)

    def addWidget(self, widget):
        self.addChildWidget(widget)
        self.addItem(VWidgetItem(self, widget))
        
    
    def contentsRect(self):
        return (0,0,0,0)
    
    def parentWidget(self):
        parent = self.parent()
        
        if self.topLevel():
            return parent
            
        if parent is None:
            return None
        
        if isinstance(parent, VLayout):
            return parent.parentWidget()
        
        return None
    
    def isEmpty(self):
        return any([not item.isEmpty() for item in self.items()])
        
    def setGeometry(self, rect):
        self._rect = rect
    
    def geometry(self):
        return self._rect
                
    def invalidate(self):
        self._rect = (0,0,0,0)
        self.update()
        
    def addChildWidget(self, widget):
        this_parent = self.parent()
        widget_parent = widget.parent()
        if widget_parent is not None:
            raise Exception("Cannot reparent widget yet")
        widget.setParent(this_parent)

    
    # -----------------------
    
    
    def update(self):
        layout = self
        while layout and layout.activated():
            if layout.topLevel():
                widget = layout.parent()
                QApplication.postEvent(widget, VEvent(VEvent.LayoutRequest))
                break
            layout = layout.parent()
            

    def activate(self):
        parent = self.parent()
        activateRecursive(self)
        
        
        self.doResize(widget.size())
        widget.updateGeometry()
        return True
        
    def doResize(self):
        parent = self.parentWidget()
        self.setGeometry(parent.rect())
        
    
    def widgetEvent(self, event):
        
        if (e.eventType() == VEvent.Resize):
            if self.activated():
                self.doResize(event.size())
            else:
                self.activate()
            
        elif (event.eventType() == VEvent.ChildRemoved):
            child = event.child()
            removeWidgetRecursively(self, child)
        
        elif (event.eventType() == VEvent.LayoutRequest):
            if self.parent().isVisible():
                self.activate()
    
    def childEvent(self, event):
        if not self.enabled():
            return
        
        if event.eventType() == VEvent.ChildRemoved:
            for i, item in enumerate(self.items()):
                if item == event.child():
                    self.takeAt(i)
                    self.invalidate()
                    break
                    
        
        
def removeWidgetRecursively(item, widget):
    layout = item.layout()
    if not layout:
        return False
        
