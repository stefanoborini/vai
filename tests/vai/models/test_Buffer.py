import unittest
from vai.models.TextDocument import TextDocument
from vai.models.TextDocumentCursor import TextDocumentCursor
from vai.models.EditAreaModel import EditAreaModel
from vai.models.Buffer import Buffer
from unittest.mock import Mock

class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.document = Mock(spec=TextDocument)
        self.edit_area_model = Mock(spec=EditAreaModel)
        self.buf = Buffer()
        self.buf._document = self.document
        self.buf._edit_area_model = self.edit_area_model

    def testBufferInit(self):
        b = self.buf
        self.assertIsInstance(b, Buffer)
        self.assertEqual(len(b.command_history), 0)

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

        self.assertEqual(len(b.command_history), 0)
        b.command_history.push(command1)
        b.command_history.push(command2)

        self.assertEqual(len(b.command_history), 2)
        self.assertEqual(b.command_history.pop(), command2)
        self.assertEqual(len(b.command_history), 1)
        self.assertEqual(b.command_history.pop(), command1)
        self.assertEqual(len(b.command_history), 0)
        self.assertRaises(IndexError, lambda : b.command_history.pop())

    def testDocumentCursor(self):
        b = self.buf
        self.assertIsInstance(b.cursor, TextDocumentCursor)

    def testDocument(self):
        b = self.buf
        self.assertIsInstance(b.document, TextDocument)

    def testEditAreaModel(self):
        b = self.buf
        self.assertIsInstance(b.edit_area_model, EditAreaModel)



if __name__ == '__main__':
    unittest.main()
