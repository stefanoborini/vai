import unittest
from vix.models.TextDocument import TextDocument
from vix.models.TextDocumentCursor import TextDocumentCursor
from vix.models.EditAreaModel import EditAreaModel
from vix.models.Buffer import Buffer
from unittest.mock import Mock

class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.document = Mock(spec=TextDocument)
        self.edit_area_model = Mock(spec=EditAreaModel)
        self.buf = Buffer(self.document, self.edit_area_model)

    def testBufferInit(self):
        b = self.buf
        self.assertIsInstance(b,Buffer)
        self.assertEqual(len(b.commandHistory()), 0)

    def testIsEmpty(self):
        b = self.buf
        self.document.isEmpty.return_value = False
        self.assertFalse(b.isEmpty())

        self.document.isEmpty.return_value = True
        self.assertTrue(b.isEmpty())

    def testIsModified(self):
        b = self.buf
        self.document.isModified.return_value = False
        self.assertFalse(b.isModified())

        self.document.isModified.return_value = True
        self.assertTrue(b.isModified())

    def testCommandHistory(self):
        b = self.buf
        command = Mock()
        command1 = command()
        command2 = command()

        self.assertEqual(len(b.commandHistory()), 0)
        b.addCommandHistory(command1)
        b.addCommandHistory(command2)

        self.assertEqual(len(b.commandHistory()), 2)
        self.assertEqual(b.popCommandHistory(), command2)
        self.assertEqual(len(b.commandHistory()), 1)
        self.assertEqual(b.popCommandHistory(), command1)
        self.assertEqual(len(b.commandHistory()), 0)
        self.assertRaises(IndexError, lambda : b.popCommandHistory())

    def testDocumentCursor(self):
        b = self.buf
        self.assertIsInstance(b.documentCursor(), TextDocumentCursor)

    def testDocument(self):
        b = self.buf
        self.assertIsInstance(b.document(), TextDocument)

    def testEditAreaModel(self):
        b = self.buf
        self.assertIsInstance(b.editAreaModel(), EditAreaModel)



if __name__ == '__main__':
    unittest.main()
