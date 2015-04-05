import unittest
from vai import models
from vai.models import commands
from tests import fixtures


class TestDeleteLinesCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()
        self.buffer.document.open(fixtures.get("basic_python.py"))

    def testDeleteLineAtCursorCommand1(self):
        removed_line = self.buffer.document.lineText(1)

        command = commands.DeleteLinesCommand(self.buffer, 2, 2)
        result = command.execute()
        self.assertNotEqual(result, None)
        self.assertTrue(result.success)


if __name__ == '__main__':
    unittest.main()
