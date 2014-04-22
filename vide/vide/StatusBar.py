from videtoolkit import gui, core, utils

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super().__init__("", parent)
        self._filename = ""
        self._file_changed_flag = False
        self._position = ""
        self._message = ""

        self.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)

    def setMessage(self, message, timeout=None):
        self._message = message
        self.logger.info("Setting message: %s" % self._message)
        self._updateText()
        if timeout is not None:
            self.logger.info("Starting timer")
            core.VTimer.singleShot(timeout, self.clearMessage)

    def clearMessage(self):
        self.logger.info("Removing message")
        self._message = ""
        self._updateText()

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, document_pos):
        self._position = str(document_pos.row)+","+str(document_pos.column)
        self._updateText()

    def setFileChangedFlag(self, changed):
        self._file_changed_flag = changed
        self._updateText()

    def _updateText(self):
        self.logger.info("Updating text")
        if self._message == "":
            self.setText(utils.strformat([(0, self._filename),
                                          (len(self._filename)+1, '[+]' if self._file_changed_flag else '   '),
                                          (self.width()-len(self._position)-3, self._position)
                                         ], self.width()))
        else:
            self.setText(utils.strformat([(0, self._message)], self.width()))

