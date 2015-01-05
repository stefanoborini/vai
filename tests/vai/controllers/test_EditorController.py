import unittest
from unittest.mock import Mock

from vai import controllers
from vai import models
from vai.Editor import Editor
from vai.linting.LinterResult import LinterResult

from tests import fixtures

class TestEditorController(unittest.TestCase):
    def setUp(self):
        self.mock_editor = Mock(spec=Editor)
        self.buffer_list = models.BufferList()
        self.global_state = models.GlobalState()
        self.editor_controller = controllers.EditorController(self.mock_editor, self.global_state, self.buffer_list)

    def testBug165(self):
        """Check if the linting data is correctly reset every time we perform a lint operation"""
        document = self.buffer_list.current.document
        document.open(fixtures.get("basic_python.py"))
        document.deleteChars((3,9), 1)
        self.editor_controller._doLint()
        self.assertTrue(isinstance(document.lineMetaInfo("LinterResult").data()[2], LinterResult))
        document.insertChars((3,9), ')')
        self.editor_controller._doLint()
        self.assertEqual(document.lineMetaInfo("LinterResult").data()[2], None)
    
if __name__ == '__main__':
    unittest.main()
