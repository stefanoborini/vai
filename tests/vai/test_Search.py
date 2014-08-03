import unittest
from .. import fixtures
from vai import flags
from vai import Search

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

    def testFindAll(self):
        buffer = fixtures.buffer("real_case_editareacontroller.py")
        doc = buffer.document()
        all_finds = Search.findAll(doc, 'Key')
        self.assertEqual(len(all_finds), 65)
        self.assertEqual(all_finds[0], (8, 28, 31))
        self.assertEqual(all_finds[-1], (194, 37, 40))

        all_finds = Search.findAll(doc, 'key_')
        self.assertEqual(len(all_finds), 0)

        all_finds = Search.findAll(doc, 'key_', case_sensitive=False)
        self.assertNotEqual(len(all_finds), 0)

if __name__ == '__main__':
    unittest.main()
