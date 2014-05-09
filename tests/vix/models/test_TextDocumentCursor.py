import os
import sys
import inspect
import unittest
from vixtk.test import VSignalSpy
from vix.models.TextDocument import TextDocument
from vix.models.TextDocumentCursor import TextDocumentCursor
from vix import flags

def baseDir():
    return os.path.dirname(inspect.getfile(sys.modules[__name__]))

def fixture(name):
    return os.path.join(baseDir(), "fixtures", name)

class TestTextDocumentCursor(unittest.TestCase):

    def testGetLine(self):
        doc = TextDocument(fixture("basic_nonempty_file.txt"))
        cursor = TextDocumentCursor(doc)

        self.assertEqual(cursor.pos(), (1,1))
        print(cursor.currentLine())

    def testMovements(self):
        doc = TextDocument(fixture("basic_nonempty_file.txt"))
        cursor = TextDocumentCursor(doc)



if __name__ == '__main__':
    unittest.main()
