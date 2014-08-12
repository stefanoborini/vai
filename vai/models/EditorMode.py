class EditorMode:
    """
    Separate enum class to hold the current editor mode
    """
    COMMAND = 0
    COMMAND_INPUT = 1
    INSERT = 2
    REPLACE = 3
    VISUAL_BLOCK = 4
    VISUAL_LINE = 5
    VISUAL = 6
    DELETE = 7
    SEARCH_FORWARD = 8
    SEARCH_BACKWARD = 9
    GO = 10
    YANK = 11

