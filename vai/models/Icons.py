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
                                }

        cls._ICONS["unicode1"] = {
                                 "EditArea.tab"              : "\u254e", # dotted lines
                                 "SideRuler.warning"         : "\u203c", # Double exclamation
                                 "SideRuler.error"           : "\u203c", # Double exclamation
                                 "SideRuler.info"            : "I",
                                 "SideRuler.added"           : "+",
                                 "SideRuler.deletion_before" : "\u21a7", # Arrow
                                 "SideRuler.deletion_after"  : "\u21a5", # Arrow
                                 "SideRuler.modified"        : "\u2023", # Triangle bullet
                                 "SideRuler.unexistent_line" : "~",
                                 "SideRuler.border"          : "\u2551", # double line
                                }


