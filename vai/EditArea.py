import vixtk
from vixtk import gui, core, utils
from .EditAreaController import EditAreaController
from . import flags
from .models.TextDocument import CharMeta
from . import Search

from pygments import token

TOKEN_TO_COLORS = {
    token.Keyword:              (gui.VGlobalColor.yellow, None),
    token.Keyword.Constant:     (gui.VGlobalColor.red, None),
    token.Keyword.Pseudo:       (gui.VGlobalColor.red, None),
    token.Keyword.Namespace:    (gui.VGlobalColor.magenta, None),
    token.Keyword.Reserved:     (gui.VGlobalColor.magenta, None),
    token.Keyword.Type:         (gui.VGlobalColor.magenta, None),
    token.Comment:              (gui.VGlobalColor.cyan, None),
    token.Comment.Single:       (gui.VGlobalColor.cyan, None),
    token.Name.Function:        (gui.VGlobalColor.cyan, None),
    token.Name.Class:           (gui.VGlobalColor.cyan, None),
    token.String:               (gui.VGlobalColor.red, None),
    token.Literal:              (gui.VGlobalColor.red, None),
    token.Literal.String.Doc:   (gui.VGlobalColor.red, None),
    token.Number:               (gui.VGlobalColor.red, None),
    token.Number.Integer:       (gui.VGlobalColor.red, None),
    token.Number.Float:         (gui.VGlobalColor.red, None),
    token.Number.Hex:           (gui.VGlobalColor.red, None),
    token.Number.Oct:           (gui.VGlobalColor.red, None),
    token.Operator.Word:        (gui.VGlobalColor.yellow, None),
    token.Name.Decorator:       (gui.VGlobalColor.blue, None),
    token.Name.Builtin.Pseudo:  (gui.VGlobalColor.cyan, None),
}

class EditArea(gui.VWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._controller = EditAreaController(self)

        self._buffer = None
        self._editor_model = None
        self._visual_cursor_pos = (0,0)
        self.setFocusPolicy(vixtk.FocusPolicy.StrongFocus)

        self.cursorPositionChanged = core.VSignal(self)

    def setModels(self, buffer, editor_model):
        self._buffer = buffer
        self._editor_model = editor_model
        self._controller.setModels(buffer, editor_model)
        self.update()

    def paintEvent(self, event):
        w, h = self.size()
        pos_at_top = self._buffer.editAreaModel().documentPosAtTop()
        visible_line_interval = (pos_at_top[0], pos_at_top[0]+h)
        cursor_pos = self._buffer.documentCursor().pos()
        document = self._buffer.document()

        painter = gui.VPainter(self)
        painter.erase()

        if not self._hasModels():
            return

        # Find the current hovered word to set highlighting
        current_word, current_word_pos = self._buffer.document().wordAt(cursor_pos)
        word_entries = []
        if current_word_pos is not None:
            # find all the words only in the visible area
            word_entries = Search.findAll(self._buffer.document(),
                                          current_word,
                                          line_interval=visible_line_interval,
                                          word=True)


        for visual_line_num, doc_line_num in enumerate(range(*visible_line_interval)):
            if doc_line_num > self._buffer.document().numLines():
                continue

            # Get the relevant text
            line_text = document.lineText(doc_line_num)[pos_at_top[1]-1:]
            painter.drawText( (0, visual_line_num), line_text.replace('\n', ' '))

            # Apply colors. First through the Lexer designation
            char_meta = document.charMeta( (doc_line_num,1))
            colors = [TOKEN_TO_COLORS.get(tok, (None, None)) for tok in char_meta.get(CharMeta.LexerToken, [])]

            # Then, if there's a word, replace (None, None) entries with the highlight color
            word_entries_for_line = [x[1] for x in word_entries if x[0] == doc_line_num]
            for word_start in word_entries_for_line:
                for pos in range(word_start-1, word_start-1+len(current_word)):
                    if colors[pos] == (None, None):
                        colors[pos] = (gui.VGlobalColor.red, None)

            painter.recolor((0, visual_line_num), colors[pos_at_top[1]-1:])

        self._setVisualCursorPos((cursor_pos[1]-pos_at_top[1], cursor_pos[0]-pos_at_top[0] ))

    def visualCursorPos(self):
        return self._visual_cursor_pos

    def scrollDown(self):
        if not self._hasModels():
            return
        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        if top_pos[0] + self.height() > self._buffer.document().numLines():
            return
        new_pos = (top_pos[0]+1, top_pos[1])
        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollUp(self):
        if not self._hasModels():
            return
        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        if top_pos[0] == 1:
            return

        new_pos = (top_pos[0]-1, top_pos[1])
        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollPageUp(self):
        if not self._hasModels():
            return

        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        new_pos = (top_pos[0]-self.height()+2, top_pos[1])
        if new_pos[0] < 1:
           new_pos = (1, top_pos[1])

        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollPageDown(self):
        if not self._hasModels():
            return

        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        new_pos = (top_pos[0]+self.height()-2, top_pos[1])
        if new_pos[0] > self._buffer.document().numLines():
            new_pos = (self._buffer.document().numLines(),  top_pos[1])

        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollPageLeft(self):
        if not self._hasModels():
            return

        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        new_pos = (top_pos[0], top_pos[1]-int(self.width()/2))
        if new_pos[1] < 1:
           new_pos = (top_pos[0], 1)

        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def scrollPageRight(self):
        if not self._hasModels():
            return

        top_pos = self._buffer.editAreaModel().documentPosAtTop()
        new_pos = (top_pos[0], top_pos[1]+int(self.width()/2))

        self._buffer.editAreaModel().setDocumentPosAtTop(new_pos)
        self.update()

    def keyEvent(self, event):
        if not self._hasModels():
            return
        self._controller.handleKeyEvent(event)
        self.update()

    def focusInEvent(self, event):
        if not self._hasModels():
            return
        gui.VCursor.setPos(self.mapToGlobal((self._visual_cursor_pos[0], self._visual_cursor_pos[1])))

    def ensureCursorVisible(self):
        # There are multiple zones where the cursor can be, and the behavior is
        # different depending where the cursor is relative to the viewport area.
        # if the cursor is within 1 position above or below the visible area,
        # then it should scroll one line.
        # In all other cases (horizontal, and vertical distant) it should jump.

        doc_cursor_pos = self._buffer.documentCursor().pos()
        top_pos = self._buffer.editAreaModel().documentPosAtTop()

        new_top_pos = top_pos
        # Check and adjust the vertical positioning

        if doc_cursor_pos[0] == top_pos[0] - 1:
            # Cursor is just outside the top border, scroll one
            new_top_pos = (top_pos[0]-1, top_pos[1])
        elif doc_cursor_pos[0] == top_pos[0] + self.height():
            new_top_pos = (top_pos[0]+1, top_pos[1])
        elif doc_cursor_pos[0] < top_pos[0] - 1 \
            or doc_cursor_pos[0] > top_pos[0] + self.height():
            # Cursor is far away. Put the line in the center
            new_top_pos = (doc_cursor_pos[0]-int(self.height()/2), new_top_pos[1])

        # Now check horizontal positioning. This is easier because
        # We never scroll 1
        if doc_cursor_pos[1] < top_pos[1] or \
            doc_cursor_pos[1] > top_pos[1] + self.width():
            new_top_pos = (new_top_pos[0], doc_cursor_pos[1] - int(self.width()/2))

        #
        new_top_pos = ( max(1, new_top_pos[0]), new_top_pos[1])
        self._buffer.editAreaModel().setDocumentPosAtTop(new_top_pos)
        self.update()


    def handleDirectionalKey(self, event):
        # XXX move to controller?
        if not self._hasModels():
            return

        if self._buffer.document().isEmpty():
            return

        key = event.key()

        direction = { vixtk.Key.Key_Up:       flags.UP,
                      vixtk.Key.Key_Down:     flags.DOWN,
                      vixtk.Key.Key_Left:     flags.LEFT,
                      vixtk.Key.Key_Right:    flags.RIGHT,
                      vixtk.Key.Key_PageUp:   flags.PAGE_UP,
                      vixtk.Key.Key_PageDown: flags.PAGE_DOWN,
                      vixtk.Key.Key_Home:     flags.HOME,
                      vixtk.Key.Key_End:      flags.END,
                    }[key]

        self.moveCursor(direction)

    def moveCursor(self, direction):
        doc_cursor = self._buffer.documentCursor()

        if direction == flags.UP:
            if self._visual_cursor_pos[1] == 0:
                self.scrollUp()
            doc_cursor.toLinePrev()
        elif direction == flags.DOWN:
            if self._visual_cursor_pos[1] == self.height()-1:
                self.scrollDown()
            doc_cursor.toLineNext()
        elif direction == flags.LEFT:
            if self._visual_cursor_pos[0] == 0:
                self.scrollPageLeft()
            doc_cursor.toCharPrev()
        elif direction == flags.RIGHT:
            if self._visual_cursor_pos[0] == self.width()-1:
                self.scrollPageRight()
            doc_cursor.toCharNext()
        elif direction == flags.END:
            doc_cursor.toLineEnd()
        elif direction == flags.HOME:
            doc_cursor.toLineBeginning()
        elif direction == flags.PAGE_UP:
            self.scrollPageUp()
            doc_cursor.toLine(self._buffer.editAreaModel().documentPosAtTop()[0])
        elif direction == flags.PAGE_DOWN:
            self.scrollPageDown()
            doc_cursor.toLine(self._buffer.editAreaModel().documentPosAtTop()[0])
        else:
            raise Exception("Unknown direction flag %s", str(direction))

    # Private

    def _hasModels(self):
        return self._buffer and self._editor_model

    def _setVisualCursorPos(self, cursor_pos):
        pos_x = utils.clamp(cursor_pos[0], 0, self.width()-1)
        pos_y = utils.clamp(cursor_pos[1], 0, self.height()-1)
        self._visual_cursor_pos = (pos_x, pos_y)
        gui.VCursor.setPos(self.mapToGlobal((pos_x, pos_y)))
