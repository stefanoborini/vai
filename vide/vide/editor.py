from videtoolkit import gui, core, utils

from .SideRuler import SideRuler
from .SideRulerController import SideRulerController
from .StatusBar import StatusBar
from .StatusBarController import StatusBarController
from .CommandBar import CommandBar
from .EditArea import EditArea
from .EditAreaEventFilter import EditAreaEventFilter
from .ViewModel import ViewModel
from .LineBadge import LineBadge
from . import commands
from . import flags
import logging

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super(Editor, self).__init__(parent=parent)
        self._document_model = document_model
        self._view_model = ViewModel()

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()
        self._edit_area.setFocus()

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move( (0, self.height()-2) )
        self._status_bar.resize( (self.width(), 1) )
        self._status_bar.setFilename(self._document_model.filename())
        self._status_bar_controller = StatusBarController(self._status_bar, self._view_model)

    def _createCommandBar(self):
        self._command_bar = CommandBar(self)
        self._command_bar.move( (0, self.height()-1) )
        self._command_bar.resize( (self.width(), 1) )
        self._command_bar.setMode(flags.COMMAND_MODE)
        self._view_model.modeChanged.connect(self._command_bar.setMode)
        self._command_bar.returnPressed.connect(self.executeCommand)
        self._command_bar.escapePressed.connect(self.abortCommand)

    def _createSideRuler(self):
        self._side_ruler = SideRuler(self)
        self._side_ruler.move( (0, 0) )
        self._side_ruler.resize( (4, self.height()-2) )
        self._side_ruler.addBadge(3,LineBadge(mark="*"))
        self._side_ruler_controller = SideRulerController(self._side_ruler, self._view_model)

    def _createEditArea(self):
        self._edit_area = EditArea(self._document_model, self._view_model, parent = self)
        self._edit_area.move( (4, 0) )
        self._edit_area.resize( (self.width()-4, self.height()-2) )
        self._edit_area.setFocus()

        self._edit_area_event_filter = EditAreaEventFilter(self._view_model, self._command_bar)
        self._edit_area.installEventFilter(self._edit_area_event_filter)

    def viewModelChanged(self):
        self.update()

    def executeCommand(self):
        command_text = self._command_bar.commandText().strip()
        logging.info("Executing command "+command_text)

        if command_text == 'q':
            gui.QApplication.qApp.exit()
        elif command_text == "w":
            self.doSave()

        self._command_bar.clear()
        self._edit_area.setFocus()

    def abortCommand(self):
        logging.info("Aborting command")
        self._command_bar.clear()
        self._view_model.setEditorMode(flags.COMMAND_MODE)
        self._edit_area.setFocus()

    def doSave(self):
        logging.info("Saving file")
        self._document_model.saveAs("output")

    def show(self):
        super(Editor, self).show()
        self._edit_area.setFocus()

