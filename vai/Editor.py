from vaitk import gui, core
import os

from . import widgets
from .SideRulerController import SideRulerController
from .StatusBarController import StatusBarController
from .CommandBarController import CommandBarController
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .Lexer import Lexer
from .PyFlakesLinter import PyFlakesLinter
from . import flags
from . import Search
from . import models
import logging


class Editor(gui.VWidget):
    def __init__(self, editor_model, parent=None):
        super().__init__(parent=parent)

        self._model = editor_model

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()

        self._initBackupTimer()

        self._controller = EditorController(self, self._model)

    @property
    def status_bar(self):
        return self._status_bar

    @property
    def edit_area(self):
        return self._edit_area

    @property
    def controller(self):
        return self._controller

    @property
    def model(self):
        return self._model

    def show(self):
        super().show()
        self._edit_area.setFocus()

    # Private

    def _createStatusBar(self):
        self._status_bar = widgets.StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)
        self._status_bar_controller = StatusBarController(self._status_bar)

    def _createCommandBar(self):
        self._command_bar = widgets.CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar_controller = CommandBarController(self._command_bar, self._controller)

    def _createSideRuler(self):
        self._side_ruler = widgets.SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (5, self.height()-2) )
        self._side_ruler_controller = SideRulerController(self._side_ruler)

    def _createEditArea(self):
        self._edit_area = EditArea(parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )
        self._edit_area.setFocus()

        self._edit_area_event_filter = EditAreaEventFilter(self._command_bar)
        self._edit_area_event_filter.setModel(self._model)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

    def _showInfoHoverBoxIfNeeded(self, document_pos):
        current_buffer = self._model.buffer_list.current
        pos_at_top = current_buffer.edit_area_model.document_pos_at_top

        badge = self._side_ruler.badge(document_pos[0])

        if badge is not None:
            gui.VToolTip.showText((0, document_pos[0]-pos_at_top[0]+1), badge.description)
        else:
            gui.VToolTip.hide()

