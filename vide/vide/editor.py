import videtoolkit
from videtoolkit import gui, core, utils

from .SideRuler import SideRuler
from .StatusBar import StatusBar
from .CommandBar import CommandBar
from . import commands
from collections import namedtuple
from . import flags
import logging
import curses
import math


DocumentPos = namedtuple('DocumentPos', ['row', 'column'])
CursorPos = namedtuple('CursorPos', ['x', 'y'])

class LineBadge(object):
    def __init__(self, mark, description=None, fg_color=None, bg_color=None):
       self._mark = mark
       self._description = description
       self._fg_color = fg_color
       self._bg_color = bg_color

    def mark():
        return self._mark

class ViewModel(core.VObject):
    def __init__(self):
        super(ViewModel, self).__init__()
        self._editor_mode = flags.COMMAND_MODE
        self._document_pos_at_top = DocumentPos(1,1)
        self._badges = {}
        self.changed = core.VSignal(self)

    def editorMode(self):
        return self._editor_mode

    def setEditorMode(self, mode):
        self._editor_mode = mode
        self.changed.emit()

    def documentPosAtTop(self):
        return self._document_pos_at_top

    def setDocumentPosAtTop(self, doc_pos):
        self._document_pos_at_top = doc_pos
        self.changed.emit()

    def addBadge(self, doc_line, badge):
        self._badges[doc_line] = badge
        self.changed.emit()

    def badge(self, doc_line):
        return self._badges.get(doc_line)

DIRECTIONAL_KEYS = [ videtoolkit.Key.Key_Up,
                     videtoolkit.Key.Key_Down,
                     videtoolkit.Key.Key_Left,
                     videtoolkit.Key.Key_Right ]


class EditorController(core.VObject):
    def __init__(self, document_model, view_model, view):
        self._document_model = document_model
        self._view_model = view_model
        self._view = view
        self._command_history = []

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._view.handleDirectionalKey(event)
            event.accept()
            return

        if self._view_model.editorMode() == flags.INSERT_MODE:
            if event.key() == videtoolkit.Key.Key_Escape:
                self._view_model.setEditorMode(flags.COMMAND_MODE)
            elif event.key() == videtoolkit.Key.Key_Backspace:
                self._view.moveCursor(flags.LEFT)
                self._document_model.deleteAt(self._view.cursorToDocumentPos(),1)
            elif event.key() == videtoolkit.Key.Key_Return:
                self._document_model.breakAt(self._view.cursorToDocumentPos())
                self._view.moveCursor(flags.DOWN)
                self._view.moveCursor(flags.HOME)
            else:
                self._document_model.insertAt(self._view.cursorToDocumentPos(), event.text())
                self._view.moveCursor(flags.RIGHT)

        if self._view_model.editorMode() == flags.COMMAND_MODE:
            if event.key() == videtoolkit.Key.Key_I and event.modifiers() == 0:
                self._view_model.setEditorMode(flags.INSERT_MODE)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() == 0:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.cursorToDocumentPos().row+1)
                self._command_history.append(command)
                command.execute()
                self._view.moveCursor(flags.DOWN)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._view_model.setEditorMode(flags.INSERT_MODE)
                command = commands.CreateLineCommand(self._document_model, self._view.cursorToDocumentPos().row)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_U and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                if len(self._command_history):
                    command = self._command_history.pop()
                    command.undo()


            event.accept()


class EditArea(gui.VWidget):
    def __init__(self, document_model, view_model, parent):
        super(EditArea, self).__init__(parent)

        self._controller = EditorController(document_model, view_model, self)

        self._document_model = document_model
        self._view_model = view_model
        self._cursor_pos = CursorPos(0,0)

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        painter.clear( (0, 0, w, h))
        for i in xrange(0, h):
            document_line = self._view_model.documentPosAtTop()[1]+i
            if document_line < self._document_model.numLines():
                painter.write( (0, i), self._document_model.getLine(document_line).replace('\n', ' '))

        gui.VCursor.setPos( self.mapToGlobal(self._cursor_pos))

    def cursorPos(self):
        return self._cursor_pos

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)
        self.update()

    def cursorToDocumentPos(self):
        top_pos = self._view_model.documentPosAtTop()
        doc_pos = DocumentPos(top_pos.row+self.cursorPos().y, top_pos.column+self.cursorPos().x)
        if doc_pos.row > self._document_model.numLines():
            return None

        line_length = self._document_model.lineLength(doc_pos.row)
        if doc_pos.column > line_length+1:
            return None

        return doc_pos

    def handleDirectionalKey(self, event):
        if self._document_model.isEmpty():
            return

        key = event.key()

        direction = { videtoolkit.Key.Key_Up: flags.UP,
                      videtoolkit.Key.Key_Down: flags.DOWN,
                      videtoolkit.Key.Key_Left: flags.LEFT,
                      videtoolkit.Key.Key_Right: flags.RIGHT
                    }[key]

        self.moveCursor(direction)

    def moveCursor(self, direction):
        cursor_pos = self.cursorPos()
        current_doc_pos = self.cursorToDocumentPos()
        current_surrounding_lines_length = {}
        for offset in [-1, 0, 1]:
            line_num=current_doc_pos.row+offset
            if self._document_model.hasLine(line_num):
                current_surrounding_lines_length[offset] = self._document_model.lineLength(line_num)
            else:
                current_surrounding_lines_length[offset] = None

        mode_offset = 0 if self._view_model.editorMode() == flags.INSERT_MODE else -1

        if direction == flags.UP:
            if current_surrounding_lines_length[-1] is None:
                return
            new_pos = CursorPos( min(cursor_pos.x, current_surrounding_lines_length[-1]+mode_offset),
                                 max(cursor_pos.y-1, 0)
                      )
        elif direction == flags.DOWN:
            if current_surrounding_lines_length[1] is None:
                return
            new_pos = CursorPos(min(cursor_pos.x, current_surrounding_lines_length[1]+mode_offset),
                                min(cursor_pos.y+1, self.height()-1)
                      )
        elif direction == flags.LEFT:
            new_pos = CursorPos(max(cursor_pos.x-1,0), cursor_pos.y)
        elif direction == flags.RIGHT:
            new_pos = CursorPos(min(cursor_pos.x+1,
                           current_surrounding_lines_length[0]+mode_offset,
                           self.width()-1),
                       cursor_pos.y
                       )
        elif direction == flags.HOME:
            new_pos = CursorPos(0, cursor_pos.y)

        self._cursor_pos = new_pos
        #new_doc_pos = self.cursorToDocumentPos(new_pos)
        #self._status_bar.setPosition(new_doc_pos)
        gui.VCursor.setPos( self.mapToGlobal(new_pos))



class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super(Editor, self).__init__(parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._view_model.changed.connect(self.viewModelChanged)

        self._createStatusBar()
        self._createCommandBar()
        self._createSideRuler()
        self._createEditArea()

        self._edit_area.setFocus()

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)
        self._status_bar.setFilename(self._document_model.filename())

    def _createCommandBar(self):
        self._command_bar = CommandBar(self)
        self._command_bar.move(0, self.size()[1]-1)
        self._command_bar.resize(self.size()[0], 1)
        self._command_bar.setMode(flags.COMMAND_MODE)

    def _createSideRuler(self):
        self._side_ruler = SideRuler(self)
        self._side_ruler.move(0, 0)
        self._side_ruler.resize(4, self.size()[1]-2)

    def _createEditArea(self):
        self._edit_area = EditArea(self._document_model, self._view_model, parent = self)
        self._edit_area.move(4, 0)
        self._edit_area.resize(self.size()[0]-4, self.size()[1]-3)

    def viewModelChanged(self):
        self.update()

