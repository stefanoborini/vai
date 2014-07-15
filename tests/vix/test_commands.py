import unittest
from vix.models.Buffer import Buffer
from vix.models.TextDocument import TextDocument, LineMeta
from vix.models.EditAreaModel import EditAreaModel
from vix import commands
from tests import fixtures


class TestCommands(unittest.TestCase):
    def setUp(self):

        document = TextDocument(fixtures.get("basic_python.py"))
        edit_area_model = EditAreaModel()
        self.buffer = Buffer(document, edit_area_model)

    def testNewLineCommand(self):
        command = commands.NewLineCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.buffer.document().numLines(), 5)
        self.assertEqual(self.buffer.document().lineMeta(1), {LineMeta.Change: "added"})
        self.assertEqual(self.buffer.document().lineMeta(2), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

        command.undo()
        self.assertEqual(self.buffer.document().numLines(), 4)
        self.assertEqual(self.buffer.document().lineMeta(1), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))


    def testNewLineAfterCommand(self):
        command = commands.NewLineAfterCommand(self.buffer)
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(self.buffer.document().numLines(), 5)
        self.assertEqual(self.buffer.document().lineMeta(1), {})
        self.assertEqual(self.buffer.document().lineMeta(2), {LineMeta.Change: "added"})
        self.assertEqual(self.buffer.document().lineMeta(3), {})
        self.assertNotEqual(self.buffer.document().lineText(1), "\n")
        self.assertEqual(self.buffer.document().lineText(2), "\n")
        self.assertEqual(self.buffer.documentCursor().pos(), (2,1))

        command.undo()
        self.assertEqual(self.buffer.document().numLines(), 4)
        self.assertEqual(self.buffer.document().lineMeta(1), {})
        self.assertEqual(self.buffer.document().lineMeta(2), {})
        self.assertEqual(self.buffer.documentCursor().pos(), (1,1))

    def testDeleteLineAtCursorCommand(self):
        command = commands.DeleteLineAtCursorCommand(self.buffer)

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
