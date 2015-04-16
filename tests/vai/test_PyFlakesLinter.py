import unittest
from vai.linting import PyFlakesLinter
from vai.models import TextDocument
from tests import fixtures

class PyFlakesLinterTest(unittest.TestCase):
    def setUp(self):
        self.document = fixtures.buffer("basic_python.py").document

    def testBasicFunctionality(self):
        linter = PyFlakesLinter(self.document)
        linter.runOnce()

if __name__ == '__main__':
    unittest.main()
