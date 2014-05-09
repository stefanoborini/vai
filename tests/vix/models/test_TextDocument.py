import os
import sys
import inspect
import unittest
from vixtk.test import VSignalSpy
from vix.models.TextDocument import TextDocument
from vix import flags

def baseDir():
    return os.path.dirname(inspect.getfile(sys.modules[__name__]))

def fixture(name):
    return os.path.join(baseDir(), "fixtures", name)

class TestTextDocument(unittest.TestCase):

    def testInitEmpty(self):
        doc = TextDocument()

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), "noname.txt")
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.text(), '\n')

    def testInitFromEmptyFile(self):
        doc = TextDocument(fixture("empty_file.txt"))

        self.assertTrue(doc.isEmpty())
        self.assertEqual(doc.filename(), fixture("empty_file.txt"))
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 1)
        self.assertEqual(doc.text(), '\n')

    def testInitFromNonEmptyFile(self):
        doc = TextDocument(fixture("basic_nonempty_file.txt"))

        self.assertFalse(doc.isEmpty())
        self.assertEqual(doc.filename(), fixture("basic_nonempty_file.txt"))
        self.assertFalse(doc.isModified())
        self.assertEqual(doc.numLines(), 2)
        self.assertEqual(doc.text(), 'hello\nhow are you?\n')

    def testGetLine(self):
        doc = TextDocument(fixture("basic_nonempty_file.txt"))
        self.assertEqual(doc.getLine(1), 'hello\n')
        self.assertEqual(doc.getLine(2), 'how are you?\n')

        self.assertRaises(IndexError, lambda : doc.getLine(0))
        self.assertRaises(IndexError, lambda : doc.getLine(3))



if __name__ == '__main__':
    unittest.main()
