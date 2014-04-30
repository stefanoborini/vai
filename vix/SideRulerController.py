from .LineBadge import LineBadge
from vixtk import gui

class SideRulerController:
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler
        self._view_model = None
        self._document_model = None

    def setModel(self, document_model, view_model):
        if self._view_model:
            self._view_model.documentPosChanged.disconnect(self.updateRange)

        if self._document_model:
            self._document_model.lineMetaInfoChanged.disconnect(self.updateBadges)

        self._view_model = view_model
        self._view_model.documentPosChanged.connect(self.updateRange)

        self._document_model = document_model
        self._document_model.lineMetaInfoChanged.connect(self.updateBadges)

        self.updateRange()
        self.updateBadges()

    def updateRange(self):
        if self._view_model:
            top_pos = self._view_model.documentPosAtTop()
            self._side_ruler.setStart(top_pos.row)

    def updateBadges(self, *args):
        if self._document_model:
            for line_num in range(1,self._document_model.numLines()+1):
                meta = self._document_model.lineMeta(line_num)

                if meta.get("change") == "added":
                    self._side_ruler.addBadge(line_num, LineBadge(marker="+", description="",
                              fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.green))
                elif meta.get("change") == "modified":
                    self._side_ruler.addBadge(line_num, LineBadge(marker=".", description="",
                             fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.magenta))
                elif meta.get("change") == None:
                    self._side_ruler.removeBadge(line_num)


