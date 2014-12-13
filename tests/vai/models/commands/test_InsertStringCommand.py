import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertStringCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertStringCommand(self):
        command = commands.InsertStringCommand(self.buffer, '')
        result = command.execute()
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()
