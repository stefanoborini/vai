from .VObject import VObject
from .VPoint import VPoint
from .VRect import VRect
from .VSize import VSize
from .VCoreApplication import VCoreApplication
from .VTimer import VTimer
from .VSignal import VSignal
from .events import VTimerEvent
from ..consts import Index

def intersects(t1, t2):
    return (t1[Index.X] <= (t2[Index.X] + t2[Index.RECT_WIDTH - 1]) \
            and (t1[Index.X] + t1[Index.RECT_WIDTH] - 1) >= t2[Index.X] \
            and t1[Index.Y] <= (t2[Index.Y] + t2[Index.RECT_HEIGHT] - 1) \
            and t1[Index.Y] + t1[Index.RECT_HEIGHT] - 1 >= t2[Index.RECT_Y])
