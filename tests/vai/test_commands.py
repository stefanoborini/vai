import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument, LineMeta
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.document = TextDocument(fixtures.get("basic_python.py"))
        self.edit_area_model = EditAreaModel()
        self.buffer = Buffer(self.document, self.edit_area_model)

    def testNewLineCommand(self):
        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.document.numLines(), 5)
        self.assertEqual(self.document.lineMeta(1), {LineMeta.Change: "added"})
        self.assertEqual(self.document.lineMeta(2), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

        command.undo()
        self.assertEqual(self.document.numLines(), 4)
        self.assertEqual(self.document.lineMeta(1), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testNewLineAfterCommand(self):
        command = commands.NewLineAfterCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertTrue(status.success)
        self.assertEqual(self.document.numLines(), 5)
        self.assertEqual(self.document.lineMeta(1), {})
        self.assertEqual(self.document.lineMeta(2), {LineMeta.Change: "added"})
        self.assertEqual(self.document.lineMeta(3), {})
        self.assertNotEqual(self.document.lineText(1), "\n")
        self.assertEqual(self.document.lineText(2), "\n")
        self.assertEqual(self.buffer.documentCursor().pos(), (2,1))

        command.undo()
        self.assertEqual(self.document.numLines(), 4)
        self.assertEqual(self.document.lineMeta(1), {})
        self.assertEqual(self.document.lineMeta(2), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testDeleteLineAtCursorCommand1(self):
        removed_line = self.document.lineText(1)

        command = commands.DeleteLineAtCursorCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertTrue(status.success)

        self.assertEqual(self.document.numLines(), 3)
        self.assertNotEqual(self.document.lineText(1), removed_line)
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))
        # FIXME  check meta

        command.undo()
        self.assertEqual(self.document.numLines(), 4)
        self.assertEqual(self.document.lineText(1), removed_line)
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testDeleteLineAtCursorCommand2(self):
        """testDeleteLineAtCursorCommand from the bottom"""
        removed_line = self.document.lineText(4)
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        self.buffer.documentCursor().toPos((4,1))
        command.execute()
        self.assertEqual(self.document.numLines(), 3)
        self.assertEqual(self.buffer.documentCursor().pos(), (3,1))

        command.undo()
        self.assertEqual(self.document.numLines(), 4)
        self.assertEqual(self.document.lineText(4), removed_line)
        self.assertEqual(self.buffer.documentCursor().pos(), (4,1))

    def testDeleteLineAtCursorCommand3(self):
        """testDeleteLineAtCursorCommand all the way from the bottom"""
        self.buffer.documentCursor().toPos((4,2))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        command.execute()
        self.assertEqual(self.document.numLines(), 3)
        self.assertEqual(self.buffer.documentCursor().pos(), (3,2))

        command.execute()
        self.assertEqual(self.document.numLines(), 2)
        self.assertEqual(self.buffer.documentCursor().pos(), (2,1))

        command.execute()
        self.assertEqual(self.document.numLines(), 1)
        self.assertNotEqual(self.document.lineLength(1), 1)
        self.assertEqual(self.buffer.documentCursor().pos(), (1,2))

        command.execute()
        self.assertEqual(self.document.numLines(), 1)
        self.assertEqual(self.document.lineLength(1), 1)
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

        status = command.execute()
        self.assertFalse(status.success)
        self.assertEqual(self.document.numLines(), 1)
        self.assertEqual(self.document.lineLength(1), 1)
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testDeleteLineAtCursorCommand4(self):
        """Check if the cursor is placed at the beginning of line if next line is invalid"""
        self.buffer.documentCursor().toPos((1,6))
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testDeleteSingleCharCommand(self):
        self.buffer.documentCursor().toPos((1,1))
        line = self.document.lineText(1)
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))
        self.assertEqual(self.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

        self.buffer.documentCursor().toPos((1,2))
        result = command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))
        self.assertEqual(self.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))
        # FIXME test undo

    def testDeleteSingleCharCommand2(self):
        self.buffer.documentCursor().toPos((2,1))
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), (1,9))
        self.assertEqual(self.document.numLines(), 3)

    def testDeleteSingleCharAfterCommand(self):
        self.buffer.documentCursor().toPos((1,1))
        line = self.document.lineText(1)
        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))
        self.assertEqual(self.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

        line = self.document.lineText(1)
        self.buffer.documentCursor().toLineEnd()
        end_pos = self.buffer.documentCursor().pos()
        result = command.execute()
        self.assertEqual(self.buffer.documentCursor().pos(), end_pos)
        self.assertEqual(self.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

        # FIXME test undo

    def testBreakLineCommand(self):
        line = self.document.lineText(1)
        cursor = self.buffer.documentCursor()
        cursor.toPos((1,1))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.document.lineText(1), '\n')
        self.assertEqual(self.document.lineText(2), line)

        cursor.toPos((2,4))
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.document.lineText(2), line[:3]+'\n')
        self.assertEqual(self.document.lineText(3), line[3:])
        self.assertEqual(self.document.numLines(), 6)
        self.assertEqual(cursor.pos(), (3,1))

        # FIXME test undo

    def testJoinWithNextLineCommand(self):
        line_1 = self.document.lineText(1)
        line_2 = self.document.lineText(2)
        cursor = self.buffer.documentCursor()
        cursor.toPos((1,1))

        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.document.lineText(1), line_1[:-1]+line_2)
        self.assertEqual(cursor.pos(), (1,1))
        self.assertEqual(self.document.numLines(), 3)

    def testJoinWithNextLineCommand2(self):
        self.buffer.documentCursor().toLastLine()
        command = commands.JoinWithNextLineCommand(self.buffer)
        result = command.execute()
        self.assertFalse(result.success)

        # FIXME test undo

    def testInsertStringCommand(self):
        command = commands.InsertStringCommand(self.buffer, '')
        result = command.execute()
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()
