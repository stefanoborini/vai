import unittest
from vai import paths
import os

class PathsTest(unittest.TestCase):
    def testSystemPluginsDir(self):
        self.assertEqual(paths.systemPluginsDir(),
                         os.path.abspath(
                            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..",
                                         "..",
                                         "vai",
                                         "plugins"
                                         )
                                        )
                        )
    def testSystemSyntaxColorsDir(self):
        self.assertEqual(paths.systemSyntaxColorsDir(),
                         os.path.abspath(
                            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..",
                                         "..",
                                         "vai",
                                         "plugins",
                                         "syntaxcolors"
                                         )
                                        )
                        )

if __name__ == '__main__':
    unittest.main()
