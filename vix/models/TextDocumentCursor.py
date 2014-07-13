from vixtk import core

class TextDocumentCursor(core.VObject):
    def __init__(self, text_document):
        self._text_document = text_document
        self._text_document.registerCursor(self)
        self._pos = (1,1)
        self._optimistic_column = 1

        self.positionChanged = core.VSignal(self)

    def textDocument(self):
        return self._text_document

    def lineText(self):
        return self._text_document.lineText(self._pos[0])

    def pos(self):
        return self._pos

    def isValid(self):
        return self._text_document.isValidPos(self._pos)

    def toPos(self, pos):
        """
        Move to a specific position if possible. Return True if the
        movement succeeds. If the movement is not possible,
        the position will be unchanged and it will return False.
        """
        if not self._text_document.isValidPos(pos):
            return False

        self._pos = pos
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toLine(self, line_number):
        if not self.isValid():
            column = 1
        else:
            column = self.pos()[1]

        if not self._text_document.isValidLine(line_number):
            return False

        self._pos = (line_number, min(self._text_document.lineLength(line_number), column))
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toLineNext(self):
        next_line_number = self._pos[0]+1
        if not self._text_document.hasLine(next_line_number):
            return False

        self._pos = (next_line_number,
                     min(
                         self._text_document.lineLength(next_line_number),
                         max(self._pos[1],
                             self._optimistic_column
                        )
                      )
                    )
        self.positionChanged.emit(self._pos)
        return True

    def toLinePrev(self):
        prev_line_number = self._pos[0]-1
        if not self._text_document.hasLine(prev_line_number):
            return False

        self._pos = (prev_line_number,
                     min(
                         self._text_document.lineLength(prev_line_number),
                         max(self._pos[1],
                             self._optimistic_column
                         )
                     )
                   )
        self.positionChanged.emit(self._pos)
        return True

    def toCharNext(self):
        line_number = self._pos[0]
        next_char_number = self._pos[1]+1
        next_pos = (line_number, next_char_number)
        if not self._text_document.isValidPos(next_pos):
            return False

        self._pos = next_pos
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toCharPrev(self):
        line_number = self._pos[0]
        prev_char_number = self._pos[1]-1
        prev_pos = (line_number, prev_char_number)

        if not self._text_document.isValidPos(prev_pos):
            return False

        self._pos = prev_pos
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toLineBeginning(self):
        if not self.isValid():
            return False

        self._pos = (self._pos[0], 1)
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toLineEnd(self):
        if not self.isValid():
            return False

        self._pos = (self._pos[0], self._text_document.lineLength(self._pos[0]))
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toFirstLine(self):
        self._pos = (1,1)
        self._optimistic_column = 0
        self.positionChanged.emit(self._pos)
        return True

    def toLastLine(self):
        self._pos = (self._text_document.numLines(), 1)
        self._optimistic_column = 0
        self.positionChanged.emit(self._pos)
        return True

    def lineLength(self):
        return self._text_document.lineLength(self._pos[0])

    def updateLineMeta(self, meta_dict):
        self._text_document.updateLineMeta(self._pos[0], meta_dict)

    def lineMeta(self):
        return self._text_document.lineMeta(self._pos[0])

    def updateCharMeta(self, line_number, meta_dict): pass
    def charMeta(self): pass

    def newLineAfter(self):
        if not self.isValid():
            return False
        self._text_document.newLineAfter(self._pos[0])

    def newLine(self):
        if not self.isValid():
            return False
        self._text_document.newLine(self._pos[0])
        return True

    def deleteLine(self):
        if not self.isValid():
            return False
        current_line = self._pos[0]
        if current_line == self._text_document.numLines():
            self.toLinePrev()
        self._text_document.deleteLine(current_line)
        return True

    def insertSingleChar(self, char):
        if not self.isValid():
            return False
        self._text_document.insertChars(self._pos, char)
        self.toCharNext()
        return True

    def deleteSingleChar(self):
        if self.toCharPrev():
            deleted = self._text_document.deleteChars(self._pos, 1)
            return deleted
        return None

    def deleteSingleCharAfter(self):
        if not self.isValid():
            return None

        current_column = self._pos[1]
        if current_column == self._text_document.lineLength(self._pos[0]):
            if self.toCharPrev():
                deleted = self._text_document.deleteChars( (self._pos[0], current_column), 1)
            else:
                deleted = None
        else:
            deleted = self._text_document.deleteChars( (self._pos[0], current_column), 1)

        return deleted

    def replace(self, length, replace):
        pass

    def breakLine(self):
        if not self.isValid():
            return False

        self._text_document.breakLine(self._pos)
        self._pos = (self._pos[0]+1, 1)
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def joinWithNextLine(self):
        if not self.isValid():
            return False
        self._text_document.joinWithNextLine(self._pos[0])
        return True

