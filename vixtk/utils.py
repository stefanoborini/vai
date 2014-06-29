
def strformat(strings_at, length):
    """
    Returns a string of given length, composed by strings at specified
    positions, as specified by strings_at. The rest is filled with spaces.
    strings_at is a list of tuples of two elements, the first a number,
    the second a string.
    """

    res = ""
    for pos, string in sorted(strings_at, key=lambda x: x[0]):
        res = res[:pos]
        res += " "* (pos - len(res))
        res += string

    res = res[:length]
    res += " "* (length - len(res))
    return res

def clamp(value, minvalue, maxvalue):
    """
    Returns the value, clamped between min and max value
    if outside that range
    """
    return sorted([minvalue, value, maxvalue])[1]
