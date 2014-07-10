from .LineBadge import LineBadge
from vixtk import gui

class SideRulerController:
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler
        self._edit_area_model = None
        self._document = None

    def setModel(self, document, edit_area_model):
        if self._edit_area_model:
            self._edit_area_model.documentPosChanged.disconnect(self.updateTopRow)

        if self._document:
            self._document.lineMetaInfoChanged.disconnect(self.updateBadges)
            self._document.lineDeleted.disconnect(self.updateNumRows)
            self._document.lineCreated.disconnect(self.updateNumRows)

        self._edit_area_model = edit_area_model
        self._edit_area_model.documentPosChanged.connect(self.updateTopRow)

        self._document = document
        self._document.lineMetaInfoChanged.connect(self.updateBadges)
        self._document.lineDeleted.connect(self.updateNumRows)
        self._document.lineCreated.connect(self.updateNumRows)

        self.updateTopRow()
        self.updateNumRows()
        self.updateBadges()

    def updateTopRow(self, *args):
        if self._edit_area_model:
            top_pos = self._edit_area_model.documentPosAtTop()
            self._side_ruler.setTopRow(top_pos[0])

    def updateNumRows(self, *args):
        if self._document:
            self._side_ruler.setNumRows(self._document.numLines())

    def updateBadges(self, *args):
        if self._document:
            for line_num in range(1,self._document.numLines()+1):
                meta = self._document.lineMeta(line_num)

                if meta.get("change") == "added":
                    self._side_ruler.addBadge(line_num, LineBadge(marker="+", description="",
                              fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.green))
                elif meta.get("change") == "modified":
                    self._side_ruler.addBadge(line_num, LineBadge(marker=".", description="",
                             fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.magenta))
                elif meta.get("change") == None:
                    self._side_ruler.removeBadge(line_num)


