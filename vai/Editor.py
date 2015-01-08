from vaitk import gui

from . import widgets
from . import controllers

from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .InfoHoverBox import InfoHoverBox


class Editor(gui.VWidget):
    """
    Widget responsible for handling the overall aspect of the editor,
    aggregating the different components.
    """

    def __init__(self, global_state, buffer_list, parent=None):
        super().__init__(parent=parent)

        self._global_state = global_state
        self._buffer_list = buffer_list
        self._controller = controllers.EditorController(self, self._global_state, self._buffer_list)

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()
        self._createInfoHoverBox()

        self._status_bar_controller = controllers.StatusBarController(self._status_bar)
        self._side_ruler_controller = controllers.SideRulerController(self._side_ruler)
        self._command_bar_controller = controllers.CommandBarController(self._command_bar, self._edit_area, self._controller, self._global_state)
        self._edit_area_event_filter = EditAreaEventFilter(self._command_bar, self._global_state, self._buffer_list)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

        self._controller.registerCurrentBuffer()

    def show(self):
        super().show()
        self._edit_area.setFocus()

    # properties

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
    def side_ruler_controller(self):
        return self._side_ruler_controller

    @property
    def controller(self):
        return self._controller

    @property
    def info_hover_box(self):
        return self._info_hover_box

    # Private

    def _createStatusBar(self):
        self._status_bar = widgets.StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )

    def _createCommandBar(self):
        self._command_bar = widgets.CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )

    def _createSideRuler(self):
        self._side_ruler = widgets.SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (7, self.height()-2) )

    def _createEditArea(self):
        self._edit_area = EditArea(self._global_state, self._controller, parent = self)
        self._edit_area.move( (7, 0) )
        self._edit_area.resize((self.width()-4, self.height()-2) )

    def _createInfoHoverBox(self):
        self._info_hover_box = InfoHoverBox(self)

