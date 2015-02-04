class CommandPlugin:
    """
    A base class to implement command plugins.
    
    A command plugin is invoked when the : key is used. The first
    word after the colon is the plugin keyword. When the keyword matches,
    the method invoke() is called
    """
    
    def __init__(self, name, version_major, version_minor):
        self._name = name
        self._version_major = version_major
        self._version_minor = version_minor
    
    @property
    def keyword(self):
        raise NotImplementedError()
        
    
    def invoke(self, command_line, editorapp):
        """
        Method that handles the command.
        It receives the full command line and the instance of the Editor application,
        meaning that it can do pretty much everything.
        """
        
        raise NotImplementedError()
        
