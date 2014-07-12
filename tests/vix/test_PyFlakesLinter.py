import unittest
import os
import inspect
import sys
from vixtk import test, gui, core
from vix import PyFlakesLinter
from vix.models import TextDocument

def baseDir():
    return os.path.dirname(inspect.getfile(sys.modules[__name__]))

def fixture(name):
    return os.path.join(baseDir(), "fixtures", name)

class PyFlakesLinterTest(unittest.TestCase):
    def setUp(self):
        self.document = TextDocument.TextDocument(fixture("basic_python.py"))

    def testBasicFunctionality(self):
        linter = PyFlakesLinter.PyFlakesLinter(self.document)
        linter.runOnce()

if __name__ == '__main__':
    unittest.main()
