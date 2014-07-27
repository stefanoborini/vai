import unittest
from vix.SymbolLookupDb import SymbolLookupDb

class TestSymbolLookupDb(unittest.TestCase):
    def testLookup(self):
        symdb = SymbolLookupDb()
        
        symdb.add("TestSymbolLookup")
        symdb.add("TestSymbol")
        symdb.add("testSymbol")
        symdb.add("foo")
        symdb.add("foobar")
        symdb.add("foobaz")
        symdb.add("fooquux")
        
        self.assertEqual(set(symdb.lookup("fo")), set([ "o", "obar", "obaz", "oquux"]) )
        self.assertEqual(set(symdb.lookup("foo")), set([ '', "bar", "baz", "quux"]))
        self.assertEqual(set(symdb.lookup("foob")), set([ "ar", "az"]) )
        self.assertEqual(set(symdb.lookup("Test")), set([ "SymbolLookup", "Symbol" ]))
        self.assertEqual(set(symdb.lookup("xx")), set([]))
        
if __name__ == '__main__':
    unittest.main()
