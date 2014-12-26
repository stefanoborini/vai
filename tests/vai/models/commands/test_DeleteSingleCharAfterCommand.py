import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestDeleteSingleCharAfterCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testDeleteSingleCharAfterCommand(self):
        self.buffer.cursor.toPos((1,1))
        line = self.buffer.document.lineText(1)
        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        line = self.buffer.document.lineText(1)
        self.buffer.cursor.toLineEnd()
        end_pos = self.buffer.cursor.pos
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, end_pos)
        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

    def testUndo(self):
        self.buffer.cursor.toPos((1,1))
        line = self.buffer.document.lineText(1)
        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        result = command.execute()
        self.buffer.cursor.toPos((2,1))

        command.undo()

        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line)

    def testRedoAppliesToOldPos(self):
        self.buffer.cursor.toPos((1,1))
        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        result = command.execute()

        line = self.buffer.document.lineText(1)

        command.undo()

        self.buffer.cursor.toPos((3,1))

        command.execute()

        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line)

if __name__ == '__main__':
    unittest.main()
