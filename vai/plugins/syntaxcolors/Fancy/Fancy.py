from vai import sdk
from vaitk import gui
from vai.lexer import token

class Fancy(sdk.SyntaxColorsPlugin):
    def colorSchema(self, num_colors):
        """
        To be reimplement in the plugin to return a new schema.
        """
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
                token.Keyword:                        (gui.VGlobalColor.blue, None),
                token.Keyword.Constant:               (gui.VGlobalColor.blue, None),
                token.Keyword.Pseudo:                 (gui.VGlobalColor.blue, None),
                token.Keyword.Namespace:              (gui.VGlobalColor.blue, None),
                token.Keyword.Reserved:               (gui.VGlobalColor.blue, None),
                token.Keyword.Type:                   (gui.VGlobalColor.blue, None),
                token.Comment:                        (gui.VGlobalColor.blue, None),
                token.Comment.Single:                 (gui.VGlobalColor.blue, None),
                token.Name.Class:                     (gui.VGlobalColor.blue, None),
                token.Name.Class.PythonPrivate:       (gui.VGlobalColor.blue, None),
                token.Name.Builtin:                   (gui.VGlobalColor.blue, None),
                token.Name.Exception:                 (gui.VGlobalColor.blue, None),
                token.String:                         (gui.VGlobalColor.blue, None),
                token.Literal:                        (gui.VGlobalColor.blue, None),
                token.Literal.String.Doc:             (gui.VGlobalColor.blue, None),
                token.Number:                         (gui.VGlobalColor.blue, None),
                token.Number.Integer:                 (gui.VGlobalColor.blue, None),
                token.Number.Float:                   (gui.VGlobalColor.blue, None),
                token.Number.Hex:                     (gui.VGlobalColor.blue, None),
                token.Number.Oct:                     (gui.VGlobalColor.blue, None),
                token.Operator.Word:                  (gui.VGlobalColor.blue, None),
                token.Name.Decorator:                 (gui.VGlobalColor.blue, None),
                token.Name.Builtin.Pseudo:            (gui.VGlobalColor.blue, None),
                token.Name.Builtin.Pseudo.PythonSelf: (gui.VGlobalColor.blue, None),
                token.Name.Function:                  (gui.VGlobalColor.blue, None),
                token.Name.Function.PythonPrivate:    (gui.VGlobalColor.blue, None),
                token.Name.Function.PythonMagic:      (gui.VGlobalColor.blue, None),
            }

    def name(self):
        """
        To be reimplement in the plugin
        """
        return "Fancy"

    def supportsNumColors(self, num_colors):
        """
        To be reimplement in the plugin
        """
        return num_colors in [8, 256]

