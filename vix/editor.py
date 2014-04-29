from vixtk import gui, core, consts, utils

from .SideRuler import SideRuler
from .SideRulerController import SideRulerController
from .StatusBar import StatusBar
from .StatusBarController import StatusBarController
from .CommandBar import CommandBar
from .CommandBarController import CommandBarController
from .InfoHoverBox import InfoHoverBox
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .LineBadge import LineBadge
from .Lexer import Lexer
from . import Linter
from . import commands
from . import flags
from .models.ViewModel import ViewModel
from .models.Buffer import Buffer
from .models.BufferList import BufferList
from .models.TextDocument import TextDocument
from .models.EditorModel import EditorModel
import logging
import time
import tempfile

class Editor(gui.VWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._editor_model = EditorModel()
        self._linter = Linter.PyFlakesLinter()
        self._lexer = Lexer()

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()
        self._createInfoHoverBox()

        self._initBackupTimer()

        self._editor_model.setMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

        self._buffers = BufferList()
        self._buffers.currentBufferChanged.connect(self._bufferChanged)
        self._buffers.addAndSelect(Buffer(TextDocument(), ViewModel()))

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)
        self._status_bar_controller = StatusBarController(self._status_bar)

    def _createCommandBar(self):
        self._command_bar = CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar_controller = CommandBarController(self._command_bar, self._editor_model)
        self._command_bar.returnPressed.connect(self.executeCommand)
        self._command_bar.escapePressed.connect(self.abortCommand)

    def _createSideRuler(self):
        self._side_ruler = SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (4, self.height()-2) )
        self._side_ruler_controller = SideRulerController(self._side_ruler)

    def _createEditArea(self):
        self._edit_area = EditArea(parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )
        self._edit_area.setFocus()

        self._edit_area.cursorPositionChanged.connect(self.updateDocumentCursorInfo)
        self._edit_area_event_filter = EditAreaEventFilter(self._command_bar)
        self._edit_area_event_filter.setModel(self._editor_model)
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

    def executeCommand(self):
        command_text = self._command_bar.commandText().strip()
        logging.info("Executing command "+command_text)

        if command_text == 'q!':
            gui.VApplication.vApp.exit()
        elif command_text == 'q':
            if any([b.isModified() for b in self._buffers]):
                self._status_bar.setMessage("Document has been modified. Use :q! to quit without saving or :qw to save and quit.", 3000)
            else:
                gui.VApplication.vApp.exit()
        elif command_text == "w":
            self.doSave()
        elif command_text == "wq":
            self.doSave()
            gui.VApplication.vApp.exit()
        elif command_text == "l":
            self.doLint()
        elif command_text.startswith("e "):
            buffer = Buffer(TextDocument(command_text[2:]),
                                        ViewModel()
                                        )
            self._buffers.addAndSelect(buffer)
        elif command_text.startswith("bp"):
            self._buffers.selectPrev()
        elif command_text.startswith("bn"):
            self._buffers.selectNext()


        self._command_bar.clear()
        self._editor_model.setMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def abortCommand(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._editor_model.setMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def doLint(self):
        pass
            #tmpfile = tempfile.NamedTemporaryFile(delete=False)
            #self.currentBuffer().documentModel().saveAs(tmpfile.name)
#
#            info = self._linter.lint(filename=self._current_document.filename(), original_filename=self._current_document.filename(), code=self._current_document.text())
#            for i in info:
#                if i.level == Linter.LinterResult.Level.ERROR:
#                    self._side_ruler.addBadge(i.line,LineBadge(mark="E", description=i.message, bg_color=gui.VGlobalColor.red))
#                elif i.level == Linter.LinterResult.Level.WARNING:
#                    self._side_ruler.addBadge(i.line,LineBadge(mark="W", description=i.message,bg_color=gui.VGlobalColor.brown))
#                else:
#                    self._side_ruler.addBadge(i.line,LineBadge(mark="*", description=i.message,bg_color=gui.VGlobalColor.cyan))

    def doSave(self):
        logging.info("Saving file")
        self._status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()
        self._buffers.currentBuffer().documentModel().save()
        self._status_bar.setMessage("Saved %s" % self._buffers.currentBuffer().documentModel().filename(), 3000)

    def doBackup(self):
        logging.info("Saving backup file")
        #self._status_bar.setMessage("Saving backup...")
        #gui.VApplication.vApp.processEvents()

        #self._current_document.saveBackup()
        #self._status_bar.setTemporaryMessage("Backup saved", 3000)

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

    def openFile(self, filename):
        current_buffer = self._buffers.current()
        try:
            new_buffer = Buffer(TextDocument(filename), ViewModel())
        except Exception as e:
            self._status_bar.setMessage("Error: could not open file. %s" % str(e), 3000)
            return

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self._buffers.replaceAndSelect(current_buffer, new_buffer)
        else:
            self._buffers.addAndSelect(new_buffer)

    def _bufferChanged(self, buffer):
        self._status_bar_controller.setModels(buffer.documentModel(), buffer.viewModel())
        self._side_ruler_controller.setModel(buffer.viewModel())
        self._edit_area.setModels(buffer, self._editor_model)
        self._lexer.setModel(buffer.documentModel())

