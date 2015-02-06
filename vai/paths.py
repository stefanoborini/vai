"""
Module that centralizes specific paths we have an interest on.
"""

import os

def configFile():
    """
    Returns the default configuration path in agreement with XDG rules
    """
    config_dir = configDir()
    return os.path.join(config_dir, 'vairc')

def configDir():
    """
    Returns the default configuration dir in agreement with XDG rules
    """
    home = os.path.expanduser('~')
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
                      os.path.join(home, '.config')
    config_dir = os.path.join(xdg_config_home, 'vai')
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    return config_dir

def stateDir():
    home = os.path.expanduser('~')
    xdg_state_home = os.environ.get('XDG_STATE_HOME') or \
                     os.path.join(home, '.local', 'state')
    state_dir = os.path.join(xdg_state_home, 'vai')
    if not os.path.isdir(state_dir):
        os.makedirs(state_dir)
    return state_dir

def stateFile():
    state_dir = stateDir()
    return os.path.join(state_dir, 'vaistate')

def userPluginsDir():
    """Where to search for plugins"""
    path = os.path.join(os.path.expanduser('~'),
                        '.local',
                        'share',
                        'vai',
                        'plugins'
                       )
    if not os.path.isdir(path):
        os.makedirs(path)

    return path

def userSyntaxColorsDir():
    """Where to search for syntax highlight schemes"""
    path = os.path.join( userPluginsDir(), 'syntaxcolors')
    if not os.path.isdir(path):
        os.makedirs(path)

    return path

def systemPluginsDir():
    """Where to search for plugins"""
    return os.path.join( os.path.dirname(os.path.abspath(__file__)), 'plugins')

def systemSyntaxColorsDir():
    """Where to search for syntax highlight schemes"""
    return os.path.join( systemPluginsDir(), 'syntaxcolors')
