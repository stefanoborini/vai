class SymbolLookupDb:
    def __init__(self):
        self._db = {}
    
    def add(self, word):
        _add(self._db, word)
    
    def lookup(self, prefix):
        d = _walkDown(self._db, prefix)    
        if d is None:
            return []
        
        ret = _composePostfix(d)
        return ret
            
def _add(d, word):
    if len(word) == 0:
        d[''] = None
        return
    if word[0] not in d:
        d[word[0]] = {}
    
    _add(d[word[0]], word[1:])

def _walkDown(d, prefix):
    if len(prefix) == 1:
        return d[prefix[0]]
    
    if prefix[0] not in d:
        return None
        
    return _walkDown(d[prefix[0]], prefix[1:])
    
def _composePostfix(d, tab=0):
    ret = []
    if d is None:
        return ['']

    for k, v in d.items():
        for postfix in _composePostfix(v, tab+1):
            ret.append(k+postfix)
    
    return ret    
