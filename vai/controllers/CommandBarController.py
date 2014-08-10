from .. import models

class CommandBarController:
    def __init__(self, command_bar, editor_controller, edit_mode):
        self._command_bar = command_bar
        self._editor_controller = editor_controller
        self._edit_mode = edit_mode

        self._command_bar.returnPressed.connect(self._parseCommandBar)
        self._command_bar.escapePressed.connect(self._abortCommandBar)

        self._edit_mode.changed.connect(self._modeChanged)

    # Private

    def _parseCommandBar(self):
        command_text = self._command_bar.commandText().strip()
        mode = self._edit_mode.mode

        if mode == models.EditMode.COMMAND_INPUT:
            if command_text == 'q!':
                self._editor_controller.forceQuit()
            elif command_text == 'q':
                self._editor_controller.quit()
            elif command_text == "w":
                self._editor_controller.doSave()
            elif command_text == "wq":
                self._editor_controller.doSaveAndExit()
            elif command_text.startswith("e "):
                self._editor_controller.openFile(command_text[2:])
            elif command_text.startswith("bp"):
                self._editor_controller.selectPrevBuffer()
            elif command_text.startswith("bn"):
                self._editor_controller.selectNextBuffer()
        elif mode == models.EditMode.SEARCH_FORWARD:
                self._editor_controller.searchForward(command_text)
        elif mode == models.EditMode.SEARCH_BACKWARD:
                self._editor_controller.searchBackward(command_text)

        self._command_bar.clear()
        self._edit_mode.mode = flags.COMMAND_MODE
        self._edit_area.setFocus()

    def _abortCommandBar(self):
        self._command_bar.clear()
        self._edit_mode.mode = flags.COMMAND_MODE
        self._edit_area.setFocus()

    def _modeChanged(self, *args):
        self._command_bar.setMode(self._edit_mode.mode)


        #QQQSBO    def _bufferChanged(self, old_buffer, new_buffer):
#QQQSBO        self._status_bar_controller.setModels(new_buffer.document, new_buffer.cursor)
#QQQSBO        self._side_ruler_controller.setModels(new_buffer.document, new_buffer.edit_area_model)
#QQQSBO        self._edit_area.setModels(new_buffer, self._editor_model)
#QQQSBO        if old_buffer:
#QQQSBO            old_buffer.cursor.positionChanged.disconnect(self._showInfoHoverBoxIfNeeded)
#QQQSBO        new_buffer.cursor.positionChanged.connect(self._showInfoHoverBoxIfNeeded)
#QQQSBO        self._lexer.setModel(new_buffer.document)

