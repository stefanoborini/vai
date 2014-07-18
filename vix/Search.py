def find(buffer, text):
    document = buffer.document()
    cursor = buffer.documentCursor()

    pos = cursor.pos()

    # -1 for indexing, +1 for skip current position
    starting_column = pos[1]
    for line_num in range(pos[0], document.numLines()+1):
        index = document.lineText(line_num).find(text, starting_column)
        if index != -1:
            cursor.toPos((line_num, index+1))
            return True

        starting_column = 0


    for line_num in range(1, pos[0]):
        index = document.lineText(line_num).find(text, starting_column)
        if index != -1:
            cursor.toPos((line_num, index+1))
            return True

    return False

