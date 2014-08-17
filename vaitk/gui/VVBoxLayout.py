from .VBoxLayout import VBoxLayout

class VVBoxLayout(VBoxLayout):
    def __init__(self, parent):
        super().__init__(VBoxLayout.Direction.TopToBottom, parent)

