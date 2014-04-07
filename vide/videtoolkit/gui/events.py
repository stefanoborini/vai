from .. import Key, KeyModifier, nativeToVideKeyCode, videKeyCodeToText
from ..core.events import VEvent

class VKeyEvent(VEvent):
    def __init__(self, key_code):
        super(VKeyEvent, self).__init__(VEvent.EventType.KeyPress)
        self._key_code = key_code
        self._accepted = False

    def keyCode(self):
        return self._key_code

    def key(self):
        return self._key_code & Key.Mask

    def modifiers(self):
        return self._key_code & KeyModifier.Mask

    def text(self):
        return videKeyCodeToText(self._key_code)

    @staticmethod
    def fromNativeKeyCode(native_key_code):
        key_code = nativeToVideKeyCode(native_key_code)
        if key_code is None:
            return None
        return VKeyEvent(key_code)

class VFocusEvent(VEvent):
    def __init__(self, focus_type):
        super(VFocusEvent, self).__init__(focus_type)

class VPaintEvent(VEvent):
    def __init__(self):
        super(VPaintEvent, self).__init__(VEvent.EventType.Paint)

