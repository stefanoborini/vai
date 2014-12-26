from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from .JoinWithNextLineCommand import JoinWithNextLineCommand

TAB_SPACE = 4

class DeleteSingleCharCommand(BufferCommand):
    def execute(self):
        document = self._document
        cursor = self._cursor

        if self.savedCursorPos() is None:
            self.saveCursorPos()
        
        pos = self.savedCursorPos()
        cursor.toPos(pos)

        if pos == (1,1):
            return CommandResult(success=False, info=None)

        if pos[1] == 1:
            cursor.toPos( (pos[0]-1, document.lineLength(pos[0]-1)) )
            command = JoinWithNextLineCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
                return CommandResult(True, '\n')
            else:
                return CommandResult(False, None)

        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)

        line_meta = document.lineMetaInfo("Change")
        changed = line_meta.data(pos[0])
        if changed is None:
            line_meta.setData("modified", pos[0])

        # Check if we can remove a tab. These are the tab positions:
        # 123456789
        # T   T   T

        # Get the tab position we can go to, and how many character we need to remove
        # to get there. If we are exactly on a tab position, remove a tab from the last
        # available tab position and add a full tab spacing to potentially remove.
        # FIXME this code's math is ugly. maybe we can simplify it?
        last_tab_pos = 1+int((pos[1]-1)/TAB_SPACE)*TAB_SPACE
        how_many = pos[1]-last_tab_pos
        if last_tab_pos > 1 and how_many == 0:
            how_many = TAB_SPACE
            last_tab_pos = last_tab_pos - TAB_SPACE

        # Check if the candidate removal is only spaces. If yes, then we can remove
        # the whole bunch, otherwise revert back to single char deletion.
        text = document.lineText(pos[0])
        if len(text[last_tab_pos-1:last_tab_pos-1+how_many].strip(' ')) != 0:
            how_many = 1

        deleted = document.deleteChars( (pos[0], pos[1]-how_many), how_many)
        cursor.toPos((pos[0], pos[1]-how_many))

        return CommandResult(success=True, info=deleted)

