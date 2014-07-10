import pygments
import pygments.lexers
import logging

class Lexer:
    def __init__(self):
        self._document = None

    def setModel(self, document):
        self._document = document

        self._document.contentChanged.connect(self._lexContents)
        self._lexContents()

    def _lexContents(self):
        tokens = pygments.lex(self._document.documentText(), pygments.lexers.PythonLexer())
        self._document.beginTransaction()
        current_line_num = 1
        meta = []
        for token in tokens:
            ttype, string = token

            meta.extend([ttype]*len(string))

            if string.endswith('\n'):
                self._document.updateCharMeta((current_line_num,1), {"lextoken": meta})
                current_line_num += 1
                meta = []

        self._document.endTransaction()
