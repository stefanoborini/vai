from vaitk import gui, core
import os

from . import widgets
from .SideRulerController import SideRulerController
from .StatusBarController import StatusBarController
from .CommandBarController import CommandBarController
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .Lexer import Lexer
from .PyFlakesLinter import PyFlakesLinter
from . import flags
from . import Search
from .models.Buffer import Buffer
from .models.BufferList import BufferList
from .models.TextDocument import LineMeta
from .models.EditorModel import EditorModel
import logging

class Editor(gui.VWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._editor_model = EditorModel()
        self._lexer = Lexer()
        self._buffer_list = BufferList()

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()

        self._initBackupTimer()

        self._editor_model.mode = flags.COMMAND_MODE
        self._edit_area.setFocus()

        self._buffer_list.currentBufferChanged.connect(self._bufferChanged)
        self._buffer_list.addAndSelect(Buffer())

    @property
    def buffer_list(self):
        return self._buffer_list

    def show(self):
        super().show()
        self._edit_area.setFocus()

    def openFile(self, filename):
        if os.path.exists(filename) and os.path.isfile(filename):
            for buffer in self.buffer_list.buffers:
                if buffer.document.filename() is None:
                    continue

                if os.path.samefile( os.path.abspath(os.path.realpath(buffer.document.filename())),
                    filename):

                    self.buffer_list.select(buffer)
                    return

        current_buffer = self.buffer_list.current
        new_buffer = Buffer()

        try:
            new_buffer.document.open(filename)
        except FileNotFoundError:
            new_buffer.document.setFilename(filename)
            self._status_bar.setMessage("%s [New file]" % filename, 3000)
        except Exception as e:
            new_buffer.document.setFilename(filename)
            self._status_bar.setMessage("%s [Error: %s]" % (filename, str(e)), 3000)

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self.buffer_list.replaceAndSelect(current_buffer, new_buffer)
        else:
            self.buffer_list.addAndSelect(new_buffer)

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
        self._command_bar.returnPressed.connect(self._parseCommandBar)
        self._command_bar.escapePressed.connect(self._abortCommandBar)

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
        self._edit_area_event_filter.setModels(self._editor_model, self.buffer_list)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

    def _initBackupTimer(self):
        self._backup_timer = core.VTimer()
        self._backup_timer.setInterval(60*1000)
        self._backup_timer.setSingleShot(False)
        self._backup_timer.timeout.connect(self._doBackup)
        self._backup_timer.start()

    def _parseCommandBar(self):
        command_text = self._command_bar.commandText().strip()
        mode = self._editor_model.mode

        if mode == flags.COMMAND_INPUT_MODE:
            if command_text == 'q!':
                gui.VApplication.vApp.exit()
            elif command_text == 'q':
                if any([b.isModified() for b in self.buffer_list.buffers]):
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
                self.openFile(command_text[2:])
            elif command_text.startswith("bp"):
                self.buffer_list.selectPrev()
            elif command_text.startswith("bn"):
                self.buffer_list.selectNext()
        elif mode == flags.SEARCH_FORWARD_MODE:
            if command_text == '':
                if self._editor_model.current_search is not None:
                    command_text = self._editor_model.current_search[0]

            if command_text != '':
                self._editor_model.current_search = (command_text, flags.FORWARD)
                Search.find(self.buffer_list.current, command_text, flags.FORWARD)
                self._edit_area.ensureCursorVisible()
        elif mode == flags.SEARCH_BACKWARD_MODE:
            if command_text == '':
                if self._editor_model.current_search is not None:
                    command_text = self._editor_model.current_search[0]

            if command_text != '':
                self._editor_model.current_search = (command_text, flags.BACKWARD)
                Search.find(self.buffer_list.current, command_text, flags.BACKWARD)
                self._edit_area.ensureCursorVisible()

        self._command_bar.clear()
        self._editor_model.mode = flags.COMMAND_MODE
        self._edit_area.setFocus()

    def _abortCommandBar(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._editor_model.mode = flags.COMMAND_MODE
        self._edit_area.setFocus()

    def _doLint(self):
        document = self.buffer_list.current.document

        linter1 = PyFlakesLinter(document)
        #linter2 = Linter.PyLintLinter()
        info = linter1.runOnce() #+ linter2.lint(document)

        for i in info:
            document.updateLineMeta(i.line, {LineMeta.LinterResult: i})

    def _doSave(self):
        logging.info("Saving file")
        self._status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()
        document = self.buffer_list.current.document

        try:
            document.save()
            self._status_bar.setMessage("Saved %s" % document.filename(), 3000)
        except Exception as e:
            self._status_bar.setMessage("Error! Cannot save %s. %s" % (document.filename(), str(e)), 3000)
            return


        for line_num in range(1, document.numLines()+1):
            document.deleteLineMeta(line_num, LineMeta.Change)

    def _doBackup(self):
        logging.info("Saving backup file")
        #self._status_bar.setMessage("Saving backup...")
        #gui.VApplication.vApp.processEvents()

        #self._current_document.saveBackup()
        #self._status_bar.setTemporaryMessage("Backup saved", 3000)

    def _showInfoHoverBoxIfNeeded(self, document_pos):
        current_buffer = self.buffer_list.current
        pos_at_top = current_buffer.edit_area_model.document_pos_at_top

        badge = self._side_ruler.badge(document_pos[0])

        if badge is not None:
            gui.VToolTip.showText((0, document_pos[0]-pos_at_top[0]+1), badge.description)
        else:
            gui.VToolTip.hide()


    def _bufferChanged(self, old_buffer, new_buffer):
        self._status_bar_controller.setModels(new_buffer.document, new_buffer.cursor)
        self._side_ruler_controller.setModels(new_buffer.document, new_buffer.edit_area_model)
        self._edit_area.setModels(new_buffer, self._editor_model)
        if old_buffer:
            old_buffer.cursor.positionChanged.disconnect(self._showInfoHoverBoxIfNeeded)
        new_buffer.cursor.positionChanged.connect(self._showInfoHoverBoxIfNeeded)
        self._lexer.setModel(new_buffer.document)

