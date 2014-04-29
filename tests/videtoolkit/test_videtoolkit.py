import unittest
import videtoolkit

class TestVideToolkit(unittest.TestCase):

    def testNativeToVideKeyCode(self):
        self.assertEqual(videtoolkit.nativeToVideKeyCode(ord('a')), videtoolkit.Key.Key_A)
        self.assertEqual(videtoolkit.nativeToVideKeyCode(ord('A')), videtoolkit.Key.Key_A | videtoolkit.KeyModifier.ShiftModifier)

    def testIsKeyCodePrintable(self):
        self.assertTrue(videtoolkit.isKeyCodePrintable(videtoolkit.Key.Key_A))
        self.assertTrue(videtoolkit.isKeyCodePrintable(videtoolkit.Key.Key_A|videtoolkit.KeyModifier.ShiftModifier))
        self.assertFalse(videtoolkit.isKeyCodePrintable(videtoolkit.Key.Key_Escape))

    def testVideKeyCodeToText(self):
        self.assertEqual(videtoolkit.videKeyCodeToText(videtoolkit.Key.Key_A), 'a')
        self.assertEqual(videtoolkit.videKeyCodeToText(videtoolkit.Key.Key_Escape), '')
if __name__ == '__main__':
    unittest.main()
