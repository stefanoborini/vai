import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestBreakLineCommands(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testAtBeginningOfLine(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        line = doc.lineText(1)
        cursor.toPos((1,1))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), '\n')
        self.assertEqual(doc.lineText(2), line)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), "added")

        command.undo()

        self.assertEqual(self.buffer.document.lineText(1), line)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), None)
        self.assertEqual(cursor.pos, (1,1))

    def testAtCenterLine(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        saved_line = doc.lineText(1)
        doc.lineMetaInfo("Change")
        doc.lineMetaInfo("Change")
        self.assertEqual(doc.numLines(), 4)

        cursor.toPos((1,4))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), saved_line[:3]+'\n')
        self.assertEqual(doc.lineText(2), saved_line[3:])
        self.assertEqual(doc.lineMetaInfo("Change").data(1), "modified")
        self.assertEqual(doc.lineMetaInfo("Change").data(2), "added")
        self.assertEqual(doc.numLines(), 5)
        self.assertEqual(cursor.pos, (2,1))

        command.undo()

        self.assertEqual(doc.lineText(1), saved_line)
        self.assertEqual(doc.lineMetaInfo("Change").data(1), None)
        self.assertEqual(doc.numLines(), 4)
        self.assertEqual(cursor.pos, (1,4))

    def testBreakLineCommandAtEndOfLine(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor
        cursor.toLineEnd()
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), '#!python\n')
        self.assertEqual(doc.lineText(2), '\n')
        self.assertEqual(doc.lineText(3), '\n')

        command.undo()

    def testBreakStripsSpaces(self):
        """Test if breaking a line removes the excess spaces"""
        doc = self.buffer.document
        cursor = self.buffer.cursor

        doc.insertLine(1, "foo          bar")
        cursor.toPos((1,6))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertEqual(doc.lineText(1), "foo  \n")
        self.assertEqual(doc.lineText(2), "bar\n")

    def testRedoAppliesToOldPlace(self):
        doc = self.buffer.document
        cursor = self.buffer.cursor

        saved_line_1 = doc.lineText(1)
        saved_line_3 = doc.lineText(3)
        self.assertEqual(doc.numLines(), 4)

        cursor.toPos((1,4))
        command = commands.BreakLineCommand(self.buffer)
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), saved_line_1[:3]+'\n')
        self.assertEqual(doc.lineText(2), saved_line_1[3:])

        command.undo()

        cursor.toPos((3,1))
        
        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(doc.lineText(1), saved_line_1[:3]+'\n')
        self.assertEqual(doc.lineText(2), saved_line_1[3:])
        self.assertEqual(doc.lineText(4), saved_line_3)
        self.assertEqual(cursor.pos, (2,1))
        

if __name__ == '__main__':
    unittest.main()
