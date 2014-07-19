def find(buffer, text, backwards=False):
    document = buffer.document()
    cursor = buffer.documentCursor()

    pos = cursor.pos()

    # -1 for indexing, +1 for skip current position

    if backwards is False:
        intervals = [(pos[0], document.numLines()+1), (1, pos[0])]
        starting_column = pos[1]
        ending_column = None
    else:
        intervals = [(pos[0], 0, -1), (document.numLines(), pos[0]-1, -1)]
        starting_column = None
        ending_column = pos[1]-1


    for line_num in range(*intervals[0]):
        index = document.lineText(line_num).find(text, starting_column, ending_column)
        if index != -1:
            cursor.toPos((line_num, index+1))
            return True

        starting_column = 0

    for line_num in range(*intervals[1]):
        index = document.lineText(line_num).find(text)
        if index != -1:
            cursor.toPos((line_num, index+1))
            return True

    return False

