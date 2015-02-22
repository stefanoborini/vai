def log(message):
    """
    Writes a message out in a log file.
    Use this to do printing while debugging, as you can't print while ncurses takes over the screen.
    """
    with open("vai.log", "a") as f:
        f.write(str(message)+'\n')

