from .. import Debug
from vaitk import gui
from yapsy.PluginManager import PluginManager
import collections
from .. import paths
from ..lexer import token

class SyntaxColors:
    def __init__(self, schema_name, num_colors):
        self._color_map = collections.defaultdict(lambda : (None, None))

        if schema_name != "default" and self._tryLoad(schema_name, num_colors):
            return

        self._installDefault(num_colors)

    def _tryLoad(self, schema_name, num_colors):
        Debug.log("trying loading "+str(schema_name))
        plugin_manager = PluginManager()
        plugin_manager.getPluginLocator().setPluginInfoExtension("ini")
        plugin_manager.setPluginPlaces([paths.pluginsDir("user", "syntaxcolors"), paths.pluginsDir("system", "syntaxcolors")])
        plugin_manager.collectPlugins()

        for plugin_info in plugin_manager.getAllPlugins():
            Debug.log("plugin found "+str(plugin_info.name))
            plugin_manager.activatePluginByName(plugin_info.name)

            plugin_object = plugin_info.plugin_object
            if plugin_object.name() == schema_name and plugin_object.supportsNumColors(num_colors):
                self._color_map.update(plugin_object.colorSchema(num_colors))
                return True

        return False

    def _installDefault(self, num_colors):
        self._color_map.update(defaultColorSchema(num_colors))

    def colorMap(self):
        return self._color_map

def defaultColorSchema(num_colors):
    if num_colors == 8:
        return {
            token.Keyword:              (gui.VGlobalColor.yellow, None),
            token.Keyword.Constant:     (gui.VGlobalColor.red, None),
            token.Keyword.Pseudo:       (gui.VGlobalColor.red, None),
            token.Keyword.Namespace:    (gui.VGlobalColor.magenta, None),
            token.Keyword.Reserved:     (gui.VGlobalColor.magenta, None),
            token.Keyword.Type:         (gui.VGlobalColor.magenta, None),
            token.Comment:              (gui.VGlobalColor.cyan, None),
            token.Comment.Single:       (gui.VGlobalColor.cyan, None),
            token.Name.Function:        (gui.VGlobalColor.cyan, None),
            token.Name.Class:           (gui.VGlobalColor.cyan, None),
            token.Name.Builtin:         (gui.VGlobalColor.cyan, None),
            token.Name.Exception:       (gui.VGlobalColor.cyan, None),
            token.String:               (gui.VGlobalColor.red, None),
            token.Literal:              (gui.VGlobalColor.red, None),
            token.Literal.String.Doc:   (gui.VGlobalColor.red, None),
            token.Number:               (gui.VGlobalColor.red, None),
            token.Number.Integer:       (gui.VGlobalColor.red, None),
            token.Number.Float:         (gui.VGlobalColor.red, None),
            token.Number.Hex:           (gui.VGlobalColor.red, None),
            token.Number.Oct:           (gui.VGlobalColor.red, None),
            token.Operator.Word:        (gui.VGlobalColor.yellow, None),
            token.Name.Decorator:       (gui.VGlobalColor.blue, None),
            token.Name.Builtin.Pseudo:  (gui.VGlobalColor.green, None),
        }

    elif num_colors == 256:
        return {
            token.Keyword:                        (gui.VGlobalColor.term_ffd75f, None),
            token.Keyword.Constant:               (gui.VGlobalColor.lightred, None),
            token.Keyword.Pseudo:                 (gui.VGlobalColor.lightred, None),
            token.Keyword.Namespace:              (gui.VGlobalColor.term_af87af, None),
            token.Keyword.Reserved:               (gui.VGlobalColor.term_af87af, None),
            token.Keyword.Type:                   (gui.VGlobalColor.term_af87af, None),
            token.Comment:                        (gui.VGlobalColor.cyan, None),
            token.Comment.Single:                 (gui.VGlobalColor.cyan, None),
            token.Name.Class:                     (gui.VGlobalColor.lightcyan, None),
            token.Name.Class.PythonPrivate:       (gui.VGlobalColor.term_ff5f5f, None),
            token.Name.Builtin:                   (gui.VGlobalColor.lightcyan, None),
            token.Name.Exception:                 (gui.VGlobalColor.lightcyan, None),
            token.String:                         (gui.VGlobalColor.lightred, None),
            token.Literal:                        (gui.VGlobalColor.lightred, None),
            token.Literal.String.Doc:             (gui.VGlobalColor.lightred, None),
            token.Number:                         (gui.VGlobalColor.lightred, None),
            token.Number.Integer:                 (gui.VGlobalColor.lightred, None),
            token.Number.Float:                   (gui.VGlobalColor.lightred, None),
            token.Number.Hex:                     (gui.VGlobalColor.lightred, None),
            token.Number.Oct:                     (gui.VGlobalColor.lightred, None),
            token.Operator.Word:                  (gui.VGlobalColor.yellow, None),
            token.Name.Decorator:                 (gui.VGlobalColor.blue, None),
            token.Name.Builtin.Pseudo:            (gui.VGlobalColor.term_5fafd7, None),
            token.Name.Builtin.Pseudo.PythonSelf: (gui.VGlobalColor.pink, None),
            token.Name.Function:                  (gui.VGlobalColor.term_5fff5f, None),
            token.Name.Function.PythonPrivate:    (gui.VGlobalColor.term_ff5f5f, None),
            token.Name.Function.PythonMagic:      (gui.VGlobalColor.term_5f5fff, None),
        }

