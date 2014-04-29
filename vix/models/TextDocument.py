import time
from vixtk import gui, core, utils
import contextlib

EOL='\n'
LINE_META_INDEX = 0
CHAR_META_INDEX = 1
LINE_INDEX = 2

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
            self._contents = []
            with contextlib.closing(open(filename,'r')) as f:
                for line in f:
                    self._contents.append([{}, {}, line])

            if len(self._contents) == 0:
                self._contents.append([{}, {}, EOL])

            # Always add an EOL character at the very end if not already there.
            # It appears to be a common convention in the unix world.
            if len(self._contents) > 0 and not self._contents[-1][LINE_INDEX].endswith(EOL):
                self._contents[-1][LINE_INDEX] = self._contents[-1][LINE_INDEX] + EOL
        else:
            self._contents = [ [{}, {}, EOL] ]
            self._filename = 'noname.txt'

        self._modified = False

        self.lineChanged = core.VSignal(self)
        self.lineDeleted = core.VSignal(self)
        self.lineCreated = core.VSignal(self)
        self.contentChanged = core.VSignal(self)
        self.modifiedChanged = core.VSignal(self)
        self.filenameChanged = core.VSignal(self)
        self.lineMetaInfoChanged = core.VSignal(self)
        self.charMetaInfoChanged = core.VSignal(self)
        self.transactionFinished = core.VSignal(self)

    def enableSignals(self, enabled):
        for signal in [ self.lineChanged,
                        self.lineDeleted,
                        self.lineCreated,
                        self.modifiedChanged,
                        self.filenameChanged,
                        self.lineMetaInfoChanged,
                        self.charMetaInfoChanged,
                        self.transactionFinished,
                        self.contentChanged
                        ]:
            signal.setEnabled(enabled)

    def isEmpty(self):
        return len(self._contents) == 1 \
                and len(self._contents[0][LINE_INDEX]) == 1 \
                and self._contents[0][LINE_INDEX][0] == EOL

    def getLine(self, line_number):
        self._checkLineNumber(line_number)
        return self._contents[line_number-1][LINE_INDEX]

    def setLineMeta(self, line_number, key, value):
        self._contents[line_number-1][LINE_META_INDEX][key] = value
        self.lineMetaInfoChanged.emit(line_number, key, value)

    def lineMeta(self, line_number):
        return self._contents[line_number-1][LINE_META_INDEX]

    def charMeta(self, line_number):
        return self._contents[line_number-1][CHAR_META_INDEX]

    def setCharMeta(self, line_number, key, values):
        if len(values) != len(self._contents[line_number-1][LINE_INDEX]):
            raise Exception("Invalid length")

        self._contents[line_number-1][CHAR_META_INDEX][key] = values
        self.charMetaInfoChanged.emit(line_number, key, values)

    def beginTransaction(self):
        self.enableSignals(False)

    def endTransaction(self):
        self.enableSignals(True)
        self.transactionFinished.emit()

    def hasLine(self, line_number):
        try:
            self._checkLineNumber(line_number)
        except:
            return False
        return True

    def lineLength(self, line_number):
        return len(self.getLine(line_number))

    def createLineAfter(self, line_number):
        self._checkLineNumber(line_number)
        # Add an EOL if not already there
        if not self._contents[line_number-1][LINE_INDEX].endswith(EOL):
            self._contents[line_number-1][LINE_INDEX] = self._contents[line_number-1][LINE_INDEX]+EOL

        self._contents.insert(line_number, [{}, {}, EOL])
        self._setModified(True)

    def createLine(self, line_number):
        self._contents.insert(line_number-1, [{}, {}, EOL])
        self._setModified(True)

    def insertLine(self, line_number, text):
        if not text.endswith(EOL):
            text += EOL
        self._contents.insert(line_number-1, [{}, {}, text])
        self._setModified(True)

    def insertAt(self, document_pos, string):
        text = self._contents[document_pos.row-1][LINE_INDEX]
        self._contents[document_pos.row-1][LINE_INDEX] = text[:document_pos.column-1] + \
                                                         string + \
                                                         text[document_pos.column-1:]

        char_meta = self._contents[document_pos.row-1][CHAR_META_INDEX]
        for key, values in char_meta.items():
            char_meta[key] = values[:document_pos.column-1] + \
                             [None] * len(string) + \
                             values[document_pos.column-1:]

        self.lineChanged.emit(document_pos, string, None)
        self.contentChanged.emit()
        self._setModified(True)

    def deleteAt(self, document_pos, length):
        removed = self._contents[document_pos.row-1][LINE_INDEX][document_pos.column-1:document_pos.column+length-1]

        text = self._contents[document_pos.row-1][LINE_INDEX]
        self._contents[document_pos.row-1][LINE_INDEX] = text[:document_pos.column-1] + text[document_pos.column+length-1:]

        char_meta = self._contents[document_pos.row-1][CHAR_META_INDEX]
        for key, values in char_meta.items():
           char_meta[key] = values[:document_pos.column-1] + values[document_pos.column+length-1:]

        self.lineChanged.emit(document_pos, None, removed)
        self.contentChanged.emit()
        self._setModified(True)

#    def replaceAt(self, line_number, column, length, replace):
#        removed = self._contents[line_number-1][column-1:column+length-1]
#        self._contents[line_number-1] = self._contents[line_number-1][:column-1] + replace + self._contents[line_number-1][column+length-1:]
#        self.lineChanged.emit(line_number, column, replace, removed)
#        self._setModified(True)

    def breakAt(self, document_pos):
        self._contents.insert(document_pos.row, [dict(self._contents[document_pos.row-1][LINE_META_INDEX]),
                                                 self._contents[document_pos.row-1][CHAR_META_INDEX][document_pos.column-1:],
                                                 self._contents[document_pos.row-1][LINE_INDEX][document_pos.column-1:]
                                                ])

        char_meta = self._contents[document_pos.row-1][CHAR_META_INDEX]
        for key, values in char_meta.items():
           char_meta[key] = values[:document_pos.column-1] + [None]

        self._contents[document_pos.row-1][LINE_INDEX] = self._contents[document_pos.row-1][LINE_INDEX][:document_pos.column-1]+'\n'

        self.lineChanged.emit(document_pos, None, None)
        self.contentChanged.emit()
        self._setModified(True)

#    def joinAt(self, line_number):
#        self._contents[line_number-1] = self._contents[line_number-1][:-1] + self._contents[line_number]
#        self._contents.pop(line_number)
#        self.lineChanged.emit(line_number, 0, None, None)
#        self._setModified(True)

    def deleteLine(self, line_number):
        self._contents.pop(line_number-1)
        self.lineDeleted.emit(line_number)
        self.contentChanged.emit()
        self._setModified(True)

    def filename(self):
        return self._filename

    def numLines(self):
        return len(self._contents)

    def _checkLineNumber(self, line_number):
        if line_number < 1 or line_number > len(self._contents):
            raise Exception("Out of bound request in getLine")

    def isModified(self):
        return self._modified

    def save(self):
        self.saveAs(self.filename())

    def saveAs(self, filename):
        self._filename = filename
        self._dumpContentsToFile(self._filename)
        self._setModified(False)
        self.filenameChanged.emit(self.filename())

    def saveBackup(self):
        self._dumpContentsToFile(self._filename+".bak")

    def text(self):
        return "".join([x[LINE_INDEX] for x in self._contents])

    def _dumpContentsToFile(self, filename):
        with contextlib.closing(open(filename,'w')) as f:
            f.write(self.text())

    def _setModified(self, modified):
        if self._modified != modified:
            self._modified = modified
            self.modifiedChanged.emit(self._modified)
