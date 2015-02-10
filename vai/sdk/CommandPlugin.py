from yapsy.IPlugin import IPlugin

class CommandPlugin(IPlugin):
    """
    A base class to implement command plugins.

    A command plugin is invoked when the : key is used. The first
    word after the colon is the plugin keyword. When the keyword matches,
    the method execute() is called
    """

    def __init__(self):
        pass

    def name(self):
        """Returns the name of the plugin. To be reimplemented"""
        return None

    def keyword(self):
        """The keyword to activate the plugin."""
        return None

    def execute(self, command_line):
        """
        Method that handles the command.
        It receives the full command line as a string, meaning that it can do pretty much everything.
        If it fails, it's responsibility of the plugin to communicate the error condition.
        Return False if execution failed. True if successful.
        """
        return False

