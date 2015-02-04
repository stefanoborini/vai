import os
import json
from vaitk import gui
import collections
from .. import paths
from ..lexer import token

class SyntaxColor:
    def __init__(self, schema_name, num_colors):
        self._color_map = collections.defaultdict(lambda : (None, None))
        
        self._installDefault(num_colors)

        if schema_name != "default":
            self._tryLoad(schema_name, num_colors)

    def _tryLoad(self, schema_name, num_colors):
        schema_file = os.path.join(paths.syntaxColorDir(), "%s_%d.json" % (schema_name, num_colors))
        if not os.path.isfile(schema_file):
            return 

        try:
            with open(schema_file, "r") as f:
                data = json.loads(f.read())

            for k, v in data.items():
                tok = token.string_to_tokentype(k)

                fg_string, bg_string = v
                fg = gui.VGlobalColor.nameToColor(fg_string)
                bg = gui.VGlobalColor.nameToColor(bg_string)

                self._color_map[tok] = (fg, bg)
        except:
            pass

    def _installDefault(self, num_colors):
        if num_colors == 8:
            self._color_map.update({
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
            })

        elif num_colors == 256:
            self._color_map.update({
                token.Keyword:                        (gui.VGlobalColor.term_ffd75f, None),
                token.Keyword.Constant:               (gui.VGlobalColor.red, None),
                token.Keyword.Pseudo:                 (gui.VGlobalColor.red, None),
                token.Keyword.Namespace:              (gui.VGlobalColor.term_af87af, None),
                token.Keyword.Reserved:               (gui.VGlobalColor.term_af87af, None),
                token.Keyword.Type:                   (gui.VGlobalColor.term_af87af, None),
                token.Comment:                        (gui.VGlobalColor.cyan, None),
                token.Comment.Single:                 (gui.VGlobalColor.cyan, None),
                token.Name.Class:                     (gui.VGlobalColor.lightcyan, None),
                token.Name.Class.PythonPrivate:       (gui.VGlobalColor.term_ff5f5f, None),
                token.Name.Builtin:                   (gui.VGlobalColor.lightcyan, None),
                token.Name.Exception:                 (gui.VGlobalColor.lightcyan, None),
                token.String:                         (gui.VGlobalColor.red, None),
                token.Literal:                        (gui.VGlobalColor.red, None),
                token.Literal.String.Doc:             (gui.VGlobalColor.red, None),
                token.Number:                         (gui.VGlobalColor.red, None),
                token.Number.Integer:                 (gui.VGlobalColor.red, None),
                token.Number.Float:                   (gui.VGlobalColor.red, None),
                token.Number.Hex:                     (gui.VGlobalColor.red, None),
                token.Number.Oct:                     (gui.VGlobalColor.red, None),
                token.Operator.Word:                  (gui.VGlobalColor.yellow, None),
                token.Name.Decorator:                 (gui.VGlobalColor.blue, None),
                token.Name.Builtin.Pseudo:            (gui.VGlobalColor.term_5fafd7, None),
                token.Name.Builtin.Pseudo.PythonSelf: (gui.VGlobalColor.brown, None),
                token.Name.Function:                  (gui.VGlobalColor.term_5fff5f, None),
                token.Name.Function.PythonPrivate:    (gui.VGlobalColor.term_ff5f5f, None),
                token.Name.Function.PythonMagic:      (gui.VGlobalColor.term_5f5fff, None),
            })

    def colorMap(self):
        return self._color_map
