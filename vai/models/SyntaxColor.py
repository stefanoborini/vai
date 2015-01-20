import os
import json
from vaitk import gui
import collections
from .. import Debug
from .. import paths
from ..lexer import token

class SyntaxColor:
    def __init__(self, schema_name, num_colors):
        self._color_map = collections.defaultdict(lambda : (None, None))
        
        if schema_name == "default":
            self._installDefault(num_colors)
            return

        found = self._tryLoad(schema_name, num_colors)

        if not found:
            self._installDefault(num_colors) 

    def _tryLoad(self, schema_name, num_colors):
        schema_file = os.path.join(paths.syntaxColorDir(), "%s_%d.json" % (schema_name, num_colors))
        if not os.path.isfile(schema_file):
            return False

        try:
            with open(schema_file, "r") as f:
                data = json.loads(f.read())

            color_map = {}
            for k, v in data.items():
                tok = token.string_to_tokentype(k)

                fg_string, bg_string = v
                if fg_string is not None and hasattr(gui.VGlobalColor, fg_string):
                    fg = getattr(gui.VGlobalColor, fg_string)
                else:
                    fg = None

                if bg_string is not None and hasattr(gui.VGlobalColor, bg_string):
                    bg = getattr(gui.VGlobalColor, bg_string)
                else:
                    bg = None

                color_map[tok] = (fg, bg)
        except:
            raise
            return False

        self._color_map.update(color_map)
        return True

    def _installDefault(self, num_colors):
        if num_colors == 8:
            self._color_map.update({
                token.Keyword:              (gui.VGlobalColor.yellow, None),
                token.Keyword.Constant:     (gui.VGlobalColor.darkred, None),
                token.Keyword.Pseudo:       (gui.VGlobalColor.darkred, None),
                token.Keyword.Namespace:    (gui.VGlobalColor.darkmagenta, None),
                token.Keyword.Reserved:     (gui.VGlobalColor.darkmagenta, None),
                token.Keyword.Type:         (gui.VGlobalColor.darkmagenta, None),
                token.Comment:              (gui.VGlobalColor.darkcyan, None),
                token.Comment.Single:       (gui.VGlobalColor.darkcyan, None),
                token.Name.Function:        (gui.VGlobalColor.lightcyan, None),
                token.Name.Class:           (gui.VGlobalColor.lightcyan, None),
                token.Name.Builtin:         (gui.VGlobalColor.lightcyan, None),
                token.Name.Exception:       (gui.VGlobalColor.lightcyan, None),
                token.String:               (gui.VGlobalColor.darkred, None),
                token.Literal:              (gui.VGlobalColor.darkred, None),
                token.Literal.String.Doc:   (gui.VGlobalColor.darkred, None),
                token.Number:               (gui.VGlobalColor.darkred, None),
                token.Number.Integer:       (gui.VGlobalColor.darkred, None),
                token.Number.Float:         (gui.VGlobalColor.darkred, None),
                token.Number.Hex:           (gui.VGlobalColor.darkred, None),
                token.Number.Oct:           (gui.VGlobalColor.darkred, None),
                token.Operator.Word:        (gui.VGlobalColor.yellow, None),
                token.Name.Decorator:       (gui.VGlobalColor.darkblue, None),
                token.Name.Builtin.Pseudo:  (gui.VGlobalColor.green, None),
            })

        elif num_colors == 256:
            self._color_map.update({
                token.Keyword:              (gui.VGlobalColor.yellow, None),
                token.Keyword.Constant:     (gui.VGlobalColor.darkred, None),
                token.Keyword.Pseudo:       (gui.VGlobalColor.darkred, None),
                token.Keyword.Namespace:    (gui.VGlobalColor.darkmagenta, None),
                token.Keyword.Reserved:     (gui.VGlobalColor.darkmagenta, None),
                token.Keyword.Type:         (gui.VGlobalColor.darkmagenta, None),
                token.Comment:              (gui.VGlobalColor.darkcyan, None),
                token.Comment.Single:       (gui.VGlobalColor.darkcyan, None),
                token.Name.Function:        (gui.VGlobalColor.lightcyan, None),
                token.Name.Class:           (gui.VGlobalColor.lightcyan, None),
                token.Name.Builtin:         (gui.VGlobalColor.lightcyan, None),
                token.Name.Exception:       (gui.VGlobalColor.lightcyan, None),
                token.String:               (gui.VGlobalColor.darkred, None),
                token.Literal:              (gui.VGlobalColor.darkred, None),
                token.Literal.String.Doc:   (gui.VGlobalColor.darkred, None),
                token.Number:               (gui.VGlobalColor.darkred, None),
                token.Number.Integer:       (gui.VGlobalColor.darkred, None),
                token.Number.Float:         (gui.VGlobalColor.darkred, None),
                token.Number.Hex:           (gui.VGlobalColor.darkred, None),
                token.Number.Oct:           (gui.VGlobalColor.darkred, None),
                token.Operator.Word:        (gui.VGlobalColor.yellow, None),
                token.Name.Decorator:       (gui.VGlobalColor.darkblue, None),
                token.Name.Builtin.Pseudo:  (gui.VGlobalColor.pink, None),
            })

    def colorMap(self):
        return self._color_map
