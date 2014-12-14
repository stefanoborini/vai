class EditorMode:
    """
    Separate enum class to hold the current editor mode
    """
    COMMAND = 0         # Normal, command mode, waiting for something to happen
    COMMAND_INPUT = 1   # When : has been pressed
    INSERT = 2          # When in insert mode you can type in the document.
    REPLACE = 3         # Single place replacement for r<char>
    VISUAL_BLOCK = 4    # For visual block mode (selection). Not yet used.
    VISUAL_LINE = 5     # For visual line mode (selection). Not yet used.
    VISUAL = 6          # For visual char mode (selection). Not yet used.
    DELETE = 7          # When d has been pressed and waiting for specification on what to delete
    SEARCH_FORWARD = 8  # When / has been pressed
    SEARCH_BACKWARD = 9 # When ? has been pressed
    GO = 10             # When g is pressed and it's waiting for the second g to go at BOF
    YANK = 11           # When y has been pressed and waiting for the second y.
    ZETA = 12           # When capital Z has been pressed and waiting for the second Z
    BOOKMARK = 13       #

