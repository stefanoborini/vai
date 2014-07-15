import unittest
from vix.models.Buffer import Buffer
from vix.models.TextDocument import TextDocument, LineMeta
from vix.models.EditAreaModel import EditAreaModel
from vix import commands
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

    def testDeleteLineAtCursorCommand(self):
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

        removed_line = self.document.lineText(4)
        self.buffer.documentCursor().toPos((4,1))
        command.execute()
        self.assertEqual(self.document.numLines(), 3)
        self.assertEqual(self.buffer.documentCursor().pos(), (3,1))

        command.undo()
        self.assertEqual(self.document.numLines(), 4)
        self.assertEqual(self.document.lineText(4), removed_line)
        self.assertEqual(self.buffer.documentCursor().pos(), (4,1))


    def testDeleteSingleCharCommand(self):
        command = commands.DeleteSingleCharCommand(self.buffer)

    def testDeleteSingleCharAfterCommand(self):
        command = commands.DeleteSingleCharAfterCommand(self.buffer)

    def testBreakLineCommand(self):
        command = commands.BreakLineCommand(self.buffer)

    def testJoinWithNextLineCommand(self):
        command = commands.JoinWithNextLineCommand(self.buffer)

    def testInsertStringCommand(self):
        command = commands.InsertStringCommand(self.buffer, '')

if __name__ == '__main__':
    unittest.main()
