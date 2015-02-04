import importlib
import sys
import os
from .. import paths
from .. import Debug
from .. import sdk

class PluginRegistry:
    _instance = None

    def __init__(self):
        self._command_plugins = {}

    @classmethod
    def commandPluginForKeyword(cls, keyword):
        """
        Returns the command plugin for a given keyword, or None if not present
        """
        return cls._instance._command_plugins.get(keyword)

    @classmethod
    def initialize(cls, plugins_dir=None):
        cls._instance = PluginRegistry()

        plugins_dir = plugins_dir or paths.pluginsDir()
        sys.path.insert(0, plugins_dir)

        for d in os.listdir(plugins_dir):
            try:
                module = importlib.import_module(d)
            except:
                pass

            for p in module.plugins():
                if isinstance(p, sdk.CommandPlugin):
                    cls._instance._command_plugins[p.keyword] = p
