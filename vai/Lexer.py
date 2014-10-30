import pygments
import pygments.lexers
from .SymbolLookupDb import SymbolLookupDb
from .SyncDocumentProcessor import SyncDocumentProcessor
from .models.CharMeta import CharMeta
import pygments.token

class Lexer(SyncDocumentProcessor):
    def __init__(self, document):
        super().__init__(self, document)
        self._output = CharMeta()

    def processContents(self):
        self._output.resync(self.input())

        # We add a space in front because otherwise the lexer will discard
        # everything up to the first token, meaning that we lose the potentially
        # empty first lines and mess up the matching. With the space, we force
        # the lexer to process the initial \n. and we just skip the space token
        tokens = pygments.lexers.PythonLexer(stripnl=False, stripall=False).get_tokens(self.input().documentText())
        current_line = 1
        current_col = 1
        # Skip the space token

        for token in tokens:
            ttype, token_string = token
            token_lines = token_string.splitlines(True)
            for token_line in token_lines:
                meta = [ttype]*len(token_line)

                self._output.update((current_line, current_col), meta)
                current_col += len(token_line)
                if token_line.endswith("\n"):
                    current_line += 1
                    current_col = 1

        self._output.notifyObservers()

    def output(self):
        return self._output
