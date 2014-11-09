from vaitk import gui
from pygments import token
import collections

class DefaultColorSchema:
    def __init__(self):
        # test
        self.COLORMAP = collections.defaultdict(lambda : (None, None))
        self.COLORMAP.update({
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

