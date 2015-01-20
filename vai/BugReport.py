import contextlib

def report(saved_files):
    print("Apologies. Vai has crashed.")
    print("---------------------------")
    with contextlib.closing(open("vai_crashreport.out")) as f:
        print(f.read())

    print("---------------------------")
    if len(saved_files) != 0:
        print("Your buffers have been dumped to the following files")
        print("")
        for f in saved_files:
            print("  "+str(f))
    print("")
    print("The traceback has been saved in vai_crashreport.out")


def yes():
    y_or_n = input("[y/N]> ")
    if y_or_n.strip().lower() in ['y','yes']:
        return True
    return False


