import unittest
import os
import inspect
import sys
from vaitk import test, gui, core
from vai import PyFlakesLinter
from vai.models import TextDocument
from tests import fixtures

class PyFlakesLinterTest(unittest.TestCase):
    def setUp(self):
        self.document = TextDocument.TextDocument(fixtures.get("basic_python.py"))

    def testBasicFunctionality(self):
        linter = PyFlakesLinter.PyFlakesLinter(self.document)
        linter.runOnce()

if __name__ == '__main__':
    unittest.main()
