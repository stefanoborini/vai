from vaitk import gui
from pygments import token
import collections

class Icons:
    _ICONS = None

    @classmethod
    def getCollection(cls, collection_name):
        if cls._ICONS is None:
            cls._initIcons()
        return cls._ICONS[collection_name]

    @classmethod
    def _initIcons(cls):
        cls._ICONS = {}
        cls._ICONS["ascii"] = {
                                 "tabulator"       : ".",
                                 "warning"         : "W",
                                 "error"           : "E",
                                 "info"            : "I",
                                 "added"           : "+",
                                 "deletion_before" : "_",
                                 "deletion_after"  : "^",
                                 "modified"        : ".",
                                 "unexistent_line" : "~",
                                 "vertical_border" : "|",
                                 "bookmarks"       : "abcdefghijklmnopqrstuvwxyz"
                                }

        cls._ICONS["unicode1"] = {
                                 "tabulator"       : "\u254e", # dotted lines
                                 "warning"         : "\u203c", # Double exclamation
                                 "error"           : "\u203c", # Double exclamation
                                 "info"            : "I",
                                 "added"           : "+",
                                 "deletion_before" : "\u2304", # Arrow
                                 "deletion_after"  : "\u2303", # Arrow
                                 "modified"        : "\u25fe", # Square
                                 "unexistent_line" : "~",
                                 "vertical_border" : "\u2551", # Double line
                                 "bookmarks"       : "\u24D0"+ # Circled letters
                                                     "\u24D1"+
                                                     "\u24D2"+
                                                     "\u24D3"+
                                                     "\u24D4"+
                                                     "\u24D5"+
                                                     "\u24D6"+
                                                     "\u24D7"+
                                                     "\u24D8"+
                                                     "\u24D9"+
                                                     "\u24DA"+
                                                     "\u24DB"+
                                                     "\u24DC"+
                                                     "\u24DD"+
                                                     "\u24DE"+
                                                     "\u24DF"+
                                                     "\u24E0"+
                                                     "\u24E1"+
                                                     "\u24E2"+
                                                     "\u24E3"+
                                                     "\u24E4"+
                                                     "\u24E5"+
                                                     "\u24E6"+
                                                     "\u24E7"+
                                                     "\u24E8"+
                                                     "\u24E9"+
                                                     "\u24B6"+
                                                     "\u24B7"+
                                                     "\u24B8"+
                                                     "\u24B9"+
                                                     "\u24BA"+
                                                     "\u24BB"+
                                                     "\u24BC"+
                                                     "\u24BD"+
                                                     "\u24BE"+
                                                     "\u24BF"+
                                                     "\u24C0"+
                                                     "\u24C1"+
                                                     "\u24C2"+
                                                     "\u24C3"+
                                                     "\u24C4"+
                                                     "\u24C5"+
                                                     "\u24C6"+
                                                     "\u24C7"+
                                                     "\u24C8"+
                                                     "\u24C9"+
                                                     "\u24CA"+
                                                     "\u24CB"+
                                                     "\u24CC"+
                                                     "\u24CD"+
                                                     "\u24CE"+
                                                     "\u24CF"
                                }


