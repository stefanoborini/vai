from ..EditorApp import EditorApp
from vai.lexer import token as lexertoken
from vaitk import gui

def application():
    """
    Returns the Vai application
    """

    return EditorApp.vApp

def token(token_string):
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
    return gui.VGlobalColor.__dict__.get(color_string)

