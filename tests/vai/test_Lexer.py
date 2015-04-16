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

if __name__ == '__main__':
    unittest.main()
