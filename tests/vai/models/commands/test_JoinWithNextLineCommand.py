import unittest
from vai import models
from vai.models import commands
from tests import fixtures

class TestJoinWithNextLineCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        with open(fixtures.get("basic_python.py"), 'r') as f:
            self.buffer.document.read(f)

    def testJoinWithNextLineCommand(self):
        line_1 = self.buffer.document.lineText(1)
        line_2 = self.buffer.document.lineText(2)
        cursor = self.buffer.cursor
        cursor.toPos((1,1))

        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(1), line_1[:-1]+line_2)
        self.assertEqual(cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.numLines(), 3)

    def testJoinWithNextLineCommand2(self):
        self.buffer.cursor.toLastLine()
        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        self.assertFalse(result.success)

    def testUndo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document
        cursor = self.buffer.cursor
        cursor.toPos((1,1))
        line_1 = document.lineText(1)
        line_2 = document.lineText(2)

        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        command.undo()

        self.assertEqual(line_1, document.lineText(1))
        self.assertEqual(line_2, document.lineText(2))

    def testRedo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document
        cursor = self.buffer.cursor
        cursor.toPos((1,1))
        line_1 = document.lineText(1)
        line_2 = document.lineText(2)

        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        command.undo()

        cursor.toPos((3,1))

        command.execute()

        self.assertEqual(self.buffer.document.lineText(1), line_1[:-1]+line_2)
        self.assertEqual(cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.numLines(), 3)

if __name__ == '__main__':
    unittest.main()
