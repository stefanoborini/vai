import re
import time
import copy
import os
from vaitk import core
import contextlib
from .TextDocumentCursor import TextDocumentCursor

EOL='\n'
LINE_META_INDEX = 0
CHAR_META_INDEX = 1
TEXT_INDEX = 2

class DocumentMeta:
    Modified = "Modified"            # bool. If the file has been modified since its opening
    LastModified = "LastModified"    # The time when the last modification occurred
    Filename = "Filename"            # The filename
    NewFile = "NewFile"              # bool. If the TextDocument has no file on the disk yet.

class LineMeta:
    Change = "Change"
    LinterResult = "LinterResult"

class CharMeta:
    LexerToken = "LexerToken"

class TextDocument(core.VObject):
    """
    Represents the contents of a file.
    """

    class MissingFilenameException(Exception): pass

    def __init__(self):
        self._initSignals()

        self._document_meta = {}

        self._contents = [ ({}, {}, EOL) ]
        self._document_meta[DocumentMeta.Filename] = None
        self._document_meta[DocumentMeta.Modified] = False
        self._document_meta[DocumentMeta.LastModified] = time.time()
        self._cursors = []


    # Query routines
    def isEmpty(self):
        return len(self._contents) == 1 \
                and len(self._contents[0][TEXT_INDEX]) == 1 \
                and self._contents[0][TEXT_INDEX][0] == EOL

    def isLineEmpty(self, line_number):
        line_index = line_number - 1
        return len(self._contents[line_index][TEXT_INDEX]) == 1 \
                and self._contents[line_index][TEXT_INDEX][0] == EOL

    def lineText(self, line_number):
        self._checkLineNumber(line_number)
        line_index = line_number - 1
        return self._contents[line_index][TEXT_INDEX]

    def hasLine(self, line_number):
        try:
            self._checkLineNumber(line_number)
        except:
            return False
        return True

    def lineLength(self, line_number):
        return len(self.lineText(line_number))

    def documentText(self):
        return "".join([x[TEXT_INDEX] for x in self._contents])

    def filename(self):
        return self._document_meta[DocumentMeta.Filename]

    def setFilename(self, filename):
        self._document_meta[DocumentMeta.Filename] = filename

    def numLines(self):
        return len(self._contents)

    def isModified(self):
        return self._document_meta[DocumentMeta.Modified]

    ## Meta info routines
    # Document Meta

    def documentMeta(self):
        return self._document_meta

    def updateDocumentMeta(self, meta_info):
        self._document_meta.update(meta_info)

    def deleteDocumentMeta(self, keys):
        if isinstance(keys, str):
            keys = [keys]

        for k in keys:
            try:
                del self._document_meta[k]
            except KeyError:
                pass

    def lastModified(self):
        return self._document_meta[DocumentMeta.LastModified]


    # Line meta

    def lineMeta(self, line_number):
        self._checkLineNumber(line_number)
        line_index = line_number - 1
        return self._contents[line_index][LINE_META_INDEX]

    def updateLineMeta(self, line_number, meta_dict):
        self._checkLineNumber(line_number)

        line_index = line_number - 1
        self._contents[line_index][LINE_META_INDEX].update(meta_dict)
        self.contentChanged.emit()

    def updateLinesMeta(self, line_number, how_many, meta_dict):
        self._checkLineNumber(line_number)
        self._checkLineNumber(line_number+how_many)

        line_index = line_number - 1
        for i in range(line_index, line_index+how_many):
            self._contents[i][LINE_META_INDEX].update(meta_dict)

        self.contentChanged.emit()

    def deleteLineMeta(self, line_number, keys):
        self._checkLineNumber(line_number)
        line_index = line_number - 1

        if isinstance(keys, str):
            keys = [keys]

        for k in keys:
            try:
                del self._contents[line_index][LINE_META_INDEX][k]
            except KeyError:
                pass

        self.contentChanged.emit()

    # Char meta

    def charMeta(self, pos):
        self._checkPos(pos)

        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1

        how_many = char_number - self.lineLength(line_number)
        char_meta = self._contents[line_index][CHAR_META_INDEX]
        ret = {}
        for key, value in char_meta.items():
            ret[key] = value[char_index:]

        return ret

    def updateCharMeta(self, pos, meta_dict):
        self._checkPos(pos)
        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1

        char_meta = self._contents[line_index][CHAR_META_INDEX]
        text = self._contents[line_index][TEXT_INDEX]
        for key, value in meta_dict.items():
            if not key in char_meta:
                char_meta[key] = [None]*len(text)

            char_meta[key][char_index:char_index+len(value)] = value
            char_meta[key] = char_meta[key][0:len(text)]

        self.contentChanged.emit()

    def deleteCharMeta(self, pos, how_many, keys):
        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1

        char_meta = self._contents[line_index][CHAR_META_INDEX]
        for key in keys:
            try:
                meta_values = char_meta[key]
            except KeyError:
                continue
            meta_values[char_index:char_index+how_many] = None
            char_meta[key] = meta_values

        self.contentChanged.emit()

    def wordAt(self, pos, split_func=None):
        """
        find the full word at a given document position.
        Returns a tuple with the full word and the document column where the
        word starts
        """
        self._checkPos(pos)

        if split_func == None:
            split_func = re.compile("(\w+)").finditer

        line_text = self.lineText(pos[0])

        res = list(filter(lambda x: x.start() <= pos[1]-1 < x.end(), split_func(line_text)))

        if len(res) == 1:
            return (res[0].group(0), res[0].start()+1)

        return ('', None)

    ## Modify document routines
    # Line operations
    def newLineAfter(self, line_number):
        self._checkLineNumber(line_number)
        line_index = line_number - 1

        # Add an EOL if not already there
        self._contents[line_index] = ( self._contents[line_index][LINE_META_INDEX],
                                       self._contents[line_index][CHAR_META_INDEX],
                                       _withEOL(self._contents[line_index][TEXT_INDEX])
                                      )

        self._contents.insert(line_index+1, ({}, {}, EOL))
        self._setModified(True)

        self.contentChanged.emit()

    def newLine(self, line_number):
        line_index = line_number - 1
        self._contents.insert(line_index, ({}, {}, EOL))
        self._setModified(True)

        self.contentChanged.emit()

    def insertLine(self, line_number, text, line_meta=None, char_meta=None):
        if not (1 <= line_number <= self.numLines()+1):
            raise IndexError("Invalid insertion line %d" % line_number)

        line_index = line_number - 1
        line_meta = {} if line_meta is None else line_meta
        char_meta = {} if char_meta is None else char_meta
        self._contents.insert(line_index, [line_meta, char_meta, _withEOL(text)])
        self._setModified(True)
        self.contentChanged.emit()

    def insertLines(self, insert_at, text_lines):
        if not (1 <= insert_at <= self.numLines()+1):
            raise IndexError("Invalid insertion line %d" % insert_at)

        insert_at_index = insert_at - 1
        for idx, text in enumerate(text_lines):
            self._contents.insert(insert_at+idx, [{}, {}, _withEOL(text)])

        self._setModified(True)
        self.contentChanged.emit()

    def deleteLine(self, line_number):
        self._checkLineNumber(line_number)
        line_index = line_number - 1
        self._contents.pop(line_index)
        self._setModified(True)
        if len(self._contents) == 0:
            self._contents.append(({}, {}, EOL))
        self.contentChanged.emit()

    def deleteLines(self, from_line, how_many):
        self._checkLineNumber(from_line)
        self._checkLineNumber(from_line+how_many)
        from_line_index = from_line - 1
        self._contents = self._contents[:from_line_index] + self._contents[from_line_index+how_many:]

        if len(self._contents) == 0:
            self._contents.append(({}, {}, EOL))

        self._setModified(True)
        self.contentChanged.emit()

    def replaceLine(self, line_number, text, line_meta=None, char_meta=None):
        self._checkLineNumber(line_number)

        line_index = line_number - 1
        self._contents.pop(line_index)
        line_meta = {} if line_meta is None else line_meta
        char_meta = {} if char_meta is None else char_meta

        self._contents.insert(line_index, (line_meta, char_meta, _withEOL(text)))
        self._setModified(True)
        self.contentChanged.emit()

    def breakLine(self, pos):
        self._checkPos(pos)
        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1

        current_line_contents = self._contents.pop(line_index)

        orig_line_meta = current_line_contents[LINE_META_INDEX]
        orig_char_meta = current_line_contents[CHAR_META_INDEX]
        orig_text      = current_line_contents[TEXT_INDEX]

        above_char_meta = {}
        below_char_meta = {}
        for key, values in orig_char_meta.items():
           above_char_meta[key] = values[:char_index] + [None]
           below_char_meta[key] = values[char_index:]

        above_text = _withEOL(orig_text[:char_index])
        below_text = _withEOL(orig_text[char_index:])

        self._contents.insert(line_index, (dict(orig_line_meta),
                                           below_char_meta,
                                           below_text
                                          )
                            )

        self._contents.insert(line_index, (dict(orig_line_meta),
                                           above_char_meta,
                                           above_text
                                          )
                            )

        self._setModified(True)
        self.contentChanged.emit()

    def joinWithNextLine(self, line_number):
        self._checkLineNumber(line_number)

        if not self.hasLine(line_number+1):
            return

        line_index = line_number - 1

        if self.isLineEmpty(line_number):
            if not self.isEmpty():
                self._contents.pop(line_index)
                self._setModified(True)
                self.contentChanged.emit()
            return

        current_line_contents = self._contents.pop(line_index)
        current_line_meta = current_line_contents[LINE_META_INDEX]
        current_line_char_meta = current_line_contents[CHAR_META_INDEX]
        current_line_text = current_line_contents[TEXT_INDEX]

        next_line_contents = self._contents.pop(line_index)
        next_line_meta = next_line_contents[LINE_META_INDEX]
        next_line_char_meta = next_line_contents[CHAR_META_INDEX]
        next_line_text = next_line_contents[TEXT_INDEX]

        # Merge line meta. Collisions: current_line values are chosen

        new_line_meta = dict(next_line_meta)
        new_line_meta.update(current_line_meta)

        # Merge char meta. Collisions: meta will be merged.
        # [1,1] + [2,2] = [1,1,2,2]

        new_char_meta = {}
        all_keys = set(list(current_line_char_meta.keys()) + list(next_line_char_meta.keys()))
        for key in all_keys:
            current_line_char_values = current_line_char_meta.get(key)
            next_line_char_values = next_line_char_meta.get(key)
            if current_line_char_values is None:
                current_line_char_values = [None] * len(_withoutEOL(current_line_text))
            if next_line_char_values is None:
                next_line_char_values = [None] * len(_withEOL(next_line_text))

            new_char_meta[key] = current_line_char_values + next_line_char_values

        self._contents.insert(line_index, ( new_line_meta,
                                             new_char_meta,
                                             _withoutEOL(current_line_text) + _withEOL(next_line_text)
                                        )
                             )
        self._setModified(True)
        self.contentChanged.emit()

    # Char operations
    def insertChars(self, pos, string):
        self._checkPos(pos)
        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1

        contents = self._contents.pop(line_index)
        text = contents[TEXT_INDEX]

        new_text = text[:char_index] + \
                   string + \
                   text[char_index:]

        char_meta = contents[CHAR_META_INDEX]
        for key, values in char_meta.items():
            char_meta[key] = values[:char_index] + \
                             [None] * len(string) + \
                             values[char_index:]

        self._contents.insert(line_index, ( contents[LINE_META_INDEX],
                                            char_meta,
                                            new_text
                                          )
                                )

        self._setModified(True)
        self.contentChanged.emit()

    def deleteChars(self, pos, how_many):
        """
        Deletes at max how_many characters, starting and including
        position pos. The EOL is never deleted.
        Returns a tuple containing the deleted string and the character
        metainfo for that string.
        """
        self._checkPos(pos)
        if how_many < 0:
            raise ValueError("Negative how_many passed")

        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1
        line_length = self.lineLength(line_number)

        #  0 1 2 3 4 5
        # 'h e l l o \n'  line_length = 6
        #   |       |
        #   |       char_index+how_many = 5. how_many = 4
        #   char_index = 1
        if char_index+how_many > line_length-1:
            how_many = line_length-char_index-1

        contents = self._contents.pop(line_index)
        text = contents[TEXT_INDEX]
        line_meta = contents[LINE_META_INDEX]

        new_text = text[:char_index] + text[char_index+how_many:]
        deleted_text = text[char_index:char_index+how_many]

        new_eol_meta = []
        if not _hasEOL(new_text):
            new_eol_meta = [None]

        char_meta = contents[CHAR_META_INDEX]
        deleted_char_meta = {}
        for key, values in char_meta.items():
            char_meta[key] = values[:char_index] + values[char_index+how_many:] + new_eol_meta
            deleted_char_meta[key] = values[char_index:char_index+how_many]

        self._contents.insert(line_index, ( line_meta,
                                            char_meta,
                                            new_text
                                        )
                                )

        self._setModified(True)
        self.contentChanged.emit()
        return (deleted_text, deleted_char_meta)

    def replaceChars(self, pos, how_many, string):
        self._checkPos(pos)
        if how_many < 0:
            raise ValueError("Negative how_many passed")

        line_number, char_number = pos
        line_index = line_number - 1
        char_index = char_number - 1
        line_length = self.lineLength(line_number)

        #  0 1 2 3 4 5
        # 'h e l l o \n'  line_length = 6
        #   |       |
        #   |       char_index+how_many = 5. how_many = 4
        #   char_index = 1
        if char_index+how_many > line_length-1:
            how_many = line_length-char_index-1

        contents = self._contents.pop(line_index)
        text = contents[TEXT_INDEX]
        line_meta = contents[LINE_META_INDEX]

        new_text = text[:char_index] + string + text[char_index+how_many:]
        deleted_text = text[char_index:char_index+how_many]

        new_eol_meta = []
        if not _hasEOL(new_text):
            new_eol_meta = [None]

        char_meta = contents[CHAR_META_INDEX]
        deleted_char_meta = {}
        for key, values in char_meta.items():
            char_meta[key] = values[:char_index] + [None]*len(string) + values[char_index+how_many:] + new_eol_meta
            deleted_char_meta[key] = values[char_index:char_index+how_many]

        self._contents.insert(line_index, ( line_meta,
                                            char_meta,
                                            new_text
                                        )
                                )

        self._setModified(True)
        self.contentChanged.emit()
        return (deleted_text, deleted_char_meta)

    # Input Output

    def open(self, filename):
        contents = []
        with contextlib.closing(open(filename,'r')) as f:
            for textline in f:
                contents.append(({}, {}, _withEOL(textline)))

        if len(contents) == 0:
            contents.append(({}, {}, EOL))

        self._document_meta[DocumentMeta.Filename] = filename
        self._document_meta[DocumentMeta.Modified] = False
        self._document_meta[DocumentMeta.LastModified] = time.time()
        self._contents = contents
        self._cursors = []

        self.contentChanged.emit()
        self.modifiedChanged.emit(False)
        self.filenameChanged.emit(filename)

    def save(self):
        if self.filename() is None:
            raise TextDocument.MissingFilenameException()

        self.saveAs(self.filename())

    def saveAs(self, filename):
        with contextlib.closing(open(filename,'w')) as f:
            f.write(self.documentText())

        filename_changed = (self._document_meta[DocumentMeta.Filename] != filename)

        self._document_meta[DocumentMeta.Filename] = filename
        self._setModified(False)
        if filename_changed:
            self.filenameChanged.emit(filename)
        self.documentSaved.emit(filename)

    # Cursor handling
    def registerCursor(self, cursor):
        self._cursors.append(cursor)

    def createCursor(self):
        return TextDocumentCursor(self)

    def isValidLine(self, line_number):
        return (1 <= line_number <= len(self._contents))

    def isValidPos(self, pos):
        return (self.isValidLine(pos[0]) and (1 <= pos[1] <= self.lineLength(pos[0])))

    # Memento extraction for a line

    def lineMemento(self, line_number):
        return copy.deepcopy(self._contents[line_number-1])

    def insertFromMemento(self, line_number, memento):
        self._contents.insert(line_number-1, copy.deepcopy(memento))
        self.contentChanged.emit()

    def replaceFromMemento(self, line_number, memento):
        self._contents[line_number-1] = copy.deepcopy(memento)
        self.contentChanged.emit()

    # Private

    def _initSignals(self):
        self.contentChanged = core.VSignal(self)
        self.modifiedChanged = core.VSignal(self)
        self.filenameChanged = core.VSignal(self)
        self.documentSaved = core.VSignal(self)

    def _checkLineNumber(self, line_number):
        if not self.isValidLine(line_number):
            raise IndexError("Out of bound. line_number = %d, len = %d" % (line_number, len(self._contents)))

    def _checkPos(self, pos):
        if not self.isValidPos(pos):
            raise IndexError("Out of bound. pos = %s" % str(pos))

    def _setModified(self, modified):
        if modified:
            self._document_meta[DocumentMeta.LastModified] = time.time()

        if self._document_meta[DocumentMeta.Modified] != modified:
            self._document_meta[DocumentMeta.Modified] = modified
            self.modifiedChanged.emit(modified)



def _withEOL(text):
    if len(text) == 0 or text[-1] != EOL:
        return text+EOL
    return text

def _withoutEOL(text):
    if len(text) == 0 or text[-1] != EOL:
        return text
    return text[:-1]

def _hasEOL(text):
    return (len(text) != 0 and text[-1] == EOL)
