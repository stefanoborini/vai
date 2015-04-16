import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestDeleteSingleCharCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        with open(fixtures.get("basic_python.py"), 'r') as f:
            self.buffer.document.read(f)

    def testDeleteSingleCharCommand(self):
        self.buffer.cursor.toPos((1,1))
        line = self.buffer.document.lineText(1)
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

        command = commands.DeleteSingleCharCommand(self.buffer)
        self.buffer.cursor.toPos((1,2))
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

    def testDeleteSingleCharCommand2(self):
        self.buffer.cursor.toPos((2,1))
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,9))
        self.assertEqual(self.buffer.document.numLines(), 3)

    def testUndo(self):
        line = self.buffer.document.lineText(1)
        self.buffer.cursor.toPos((1,2))
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

        command.undo()
        self.assertEqual(self.buffer.cursor.pos, (1,2))
        self.assertEqual(self.buffer.document.lineText(1), line)

    def testRedoAppliesToOldPos(self):
        line = self.buffer.document.lineText(1)
        self.buffer.cursor.toPos((1,2))
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()

        command.undo()
        self.buffer.cursor.toPos((3,1))
        result = command.execute()

        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

if __name__ == '__main__':
    unittest.main()
