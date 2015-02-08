from vai import sdk
import time

class TimePlugin(sdk.CommandPlugin):
    def name(self):
        """
        To be reimplement in the plugin
        """
        return "Time"

    def keyword(self):
        return "time"

    def execute(self, command_line):
        sdk.statusBar().setMessage(time.asctime(), 3000)
