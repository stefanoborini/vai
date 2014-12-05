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
                                 "EditArea.tab" : ".",
                                 "SideRuler.warning" : "W",
                                 "SideRuler.error"   : "E",
                                 "SideRuler.error"   : "I",
                                 "SideRuler.added"   : "+",
                                 "SideRuler.deletion_before" : "_",
                                 "SideRuler.deletion_after"  : "^",
                                 "SideRuler.modified"        : ".",
                                 "SideRuler.unexistent_line" : "~",
                                 "SideRuler.border"          : "|",
                                 "SideRuler.bookmarks"       : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                                }

        cls._ICONS["unicode1"] = {
                                 "EditArea.tab"              : "\u254e", # dotted lines
                                 "SideRuler.warning"         : "\u203c", # Double exclamation
                                 "SideRuler.error"           : "\u203c", # Double exclamation
                                 "SideRuler.info"            : "I",
                                 "SideRuler.added"           : "+",
                                 "SideRuler.deletion_before" : "\u2304", # Arrow
                                 "SideRuler.deletion_after"  : "\u2303", # Arrow
                                 "SideRuler.modified"        : "\u25a0", # Square
                                 "SideRuler.unexistent_line" : "~",
                                 "SideRuler.border"          : "\u2551", # double line
                                 "SideRuler.bookmarks"       : "\u24B6"+
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
                                                               "\u24CF"+
                                                               "\u24D0"+
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
                                                               "\u24E9"
                                }


