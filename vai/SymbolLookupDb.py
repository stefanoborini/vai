class SymbolLookupDb:
    """
    Singleton class. Contains the database storing the various symbols in the current open codes.
    At the moment, this is filled up by the Lexer.
    Implemented as a simple trie. Nothing fancy.
    """

    _db = {}

    @classmethod
    def clear(cls):
        """
        Completely clears the database
        """
        cls._db = {}

    @classmethod
    def add(cls, word):
        """
        Adds a word to the database
        """
        _add(cls._db, word)

    @classmethod
    def lookup(cls, prefix):
        """
        Given a prefix, looks up all entries having that prefix.
        Returns a list of all postfixes, or an empty list if
        nothing is available.
        """
        d = _walkDown(cls._db, prefix)
        if d is None:
            return []

        ret = _composePostfix(d)
        return ret

# Helper routines for the above class

def _add(d, word):
    """
    Recursive function to add a word to the trie
    """
    if len(word) == 0:
        d[''] = None
        return
    if word[0] not in d:
        d[word[0]] = {}

    _add(d[word[0]], word[1:])

def _walkDown(d, prefix):
    """
    Recursive. Performs traversal of the trie given a prefix
    """
    if len(prefix) == 1:
        if prefix[0] not in d:
            return None
        return d[prefix[0]]

    try:
        return _walkDown(d[prefix[0]], prefix[1:])
    except KeyError:
        return None

def _composePostfix(d, tab=0):
    """
    Recursive function. Builds the postfixes list
    from a given trie branch.
    """

    ret = []
    if d is None:
        return ['']

    for k, v in d.items():
        for postfix in _composePostfix(v, tab+1):
            ret.append(k+postfix)

    return ret
