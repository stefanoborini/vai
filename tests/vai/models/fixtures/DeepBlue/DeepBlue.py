from vai import sdk
from vaitk import gui

class DeepBlue(sdk.SyntaxColorsPlugin):
    """
    This plugin is used to demonstrate the syntax color plugin functionality.
    It's not supposed to be used for development, but if  you do, have fun.
    """
    def colorSchema(self, num_colors):
        """
        This method returns the color schema. You have to return a dictionary
        where the key is a string describing a pygments token, and the value
        is a color as described in vaitk.gui.VColor.VGlobalColor.

        You can also specify background color as

            "blue, white"

        with blue as the foreground (text) color, and white the background color.
        The passed argument num_colors is the current number of colors the terminal
        is set up to represent. It is normally either 8 or 256. You can support both,
        providing a restricted set of colors for the 8 colors mode, or simply focus on one
        or the other. See method supportsNumColors() for details.
        """
        if num_colors == 8:
            return {
                    "Keyword":              "blue",
            }
        else:
            return {
                    "Keyword":              "term_00005f",
            }

    def name(self):
        """
        Return the name of the plugin. As a good practice, keep this equal to the name of your
        plugin and of this class.
        """
        return "DeepBlue"

    def supportsNumColors(self, num_colors):
        """
        Must return True if the plugin is able to provide a color schema for the number of colors
        of the current terminal it is running on. If you want to support both, use the current implementation,
        otherwise just compare against the number of colors you want to support.
        """
        return num_colors in [8, 256]

