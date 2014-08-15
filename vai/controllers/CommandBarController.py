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

        if mode == models.EditorMode.COMMAND_INPUT:
            if command_text == 'q!':
                self._editor_controller.forceQuit()
            elif command_text == 'q':
                self._editor_controller.tryQuit()
            elif command_text == "w":
                self._editor_controller.doSave()
            elif command_text.startswith("w "):
                self._editor_controller.doSaveAs(command_text[2:])
            elif command_text == "wq":
                self._editor_controller.doSaveAndExit()
            elif command_text.startswith("e "):
                self._editor_controller.openFile(command_text[2:])
            elif command_text.startswith("bp"):
                self._editor_controller.selectPrevBuffer()
            elif command_text.startswith("bn"):
                self._editor_controller.selectNextBuffer()
        elif mode == models.EditorMode.SEARCH_FORWARD:
                self._editor_controller.searchForward(command_text)
        elif mode == models.EditorMode.SEARCH_BACKWARD:
                self._editor_controller.searchBackward(command_text)

        self._command_bar.clear()
        self._global_state.editor_mode = models.EditorMode.COMMAND
        self._edit_area.setFocus()

    def _abortCommandBar(self):
        self._command_bar.clear()
        self._global_state.editor_mode = models.EditorMode.COMMAND
        self._edit_area.setFocus()

    def _editorModeChanged(self, *args):
        self._command_bar.editor_mode = self._global_state.editor_mode


