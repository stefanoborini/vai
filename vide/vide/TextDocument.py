import time
from videtoolkit import gui, core, utils
import contextlib

EOL='\n'

class TextDocument(core.VObject):
    """
    Represents the contents of a file.

    Line numbers and column numbers are 1-based, which is the
    standard behavior in vim. To prevent errors, document
    positions use the DocumentPos namedtuple, instead of a
    simple tuple.
    """
    def __init__(self, filename=None):
        if filename:
            self._filename = filename
            self._contents = open(filename).readlines()
            # Always add an EOL character at the very end if not already there.
            # It appears to be a common convention in the unix world.
            if len(self._contents) > 0 and self._contents[-1][-1] != EOL:
                self._contents[-1] = self._contents[-1] + EOL
        else:
            self._contents = []
            self._filename = 'noname.txt'

        self.lineChanged = core.VSignal(self)
        self.lineDeleted = core.VSignal(self)
        self.lineCreated = core.VSignal(self)

    def isEmpty(self):
        return len(self._contents) == 0

    def getLine(self, line_number):
        self._checkLineNumber(line_number)
        return self._contents[line_number-1]

    def hasLine(self, line_number):
        try:
            self.getLine(line_number)
        except:
            return False
        return True

    def lineLength(self, line_number):
        return len(self.getLine(line_number))

    def createLineAfter(self, line_number):
        self._checkLineNumber(line_number)
        # Add an EOL if not already there
        if self._contents[line_number-1][-1] != EOL:
            self._contents[line_number-1] = self._contents[line_number-1]+EOL

        self._contents.insert(line_number, EOL)

    def createLine(self, line_number):
        self._contents.insert(line_number-1, EOL)

    def insertAt(self, document_pos, string):
        self._contents[document_pos.row-1] = self._contents[document_pos.row-1][:document_pos.column-1] + \
                                        string + \
                                        self._contents[document_pos.row-1][document_pos.column-1:]
        self.lineChanged.emit(document_pos, string, None)

    def deleteAt(self, document_pos, length):
        removed = self._contents[document_pos.row-1][document_pos.column-1:document_pos.column+length-1]
        self._contents[document_pos.row-1] = self._contents[document_pos.row-1][:document_pos.column-1] \
                                             + self._contents[document_pos.row-1][document_pos.column+length-1:]
        self.lineChanged.emit(document_pos, None, removed)

    def replaceAt(self, line_number, column, length, replace):
        removed = self._contents[line_number-1][column-1:column+length-1]
        self._contents[line_number-1] = self._contents[line_number-1][:column-1] + replace + self._contents[line_number-1][column+length-1:]
        self.lineChanged.emit(line_number, column, replace, removed)

    def breakAt(self, document_pos):
        self._contents.insert(document_pos.row, self._contents[document_pos.row-1][document_pos.column-1:])
        self._contents[document_pos.row-1] = self._contents[document_pos.row-1][:document_pos.column-1]+'\n'

        self.lineChanged.emit(document_pos, None, None)

    def joinAt(self, line_number):
        self._contents[line_number-1] = self._contents[line_number-1][:-1] + self._contents[line_number]
        self._contents.pop(line_number)
        self.lineChanged.emit(line_number, 0, None, None)

    def deleteLine(self, line_number):
        self._contents.pop(line_number-1)
        self.lineDeleted.emit(line_number)

    def filename(self):
        return self._filename

    def numLines(self):
        return len(self._contents)

    def _checkLineNumber(self, line_number):
        if line_number < 1 or line_number > len(self._contents):
            raise Exception("Out of bound request in getLine")

    def save(self):
        self.saveAs(self.filename())

    def saveAs(self, filename):
        self._filename = filename

        self._dumpContentsToFile(self._filename)

    def saveBackup(self):
        self._dumpContentsToFile(self._filename+".bak")

    def _dumpContentsToFile(self, filename):
        with contextlib.closing(open(filename,'w')) as f:
            f.write(self.text())

    def text(self):
        return "".join(self._contents)
