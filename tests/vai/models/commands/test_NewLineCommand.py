import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestNewLineCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testNewLineCommand(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(doc.numLines(), 5)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), "added")
        self.assertEqual(doc.lineMetaInfo("Change").data(2), None)
        self.assertEqual(cursor.pos, (1,1))

        command.undo()
        self.assertEqual(doc.numLines(), 4)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), None)
        self.assertEqual(cursor.pos, (1,1))

        cursor.toPos((4,7))

        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(doc.numLines(), 5)
        self.assertEqual(cursor.pos, (4,5))
        cursor.toLineNext()
        self.assertEqual(cursor.pos, (5,5))

    def testRedo(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        cursor.toPos((2,1))
        command = commands.NewLineCommand(self.buffer)
        command.execute()
        command.undo()
        cursor.toPos((4,1))
        command.execute()
        self.assertEqual(doc.numLines(), 5)
        self.assertEqual(cursor.pos, (2,1))


if __name__ == '__main__':
    unittest.main()
