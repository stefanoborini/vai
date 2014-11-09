import pygments
import pygments.lexers
from .SymbolLookupDb import SymbolLookupDb
from .models.TextDocument import CharMeta
import pygments.token
from pygments import lexers, util

class Lexer:
    def __init__(self):
        self._document = None
        self._lexer = None

    def setModel(self, document):
        self._document = document
        filename = self._document.filename()
        if filename is None:
            self._lexer = None
        else:
            try:
                self._lexer = lexers.get_lexer_for_filename(self._document.filename(), stripnl=False, stripall=False)
            except util.ClassNotFound:
                self._lexer = None

        self._document.contentChanged.connect(self._lexContents)
        self._lexContents()

    def _lexContents(self):

        if self._lexer is None:
            return

        # We add a space in front because otherwise the lexer will discard
        # everything up to the first token, meaning that we lose the potentially
        # empty first lines and mess up the matching. With the space, we force
        # the lexer to process the initial \n. and we just skip the space token
        tokens = self._lexer.get_tokens(self._document.documentText())
        current_line = 1
        current_col = 1
        SymbolLookupDb.clear()
        # Skip the space token

        for token in tokens:
            ttype, token_string = token
            if ttype in [pygments.token.Name, pygments.token.Name.Class, pygments.token.Name.Function]:
                SymbolLookupDb.add(token_string)

            token_lines = token_string.splitlines(True)
            for token_line in token_lines:
                meta = [ttype]*len(token_line)

                self._document.updateCharMeta((current_line, current_col), {CharMeta.LexerToken: meta})
                current_col += len(token_line)
                if token_line.endswith("\n"):
                    current_line += 1
                    current_col = 1

