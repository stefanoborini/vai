from .. import Key, KeyModifier, nativeToVideKeyCode, videKeyCodeToText

class VKeyEvent(object):
    def __init__(self, key_code):
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

    def accept(self):
        self._accepted = True

    def ignore(self):
        self._accepted = False

    def setAccepted(self, accepted):
        self._accepted = accepted

    def accepted(self):
        return self._accepted

    @staticmethod
    def fromNativeKeyCode(native_key_code):
        key_code = nativeToVideKeyCode(native_key_code)
        return VKeyEvent(key_code)

class VPaintEvent(object):
    pass

