import pygments
import pygments.lexers
import logging
from .models.TextDocument import CharMeta

class Lexer:
    def __init__(self):
        self._document = None

    def setModel(self, document):
        self._document = document

        self._document.contentChanged.connect(self._lexContents)
        self._lexContents()

    def _lexContents(self):
        # We add a space in front because otherwise the lexer will discard
        # everything up to the first token, meaning that we lose the potentially
        # empty first lines and mess up the matching. With the space, we force
        # the lexer to process the initial \n. and we just skip the space token
        tokens = list(pygments.lex(" "+self._document.documentText(), pygments.lexers.PythonLexer()))
        self._document.beginTransaction()
        current_line_num = 1
        meta = []

        # Skip the space token
        for token in tokens[1:]:
            ttype, string = token

            meta.extend([ttype]*len(string))

            if string.endswith('\n'):
                self._document.deleteCharMeta( (current_line_num,1),
                                                self._document.lineLength(current_line_num),
                                                CharMeta.LexerToken)
                self._document.updateCharMeta((current_line_num,1), {CharMeta.LexerToken: meta})
                current_line_num += 1
                meta = []

        self._document.endTransaction()
