"""
Module that wraps and augments the pygment tokens, so that we can provide additional
tokens if we recognize them as having additional properties worth of interest.
"""

from pygments.token import *

# Special tokens for python stuff
PythonSelf = Name.Builtin.Pseudo.PythonSelf
PythonPrivate = Name.Function.PythonPrivate
PythonMagic = Name.Function.PythonMagic


def getTokenByString(token_fqname):
    components = token_fqname.split(".")
    current = globals()
    for c in components:
        if c not in current:
            return None
        else:
            current = current.__dict__[c]
    
    return current

