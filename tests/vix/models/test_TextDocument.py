import os
import sys
import inspect
import unittest
import time
from vixtk.test import VSignalSpy
from vix.models.TextDocument import TextDocument
from vix.models.TextDocument import _withEOL, _withoutEOL
from vix import flags
from tests import fixtures

class TestTextDocument(unittest.TestCase):
    def testInitEmpty(self):
        doc = TextDocument()

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), "noname.txt")
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromEmptyFile(self):
        doc = TextDocument(fixtures.get("empty_file.txt"))

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), fixtures.get("empty_file.txt"))
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromNonEmptyFile(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))

        self.assertFalse(doc.isEmpty())
        self.assertEqual(doc.filename(), fixtures.get("basic_nonempty_file.txt"))
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 2)
        self.assertEqual(doc.documentText(), 'hello\nhow are you?\n')

    def testIsEmpty(self):
        doc = TextDocument()

        self.assertTrue(doc.isEmpty())
        doc.insertLine(1, "hello")

        self.assertFalse(doc.isEmpty())

        doc.deleteLine(1)
        self.assertTrue(doc.isEmpty())

    def testLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        print(doc.documentText())
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')

        self.assertRaises(IndexError, lambda : doc.lineText(-1))
        self.assertRaises(IndexError, lambda : doc.lineText(0))
        self.assertRaises(IndexError, lambda : doc.lineText(5))

    def testHasLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        self.assertTrue(doc.hasLine(1))
        self.assertFalse(doc.hasLine(20))

    def testLineLength(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(doc.lineLength(1), 6)
        self.assertEqual(doc.lineLength(2), 13)

        doc = TextDocument(fixtures.get("empty_file.txt"))
        self.assertEqual(doc.lineLength(1), 1)

    def testDocumentMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(type(doc.documentMeta()), dict)

    def testUpdateDocumentMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateDocumentMeta({"Hello": 5})
        self.assertEqual(type(doc.documentMeta()), dict)
        self.assertEqual(doc.documentMeta()["Hello"], 5)

    def testDeleteDocumentMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateDocumentMeta({"Hello": 5})
        self.assertEqual(doc.documentMeta()["Hello"], 5)
        doc.deleteDocumentMeta("Hello")
        self.assertNotIn("Hello", doc.documentMeta())

    def testLastModified(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        last_modified = doc.lastModified()
        self.assertEqual(doc.lastModified(), last_modified)
        time.sleep(0.1)
        doc.insertLine(1,"")
        self.assertNotEqual(doc.lastModified(), last_modified)

    def testLineMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(type(doc.lineMeta(1)), dict)
        self.assertRaises(IndexError, lambda : doc.lineMeta(20))

    def testUpdateLineMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateLineMeta(1, {"hello": 5})
        self.assertEqual(type(doc.lineMeta(1)), dict)
        self.assertEqual(doc.lineMeta(1)["hello"], 5)

        self.assertRaises(IndexError, lambda : doc.updateLineMeta(20, {}))

    def testDeleteLineMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateLineMeta(1, {"hello": 5})
        self.assertEqual(doc.lineMeta(1)["hello"], 5)

        doc.deleteLineMeta(1, ["hello"])
        self.assertNotIn("hello", doc.lineMeta(1))

        self.assertRaises(IndexError, lambda : doc.deleteLineMeta(20, "hello"))

    def testCharMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateCharMeta((1,1), {"Hello": [1]})
        self.assertEqual(len(doc.charMeta((1,1))["Hello"]), len(doc.lineText(1)))
        self.assertEqual(doc.charMeta((1,1))["Hello"], [1, None, None, None, None, None])

    def testUpdateCharMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.updateCharMeta( (1, 3), { "foo" : ["a", "a"],
                                      "bar" : ['b', None, 'b'],
                                    }
                          )

    def testDeleteCharMeta(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.deleteCharMeta( (1, 3), 2, ['foo', 'bar'])

    def testNewLineAfter(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.newLineAfter(1)

    def testNewLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.newLine(1)

    def testInsertLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.insertLine(1,"babau")

    def testDeleteLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))

        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)
        self.assertFalse(doc.isModified())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), 'how are you?\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertFalse(doc.isEmpty())
        self.assertTrue(doc.isModified())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())
        self.assertTrue(doc.isModified())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())
        self.assertTrue(doc.isModified())

    def testDeleteLine2(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))

        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)
        self.assertFalse(doc.isModified())

        self.assertRaises(IndexError, lambda :  doc.deleteLine(5))
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)
        self.assertFalse(doc.isModified())

        doc.deleteLine(2)
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertFalse(doc.isEmpty())
        self.assertTrue(doc.isModified())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())
        self.assertTrue(doc.isModified())

    def testReplaceLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.replaceLine(1, "babau")

    def testBreakLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.breakLine((1,3))

    def testJoinWithNextLine(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')
        self.assertTrue(doc.isModified())

        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')

    def testJoinWithNextLine2(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.joinWithNextLine(2)
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)
        self.assertFalse(doc.isModified())

    def testInsertChars(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.insertChars( (1,3), "babau")

    def testDeleteChars(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        d = doc.deleteChars( (1,3), 1)
        self.assertEqual(doc.lineText(1), 'helo\n')
        self.assertEqual(d[0], 'l')

        d = doc.deleteChars( (1,2), 100)
        self.assertEqual(doc.lineText(1), 'h\n')
        self.assertEqual(d[0], 'elo')

        d = doc.deleteChars( (1,2), 100)
        self.assertEqual(doc.lineText(1), 'h\n')
        self.assertEqual(d[0], '')

        d = doc.deleteChars( (1,1), 100)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(d[0], 'h')

        d = doc.deleteChars( (1,1), 100)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(d[0], '')

    def testReplaceChars(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.replaceChars( (1,3), 1, "hello")

    def testSave(self):
        pass
        #doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        #doc.save()

    def testSaveAs(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.saveAs("foo")

    def createCursor(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        doc.createCursor()

    def registerCursor(self):
        doc = TextDocument(fixtures.get("basic_nonempty_file.txt"))
        cursor = TextDocumentCursor(doc)

    def testWithEOL(self):
        self.assertEqual(_withEOL("foo"), "foo\n")
        self.assertEqual(_withEOL("foo\n"), "foo\n")
        self.assertEqual(_withEOL(""), "\n")

    def testWithoutEOL(self):
        self.assertEqual(_withoutEOL("foo"), "foo")
        self.assertEqual(_withoutEOL("foo\n"), "foo")
        self.assertEqual(_withoutEOL(""), "")
        self.assertEqual(_withoutEOL("\n"), "")

if __name__ == '__main__':
    unittest.main()
