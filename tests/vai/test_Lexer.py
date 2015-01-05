import unittest
from vai import Lexer
from vai.models import TextDocument
from pygments import token
from tests import fixtures

class LexerTest(unittest.TestCase):
    def testBug58(self):
        document = TextDocument()
        document.open(fixtures.get("bug_58.py"))
        lexer = Lexer.Lexer()
        lexer.setModel(document)
        self.assertEqual(document.charMeta((1,1))["LexerToken"][0], token.Token.Keyword)

    def testBug69(self):
        document = TextDocument()
        document.open(fixtures.get("bug_69.py"))
        lexer = Lexer.Lexer()
        lexer.setModel(document)
        self.assertEqual(document.charMeta((1,1))["LexerToken"][0], token.Token.Text)

if __name__ == '__main__':
    unittest.main()
