import unittest
from .. import fixtures
from vai import Search

class TestSearch(unittest.TestCase):
    def testSearch(self):
        buffer = fixtures.buffer("real_case_editareacontroller.py")
        self.assertEqual(buffer.cursor.pos, (1,1))
        Search.find(buffer, 'Key', direction=Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (8,28))
        Search.find(buffer, 'Key', direction=Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (8,32))
        Search.find(buffer, 'Key', direction=Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (9,28))
        Search.find(buffer, 'Key', direction=Search.SearchDirection.BACKWARD)
        self.assertEqual(buffer.cursor.pos, (8,32))

    def testFindAll(self):
        buffer = fixtures.buffer("real_case_editareacontroller.py")
        doc = buffer.document
        all_finds = Search.findAll(doc, 'Key')
        self.assertEqual(len(all_finds), 65)
        self.assertEqual(all_finds[0], (8, 28, 31))
        self.assertEqual(all_finds[-1], (194, 37, 40))

        all_finds = Search.findAll(doc, 'key_')
        self.assertEqual(len(all_finds), 0)

        all_finds = Search.findAll(doc, 'key_', case_sensitive=False)
        self.assertNotEqual(len(all_finds), 0)

    def testBug113(self):
        buffer = fixtures.buffer("bug_113")
        doc = buffer.document
        all_finds = Search.findAll(doc, 'all')
        self.assertEqual(len(all_finds), 4)
        self.assertEqual(all_finds, [(1, 7, 10), (2, 1, 4), (3, 1, 4), (4, 6, 9)])

    def testBug113Find(self):
        buffer = fixtures.buffer("bug_113")
        all_finds = Search.find(buffer, 'all', Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (1,7))
        all_finds = Search.find(buffer, 'all', Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (2,1))
        all_finds = Search.find(buffer, 'all', Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (3,1))
        all_finds = Search.find(buffer, 'all', Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (4,6))
        all_finds = Search.find(buffer, 'all', Search.SearchDirection.FORWARD)
        self.assertEqual(buffer.cursor.pos, (1,7))

if __name__ == '__main__':
    unittest.main()
