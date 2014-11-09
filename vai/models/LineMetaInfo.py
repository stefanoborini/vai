from vaitk import core
import collections
import copy
from ..Debug import log

# New class to store meta information in a separate
# object, so that we can listen to specific notifications
# from specific meta objects. We need to keep it synchronized
# to the current document though.
class LineMetaInfo:
    def __init__(self, meta_type, document):
        self._meta_type = meta_type
        self._document = document
        self._data = [None] * self._document.numLines()

        self.contentChanged = core.VSignal(self)

    def numLines(self):
        return len(self._data)

    # Meant to be called by document.
    def addLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.insert(line_number-1, None)

    # Meant to be called by document.
    def deleteLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.pop(line_number-1)

    def setData(self, data, from_line=1):
        # As a method, so we can bind to it via signal/slot. Property with slice needed.
        if not isinstance(data, collections.Iterable) or isinstance(data, str):
            data = [ data ]

        try:
            for idx, d in enumerate(data):
                self._data[from_line-1+idx] = d
        except IndexError:
            pass

        self.notifyObservers()

    def setDataForLines(self, data_dict):
        for k, v in data_dict.items():
            self._data[k-1] = v

        self.notifyObservers()

    def data(self, from_line=None, how_many=None):
        if from_line is not None:
            if how_many is None:
                return self._data[from_line-1]
            else:
                return self._data[from_line-1:from_line-1+how_many]
        else:
            if how_many is None:
                return self._data
            else:
                return self._data[:how_many]

    def notNoneData(self):
        return { i+1: v for i,v in enumerate(self._data) if v is not None}

    def dataForLines(self, lines):
        log("XXX")
        log(lines)
        log(self._data)
        log("YYYXXX")
        return {i: self._data[i-1] for i in lines}

    def clear(self):
        self._data = [None] * self._document.numLines()
        self.notifyObservers()

    def notifyObservers(self):
        self.contentChanged.emit()

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def document(self):
        return self._document

    def memento(self, line):
        return copy.deepcopy(self._data[line-1])

    def insertFromMemento(self, line, memento):
        self._data.insert(line-1, copy.deepcopy(memento))
        self.notifyObservers()

    def replaceFromMemento(self, line, memento):
        self._data[line-1] = copy.deepcopy(memento)
        self.notifyObservers()


