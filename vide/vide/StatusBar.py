from videtoolkit import gui, core, utils

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super(StatusBar,self).__init__("", parent)
        self._filename = ""
        self._file_changed_flag = False
        self._position = ""
        self.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, document_pos):
        self._position = str(document_pos.row)+","+str(document_pos.column)
        self._updateText()

    def setFileChangedFlag(self, changed):
        self._file_changed_flag = changed

    def _updateText(self):
        self.setText(utils.strformat([(0, self._filename),
                                      (len(self._filename)+1, '[+]' if self._file_changed_flag else '   '),
                                      (self.width()-len(self._position)-3, self._position)
                                     ], self.width()))

