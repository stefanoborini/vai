from ..EditorApp import EditorApp
from vai.lexer import token
from vaitk import gui

def application():
    """
    Returns the Vai application
    """

    return EditorApp.vApp

def token(token_string):
    return token.__dict__.get(token_string)

def color(color_string):
    return gui.VGlobalColor.__dict__.get(color_string)

