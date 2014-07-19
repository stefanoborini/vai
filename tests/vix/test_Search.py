import unittest
from .. import fixtures
from vix import flags
from vix import Search

class TestSearch(unittest.TestCase):
    def testSearch(self):
        buffer = fixtures.buffer("real_case_editareacontroller.py")
        self.assertEqual(buffer.documentCursor().pos(), (1,1))
        Search.find(buffer, 'Key', direction=flags.FORWARD)
        self.assertEqual(buffer.documentCursor().pos(), (8,28))
        Search.find(buffer, 'Key', direction=flags.FORWARD)
        self.assertEqual(buffer.documentCursor().pos(), (8,32))
        Search.find(buffer, 'Key', direction=flags.FORWARD)
        self.assertEqual(buffer.documentCursor().pos(), (9,28))
        Search.find(buffer, 'Key', direction=flags.BACKWARD)
        self.assertEqual(buffer.documentCursor().pos(), (8,32))



if __name__ == '__main__':
    unittest.main()
