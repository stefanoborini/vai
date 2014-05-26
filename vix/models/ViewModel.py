from vixtk import core
from .. import flags
from ..positions import DocumentPos

class ViewModel(core.VObject):
    def __init__(self):
        super(ViewModel, self).__init__()
        self._document_pos_at_top = DocumentPos(1,1)
        self.documentPosChanged = core.VSignal(self)

    def documentPosAtTop(self):
        return self._document_pos_at_top

    def setDocumentPosAtTop(self, doc_pos):
        self._document_pos_at_top = doc_pos
        self.documentPosChanged.emit()

