from .VColor import VColor
import copy

class VPalette(object):
    class ColorGroup(object):
        Active, Disabled, Inactive = range(3)

    class ColorRole(object):
        WindowText, \
        Button, \
        Light, \
        Midlight, \
        Dark, \
        Mid, \
        Text, \
        BrightText, \
        ButtonText, \
        Base, \
        Window, \
        Shadow, \
        Highlight, \
        HighlightedText, \
        Link, \
        LinkVisited, \
        AlternateBase, \
        NoRole, \
        ToolTipBase, \
        ToolTipText = range(20)

    def __init__(self):
        self._colors = {}

    def color(self, color_group, color_role):
        return self._colors[(color_group, color_role)]

    def setColor(self, color_group, color_role, color):
        self._colors[(color_group, color_role)] = color

    def setDefaults(self):
        self._colors = {
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Button) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Light) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Midlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Dark) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Mid) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Text) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.BrightText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.ButtonText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Base) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Window) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Shadow) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Highlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.HighlightedText) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.Link) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.LinkVisited) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.AlternateBase) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.NoRole) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipBase) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.WindowText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Button) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Light) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Midlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Dark) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Mid) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Text) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.BrightText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.ButtonText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Base) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Window) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Shadow) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Highlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.HighlightedText) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.Link) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.LinkVisited) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.AlternateBase) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.NoRole) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.ToolTipBase) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Disabled, VPalette.ColorRole.ToolTipText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.WindowText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Button) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Light) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Midlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Dark) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Mid) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Text) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.BrightText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.ButtonText) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Base) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Window) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Shadow) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Highlight) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.HighlightedText) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.Link) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.LinkVisited) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.AlternateBase) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.NoRole) : VColor( rgb = (255,255,255)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.ToolTipBase) : VColor( rgb = (0,0,0)),
            ( VPalette.ColorGroup.Inactive, VPalette.ColorRole.ToolTipText) : VColor( rgb = (255,255,255))
            }

    def copy(self):
        return copy.deepcopy(self)

