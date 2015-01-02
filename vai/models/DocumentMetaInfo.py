from vaitk import core

class DocumentMetaInfo:
    def __init__(self, meta_type, document, data=None):
        self._meta_type = meta_type
        self._document = document
        self._data = data
        self.contentChanged = core.VSignal(self)

    def setData(self, data):
        if self._data != data:
            self._data = data
            self.notifyObservers()

    def data(self):
        return self._data

    def clear(self):
        if self._data is not None:
            self._data = None
            self.notifyObservers()

    def notifyObservers(self):
        self.contentChanged.emit()

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def document(self):
        return self._document

    def __str__(self):
        return str(self._data)
