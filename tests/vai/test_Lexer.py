import unittest
from vai.lexer import Lexer
from vai.models import TextDocument
from pygments import token
from tests import fixtures

class LexerTest(unittest.TestCase):
    def testBug58(self):
        document = fixtures.buffer("bug_58.py").document
        lexer = Lexer()
        lexer.setModel(document)
        self.assertEqual(document.charMeta((1,1))["LexerToken"][0], token.Token.Keyword)

    def testBug69(self):
        document = fixtures.buffer("bug_69.py").document
        lexer = Lexer()
        lexer.setModel(document)
        self.assertEqual(document.charMeta((1,1))["LexerToken"][0], token.Token.Text)

    def testTokenMetadataCoversEveryLine(self):
        document = fixtures.buffer("bug_58.py").document
        lexer = Lexer()
        lexer.setModel(document)

        for line_number in range(1, document.numLines() + 1):
            metadata = document.charMeta((line_number, 1))["LexerToken"]
            self.assertEqual(len(metadata), document.lineLength(line_number))

if __name__ == '__main__':
    unittest.main()
