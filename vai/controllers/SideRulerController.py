from ..widgets import LineBadge
from ..linting import LinterResult
from ..models.TextDocument import LineMeta
from ..models import Configuration
from ..Utils import stringToColor
from vaitk import gui

class SideRulerController:
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler
        config = Configuration.instance()

        self._side_ruler.setColors(stringToColor(config["colors.side_ruler.fg"]),
                                   stringToColor(config["colors.side_ruler.bg"])
                                  )

        self._buffer = None

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        if self._buffer:
            self._buffer.edit_area_model.documentPosAtTopChanged.disconnect(self.updateTopRow)
            self._buffer.document.lineMetaInfoChanged.disconnect(self.updateBadges)
            self._buffer.document.contentChanged.disconnect(self.updateNumRows)

        self._buffer = buffer

        # Set signals
        self._buffer.edit_area_model.documentPosAtTopChanged.connect(self.updateTopRow)

        self._buffer.document.lineMetaInfoChanged.connect(self.updateBadges)
        self._buffer.document.contentChanged.connect(self.updateNumRows)

        # Refresh
        self.updateTopRow()
        self.updateNumRows()
        self.updateBadges()

    def updateTopRow(self, *args):
        if self._buffer:
            top_pos = self._buffer.edit_area_model.document_pos_at_top
            self._side_ruler.setTopRow(top_pos[0])

    def updateNumRows(self, *args):
        if self._buffer:
            self._side_ruler.setNumRows(self._buffer.document.numLines())

    def updateBadges(self, *args):
        if self._buffer:
            for line_num in range(1,self._buffer.document.numLines()+1):
                meta = self._buffer.document.lineMeta(line_num)
                badge = None

                lint = meta.get(LineMeta.LinterResult)
                if lint is not None:
                    if lint.level == LinterResult.Level.ERROR:
                        badge = LineBadge(marker="E",
                                          description=lint.message,
                                          fg_color=gui.VGlobalColor.yellow,
                                          bg_color=gui.VGlobalColor.red
                                )
                    elif lint.level == LinterResult.Level.WARNING:
                        badge = LineBadge(marker="W",
                                          description=lint.message,
                                          fg_color=gui.VGlobalColor.yellow,
                                          bg_color=gui.VGlobalColor.brown
                                )
                    elif lint.level == LinterResult.Level.INFO:
                        badge = LineBadge(marker="*",
                                          description=lint.message,
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

