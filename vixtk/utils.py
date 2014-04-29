def strformat(strings_at, length):
    res = ""
    for pos, string in sorted(strings_at,key=lambda x: x[0]):
        res = res[:pos]
        res += " "* (pos - len(res))
        res += string

    res = res[:length]
    res += " "* (length - len(res))
    return res
