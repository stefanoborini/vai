import os
import contextlib
import unittest
from tests import fixtures
from vai.models import EditorState

class TestConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._editor_state_path_orig = EditorState.editorStatePath

    @classmethod
    def tearDownClass(cls):
        EditorState.editorStatePath = cls._editor_state_path_orig

    def tearDown(self):
        EditorState._instance = None

    def testInit(self):
        f = fixtures.tempFile("not_there_editor_state")
        EditorState.editorStatePath = lambda x : f
        state = EditorState.instance()
        self.assertEqual(state._state, {})

    def testSaveBufferCursorPos(self):
        f = fixtures.tempFile("editor_state")
        EditorState.editorStatePath = lambda x : f
        state = EditorState.instance()

        state.setCursorPosForPath("foobar", (1,2))
        self.assertEqual(state.cursorPosForPath('foobar'), (1,2))

        state.save()
        self.assertTrue(os.path.exists(f))
        with contextlib.closing(open(f, "r")) as tmp:
            # Just checking lengths. the order is arbitrary.
            self.assertEqual(len(tmp.read()),
                            len("{'buffers': [{'absolute_path': 'foobar', 'cursor_pos': [1, 2]}]}"))

    def testGetBufferCursorPos(self):
        f = fixtures.get("editor_state")
        EditorState.editorStatePath = lambda x : f
        state = EditorState.instance()

        self.assertEqual(state.cursorPosForPath('foobar'), (1,2))
        self.assertEqual(state.cursorPosForPath('notpresent'), None)



if __name__ == '__main__':
    unittest.main()
