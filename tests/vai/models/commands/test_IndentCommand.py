import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestIndent(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testIndent(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        cursor.toPos((1,1))
        
        command = commands.IndentCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), '    #!python\n')
        self.assertEqual(doc.lineMetaInfo("Change").data(1), "modified")
        self.assertEqual(cursor.pos, (1,5))

        command.undo()

        self.assertEqual(doc.lineText(1), "#!python\n")
        self.assertEqual(doc.lineMetaInfo("Change").data(1), None)
        self.assertEqual(cursor.pos, (1,1))

    def testRedoAppliesToOldPlace(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor
        
        cursor.toPos((1,1))

        command = commands.IndentCommand(self.buffer)
        result = command.execute()
        command.undo()
        cursor.toPos((3,1))
        result = command.execute()
        self.assertEqual(cursor.pos, (1,5))
        

if __name__ == '__main__':
    unittest.main()
