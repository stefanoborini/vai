from vaitk import core

class EditAreaModel(core.VObject):
    def __init__(self):
        super().__init__()
        self._document_pos_at_top = (1,1)
        self.documentPosChanged = core.VSignal(self)

    @property
    def document_pos_at_top(self):
        return self._document_pos_at_top

    @document_pos_at_top.setter
    def document_pos_at_top(self, doc_pos):
        if doc_pos[0] < 1 or doc_pos[1] < 1:
            raise ValueError("document pos cannot be < 1")

        self._document_pos_at_top = doc_pos
        self.documentPosChanged.emit()
