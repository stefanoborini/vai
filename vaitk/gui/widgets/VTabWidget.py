from ..VWidget import VWidget
class VTabWidget(VWidget):
    def __init__(self, parent=None):
        super(VTabWidget, self).__init__(parent)
        self._tabs = []
        self._selected_tab_idx = -1

    def addTab(self, widget, label):
        self._tabs.append((widget, label))
        self._selected_tab_idx = 2

    def render(self, screen):
        screen = VApplication.vApp.screen()
        w, h = screen.size()
        if len(self._tabs):
            tab_size = w/len(self._tabs)
            header = ""
            for index, (_, label) in enumerate(self._tabs):
                header = label+" "*(tab_size-len(label))
                screen.write(tab_size * index, 0, header, curses.color_pair(1 if index == self._selected_tab_idx else 0))
            widget = self._tabs[self._selected_tab_idx][0]
            widget.render(screen)

