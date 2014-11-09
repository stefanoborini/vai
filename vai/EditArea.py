import vaitk
from vaitk import gui, core, utils
from . import controllers
from .models.TextDocument import CharMeta
from .DefaultColorSchema import DefaultColorSchema
from . import Search



class EditArea(gui.VWidget):
    def __init__(self, global_state, editor_controller, parent):
        super().__init__(parent)
        self._buffer = None

        self._controller = controllers.EditAreaController(self, global_state, editor_controller)
        self._color_schema = DefaultColorSchema()

        self._visual_cursor_pos = (0,0)
        self.setFocusPolicy(vaitk.FocusPolicy.StrongFocus)

    # properties
    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            raise Exception("Cannot set buffer to None")

        self._buffer = buffer
        self._controller.buffer = buffer

    @property
    def visual_cursor_pos(self):
        return self._visual_cursor_pos

    @visual_cursor_pos.setter
    def visual_cursor_pos(self, cursor_pos):
        pos_x = utils.clamp(cursor_pos[0], 0, self.width()-1)
        pos_y = utils.clamp(cursor_pos[1], 0, self.height()-1)
        self._visual_cursor_pos = (pos_x, pos_y)
        gui.VCursor.setPos(self.mapToGlobal((pos_x, pos_y)))

    def paintEvent(self, event):
        painter = gui.VPainter(self)
        painter.erase()

        buffer = self._buffer
        if buffer is None:
            return

        w, h = self.size()
        pos_at_top = buffer.edit_area_model.document_pos_at_top
        visible_line_interval = (pos_at_top[0], pos_at_top[0]+h)
        cursor_pos = buffer.cursor.pos
        document = buffer.document

        # Find the current hovered word to set highlighting
        current_word, current_word_pos = document.wordAt(cursor_pos)
        word_entries = []
        if current_word_pos is not None:
            # find all the words only in the visible area
            word_entries = Search.findAll(document,
                                          current_word,
                                          line_interval=visible_line_interval,
                                          word=True)


        for visual_line_num, doc_line_num in enumerate(range(*visible_line_interval)):
            if doc_line_num > document.numLines():
                continue

            # Get the relevant text
            line_text = document.lineText(doc_line_num)[pos_at_top[1]-1:]
            line_text.replace('\n', ' ')

            # Apply colors. First through the Lexer designation
            colors = [(None, None)]*len(line_text)

            # Add markers for the indentation
            indent_spaces = len(line_text)-len(line_text.lstrip())
            for i in range(5, indent_spaces, 4):
                line_text = line_text[:i-1]+'.'+line_text[i:]

            char_meta = document.charMeta( (doc_line_num,1))
            if CharMeta.LexerToken in char_meta:
                colors = [self._color_schema.COLORMAP[tok] for tok in char_meta.get(CharMeta.LexerToken)]

            for i in range(5, indent_spaces, 4):
                colors[i-1] = (gui.VGlobalColor.blue, None)

            # Then, if there's a word, replace (None, None) entries with the highlight color
            word_entries_for_line = [x[1] for x in word_entries if x[0] == doc_line_num]
            for word_start in word_entries_for_line:
                for pos in range(word_start-1, word_start-1+len(current_word)):
                    if colors[pos] == (None, None):
                        colors[pos] = (gui.VGlobalColor.red, None)

            painter.drawText( (0, visual_line_num), line_text.replace('\n', ' '))
            painter.recolor((0, visual_line_num), colors[pos_at_top[1]-1:])

        self.visual_cursor_pos = (cursor_pos[1]-pos_at_top[1], cursor_pos[0]-pos_at_top[0])

    def keyEvent(self, event):
        self._controller.handleKeyEvent(event)

    def focusInEvent(self, event):
        gui.VCursor.setPos(self.mapToGlobal((self._visual_cursor_pos[0], self._visual_cursor_pos[1])))

