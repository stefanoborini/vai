import unittest
from vai.models.Buffer import Buffer
from vai.models.BufferList import BufferList
from unittest.mock import Mock

class TestBufferList(unittest.TestCase):
    def testBufferInit(self):

        buffer_list = BufferList()
        self.assertEqual(len(buffer_list.buffers), 0)
        self.assertIsNone(buffer_list.current)

    def testAdd(self):
        b = Mock(spec=Buffer)
        blist = BufferList()
        self.assertEqual(blist.add(b), b)

        self.assertEqual(len(blist.buffers), 1)

    def testSelection(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        blist = BufferList()

        self.assertEqual(blist.add(b1), b1)
        self.assertIsNone(blist.current)

        self.assertEqual(blist.addAndSelect(b2), b2)
        self.assertEqual(blist.current, b2)

        self.assertEqual(blist.select(b1), b1)
        self.assertEqual(blist.current, b1)

    def testPrevNextSelection(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        b3 = Mock(spec=Buffer)
        blist = BufferList()

        blist.add(b1)
        blist.add(b2)
        blist.add(b3)

        self.assertIsNone(blist.current)
        self.assertIsNone(blist.selectPrev())
        self.assertIsNone(blist.current)
        self.assertIsNone(blist.selectNext())
        self.assertIsNone(blist.current)

        blist.select(b2)
        self.assertEqual(blist.selectNext(), b3)

        blist.select(b2)
        self.assertEqual(blist.selectPrev(), b1)

        blist.select(b3)
        self.assertEqual(blist.selectNext(), b1)

        blist.select(b3)
        self.assertEqual(blist.selectPrev(), b2)

        blist.select(b1)
        self.assertEqual(blist.selectNext(), b2)

        blist.select(b1)
        self.assertEqual(blist.selectPrev(), b3)

    def testReplaceAndSelect(self):
        b1 = Mock(spec=Buffer)
        b2 = Mock(spec=Buffer)
        b3 = Mock(spec=Buffer)
        blist = BufferList()

        blist.add(b1)
        blist.add(b2)
        self.assertIsNone(blist.current)

        self.assertEqual(blist.replaceAndSelect(b2, b3), b3)
        self.assertEqual(blist.current, b3)

        self.assertNotIn(b2, blist.buffers)


if __name__ == '__main__':
    unittest.main()
