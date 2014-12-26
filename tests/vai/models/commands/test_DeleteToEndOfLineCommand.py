import unittest
from vai import models
from vai.models import commands
from tests import fixtures

class TestDeleteToEndOfLineCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testDeleteToEndOfLineCommand(self):
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfLineCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,5))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")

    def testUndo(self):
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfLineCommand(self.buffer)
        result = command.execute()

        self.buffer.cursor.toPos((3,1))
        command.undo()

        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "#!python\n")

    def testRedoToOldPos(self):
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfLineCommand(self.buffer)
        result = command.execute()

        self.buffer.cursor.toPos((3,1))
        command.undo()

        self.buffer.cursor.toPos((3,1))
        command.execute()

        self.assertEqual(self.buffer.cursor.pos, (1,5))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")
