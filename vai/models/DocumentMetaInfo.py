from vaitk import core

class DocumentMetaInfo:
    """
    Information holder for meta information about the document as a whole.
    """
    def __init__(self, meta_type, document, data=None):
        """
        Initializes the meta info.
        Not publicly used. There's a factory method on the TextDocument.

        Args:
            meta_type (str) : A descriptive identifier string (e.g. CreationTime)
            document (TextDocument) : the associated TextDocument instance.
            data (Any, default None) : the value of the meta information.
        """

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
