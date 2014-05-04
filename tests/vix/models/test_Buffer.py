import unittest
from vix.models.TextDocument import TextDocument
from vix.models.ViewModel import ViewModel
from vix.models.Buffer import Buffer
from unittest.mock import Mock

class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.document = Mock(spec=TextDocument)
        self.view_model = Mock(spec=ViewModel)

    def testBufferInit(self):
        b = Buffer(self.document, self.view_model)
        self.assertIsInstance(b,Buffer)
        self.assertEqual(len(b.commandHistory()), 0)

    def testIsEmpty(self):
        b = Buffer(self.document, self.view_model)
        self.document.isEmpty.return_value = False
        self.assertFalse(b.isEmpty())

        self.document.isEmpty.return_value = True
        self.assertTrue(b.isEmpty())

    def testIsModified(self):
        b = Buffer(self.document, self.view_model)
        self.document.isModified.return_value = False
        self.assertFalse(b.isModified())

        self.document.isModified.return_value = True
        self.assertTrue(b.isModified())

    def testCommandHistory(self):
        b = Buffer(self.document, self.view_model)
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



if __name__ == '__main__':
    unittest.main()
