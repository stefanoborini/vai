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
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromEmptyFile(self):
        doc = TextDocument()
        with open(fixtures.get("empty_file.txt"), "r") as f:
            doc.read(f)

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.documentText(), '\n')

    def testInitFromNonEmptyFile(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)

        self.assertFalse(doc.isEmpty())
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
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)

        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')

        self.assertRaises(IndexError, lambda : doc.lineText(-1))
        self.assertRaises(IndexError, lambda : doc.lineText(0))
        self.assertRaises(IndexError, lambda : doc.lineText(5))

    def testHasLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        self.assertTrue(doc.hasLine(1))
        self.assertFalse(doc.hasLine(20))

    def testLineLength(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        self.assertEqual(doc.lineLength(1), 6)
        self.assertEqual(doc.lineLength(2), 13)

        doc = TextDocument()
        with open(fixtures.get("empty_file.txt"), 'r') as f:
            doc.read(f)
        self.assertEqual(doc.lineLength(1), 1)

    def testDocumentMeta(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.createDocumentMetaInfo("Hello")
        self.assertEqual(doc.documentMetaInfo("Hello").data(), None)

        doc.createDocumentMetaInfo("Hello2", 2)
        self.assertEqual(doc.documentMetaInfo("Hello2").data(), 2)

    def testUpdateDocumentMeta(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.createDocumentMetaInfo("Hello")
        doc.documentMetaInfo("Hello").setData(5)
        self.assertEqual(doc.documentMetaInfo("Hello").data(), 5)

    def testCharMeta(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.updateCharMeta((1,1), {"Hello": [1]})
        self.assertEqual(len(doc.charMeta((1,1))["Hello"]), len(doc.lineText(1)))
        self.assertEqual(doc.charMeta((1,1))["Hello"], [1, None, None, None, None, None])

    def testUpdateCharMeta(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.updateCharMeta( (1, 3), { "foo" : ["a", "a"],
                                      "bar" : ['b', None, 'b'],
                                    }
                          )

    def testDeleteCharMeta(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.deleteCharMeta( (1, 3), 2, ['foo', 'bar'])

    def testNewLineAfter(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.newLineAfter(1)

    def testNewLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.newLine(1)

    def testInsertLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        self.assertEqual(doc.numLines(), 2)
        doc.insertLine(1,"babau")
        self.assertEqual(doc.numLines(), 3)

        self.assertRaises(IndexError, lambda : doc.insertLine(6,"say what again"))

        doc.insertLine(4,"say what again")
        self.assertEqual(doc.numLines(), 4)

    def testDeleteLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)

        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), 'how are you?\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertFalse(doc.isEmpty())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())

    def testDeleteLine2(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)

        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)

        self.assertRaises(IndexError, lambda :  doc.deleteLine(5))
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)

        doc.deleteLine(2)
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertFalse(doc.isEmpty())

        doc.deleteLine(1)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.numLines(), 1)
        self.assertTrue(doc.isEmpty())

    def testReplaceLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.replaceLine(1, "babau")

    def testBreakLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.breakLine((1,3))
        self.assertEqual(doc.lineText(1), "he\n")
        self.assertEqual(doc.lineText(2), "llo\n")

    def testJoinWithNextLine(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')

        doc.joinWithNextLine(1)
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.lineText(1), 'hellohow are you?\n')

    def testJoinWithNextLine2(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.joinWithNextLine(2)
        self.assertEqual(doc.lineText(1), 'hello\n')
        self.assertEqual(doc.lineText(2), 'how are you?\n')
        self.assertEqual(doc.numLines(), 2)

    def testInsertChars(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.insertChars( (1,3), "babau")

    def testDeleteChars(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)

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
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.replaceChars( (1,3), 1, "hello")

        self.assertEqual(doc.lineText(1), 'hehellolo\n')

        doc.replaceChars( (1,1), 1, "c")

        self.assertEqual(doc.lineText(1), 'cehellolo\n')

    def testSave(self):
        path = fixtures.tempFile("testSave")
        doc = TextDocument()
        with open(path, 'w') as f:
            doc.write(f)
        self.assertTrue(os.path.exists(path))

    def createCursor(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.createCursor()

    def registerCursor(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
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
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        self.assertEqual(doc.wordAt((2,6)), ('are', 5))

    def testDeleteLines(self):
        doc = TextDocument()
        with open(fixtures.get("bigfile.py"), 'r') as f:
            doc.read(f)
        doc.deleteLines(1,3)

    def testInsertLines(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.insertLines(2, ['foo', 'bar'])
        self.assertEqual(doc.numLines(), 4)

    def testLineMetaInfoBasic(self):
        doc = TextDocument()
        doc.createLineMetaInfo("whatever")
        meta_info = doc.lineMetaInfo("whatever")

        self.assertEqual(meta_info.document, doc)
        self.assertEqual(meta_info.meta_type, "whatever")
        self.assertEqual(meta_info.numLines(), 1)
        self.assertEqual(meta_info.data(1), None)

        meta_info.setData("hello",1)
        self.assertEqual(meta_info.data(1), "hello")

    def testLineMetaSameObject(self):
        doc = TextDocument()
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")
        self.assertEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever"))
        self.assertNotEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever2"))

    def testLineMetaInfoChangeLineNumber(self):
        doc = TextDocument()
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")
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
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")

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

    def testReplaceFromMemento(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.createLineMetaInfo("whatever")
        initial_text = doc.documentText()
        meta_info1 = doc.lineMetaInfo("whatever")
        meta_info1.setData("hello", 1)

        memento = doc.lineMemento(1)
        doc.insertChars((1,1), 'gnakgnak')
        meta_info1.setData("byebye", 1)
        doc.replaceFromMemento(1, memento)

        self.assertEqual(doc.documentText(), initial_text)
        self.assertEqual(meta_info1.data(1), "hello")

    def testLineMetaInfoMemento(self):
        doc = TextDocument()
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")

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

    def testReplaceFromMemento(self):
        doc = TextDocument()
        with open(fixtures.get("basic_nonempty_file.txt"), 'r') as f:
            doc.read(f)
        doc.createLineMetaInfo("whatever")
        initial_text = doc.documentText()
        meta_info1 = doc.lineMetaInfo("whatever")
        meta_info1.setData("hello", 1)

        memento = doc.lineMemento(1)
        doc.insertChars((1,1), 'gnakgnak')
        meta_info1.setData("byebye", 1)
        doc.replaceFromMemento(1, memento)

        self.assertEqual(doc.documentText(), initial_text)
        self.assertEqual(meta_info1.data(1), "hello")

    def testExtractFragment(self):
        doc = TextDocument()
        with open(fixtures.get("bigfile.py"), 'r') as f:
            doc.read(f)
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")

        fragment = doc.extractFragment(2)
        self.assertEqual(fragment.numLines(), 1)
        self.assertEqual(fragment.lineText(1), doc.lineText(2))
        self.assertTrue(fragment.hasLineMetaInfo("whatever"))
        self.assertTrue(fragment.hasLineMetaInfo("whatever2"))

        fragment = doc.extractFragment(2, 3)
        self.assertEqual(fragment.numLines(), 3)
        self.assertEqual(fragment.lineText(1), doc.lineText(2))
        self.assertEqual(fragment.lineText(2), doc.lineText(3))
        self.assertEqual(fragment.lineText(3), doc.lineText(4))
        self.assertTrue(fragment.hasLineMetaInfo("whatever"))
        self.assertTrue(fragment.hasLineMetaInfo("whatever2"))

    def testInsertFragment(self):
        doc = TextDocument()
        with open(fixtures.get("numbers.txt"), 'r') as f:
            doc.read(f)
        doc.createLineMetaInfo("whatever")
        doc.createLineMetaInfo("whatever2")

        fragment = doc.extractFragment(2)
        self.assertNotEqual(fragment.lineText(1), doc.lineText(15))
        doc.insertFragment(15, fragment)
        self.assertEqual(fragment.lineText(1), doc.lineText(15))

        fragment = doc.extractFragment(2,4)
        self.assertNotEqual(fragment.lineText(1), doc.lineText(10))
        doc.insertFragment(10, fragment)

        self.assertEqual(fragment.lineText(1), doc.lineText(10))
        self.assertEqual(fragment.lineText(2), doc.lineText(11))
        self.assertEqual(fragment.lineText(3), doc.lineText(12))
        self.assertEqual(fragment.lineText(4), doc.lineText(13))

if __name__ == '__main__':
    unittest.main()
