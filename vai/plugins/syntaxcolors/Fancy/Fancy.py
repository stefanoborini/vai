from vai import sdk
from vaitk import gui
from vai.sdk import token, color

class Fancy(sdk.SyntaxColorsPlugin):
    def colorSchema(self, num_colors):
        """
        To be reimplement in the plugin to return a new schema.
        """
        return {
                token("Keyword"):              (color("blue"), None),
                token("Keyword.Constant"):     (color("blue"), None),
                token("Keyword.Pseudo"):       (color("blue"), None),
                token("Keyword.Namespace"):    (color("blue"), None),
                token("Keyword.Reserved"):     (color("blue"), None),
                token("Keyword.Type"):         (color("blue"), None),
                token("Comment"):              (color("blue"), None),
                token("Comment.Single"):       (color("blue"), None),
                token("Name.Function"):        (color("blue"), None),
                token("Name.Class"):           (color("blue"), None),
                token("Name.Builtin"):         (color("blue"), None),
                token("Name.Exception"):       (color("blue"), None),
                token("String"):               (color("blue"), None),
                token("Literal"):              (color("blue"), None),
                token("Literal.String.Doc"):   (color("blue"), None),
                token("Number"):               (color("blue"), None),
                token("Number.Integer"):       (color("blue"), None),
                token("Number.Float"):         (color("blue"), None),
                token("Number.Hex"):           (color("blue"), None),
                token("Number.Oct"):           (color("blue"), None),
                token("Operator.Word"):        (color("blue"), None),
                token("Name.Decorator"):       (color("blue"), None),
                token("Name.Builtin.Pseudo"):  (color("blue"), None),
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

