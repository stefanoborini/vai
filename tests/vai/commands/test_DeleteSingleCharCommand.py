import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestDeleteSingleCharCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

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

if __name__ == '__main__':
    unittest.main()
