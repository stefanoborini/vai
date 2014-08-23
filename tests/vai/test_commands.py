import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument, LineMeta
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testNewLineCommand(self):
        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.buffer.document.numLines(), 5)
        self.assertEqual(self.buffer.document.lineMeta(1), {LineMeta.Change: "added"})
        self.assertEqual(self.buffer.document.lineMeta(2), {})
        self.assertEqual(self.buffer.cursor.pos, (1,1))

        command.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)
        self.assertEqual(self.buffer.document.lineMeta(1), {})
        self.assertEqual(self.buffer.cursor.pos, (1,1))

        self.buffer.cursor.toPos((4,7))
        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.buffer.document.numLines(), 5)
        self.assertEqual(self.buffer.cursor.pos, (4,5))
        self.buffer.cursor.toLineNext()
        self.assertEqual(self.buffer.cursor.pos, (5,5))

    def testNewLineAfterCommand(self):
        command = commands.NewLineAfterCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertTrue(status.success)
        self.assertEqual(self.buffer.document.numLines(), 5)
        self.assertEqual(self.buffer.document.lineMeta(1), {})
        self.assertEqual(self.buffer.document.lineMeta(2), {LineMeta.Change: "added"})
        self.assertEqual(self.buffer.document.lineMeta(3), {})
        self.assertNotEqual(self.buffer.document.lineText(1), "\n")
        self.assertEqual(self.buffer.document.lineText(2), "\n")
        self.assertEqual(self.buffer.cursor.pos, (2,1))

        command.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)
        self.assertEqual(self.buffer.document.lineMeta(1), {})
        self.assertEqual(self.buffer.document.lineMeta(2), {})
        self.assertEqual(self.buffer.cursor.pos, (1,1))

        self.buffer.cursor.toPos((4,7))
        command = commands.NewLineAfterCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.buffer.document.numLines(), 5)
        self.assertEqual(self.buffer.cursor.pos, (5,5))
        self.buffer.cursor.toLinePrev()
        self.assertEqual(self.buffer.cursor.pos, (4,5))
        command.undo()

    def testDeleteLineAtCursorCommand1(self):
        removed_line = self.buffer.document.lineText(1)

        command = commands.DeleteLineAtCursorCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertTrue(status.success)

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
        removed_line = self.buffer.document.lineText(4)
        command = commands.DeleteLineAtCursorCommand(self.buffer)
        self.buffer.cursor.toPos((4,1))
        command.execute()
        self.assertEqual(self.buffer.document.numLines(), 3)
        self.assertEqual(self.buffer.cursor.pos, (3,1))

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

    def testDeleteSingleCharCommand(self):
        self.buffer.cursor.toPos((1,1))
        line = self.buffer.document.lineText(1)
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

        self.buffer.cursor.toPos((1,2))
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))
        # FIXME test undo

    def testDeleteSingleCharCommand2(self):
        self.buffer.cursor.toPos((2,1))
        command = commands.DeleteSingleCharCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,9))
        self.assertEqual(self.buffer.document.numLines(), 3)

    def testDeleteToEndOfWordCommand(self):
        self.buffer.cursor.toPos((1,6))
        command = commands.DeleteToEndOfWordCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,6))
        self.assertEqual(self.buffer.document.lineText(1), "#!pyt\n")

    def testDeleteSingleCharAfterCommand(self):
        self.buffer.cursor.toPos((1,1))
        line = self.buffer.document.lineText(1)
        command = commands.DeleteSingleCharAfterCommand(self.buffer)
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, (1,1))
        self.assertEqual(self.buffer.document.lineText(1), line[1:])
        self.assertTrue(result.success)
        self.assertEqual(result.info, ('#', {}))

        line = self.buffer.document.lineText(1)
        self.buffer.cursor.toLineEnd()
        end_pos = self.buffer.cursor.pos
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, end_pos)
        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

        # FIXME test undo

    def testBreakLineCommand(self):
        line = self.buffer.document.lineText(1)
        cursor = self.buffer.cursor
        cursor.toPos((1,1))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(1), '\n')
        self.assertEqual(self.buffer.document.lineText(2), line)
        command.undo()
        command.execute()

        cursor.toPos((2,4))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(2), line[:3]+'\n')
        self.assertEqual(self.buffer.document.lineText(3), line[3:])
        self.assertEqual(self.buffer.document.numLines(), 6)
        self.assertEqual(cursor.pos, (3,1))

        command.undo()
        command.execute()

        cursor.toPos((1,1))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(1), '\n')
        self.assertEqual(self.buffer.document.lineText(2), '\n')

        command.undo()


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

    def testInsertStringCommand(self):
        command = commands.InsertStringCommand(self.buffer, '')
        result = command.execute()
        self.assertTrue(result.success)

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

if __name__ == '__main__':
    unittest.main()
