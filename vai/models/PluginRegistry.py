import importlib
from .. import paths

class PluginRegistry:
    _instance = None

    def __init__(self):
        self._command_plugins = {}

    @classmethod
    def commandPluginForKeyword(cls, keyword):
        """
        Returns the command plugin for a given keyword, or None if not present
        """
        return cls._instance.command_plugins.get(keyword)



    @classmethod
    def initialize():

        plugin_dir = paths.pluginsDir()

        for d in os.listdir(plugin_dir):
            try:
                importlib.import_module()

