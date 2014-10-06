import pygments
import pygments.lexers
from .SymbolLookupDb import SymbolLookupDb
from .models.TextDocument import CharMeta
import pygments.token

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
        import time
        start = time.time()
        tokens = pygments.lexers.PythonLexer(stripnl=False, stripall=False).get_tokens(self._document.documentText())
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

