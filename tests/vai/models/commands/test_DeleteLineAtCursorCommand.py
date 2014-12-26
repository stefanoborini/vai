import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestDeleteLineAtCursorCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testDeleteLineAtCursorCommand1(self):
        removed_line = self.buffer.document.lineText(1)

        command = commands.DeleteLineAtCursorCommand(self.buffer)
        result = command.execute()
        self.assertNotEqual(result, None)
        self.assertTrue(result.success)
        self.assertEqual(result.info, [ ({}, '#!python\n'), {'LinterResult': None, 'Change': None, 'Bookmark': None}])

        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertNotEqual(self.buffer.document.lineText(1), removed_line)
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        # FIXME  check meta

        command.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)
        self.assertEqual(self.buffer.document.lineText(1), removed_line)
        self.assertEqual(self.buffer.cursor.pos, (1,1))

    def testDeleteLineAtCursorCommand2(self):
        """testDeleteLineAtCursorCommand from the bottom"""
        second_to_last_line = self.buffer.document.lineText(3)
        removed_line = self.buffer.document.lineText(4)
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        self.buffer.cursor.toPos((4,1))
        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertEqual(self.buffer.cursor.pos, (3,1))
        self.assertEqual(self.buffer.document.lineText(3), second_to_last_line)

        command.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)
        self.assertEqual(self.buffer.document.lineText(4), removed_line)
        self.assertEqual(self.buffer.cursor.pos, (4,1))

    def testDeleteLineAtCursorCommand3(self):
        """testDeleteLineAtCursorCommand all the way from the bottom"""
        self.buffer.cursor.toPos((4,2))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertEqual(self.buffer.cursor.pos, (3,2))

        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 2)
        self.assertEqual(self.buffer.cursor.pos, (2,1))

        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 1)
        self.assertNotEqual(self.buffer.document.lineLength(1), 1)
        self.assertEqual(self.buffer.cursor.pos, (1,2))

        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 1)
        self.assertEqual(self.buffer.document.lineLength(1), 1)
        self.assertEqual(self.buffer.cursor.pos, (1,1))

        status = command.execute()
        self.assertFalse(status.success)
        self.assertEqual(self.buffer.document.numLines(), 1)
        self.assertEqual(self.buffer.document.lineLength(1), 1)
        self.assertEqual(self.buffer.cursor.pos, (1,1))

    def testDeleteLineAtCursorCommand4(self):
        """Check if the cursor is placed at the end of line if next line is invalid"""
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))

    def testDeleteLineAtCursorCommand5(self):
        """testDeleteLineAtCursorCommand all the way from the bottom"""
        self.buffer.cursor.toPos((3,2))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        command.execute()
        self.assertEqual(self.buffer.document.lineMetaInfo("Change").data(), [None, 'deletion_before', 'deletion_after'])

    def testRedoAppliesToOldPosition(self):
        removed_line = self.buffer.document.lineText(1)
        second_line = self.buffer.document.lineText(2)

        self.buffer.cursor.toPos((1,1))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        result = command.execute()
        self.assertNotEqual(result, None)
        self.assertTrue(result.success)

        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), second_line)

        command.undo()
        self.buffer.cursor.toPos((3,1))
        self.assertEqual(self.buffer.document.numLines(), 4)

        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), second_line)

        
if __name__ == '__main__':
    unittest.main()
