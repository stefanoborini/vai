from yapsy.IPlugin import IPlugin
from ..models import SyntaxColors

class SyntaxColorsPlugin(IPlugin):
    def defaultSchema(num_colors=None):
        """
        Returns the default color schema for a given number of colors,
        or for the current number of colors if not specified
        """
        num_colors = num_colors or self.numColors()
        return SyntaxColors.defaultColorSchema(num_colors)

    def getSchema(self, num_colors):
        """
        To be reimplement in the plugin to return a new schema.
        """
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()

    def supportsNumColors(self, num_colors):
        return False
