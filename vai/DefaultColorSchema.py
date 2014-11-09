from vaitk import gui
from pygments import token
import collections

class DefaultColorSchema:
    def __init__(self):
        self.COLORMAP = collections.defaultdict(lambda : (None, None))
        self.COLORMAP.update({
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
            token.Name.Builtin.Pseudo:  (gui.VGlobalColor.cyan, None),
        })

