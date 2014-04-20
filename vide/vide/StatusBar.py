from videtoolkit import gui, core, utils
import logging

class StatusBar(gui.VLabel):
    debug=logging.INFO
    def __init__(self, parent):
        super(StatusBar,self).__init__("", parent)
        self._filename = ""
        self._file_changed_flag = False
        self._position = ""
        self._temporary_message = ""

        self.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)

    def setTemporaryMessage(self, message, timeout=None):
        self._temporary_message = message
        self.logger.info("Setting temporary message: %s" % self._temporary_message)
        self._updateText()
        if timeout is not None:
            self.logger.info("Starting timer")
            core.VTimer.singleShot(timeout, self.removeTemporaryMessage)

    def removeTemporaryMessage(self):
        self.logger.info("Removing temporary message")
        self._temporary_message = ""
        self._updateText()

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, document_pos):
        self._position = str(document_pos.row)+","+str(document_pos.column)
        self._updateText()

    def setFileChangedFlag(self, changed):
        self._file_changed_flag = changed

    def _updateText(self):
        self.logger.info("Updating text")
        if self._temporary_message == "":
            self.setText(utils.strformat([(0, self._filename),
                                          (len(self._filename)+1, '[+]' if self._file_changed_flag else '   '),
                                          (self.width()-len(self._position)-3, self._position)
                                         ], self.width()))
        else:
            self.logger.info("Temporary message: %s" % self._temporary_message)
            self.setText(utils.strformat([(1, self._temporary_message)], self.width()))

