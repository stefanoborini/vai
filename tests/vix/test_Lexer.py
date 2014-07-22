import unittest
import os
import inspect
import sys
from vixtk import test, gui, core
from vix import Lexer
from vix.models import TextDocument
from tests import fixtures

class LexerTest(unittest.TestCase):

    def testBug58(self):
        document = TextDocument.TextDocument(fixtures.get("bug_58.py"))
        lexer = Lexer.Lexer()
        lexer.setModel(document)
        for line_num in range(1, document.numLines()):
            print(document.lineText( line_num))
            print(document.charMeta( (line_num,1)))

if __name__ == '__main__':
    unittest.main()
