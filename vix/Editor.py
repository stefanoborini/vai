from vixtk import gui, core, consts, utils

from .SideRulerController import SideRulerController
from . import widgets
from .StatusBarController import StatusBarController
from .CommandBarController import CommandBarController
from .InfoHoverBox import InfoHoverBox
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .Lexer import Lexer
from .LinterResult import LinterResult
from .PyFlakesLinter import PyFlakesLinter
from . import flags
from .models.EditAreaModel import EditAreaModel
from .models.Buffer import Buffer
from .models.BufferList import BufferList
from .models.TextDocument import TextDocument, LineMeta
from .models.EditorModel import EditorModel
import logging

class Editor(gui.VWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._editor_model = EditorModel()
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
        self._buffers.addAndSelect(Buffer(TextDocument(), EditAreaModel()))

    def buffers(self):
        return self._buffers

    def show(self):
        super().show()
        self._edit_area.setFocus()

    def openFile(self, filename):
        current_buffer = self._buffers.current()
        try:
            new_buffer = Buffer(TextDocument(filename), EditAreaModel())
        except Exception as e:
            self._status_bar.setMessage("Error: could not open file. %s" % str(e), 3000)
            return

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self._buffers.replaceAndSelect(current_buffer, new_buffer)
        else:
            self._buffers.addAndSelect(new_buffer)

        self._doLint()

    # Private

    def _createStatusBar(self):
        self._status_bar = widgets.StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)
        self._status_bar_controller = StatusBarController(self._status_bar)

    def _createCommandBar(self):
        self._command_bar = widgets.CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar_controller = CommandBarController(self._command_bar, self._editor_model)
        self._command_bar.returnPressed.connect(self._executeCommand)
        self._command_bar.escapePressed.connect(self._abortCommand)

    def _createSideRuler(self):
        self._side_ruler = widgets.SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (5, self.height()-2) )
        self._side_ruler_controller = SideRulerController(self._side_ruler)

    def _createEditArea(self):
        self._edit_area = EditArea(parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )
        self._edit_area.setFocus()

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
        self._backup_timer.timeout.connect(self._doBackup)
        self._backup_timer.start()

    def _executeCommand(self):
        command_text = self._command_bar.commandText().strip()
        logging.info("Executing command "+command_text)

        if command_text == 'q!':
            gui.VApplication.vApp.exit()
        elif command_text == 'q':
            if any([b.isModified() for b in self._buffers.buffers()]):
                self._status_bar.setMessage("Document has been modified. Use :q! to quit without saving or :qw to save and quit.", 3000)
            else:
                gui.VApplication.vApp.exit()
        elif command_text == "w":
            self._doSave()
            self._doLint()
        elif command_text == "wq":
            self._doSave()
            gui.VApplication.vApp.exit()
        elif command_text.startswith("e "):
            buffer = Buffer(TextDocument(command_text[2:]),
                                        EditAreaModel()
                                        )
            self._buffers.addAndSelect(buffer)
            self._doLint()
        elif command_text.startswith("bp"):
            self._buffers.selectPrev()
        elif command_text.startswith("bn"):
            self._buffers.selectNext()


        self._command_bar.clear()
        self._editor_model.setMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def _abortCommand(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._editor_model.setMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def _doLint(self):
        document = self.buffers().current().document()

        linter1 = PyFlakesLinter(document)
        #linter2 = Linter.PyLintLinter()
        info = linter1.runOnce() #+ linter2.lint(document)

        for i in info:
            document.updateLineMeta(i.line, {LineMeta.LinterResult: i})

    def _doSave(self):
        logging.info("Saving file")
        self._status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()
        self._buffers.current().document().save()
        self._status_bar.setMessage("Saved %s" % self._buffers.current().document().filename(), 3000)

    def _doBackup(self):
        logging.info("Saving backup file")
        #self._status_bar.setMessage("Saving backup...")
        #gui.VApplication.vApp.processEvents()

        #self._current_document.saveBackup()
        #self._status_bar.setTemporaryMessage("Backup saved", 3000)

    def _showInfoHoverBoxIfNeeded(self, document_pos):
        badge = self._side_ruler.badge(document_pos[0])
        if badge is not None:
            self._status_bar.setMessage(badge.description, 3000)
            #self._info_hover_box.resize((1,len(badge.description)))
            #self._info_hover_box.move((0, self._edit_area.visualCursorPos()[1]+1))
            #self._info_hover_box.show()
        else:
            self._status_bar.setMessage(None)
            #self._info_hover_box.hide()


    def _bufferChanged(self, old_buffer, new_buffer):
        self._status_bar_controller.setModels(new_buffer.document(), new_buffer.documentCursor())
        self._side_ruler_controller.setModel(new_buffer.document(),new_buffer.editAreaModel())
        self._edit_area.setModels(new_buffer, self._editor_model)
        if old_buffer:
            old_buffer.documentCursor().positionChanged.disconnect(self._showInfoHoverBoxIfNeeded)
        new_buffer.documentCursor().positionChanged.connect(self._showInfoHoverBoxIfNeeded)
        self._lexer.setModel(new_buffer.document())

