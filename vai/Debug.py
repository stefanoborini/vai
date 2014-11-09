def log(message):
    with open("vai.log", "a") as f:
        f.write(str(message)+'\n')

