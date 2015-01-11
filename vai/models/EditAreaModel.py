from vaitk import core

class EditAreaModel(core.VObject):
    """
    Model defining data pertinent to the Edit Area View.
    """
    def __init__(self):
        super().__init__()
        self._document_pos_at_top = (1,1)
        self.documentPosAtTopChanged = core.VSignal(self)

    @property
    def document_pos_at_top(self):
        """The document position (in document index) in the top-left corner of the editor"""
        return self._document_pos_at_top

    @document_pos_at_top.setter
    def document_pos_at_top(self, doc_pos):
        if doc_pos[0] < 1 or doc_pos[1] < 1:
            raise ValueError("document pos cannot be < 1")

        self._document_pos_at_top = doc_pos
        self.documentPosAtTopChanged.emit()
