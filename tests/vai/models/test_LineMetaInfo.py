import os
import unittest
import time
from vai.models.TextDocument import TextDocument
from vai.models.TextDocument import _withEOL, _withoutEOL
from tests import fixtures

class TestLineMetaInfo(unittest.TestCase):
    def testBasic(self):
        doc = TextDocument()
        meta_info = doc.lineMetaInfo("whatever")

        self.assertEqual(meta_info.document, doc)
        self.assertEqual(meta_info.meta_type, "whatever")
        self.assertEqual(meta_info.numLines(), 1)
        self.assertEqual(meta_info.data(1), None)

        meta_info.setData("hello",1)
        self.assertEqual(meta_info.data(1), "hello")

    def testSameObject(self):
        doc = TextDocument()
        self.assertEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever"))
        self.assertNotEqual(doc.lineMetaInfo("whatever"), doc.lineMetaInfo("whatever2"))

    def testChangeLineNumber(self):
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

    def testSetDataForLines(self):
        doc = TextDocument()
        doc.insertLine(1, "hello")
        doc.insertLine(1, "hello")
        doc.insertLine(1, "hello")
        meta_info = doc.lineMetaInfo("whatever")

        meta_info.setDataForLines({2: "damn"})

        self.assertEqual(meta_info.data(), [None, "damn", None])





if __name__ == '__main__':
    unittest.main()
