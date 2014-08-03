import unittest
import vaitk

class TestVaiTk(unittest.TestCase):
    def testNativeToVaiKeyCode(self):
        self.assertEqual(vaitk.nativeToVaiKeyCode(ord('a')), vaitk.Key.Key_A)
        self.assertEqual(vaitk.nativeToVaiKeyCode(ord('A')), vaitk.Key.Key_A | vaitk.KeyModifier.ShiftModifier)

    def testIsKeyCodePrintable(self):
        self.assertTrue(vaitk.isKeyCodePrintable(vaitk.Key.Key_A))
        self.assertTrue(vaitk.isKeyCodePrintable(vaitk.Key.Key_A|vaitk.KeyModifier.ShiftModifier))
        self.assertFalse(vaitk.isKeyCodePrintable(vaitk.Key.Key_Escape))

    def testVaiKeyCodeToText(self):
        self.assertEqual(vaitk.vaiKeyCodeToText(vaitk.Key.Key_A), 'a')
        self.assertEqual(vaitk.vaiKeyCodeToText(vaitk.Key.Key_Escape), '')

if __name__ == '__main__':
    unittest.main()
