import contextlib

def report():
    print("Apologies. Vai has crashed.")
    print("---------------------------")
    with contextlib.closing(open("vai_crashreport.out")) as f:
        print(f.read())

    print("---------------------------")
    print("The traceback has been saved in vai_crashreport.out")

    #print("Would you like to send a bug report to the development team?")
    #print("The bug report will not contain information about your document content.")
    #if yes():
        #print("Sending traceback to developers")
        #print("Sending unsuccessful. Feature not implemented")


def yes():
    y_or_n = input("[y/N]> ")
    if y_or_n.strip().lower() in ['y','yes']:
        return True
    return False


