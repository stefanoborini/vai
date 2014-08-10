from .. import flags
from .. import Search
from .. import linting
from ..Lexer import Lexer

class EditorController:
    def __init__(self, editor, editor_model):
        self._model = editor_model
        self._editor = editor
        self._lexer = Lexer()

    def forceQuit(self):
        gui.VApplication.vApp.exit()

    def doSave(self):
        self._doSave()
        self._doLint()

    def tryQuit(self):
        if any([b.isModified() for b in self._model.buffer_list.buffers]):
            self._editor.status_bar.setMessage("Document has been modified. " +
                                               "Use :q! to quit without saving " +
                                               "or :qw to save and quit.", 3000)
        else:
            gui.VApplication.vApp.exit()

    def searchForward(self, search_text):
        if search_text == '':
            if self._model.current_search is not None:
                search_text = self._model.current_search[0]

        if search_text != '':
            self._model.current_search = (search_text, flags.FORWARD)
            Search.find(self.buffer_list.current, search_text, flags.FORWARD)
            self._editor.edit_area.ensureCursorVisible()

    def searchBackward(self, search_text):
        if search_text == '':
            if self._model.current_search is not None:
                search_text = self._model.current_search[0]

        if search_text != '':
            self._model.current_search = (search_text, flags.BACKWARD)
            Search.find(self.buffer_list.current, search_text, flags.BACKWARD)
            self._editor.edit_area.ensureCursorVisible()

    def selectPrevBuffer(self):
        self._model.buffer_list.selectPrev()

    def selectNextBuffer(self):
        self._model.buffer_list.selectNext()

    def doSaveAndExit(self):
        self._doSave()
        gui.VApplication.vApp.exit()

    def openFile(self, filename):
        buffer = bufferForFilename(filename)
        if buffer is not None:
            self._model.buffer_list.select(buffer)
            return

        current_buffer = self._model.buffer_list.current
        new_buffer = Buffer()
        status_bar = self.editor.status_bar

        try:
            new_buffer.document.open(filename)
        except FileNotFoundError:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [New file]" % filename, 3000)
        except Exception as e:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [Error: %s]" % (filename, str(e)), 3000)

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self.buffer_list.replaceAndSelect(current_buffer, new_buffer)
        else:
            self.buffer_list.addAndSelect(new_buffer)

        self._doLint()

    def createEmptyBuffer(self):
        self._model.buffer_list.addAndSelect(Buffer())

    def setMode(self, mode):
        self._model.edit_mode.setMode(EditMode.COMMAND)

    # Private

    def _doLint(self):
        document = self._model.buffer_list.current.document

        linter1 = linting.PyFlakesLinter(document)
        info = linter1.runOnce()

        for line_num in range(1, document.numLines()+1):
            document.deleteLineMeta(line_num, LineMeta.LinterResult)

        for i in info:
            document.updateLineMeta(i.line, {LineMeta.LinterResult: i})

    def _doSave(self):
        status_bar = self._editor.status_bar
        document = self._model.buffer_list.current.document

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

