from ..widgets import LineBadge
from ..linting import LinterResult
from ..models import Configuration, Icons
from vaitk import gui

class SideRulerController:
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler


        self._buffer = None
        self._icons = Icons.getCollection(Configuration.get("icons.collection"))

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        if self._buffer:
            self._buffer.edit_area_model.documentPosAtTopChanged.disconnect(self.updateWidget)
            self._buffer.document.numLinesChanged.disconnect(self.updateWidget)
            self._buffer.document.lineMetaInfo("LinterResult").contentChanged.disconnect(self.updateWidget)
            self._buffer.document.lineMetaInfo("Change").contentChanged.disconnect(self.updateWidget)
            self._buffer.document.lineMetaInfo("Bookmark").contentChanged.disconnect(self.updateWidget)

        self._buffer = buffer

        # Set signals
        self._buffer.edit_area_model.documentPosAtTopChanged.connect(self.updateWidget)
        self._buffer.document.numLinesChanged.connect(self.updateWidget)
        self._buffer.document.lineMetaInfo("LinterResult").contentChanged.connect(self.updateWidget)
        self._buffer.document.lineMetaInfo("Change").contentChanged.connect(self.updateWidget)
        self._buffer.document.lineMetaInfo("Bookmark").contentChanged.connect(self.updateWidget)

        # Refresh
        self.updateWidget()

    def updateWidget(self, *args):
        if self._buffer is None:
            return

        top_pos = self._buffer.edit_area_model.document_pos_at_top
        self._side_ruler.setTopLine(top_pos[0])
        self._side_ruler.setNumLines(self._buffer.document.numLines())

        badges = {}
        needed_lines = self._side_ruler.visibleLineNumbers()
        changed_data = self._buffer.document.lineMetaInfo("Change").dataForLines(needed_lines)

        for line, change in changed_data.items():
            if change == "added":
                badges[line] = LineBadge(marker=self._icons["SideRuler.added"],
                                         fg_color=gui.VGlobalColor.green,
                                         bg_color=None)
            elif change == "modified":
                badges[line] = LineBadge(marker=self._icons["SideRuler.modified"],
                                         fg_color=gui.VGlobalColor.magenta,
                                         bg_color=None)
            elif change == "deletion_before":
                badges[line] = LineBadge(marker=self._icons["SideRuler.deletion_before"],
                                         fg_color=gui.VGlobalColor.red,
                                         bg_color=None)
            elif change == "deletion_after":
                badges[line] = LineBadge(marker=self._icons["SideRuler.deletion_after"],
                                         fg_color=gui.VGlobalColor.red,
                                         bg_color=None)

        bookmarks = self._buffer.document.lineMetaInfo("Bookmark").dataForLines(needed_lines)

        for line, mark in bookmarks.items():
            if mark is None:
                continue

            badges[line] = LineBadge(marker=self._icons["SideRuler.bookmarks"][ord(mark)-ord('a')],
                                  fg_color=gui.VGlobalColor.yellow,
                                  bg_color=None,
                        )

        lint_data = self._buffer.document.lineMetaInfo("LinterResult").dataForLines(needed_lines)

        for line, lint in lint_data.items():
            if lint is None:
                continue

            if lint.level == LinterResult.Level.ERROR:
                badges[line] = LineBadge(marker=self._icons["SideRuler.error"],
                                  fg_color=gui.VGlobalColor.red,
                                  bg_color=None
                        )
            elif lint.level == LinterResult.Level.WARNING:
                badges[line] = LineBadge(marker=self._icons["SideRuler.warning"],
                                  fg_color=gui.VGlobalColor.yellow,
                                  bg_color=None
                        )
            elif lint.level == LinterResult.Level.INFO:
                badges[line] = LineBadge(marker=self._icons["SideRuler.info"],
                                  fg_color=gui.VGlobalColor.cyan,
                                  bg_color=None
                                )

        self._side_ruler.setBadges(badges)
        self._side_ruler.update()


