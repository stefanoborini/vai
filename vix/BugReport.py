def report():
    print("Apologies. Vix has crashed. ")
    print("A traceback report of the error has been created in vix_crashreport.log")

    print("Would you like to send a bug report to the development team?")
    print("The bug report will not contain information about your document content.")
    if yes():
        print("Sending traceback to developers")
        print("Sending unsuccessful. Feature not implemented")


def yes():
    y_or_n = input("[y/N]> ")
    if y_or_n.strip().lower() in ['y','yes']:
        return True
    return False


