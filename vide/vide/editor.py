from videtoolkit import gui, core, utils

from .SideRuler import SideRuler
from .SideRulerController import SideRulerController
from .StatusBar import StatusBar
from .StatusBarController import StatusBarController
from .CommandBar import CommandBar
from .InfoHoverBox import InfoHoverBox
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .ViewModel import ViewModel
from .LineBadge import LineBadge
from .Linter import Linter
from . import commands
from . import flags
import logging

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super().__init__(parent=parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._linter = Linter()

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()
        self._createInfoHoverBox()
        self._edit_area.setFocus()

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move( core.VPoint(0, self.height()-2) )
        self._status_bar.resize( core.VSize(self.width(), 1) )
        self._status_bar.setFilename(self._document_model.filename())
        self._status_bar_controller = StatusBarController(self._status_bar, self._view_model)

    def _createCommandBar(self):
        self._command_bar = CommandBar(self)
        self._command_bar.move( core.VPoint(0, self.height()-1) )
        self._command_bar.resize( core.VSize(self.width(), 1) )
        self._command_bar.setMode(flags.COMMAND_MODE)
        self._view_model.modeChanged.connect(self._command_bar.setMode)
        self._command_bar.returnPressed.connect(self.executeCommand)
        self._command_bar.escapePressed.connect(self.abortCommand)

    def _createSideRuler(self):
        self._side_ruler = SideRuler(self)
        self._side_ruler.move( core.VPoint(0, 0) )
        self._side_ruler.resize( core.VSize(4, self.height()-2) )
        self._side_ruler_controller = SideRulerController(self._side_ruler, self._view_model)

    def _createEditArea(self):
        self._edit_area = EditArea(self._document_model, self._view_model, parent = self)
        self._edit_area.move( core.VPoint(4, 0) )
        self._edit_area.resize( core.VSize(self.width()-4, self.height()-2) )
        self._edit_area.setFocus()
        self._edit_area.cursorPositionChanged.connect(self.updateDocumentCursorInfo)

        self._edit_area_event_filter = EditAreaEventFilter(self._view_model, self._command_bar)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

    def _createInfoHoverBox(self):
        self._info_hover_box = InfoHoverBox(parent=self)
        self._info_hover_box.resize(core.VSize(0,0))
        self._info_hover_box.hide()

    def viewModelChanged(self):
        self.update()

    def executeCommand(self):
        command_text = self._command_bar.commandText().strip()
        logging.info("Executing command "+command_text)

        if command_text == 'q':
            gui.QApplication.qApp.exit()
        elif command_text == "w":
            self.doSave()
        elif command_text == "l":
            info = self._linter.lint(self._document_model)
            for i in info:
                if i[1] == 'E':
                    self._side_ruler.addBadge(i[2],LineBadge(mark="E", description=i[6], bg_color=gui.VGlobalColor.red))
                elif i[1] == 'W':
                    self._side_ruler.addBadge(i[2],LineBadge(mark="W", description=i[6],bg_color=gui.VGlobalColor.brown))
                else:
                    self._side_ruler.addBadge(i[2],LineBadge(mark="*", description=i[6],bg_color=gui.VGlobalColor.cyan))


        self._command_bar.clear()
        self._edit_area.setFocus()

    def abortCommand(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._view_model.setEditorMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def doSave(self):
        logging.info("Saving file")
        self._document_model.saveAs("output")

    def show(self):
        super().show()
        self._edit_area.setFocus()

    def updateDocumentCursorInfo(self, document_pos):
        self._status_bar.setPosition(document_pos)
        badge = self._side_ruler.badge(document_pos.row)
        if badge is not None:
            self._info_hover_box.setText(badge.description())
            self._info_hover_box.move(core.VPoint(0, gui.VCursor.pos().y()+1))
            self._info_hover_box.show()
        else:
            self._info_hover_box.hide()
