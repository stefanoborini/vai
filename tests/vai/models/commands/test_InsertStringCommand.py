import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertStringCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        with open(fixtures.get("basic_python.py"), 'r') as f:
            self.buffer.document.read(f)

    def testInsertStringCommand(self):
        command = commands.InsertStringCommand(self.buffer, '')
        result = command.execute()
        self.assertTrue(result.success)

    def testUndo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document
        cursor.toPos((3,1))
        command = commands.InsertStringCommand(self.buffer, 'hello')
        result = command.execute()

        self.assertTrue(result.success)
        self.assertEqual(document.lineText(3), 'hellodef foo():\n')

        command.undo()
        self.assertEqual(document.lineText(3), 'def foo():\n')

    def testRedo(self):
        cursor = self.buffer.cursor
        document = self.buffer.document
        cursor.toPos((3,1))
        command = commands.InsertStringCommand(self.buffer, 'hello')
        result = command.execute()
        command.undo()

        cursor.toPos((1,1))
        command.execute()

        self.assertEqual(document.lineText(3), 'hellodef foo():\n')

if __name__ == '__main__':
    unittest.main()
