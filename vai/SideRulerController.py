from .LineBadge import LineBadge
from .LinterResult import LinterResult
from .models.TextDocument import LineMeta
from vaitk import gui

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
        self._document.lineMetaInfoDeleted.connect(self.updateBadges)
        self._document.contentChanged.connect(self.updateNumRows)
        self._document.contentChanged.connect(self.updateBadges)

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
                badge = None

                linting = meta.get(LineMeta.LinterResult)
                if linting is not None:
                    if linting.level == LinterResult.Level.ERROR:
                        badge = LineBadge(marker="E",
                                          description=linting.message,
                                          fg_color=gui.VGlobalColor.yellow,
                                          bg_color=gui.VGlobalColor.red
                                )
                    elif linting.level == LinterResult.Level.WARNING:
                        badge = LineBadge(marker="W",
                                          description=linting.message,
                                          fg_color=gui.VGlobalColor.yellow,
                                          bg_color=gui.VGlobalColor.brown
                                )
                    elif linting.level == LinterResult.Level.INFO:
                        badge = LineBadge(marker="*",
                                          description=linting.message,
                                          fg_color=gui.VGlobalColor.yellow,
                                          bg_color=gui.VGlobalColor.cyan
                                        )

                change = meta.get(LineMeta.Change)
                if change == "added":
                    badge = LineBadge(marker="+", description="", fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.green)
                elif change == "modified":
                    badge = LineBadge(marker=".", description="", fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.magenta)


                if badge is None:
                    self._side_ruler.removeBadge(line_num)
                else:
                    self._side_ruler.addBadge(line_num, badge)

