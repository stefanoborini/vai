from vixtk import core

class TextDocumentCursor(core.VObject):
    def __init__(self, text_document):
        self._text_document = text_document
        self._pos = (1,1)
        self._optimistic_column = 1

    def currentLine(self):
        return self._text_document.getLine(self._pos[0])

    def pos(self):
        return self._pos

    def moveTo(self, line, column):
        if line < 1 or line > self._text_document.numLines() or column < 1:
            return False

        self._pos = (line, min(self._text_document.lineLength(line), column))
        self._optimistic_column = self._pos[1]
        return True

    def toLineNext():
        if self._pos[0] >= self._text_document.numLines():
            return False
        self._pos = (self._pos[0]+1,
                                    min(
                                        self._text_document.lineLength(self._pos[0]),
                                        max(self._pos[1],
                                            self._optimistic_column
                                           )
                                        )
                    )
        return True

    def toLinePrev():
        if self._pos[0] == 1:
            return False

        self._pos = (self._pos[0]-1,
                                    min(
                                        self._text_document.lineLength(self._pos[0]),
                                        max(self._pos[1],
                                            self._optimistic_column
                                           )
                                        )
                    )
        return True

    def toCharNext():
        if self._pos[1] == self._text_document.lineLength(self._pos[0]):
            return False

        self._pos = (self._pos[0], self._pos[1]+1)
        self._optimistic_column = self._pos[1]
        return True

    def toCharPrev():
        if self._pos[1] == 1:
            return False

        self._pos = (self._pos[0], self._pos[1]-1)
        self._optimistic_column = self._pos[1]
        return True

    def toLineBeginning():
        self._pos = (self._pos[0], 1)
        self._optimistic_column = self._pos[1]
        return True

    def toLineEnd():
        self._pos = (self._pos[0], self._text_document.lineLength(self._pos[0]))
        self._optimistic_column = self._pos[1]
        return True

    def toFirstLine():
        self._pos = (1,1)
        self._optimistic_column = self._pos[1]
        return True

    def toLastLine():
        self._pos = (self._text_document.numLines(), 1)
        self._optimistic_column = self._pos[1]
        return True

    def lineLength(self):
        return self._text_document.lineLength(self._pos[0])

    def setLineMeta(self, key, value): pass
    def lineMeta(self): pass
    def setCharMeta(self, line_number, key, values): pass
    def charMeta(self): pass

    def newLineAfter(self): pass
    def newLine(self): pass
    def insertLine(self, string): pass
    def deleteLine(self): pass
    def insert(self, string): pass
    def delete(self, length): pass
    def replace(self, length, replace): pass
    def breakLine(self): pass
    def joinWithPrevLine(self): pass
    def joinWithNextLine(self): pass
