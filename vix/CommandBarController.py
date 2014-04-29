class CommandBarController:
    def __init__(self, command_bar, editor_model):
        self._command_bar = command_bar
        self._editor_model = editor_model
        self._editor_model.modeChanged.connect(self._command_bar.setMode)

