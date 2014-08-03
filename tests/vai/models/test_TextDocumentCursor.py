import unittest
from vai.models.TextDocument import TextDocument
from vai.models.TextDocumentCursor import TextDocumentCursor
from tests import fixtures

class TestTextDocumentCursor(unittest.TestCase):

    def setUp(self):
        self.doc = TextDocument()
        self.doc.open(fixtures.get("basic_nonempty_file.txt"))

    def testPos(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertEqual(cursor.pos, (1,1))
        cursor.toPos( (1,4) )
        self.assertEqual(cursor.pos, (1,4))

    def testTextDocument(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertEqual(cursor.textDocument(), self.doc)

    def testToPos(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertTrue(cursor.toPos( (1,1) ))
        self.assertTrue(cursor.toPos( (1,3) ))
        self.assertFalse(cursor.toPos( (0,1) ))
        self.assertFalse(cursor.toPos( (1,0) ))
        self.assertFalse(cursor.toPos( (1,30) ))
        self.assertFalse(cursor.toPos( (30,1) ))

    def testToLine(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertTrue(cursor.toLine(1))
        self.assertTrue(cursor.toLine(2))
        self.assertFalse(cursor.toLine(-1))
        self.assertFalse(cursor.toLine(30))

    def testToLinePrev(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertFalse(cursor.toLinePrev())
        self.assertTrue(cursor.toLine(2))
        self.assertTrue(cursor.toLinePrev())

    def testToLineNext(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertTrue(cursor.toLineNext())
        self.assertFalse(cursor.toLineNext())

    def testToCharPrev(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertFalse(cursor.toCharPrev())
        cursor.toPos((1,4))
        self.assertTrue(cursor.toCharPrev())
        self.assertTrue(cursor.toCharPrev())
        self.assertTrue(cursor.toCharPrev())
        self.assertFalse(cursor.toCharPrev())

    def testToCharNext(self):
        cursor = TextDocumentCursor(self.doc)
        self.assertTrue(cursor.toCharNext())
        self.assertTrue(cursor.toCharNext())
        self.assertTrue(cursor.toCharNext())
        self.assertTrue(cursor.toCharNext())
        self.assertTrue(cursor.toCharNext())
        self.assertFalse(cursor.toCharNext())

    def testToLineBeginning(self):
        cursor = TextDocumentCursor(self.doc)
        cursor.toPos((1,4))
        cursor.toLineBeginning()
        self.assertEqual(cursor.pos, (1,1))

    def testToLineEnd(self):
        cursor = TextDocumentCursor(self.doc)
        cursor.toPos((1,4))
        cursor.toLineEnd()
        self.assertEqual(cursor.pos, (1,6))

    def testToFirstLine(self):
        cursor = TextDocumentCursor(self.doc)
        cursor.toPos((2,4))
        cursor.toFirstLine()
        self.assertEqual(cursor.pos, (1,1))

    def testToLastLine(self):
        cursor = TextDocumentCursor(self.doc)
        cursor.toPos((1,4))
        cursor.toLastLine()
        self.assertEqual(cursor.pos, (2,1))

if __name__ == '__main__':
    unittest.main()
