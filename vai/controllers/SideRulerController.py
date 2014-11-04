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
            self._buffer.document.lineMetaInfo("LinterResult").contentChanged.disconnect(self.updateBadges)
            self._buffer.document.numLinesChanged.disconnect(self.updateNumRows)

        self._buffer = buffer

        # Set signals
        self._buffer.edit_area_model.documentPosAtTopChanged.connect(self.updateTopRow)
        self._buffer.document.lineMetaInfo("LinterResult").contentChanged.connect(self.updateBadges)
        self._buffer.document.numLinesChanged.connect(self.updateNumRows)

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
        if not self._buffer:
            return

        top_pos = self._buffer.edit_area_model.document_pos_at_top[0]
        # FIXME: compute actual number of rows
        num_lines = 50
        badges = [None] * num_lines

        changed_data = self._buffer.document.lineMetaInfo("Change").data(top_pos, num_lines)

        for idx, change in enumerate(changed_data):
            if change == "added":
                badges[idx] = LineBadge(marker="+", description="", fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.green)
            elif change == "modified":
                badges[idx] = LineBadge(marker=".", description="", fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.magenta)

        lint_data = self._buffer.document.lineMetaInfo("LinterResult").data(top_pos, num_lines)

        for idx, lint in enumerate(lint_data):
            if lint is None:
                continue

            if lint.level == LinterResult.Level.ERROR:
                badges[idx] = LineBadge(marker="E",
                                  description=lint.message,
                                  fg_color=gui.VGlobalColor.yellow,
                                  bg_color=gui.VGlobalColor.red
                        )
            elif lint.level == LinterResult.Level.WARNING:
                badges[idx] = LineBadge(marker="W",
                                  description=lint.message,
                                  fg_color=gui.VGlobalColor.yellow,
                                  bg_color=gui.VGlobalColor.brown
                        )
            elif lint.level == LinterResult.Level.INFO:
                badges[idx] = LineBadge(marker="*",
                                  description=lint.message,
                                  fg_color=gui.VGlobalColor.yellow,
                                  bg_color=gui.VGlobalColor.cyan
                                )

        self._side_ruler.setBadges(badges)

