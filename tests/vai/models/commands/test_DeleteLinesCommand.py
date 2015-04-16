import unittest
from vai import models
from vai.models import commands
from tests import fixtures
from vai import models


class TestDeleteLinesCommand(unittest.TestCase):
    def setUp(self):
        self.buffer = models.Buffer()

        with open(fixtures.get("20_lines.txt"), 'r') as f:
            self.buffer.document.read(f)

    def testDeleteLinesCommand(self):
        command = commands.DeleteLinesCommand(self.buffer, 5, 3)
        result = command.execute()
        self.assertNotEqual(result, None)
        self.assertTrue(result.success)
        self.assertTrue(isinstance(result.info, models.TextDocument))

        self.assertEqual(result.info.numLines(), 3)
        self.assertEqual(result.info.lineText(1), "5\n")
        self.assertEqual(result.info.lineText(2), "6\n")
        self.assertEqual(result.info.lineText(3), "7\n")

    def testUndo(self):
        command = commands.DeleteLinesCommand(self.buffer,5,3)
        result = command.execute()

        self.assertEqual(self.buffer.document.numLines(), 17)

        command.undo()
        self.assertEqual(self.buffer.document.numLines(), 20)

        for i in range(1,21):
            self.assertEqual(self.buffer.document.lineText(i), "%d\n" % i)

if __name__ == '__main__':
    unittest.main()
