import unittest
from vix.models.Buffer import Buffer
from vix.models.TextDocument import TextDocument
from vix.models.EditAreaModel import EditAreaModel
from vix import commands

class TestCommands(unittest.TestCase):
    def setUp(self):
        document = TextDocument()
        edit_area_model = EditAreaModel()
        self.buffer = Buffer(document, edit_area_model)

    def testNewLineCommand(self):
        command = commands.NewLineCommand(self.buffer)

    def testNewLineAfterCommand(self):
        command = commands.NewLineAfterCommand(self.buffer)

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
