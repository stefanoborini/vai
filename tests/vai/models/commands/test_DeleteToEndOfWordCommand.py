import unittest
from vai import models
from vai.models import commands
from tests import fixtures

class TestDeleteToEndOfWordCommands(unittest.TestCase):
    def testDeleteToEndOfWordCommand(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfWordCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")

    def testUndo(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfWordCommand(self.buffer)
        result = command.execute()

        self.buffer.cursor.toPos((3,1))

        command.undo()

        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "#!python\n")

    def testRedo(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfWordCommand(self.buffer)
        result = command.execute()

        self.buffer.cursor.toPos((3,1))

        command.undo()
        self.buffer.cursor.toPos((3,1))
        command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")

    def testParenthesisPreserved(self):
        """Check if parentheses are preserved (#124)"""
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("issue_124"))
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfWordCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "def f(bar, baz):\n")
