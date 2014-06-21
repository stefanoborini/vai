import unittest
from vixtk import utils

class TestUtils(unittest.TestCase):

    def testStrFormat(self):
        self.assertEqual(utils.strformat([], 40), " "*40)
        self.assertEqual(utils.strformat([(0, "hello"), (10, "ciao"), (30, "whatever")], 40),
                                          "hello     ciao                whatever  ")
                                         # 01234567890123456789012345678901234567890
        self.assertEqual(utils.strformat([(0, "hello"), (5, "ciao"), (36, "whatever")], 40),
                                          "hellociao                           what")
                                         # 01234567890123456789012345678901234567890
        self.assertEqual(utils.strformat([(0, "hello"), (3, "ciao"), (36, "whatever")], 40),
                                          "helciao                             what")
                                         # 01234567890123456789012345678901234567890

        self.assertEqual(utils.strformat([(10, "hello"), (23, "ciao"), (36, "whatever")], 40),
                                          "          hello        ciao         what")
                                         # 01234567890123456789012345678901234567890

        self.assertEqual(utils.strformat([(10, "hello"), (3, "ciao"), (36, "whatever")], 40),
                                          "   ciao   hello                     what")
                                         # 01234567890123456789012345678901234567890


if __name__ == '__main__':
    unittest.main()
