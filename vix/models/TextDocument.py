import time
from vixtk import gui, core, utils
import contextlib
from .TextDocumentCursor import TextDocumentCursor

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
        self._cursors = []

        self.lineChanged = core.VSignal(self)
        self.lineDeleted = core.VSignal(self)
        self.lineCreated = core.VSignal(self)
        self.contentChanged = core.VSignal(self)
        self.modifiedChanged = core.VSignal(self)
        self.filenameChanged = core.VSignal(self)
        self.lineMetaInfoChanged = core.VSignal(self)
        self.charMetaInfoChanged = core.VSignal(self)
        self.transactionFinished = core.VSignal(self)

    def createCursor(self):
        return TextDocumentCursor(self)

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

    def updateLineMeta(self, line_number, meta_dict):
        self._contents[line_number-1][LINE_META_INDEX].update(meta_dict)
        self.lineMetaInfoChanged.emit(line_number, meta_dict)

    def lineMeta(self, line_number):
        return self._contents[line_number-1][LINE_META_INDEX]

    def updateCharMeta(self, line_number, meta_dict):
        for values in meta_dict.values():
            if len(values) != len(self._contents[line_number-1][LINE_INDEX]):
                raise Exception("Invalid length")

        self._contents[line_number-1][CHAR_META_INDEX].update(meta_dict)
        self.charMetaInfoChanged.emit(line_number, meta_dict)

    def charMeta(self, line_number):
        return self._contents[line_number-1][CHAR_META_INDEX]

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

    def newLineAfter(self, line_number):
        self._checkLineNumber(line_number)
        # Add an EOL if not already there
        if not self._contents[line_number-1][LINE_INDEX].endswith(EOL):
            self._contents[line_number-1][LINE_INDEX] = self._contents[line_number-1][LINE_INDEX]+EOL

        self._contents.insert(line_number, [{}, {}, EOL])
        self._setModified(True)

    def newLine(self, line_number):
        self._contents.insert(line_number-1, [{}, {}, EOL])
        self._setModified(True)

    def insertLine(self, line_number, text):
        if not text.endswith(EOL):
            text += EOL
        self._contents.insert(line_number-1, [{}, {}, text])
        self._setModified(True)

    def insert(self, document_pos, string):
        text = self._contents[document_pos[0]-1][LINE_INDEX]
        self._contents[document_pos[0]-1][LINE_INDEX] = text[:document_pos[1]-1] + \
                                                         string + \
                                                         text[document_pos[1]-1:]

        char_meta = self._contents[document_pos[0]-1][CHAR_META_INDEX]
        for key, values in char_meta.items():
            char_meta[key] = values[:document_pos[1]-1] + \
                             [None] * len(string) + \
                             values[document_pos[1]-1:]

        self.lineChanged.emit(document_pos, string, None)
        self.contentChanged.emit()
        self._setModified(True)

    def delete(self, document_pos, length):
        removed = self._contents[document_pos[0]-1][LINE_INDEX][document_pos[1]-1:document_pos[1]+length-1]

        text = self._contents[document_pos[0]-1][LINE_INDEX]
        self._contents[document_pos[0]-1][LINE_INDEX] = text[:document_pos[1]-1] + text[document_pos[1]+length-1:]

        char_meta = self._contents[document_pos[0]-1][CHAR_META_INDEX]
        for key, values in char_meta.items():
           char_meta[key] = values[:document_pos[1]-1] + values[document_pos[1]+length-1:]

        self.lineChanged.emit(document_pos, None, removed)
        self.contentChanged.emit()
        self._setModified(True)

#    def replace(self, line_number, column, length, replace):
#        removed = self._contents[line_number-1][column-1:column+length-1]
#        self._contents[line_number-1] = self._contents[line_number-1][:column-1] + replace + self._contents[line_number-1][column+length-1:]
#        self.lineChanged.emit(line_number, column, replace, removed)
#        self._setModified(True)

    def breakLine(self, document_pos):
        current_line_contents = self._contents[document_pos[0]-1]

        char_meta = current_line_contents[CHAR_META_INDEX]
        newline_char_meta = {}
        oldline_char_meta = {}
        for key, values in char_meta.items():
           oldline_char_meta[key] = values[:document_pos[1]-1] + [None]
           newline_char_meta[key] = values[document_pos[1]-1:]

        self._contents.insert(document_pos[0], [dict(current_line_contents[LINE_META_INDEX]),
                                                 newline_char_meta,
                                                 current_line_contents[LINE_INDEX][document_pos[1]-1:]
                                                ])

        self._contents[document_pos[0]-1] = [ dict(current_line_contents[LINE_META_INDEX]),
                                                oldline_char_meta,
                                                current_line_contents[LINE_INDEX][:document_pos[1]-1]+'\n'
                                            ]

        self.lineChanged.emit(document_pos, None, None)
        self.contentChanged.emit()
        self._setModified(True)

    def joinWithNextLine(self, line_number):
        if not self.hasLine(line_number+1):
            return

        if len(self._contents[line_number][LINE_INDEX].strip()) == 0:
            self._contents.pop(line_number)
            self.contentChanged.emit()
            self._setModified(True)
            return

        current_line_contents = self._contents[line_number-1]
        next_line_contents = self._contents[line_number]
        current_line_char_meta = current_line_contents[CHAR_META_INDEX]
        next_line_char_meta = next_line_contents[CHAR_META_INDEX]

        new_char_meta = {}
        all_keys = set(list(current_line_char_meta.keys()) + list(next_line_char_meta.keys()))
        for key in all_keys:
            current_line_values = current_line_char_meta.get(key)
            next_line_values = next_line_char_meta.get(key)
            if current_line_values is None:
                current_line_values = [None] * len(current_line_contents[LINE_INDEX])
            if next_line_values is None:
                next_line_values = [None] * len(next_line_contents[LINE_INDEX].strip())

            new_char_meta[key] = current_line_values + next_line_values

        new_line_meta = next_line_contents[LINE_META_INDEX]
        new_char_meta.update(current_line_contents[LINE_META_INDEX])

        self._contents[line_number-1] = [
                                          new_line_meta,
                                          new_char_meta,
                                          current_line_contents[LINE_INDEX][:-1]+" "+next_line_contents[LINE_INDEX].lstrip()
                                        ]
        self._contents.pop(line_number)
        self.contentChanged.emit()
        self._setModified(True)

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
            raise IndexError("Out of bound. line_number = %d, len = %d" % (line_number, len(self._contents)))

    def isModified(self):
        return self._modified

    def save(self):
        self.saveAs(self.filename())

    def saveAs(self, filename):
        self._filename = filename

        with contextlib.closing(open(filename,'w')) as f:
            f.write(self.text())

        self._setModified(False)
        self.filenameChanged.emit(self.filename())

    def text(self):
        return "".join([x[LINE_INDEX] for x in self._contents])

    def _setModified(self, modified):
        if self._modified != modified:
            self._modified = modified
            self.modifiedChanged.emit(self._modified)

    def registerCursor(self, cursor):
        self._cursors.append(cursor)
