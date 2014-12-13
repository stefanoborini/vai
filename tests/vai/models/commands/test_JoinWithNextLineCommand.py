import unittest
from vai import models
from vai.models import commands
from tests import fixtures

class TestJoinWithNextLineCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

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

        # FIXME test undo

if __name__ == '__main__':
    unittest.main()
