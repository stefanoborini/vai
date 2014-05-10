import pygments
import pygments.lexers
import logging
class Lexer:
    def __init__(self):
        self._document_model = None

    def setModel(self, document_model):
        self._document_model = document_model

        self._document_model.contentChanged.connect(self._lexContents)
        self._lexContents()

    def _lexContents(self):
        tokens = pygments.lex(self._document_model.text(), pygments.lexers.PythonLexer())
        self._document_model.beginTransaction()
        current_line_num = 1
        meta = []
        for token in tokens:
            ttype, string = token

            meta.extend([ttype]*len(string))

            if string.endswith('\n'):
                self._document_model.updateCharMeta(current_line_num, {"lextoken": meta})
                current_line_num += 1
                meta = []

        self._document_model.endTransaction()
