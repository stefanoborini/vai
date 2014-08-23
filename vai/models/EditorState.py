import os
import copy
import contextlib
import json

class EditorState:
    _instance = None

    @staticmethod
    def editorStatePath():
        return os.path.expanduser("~/.vaistate")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception("Only one instance allowed")

        self._state = {}
        try:
            with contextlib.closing(open(self.editorStatePath(), "r")) as f:
                self._state = json.loads(f.read())
        except:
            self._state = {}

    def setCursorPosForPath(self, absolute_path, cursor_pos):
        if "buffers" not in self._state:
            self._state["buffers"] = []

        buffers = self._state["buffers"]

        for b in buffers:
            if b.get("absolute_path") == absolute_path:
                b["cursor_pos"] = cursor_pos
        else:
            buffers.append( { "absolute_path" : absolute_path,
                              "cursor_pos" : cursor_pos
                            })

    def cursorPosForPath(self, absolute_path):
        buffers = self._state.get("buffers", [])

        for b in buffers:
            if b.get("absolute_path") == absolute_path:
                return tuple(b.get("cursor_pos"))

        return None

    def save(self):
        with contextlib.closing(open(self.editorStatePath(),"w")) as f:
            f.write(json.dumps(self._state))

