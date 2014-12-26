import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertFileCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertFileCommand(self):
        cursor = self.buffer.cursor
        document = self.buffer.document

        cursor.toPos((1,1))
        command = commands.InsertFileCommand(self.buffer, fixtures.get("basic_python.py"))

        result = command.execute()
        self.assertTrue(result.success)
        self.assertEqual(document.lineText(1), document.lineText(2))
        self.assertEqual(document.numLines(), 8)

    def testUndo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document

        old_lines = [document.lineText(i) for i in range(1,5)]

        cursor.toPos((1,1))
        command = commands.InsertFileCommand(self.buffer, fixtures.get("basic_python.py"))

        result = command.execute()
        
        command.undo() 

        self.assertEqual(document.numLines(), 4)
        for i in range(1,5):
            self.assertEqual(document.lineText(i), old_lines[i-1])

    def testRedo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document


        cursor.toPos((1,1))
        command = commands.InsertFileCommand(self.buffer, fixtures.get("basic_python.py"))

        result = command.execute()

        old_lines = [document.lineText(i) for i in range(1,9)]
        
        command.undo() 
        command.execute()

        self.assertEqual(document.numLines(), 8)
        for i in range(1,9):
            self.assertEqual(document.lineText(i), old_lines[i-1])

if __name__ == '__main__':
    unittest.main()
