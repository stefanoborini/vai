from vixtk import gui, core, utils

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super().__init__("", parent)
        self._filename = ""
        self._file_changed_flag = False
        self._position = ""
        self._message = ""
        self._remove_message_timer = core.VTimer()
        self._remove_message_timer.setSingleShot(True)
        self._remove_message_timer.timeout.connect(self.clearMessage)

    def setMessage(self, message, timeout=None):

        if self._remove_message_timer.isRunning():
            self._remove_message_timer.stop()

        if message is None:
            self.clearMessage()
            return

        self._message = message
        self.logger.info("Setting message: %s" % self._message)
        self._updateText()

        if timeout is not None:
            self.logger.info("Starting timer")
            self._remove_message_timer.setInterval(timeout)
            self._remove_message_timer.start()

    def clearMessage(self):
        self.logger.info("Removing message")
        self._message = ""
        self._updateText()

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, pos):
        self._position = str(pos[0])+","+str(pos[1])
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

