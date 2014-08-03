import unittest
from vixtk import gui, core, test

from vixtk.gui.VScreen import VScreenArea

class TestVScreenArea(unittest.TestCase):
    @unittest.skip
    def testWrite(self):
        screen = test.VTextScreen((30, 30))
        area = VScreenArea(screen, (5, 7, 10, 3))

        area.write((0,0),"0123456789012345")
        area.write((0,1),"123456789012345")
        area.write((0,2),"23456789012345")
        area.write((0,3),"3456789012345")

        self.assertEqual(screen.stringAt(4,6,12), '............')
        self.assertEqual(screen.stringAt(4,7,12), '.0123456789.')
        self.assertEqual(screen.stringAt(4,8,12), '.1234567890.')
        self.assertEqual(screen.stringAt(4,9,12), '.2345678901.')
        self.assertEqual(screen.stringAt(4,10,12),'............')

    @unittest.skip
    def testClear(self):
        screen = test.VTextScreen((30, 30))
        area = VScreenArea(screen, (5, 7, 10, 3))

        area.erase()

        self.assertEqual(screen.stringAt(4,6,12), '............')
        self.assertEqual(screen.stringAt(4,7,12), '.          .')
        self.assertEqual(screen.stringAt(4,8,12), '.          .')
        self.assertEqual(screen.stringAt(4,9,12), '.          .')
        self.assertEqual(screen.stringAt(4,10,12),'............')

if __name__ == '__main__':
    unittest.main()
