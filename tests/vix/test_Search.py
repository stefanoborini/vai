import unittest
from unittest.mock import Mock
from vixtk import gui, test, core
from vix.EditAreaController import EditAreaController
from vix.EditArea import EditArea
from vix.models.EditorModel import EditorModel
from vix.models.Buffer import Buffer
from vixtk.gui import events
from .. import fixtures
import vixtk
from vix import flags
from vix import Search

class TestSearch(unittest.TestCase):
    def testSearch(self):
        buffer = fixtures.buffer("real_case_editareacontroller.py")
        self.assertEqual(buffer.documentCursor().pos(), (1,1))
        Search.find(buffer, 'Key')
        self.assertEqual(buffer.documentCursor().pos(), (8,28))
        Search.find(buffer, 'Key')
        self.assertEqual(buffer.documentCursor().pos(), (8,32))
        Search.find(buffer, 'Key')
        self.assertEqual(buffer.documentCursor().pos(), (9,28))
        Search.find(buffer, 'Key', backwards=True)
        self.assertEqual(buffer.documentCursor().pos(), (8,32))



if __name__ == '__main__':
    unittest.main()
