import os
import unittest
import time
from vai.models.TextDocument import TextDocument
from vai.models.TextDocument import _withEOL, _withoutEOL
from tests import fixtures

class TestTextDocument(unittest.TestCase):
    def testInitEmpty(self):
        doc = TextDocument()

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), None)
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromEmptyFile(self):
        doc = TextDocument()
        doc.open(fixtures.get("empty_file.txt"))

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), fixtures.get("empty_file.txt"))
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromNonEmptyFile(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))

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
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')

        self.assertRaises(IndexError, lambda : doc.lineText(-1))
        self.assertRaises(IndexError, lambda : doc.lineText(0))
        self.assertRaises(IndexError, lambda : doc.lineText(5))

    def testHasLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertTrue(doc.hasLine(1))
        self.assertFalse(doc.hasLine(20))

    def testLineLength(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(doc.lineLength(1), 6)
        self.assertEqual(doc.lineLength(2), 13)

        doc = TextDocument()
        doc.open(fixtures.get("empty_file.txt"))
        self.assertEqual(doc.lineLength(1), 1)

    def testDocumentMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(type(doc.documentMeta()), dict)

    def testUpdateDocumentMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.updateDocumentMeta({"Hello": 5})
        self.assertEqual(type(doc.documentMeta()), dict)
        self.assertEqual(doc.documentMeta()["Hello"], 5)

    def testDeleteDocumentMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.updateDocumentMeta({"Hello": 5})
        self.assertEqual(doc.documentMeta()["Hello"], 5)
        doc.deleteDocumentMeta("Hello")
        self.assertNotIn("Hello", doc.documentMeta())

    def testLastModified(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        last_modified = doc.lastModified()
        self.assertEqual(doc.lastModified(), last_modified)
        time.sleep(0.1)
        doc.insertLine(1,"")
        self.assertNotEqual(doc.lastModified(), last_modified)

    def testCharMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.updateCharMeta((1,1), {"Hello": [1]})
        self.assertEqual(len(doc.charMeta((1,1))["Hello"]), len(doc.lineText(1)))
        self.assertEqual(doc.charMeta((1,1))["Hello"], [1, None, None, None, None, None])

    def testUpdateCharMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.updateCharMeta( (1, 3), { "foo" : ["a", "a"],
                                      "bar" : ['b', None, 'b'],
                                    }
                          )

    def testDeleteCharMeta(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.deleteCharMeta( (1, 3), 2, ['foo', 'bar'])

    def testNewLineAfter(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.newLineAfter(1)

    def testNewLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.newLine(1)

    def testInsertLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(doc.numLines(), 2)
        doc.insertLine(1,"babau")
        self.assertEqual(doc.numLines(), 3)

        self.assertRaises(IndexError, lambda : doc.insertLine(6,"say what again"))

        doc.insertLine(4,"say what again")
        self.assertEqual(doc.numLines(), 4)

    def testDeleteLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))

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
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))

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
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.replaceLine(1, "babau")

    def testBreakLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.breakLine((1,3))
        self.assertEqual(doc.lineText(1), "he\n")
        self.assertEqual(doc.lineText(2), "llo\n")

    def testJoinWithNextLine(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')
        self.assertTrue(doc.isModified())

        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')

    def testJoinWithNextLine2(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.joinWithNextLine(2)
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)
        self.assertFalse(doc.isModified())

    def testInsertChars(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.insertChars( (1,3), "babau")

    def testDeleteChars(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))

        self.assertRaises(ValueError, lambda : doc.deleteChars((1,3), -1))

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
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.replaceChars( (1,3), 1, "hello")

        self.assertEqual(doc.lineText(1), 'hehellolo\n')

        doc.replaceChars( (1,1), 1, "c")

        self.assertEqual(doc.lineText(1), 'cehellolo\n')

    def testSave(self):
        path = fixtures.tempFile("testSave")
        doc = TextDocument()
        doc.setFilename(path)
        doc.save()
        self.assertTrue(os.path.exists(path))

    def testSaveUnnamed(self):
        doc = TextDocument()
        self.assertRaises(TextDocument.MissingFilenameException, lambda: doc.save())

        path = fixtures.tempFile("testSaveUnnamed")
        doc.saveAs(path)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(doc.filename(), path)

    def testSaveAs(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.saveAs("foo")

    def createCursor(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.createCursor()

    def registerCursor(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
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

    def testWordAt(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        self.assertEqual(doc.wordAt((2,6)), ('are', 5))

    def testDeleteLines(self):
        doc = TextDocument()
        doc.open(fixtures.get("bigfile.py"))
        doc.deleteLines(1,3)

    def testInsertLines(self):
        doc = TextDocument()
        doc.open(fixtures.get("basic_nonempty_file.txt"))
        doc.insertLines(2, ['foo', 'bar'])
        self.assertEqual(doc.numLines(), 4)

    def testLineMetaInfoBasic(self):
        doc = TextDocument()
        meta_info = doc.lineMetaInfo("whatever")

        self.assertEqual(meta_info.document, doc)
        self.assertEqual(meta_info.meta_type, "whatever")
        self.assertEqual(meta_info.numLines(), 1)
        self.assertEqual(meta_info.data(1), None)

        meta_info.setData("hello",1)
        self.assertEqual(meta_info.data(1), "hello")

    def testLineMetaSameObject(self):
        doc = TextDocument()
        self.assertEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever"))
        self.assertNotEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever2"))

    def testLineMetaInfoChangeLineNumber(self):
        doc = TextDocument()
        meta_info1 = doc.lineMetaInfo("whatever")
        meta_info2 = doc.lineMetaInfo("whatever2")

        meta_info1.setData("hello", 1)
        meta_info2.setData("byebye", 1)

        doc.newLineAfter(1)

        self.assertEqual(meta_info1.numLines(), 2)
        self.assertEqual(meta_info2.numLines(), 2)

        self.assertEqual(meta_info1.data(1,2), ["hello", None])
        self.assertEqual(meta_info2.data(1,2), ["byebye", None])

        doc.newLine(1)

        self.assertEqual(meta_info1.numLines(), 3)
        self.assertEqual(meta_info2.numLines(), 3)

        self.assertEqual(meta_info1.data(1,3), [None, "hello", None])
        self.assertEqual(meta_info2.data(1,3), [None, "byebye", None])

        doc.deleteLine(2)

        self.assertEqual(meta_info1.numLines(), 2)
        self.assertEqual(meta_info2.numLines(), 2)

        self.assertEqual(meta_info1.data(1,2), [None, None])
        self.assertEqual(meta_info2.data(1,2), [None, None])

        self.assertEqual(meta_info1.data(1,1), [None])
        self.assertEqual(meta_info2.data(1,1), [None])

        self.assertEqual(meta_info1.data(1), None)
        self.assertEqual(meta_info2.data(1), None)

    def testLineMetaInfoMemento(self):
        doc = TextDocument()
        meta_info1 = doc.lineMetaInfo("whatever")
        meta_info2 = doc.lineMetaInfo("whatever2")
        doc.newLineAfter(1)
        doc.newLine(1)

        meta_info1.setData("hello", 1)
        meta_info2.setData("byebye", 1)

        memento = doc.lineMemento(1)

        doc.deleteLine(1)
        self.assertEqual(doc.lineMetaInfo("whatever").data(1), None)
        self.assertEqual(doc.lineMetaInfo("whatever2").data(1), None)

        doc.insertFromMemento(1, memento)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.lineMetaInfo("whatever").data(1), 'hello')
        self.assertEqual(doc.lineMetaInfo("whatever2").data(1), 'byebye')



if __name__ == '__main__':
    unittest.main()
