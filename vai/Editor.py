from vaitk import gui, core
import os

from . import widgets
from . import controllers

from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
import logging


class Editor(gui.VWidget):
    def __init__(self, global_state, buffer_list, parent=None):
        super().__init__(parent=parent)

        self._global_state = global_state
        self._buffer_list = buffer_list
        self._controller = controllers.EditorController(self, self._global_state, self._buffer_list)

        self._createStatusBar()
        #self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()

    @property
    def status_bar(self):
        return self._status_bar

    @property
    def edit_area(self):
        return self._edit_area

    @property
    def status_bar_controller(self):
        return self._status_bar_controller

    @property
    def controller(self):
        return self._controller

    def show(self):
        super().show()
#        self._edit_area.setFocus()

    # Private

    def _createStatusBar(self):
        self._status_bar = widgets.StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)
        self._status_bar_controller = controllers.StatusBarController(self._status_bar)
        self._status_bar_controller.buffer = self._buffer_list.current

    """
    def _createCommandBar(self):
        self._command_bar = widgets.CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar_controller = controllers.CommandBarController(self._command_bar, self._controller, self._model.edit_mode)
    """

    def _createSideRuler(self):
        self._side_ruler = widgets.SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (5, self.height()-2) )
        self._side_ruler_controller = controllers.SideRulerController(self._side_ruler)
        self._side_ruler_controller.buffer = self._buffer_list.current

    def _createEditArea(self):
        self._edit_area = EditArea(self._global_state, parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )
        self._edit_area.setFocus()

        #self._edit_area_event_filter = EditAreaEventFilter(self._command_bar, self._global_state)
        #self._edit_area.installEventFilter(self._edit_area_event_filter)

    """
    def _showInfoHoverBoxIfNeeded(self, document_pos):
        current_buffer = self._model.buffer_list.current
        pos_at_top = current_buffer.edit_area_model.document_pos_at_top

        badge = self._side_ruler.badge(document_pos[0])

        if badge is not None:
            gui.VToolTip.showText((0, document_pos[0]-pos_at_top[0]+1), badge.description)
        else:
            gui.VToolTip.hide()
    """
