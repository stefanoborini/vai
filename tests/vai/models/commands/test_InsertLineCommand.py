import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertLineCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertLineCommand(self):
        self.buffer.cursor.toFirstLine()
        command1 = commands.InsertLineCommand(self.buffer, '1234')
        result = command1.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(1), "1234\n")

        self.buffer.cursor.toLastLine()
        command2 = commands.InsertLineCommand(self.buffer, '5678')
        result = command2.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(5), "5678\n")

        command2.undo()
        self.assertEqual(self.buffer.document.numLines(), 5)
        command1.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)

    def testRedo(self):
        self.buffer.cursor.toPos((2,1))
        command = commands.InsertLineCommand(self.buffer, '1234')
        command.execute()
        command.undo()

        self.buffer.cursor.toPos((4,1))
        command.execute()
        self.assertEqual(self.buffer.cursor.pos, (2,1))


if __name__ == '__main__':
    unittest.main()
