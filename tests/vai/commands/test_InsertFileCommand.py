import unittest
from vai.models.Buffer import Buffer
from vai.models.TextDocument import TextDocument
from vai.models.EditAreaModel import EditAreaModel
from vai import commands
from tests import fixtures


class TestInsertStringCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testInsertFileCommand(self):
        command = commands.InsertFileCommand(self.buffer, fixtures.get("basic_python.py"))
        result = command.execute()
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()
