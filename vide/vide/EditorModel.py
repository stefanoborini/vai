from videtoolkit import gui, core, utils

class EditorModel(core.VObject):
    def __init__(self, filename=None):
        if filename:
            self._contents = open(filename).read().splitlines()
            self._filename = filename
        else:
            self._contents = []
            self._filename = 'noname.txt'

        self.lineChanged = core.VSignal(self)
        self.lineDeleted = core.VSignal(self)
        self.lineCreated = core.VSignal(self)

    def isEmpty(self):
        return len(self._contents) == 0

    def getLine(self, line_number):
        return self._contents[line_number]

    def hasLine(self, line_number):
        try:
            self._contents[line_number]
        except:
            return False
        return True

    def lineLength(self, line_number):
        return len(self._contents[line_number])

    def createLineAfter(self, line_number):
        self._contents.insert(line_number+1,'')

    def createLineBefore(self, line_number):
        self._contents.insert(line_number,'')

    def insertAt(self, line_number, column, string):
        self._contents[line_number] = self._contents[line_number][:column] + \
                                      string + \
                                      self._contents[line_number][column:]
        self.lineChanged.emit(line_number, column, string, None)

    def deleteAt(self, line_number, column, length):
        removed = self._contents[line_number][column:column+length]
        self._contents[line_number] = self._contents[line_number][:column] + self._contents[line_number][column+length:]
        self.lineChanged.emit(line_number, column, None, removed)

    def replaceAt(self, line_number, column, length, replace):
        removed = self._contents[line_number][column:column+length]
        self._contents[line_number] = self._contents[line_number][:column] + replace + self._contents[line_number][column+length:]
        self.lineChanged.emit(line_number, column, replace, removed)

    def deleteLine(self, line_number):
        self._contents.pop(line_number)
        self.lineDeleted.emit(line_number)

    def filename(self):
        return self._filename

    def numLines(self):
        return len(self._contents)

