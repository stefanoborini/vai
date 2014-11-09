import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestDeleteSingleCharAfterCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
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

        line = self.buffer.document.lineText(1)
        self.buffer.cursor.toLineEnd()
        end_pos = self.buffer.cursor.pos
        result = command.execute()
        self.assertEqual(self.buffer.cursor.pos, end_pos)
        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertFalse(result.success)
        self.assertEqual(result.info, None)

if __name__ == '__main__':
    unittest.main()
