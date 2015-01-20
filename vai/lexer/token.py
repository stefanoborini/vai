"""
Module that wraps and augments the pygment tokens, so that we can provide additional
tokens if we recognize them as having additional properties worth of interest.
"""

from pygments.token import *

# Special tokens for python stuff
PythonSelf = Name.Builtin.Pseudo.PythonSelf
PythonPrivate = Name.Function.PythonPrivate
PythonMagic = Name.Function.PythonMagic


