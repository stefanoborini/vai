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
        current_line = 1
        current_col = 1

        # Skip the space token
        for token in tokens[1:]:
            ttype, token_string = token

            token_lines = token_string.splitlines(True)
            for token_line in token_lines:
                meta = [ttype]*len(token_line)

                self._document.updateCharMeta((current_line, current_col), {CharMeta.LexerToken: meta})
                current_col += len(token_line)
                if token_line.endswith("\n"):
                    current_line += 1
                    current_col = 1

        self._document.endTransaction()
