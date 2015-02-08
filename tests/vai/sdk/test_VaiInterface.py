import unittest
from vai import sdk

class TestVaiInterface(unittest.TestCase):
    def testColor(self):
        self.assertIsNotNone(sdk.color("blue"))

    def testToken(self):
        self.assertIsNotNone(sdk.token("Keyword"))
        self.assertIsNotNone(sdk.token("Keyword.Constant"))

if __name__ == '__main__':
    unittest.main()
