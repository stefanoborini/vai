from vaitk import gui
from yapsy.PluginManager import PluginManager
import collections
from .. import paths
from ..lexer import token as lexertoken

class SyntaxColors:
    def __init__(self, schema_name, num_colors):
        self._color_map = collections.defaultdict(lambda : (None, None))

        if schema_name != "default" and self._tryLoad(schema_name, num_colors):
            return

        self._installDefault(num_colors)

    def _tryLoad(self, schema_name, num_colors):
        plugin_manager = PluginManager()
        plugin_manager.getPluginLocator().setPluginInfoExtension("ini")
        plugin_manager.setPluginPlaces([paths.pluginsDir("user", "syntaxcolors"), paths.pluginsDir("system", "syntaxcolors")])
        plugin_manager.collectPlugins()

        for plugin_info in plugin_manager.getAllPlugins():

            # Useless, but let's activate them
            plugin_manager.activatePluginByName(plugin_info.name)

            plugin_object = plugin_info.plugin_object
            if plugin_object.name() == schema_name and plugin_object.supportsNumColors(num_colors):

                self._color_map.update(_parseColorSchema(plugin_object.colorSchema(num_colors)))
                return True

        return False

    def _installDefault(self, num_colors):
        self._color_map.update(_parseColorSchema(defaultColorSchema(num_colors)))

    def colorMap(self):
        return self._color_map

def defaultColorSchema(num_colors):
    if num_colors == 8:
        return {
            "Keyword":              "yellow",
            "Keyword.Constant":     "red",
            "Keyword.Pseudo":       "red",
            "Keyword.Namespace":    "magenta",
            "Keyword.Reserved":     "magenta",
            "Keyword.Type":         "magenta",
            "Comment":              "cyan",
            "Comment.Single":       "cyan",
            "Name.Function":        "cyan",
            "Name.Class":           "cyan",
            "Name.Builtin":         "cyan",
            "Name.Exception":       "cyan",
            "String":               "red",
            "Literal":              "red",
            "Literal.String.Doc":   "red",
            "Number":               "red",
            "Number.Integer":       "red",
            "Number.Float":         "red",
            "Number.Hex":           "red",
            "Number.Oct":           "red",
            "Operator.Word":        "yellow",
            "Name.Decorator":       "blue",
            "Name.Builtin.Pseudo":  "green",
        }

    elif num_colors == 256:
        return {
            "Keyword":                        "term_ffd75f",
            "Keyword.Constant":               "lightred",
            "Keyword.Pseudo":                 "lightred",
            "Keyword.Namespace":              "term_af87af",
            "Keyword.Reserved":               "term_af87af",
            "Keyword.Type":                   "term_af87af",
            "Comment":                        "cyan",
            "Comment.Single":                 "cyan",
            "Name.Class":                     "lightcyan",
            "Name.Class.PythonPrivate":       "term_ff5f5f",
            "Name.Builtin":                   "lightcyan",
            "Name.Exception":                 "lightcyan",
            "String":                         "lightred",
            "Literal":                        "lightred",
            "Literal.String.Doc":             "lightred",
            "Number":                         "lightred",
            "Number.Integer":                 "lightred",
            "Number.Float":                   "lightred",
            "Number.Hex":                     "lightred",
            "Number.Oct":                     "lightred",
            "Operator.Word":                  "term_ffd75f",
            "Name.Decorator":                 "blue",
            "Name.Builtin.Pseudo":            "term_5fafd7",
            "Name.Builtin.Pseudo.PythonSelf": "pink",
            "Name.Function":                  "term_5fff5f",
            "Name.Function.PythonPrivate":    "term_ff5f5f",
            "Name.Function.PythonMagic":      "term_5f5fff",
        }

def _parseColorSchema(color_schema_dict):
    result = {}
    for tok, col in color_schema_dict.items():
        result[_token(tok)] = _color(col)

    return result

def _token(token_string):
    """
    Returns a representation useful for the SyntaxColors Plugin.
    token_string is a string describing the token. The names are the one provides
    by pygments, with the addition of some vai specific tokens

    To return a representation of the Keyword token

        token("Keyword")

    To return a representation of the Keyword.Constant token

        token("Keyword.Constant")

    The returned representation is an implementation detail.
    """
    subtokens = token_string.split(".")

    if len(subtokens) == 0:
        return None

    target = lexertoken
    for subtoken in subtokens:
        new_target = target.__dict__.get(subtoken)
        if new_target is None:
            return None
        target = new_target

    return target

def _color(color_string):
    """
    Ease method to produce a representation of a color for the syntax highlighting.
    It can be called in the following ways

    To return a representation of the color blue for the foreground

        color("blue")

    To return a representation of the color blue, with bold character

        color("blue bold")

    To return a representation of blue foreground with white background

        color("blue,white")

    To return a representation of blue bold foreground with white background

        color("blue bold,white")
    """

    fg_bg = color_string.split(",")

    fg, bg_color = fg_bg if len(fg_bg) == 2 else (fg_bg[0], None)
    if bg_color is not None:
        bg_color = bg_color.strip()

    fg_font = fg.split(" ")

    fg_color, fg_font = fg_font if len(fg_font) == 2 else (fg_font[0], None)

    fg_color = fg_color.strip()
    if fg_font is not None:
        fg_font = fg_font.strip()

    return (gui.VGlobalColor.__dict__.get(fg_color), None, gui.VGlobalColor.__dict__.get(bg_color))

