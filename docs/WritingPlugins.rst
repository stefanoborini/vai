Writing plugins for vai
=======================

**Updated to vai 1.6**

Vai has a, for now, simple plugin system based on yapsy. Vai supports two types of plugins at the moment

- Command plugins, which are activated when the user types :sometext while in command mode and presses enter, and
- Syntaxcolor plugins, which are activated on startup to determine the personalized color highlighting of syntax.

Plugin development is made easier by a SDK package provided as vai.sdk. Plugins importing vai.sdk get access to a set
of easy access functions and classes that abstract the inner workings of vai as much as possible, making plugins
more stable in the face of changes in vai and easier to write for the plugin developer.

There are two levels of plugins. The system plugins are shipped with vai, and must be placed in the proper directory under
vai/plugins. User plugins are plugins that are installed by the user, and must go in the proper subdirectory of
~/.local/share/vai/plugins/

All plugins must be contained in their own directory (e.g. MyPlugin). This directory must contain the following files

- MyPlugin.ini : contains information about the plugin, in a simple INI format.
- MyPlugin.py  : This is the "entry point" for the plugin. In most cases, this
                 contains a single class with a proper interface we will explain later.
- __init__.py  : Being a plugin a python package, this file must exist, and in general must be empty

The ini file has the same structure regardless of the plugin type, and must
contain the following entries, which are quite self-explanatory. Module must refer to the MyPlugin.py file containing
the plugin classes

..

    [Core]
    Name = MyPlugin
    Module = MyPlugin.py

    [Documentation]
    Author = Stefano Borini
    Version = 1.0
    Website = http://github.com/stefanoborini/vai
    Description = My first plugin

The content of the MyPlugin.py depends on the actual plugin type.

Writing a SyntaxColor plugin
============================

To write a syntaxcolor plugin, the best starting point is the DeepBlue syntaxcolor plugin, available in vai/plugins/syntaxcolors/.
This is a very dumb syntax color plugin that paints all syntax tokens blue.

The Module file DeepBlue.py must define a class instance of sdk.SyntaxColorsPlugin

..

    class DeepBlue(sdk.SyntaxColorsPlugin):

This class must define three methods:

    - name(self): Returns the name of the plugin as a string.
    - supportsNumColors(self, num_colors): returns True if the plugin supports the passed amount of colors. If you develop a purely 8 colors plugin, return True only if num_colors is 8, False otherwise.
    - colorSchema(self, num_colors): this is the business end of the class. It must return a dictionary associating syntax tokens to colors.


To better explain the last method, see the following examples:

    token("Keyword"):              color("blue"),

This entry associates the "Keyword" token, to the color blue. All keywords will appear as blue, if not specified otherwise with a more specific Keyword identification.

    token("Keyword.Constant"):     (color("white"), color("blue")),

This entry will specialize Constant keywords. They will appear white on a blue background.

The content of the value in the dictionary can be

    - a single entry: that color will be the color of the identifier
    - a tuple with two entries: the first color is the foreground, the second is the background. If the background is None, it is equivalent to the single entry option.

Always use the sdk.color() and sdk.token() functions to create the dictionary.

You can obtain a list of the available tokens from the pygments documentation, and the list of the available colors from
the module vaitk.gui.VColor.VGlobalColors distributed together with vai.

To install the syntaxcolor plugin you have to copy the plugin directory into
~/.local/share/vai/plugins/syntaxcolors/. The new colorscheme will only be used if chosen. You enable it
by editing ~/.config/vai/vairc and setting

    "colors.syntax_schema": "your_syntaxcolor_name",

Writing a command plugin
========================

A command plugin is triggered when the user types a :command while in command mode.
The command plugin is defined as a class derived from sdk.CommandPlugin. Your plugin must reimplement this class
The Time plugin, available in vai/plugins/commands/Time, shows a trivial plugin that sets the current time in the
status bar for 3 seconds.

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
        return True


The name method, as in the case of the syntaxcolors plugins, must return the conventional name for the plugin.
The keyword method must return the keyword that will activate the plugin at the command line. In this case,
typing :time will activate the plugin. When this happens, the execute() method will be called. The full command line
as a string will be passed as an argument.






