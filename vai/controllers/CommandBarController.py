import shlex
from .. import models

class CommandBarController:
    def __init__(self, command_bar, edit_area, editor_controller, global_state):
        self._command_bar = command_bar
        self._edit_area = edit_area
        self._editor_controller = editor_controller
        self._global_state = global_state

        self._command_bar.returnPressed.connect(self._parseCommandBar)
        self._command_bar.escapePressed.connect(self._abortCommandBar)

        self._global_state.editorModeChanged.connect(self._editorModeChanged)

    # Private

    def _parseCommandBar(self):
        command_text = self._command_bar.command_text
        mode = self._global_state.editor_mode
        self._global_state.editor_mode = models.EditorMode.COMMAND

        if mode == models.EditorMode.COMMAND_INPUT:
            if self._interpretLine(command_text):
                self._command_bar.clear()
        elif mode == models.EditorMode.SEARCH_FORWARD:
            self._editor_controller.searchForward(command_text)
            self._command_bar.clear()
        elif mode == models.EditorMode.SEARCH_BACKWARD:
            self._editor_controller.searchBackward(command_text)
            self._command_bar.clear()

        self._edit_area.setFocus()

    def _abortCommandBar(self):
        self._command_bar.clear()
        self._global_state.editor_mode = models.EditorMode.COMMAND
        self._edit_area.setFocus()

    def _editorModeChanged(self, *args):
        self._command_bar.editor_mode = self._global_state.editor_mode

    def _interpretLine(self, command_text):
        command = shlex.split(command_text)
        if command[0] == 'q!':
            self._editor_controller.forceQuit()
        elif command[0] == 'q':
            self._editor_controller.tryQuit()
        elif command[0] == "w":
            if len(command) == 1:
                self._editor_controller.doSave()
            elif len(command) == 2:
                self._editor_controller.doSaveAs(command[1])
            else:
                self._reportError("Only one filename allowed at write")
                return False
        elif command[0] == "r":
            if len(command) == 1:
                self._reportError("Specify filename")
                return False
            elif len(command) == 2:
                self._editor_controller.doInsertFile(command[1])
            else:
                self._reportError("Only one filename allowed")
                return False
        elif command[0] in ("wq", "x"):
            self._editor_controller.doSaveAndExit()
        elif command[0] == "e":
            if len(command) == 1:
                self._reportError("Specify filename")
            elif len(command) == 2:
                self._editor_controller.openFile(command[1])
            else:
                self._reportError("Only one filename allowed")
                return False
        elif command[0] == "bp":
            self._editor_controller.selectPrevBuffer()
        elif command[0] == "bn":
            self._editor_controller.selectNextBuffer()
        else:
            self._reportError("Unknown command")
            return False
        return True

    def _reportError(self, error_string):
        self._command_bar.setErrorString(error_string)
