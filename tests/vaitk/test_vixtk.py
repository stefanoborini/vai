import unittest
import vixtk

class TestVixTk(unittest.TestCase):
    def testNativeToVixKeyCode(self):
        self.assertEqual(vixtk.nativeToVixKeyCode(ord('a')), vixtk.Key.Key_A)
        self.assertEqual(vixtk.nativeToVixKeyCode(ord('A')), vixtk.Key.Key_A | vixtk.KeyModifier.ShiftModifier)

    def testIsKeyCodePrintable(self):
        self.assertTrue(vixtk.isKeyCodePrintable(vixtk.Key.Key_A))
        self.assertTrue(vixtk.isKeyCodePrintable(vixtk.Key.Key_A|vixtk.KeyModifier.ShiftModifier))
        self.assertFalse(vixtk.isKeyCodePrintable(vixtk.Key.Key_Escape))

    def testVixKeyCodeToText(self):
        self.assertEqual(vixtk.vixKeyCodeToText(vixtk.Key.Key_A), 'a')
        self.assertEqual(vixtk.vixKeyCodeToText(vixtk.Key.Key_Escape), '')

if __name__ == '__main__':
    unittest.main()
