from .VLabel import VLabel
import logging

class VToolTip(VLabel):
    @staticmethod
    def showText(pos, text):
        tip = VToolTip(text, parent=None)
        tip.resize(tip.minimumSize())
        tip.move(pos)
        tip.show()
