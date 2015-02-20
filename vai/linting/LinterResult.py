import collections

LinterResult = collections.namedtuple("LinterResult", ["filename", "line", "column", "level", "message"])
