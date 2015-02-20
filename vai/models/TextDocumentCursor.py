from vaitk import core

class TextDocumentCursor(core.VObject):
    def __init__(self, text_document):
        self._text_document = text_document
        self._text_document.registerCursor(self)
        self._pos = (1,1)
        self._optimistic_column = 1

        self.positionChanged = core.VSignal(self)

    def textDocument(self):
        return self._text_document

    @property
    def pos(self):
        return self._pos

    @property
    def line(self):
        return self._pos[0]

    @property
    def column(self):
        return self._pos[1]

    # Note: not a setter, because we want to check success in a "soft" way.
    # at least for now.
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

    def isValid(self):
        return self._text_document.isValidPos(self._pos)

    def toLine(self, line_number):
        if not self.isValid():
            column = 1
        else:
            column = self.pos[1]

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

    def toCharFirstNonBlank(self):
        """Moves the cursor along the line, to the first character that is not a blank (e.g. space)."""
        if not self.isValid():
            return False

        text = self._text_document.lineText(self._pos[0])
        lstrip_text = text.lstrip()
        if len(lstrip_text) == 0:
            self._pos = (self._pos[0], 1)
        else:
            self._pos = (self._pos[0], 1 + len(text) - len(lstrip_text))
        self._optimistic_column = self._pos[1]
        self.positionChanged.emit(self._pos)
        return True

    def toCharFirstNonBlankForLine(self, line_number):
        """Moves the cursor to the first non-blank character on the specified line"""
        if not self.isValid():
            return False

        text = self._text_document.lineText(line_number)
        lstrip_text = text.lstrip()
        if len(lstrip_text) == 0:
            self._pos = (line_number, 1)
        else:
            self._pos = (line_number, 1 + len(text) - len(lstrip_text))
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

