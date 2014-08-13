from vaitk import gui

def stringToColor(string):
    return {"cyan" : gui.VGlobalColor.cyan,
            "blue" : gui.VGlobalColor.blue
            }.get(string, None)

