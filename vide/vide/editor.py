from videtoolkit import gui, core, consts, utils

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
from . import Linter
from . import commands
from . import flags
import logging
import time
import tempfile

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super().__init__(parent=parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._linter = Linter.PyFlakesLinter()

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()
        self._createInfoHoverBox()
        self._edit_area.setFocus()

        self._initBackupTimer()

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setFilename(self._document_model.filename())
        self._status_bar_controller = StatusBarController(self._status_bar, self._document_model, self._view_model)

    def _createCommandBar(self):
        self._command_bar = CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar.setMode(flags.COMMAND_MODE)
        self._view_model.modeChanged.connect(self._command_bar.setMode)
        self._command_bar.returnPressed.connect(self.executeCommand)
        self._command_bar.escapePressed.connect(self.abortCommand)

    def _createSideRuler(self):
        self._side_ruler = SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (4, self.height()-2) )
        self._side_ruler_controller = SideRulerController(self._side_ruler, self._view_model)

    def _createEditArea(self):
        self._edit_area = EditArea(self._document_model, self._view_model, parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )
        self._edit_area.setFocus()
        self._edit_area.cursorPositionChanged.connect(self.updateDocumentCursorInfo)

        self._edit_area_event_filter = EditAreaEventFilter(self._view_model, self._command_bar)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

    def _createInfoHoverBox(self):
        self._info_hover_box = InfoHoverBox(parent=self)
        self._info_hover_box.resize((0,0))
        self._info_hover_box.hide()

    def _initBackupTimer(self):
        self._backup_timer = core.VTimer()
        self._backup_timer.setInterval(60*1000)
        self._backup_timer.setSingleShot(False)
        self._backup_timer.timeout.connect(self.doBackup)
        self._backup_timer.start()

    def viewModelChanged(self):
        self.update()

    def executeCommand(self):
        command_text = self._command_bar.commandText().strip()
        logging.info("Executing command "+command_text)

        if command_text == 'q':
            gui.VApplication.vApp.exit()
        elif command_text == "w":
            self.doSave()
        elif command_text == "l":
            tmpfile = tempfile.NamedTemporaryFile(delete=False)
            self._document_model.saveAs(tmpfile.name)

            info = self._linter.lint(filename=self._document_model.filename(), original_filename=self._document_model.filename(), code=self._document_model.text())
            for i in info:
                if i.level == Linter.LinterResult.Level.ERROR:
                    self._side_ruler.addBadge(i.line,LineBadge(mark="E", description=i.message, bg_color=gui.VGlobalColor.red))
                elif i.level == Linter.LinterResult.Level.WARNING:
                    self._side_ruler.addBadge(i.line,LineBadge(mark="W", description=i.message,bg_color=gui.VGlobalColor.brown))
                else:
                    self._side_ruler.addBadge(i.line,LineBadge(mark="*", description=i.message,bg_color=gui.VGlobalColor.cyan))


        self._command_bar.clear()
        self._view_model.setEditorMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def abortCommand(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._view_model.setEditorMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def doSave(self):
        logging.info("Saving file")
        self._status_bar.setTemporaryMessage("Saving...")
        gui.VApplication.vApp.processEvents()
        self._document_model.save()
        self._status_bar.setTemporaryMessage("Saved", 2000)

    def doBackup(self):
        logging.info("Saving backup file")
        self._status_bar.setTemporaryMessage("Saving backup...")
        gui.VApplication.vApp.processEvents()
        self._document_model.saveBackup()
        self._status_bar.setTemporaryMessage("Backup saved", 2000)

    def show(self):
        super().show()
        self._edit_area.setFocus()

    def updateDocumentCursorInfo(self, document_pos):
        self._status_bar.setPosition(document_pos)
        badge = self._side_ruler.badge(document_pos.row)
        if badge is not None:
            self._info_hover_box.setText(badge.description())
            self._info_hover_box.move((0, gui.VCursor.pos()[consts.Index.Y]+1))
            self._info_hover_box.show()
        else:
            self._info_hover_box.hide()
