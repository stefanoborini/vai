import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestInsertLineCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertLineCommand(self):
        self.buffer.cursor.toFirstLine()
        command1 = commands.InsertLineCommand(self.buffer, '1234')
        result = command1.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(1), "1234\n")

        self.buffer.cursor.toLastLine()
        command2 = commands.InsertLineCommand(self.buffer, '5678')
        result = command2.execute()
        self.assertTrue(result.success)
        self.assertEqual(self.buffer.document.lineText(5), "5678\n")

        command2.undo()
        self.assertEqual(self.buffer.document.numLines(), 5)
        command1.undo()
        self.assertEqual(self.buffer.document.numLines(), 4)

if __name__ == '__main__':
    unittest.main()
