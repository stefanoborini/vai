import videtoolkit
from videtoolkit import gui, core, utils
from . import commands
import logging
import curses
import math

COMMAND_MODE = -1
INSERT_MODE = 1

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
        self._editor_mode = COMMAND_MODE
        self._document_pos_at_top = (0,0)
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

class StatusBar(gui.VLabel):
    def __init__(self, parent):
        super(StatusBar,self).__init__("", parent)
        self._filename = ""
        self._position = ""
        self.setColors(gui.VGlobalColor.cyan, gui.VGlobalColor.blue)

    def setFilename(self, filename):
        self._filename = filename
        self._updateText()

    def setPosition(self, row, col):
        self._position = str(row)+","+str(col)
        self._updateText()

    def _updateText(self):
        self.setText(utils.strformat([(0, self._filename),
                                      (self.width()-len(self._position)-3, self._position)
                                     ], self.width()))

class CommandBar(gui.VLabel):
    def __init__(self, view_model, parent=None):
        super(CommandBar,self).__init__(parent)
        self._view_model = view_model
        self._view_model.changed.connect(self.updateContent)
        self._mode = None
        self._updateText()

    def _updateText(self):
        if self._mode == INSERT_MODE:
            self.setText("-- INSERT --")
        else:
            self.setText("")

    def setMode(self, mode):
        self._mode = mode
        self._updateText()

    def updateContent(self):
        self.setMode(self._view_model.state())

class EditorController(core.VObject):
    def __init__(self, document_model, view_model, view):
        self._document_model = document_model
        self._view_model = view_model
        self._view = view
        self._command_history = []

    def handleKeyEvent(self, event):
        if event.key() in DIRECTIONAL_KEYS:
            logging.info("Directional key")
            self._view.moveCursor(event)
            event.accept()
            return

        if self._view_model.state() == INSERT_MODE:
            if event.key() == videtoolkit.Key.Key_Escape:
                self._view_model.setState(COMMAND_MODE)
                event.accept()
            return

        if self._view_model.state() == COMMAND_MODE:
            if event.key() == videtoolkit.Key.Key_I and event.modifiers() == 0:
                self._view_model.setState(INSERT_MODE)
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() == 0:
                self._view_model.setState(INSERT_MODE)
                command = commands.InsertLineAfterCommand(self._document_model, 2)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_O and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                self._view_model.setState(INSERT_MODE)
                command = commands.InsertLineBeforeCommand(self._document_model, 2)
                self._command_history.append(command)
                command.execute()
            elif event.key() == videtoolkit.Key.Key_U and event.modifiers() & videtoolkit.KeyModifier.ShiftModifier:
                if len(self._command_history):
                    command = self._command_history.pop()
                    command.undo()


            event.accept()

class Editor(gui.VWidget):
    def __init__(self, document_model, parent=None):
        super(Editor, self).__init__(parent)
        self._document_model = document_model
        self._view_model = ViewModel()
        self._view_model.changed.connect(self.viewModelChanged)
        self._controller = EditorController(self._document_model, self._view_model, self)

        self._createStatusBar()

        self._edit_area_cursor_pos = (0,0)
        gui.VCursor.setPos(
                            *self.mapToGlobal(
                                *self.editAreaCursorPosToWidgetPos(
                                    self.editAreaCursorPos()
                                )
                            )
                        )
        self.setFocus()

    def _createStatusBar(self):
        self._status_bar = StatusBar(self)
        self._status_bar.move(0, self.size()[1]-2)
        self._status_bar.resize(self.size()[0], 1)
        self._status_bar.setFilename(self._document_model.filename())


    def statusBar(self):
        return self._status_bar

    def paintEvent(self, event):
        w, h = self.size()
        painter = gui.VPainter(self)
        num_digits = self.lineNumberWidth()
        for i in xrange(0, h-2):
            painter.clear(0, i, w, 1)
            document_line = self._view_model.documentPosAtTop()[1]+i
            if document_line < self._document_model.numLines():
                badge = self._view_model.badge(document_line)
                if badge is None:
                    badge_mark = " "*self.badgeAreaWidth()
                else:
                    badge_mark = badge.mark()
                painter.write(0, i, str(document_line).rjust(num_digits) + \
                                    badge_mark + \
                                    " " \
                            )
                painter.write(self.leftBorderWidth(), i, self._document_model.getLine(document_line))
            else:
                painter.write(0, i, "~")

    def editAreaCursorToDocumentPos(self, edit_area_cursor_pos):
        top_pos = self._view_model.documentPosAtTop()
        doc_pos = (top_pos[0]+edit_area_cursor_pos[0], top_pos[1]+edit_area_cursor_pos[1])
        if doc_pos[1] < 0 or doc_pos[1] > self._document_model.numLines():
            return None

        line_length = self._document_model.lineLength(doc_pos[1])
        if doc_pos[0] < 0 or doc_pos[0] > line_length:
            return None

        return doc_pos

    def editAreaCursorPos(self):
        return self._edit_area_cursor_pos

    def editAreaCursorPosToWidgetPos(self, edit_area_cursor_pos):
        return (edit_area_cursor_pos[0]+self.leftBorderWidth(), edit_area_cursor_pos[1])

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)
        self.update()

    def moveCursor(self, event):
        if self._document_model.isEmpty():
            return

        current_edit_area_pos = self.editAreaCursorPos()
        current_doc_pos = self.editAreaCursorToDocumentPos(current_edit_area_pos)
        current_surrounding_lines_length = []
        for line_num in [current_doc_pos[1]-1, current_doc_pos[1], current_doc_pos[1]+1]:
            if self._document_model.hasLine(line_num):
                current_surrounding_lines_length.append(self._document_model.lineLength(line_num))
            else:
                current_surrounding_lines_length.append(None)

        mode_offset = 1 if self._view_model.editorMode() == INSERT_MODE else 0

        key = event.key()
        if key == videtoolkit.Key.Key_Up:
            if current_surrounding_lines_length[0] is None:
                return
            new_pos = (min(current_edit_area_pos[0], current_surrounding_lines_length[0]+mode_offset),
                       max(self._edit_area_cursor_pos[1]-1, 0)
                      )
        elif key == videtoolkit.Key.Key_Down:
            if current_surrounding_lines_length[2] is None:
                return
            new_pos = (min(current_edit_area_pos[0], current_surrounding_lines_length[0]+mode_offset),
                       min(self._edit_area_cursor_pos[1]+1, self.editableAreaHeight()-1)
                      )

        elif key == videtoolkit.Key.Key_Left:
            new_pos = (max(self._edit_area_cursor_pos[0]-1,0), self._edit_area_cursor_pos[1])
        elif key == videtoolkit.Key.Key_Right:
            new_pos = (min(self._edit_area_cursor_pos[0]+1,
                           current_surrounding_lines_length[1]+mode_offset,
                           self.editableAreaWidth()-1),
                       self._edit_area_cursor_pos[1]
                       )


        self._edit_area_cursor_pos = new_pos
        new_doc_pos = self.editAreaCursorToDocumentPos(new_pos)
        self._status_bar.setPosition(*new_doc_pos)
        gui.VCursor.setPos(
                            *self.mapToGlobal(
                                *self.editAreaCursorPosToWidgetPos(new_pos)
                             )
                        )

    def lineNumberWidth(self):
        num_digits = int(math.log10(self._document_model.numLines()))+1
        return num_digits

    def leftBorderWidth(self):
        return self.lineNumberWidth()+self.badgeAreaWidth()+1

    def badgeAreaWidth(self):
        return 1

    def viewModelChanged(self):
        self.update()

    def editableAreaHeight(self):
        return self.height()-1

    def editableAreaWidth(self):
        return self.width()-self.leftBorderWidth()

