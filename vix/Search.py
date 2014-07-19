from . import flags

def find(buffer, text, direction):
    document = buffer.document()
    cursor = buffer.documentCursor()

    pos = cursor.pos()

    current_line, current_col = pos

    if direction == flags.FORWARD:
        first_half, second_half = ((pos[0], document.numLines()+1), (1, pos[0]+1))
        find_routine = "find"
    else:
        first_half, second_half = ((pos[0], 0, -1), (document.numLines(), pos[0]-1, -1))
        find_routine = "rfind"


    for line_num in range(*first_half):
        start, stop = (None, None)
        if line_num == current_line:
            start, stop = (current_col, None) if direction == flags.FORWARD else (None, current_col)

        index = getattr(document.lineText(line_num), find_routine)(text, start, stop)
        if index != -1 and index:
            cursor.toPos((line_num, index+1))
            return True

    # Reached the end, start from the other side
    for line_num in range(*second_half):
        start, stop = (None, None)
        if line_num == current_line:
            start, stop = (None, current_col) if direction == flags.FORWARD else (current_col, None)

        index = getattr(document.lineText(line_num), find_routine)(text, start, stop)

        if index != -1:
            cursor.toPos((line_num, index+1))
            return True

    return False

