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

