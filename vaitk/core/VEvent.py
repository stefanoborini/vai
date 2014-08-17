class VEvent:
    class EventType:
        NoEvent  = 0
        Timer    = 1
        KeyPress = 6
        FocusIn  = 8
        FocusOut = 9
        Paint    = 12
        Move     = 13
        Resize   = 14
        Show     = 17
        Hide     = 18
        Close    = 19
        Quit     = 20
        ParentChange = 21
        ChildAdded = 68
        ChildPolished = 69
        ChildRemoved = 71
        LayoutRequest = 76
        UpdateRequest = 77
        ZOrderChange = 126
        ContentsRectChange = 178
        

    def __init__(self, event_type):
        self._event_type = event_type
        self._accepted = False
        self._spontaneous = False

    def accept(self):
        self.setAccepted(True)

    def ignore(self):
        self.setAccepted(False)

    def isAccepted(self):
        return self._accepted

    def setAccepted(self, accepted):
        self._accepted = accepted

    def eventType(self):
        return self._event_type

    def spontaneous(self):
        return self._spontaneous
        
    def setSpontaneous(self, spontaneous):
        self._spontaneous = spontaneous
        
    def __str__(self):
        return (self.__class__.__name__+"(%d)") % self.eventType()

