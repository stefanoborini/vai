class SideRulerController(object):
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler
        self._view_model = None

    def setModel(self, view_model):
        if self._view_model:
            self._view_model.documentPosChanged.disconnect(self.updateRange)

        self._view_model = view_model
        self._view_model.documentPosChanged.connect(self.updateRange)
        self.updateRange()

    def updateRange(self):
        if self._view_model:
            top_pos = self._view_model.documentPosAtTop()
            self._side_ruler.setStart(top_pos.row)




