from vaitk import core, gui
from .. import Search
from .. import linting
from ..Lexer import Lexer
from ..models import Buffer
from ..models.TextDocument import LineMeta

class EditorController:
    def __init__(self, editor, global_state, buffer_list):
        self._editor = editor
        self._global_state = global_state
        self._buffer_list = buffer_list
        self._lexer = Lexer()

        self._buffer_list.currentBufferChanged.connect(self._currentBufferChanged)

    def _currentBufferChanged(self, *args):
        self._editor.edit_area.buffer = self._buffer_list.current
        self._editor.status_bar_controller.buffer = self._buffer_list.current
        self._editor.side_ruler_controller.buffer = self._buffer_list.current
        self._editor.info_hover_box.buffer = self._buffer_list.current

    def forceQuit(self):
        gui.VApplication.vApp.exit()

    def doSave(self):
        self._doSave()
        self._doLint()

    def tryQuit(self):
        if any([b.isModified() for b in self._buffer_list.buffers]):
            self._editor.status_bar.setMessage("Document has been modified. " +
                                               "Use :q! to quit without saving " +
                                               "or :qw to save and quit.", 3000)
        else:
            gui.VApplication.vApp.exit()

    def searchForward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.FORWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.FORWARD)

    def searchBackward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.BACKWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.BACKWARD)

    def selectPrevBuffer(self):
        self._buffer_list.selectPrev()

    def selectNextBuffer(self):
        self._buffer_list.selectNext()

    def doSaveAndExit(self):
        self._doSave()
        gui.VApplication.vApp.exit()

    def openFile(self, filename):
        buffer = self._buffer_list.bufferForFilename(filename)
        if buffer is not None:
            self._buffer_list.select(buffer)
            return

        current_buffer = self._buffer_list.current
        new_buffer = Buffer()
        status_bar = self._editor.status_bar

        try:
            new_buffer.document.open(filename)
        except FileNotFoundError:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [New file]" % filename, 3000)
        except Exception as e:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [Error: %s]" % (filename, str(e)), 3000)

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self._buffer_list.replaceAndSelect(current_buffer, new_buffer)
        else:
            self._buffer_list.addAndSelect(new_buffer)

        self._doLint()

    def createEmptyBuffer(self):
        self._buffer_list.addAndSelect(Buffer())

    def setMode(self, mode):
        self._global_state.edit_mode = EditMode.COMMAND

    # Private

    def _doLint(self):
        document = self._buffer_list.current.document

        linter1 = linting.PyFlakesLinter(document)
        info = linter1.runOnce()

        for line_num in range(1, document.numLines()+1):
            document.deleteLineMeta(line_num, LineMeta.LinterResult)

        for i in info:
            document.updateLineMeta(i.line, {LineMeta.LinterResult: i})

    def _doSave(self):
        status_bar = self._editor.status_bar
        document = self._buffer_list.current.document

        status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()

        try:
            document.save()
        except Exception as e:
            status_bar.setMessage("Error! Cannot save %s. %s" % (document.filename(), str(e)), 3000)
            return
        else:
            status_bar.setMessage("Saved %s" % document.filename(), 3000)

        for line_num in range(1, document.numLines()+1):
            document.deleteLineMeta(line_num, LineMeta.Change)

