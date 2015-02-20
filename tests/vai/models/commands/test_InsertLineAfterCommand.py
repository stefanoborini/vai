import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertLineAfterCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertLineAfterCommand(self):
        self.buffer.cursor.toFirstLine()
        command1 = commands.InsertLineAfterCommand(self.buffer, '1234')
        result = command1.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(2), "1234\n")

        self.buffer.cursor.toLastLine()
        command2 = commands.InsertLineAfterCommand(self.buffer, '5678')
        result = command2.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(6), "5678\n")

        command2.undo()
        self.assertEqual(self.buffer.document.numLines(), 5)
        command1.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)

    def testRedo(self):
        cursor = self.buffer.cursor
        cursor.toPos((2,1))
        command = commands.InsertLineAfterCommand(self.buffer, '1234')
        result = command.execute()
        command.undo()

        cursor.toPos((4,1))
        result = command.execute()
        self.assertEqual(cursor.pos, (3,1))

    def testInsertCursorPositioning(self):
        cursor = self.buffer.cursor
        cursor.toFirstLine()
        command = commands.InsertLineAfterCommand(self.buffer, '    1234')
        result = command.execute()
        self.assertEqual(cursor.pos, (2,5))

if __name__ == '__main__':
    unittest.main()
