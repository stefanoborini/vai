import unittest
from videtoolkit import gui, core

from videtoolkit.gui.VScreen import DummyVScreen
from videtoolkit.gui.VScreen import VScreenArea

class TestVScreenArea(unittest.TestCase):
    def testWrite(self):
        screen = DummyVScreen(30, 30)
        area = VScreenArea(screen, core.VRect(top_left=core.VPoint(x=5, y=7),
                                         size=core.VSize(width=10, height=3)))

        area.write(core.VPoint(0,0),"0123456789012345")
        area.write(core.VPoint(0,1),"123456789012345")
        area.write(core.VPoint(0,2),"23456789012345")
        area.write(core.VPoint(0,3),"3456789012345")

        self.assertEqual(screen.stringAt(4,6,12), '............')
        self.assertEqual(screen.stringAt(4,7,12), '.0123456789.')
        self.assertEqual(screen.stringAt(4,8,12), '.1234567890.')
        self.assertEqual(screen.stringAt(4,9,12), '.2345678901.')
        self.assertEqual(screen.stringAt(4,10,12),'............')

    def testClear(self):
        screen = DummyVScreen(30, 30)
        area = VScreenArea(screen, core.VRect(top_left=core.VPoint(5, 7), size=core.VSize(10, 3)))

        area.erase()

        self.assertEqual(screen.stringAt(4,6,12), '............')
        self.assertEqual(screen.stringAt(4,7,12), '.          .')
        self.assertEqual(screen.stringAt(4,8,12), '.          .')
        self.assertEqual(screen.stringAt(4,9,12), '.          .')
        self.assertEqual(screen.stringAt(4,10,12),'............')

if __name__ == '__main__':
    unittest.main()
