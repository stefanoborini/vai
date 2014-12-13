import unittest
from vai import models
from vai.models import commands
from tests import fixtures

class TestDeleteToEndOfLineCommands(unittest.TestCase):
    def testDeleteToEndOfLineCommand(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfLineCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,5))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")

