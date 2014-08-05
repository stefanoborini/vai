class EditorController:
    def __init__(self, editor, editor_model, buffer_list):
        self._editor_model = editor_model
        self._editor = editor
        self._buffer_list = buffer_list
        self._lexer = Lexer()

    def forceQuit(self):
        gui.VApplication.vApp.exit()

    def doSave(self):
        self._doSave()
        self._doLint()

    def tryQuit(self):
        if any([b.isModified() for b in self.buffer_list.buffers]):
            self._editor.status_bar.setMessage("Document has been modified. " +
                                               "Use :q! to quit without saving " +
                                               "or :qw to save and quit.", 3000)
        else:
            gui.VApplication.vApp.exit()

    def searchForward(self, search_text):
        if search_text == '':
            if self._editor_model.current_search is not None:
                search_text = self._editor_model.current_search[0]

        if search_text != '':
            self._editor_model.current_search = (search_text, flags.FORWARD)
            Search.find(self.buffer_list.current, search_text, flags.FORWARD)
            self._editor.edit_area.ensureCursorVisible()

    def searchBackward(self, search_text)
        if search_text == '':
            if self._editor_model.current_search is not None:
                search_text = self._editor_model.current_search[0]

        if search_text != '':
            self._editor_model.current_search = (search_text, flags.BACKWARD)
            Search.find(self.buffer_list.current, search_text, flags.BACKWARD)
            self._edit_area.ensureCursorVisible()

    def selectPrevBuffer(self):
        self.buffer_list.selectPrev()

    def selectNextBuffer(self):
        self.buffer_list.selectNext()

    def doSaveAndExit(self):
        self._doSave()
        gui.VApplication.vApp.exit()

    def _doLint(self):
        document = self.buffer_list.current.document

        linter1 = PyFlakesLinter(document)
        #linter2 = Linter.PyLintLinter()
        info = linter1.runOnce() #+ linter2.lint(document)

        for i in info:
            document.updateLineMeta(i.line, {LineMeta.LinterResult: i})

    def _doSave(self):
        status_bar = self._editor.status_bar
        status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()

        document = self.buffer_list.current.document

        try:
            document.save()
        except Exception as e:
            status_bar.setMessage("Error! Cannot save %s. %s" % (document.filename(), str(e)), 3000)
            return
        else:
            status_bar.setMessage("Saved %s" % document.filename(), 3000)

        for line_num in range(1, document.numLines()+1):
            document.deleteLineMeta(line_num, LineMeta.Change)

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
        self._buffer_list.addAndSelect(Buffer())

    def setMode(self, mode):
        self._editor_model.mode = flags.COMMAND_MODE
