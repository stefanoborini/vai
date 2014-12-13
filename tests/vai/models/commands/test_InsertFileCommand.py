import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestInsertStringCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertFileCommand(self):
        command = commands.InsertFileCommand(self.buffer, fixtures.get("basic_python.py"))
        result = command.execute()
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()
