import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestReplaceSingleCharCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testReplaceSingleChar(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        command = commands.ReplaceSingleCharCommand(self.buffer, 'r')
        status = command.execute()
        self.assertNotEqual(status, None)
        self.assertEqual(doc.numLines(), 4)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), "modified")
        self.assertEqual(cursor.pos, (1,1))
        self.assertEqual(doc.lineText(1), 'r!python\n')

        command.undo()
        self.assertEqual(doc.numLines(), 4)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), None)
        self.assertEqual(cursor.pos, (1,1))
        self.assertEqual(doc.lineText(1), '#!python\n')

if __name__ == '__main__':
    unittest.main()
