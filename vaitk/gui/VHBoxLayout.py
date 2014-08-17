from .VBoxLayout import VBoxLayout

class VHBoxLayout(VBoxLayout):
    def __init__(self, parent):
        super().__init__(VBoxLayout.LeftToRight, parent)
