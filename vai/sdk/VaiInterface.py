from ..EditorApp import EditorApp
from vai.lexer import token as lexertoken
from vaitk import gui

def application():
    """
    Returns the Vai application.
    """

    return EditorApp.vApp

def statusBar():
    """
    Returns the application's status bar.
    """
    return application().editor.status_bar

def token(token_string):
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

def color(color_string):
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

    The representation is an implementation detail that is not important.
    """

    fg_bg = color_string.split(",")

    fg, bg_color = fg_bg if len(fg_bg) == 2 else (fg_bg[0], None)

    fg_font = fg.split(" ")

    fg_color, fg_font = fg_font if len(fg_font) == 2 else (fg_font[0], None)

    return (gui.VGlobalColor.__dict__.get(fg_color), None, gui.VGlobalColor.__dict__.get(bg_color))

